from main import *
from threading import Thread
def run():
    output_result("E:/Emotion_rec/4dac1f7abf38e1887e3cf70b1516beaa.mp4")
    result = results()
    print(result1)

t1 = Thread(target = run())
t1.start()

