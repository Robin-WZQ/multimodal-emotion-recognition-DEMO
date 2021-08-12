# An End-to-End Visual-Audio Attention Network for Emotion Recognition in User-Generated Videos

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

This is the official implementation of the paper ["An End-to-End Visual-Audio Attention Network for Emotion Recognition in User-Generated Videos"](https://www.aiide.org/ojs/index.php/AAAI/article/view/5364).

## Citation 

If you use this code, please cite the following:
```bibtex
@inproceedings{Zhao2020AnEV,
  title={An End-to-End Visual-Audio Attention Network for Emotion Recognition in User-Generated Videos},
  author={Sicheng Zhao and Yunsheng Ma and Yang Gu and Jufeng Yang and Tengfei Xing and Pengfei Xu and Runbo Hu and Hua Chai and Kurt Keutzer},
  booktitle={AAAI},
  year={2020}
}
```

## Requirements
* [PyTorch](http://pytorch.org/) (ver. 0.4+ required)
* FFmpeg
* Python3

## Preparation

### VideoEmotion-8
* Download the videos [here](https://drive.google.com/drive/u/1/folders/0B5peJ1MHnIWGd3pFbzMyTG5BSGs).
* Convert from mp4 to jpg files using ```/tools/video2jpg.py```
* Add n_frames information using ```/tools/n_frames.py```
* Generate annotation file in json format using ```/tools/ve8_json.py```
* Convert from mp4 to mp3 files using ```/tools/video2mp3.py```

## Running the code
Assume the strcture of data directories is the following:
```misc
~/
  VideoEmotion8--imgs
    .../ (directories of class names)
      .../ (directories of video names)
        .../ (jpg files)
  VideoEmotion8--mp3
    .../ (directories of class names)
      .../ (mp3 files)
  results
  ve8_01.json
```

Confirm all options in ```~/opts.py```.
```bash
python main.py
```