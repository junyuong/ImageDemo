from tkinter import *
from tkinter.filedialog import *
from tkinter.simpledialog import *
from PIL import ImageTk, Image, ImageFilter
import matplotlib.pyplot as plt
from pytesseract import *



import cv2
from matplotlib.image import imread
import numpy as np

## 전역 변수 선언 부분 ##
filename = ""
gImage = ""

## 함수 선언 부분 ##
def func_open():
    global filename  # 오픈한 이미지를 확대, 축소하기 위해 변수 공유
    filename = askopenfilename(parent=window, filetypes=
    (("jpg 파일", "*.jpg"), ("모든 파일", "*.*")))
    photo = ImageTk.PhotoImage(file=filename)
    pLabel.configure(image=photo)
    pLabel.image = photo

    image = cv2.imread(filename, cv2.IMREAD_GRAYSCALE)
    global gImage
    gImage = image


def func_exit():
    window.quit()
    window.destroy()


# def convert_to_tkimage():
#     image=cv2.imread(filename, cv2.IMREAD_GRAYSCALE)
#     ret,img_result1 = cv2.threshold(image, 127, 255, cv2.THRESH_BINARY)
#     im = Image.fromarray(img_result1)
#     imgtk = ImageTk.PhotoImage(image=im)

#     pLabel.configure(image = imgtk) # 윈도창에 나타내기
#     pLabel.image = imgtk

def Binary(self):
    image = cv2.imread(filename, cv2.IMREAD_GRAYSCALE)
    # image type is <class 'numpy.ndarray'>
    ret, img_result = cv2.threshold(image, binaryScale.get(), 255, cv2.THRESH_BINARY)
    # Convert the Image object into a TkPhoto object
    # img_result = cv2.resize(img_result, None, fx=0.5, fy=0.5, interpolation=cv2.INTER_CUBIC)
    im = Image.fromarray(img_result)
    # ocrImage = im
    imgtk = ImageTk.PhotoImage(image=im)
    # imgtk type is <class 'PIL.ImageTk.PhotoImage'>
    pLabel.configure(image=imgtk)  # 윈도창에 나타내기
    pLabel.image = imgtk
    global gImage
    gImage = img_result


def Adaptive(self):
    image = cv2.imread(filename, cv2.IMREAD_GRAYSCALE)
    # image type is <class 'numpy.ndarray'>
    img_result = cv2.adaptiveThreshold(image, AScale.get(), cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 5)
    # 맨 뒤에 파라미터 수정 필요.

    # Convert the Image object into a TkPhoto object
    im = Image.fromarray(img_result)
    # ocrImage = im
    imgtk = ImageTk.PhotoImage(image=im)
    # imgtk type is <class 'PIL.ImageTk.PhotoImage'>
    pLabel.configure(image=imgtk)  # 윈도창에 나타내기
    pLabel.image = imgtk
    global gImage
    gImage = img_result


def getOCR():
    text = image_to_string(gImage, lang="kor+eng")
    global pLabelTxt
    pLabelTxt.destroy()
    pLabelTxt = Label(rframe, text="")
    pLabelTxt = Label(lframe, text=text)
    pLabelTxt.grid(row=2, column=0)
    # pLabelTxt.pack(expand = 1, anchor = CENTER)


def saveImage():
    # "C:/AI/OCR/SO/S18MSO01010101ME000003.jpg"
    saveName = filename.split("/")
    # cv2.imwrite(filename+"_.jpg",gImage)
    print(gImage)
    print(filename)


## 메인 코드 부분 ##
window = Tk()
window.geometry("1200x1200")
window.title("이미지 데모 툴 : 김준영")

##좌, 우 프레임 구분을 위한 셋팅 부분##
lframe = tkinter.Frame(window, relief="solid", bd=2)
lframe.grid(row=0, column=0)
# lframe.pack(side="left", fill="both", expand=True)

rframe = tkinter.Frame(window, relief="solid", bd=2)
rframe.grid(row=0, column=1)
# rframe.pack(side="right", fill="both", expand=True)


ocr_button = tkinter.Button(rframe, text="OCR 변환", command=getOCR)
ocr_button.grid(row=2, column=1)
# ocr_button.pack(side="right", expand=True)

save_button = tkinter.Button(rframe, text="이미지저장", command=saveImage)
save_button.grid(row=3, column=1)

##################Binary Scale 영역##################
var = tkinter.IntVar()
binaryScaleTxt = Label(rframe, text="Binary")
binaryScaleTxt.grid(row=0, column=2)
binaryScale = tkinter.Scale(rframe, variable=var, command=Binary,
                            orient="horizontal", showvalue=True,
                            tickinterval=50, to=255, length=300, repeatinterval=100)
binaryScale.set(100)
binaryScale.grid(row=0, column=1)
##################Binary Scale 영역##################

##################Adaptive Thresold Scale 영역##################
var = tkinter.IntVar()
AScaleTxt = Label(rframe, text="Adaptive")
AScaleTxt.grid(row=1, column=2)
AScale = tkinter.Scale(rframe, variable=var, command=Adaptive,
                       orient="horizontal", showvalue=True,
                       tickinterval=50, to=255, length=300, repeatinterval=100)
AScale.set(100)
AScale.grid(row=1, column=1)
##################Binary Scale 영역##################


# scale.pack(side="right",expand=False)

photo = PhotoImage()
pLabel = Label(lframe, image=photo)
pLabel.grid(row=0, column=0)
# pLabel.pack(expand = 1, anchor = CENTER)
pLabelTxt = Label(window, text="")
pLabelTxt.grid(row=1, column=0)
# pLabelTxt.pack(expand = 1, anchor = CENTER)

mainMenu = Menu(window)
window.config(menu=mainMenu)

fileMenu = Menu(mainMenu)
mainMenu.add_cascade(label="파일", menu=fileMenu)
fileMenu.add_command(label="파일 열기", command=func_open)
fileMenu.add_separator()
fileMenu.add_command(label="프로그램 종료", command=func_exit)

## 이미지 효과 메뉴 추가하는 부분 ##
imageMenu = Menu(mainMenu)

window.mainloop()