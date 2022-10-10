from msilib.schema import ListBox
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from random import *
from tkinter import *
import requests
import json

driver = webdriver.Chrome('.\Lotto\chromedriver.exe')
driver.get("https://dhlottery.co.kr/gameResult.do?method=byWin")
elem = driver.find_element(By.XPATH, "//*[@id=\"article\"]/div[2]/div/div[2]/h4/strong")

draw_count = int(elem.text[0:len(elem.text)-1])
url = "https://www.dhlottery.co.kr/common.do?method=getLottoNumber&drwNo="
drawlist = list()

i = 0

while len(drawlist) < 2:
    r = requests.get(url + str(draw_count - i))
    result = r.json()
    no = list()
    no.append(int(result['drwtNo1']))
    no.append(int(result['drwtNo2']))
    no.append(int(result['drwtNo3']))
    no.append(int(result['drwtNo4']))
    no.append(int(result['drwtNo5']))
    no.append(int(result['drwtNo6']))
    drawlist.append(no)
    i += 1

print(drawlist)
driver.close()

winlist = list()

# 랜덤 번호 5개
def lotto_num1():
    while len(winlist) < 5:
        no1 = list()
        while len(no1) < 6:
            i = randint(1, 45)
            no1.append(i)
            if no1.count(i) > 1: # 같은번호 제거
                no1.pop()

        no1.sort()
        winlist.append(no1)
 
# 바로 전 1회차 번호는 빼고 5개
def lotto_num2():
    while len(winlist) < 5:
        no1 = list()
        while len(no1) < 6:
            i = randint(1, 45)
            if i in drawlist[0]: # 바로 이전 번호 스킵
                continue
            no1.append(i)
            if no1.count(i) > 1: # 같은번호 제거
                no1.pop()
        
        no1.sort()
        winlist.append(no1)
        

# 바로 전 2회차 번호는 빼고
def lotto_num3():
    while len(winlist) < 5:
        no1 = list()
        while len(no1) < 6:
            i = randint(1, 45)
            if i in drawlist[0]:
                continue
            if i in drawlist[1]:
                continue
            no1.append(i)
            if no1.count(i) > 1: # 같은번호 제거
                no1.pop()

        no1.sort()
        winlist.append(no1)

window = Tk()
window.title("로또 번호 생성기")
window.geometry("300x300")
frame_top = Frame(window)
frame_top.pack(side="top")

radio_var = IntVar()
r1_button = Radiobutton(frame_top, text="랜덤하게 번호 선택", value=1, variable=radio_var)
r2_button = Radiobutton(frame_top, text="바로전 1회차 번호 제외", value=2, variable=radio_var)
r3_button = Radiobutton(frame_top, text="바로전 2회차 번호 제외", value=3, variable=radio_var)

r1_button.pack(side="top")
r2_button.pack(side="top")
r3_button.pack(side="top")

# 버튼 클릭하면 로또 번호 생성
def button_command():
    winlist.clear()
    opt = radio_var.get()
    if opt == 1:
        lotto_num1()
    elif opt == 2:
        lotto_num2()
    else:
        lotto_num3()

    # print(winlist)
    listbox.delete(0,END)
    for no in winlist:
        str = "{0:2d} {1:2d} {2:2d} {3:2d} {4:2d} {5:2d}"
        fmt = str.format(no[0], no[1], no[2], no[3], no[4], no[5])
        listbox.insert(END, fmt)

button = Button(frame_top, text="실행", command=button_command)
button.pack(side="top")

listbox = Listbox(frame_top,selectmode="extended", height=0)
listbox.insert(0, "첫번째 번호")
listbox.insert(1, "두번째 번호")
listbox.insert(2, "세번째 번호")
listbox.insert(3, "네번째 번호")
listbox.insert(4, "다섯번째 번호")
listbox.pack(side="top")

frame_bot = Frame(window)
frame_bot.pack(side="top")

first_lbl = Label(frame_bot, text="{0:4d}회".format(draw_count))
first_lbl.grid(column=0, row=0)
first_str = StringVar()
first_str.set("{0:2d} {1:2d} {2:2d} {3:2d} {4:2d} {5:2d}".format(drawlist[0][0],drawlist[0][1],drawlist[0][2],drawlist[0][3],drawlist[0][4],drawlist[0][5]))
first_txt = Entry(frame_bot, width=30, textvariable=first_str)
first_txt.grid(column=1, row=0)

second_lbl = Label(frame_bot, text="{0:4d}회".format(draw_count-1))
second_lbl.grid(column=0, row=1)
second_str = StringVar()
second_str.set("{0:2d} {1:2d} {2:2d} {3:2d} {4:2d} {5:2d}".format(drawlist[1][0],drawlist[1][1],drawlist[1][2],drawlist[1][3],drawlist[1][4],drawlist[1][5]))
second_txt = Entry(frame_bot, width=30, textvariable=second_str)
second_txt.grid(column=1,row=1)

window.mainloop()