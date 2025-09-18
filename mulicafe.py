from sympy import symbols, Eq, simplify, solve, gcd, sqrt

yaho = 0

class fraction:
    def __init__(self, son=None, mom=None):
        self.son = son
        self.mom = mom
    def __add__(self,other):
        add = fraction(son=(self.son*other.mom)+(other.son*self.mom),mom=self.mom*other.mom)
        add.simplify()
        return add
    def __sub__(self,other):
        add = fraction(son=(self.son*other.mom)-(other.son*self.mom),mom=self.mom*other.mom)
        add.simplify()
        return add
    def __mul__(self,other):
        mul = fraction(son=self.son*other.son,mom=self.mom*other.mom)
        mul.simplify()
        return mul
    def __truediv__(self,other):
        div = fraction(son=self.son*other.mom,mom=self.mom*other.son)
        div.simplify()
        return div
    def square(self):
        squ = fraction(self.son**2,self.mom**2)
        squ.simplify()
        return squ
    def squat(self):
        sqt = fraction(sqrt(self.son),sqrt(self.mom))
        sqt.simplify()
        return sqt
    def simplify(self):
        self.son, self.mom = self.son/gcd(self.son,self.mom), self.mom/gcd(self.son,self.mom)

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

Variables['None']=symbols('None')
Relative['None']=[]
Map = []
SectionIndexMap = []  # section의 (start, end) 저장

object_num = 2
line_num = 4
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
    Map[i][0][0].T = fraction(0,1)

# 자동 입력용 명령 리스트
commands = [
    "setVariable a",
    "setVariable d",
    "setVariable t",
    "setValue line T 0 3 8 None 1 None",
    "setValue line T 1 3 8 None 1 None",
    "setValue line V 0 0 10 None 1 None",
    "setValue line V 1 0 0 None 1 None",
    "setValue section A 0 0 3 0 None 1 None",
    "setValue section A 1 0 3 1 a 1 None",
    "setValue section L 0 0 2 1 d 1 None",
    "setValue section L 0 2 3 1 d 1 None",
    "setValue section dT 0 0 2 1 t 1 None",
    "setValue section dT 1 0 1 1 t 1 None",
    "simai"
]

command_index = 0
wait = True
while wait and command_index < len(commands):
    prompt = commands[command_index]
    print(f"What do you want? {prompt}")  # 출력 시 실제 입력처럼 보여줌
    command_index += 1

    prompt = prompt.split()
    if prompt[0] == 'setValue':
        if prompt[1] == 'line':
            if prompt[2] == 'S':
                linePop(prompt[3], prompt[4]).S = fraction(int(prompt[5]) * Variables[prompt[6]], int(prompt[7]) * Variables[prompt[8]])
            elif prompt[2] == 'V':
                linePop(prompt[3], prompt[4]).V = fraction(int(prompt[5]) * Variables[prompt[6]], int(prompt[7]) * Variables[prompt[8]])
            elif prompt[2] == 'A':
                linePop(prompt[3], prompt[4]).A = fraction(int(prompt[5]) * Variables[prompt[6]], int(prompt[7]) * Variables[prompt[8]])
            elif prompt[2] == 'T':
                linePop(prompt[3], prompt[4]).T = fraction(int(prompt[5]) * Variables[prompt[6]], int(prompt[7]) * Variables[prompt[8]])
        else:
            if prompt[2] == 'L':
                sectionPop(prompt[3], prompt[4], prompt[5]).L = fraction(int(prompt[6]) * Variables[prompt[7]], int(prompt[8]) * Variables[prompt[9]])
            elif prompt[2] == 'aV':
                sectionPop(prompt[3], prompt[4], prompt[5]).aV = fraction(int(prompt[6]) * Variables[prompt[7]], int(prompt[8]) * Variables[prompt[9]])
            elif prompt[2] == 'A':
                sectionPop(prompt[3], prompt[4], prompt[5]).A = fraction(int(prompt[6]) * Variables[prompt[7]], int(prompt[8]) * Variables[prompt[9]])
            elif prompt[2] == 'dT':
                sectionPop(prompt[3], prompt[4], prompt[5]).dT = fraction(int(prompt[6]) * Variables[prompt[7]], int(prompt[8]) * Variables[prompt[9]])
    elif prompt[0] == 'simai':
        wait = False
    elif prompt[0] == 'setVariable':
        Variables[prompt[1]] = symbols(prompt[1])
        Relative[prompt[1]] = []

lastResult = ''
def print_map(Map,reference):
    global lastResult
    result = ''
    for obj_num, (lines, sections) in enumerate(Map):
        result += (f"\n\nObject {obj_num}:")
        line_count = len(lines)

        # Print line headers
        line_headers = " | ".join([f"Line {i}" for i in range(line_count)])
        result += '\n'+(f"{line_headers}")

        # Print line details
        line_values = []
        for line in lines:
            details = []
            details.append(f"S={line.S.son}/{line.S.mom}" if line.S else "S=ㅁ")
            details.append(f"V={line.V.son}/{line.V.mom}" if line.V else "V=ㅁ")
            details.append(f"A={line.A.son}/{line.A.mom}" if line.A else "A=ㅁ")
            details.append(f"T={line.T.son}/{line.T.mom}" if line.T else "T=ㅁ")
            line_values.append("(" + ", ".join(details) + ")")
        result += '\n'+(" | ".join(line_values))

        # Print sections
        result += ("\nSections:")
        for section in sections:
            s_details = []
            s_details.append(f"[{section.start}-{section.end}]")
            s_details.append(f"L={section.L.son}/{section.L.mom}" if section.L else "L=ㅁ")
            s_details.append(f"aV={section.aV.son}/{section.aV.mom}" if section.aV else "aV=ㅁ")
            s_details.append(f"A={section.A.son}/{section.A.mom}" if section.A else "A=ㅁ")
            s_details.append(f"dT={section.dT.son}/{section.dT.mom}" if section.dT else "dT=ㅁ")
            result += '\n'+(" | ".join(s_details))
    if result != lastResult:
        lastResult = result
        print(result+'\n'+reference+'\n')

def safe_subs(obj, var, val):
    if hasattr(obj, 'son'):
        if hasattr(obj.son, 'subs'):
            obj.son = obj.son.subs(var, val)
            obj.mom = obj.mom.subs(var, val)
            obj.simplify()
    else:
        if hasattr(obj, 'subs'):
            obj = obj.subs(var, val)

def varEqa(var,val):
    print(var, val)
    #map 전체 돌면서 변수 대입
    for objNum in range(len(Map)):
        for lineNum in range(len(Map[objNum][0])):
            safe_subs(Map[objNum][0][lineNum].S,var,val)
            safe_subs(Map[objNum][0][lineNum].V,var,val)
            safe_subs(Map[objNum][0][lineNum].A,var,val)
            safe_subs(Map[objNum][0][lineNum].T,var,val)
        for startNum in range(len(Map[objNum][0])):
            for endNum in range(startNum+1,len(Map[objNum][0])):
                safe_subs(sectionPop(objNum,startNum,endNum).L,var,val)
                safe_subs(sectionPop(objNum,startNum,endNum).aV,var,val)
                safe_subs(sectionPop(objNum,startNum,endNum).A,var,val)
                safe_subs(sectionPop(objNum,startNum,endNum).dT,var,val)

def fracEq(lhs,rhs):
    return Eq(lhs.son * rhs.mom, rhs.son * lhs.mom,evaluate=False)

def sync_if_different(target_ref, expected_val):
    if target_ref is not None:
        if target_ref == expected_val:
            return
        Equ = fracEq(target_ref, expected_val)
        symbolIn = list(Equ.free_symbols)
        if symbolIn:
            varEqa(symbolIn[0].name, solve(Equ, symbolIn[0])[0])
    else:
        target_ref = expected_val

varEqa('None',1)
print_map(Map,'======================================================')
#autoCal
while yaho<8:
    
    #시각 ; 시각과 시간 통일
    #위치 ; 위치와 길이 통일
    #속도 ; 평속 계산
    #가속 ; 구간의 가속도로 하위 구간의 가속도 통일
    #      등속도이면 평균속도 통일
    #길이 ; 이웃 구간 길이와 합쳐서 상위 구간의 길이 계산
    #      시간도 존재하면 평속 계산
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
    #오브젝트 달라도 길이는 같다
    for objNum in range(len(Map)):
        for startNum in range(len(Map[objNum][0])):
            for endNum in range(startNum+1,len(Map[objNum][0])):
                if sectionPop(objNum,startNum,endNum).L is not None:
                    for otherObjNum in range(len(Map)):
                        if objNum==otherObjNum:
                            continue
                        sectionPop(otherObjNum,startNum,endNum).L = sectionPop(objNum,startNum,endNum).L
    print_map(Map,'거리 통일')
    #속도 ; 평속 계산
    for objNum in range(len(Map)):
        for lineNum in range(len(Map[objNum][0])):
            if Map[objNum][0][lineNum].V is not None:
                for nextlineNum in range(lineNum+1,len(Map[objNum][0])):
                    if Map[objNum][0][nextlineNum].V is not None:
                        #if aV already exist: 비교 후 변수통합 혹은 그냥두기
                        preinsert = (linePop(objNum,nextlineNum).V + linePop(objNum,lineNum).V)/fraction(2,1)
                        if sectionPop(objNum,lineNum,nextlineNum).aV is not None:
                            Equ = fracEq(sectionPop(objNum,lineNum,nextlineNum).aV, preinsert)
                            if simplify(Equ.lhs-Equ.rhs) == 0:
                                continue
                            #변수통합
                            symbolIn = list(Equ.free_symbols)
                            if len(symbolIn)!=0:
                                varEqa(symbolIn[0].name,solve(Equ,symbolIn[0])[0])
                        else:
                            sectionPop(objNum,lineNum,nextlineNum).aV = preinsert
    print_map(Map,'속도->평균속도  aV=(v-v0)/2')
    #가속 ; 구간의 가속도로 하위 구간의 가속도 통일
    sectionCan = []
    for objNum in range(len(Map)):
        for startNum in range(len(Map[objNum][0])):
            for endNum in range(startNum+1,len(Map[objNum][0])):
                if sectionPop(objNum,startNum,endNum).A is not None:
                    for small_startNum in range(startNum,endNum):
                        for small_endNum in range(small_startNum+1,endNum+1):
                            if small_startNum==startNum and small_endNum == endNum:
                                continue
                            sectionCan.append([objNum,small_startNum,small_endNum,sectionPop(objNum,startNum,endNum).A])
    for sect in sectionCan:
        sectionPop(sect[0],sect[1],sect[2]).A = sect[3]
    print_map(Map,'가속도 통일')
    #      등속도이면 평균속도 통일
    for objNum in range(len(Map)):
        for startNum in range(len(Map[objNum][0])):
            for endNum in range(startNum+1,len(Map[objNum][0])):
                if sectionPop(objNum,startNum,endNum).A is not None and sectionPop(objNum,startNum,endNum).A.son==0:
                    V = None
                    for linenum in range(startNum,endNum+1):
                        if linePop(objNum,linenum).V is not None:
                            preinsert = linePop(objNum,linenum).V
                            if V is not None:
                                Equ = fracEq(V, preinsert)
                                if simplify(Equ.lhs-Equ.rhs) == 0:
                                    continue
                                #변수통합
                                symbolIn = list(Equ.free_symbols)
                                if len(symbolIn)!=0:
                                    varEqa(symbolIn[0].name,solve(Equ,symbolIn[0])[0])
                            else:
                                V = preinsert
                    if V is not None:
                        for startnum in range(startNum,endNum):
                            for endnum in range(startnum+1,endNum+1):
                                sectionPop(objNum,startnum,endnum).aV = V
    print_map(Map,'등가속도에서 평균속도 일정')
    #길이 ; 이웃 구간 길이와 합쳐서 상위 구간의 길이 계산
    for objNum in range(len(Map)):
        for startNum in range(len(Map[objNum][0])):
            for endNum in range(startNum+1,len(Map[objNum][0])):
                if sectionPop(objNum,startNum,endNum).L is not None:
                    for next_endNum in range(endNum+1,len(Map[objNum][0])):
                        if sectionPop(objNum,endNum,next_endNum).L is not None:
                            preinsert = sectionPop(objNum,startNum,endNum).L + sectionPop(objNum,endNum,next_endNum).L
                            if sectionPop(objNum,startNum,next_endNum).L is not None:
                                Equ = fracEq(sectionPop(objNum,startNum,next_endNum).L, preinsert)
                                if simplify(Equ.lhs-Equ.rhs) == 0:
                                    continue
                                #변수통합
                                symbolIn = list(Equ.free_symbols)
                                if len(symbolIn)!=0:
                                    varEqa(symbolIn[0].name,solve(Equ,symbolIn[0])[0])
                            else:
                                sectionPop(objNum,startNum,next_endNum).L = preinsert
    print_map(Map,'길이 합치기')
    #      시간도 존재하면 평속 계산
    for objNum in range(len(Map)):
        for startNum in range(len(Map[objNum][0])):
            for endNum in range(startNum+1,len(Map[objNum][0])):
                if sectionPop(objNum,startNum,endNum).L is not None and sectionPop(objNum,startNum,endNum).dT is not None:
                    preinsert = sectionPop(objNum,startNum,endNum).L / sectionPop(objNum,startNum,endNum).dT
                    if sectionPop(objNum,startNum,endNum).aV is not None:
                        Equ = fracEq(sectionPop(objNum,startNum,endNum).aV, preinsert)
                        if simplify(Equ.lhs-Equ.rhs) == 0:
                            continue
                        #변수통합
                        symbolIn = list(Equ.free_symbols)
                        if len(symbolIn)!=0:
                            varEqa(symbolIn[0].name,solve(Equ,symbolIn[0])[0])
                    else:
                        sectionPop(objNum,startNum,endNum).aV = preinsert
    print_map(Map,'길이,시간->평균속도  aV=s/t')
    #평속 ; 시간도 존재하면 길이 계산
    for objNum in range(len(Map)):
        for startNum in range(len(Map[objNum][0])):
            for endNum in range(startNum+1,len(Map[objNum][0])):
                if sectionPop(objNum,startNum,endNum).aV is not None:
                    if sectionPop(objNum,startNum,endNum).dT is not None:
                        preinsert = sectionPop(objNum,startNum,endNum).aV * sectionPop(objNum,startNum,endNum).dT
                        if sectionPop(objNum,startNum,endNum).L is not None:
                            Equ = fracEq(sectionPop(objNum,startNum,endNum).L, preinsert)
                            if simplify(Equ.lhs-Equ.rhs) == 0:
                                continue
                            #변수통합
                            symbolIn = list(Equ.free_symbols)
                            if len(symbolIn)!=0:
                                varEqa(symbolIn[0].name,solve(Equ,symbolIn[0])[0])
                        else:
                            sectionPop(objNum,startNum,endNum).L = preinsert
    print_map(Map,'평균속도,시간->길이  s=aVt')
    #      길이도 존재하면 시간 계산
    for objNum in range(len(Map)):
        for startNum in range(len(Map[objNum][0])):
            for endNum in range(startNum+1,len(Map[objNum][0])):
                if sectionPop(objNum,startNum,endNum).aV is not None:
                    if sectionPop(objNum,startNum,endNum).L is not None:
                        preinsert = sectionPop(objNum,startNum,endNum).L / sectionPop(objNum,startNum,endNum).aV
                        if sectionPop(objNum,startNum,endNum).dT is not None:
                            Equ = fracEq(sectionPop(objNum,startNum,endNum).dT, preinsert)
                            if simplify(Equ.lhs-Equ.rhs) == 0:
                                continue
                            #변수통합
                            symbolIn = list(Equ.free_symbols)
                            if len(symbolIn)!=0:
                                varEqa(symbolIn[0].name,solve(Equ,symbolIn[0],evaluate=False)[0])
                        else:
                            sectionPop(objNum,startNum,endNum).dT = preinsert
    print_map(Map,'평균속도,길이->시간  t=s/aV')
    # 2as 공식: v^2 = v0^2 + 2as
    for objNum in range(len(Map)):
        for startNum in range(len(Map[objNum][0])):
            for endNum in range(startNum + 1, len(Map[objNum][0])):
                sec = sectionPop(objNum, startNum, endNum)
                lineS = linePop(objNum, startNum)
                lineE = linePop(objNum, endNum)

                if sec.L is not None and sec.A is not None:
                    # v0 있고 v 없음 → v 계산
                    if lineS.V is not None and lineE.V is None:
                        preinsert = fraction(
                            ((lineS.V.square() + fraction(2, 1) * sec.A * sec.L).son),
                            ((lineS.V.square() + fraction(2, 1) * sec.A * sec.L).mom)
                        ).squat()
                        if lineE.V is not None:
                            Equ = fracEq(lineE.V, preinsert)
                            if lineE.V == preinsert:
                                pass  # 값 같으면 그대로 둠
                            else:
                                symbolIn = list(Equ.free_symbols)
                                if len(symbolIn) != 0:
                                    varEqa(symbolIn[0].name, solve(Equ, symbolIn[0])[0])
                        else:
                            lineE.V = preinsert

                    # v 있고 v0 없음 → v0 계산
                    elif lineE.V is not None and lineS.V is None:
                        preinsert = fraction(
                            ((lineE.V.square() - fraction(2, 1) * sec.A * sec.L).son),
                            ((lineE.V.square() - fraction(2, 1) * sec.A * sec.L).mom)
                        ).squat()
                        if lineS.V is not None:
                            Equ = fracEq(lineS.V, preinsert)
                            if lineS.V == preinsert:
                                pass  # 값 같으면 그대로 둠
                            else:
                                symbolIn = list(Equ.free_symbols)
                                if len(symbolIn) != 0:
                                    varEqa(symbolIn[0].name, solve(Equ, symbolIn[0])[0])
                        else:
                            lineS.V = preinsert
    print_map(Map,'한쪽 속도,가속도,길이->다른쪽 속도  2as=v^2-v0^2')

    #속도 ; 시간도 존재하면 가속 계산
    for objNum in range(len(Map)):
        for startNum in range(len(Map[objNum][0])):
            for endNum in range(startNum+1,len(Map[objNum][0])):
                if sectionPop(objNum,startNum,endNum).dT is not None:
                    if linePop(objNum,startNum).V is not None and linePop(objNum,endNum).V is not None:
                        preinsert = (linePop(objNum, endNum).V - linePop(objNum, startNum).V) / sectionPop(objNum, startNum, endNum).dT
                        if sectionPop(objNum, startNum, endNum).A is not None:
                            Equ = fracEq(sectionPop(objNum, startNum, endNum).A, preinsert)
                            if simplify(Equ.lhs-Equ.rhs) == 0 == 0:
                                pass  # 값 같으면 그대로 둠
                            else:
                                symbolIn = list(Eq(Equ.lhs**2,Equ.rhs**2).free_symbols)
                                if len(symbolIn)==0:
                                    continue
                                try:
                                    var = solve(Equ, symbolIn[0])
                                except:
                                    pass
                                if len(var) == 0:
                                    pass
                                elif len(var) == 1:
                                    varEqa(symbolIn[0].name, var[0])
                                else:
                                    for i in var:
                                        if i==0:
                                            continue
                                        varEqa(symbolIn[0].name, i)
                                        break
                        else:
                            sectionPop(objNum, startNum, endNum).A = preinsert
    print_map(Map,'속도,시간->가속도  a=Δvt')
    #편속 ; 시간도 가속도 존재하면 편속 계산
    for objNum in range(len(Map)):
        for startNum in range(len(Map[objNum][0])):
            for endNum in range(startNum+1,len(Map[objNum][0])):
                if sectionPop(objNum,startNum,endNum).dT is not None and sectionPop(objNum,startNum,endNum).A is not None:
                    if linePop(objNum,startNum).V is not None:
                        preinsert = linePop(objNum, startNum).V + sectionPop(objNum, startNum, endNum).A * sectionPop(objNum, startNum, endNum).dT
                        if linePop(objNum, endNum).V is not None:
                            Equ = fracEq(linePop(objNum, endNum).V, preinsert)
                            if simplify(Equ.lhs-Equ.rhs) == 0 == 0 :
                                pass  # 값 같으면 아무것도 안 함
                            else:
                                symbolIn = list(Equ.free_symbols)
                                if len(symbolIn) != 0:
                                    varEqa(symbolIn[0].name, solve(Equ, symbolIn[0])[0])
                        else:
                            linePop(objNum, endNum).V = preinsert
                    if linePop(objNum,endNum).V is not None:
                        preinsert = linePop(objNum, endNum).V - sectionPop(objNum, startNum, endNum).A * sectionPop(objNum, startNum, endNum).dT
                        if linePop(objNum, startNum).V is not None:
                            Equ = fracEq(linePop(objNum, startNum).V, preinsert)
                            if simplify(Equ.lhs-Equ.rhs) == 0 == 0:
                                pass  # 값 같으면 그대로 둠
                            else:
                                symbolIn = list(Equ.free_symbols)
                                if len(symbolIn) != 0:
                                    varEqa(symbolIn[0].name,solve(Equ,symbolIn[0])[0])
                        else:
                            linePop(objNum, startNum).V = preinsert
    print_map(Map,'한쪽 속도,시간,가속도->다른쪽 속도  v=v0+at')

    
    #종료
    '''for objNum in range(len(Map)):
        for startNum in range(len(Map[objNum][0])):
            for endNum in range(startNum+1,len(Map[objNum][0])):'''
    # Example usage
    print_map(Map,'======================================================================')
    yaho += 1
