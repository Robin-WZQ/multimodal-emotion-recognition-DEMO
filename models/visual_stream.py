import torch
import torch.nn as nn
import torchvision
from models.resnet import pretrained_resnet101


class VisualStream(nn.Module):
    def __init__(self,
                 snippet_duration,
                 sample_size,
                 n_classes,
                 seq_len,
                 pretrained_resnet101_path):
        super(VisualStream, self).__init__()
        self.snippet_duration = snippet_duration
        self.sample_size = sample_size
        self.n_classes = n_classes
        self.seq_len = seq_len
        self.ft_begin_index = 5
        self.pretrained_resnet101_path = pretrained_resnet101_path

        self._init_norm_val()
        self._init_hyperparameters()
        self._init_encoder()
        self._init_attention_subnets()
        self._init_params()

    def _init_norm_val(self):
        self.NORM_VALUE = 255.0
        self.MEAN = 100.0 / self.NORM_VALUE

    def _init_encoder(self):
        resnet, _ = pretrained_resnet101(snippet_duration=self.snippet_duration,
                                         sample_size=self.sample_size,
                                         n_classes=self.n_classes,
                                         ft_begin_index=self.ft_begin_index,
                                         pretrained_resnet101_path=self.pretrained_resnet101_path)

        children = list(resnet.children())
        self.resnet = nn.Sequential(*children[:-2])  # delete the last fc and the avgpool layer
        for param in self.resnet.parameters():
            param.requires_grad = False

    def _init_hyperparameters(self):
        self.hp = {
            'nc': 2048,
            'k': 512,
            'm': 16,
            'hw': 4
        }

    def _init_attention_subnets(self):
        self.conv0 = nn.Sequential(
            *[nn.Conv1d(self.hp['nc'], self.hp['k'], 1, bias=True),
              nn.BatchNorm1d(self.hp['k']),
              nn.ReLU()])

        self.sa_net = nn.ModuleDict({
            'conv': nn.Sequential(
                nn.Conv1d(self.hp['k'], 1, 1, bias=False),
                nn.BatchNorm1d(1),
                nn.Tanh(),
            ),
            'fc': nn.Linear(self.hp['m'], self.hp['m'], bias=False),
            'softmax': nn.Softmax(dim=1)
        })

        self.ta_net = nn.ModuleDict({
            'conv': nn.Sequential(
                nn.Conv1d(self.hp['k'], 1, 1, bias=False),
                nn.BatchNorm1d(1),
                nn.Tanh(),
            ),
            'fc': nn.Linear(self.seq_len, self.seq_len, bias=True),
            'relu': nn.ReLU()
        })

        self.cwa_net = nn.ModuleDict({
            'conv': nn.Sequential(
                nn.Conv1d(self.hp['m'], 1, 1, bias=False),
                nn.BatchNorm1d(1),
                nn.Tanh(),
            ),
            'fc': nn.Linear(self.hp['k'], self.hp['k'], bias=False),
            'softmax': nn.Softmax(dim=1)
        })

        self.fc = nn.Linear(self.hp['k'], self.n_classes)

    def _init_params(self):
        for subnet in [self.conv0, self.sa_net, self.ta_net, self.cwa_net, self.fc]:
            if subnet is None:
                continue
            for m in subnet.modules():
                self._init_module(m)
        self.ta_net['fc'].bias.data.fill_(1.0)

    def _init_module(self, m):
        if isinstance(m, nn.BatchNorm1d):
            m.weight.data.fill_(1)
            m.bias.data.zero_()
        elif isinstance(m, nn.Conv1d):
            nn.init.kaiming_normal_(m.weight, mode='fan_out')

    def forward(self, input: torch.Tensor):
        input = input.transpose(0, 1).contiguous()  # input.shape=[seq_len, batch, 3, 16, 112, 112]
        input.div_(self.NORM_VALUE).sub_(self.MEAN)

        seq_len, batch, nc, snippet_duration, sample_size, _ = input.size()
        input = input.view(seq_len * batch, nc, snippet_duration, sample_size, sample_size)
        with torch.no_grad():
            output = self.resnet(input)
            output = torch.squeeze(output, dim=2)
            output = torch.flatten(output, start_dim=2)
        F = self.conv0(output)  # [B x 512 x 16]

        Hs = self.sa_net['conv'](F)
        Hs = torch.squeeze(Hs, dim=1)
        Hs = self.sa_net['fc'](Hs)
        As = self.sa_net['softmax'](Hs)
        As = torch.mul(As, self.hp['m'])
        alpha = As.view(seq_len, batch, self.hp['m'])

        fS = torch.mul(F, torch.unsqueeze(As, dim=1).repeat(1, self.hp['k'], 1))

        G = fS.transpose(1, 2).contiguous()
        Hc = self.cwa_net['conv'](G)
        Hc = torch.squeeze(Hc, dim=1)
        Hc = self.cwa_net['fc'](Hc)
        Ac = self.cwa_net['softmax'](Hc)
        Ac = torch.mul(Ac, self.hp['k'])
        beta = Ac.view(seq_len, batch, self.hp['k'])

        fSC = torch.mul(fS, torch.unsqueeze(Ac, dim=2).repeat(1, 1, self.hp['m']))
        fSC = torch.mean(fSC, dim=2)
        fSC = fSC.view(seq_len, batch, self.hp['k']).contiguous()
        fSC = fSC.permute(1, 2, 0).contiguous()

        Ht = self.ta_net['conv'](fSC)
        Ht = torch.squeeze(Ht, dim=1)
        Ht = self.ta_net['fc'](Ht)
        At = self.ta_net['relu'](Ht)
        gamma = At.view(batch, seq_len)

        fSCT = torch.mul(fSC, torch.unsqueeze(At, dim=1).repeat(1, self.hp['k'], 1))
        fSCT = torch.mean(fSCT, dim=2)

        output = self.fc(fSCT)
        return output, alpha, beta, gamma
