import tkinter as tk
from tkinter import ttk
from sympy import symbols, Rational, Eq, simplify, solve

yaho = 0

class section:
    def __init__(self, start=None, end=None):
        self.relative = [None,None,None,None]
        self.L = None
        self.aV = None
        self.A = None
        self.dT = None
        self.start = start
        self.end = end

class line:
    def __init__(self):
        self.relative = [None,None,None,None]
        self.S = None
        self.V = None
        self.A = None
        self.T = None

Variables = {}
Relative = {}

def sectionPop(object, start, end):
    start, end = min(int(start), int(end)), max(int(start), int(end))
    return Map[int(object)][1][SectionIndexMap[int(object)].index((start, end))]

def linePop(object, linenum):
    return Map[int(object)][0][int(linenum)]

def setValue(prompt,i):
    if prompt[1]=='line':
        address = [prompt[3],prompt[4],i] #objNum lineNum SVAT
        if len(prompt)>=7 and prompt[6]=='/':
            if len(prompt)>=9 and prompt[8] in Variables.keys():
                if address not in Relative[prompt[8]]:
                    Relative[prompt[8]].append(address)
                linePop(prompt[3],prompt[4]).relative[i] = prompt[8]
                return Rational(prompt[5],prompt[7]) * Variables[prompt[8]]
            else:
                print('변수 없는 거 맞죠?')
                linePop(prompt[3],prompt[4]).relative[i] = 'None'
                return Rational(prompt[5],prompt[7])
        else:
            if len(prompt)>=7 and prompt[6] in Variables.keys():
                if address not in Relative[prompt[6]]:
                    Relative[prompt[6]].append(address)
                linePop(prompt[3],prompt[4]).relative[i] = prompt[6]
                return prompt[5] * Variables[prompt[6]]
            else:
                print('변수 없는 거 맞죠?')
                linePop(prompt[3],prompt[4]).relative[i] = 'None'
                return prompt[5]
    else:
        address = [prompt[3],prompt[4],prompt[5],i] #objNum startNum endNum LaVAdT
        if prompt[7]=='/' and len(prompt)>=7:
            if len(prompt)>=10 and prompt[9] in Variables.keys():
                if address not in Relative[prompt[9]]:
                    Relative[prompt[9]].append(address)
                linePop(prompt[3],prompt[4]).relative[i] = prompt[9]
                return Rational(prompt[6],prompt[8]) * Variables[prompt[9]]
            else:
                print('변수 없는 거 맞죠?')
                return Rational(prompt[6],prompt[8])
        else:
            if len(prompt)>=8 and prompt[7] in Variables.keys():
                if address not in Relative[prompt[7]]:
                    Relative[prompt[7]].append(address)
                return prompt[6] * Variables[prompt[7]]
            else:
                print('변수 없는 거 맞죠?')
                return prompt[6]
    
def setValueUI():
    kind = kind_var.get()
    quantity = quantity_var.get()
    obj = int(object_entry.get())
    line1 = int(line1_entry.get())
    value = numerator_entry.get()
    denom = denominator_entry.get()
    varname = variable_entry.get()

    val = Rational(value, denom)
    if varname in Variables:
        val *= Variables[varname]
        address = [obj, line1, 0]
        if address not in Relative[varname]:
            Relative[varname].append(address)
        if kind == "line":
            linePop(obj, line1).relative[0] = varname
    else:
        print("변수 없는 거 맞죠?")

    if kind == "line":
        if quantity == 'S':
            linePop(obj, line1).S = val
        elif quantity == 'V':
            linePop(obj, line1).V = val
        elif quantity == 'A':
            linePop(obj, line1).A = val
        elif quantity == 'T':
            linePop(obj, line1).T = val
    elif kind == "section":
        line2 = int(line2_entry.get())
        sec = sectionPop(obj, line1, line2)
        if quantity == 'L':
            sec.L = val
        elif quantity == 'aV':
            sec.aV = val
        elif quantity == 'A':
            sec.A = val
        elif quantity == 'dT':
            sec.dT = val

    status_label.config(text=f"값 설정 완료: {val}")

Map = []
SectionIndexMap = []  # section의 (start, end) 저장

object_num = 2
line_num = 3
#object_num = int(input("물체의 개수를 입력하세요 : "))
#line_num = int(input("선의 개수를 입력하세요(시작선 포함) : "))


for i in range(object_num):
    Map.append([[], []])  # [lines, sections]
    SectionIndexMap.append([])
    for j in range(line_num):
        Map[i][0].append(line())
    for j in range(line_num):
        for k in range(j + 1, line_num):
            Map[i][1].append(section(start=j, end=k))
            SectionIndexMap[i].append((j, k))
    Map[i][0][0].T = 0

# tkinter UI
root = tk.Tk()
root.title("물리 값 설정")

frame = ttk.Frame(root, padding=10)
frame.grid()

ttk.Label(frame, text="종류 (line/section):").grid(column=0, row=0)
kind_var = tk.StringVar(value="line")
ttk.Entry(frame, textvariable=kind_var).grid(column=1, row=0)

ttk.Label(frame, text="값 종류 (S/V/A/T/L/aV/dT):").grid(column=0, row=1)
quantity_var = tk.StringVar(value="V")
ttk.Entry(frame, textvariable=quantity_var).grid(column=1, row=1)

ttk.Label(frame, text="객체 번호:").grid(column=0, row=2)
object_entry = ttk.Entry(frame)
object_entry.grid(column=1, row=2)

ttk.Label(frame, text="라인 번호 1:").grid(column=0, row=3)
line1_entry = ttk.Entry(frame)
line1_entry.grid(column=1, row=3)

ttk.Label(frame, text="라인 번호 2 (section만):").grid(column=0, row=4)
line2_entry = ttk.Entry(frame)
line2_entry.grid(column=1, row=4)

ttk.Label(frame, text="분자:").grid(column=0, row=5)
numerator_entry = ttk.Entry(frame)
numerator_entry.grid(column=1, row=5)

ttk.Label(frame, text="분모:").grid(column=0, row=6)
denominator_entry = ttk.Entry(frame)
denominator_entry.grid(column=1, row=6)

ttk.Label(frame, text="변수 이름:").grid(column=0, row=7)
variable_entry = ttk.Entry(frame)
variable_entry.grid(column=1, row=7)

ttk.Button(frame, text="값 설정", command=setValueUI).grid(column=0, row=8, columnspan=2)

status_label = ttk.Label(frame, text="")
status_label.grid(column=0, row=9, columnspan=2)

root.mainloop()

'''wait=True
while wait:
    prompt = input('What do you want? ')
    prompt = prompt.split()
    if prompt[0]=='setValue': # setValue line S objectnum linenum son (/ mom) (Variable)
        if prompt[1]=='line':
            if prompt[2]=='S':
                linePop(prompt[3],prompt[4]).S = setValue(prompt,0)
            elif prompt[2]=='V':
                linePop(prompt[3],prompt[4]).V = setValue(prompt,1)
            elif prompt[2]=='A':
                linePop(prompt[3],prompt[4]).A = setValue(prompt,2)
            elif prompt[2]=='T':
                linePop(prompt[3],prompt[4]).T = setValue(prompt,3)
        else:
            if prompt[2]=='L':
                sectionPop(prompt[3],prompt[4],prompt[5]).L = setValue(prompt,0)
            elif prompt[2]=='aV':
                sectionPop(prompt[3],prompt[4],prompt[5]).aV = setValue(prompt,1)
            elif prompt[2]=='A':
                sectionPop(prompt[3],prompt[4],prompt[5]).A = setValue(prompt,2)
            elif prompt[2]=='dT':
                sectionPop(prompt[3],prompt[4],prompt[5]).dT = setValue(prompt,3)
    elif prompt[0]=='simai':
        wait=False
    elif prompt[0]=='setVariable':
        Variables[prompt[1]]=symbols(prompt[1])
        Relative[prompt[1]]=[]
    #elif prompt[0]=='':

#autoCal
while yaho<3:
    
    #시각 ; 시각과 시간 통일
    #위치 ; 위치와 길이 통일
    #속도 ; 평속 계산
    #가속 ; 구간의 가속도로 하위 구간의 가속도 통일
    #      등속도이면 평균속도 통일
    #길이 ; 시간도 존재하면 평속 계산
    #평속 ; 시간도 존재하면 길이 계산
    #      길이도 존재하면 시간 계산
    #속도 ; 길이도 시간도 존재하면 가속 계산

    #그냥 대입이 아니라 일단 비교해서 이미 존재하지 않으면 대입하면서 기록 이미 존재하면 같은지 판단
    #같으면 넘어가고 다르면 해 구해서 대입

    #시각 ; 시각과 시간 통일
    for objNum in range(len(Map)):
        for lineNum in range(len(Map[objNum][0])):
            if Map[objNum][0][lineNum].T is not None:
                for nextlineNum in range(lineNum+1,len(Map[objNum][0])):
                    if Map[objNum][0][nextlineNum].T is not None:
                        sectionPop(objNum,lineNum,nextlineNum).dT = linePop(objNum,nextlineNum).T - linePop(objNum,lineNum).T
    #위치 ; 위치와 길이 통일
            if Map[objNum][0][lineNum].S is not None:
                for nextlineNum in range(lineNum+1,len(Map[objNum][0])):
                    if Map[objNum][0][nextlineNum].S is not None:
                        for oobjNum in range(len(Map)): #위치 이용 시 동기화 해주세요
                            sectionPop(oobjNum,lineNum,nextlineNum).L = linePop(objNum,nextlineNum).S - linePop(objNum,lineNum).S
    #속도 ; 평속 계산
    for objNum in range(len(Map)):
        for lineNum in range(len(Map[objNum][0])):
            if Map[objNum][0][lineNum].V is not None:
                for nextlineNum in range(lineNum+1,len(Map[objNum][0])):
                    if Map[objNum][0][nextlineNum].V is not None:
                        sectionPop(objNum,lineNum,nextlineNum).aV = Rational(linePop(objNum,nextlineNum).V + linePop(objNum,lineNum).V, 2)
    #가속 ; 구간의 가속도로 하위 구간의 가속도 통일
    sectionCan = []
    for objNum in range(len(Map)):
        for startNum in range(len(Map[objNum][0])):
            for endNum in range(startNum+1,len(Map[objNum][0])):
                if sectionPop(objNum,startNum,endNum).A is not None:
                    for small_startNum in range(startNum,endNum):
                        for small_endNum in range(small_startNum+1,endNum):
                            sectionCan.append([objNum,small_startNum,small_endNum,sectionPop(objNum,startNum,endNum).A])
    for sect in sectionCan:
        sectionPop(sectionCan[0],sectionCan[1],sectionCan[2]).A = sectionCan[3]
    #      등속도이면 평균속도 통일
    for objNum in range(len(Map)):
        for startNum in range(len(Map[objNum][0])):
            for endNum in range(startNum+1,len(Map[objNum][0])):
                if sectionPop(objNum,startNum,endNum).A is not None and sectionPop(objNum,startNum,endNum).A==0:
                    if linePop(objNum,startNum).V is not None:
                        sectionPop(objNum,startNum,endNum).aV = linePop(objNum,startNum).V
                    if linePop(objNum,endNum).V is not None:
                        sectionPop(objNum,endNum,endNum).aV = linePop(objNum,endNum).V
    #길이 ; 시간도 존재하면 평속 계산
    for objNum in range(len(Map)):
        for startNum in range(len(Map[objNum][0])):
            for endNum in range(startNum+1,len(Map[objNum][0])):
                if sectionPop(objNum,startNum,endNum).L is not None and sectionPop(objNum,startNum,endNum).dT is not None:
                    sectionPop(objNum,startNum,endNum).aV = Rational(sectionPop(objNum,startNum,endNum).L, sectionPop(objNum,startNum,endNum).dT)
    #평속 ; 시간도 존재하면 길이 계산
    for objNum in range(len(Map)):
        for startNum in range(len(Map[objNum][0])):
            for endNum in range(startNum+1,len(Map[objNum][0])):
                if sectionPop(objNum,startNum,endNum).aV is not None:
                    if sectionPop(objNum,startNum,endNum).dT is not None:
                        sectionPop(objNum,startNum,endNum).L = sectionPop(objNum,startNum,endNum).aV * sectionPop(objNum,startNum,endNum).dT
    #      길이도 존재하면 시간 계산
                    if sectionPop(objNum,startNum,endNum).L is not None:
                        sectionPop(objNum,startNum,endNum).dT = Rational(sectionPop(objNum,startNum,endNum).L, sectionPop(objNum,startNum,endNum).aV)
    #속도 ; 길이도 시간도 존재하면 가속 계산
    for objNum in range(len(Map)):
        for startNum in range(len(Map[objNum][0])):
            for endNum in range(startNum+1,len(Map[objNum][0])):
                if sectionPop(objNum,startNum,endNum).L is not None and sectionPop(objNum,startNum,endNum).dT is not None:
                    if linePop(objNum,startNum).V is not None:
                        sectionPop(objNum,startNum,endNum).A = 2*Rational(sectionPop(objNum,startNum,endNum).aV-linePop(objNum,startNum).V,sectionPop(objNum,startNum,endNum).T)

    #종료'''
'''for objNum in range(len(Map)):
        for startNum in range(len(Map[objNum][0])):
            for endNum in range(startNum+1,len(Map[objNum][0])):'''
    #yaho += 1


