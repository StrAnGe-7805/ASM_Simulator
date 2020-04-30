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

f = open('./file.asm',mode="r")
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

class instructions:
    global registers
    global status
    global address
    global dt
    global data
    stats = 0

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
            registers[self.load[1][1]][int(self.load[1][2])] = data[int((int(self.load[2][:-5]) + int(registers[self.load[2][-3]][int(self.load[2][-2])],0))/4)]
            status[self.load[1][1]][int(self.load[1][2])] = 0
        elif(self.load[0] == "sw"):
            data[int((int(self.load[2][:-5]) + int(registers[self.load[2][-3]][int(self.load[2][-2])],0))/4)] = registers[self.load[1][1]][int(self.load[1][2])]

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
                    ins[i].mem()
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