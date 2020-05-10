registers = {'s':['0x0','0x0','0x0','0x0','0x0','0x0','0x0','0x0'],'t':['0x0','0x0','0x0','0x0','0x0','0x0','0x0','0x0','0x0','0x0'],'a':['0x0','0x0','0x0','0x0'],'v':['0x0','0x0'],'z':['0x0'] , 'g':['0x0','0x0','0x0','0x0','0x0','0x0'] , 'ra':['0x0']}
status = {'s':[0,0,0,0,0,0,0,0],'t':[0,0,0,0,0,0,0,0,0,0],'a':[0,0,0,0],'v':[0,0],'z':[0] , 'g':[0,0,0,0,0,0] , 'ra':[0]}
fn1 = []
fn = []
k = 1
data = []
dt = {}
address = []
cycles = []
ins = []
line = {}
No_of_stalls = 0
gig = 0
cache_mem_1 = int(input("size of level 1 cache(in bytes): "))
associativity_1 = int(input("associativity of level 1 cache: "))
cache_mem_2 = int(input("size of level 2 cache(in bytes): "))
associativity_2 = int(input("associativity of level 2 cache: "))
block_size = int(input("Block size(in bytes): "))
f_cache_1 = int(input("access latency of level 1 cache: "))
f_cache_2 = int(input("access latency of level 2 cache: "))
f_memory = int(input("access latency of memory: "))
granted = 0

f = open('/Users/gamemaster/Documents/ASM_sim/file.asm',mode="r")
f1 = f.readlines()
for x in range(len(f1)):
    f1[x]=f1[x].replace('$zero','$z0')
for x in f1:
    if(len(x) != 1):
        fn1.append(x)

for x in fn1:
    p = x.replace(',',' ').split()
    if(p[0][-1] == ':'):
        line[p[0][:-1]] = len(fn)
    fn.append(x.replace(',',' ').split())

if(fn[0] != ['.data']):
    print('ERROR :  .data not found')
    gig = 1
if(gig == 0):
    if(['.text'] not in fn):
        print('ERROR : .text not found')
        gig = 1

if(gig == 0):
    while(fn[k][0] != ".text"):
        if(fn[k][0] == ".word"):
            for i in range(1,len(fn[k])):
                data.append(hex(int(fn[k][i])))
        elif(fn[k][0] == ".ascizz"):
            st = fn1[k].replace(',',' ').split('"')
            for i in range(1,len(st)):
                if(st[i] != '' and st[i] != ' ' and st[i] != '\n'):
                    data.append(st[i])
        else:
            st = fn[k][0][:-1]
            dt[st] = hex(len(data))
            address.append(st)
            if(len(fn[k]) == 1):
                k = k + 1
                if(fn[k][0] == ".word"):
                    for i in range(1,len(fn[k])):
                        data.append(hex(int(fn[k][i])))
                elif(fn[k][0] == ".ascizz"):
                    st = fn1[k].replace(',',' ').split('"')
                    for i in range(1,len(st)):
                        if(st[i] != '' and st[i] != ' ' and st[i] != '\n'):
                            data.append(st[i])
            else:
                if(fn[k][1] == ".word"):
                    for i in range(2,len(fn[k])):
                        data.append(hex(int(fn[k][i])))
                elif(fn[k][1] == ".ascizz"):
                    st = fn1[k].replace(',',' ').split('"')
                    for i in range(2,len(st)):
                        if(st[i] != '' and st[i] != ' ' and st[i] != '\n'):
                            data.append(st[i])
        k = k + 1
if(len(data) > 1000):
    print('Excess Memory provided')
    gig = 1
if(gig == 0):
    if(fn[k+1] != ['.globl','main']):
        print('ERROR: .globl main not found')
        gig = 1
    if(gig == 0 and fn[k+2] != ['main:']):
        print('ERROR: main: not found')
        gig = 1
k = k + 3

class cache:
    global cache_mem_1
    global associativity_1
    global cache_mem_2
    global associativity_2
    global block_size
    hits_1 = 0
    hits_2 = 0
    miss_1 = 0
    miss_2 = 0

    no_of_sets_1 = int(cache_mem_1/(block_size*associativity_1))
    no_of_sets_2 = int(cache_mem_2/(block_size*associativity_2))
    block = [0,0]     # tag , priority
    seti = []
    for i in range(associativity_1):
        seti.append(block)
    sets = []
    for i in range(no_of_sets_1):
        sets.append(seti)
    seti = []
    for i in range(associativity_2):
        seti.append(block)
    sets_2 = []
    for i in range(no_of_sets_2):
        sets_2.append(seti)
    nun = 0
    while block_size != 1:
        block_size = int(block_size/2)
        nun = nun + 1

    def search(self,ad):
        nuns = 0
        p = self.no_of_sets_1
        while p != 1:
            p = int(p/2)
            nuns = nuns + 1
        val = '0b' + ad[-(self.nun+nuns):-(self.nun)]
        if(val == '0b'):
            val = 0
        else:
            val = int(val,2)
        cha = '0b' + ad[:-(self.nun+nuns)]
        if(cha == '0b'):
            cha = 0
        else:
            cha = int(cha,2)
        for i in range(len(self.sets[val])):
            if(self.sets[val][i][0] == cha and self.sets[val][i][1] != 0):
                k = self.sets[val][i][1]
                for j in range(len(self.sets[val])):
                    if(self.sets[val][j][1] == k):
                        self.sets[val][j][1] = 1
                    elif(self.sets[val][j][1] < k and self.sets[val][j][1] != 0):
                        self.sets[val][j][1] = self.sets[val][j][1] + 1
                self.hits_1 = self.hits_1 + 1
                return 1
        self.miss_1 = self.miss_1 + 1
        return 0
    
    def search_2(self,ad):
        nuns = 0
        p = self.no_of_sets_2
        while p != 1:
            p = int(p/2)
            nuns = nuns + 1
        val = '0b' + ad[-(self.nun+nuns):-(self.nun)]
        if(val == '0b'):
            val = 0
        else:
            val = int(val,2)
        cha = '0b' + ad[:-(self.nun+nuns)]
        if(cha == '0b'):
            cha = 0
        else:
            cha = int(cha,2)
        for i in range(len(self.sets_2[val])):
            if(self.sets_2[val][i][0] == cha and self.sets_2[val][i][1] != 0):
                k = self.sets_2[val][i][1]
                self.sets_2[val][i][0] = 0
                self.sets_2[val][i][1] = 0
                for j in range(len(self.sets_2[val])):
                    if(self.sets_2[val][j][1] > k):
                        self.sets_2[val][j][1] = self.sets_2[val][j][1] - 1
                self.hits_2 = self.hits_2 + 1
                return 1
        self.miss_2 = self.miss_2 + 1
        return 0

    def upgrade(self,ad):
        nuns = 0
        p = self.no_of_sets_1
        while p != 1:
            p = int(p/2)
            nuns = nuns + 1
        val = '0b' + ad[-(self.nun+nuns):-(self.nun)]
        if(val == '0b'):
            val = 0
        else:
            val = int(val,2)
        cha = '0b' + ad[:-(self.nun+nuns)]
        if(cha == '0b'):
            cha = 0
        else:
            cha = int(cha,2)
        flag = 0
        for i in range(len(self.sets[val])):
            if(self.sets[val][i][1] == 0):
                self.sets[val][i][0] = cha
                for j in range(len(self.sets[val])):
                    if(self.sets[val][j][0] == cha):
                        self.sets[val][j][1] = 1
                    elif(self.sets[val][j][1] != 0):
                        self.sets[val][j][1] = self.sets[val][j][1] + 1
                flag = 1
                break
        if(flag == 0):
            k = len(self.sets[val])
            for i in range(len(self.sets[val])):
                if(self.sets[val][i][1] == k):
                    cross = self.sets[val][i][0]
                    self.sets[val][i][0] = cha
                    for j in range(len(self.sets[val])):
                        if(self.sets[val][j][1] == k):
                            self.sets[val][j][1] = 1
                        else:
                            self.sets[val][j][1] = self.sets[val][j][1] + 1
                    k = bin(cross)[2:]
                    k = '0'*(10 - nuns - self.nun - len(k)) + k
                    ka = bin(val)[2:]
                    ka = '0'*(nuns - len(ka)) + ka
                    k = k + ka + '0'*self.nun
                    return k

    def upgrade_2(self,ad):
        nuns = 0
        p = self.no_of_sets_2
        while p != 1:
            p = int(p/2)
            nuns = nuns + 1
        val = '0b' + ad[-(self.nun+nuns):-(self.nun)]
        if(val == '0b'):
            val = 0
        else:
            val = int(val,2)
        cha = '0b' + ad[:-(self.nun+nuns)]
        if(cha == '0b'):
            cha = 0
        else:
            cha = int(cha,2)
        flag = 0
        for i in range(len(self.sets_2[val])):
            if(self.sets_2[val][i][1] == 0):
                self.sets_2[val][i][0] = cha
                for j in range(len(self.sets_2[val])):
                    if(self.sets_2[val][j][0] == cha):
                        self.sets_2[val][j][1] = 1
                    elif(self.sets_2[val][j][1] != 0):
                        self.sets_2[val][j][1] = self.sets_2[val][j][1] + 1
                flag = 1
                break
        if(flag == 0):
            k = len(self.sets_2[val])
            for i in range(len(self.sets_2[val])):
                if(self.sets_2[val][i][1] == k):
                    self.sets_2[val][i][0] = cha
                    for j in range(len(self.sets_2[val])):
                        if(self.sets_2[val][j][1] == k):
                            self.sets_2[val][j][1] = 1
                        else:
                            self.sets_2[val][j][1] = self.sets_2[val][j][1] + 1
                    break   

cached = cache()

class instructions:
    global registers
    global status
    global address
    global dt
    global data
    global f_cache_1
    global f_cache_2
    global f_memory
    global cached
    stats = 0
    cop = 0
    cops = 0

    def __init__(self,load):
        self.load = load

    def ID(self):

        if(self.load[0] == "li"):
            if(len(self.load[2]) > 2):
                if(self.load[2][1] == 'x'):
                    registers[self.load[1][1]][int(self.load[1][2])] = self.load[2]
                else:
                    registers[self.load[1][1]][int(self.load[1][2])] = hex(int(self.load[2]))
            else:
                registers[self.load[1][1]][int(self.load[1][2])] = hex(int(self.load[2]))
        elif(self.load[0] == "add" or self.load[0] == "sub" or self.load[0] == "slt" or self.load[0] == "and"):
            if(status[self.load[2][1]][int(self.load[2][2])] == 1 or status[self.load[3][1]][int(self.load[3][2])] == 1):
                return 0
            else:
                status[self.load[1][1]][int(self.load[1][2])] = 1
        elif(self.load[0] == "addi"):
            if(status[self.load[2][1]][int(self.load[2][2])] == 1):
                return 0
            else:
                status[self.load[1][1]][int(self.load[1][2])] = 1
        elif(self.load[0] == "lw"):
            if(status[self.load[2][-3]][int(self.load[2][-2])] == 1):
                return 0
            else:
                status[self.load[1][1]][int(self.load[1][2])] = 1
        elif(self.load[0] == "sll"):
            if(status[self.load[2][1]][int(self.load[2][2])] == 1):
                return 0
            else:
                status[self.load[1][1]][int(self.load[1][2])] = 1
        elif(self.load[0] == "beq"):
            if(self.load[1][1] == self.load[2][1] and self.load[1][2] == self.load[2][2]):
                return self.load[3]
            if(status[self.load[1][1]][int(self.load[1][2])] != 0 or status[self.load[2][1]][int(self.load[2][2])] != 0):
                return 0
            if(int(registers[self.load[1][1]][int(self.load[1][2])],0) == int(registers[self.load[2][1]][int(self.load[2][2])],0)):
                return self.load[3] + ':'
            return 1
        elif(self.load[0] == 'bne'):
            if(int(registers[self.load[1][1]][int(self.load[1][2])],0) != int(registers[self.load[2][1]][int(self.load[2][2])],0)):
                return self.load[3] + ':'
            return 1
        elif(self.load[0] == "la"):
            if(self.load[2] in address):
                registers[self.load[1][1]][int(self.load[1][2])] = dt[self.load[2]]
            else:
                registers[self.load[1][1]][int(self.load[1][2])] = self.load[2]
        elif(self.load[0] == "lui"):
            if(len(registers[self.load[1][1]][int(self.load[1][2])]) > 6):
                registers[self.load[1][1]][int(self.load[1][2])] = self.load[2] + registers[self.load[1][1]][int(self.load[1][2])][-4:]
            else:
                registers[self.load[1][1]][int(self.load[1][2])] = hex(int(self.load[2],0) + int(registers[self.load[1][1]][int(self.load[1][2])]))

    def exe(self):
        if(self.load[0] == "add"):
            registers[self.load[1][1]][int(self.load[1][2])] = hex(int(registers[self.load[2][1]][int(self.load[2][2])],0) + int(registers[self.load[3][1]][int(self.load[3][2])],0))
            status[self.load[1][1]][int(self.load[1][2])] = 2
        elif(self.load[0] == "sub"):
            registers[self.load[1][1]][int(self.load[1][2])] = hex(int(registers[self.load[2][1]][int(self.load[2][2])],0) - int(registers[self.load[3][1]][int(self.load[3][2])],0))
            status[self.load[1][1]][int(self.load[1][2])] = 2
        elif(self.load[0] == "addi"):
            registers[self.load[1][1]][int(self.load[1][2])] = hex(int(registers[self.load[2][1]][int(self.load[2][2])],0) + int(self.load[3]))
            status[self.load[1][1]][int(self.load[1][2])] = 2
        elif(self.load[0] == "slt"):
            if(int(registers[self.load[2][1]][int(self.load[2][2])],0) < int(registers[self.load[3][1]][int(self.load[3][2])],0)):
                registers[self.load[1][1]][int(self.load[1][2])] = hex(1)
            else:
                registers[self.load[1][1]][int(self.load[1][2])] = hex(0)
            status[self.load[1][1]][int(self.load[1][2])] = 2
        elif(self.load[0] == "sll"):
            registers[self.load[1][1]][int(self.load[1][2])] = hex(int(registers[self.load[2][1]][int(self.load[2][2])],0) * (2**int(self.load[3])))
            status[self.load[1][1]][int(self.load[1][2])] = 2

    def mem(self):
        if(self.load[0] == "add"):
            status[self.load[1][1]][int(self.load[1][2])] = 0
        elif(self.load[0] == "sub"):
            status[self.load[1][1]][int(self.load[1][2])] = 0
        elif(self.load[0] == "addi"):
            status[self.load[1][1]][int(self.load[1][2])] = 0
        elif(self.load[0] == "slt"):
            status[self.load[1][1]][int(self.load[1][2])] = 0
        elif(self.load[0] == "sll"):
            status[self.load[1][1]][int(self.load[1][2])] = 0
        if(self.load[0] == "lw"):
            if(self.cop == 0):
                ad = int(self.load[2][:-5]) + int(registers[self.load[2][-3]][int(self.load[2][-2])],0)
                ad = bin(ad)[2:]
                ad = '0'*(10 - len(ad)) + ad
                if(cached.search(ad) == 1):
                    self.cop = 1
                else:
                    if(cached.search_2(ad) == 1):
                        self.cop = 2
                        kop = cached.upgrade(ad)
                        cached.upgrade_2(kop)
                    else:
                        self.cop = 3
                        kop = cached.upgrade(ad)
                        if(kop != None):
                            cached.upgrade_2(ad)
            if(self.cop == 1):
                self.cops = self.cops + 1
                if(self.cops == f_cache_1):
                    registers[self.load[1][1]][int(self.load[1][2])] = data[int((int(self.load[2][:-5]) + int(registers[self.load[2][-3]][int(self.load[2][-2])],0))/4)]
                    status[self.load[1][1]][int(self.load[1][2])] = 0
                else:
                    return 0
            elif(self.cop == 2):
                self.cops = self.cops + 1
                if(self.cops == (f_cache_1 + f_cache_2)):
                    registers[self.load[1][1]][int(self.load[1][2])] = data[int((int(self.load[2][:-5]) + int(registers[self.load[2][-3]][int(self.load[2][-2])],0))/4)]
                    status[self.load[1][1]][int(self.load[1][2])] = 0
                else:
                    return 0
            elif(self.cop == 3):
                self.cops = self.cops + 1
                if(self.cops == (f_cache_1 + f_cache_2 + f_memory)):
                    registers[self.load[1][1]][int(self.load[1][2])] = data[int((int(self.load[2][:-5]) + int(registers[self.load[2][-3]][int(self.load[2][-2])],0))/4)]
                    status[self.load[1][1]][int(self.load[1][2])] = 0
                else:
                    return 0
        elif(self.load[0] == "sw"):
            if(self.cop == 0):
                ad = int(self.load[2][:-5]) + int(registers[self.load[2][-3]][int(self.load[2][-2])],0)
                ad = bin(ad)[2:]
                ad = '0'*(10 - len(ad)) + ad
                if(cached.search(ad) == 1):
                    self.cop = 1
                else:
                    if(cached.search_2(ad) == 1):
                        self.cop = 2
                        kop = cached.upgrade(ad)
                        cached.upgrade_2(kop)
                    else:
                        self.cop = 3
                        kop = cached.upgrade(ad)
                        if(kop != None):
                            cached.upgrade_2(ad)
            if(self.cop == 1):
                self.cops = self.cops + 1
                if(self.cops == f_cache_1):
                    data[int((int(self.load[2][:-5]) + int(registers[self.load[2][-3]][int(self.load[2][-2])],0))/4)] = registers[self.load[1][1]][int(self.load[1][2])]
                else:
                    return 0
            elif(self.cop == 2):
                self.cops = self.cops + 1
                if(self.cops == (f_cache_1 + f_cache_2)):
                    data[int((int(self.load[2][:-5]) + int(registers[self.load[2][-3]][int(self.load[2][-2])],0))/4)] = registers[self.load[1][1]][int(self.load[1][2])]
                else:
                    return 0
            elif(self.cop == 3):
                self.cops = self.cops + 1
                if(self.cops == (f_cache_1 + f_cache_2 + f_memory)):
                    data[int((int(self.load[2][:-5]) + int(registers[self.load[2][-3]][int(self.load[2][-2])],0))/4)] = registers[self.load[1][1]][int(self.load[1][2])]
                else:
                    return 0

    def wb(self):
        if(self.load[0] == 'lw'):
            status[self.load[1][1]][int(self.load[1][2])] = 0

if(gig == 0):
    while True:
        flag = 1
        if(len(ins) > 1 and ins[-1].load[0] == "jr" and ins[-1].stats == 5):
            break
        cycles.append([])
        if(len(ins) == 0):
            if(fn[k][0][-1] == ":"):
                ins.append(instructions(fn[k][1:]))
            else:
                ins.append(instructions(fn[k]))
            ins[0].stats = 1
            cycles[-1].append(" IF  ")
            flag = 0
        else:
            for i in range(len(ins)):
                if(ins[i].stats == 1):
                    jass = ins[i].ID()
                    if(jass == 0):
                        cycles[-1].append('STALL')
                        No_of_stalls = No_of_stalls + 1
                        break
                    elif(jass == 1):
                        cycles[-1].append('STALL')
                        No_of_stalls = No_of_stalls + 1
                        ins[i].stats = 2
                        break
                    elif(jass != None and jass[-1] == ':'):
                        cycles[-1].append(' ID  ')
                        cycles[-1].append('STALL')
                        No_of_stalls = No_of_stalls + 1
                        k = line[jass[:-1]]
                        ins[i].stats = 2
                        break
                    elif(jass != None):
                        cycles[-1].append(' ID  ')
                        ins[i].stats = 2
                        k = line[jass]
                    else:
                        cycles[-1].append(' ID  ')
                        ins[i].stats = 2
                elif(ins[i].stats == 2):
                    ins[i].exe()
                    cycles[-1].append(' EXE ')
                    ins[i].stats = 3
                elif(ins[i].stats == 3):
                    jass = ins[i].mem()
                    if(jass == 0):
                        cycles[-1].append('STALL')
                        No_of_stalls = No_of_stalls + 1
                        break
                    else:
                        cycles[-1].append(' MEM ')
                        ins[i].stats = 4
                elif(ins[i].stats == 4):
                    #ins[i].wb()
                    cycles[-1].append(' WB  ')
                    ins[i].stats = 5
                else:
                    cycles[-1].append(" ")
            if(cycles[-1][-1] != 'STALL' and ins[-1].load[0] != 'jr'):
                if(fn[k][0][-1] == ":"):
                    if(len(fn[k]) > 1):
                        ins.append(instructions(fn[k][1:]))
                        if(fn[k][1] == 'j'):
                            k = line[fn[k][2]] - 1
                    else:
                        k = k + 1
                        ins.append(instructions(fn[k]))
                        if(fn[k][0] == 'j'):
                            k = line[fn[k][1]] - 1
                else:
                    ins.append(instructions(fn[k]))
                    if(fn[k][0] == 'j'):
                        k = line[fn[k][1]] - 1
                ins[-1].stats = 1
                cycles[-1].append(" IF  ")
                flag = 0
        if(ins[-1].load[0] != 'jr' and flag == 0):
            k = k + 1
    kick = '=============================================================================='
    print(kick)
    kick = '````````  =   =  =      =  =   =  =       = =   = = =   = =   = = =   ````````'
    print(kick)
    kick = '```````` = =  =  = =  = =  =   =  =      =   =    =    =   =  =    =  ````````'
    print(kick)
    kick = '```````` =    =  =   =  =  =   =  =      =   =    =    =   =  =   =   ````````'
    print(kick)
    kick = '````````  =   =  =      =  =   =  =      = = =    =    =   =  =  =    ````````'
    print(kick)
    kick = '````````   =  =  =      =  =   =  =      =   =    =    =   =  =   =   ````````'
    print(kick)
    kick = '```````` = =  =  =      =  =   =  =      =   =    =    =   =  =    =  ````````'
    print(kick)
    kick = '````````  =   =  =      =   = =   = = =  =   =    =     = =   =     = ````````'
    print(kick)
    kick = '=============================================================================='
    print(kick)
    print('')
    print('No. of Instructions executed = ' + str(len(ins)))
    print('No. of Cycles = ' + str(len(cycles)))
    print('No. of Stalls = ' + str(No_of_stalls))
    print('IPC =',(len(ins)/(len(ins) + No_of_stalls)))
    access = cached.hits_1 + cached.miss_1
    H1 = cached.hits_1/access
    H2 = cached.hits_2/access
    mr1 = (access - cached.hits_1)/access
    mr2 = (access - cached.hits_2)/access
    print("Tavg =",H1*f_cache_1 + mr1*(H2*f_cache_2 + mr2*f_memory))
    print('Memory  [0x10010000]   ',end='')
    j = 0
    for i in range(len(data)):
        j = i
        kick = '0'*(10-len(data[i]))
        print(kick + data[i][2:] + '   ',end='')
        if(i%4 == 3):
            print('')
            print('                       ',end='')
    while(j%4 != 3):
        print('00000000   ',end='')
        j = j + 1
    print('')
    print('0 - Quit\n1 - Cycles( needs huge display )')
    kick = int(input())
    if(kick == 1):
        for i in range(len(cycles[-1])):
            for j in range(len(cycles)):
                if(i >= len(cycles[j])):
                    print('     ',end='')
                else:
                    print(cycles[j][i],end='')
            print('')
    print('=================================== :) :) :) ==================================')