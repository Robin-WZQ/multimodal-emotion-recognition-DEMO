import random


class LoopPadding(object):

    def __init__(self, size):
        self.size = size

    def __call__(self, frame_indices):
        out = frame_indices

        for index in out:
            if len(out) >= self.size:
                break
            out.append(index)

        return out


class TemporalRandomCrop(object):
    """
    Temporally crop the given frame indices at a random location.
    If the number of frames is less than the size, loop the indices as many times as necessary.
    """

    def __init__(self, size, seed=0):
        self.size = size

    def __call__(self, frame_indices):
        rand_end = max(0, len(frame_indices) - self.size - 1)
        begin = random.randint(0, rand_end)
        end = min(begin + self.size, len(frame_indices))
        out = frame_indices[begin:end]
        for index in out:
            if len(out) >= self.size:
                break
            out.append(index)

        return out


class TemporalCenterCrop(object):
    """
    Temporally crop the given frame indices at the center.
    If the number of frames is less than the size, loop the indices as many times as necessary.
    """

    def __init__(self, size):
        self.size = size

    def __call__(self, frame_indices):
        center_index = len(frame_indices) // 2
        begin = max(0, center_index - (self.size // 2))
        end = min(begin + self.size, len(frame_indices))

        out = frame_indices[begin:end]
        for index in out:
            if len(out) >= self.size:
                break
            out.append(index)
        return out


class TSN(object):
    def __init__(self, seq_len=12, snippet_duration=16, center=False):
        self.seq_len = seq_len
        self.snippets_duration = snippet_duration
        self.crop = TemporalRandomCrop(size=self.snippets_duration) if center == False else TemporalCenterCrop(size=self.snippets_duration)

    def __call__(self, frame_indices):
        snippets = []
        pad = LoopPadding(size=self.seq_len * self.snippets_duration)
        frame_indices = pad(frame_indices)
        num_frames = len(frame_indices)
        segment_duration = num_frames // self.seq_len
        assert segment_duration >= self.snippets_duration

        # crop = TemporalRandomCrop(size=self.snippets_duration)
        for i in range(self.seq_len):
            snippets.append(self.crop(frame_indices[segment_duration * i: segment_duration * (i + 1)]))
        return snippets
