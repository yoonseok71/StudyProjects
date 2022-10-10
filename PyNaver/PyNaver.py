from tkinter import *
from tkinter import ttk
from tkinter import messagebox as msgbox
from datetime import datetime
import calendar


import SearchTrendApi as api
# import ShoppingInsightApi

# 검색
client_id = "A_5TeRCjyPtE8XqEOylQ"
client_secret = "IAElttsqBe"

def search_func():
    res = api.SearchTrendApi(client_id, client_secret)

    if search_var.get() == 1:
        # 값이 있는지 체크
        val_is = FALSE
        if len(keyword1_entry.get()) > 0 and keyword1_entry.get() != "주제어1 입력":
            val_is = TRUE
            if len(keyword1_group.get()) == 0 or keyword1_group.get() == "주제어1에 해당하는 검색어 20개 입력":
                keyword1_group.delete(0, END)
                keyword1_group.insert(0, keyword1_entry.get())

            keywords1 = keyword1_group.get().split(',')
            keyword_group_set1 = {
                'groupName' : keyword1_entry.get(),
                'keywords' : keywords1
            }
            res.add_keyword_groups(keyword_group_set1)

        if len(keyword2_entry.get()) > 0 and keyword2_entry.get() != "주제어2 입력":
            val_is = TRUE
            if len(keyword2_group.get()) == 0 or keyword2_group.get() == "주제어2에 해당하는 검색어 20개 입력":
                keyword2_group.delete(0, END)
                keyword2_group.insert(0, keyword2_entry.get())

            keywords2 = keyword2_group.get().split(',')
            keyword_group_set2 = {
                'groupName' : keyword2_entry.get(),
                'keywords' : keywords2
            }
            res.add_keyword_groups(keyword_group_set2)

        if len(keyword3_entry.get()) > 0 and keyword3_entry.get() != "주제어3 입력":
            val_is = TRUE
            if len(keyword3_group.get()) == 0 or keyword3_group.get() == "주제어3에 해당하는 검색어 20개 입력":
                keyword3_group.delete(0, END)
                keyword3_group.insert(0, keyword3_entry.get())

            keywords3 = keyword3_group.get().split(',')
            keyword_group_set3 = {
                'groupName' : keyword3_entry.get(),
                'keywords' : keywords3
            }
            res.add_keyword_groups(keyword_group_set3)

        if val_is == FALSE:
            msgbox.showwarning("Warning", "주제어와 검색어를 입력해 주시기 바랍니다.")
            return

        startDate = f'{startYear_cb.get()}-{startMon_cb.get().zfill(2)}-{startDay_cb.get().zfill(2)}'
        endDate = f'{endYear_cb.get()}-{endMon_cb.get().zfill(2)}-{endDay_cb.get().zfill(2)}'

        p = time_cb.get()
        if p == "일간":
            timeUnit = "date"
        elif p == "주간":
            timeUnit = "week"
        else:
            timeUnit = "month"
        
        if device_var2.get() == 1:
            device = "pc"
        elif device_var3.get() == 1:
            device = "mo"
        else:
            device = ""
        
        ages = []
        if ages_12_var.get() == 1:
            ages.append("1")
        if ages_13_var.get() == 1:
            ages.append("2")
        if ages_19_var.get() == 1:
            ages.append("3")
        if ages_25_var.get() == 1:
            ages.append("4")
        if ages_30_var.get() == 1:
            ages.append("5")
        if ages_30_var.get() == 1:
            ages.append("6")
        if ages_40_var.get() == 1:
            ages.append("7")
        if ages_45_var.get() == 1:
            ages.append("8")
        if ages_50_var.get() == 1:
            ages.append("9")
        if ages_55_var.get() == 1:
            ages.append("10")
        if ages_60_var.get() == 1:
            ages.append("11")

        if gender_var2.get() == 1:
            gender = "m"
        elif gender_var3.get() == 1:
            gender = "f"
        else:
            gender = ""

        try:
            df = res.get_data(startDate, endDate, timeUnit, device, ages, gender)
            res.plot_trend(df)
        except Exception:
            msgbox.showerror("Exception", Exception.args)

    elif search_var.get() == 2:
        print("쇼핑인사이트")
    else:
        print("not selected!")


win = Tk()
win.geometry("550x350")
frame_top = Frame(win)
frame_top.pack(side="top", fill=X)
frame_opt = Frame(frame_top)
frame_opt.pack(side="left",expand=TRUE,)
frame_btn = Frame(frame_top)
frame_btn.pack(side="left",expand=TRUE)

search_var = IntVar()
btn1 = Radiobutton(frame_opt, text="통합검색어 트렌드", value = 1, variable=search_var)
btn2 = Radiobutton(frame_opt, text="쇼핑인사이트", value = 2, variable=search_var)
btn1.pack(side="top", anchor="w")
btn2.pack(side="top", anchor="w")

search_btn = Button(frame_btn, text="검색", command=search_func)
search_btn.pack(side="left")

frame_keyword = Frame(win)
frame_keyword.pack(side="top", fill=X)

# 주제어1
def keyword1_focus(event):
    if event.type == EventType.FocusIn:
        if keyword1_entry.get() == "주제어1 입력":
            keyword1_entry.delete(0, END)
    elif event.type == EventType.FocusOut:
        if len(keyword1_entry.get()) == 0:
            keyword1_entry.insert(0, "주제어1 입력")
    else:
        print(event.type)

def keyword1_grp_focus(event):
    if event.type == EventType.FocusIn:
        if keyword1_group.get() == "주제어1에 해당하는 검색어 20개 입력":
            keyword1_group.delete(0, END)
    elif event.type == EventType.FocusOut:
        if len(keyword1_group.get()) == 0:
            keyword1_group.insert(0, "주제어1에 해당하는 검색어 20개 입력")
    else:
        print(event.type)

keyword1_lbl = Label(frame_keyword, text="주제어1")
keyword1_entry = Entry(frame_keyword, width=15)
keyword1_entry.insert(0, "주제어1 입력")
keyword1_entry.bind("<FocusIn>", keyword1_focus)
keyword1_entry.bind("<FocusOut>", keyword1_focus)
keyword1_group = Entry(frame_keyword, width=50)
keyword1_group.insert(0, "주제어1에 해당하는 검색어 20개 입력")
keyword1_group.bind("<FocusIn>", keyword1_grp_focus)
keyword1_group.bind("<FocusOut>", keyword1_grp_focus)

keyword1_lbl.grid(column=0, row=0, padx=3, pady=3)
keyword1_entry.grid(column=1, row=0, padx=3, pady=3)
keyword1_group.grid(column=2, row=0, padx=3, pady=3)

# 주제어2
def keyword2_focus(event):
    if event.type == EventType.FocusIn:
        if keyword2_entry.get() == "주제어2 입력":
            keyword2_entry.delete(0, END)
    elif event.type == EventType.FocusOut:
        if len(keyword2_entry.get()) == 0:
            keyword2_entry.insert(0, "주제어2 입력")
    else:
        print(event.type)

def keyword2_grp_focus(event):
    if event.type == EventType.FocusIn:
        if keyword2_group.get() == "주제어2에 해당하는 검색어 20개 입력":
            keyword2_group.delete(0, END)
    elif event.type == EventType.FocusOut:
        if len(keyword2_group.get()) == 0:
            keyword2_group.insert(0, "주제어2에 해당하는 검색어 20개 입력")
    else:
        print(event.type)

keyword2_lbl = Label(frame_keyword, text="주제어2")
keyword2_entry = Entry(frame_keyword, width=15)
keyword2_entry.insert(0, "주제어2 입력")
keyword2_entry.bind("<FocusIn>", keyword2_focus)
keyword2_entry.bind("<FocusOut>", keyword2_focus)
keyword2_group = Entry(frame_keyword, width=50)
keyword2_group.insert(0, "주제어2에 해당하는 검색어 20개 입력")
keyword2_group.bind("<FocusIn>", keyword2_grp_focus)
keyword2_group.bind("<FocusOut>", keyword2_grp_focus)

keyword2_lbl.grid(column=0, row=1, padx=3, pady=3)
keyword2_entry.grid(column=1, row=1, padx=3, pady=3)
keyword2_group.grid(column=2, row=1, padx=3, pady=3)

# 주제어3
def keyword3_focus(event):
    if event.type == EventType.FocusIn:
        if keyword3_entry.get() == "주제어3 입력":
            keyword3_entry.delete(0, END)
    elif event.type == EventType.FocusOut:
        if len(keyword3_entry.get()) == 0:
            keyword3_entry.insert(0, "주제어3 입력")
    else:
        print(event.type)

def keyword3_grp_focus(event):
    if event.type == EventType.FocusIn:
        if keyword3_group.get() == "주제어3에 해당하는 검색어 20개 입력":
            keyword3_group.delete(0, END)
    elif event.type == EventType.FocusOut:
        if len(keyword3_group.get()) == 0:
            keyword3_group.insert(0, "주제어3에 해당하는 검색어 20개 입력")
    else:
        print(event.type)

keyword3_lbl = Label(frame_keyword, text="주제어3")
keyword3_entry = Entry(frame_keyword, width=15)
keyword3_entry.insert(0, "주제어3 입력")
keyword3_entry.bind("<FocusIn>", keyword3_focus)
keyword3_entry.bind("<FocusOut>", keyword3_focus)
keyword3_group = Entry(frame_keyword, width=50)
keyword3_group.insert(0, "주제어3에 해당하는 검색어 20개 입력")
keyword3_group.bind("<FocusIn>", keyword3_grp_focus)
keyword3_group.bind("<FocusOut>", keyword3_grp_focus)

keyword3_lbl.grid(column=0, row=3, padx=3, pady=3)
keyword3_entry.grid(column=1, row=3, padx=3, pady=3)
keyword3_group.grid(column=2, row=3, padx=3, pady=3)


# 기간(time)
frame1_time = Frame(win)
frame1_time.pack(side="top", fill=X)

time_lbl = Label(frame1_time, width=7, text="기간")
time_lbl.pack(side="left")

def time_func():
    year = datetime.today().year # 현재 연도
    month = datetime.today().month # 현재 월
    day = datetime.today().day

    startDay_cb.set(day)
    endDay_cb.set(day)

    val = time_var.get()
    if val == 1: # 전체
        startYear_cb.current(0)
        startMon_cb.current(0)
        endYear_cb.set(year)
        endMon_cb.set(month)
    elif val == 2: # 1개월
        if month == 1:
            startYear_cb.set(year-1)
            startMon_cb.set(12)
        else:
            startYear_cb.set(year)
            startMon_cb.set(month-1)
        endYear_cb.set(year)
        endMon_cb.set(month)
    elif val == 3: # 3개월
        if month < 4:
            startYear_cb.set(year-1)
            startMon_cb.set(9+month)
        else:
            startYear_cb.set(year)
            startMon_cb.set(month-3)
        endYear_cb.set(year)
        endMon_cb.set(month)
    elif val == 4: # 1년
        startYear_cb.set(year-1)
        startMon_cb.set(month)
        endYear_cb.set(year)
        endMon_cb.set(month)
    else: # 직접입력
        print("직접입력")

time_var = IntVar()
time_all = Radiobutton(frame1_time, text="전체", value=1, variable=time_var, command=time_func)
time_all.pack(side="left", padx=3, pady=3)
time_1mon = Radiobutton(frame1_time, text="1개월", value=2, variable=time_var, command=time_func)
time_1mon.pack(side="left", padx=3, pady=3)
time_3mon = Radiobutton(frame1_time, text="3개월", value=3, variable=time_var, command=time_func)
time_3mon.pack(side="left", padx=3, pady=3)
time_1year = Radiobutton(frame1_time, text="1년", value=4, variable=time_var, command=time_func)
time_1year.pack(side="left", padx=3, pady=3)
time_any = Radiobutton(frame1_time, text="직접입력", value=5, variable=time_var, command=time_func)
time_any.pack(side="left", padx=3, pady=3)

period = ["일간", "주간", "월간"]
time_cb = ttk.Combobox(frame1_time)
time_cb.config(height=5, width=7)
time_cb.config(values=period)
time_cb.config(state="readonly")
time_cb.set(period[0])
time_cb.pack(side="left", padx=3, pady=3)

frame2_time = Frame(win)
frame2_time.pack(side="top", fill=X)

time_blnk = Label(frame2_time, width=7, text=" ")
time_blnk.pack(side="left", pady=3)

# startDate은 2016.1.1부터 시작
# Start Year combobox
years = []
year = datetime.today().year
for i in range(2016, year+1):
    years.append(i)
startYear_cb = ttk.Combobox(frame2_time)
startYear_cb.config(height=5, width=5)
startYear_cb.config(values=years)
startYear_cb.config(state="readonly")
startYear_cb.current(0)
startYear_cb.pack(side="left", pady=3)

# Start Month combobox
# 월을 바꾸면 일수를 계산해서 days comobox 업데이트
def update_days(event):
    combo = event.widget.cget("text");
    last_day = 0
    days = []
    if combo == "startMon":
        last_day = get_month_range(int(startYear_cb.get()), int(startMon_cb.get()))[1]
        for i in range(1, last_day+1):
            days.append(i)
        startDay_cb.config(values=days)
        startDay_cb.set(1)
    elif combo == "endMon":
        last_day = get_month_range(int(endYear_cb.get()), int(endMon_cb.get()))[1]
        for i in range(1, last_day+1):
            days.append(i)
        endDay_cb.config(values=days)
        endDay_cb.set(1)

sMon = []
for i in range(1, 13):
    sMon.append(i)

startMon_cb = ttk.Combobox(frame2_time, text="startMon")
startMon_cb.bind("<<ComboboxSelected>>", update_days)
startMon_cb.config(height=5, width=3)
startMon_cb.config(values=sMon)
startMon_cb.config(state="readonly")
startMon_cb.set(1)
startMon_cb.pack(side="left", pady=3)

# Start Day Combobox
def get_month_range(year, month):
    """
    return tuple : (first day, last day)
    """
    date = datetime(year=year, month=month, day=1).date()
    monthrange = calendar.monthrange(date.year, date.month)
    return monthrange

sdays = []
last_day = get_month_range(int(startYear_cb.get()), int(startMon_cb.get()))[1]
for i in range(1, last_day+1):
    sdays.append(i)
startDay_cb = ttk.Combobox(frame2_time)
startDay_cb.config(height=5, width=3)
startDay_cb.config(values=sdays)
startDay_cb.config(state="readonly")
startDay_cb.set(1)
startDay_cb.pack(side="left", pady=3)

dash_lbl = Label(frame2_time, text="~")
dash_lbl.pack(side="left", pady=3)

# endDate
# End Year combobox
endYear_cb = ttk.Combobox(frame2_time)
endYear_cb.config(height=5, width=5)
endYear_cb.config(values=years)
endYear_cb.config(state="readonly")
endYear_cb.current(len(years)-1) # 마지막 연도
endYear_cb.pack(side="left", pady=3)

# End Month combobox
eMon = []
cMon = datetime.today().month
for i in range(1, cMon+1):
    eMon.append(i)
endMon_cb = ttk.Combobox(frame2_time, text="endMon")
endMon_cb.bind("<<ComboboxSelected>>", update_days)
endMon_cb.config(height=5, width=3)
endMon_cb.config(values=eMon)
endMon_cb.config(state="readonly")
endMon_cb.set(datetime.today().month)
endMon_cb.pack(side="left", pady=3)

edays = []
last_day = get_month_range(int(startYear_cb.get()), int(startMon_cb.get()))[1]
for i in range(1, last_day+1):
    edays.append(i)
endDay_cb = ttk.Combobox(frame2_time)
endDay_cb.config(height=5, width=3)
endDay_cb.config(values=edays)
endDay_cb.config(state="readonly")
endDay_cb.set(datetime.today().day)
endDay_cb.pack(side="left", pady=3)
endDay_cb.pack(side="left", pady=3)

# 기간 초기값은 1년
y = datetime.today().year
m = datetime.today().month
d = datetime.today().day

startYear_cb.set(y-1)
startMon_cb.set(m)
startDay_cb.set(d)
endYear_cb.set(y)
endMon_cb.set(m)
endDay_cb.set(d)

# device (범위)
frame_device = Frame(win)
frame_device.pack(side="top", fill=X)
device_lbl = Label(frame_device, text="범위", width=7)
device_lbl.pack(side="left", pady=3)

def device_func():
    if device_var1.get() == 1:
        device_var2.set(1)
        device_var3.set(1)
    else:
        device_var2.set(0)
        device_var3.set(0)
        
device_var1 = IntVar()
device_var2 = IntVar()
device_var3 = IntVar()
device_all = Checkbutton(frame_device, text="전체", variable=device_var1, command=device_func)
device_all.pack(side="left", padx=3, pady=3)
device_pc = Checkbutton(frame_device, text="PC", variable=device_var2)
device_pc.pack(side="left", padx=3, pady=3)
device_mobile = Checkbutton(frame_device, text="Mobile", variable=device_var3)
device_mobile.pack(side="left", padx=3, pady=3)

# gender (성별)
frame_gender = Frame(win)
frame_gender.pack(side="top", fill=X)
gender_lbl = Label(frame_gender, text="성별", width=7)
gender_lbl.pack(side="left", pady=3)

def gender_func(x):
    if x == "all":
        if gender_var1.get() == 1:
            gender_var2.set(1)
            gender_var3.set(1)
        else:
            gender_var2.set(0)
            gender_var3.set(0)

gender_var1 = IntVar()
gender_var2 = IntVar()
gender_var3 = IntVar()
gender_all = Checkbutton(frame_gender, text="전체", variable=gender_var1, command=lambda x="all": gender_func(x))
gender_all.pack(side="left", padx=3, pady=3)
gender_m = Checkbutton(frame_gender, text="남성", variable=gender_var2)
gender_m.pack(side="left", padx=3, pady=3)
gender_f = Checkbutton(frame_gender, text="여성", variable=gender_var3)
gender_f.pack(side="left", padx=3, pady=3)

# ages (연령선택)
frame_ages = Frame(win)
frame_ages.pack(side=TOP, fill=X)
ages_lbl = Label(frame_ages, text="연령선택")
ages_lbl.grid(column=0, row=0, pady=3)

def ages_func():
    if ages_all_var.get() == 1:
        ages_12_var.set(1)
        ages_13_var.set(1)
        ages_19_var.set(1)
        ages_25_var.set(1)
        ages_30_var.set(1)
        ages_35_var.set(1)
        ages_40_var.set(1)
        ages_45_var.set(1)
        ages_50_var.set(1)
        ages_55_var.set(1)
        ages_60_var.set(1)
    else:
        ages_12_var.set(0)
        ages_13_var.set(0)
        ages_19_var.set(0)
        ages_25_var.set(0)
        ages_30_var.set(0)
        ages_35_var.set(0)
        ages_40_var.set(0)
        ages_45_var.set(0)
        ages_50_var.set(0)
        ages_55_var.set(0)
        ages_60_var.set(0)


ages_all_var = IntVar()
ages_12_var = IntVar()
ages_13_var = IntVar()
ages_19_var = IntVar()
ages_25_var = IntVar()
ages_30_var = IntVar()
ages_35_var = IntVar()
ages_40_var = IntVar()
ages_45_var = IntVar()
ages_50_var = IntVar()
ages_55_var = IntVar()
ages_60_var = IntVar()
ages_all = Checkbutton(frame_ages, text="전체", variable=ages_all_var, command=ages_func)
ages_all.grid(column=1, row=0, pady=3)
ages_12 = Checkbutton(frame_ages, text="~12", variable=ages_12_var)
ages_12.grid(column=2, row=0, pady=3)
ages_13 = Checkbutton(frame_ages, text="13~18", variable=ages_13_var)
ages_13.grid(column=3, row=0, pady=3)
ages_19 = Checkbutton(frame_ages, text="19~24", variable=ages_19_var)
ages_19.grid(column=4, row=0, pady=3)
ages_25 = Checkbutton(frame_ages, text="25~29", variable=ages_25_var)
ages_25.grid(column=5, row=0, pady=3)
ages_30 = Checkbutton(frame_ages, text="30~34", variable=ages_30_var)
ages_30.grid(column=6, row=0, pady=3)

ages_blnk = Label(frame_ages, text=" ", width=7)
ages_blnk.grid(column=0, row=1, pady=3)
ages_35 = Checkbutton(frame_ages, text="35~39", variable=ages_35_var)
ages_35.grid(column=1, row=1, pady=3)
ages_40 = Checkbutton(frame_ages, text="40~44", variable=ages_40_var)
ages_40.grid(column=2, row=1, pady=3)
ages_45 = Checkbutton(frame_ages, text="45~49", variable=ages_45_var)
ages_45.grid(column=3, row=1, pady=3)
ages_50 = Checkbutton(frame_ages, text="50~54", variable=ages_50_var)
ages_50.grid(column=4, row=1, pady=3)
ages_55 = Checkbutton(frame_ages, text="55~60", variable=ages_55_var)
ages_55.grid(column=5, row=1, pady=3)
ages_60 = Checkbutton(frame_ages, text="60~", variable=ages_60_var)
ages_60.grid(column=6, row=1, pady=3)

win.mainloop()