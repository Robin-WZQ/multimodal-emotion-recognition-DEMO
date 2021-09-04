import cv2
import time
import cv2

def capture(i,j,my_camera,images_path):
    print("start capture")
    while(True):
        j+=1
        sucess,video_frame=my_camera.read()
        if(j%7==0):
            cv2.imwrite(images_path+'{:0>6d}.jpg'.format(int(j/7)),video_frame)
        if(j%56==0):
            break
    print("capture done:",time.time())

if __name__ == "__main__":
    my_camera = cv2.VideoCapture(0)
    i=0
    j=0
    capture(1,j,my_camera,"/data/")
