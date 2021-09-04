import wave
import pyaudio
import time


def record(p,stream,i,CHUNK,FORMAT,CHANNELS,RECORD_SECONDS,RATE,audio_path):
    '''实现声音的录制
    '''
    # 打开数据流
    WAVE_OUTPUT_FILENAME = audio_path+"output"+str(i)+".mp3"

    print("* recording")

    # 开始录音
    frames = []
    for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
        data = stream.read(CHUNK)
        frames.append(data)

    print("* done recording:",time.time())

    # 写入录音文件
    wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(p.get_sample_size(FORMAT))
    wf.setframerate(RATE)
    wf.writeframes(b''.join(frames))
    wf.close()

def audio_record():
    # 创建PyAudio对象
    # 定义数据流块
    CHUNK = 1024
    FORMAT = pyaudio.paInt16
    CHANNELS = 2
    RATE = 44100
    # 录音时间
    RECORD_SECONDS = 5

    p = pyaudio.PyAudio()
    stream = p.open(format=FORMAT,
            channels=CHANNELS,
            rate=RATE,
            input=True,
            frames_per_buffer=CHUNK)
    i=0
    while True:
        i+=1
        record(p,stream,i,CHUNK,FORMAT,CHANNELS,RECORD_SECONDS,RATE)
        if i==3:
            break

    # 停止数据流
    stream.stop_stream()
    stream.close()

    # 关闭PyAudio
    p.terminate()

if __name__ == "__main__":
    audio_record()