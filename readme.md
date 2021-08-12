# An End-to-End Visual-Audio Attention Network for Emotion Recognition DMOE

<!-- ### [Project Page](https://github.com/maysonma/VAANet) | [Paper](https://www.aiide.org/ojs/index.php/AAAI/article/view/5364)

Sicheng Zhao\*,
Yunsheng Ma\*,
Yang Gu,
Jufeng Yang,
Tengfei Xing,
Pengfei Xu,
Runbo Hu,
Hua Chai,
Kurt Keutzer<br>
\*denotes equal contribution -->

This is the demo implementation of the paper ["An End-to-End Visual-Audio Attention Network for Emotion Recognition in User-Generated Videos"](https://www.aiide.org/ojs/index.php/AAAI/article/view/5364). [NOT OFFICIAL!!]

## Citation 

If you use this code, please cite the following:
```bibtex
@inproceedings{Robin-WZQ,
  title={An End-to-End Visual-Audio Attention Network for Emotion Recognition in User-Generated Videos DEMO},
  author={Wang zhongqi, Wang Jianan,Li Tong},
  year={2021}
}
```

## Requirements
* [PyTorch](http://pytorch.org/) (ver. 0.4+ required)
* FFmpeg
* Python3
* AVL
* Pyqt5

## Preparation

### data（ve8）
* Download the videos [here](https://drive.google.com/drive/u/1/folders/0B5peJ1MHnIWGd3pFbzMyTG5BSGs).(offical)
* video pre-processing using ``` /tools/processing.py```(mp4 to jpg+ Add n_frames information + Generate annotation file in json format + mp4 to mp3)

### model
* pre-trained model download [here]
* trained model download [here]

## Running the code
Assume the strcture of data directories is the following:
```misc
~/
  data
    Joy/
      .../(video name)
        images/(jpg files)
        mp3/
          mp3/(mp3 file)
  results
  resnet-101-kinetics.pth
  save_30.pth
  ve8_01.json
  
```

Confirm all options in ```~/opts.py```.
```bash
python Emotion.py
```
