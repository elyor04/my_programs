from os import listdir
from os.path import isfile
from cv2 import imread, bilateralFilter
from keyboard import is_pressed
from time import sleep

img_path = ""

def searchImgPath(main_path: str) -> None:
    global img_path
    for vl in listdir(main_path):
        pth = f"{main_path}/{vl}"
        if not isfile(pth):
            try: searchImgPath(pth)
            except: pass
        else:
            if vl.endswith(".jpg") or vl.endswith(".png"):
                img_path = pth
        if img_path: return

searchImgPath("C:/Users")
img = imread(img_path)

print("YIG\'ISH BOSHLANDI")
img_list = [img for i in range(600000000)]
print("YIG\'ISH TUGADI")

while True:
    if is_pressed("ctrl+shift+q"):
        break
    bilateralFilter(img, 10, 20, 15)
    sleep(0.002)

del img_list
print("BARCHASI TOZALANDI")
