import math
import numpy


maximum=0
critical = 0
theTest={}
for i in range(1,129):
    theTest[i]=0
theTerms = [[]]


def append2Aleph(Aleph,Bet:int):
    return numpy.concatenate((Aleph,numpy.array([Bet])))


def calS(binary:int): #Summon Binary && Make it Aleph
    #Bet θ:0,0:1,1:-1
    #Aleph array([Bet,Bet,...,Bet])

    #Binarize
    outputAleph = []
    for i in range(0,int(math.log2(binary))+1): #[0,i승자리의i]
        outputBet = binary%(2**(i+1))
        binary -= outputBet
        outputAleph.append(outputBet)
    outputAleph.reverse()

    #Alepharize
    for i in range(0,len(outputAleph)):
        if outputAleph[i] == 0:
            outputAleph[i] = 1
        else:
            outputAleph[i] = -1

    return numpy.array(outputAleph)
                  

def calT(binary:int): #Summon Terms
    #Terms [[Aleph,Aleph],...,[Aleph,Aleph]]
    outputTerms = []
    Llist = calS(binary) #type==Aleph
    Rlist = numpy.array([0])

    LlistLen = len(Llist)
    for i in range(0,LlistLen):
        Rlist = append2Aleph(Rlist,Llist[0])
        Llist = numpy.delete(Llist,0) if i+1<LlistLen else numpy.array([0])
        outputTerms.append([Llist.copy(),Rlist.copy()])

    return outputTerms
    
def getT(binary:int):
    if len(theTerms)>binary:
        return theTerms[binary]
    else:
        theTerms.append(calT(binary))
        return theTerms[binary]


def calC(a:list,b:list): #Calculate Alephs
    #a:Aleph, b:Aleph
    ternA = 0
    ternB = 0
    aa = a.copy()
    bb = b.copy()
    outputAleph = numpy.array([])
    isFail = False
    if len(aa)==len(bb):
        if (aa==bb).all():
            return a
    while True:
        # 0,0 이면 0 next
        # 1,1 이면 1 next
        # 0,1 이면 1 next
        # -1,-1 이면 -1 next
        # 0,-1 이면 0후에 -1인지 확인 -1 nextnext,next
        # 1,-1 이면 -1전에 0이었는지 확인 1 next,again 엘스 에프
        if aa[ternA]==-1 or bb[ternB]==-1:
            if aa[ternA]==bb[ternB]:
                outputAleph=append2Aleph(outputAleph,-1)
            elif aa[ternA] == 0:                  #0,-1
                if ternA+1<len(a):
                    if aa[ternA+1]==-1:
                        outputAleph=append2Aleph(outputAleph,-1)
                        ternA+=1
                    else:
                        isFail = True
                        break #F
                else:
                    isFail = True
                    break #F
            elif bb[ternB] == 0:                #-1,0
                if ternB+1<len(b):
                    if bb[ternB+1]==-1:
                        outputAleph=append2Aleph(outputAleph,-1)
                        ternB+=1
                    else:
                        isFail = True
                        break #F
                else:
                    isFail = True
                    break #F
            elif aa[ternA] == -1:               #-1,1
                if ternA>0:
                    if aa[ternA-1]==0:
                        outputAleph=append2Aleph(outputAleph,1)
                        ternA -=1
                    else:
                        isFail = True
                        break #F
                else:
                    isFail = True
                    break #F
            else:                               #1,-1
                if ternB>0:
                    if bb[ternB-1]==0:
                        outputAleph=append2Aleph(outputAleph,1)
                        ternB -=1
                    else:
                        isFail = True
                        break #F
                else:
                    isFail = True
                    break #F
        else:
            outputAleph=append2Aleph(outputAleph,aa[ternA]+bb[ternB])

        # 원소딱맞으면 브레이크(성공)
        # 원소부족하면 전에 0이었는지 확인 0추가 엘이프 상대가 0이면 브레이크(성공) 엘스 에프
        
        ternA += 1
        ternB += 1
        if ternA==len(aa) and ternB==len(bb):
            break #S
        if ternA==len(aa):
            if aa[ternA-1]==0:
                aa=append2Aleph(aa,0)
            elif bb[ternB]==0:
                break #S
            else:
                isFail = True
                break #F
        if ternB==len(bb):
            if bb[ternB-1]==0:
                bb=append2Aleph(bb,0)
            elif aa[ternA]==0:
                break #S
            else:
                isFail = True
                break #F
    if isFail:
        return
    else:
        return numpy.clip(outputAleph,-1,1)


def calF(binary:int,Ldice,Rdice): #Flow calC
    global maximum
    if binary>100:
        for i in theTest:
            print(theTest[i])
        print(maximum)

    
    #문제는 뭐다? 이전 조건을 만족시키지 않는 dice를 살림.
    #dumy에 dice를 append해야 하는데 face가 append?

    #print('                             ',Ldice,Rdice)
    #output Ldice,Rdice,maxbinary if one of the dice filled max
    #terms  ㅡ>each_dice    ㅡ>if F conti else dice=dice , calF
    #start at calF(1,?,?)
    facenumber = 6
    output =[]
    
    for terms in getT(binary): #terms [Aleph,Aleph]
        outload=False
        Fs = [True,True,True,True]
        dumies = [[],[],[],[]] #[[dice,dice,...,dice],L(1),R(0),R(1)] calC성공한 dice들
        #print('                             ',binary,terms)
        
        # dumies에 face 하나가 calC된 dice들을 넣는다
        # 만일 아무face도 calC되지 않으면 다음을 시도한다
        # dice가 다 차면 기록저장 else 그냥 넣기
        for i in range(0,len(Ldice)): #dumies[0]에 calC된 dice 넣고
            L = Ldice.copy()
            L[i] = calC(terms[0],L[i])
            if L[i] is None:
                continue
            isalready=False
            for dice in dumies[0]:
                for l in L:
                    for d in dice:
                        if (calC(l,d) is not None) and len(l)<=len(d):
                            isalready=True
                            break
                    if isalready:
                        break
            if not isalready:
                Fs[0] = False
                dumies[0].append(L)
        for i in range(0,len(Ldice)):
            L = Ldice.copy()
            L[i] = calC(terms[0][::-1],L[i])
            if L[i] is None:
                continue
            isalready=False
            for dice in dumies[0]:
                for l in L:
                    for d in dice:
                        if (calC(l,d) is not None) and len(l)<=len(d):
                            isalready=True
                            break
                    if isalready:
                        break
            if not isalready:
                Fs[0] = False
                dumies[0].append(L)
        for i in range(0,len(Ldice)):
            L = Ldice.copy()
            L[i] = calC(terms[1],L[i])
            if L[i] is None:
                continue
            isalready=False
            for dice in dumies[1]:
                for l in L:
                    for d in dice:
                        if (calC(l,d) is not None) and len(l)<=len(d):
                            isalready=True
                            break
                    if isalready:
                        break
            if not isalready:
                Fs[1] = False
                dumies[1].append(L)
        for i in range(0,len(Ldice)):
            L = Ldice.copy()
            L[i] = calC(terms[1][::-1],L[i])
            if L[i] is None:
                continue
            isalready=False
            for dice in dumies[1]:
                for l in L:
                    for d in dice:
                        if (calC(l,d) is not None) and len(l)<=len(d):
                            isalready=True
                            break
                    if isalready:
                        break
            if not isalready:
                Fs[1] = False
                dumies[1].append(L)
        for i in range(0,len(Rdice)):
            R = Rdice.copy()
            R[i] = calC(terms[0],R[i])
            if R[i] is None:
                continue
            isalready=False
            for dice in dumies[2]:
                for r in R:
                    for d in dice:
                        if (calC(r,d) is not None) and len(r)<=len(d):
                            isalready=True
                            break
                    if isalready:
                        break
            if not isalready:
                Fs[2] = False
                dumies[2].append(R)
        for i in range(0,len(Rdice)):
            R = Rdice.copy()
            R[i] = calC(terms[0][::-1],R[i])
            if R[i] is None:
                continue
            isalready=False
            for dice in dumies[2]:
                for r in R:
                    for d in dice:
                        if (calC(r,d) is not None) and len(r)<=len(d):
                            isalready=True
                            break
                    if isalready:
                        break
            if not isalready:
                Fs[2] = False
                dumies[2].append(R)
        for i in range(0,len(Rdice)):
            R = Rdice.copy()
            R[i] = calC(terms[1],R[i])
            if R[i] is None:
                continue
            isalready=False
            for dice in dumies[3]:
                for r in R:
                    for d in dice:
                        if (calC(r,d) is not None) and len(r)<=len(d):
                            isalready=True
                            break
                    if isalready:
                        break
            if not isalready:
                Fs[3] = False
                dumies[3].append(R)
        for i in range(0,len(Rdice)):
            R = Rdice.copy()
            R[i] = calC(terms[1][::-1],R[i])
            if R[i] is None:
                continue
            isalready=False
            for dice in dumies[3]:
                for r in R:
                    for d in dice:
                        if (calC(r,d) is not None) and len(r)<=len(d):
                            isalready=True
                            break
                    if isalready:
                        break
            if not isalready:
                Fs[3] = False
                dumies[3].append(R)

        #채우기 실패시 그냥 넣기 시도
        if Fs[0]: #0 실패
            #다 찼으면 기록저장 else 넣기
            if len(Ldice)<facenumber:
                dumies[0].append(Ldice + [terms[0]])
            else:
                #Ldice는 모두 막힘 Rdice와 짝지어 기록저장
                outload=True #return 지금 쓰면 안될듯 다음것들도 포함시켜야하나
        if Fs[3]: #3 실패
            #다 찼으면 기록저장 else 넣기
            if len(Rdice)<facenumber:
                dumies[3].append(Rdice + [terms[1]])
            else:
                #Ldice는 모두 막힘 Rdice와 짝지어 기록저장
                outload=True
        if Fs[1]: #1 실패
            #다 찼으면 기록저장 else 넣기
            if len(Ldice)<facenumber:
                dumies[1].append(Ldice + [terms[1]])
            else:
                #Rdice는 모두 막힘 Ldice와 짝지어 기록저장
                if outload:
                    return [[binary-1,Ldice,Rdice]]
        if Fs[2]: #2 실패
            #다 찼으면 기록저장 else 넣기
            if len(Rdice)<facenumber:
                dumies[2].append(Rdice + [terms[0]])
            else:
                #Rdice는 모두 막힘 Ldice와 짝지어 기록저장
                if outload:
                    return [[binary-1,Ldice,Rdice]]
        
        #calF
        #하위calF의 output추가
        
        '''
        print(Fs)
        for dumy in dumies:
            k = []
            for d in dumy:
                l = []
                for f in d:
                    l.append(f.tolist())
                k.append(l)
            print(k)
        '''
        for Ldumy in dumies[0]:
            for Rdumy in dumies[3]:
                #print(Ldumy,Rdumy)
                F=calF(binary+1,Ldumy,Rdumy)
                if F is not None and binary>maximum:
                    maximum=F[0][0]
                if binary>critical:
                    output+=F
                theTest[binary]+=1
                #print(binary)
        for Ldumy in dumies[1]:
            for Rdumy in dumies[2]:
                F=calF(binary+1,Ldumy,Rdumy)
                if F is not None and binary>maximum:
                    maximum=F[0][0]
                if binary>critical:
                    output+=F
                theTest[binary]+=1
                #print(binary)
    return output


def calM(): #Main Calculation 
    F = calF(1,[],[])
    maxBinary = 0
    output = []
    outoutput = []
    for f in F:
        if f[0]>maxBinary:
            maxBinary = f[0]
            output = [f]
        elif f[0]==maxBinary:
            output.append(f)

    for f in output:
        outoutput.append([f[0],[],[]])
        for face in f[1]:
            outoutput[-1][1].append(face.tolist())
        for face in f[2]:
            outoutput[-1][2].append(face.tolist())
        
    return outoutput


length=0
for i in calM():
    print(i)
    length+=1
print(length)
print()
for i in theTest:
    print(theTest[i])
'''
for i in range(1,8):
    print(getT(i))
'''