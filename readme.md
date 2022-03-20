# An End-to-End Visual-Audio Attention Network for Emotion Recognition DEMO



This is the demo implementation of the paper ["An End-to-End Visual-Audio Attention Network for Emotion Recognition in User-Generated Videos"](https://www.aiide.org/ojs/index.php/AAAI/article/view/5364). [NOT OFFICIAL!!]

[Original Paper Project Page](https://github.com/maysonma/VAANet) | [Paper](https://www.aiide.org/ojs/index.php/AAAI/article/view/5364)


## Requirements
* [PyTorch](http://pytorch.org/) (ver. 0.4+ required)
* FFmpeg
* Python3
* AVL
* Pyqt5

## Preparation

### data（ve8）
* If U just want to use the DEMO, this step is not necessary. Download the pre-trained and trained model is enough.
* Download the videos [here](https://drive.google.com/drive/u/1/folders/0B5peJ1MHnIWGd3pFbzMyTG5BSGs).(offical)
* video pre-processing using ``` /tools/processing.py```(mp4 to jpg+ Add n_frames information + Generate annotation file in json format + mp4 to mp3)

* Here, We provide the processed dataset, including VideoEmotion8-imgs(splited by FFmpeg) and VideoEmotion8-videos, so that you can train your own model easier.

VideoEmotion8-imgs: [here](https://pan.baidu.com/s/1NjgHAfcIKJlCVUey07XIcg) (extraction code: fhom)

VideoEmotion8-videos: [here](https://pan.baidu.com/s/10xD218Ff1aGk42Pqe_Ladg) (extraction code: 7tn3)

### model
* resnet-101-kinetics.pth:  pre-trained model download [here](https://pan.baidu.com/s/1gi01VMev8WWwMGihdbI-Ow) (extraction code:0bi8)
* save_30.pth:  trained model download [here](https://pan.baidu.com/s/1qJGtjTwh3D90uUZCh0D5Jw) (extraction code:uq82)
* ve8_01.json: download [here](https://pan.baidu.com/s/1mjCgxD82J4ORn5BtzZOqcA) (extraction code:s567)

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

## Result
![图片2](https://user-images.githubusercontent.com/60317828/129351229-7cebb23c-c1dc-4c94-a84f-b0b3394573af.png)
See the next section for details.

## Tutorial
To see another branch:click here [--Tutorial](https://github.com/Robin-WZQ/multimodel-emotion-recongnition-DEMO/tree/main)
 
(Chinese version)
