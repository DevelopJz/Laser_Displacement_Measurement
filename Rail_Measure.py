from serial import Serial
import os
import csv
import time
import numpy as np
import RPi.GPIO as GPIO
import matplotlib.pyplot as plt

#------------------------------------------------------------------------------
#Initial Value

findflag=0
countflag=1
countstat=0
oflag=0
endcount=0
f=1
j=0
co=0
tempV=0
RED=11
GREEN=13
BLUE=15

rowlist=["Num"]
raw_list=[]
firstlist=[]
tlist=[]
dlist=[]
filterlist=[]
noisef=[]
fixlist=[]

Pmode_lift=12
low=1
high=7
id_safe=5
id_warn=4.7
id_chan=4.5
id_dang=4

#-----------------------------------------------------------------------------
#Make Graph

def makegraph():
    global path, f
    t=[]
    x=[]
    alist=[]
    glist=[]
    tlist=[]
    i=0
    j=1
    h=1
    png=1
    
    with open(path+"LSM_Test/Test"+str(f)+"/Magnet_Data.csv","r") as d:
        line=d.readline()
        lines=d.readlines()
        leng=len(line.split(","))
        while len(lines)!=i:
            while len(line.split(","))!=j:
                x.append(lines[i].split(",")[j])
                j=j+1
            alist.append(x)
            x=[]
            j=1
            i=i+1
    
    line=line.replace("\n","")
    wid=int((leng-1)%4)
    mul=int((leng-1)/4)
    plt.figure(figsize=(16,10))
    
    for k in range(len(alist)):
        alist[k][-1]=alist[k][-1].replace("\n","")
    
    for gl in range(leng-1):
        glist.append([])
    
    for l in range(leng-1):
        for a in range(len(alist)):
            glist[l].append(alist[a][l])
            
    tlist=glist
    for t in range(len(glist)):
        tlist[t]=list(filter(None,tlist[t]))
        
    for c in range(len(tlist)):
        for d in range(len(tlist[c])):
            tlist[c][d]=float(tlist[c][d])
    
    for g in range(leng-1):
        print(leng,wid,mul)
        if leng<=4:
            plt.subplot(int(str(leng-1)+"1"+str(g+1)))
            plt.title(line.split(',')[g+1])
            plt.xlabel("measure num")
            plt.xticks(range(0,len(tlist[g]),500))
            plt.ylabel("Height (mm)")
            plt.ylim(4,6.2)
            plt.yticks(np.arange(4,6.2,0.2))
            plt.grid()
            plt.plot(range(0,len(tlist[g])),tlist[g],"r")
    
            plt.subplots_adjust(hspace=0.42)
            plt.savefig(path+"LSM_Test/Test"+str(f)+"/Magnet_Data_graph.png")
        else:
            if wid==0:
                plt.subplot(int("41"+str(h)))
                plt.cla()
                plt.title(line.split(',')[g+1])
                plt.xlabel("measure num")
                plt.xticks(range(0,len(tlist[g]),500))
                plt.ylabel("Height (mm)")
                plt.ylim(4,6.2)
                plt.yticks(np.arange(4,6.2,0.2))
                plt.grid()
                plt.plot(range(0,len(tlist[g])),tlist[g],"r")
                
                plt.subplots_adjust(hspace=0.42)
                plt.savefig(path+"LSM_Test/Test"+str(f)+"/Magnet_Data_graph_"+str(png)+".png")
            else:
                if mul==0:
                    plt.subplot(int(str(wid)+"1"+str(h)))
                    plt.cla()
                else:
                    plt.subplot(int("41"+str(h)))
                    plt.cla()
                plt.title(line.split(',')[g+1])
                plt.xlabel("measure num")
                plt.xticks(range(0,len(tlist[g]),500))
                plt.ylabel("Height (mm)")
                plt.ylim(4,6.2)
                plt.yticks(np.arange(4,6.2,0.2))
                plt.grid()
                plt.plot(range(0,len(tlist[g])),tlist[g],"r")
                
                plt.subplots_adjust(hspace=0.42)
                plt.savefig(path+"LSM_Test/Test"+str(f)+"/Magnet_Data_graph_"+str(png)+".png")
        if mul>0:
            if h>3:
                h=1
                mul=mul-1
                png=png+1
            else:
                h=h+1
        else:
            if h>wid-1:  
                png=png+1
            else:
                h=h+1

#------------------------------------------------------------------------------
#Folder & File Make

path="/mnt/usb/"

while True:
    if not os.path.isdir(path+"LSM_Test"):
        os.mkdir(path+"LSM_Test")
    else:
        pass
    
    if not os.path.isdir(path+"LSM_Test/Test"+str(f)):
        os.mkdir(path+"LSM_Test/Test"+str(f))
        break
    else:
        f=f+1

with open(path+"LSM_Test/Test"+str(f)+"/Magnet_Data.csv","w",newline="") as m:
    pass

with open(path+"LSM_Test/Test"+str(f)+"/Magnet_Result.txt","w",newline="") as r:
    pass

with open(path+"LSM_Test/Test"+str(f)+"/Magnet_raw.csv","w",newline="") as raw:
    write=csv.writer(raw)
    write.writerow(["Num","Raw"])
    pass

#------------------------------------------------------------------------------
#GPIO Setting

GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)
GPIO.setup(RED,GPIO.OUT,initial=GPIO.LOW)
GPIO.setup(GREEN,GPIO.OUT,initial=GPIO.LOW)
GPIO.setup(BLUE,GPIO.OUT,initial=GPIO.LOW)

#------------------------------------------------------------------------------
#Arduino Serial

mega=Serial(port="/dev/ttyACM0",baudrate=2000000,)

def Decode(A):
    try:
        A=A.decode()
        t1=A[:1]
        t2=A[2:-2]
    except UnboundLocalError:
        pass
    return t1, t2

def Ardread():
    if mega.readable():
        res=mega.readline()
        code=Decode(res)
        return code
    else:
        print("Read Error (Ardread)")
        pass
        
#------------------------------------------------------------------------------
#Value Find

def find_index(data,target):
    res=[]
    lis=data
    while True:
        try:
            res.append(lis.index(target)+(res[-1]+1 if len(res)!=0 else 0))
            lis=data[res[-1]+1:]
        except:
            break
    return res

#------------------------------------------------------------------------------
#Data To File

def dtf(rawlist,lift):
    global findflag, fixlist, j, dlist, co, autoflag
    print("Data to File...")
    while True:
        while j<len(rawlist):
            if findflag==0:
                if rawlist[j]>high or rawlist[j]<low:
                    rawlist[j]="E"
                    findflag=1
                else:
                    findflag=0
            else:
                if rawlist[j]>high or rawlist[j]<low:
                    rawlist[j]="K"
                    findflag=1
                else:
                    findflag=0
            j=j+1
        try:
            rawlist.remove("K")
        except ValueError:
            break
        
    rawlist.pop(0)
    rawlist.pop(-1)
    raw_index=find_index(rawlist,"E")
    fixlist.append(rawlist[:raw_index[0]])
    for i in range(0,len(raw_index)-1,1):
        fixlist.append(rawlist[raw_index[i]+1:raw_index[i+1]])
    fixlist.append(rawlist[raw_index[-1]+1:])
    
    for r in range(len(fixlist)):
        fixlist[r].remove(max(fixlist[r]))
        fixlist[r].remove(min(fixlist[r]))
    
    for t in range(len(fixlist)):
        tlist.append(len(fixlist[t]))
        rowlist.append("Magnet "+str(t+1))
    a=max(tlist)
    
    for h in range(len(fixlist)):
        while True:
            if len(fixlist[h])<a:
                fixlist[h].append(None)
            else:
                break
    
    fixlist.pop(int(lift))
    fixlist=fixlist[1:]
    
    with open(path+"LSM_Test/Test"+str(f)+"/Magnet_Data.csv","a",encoding='utf-8',newline='') as c:
        write=csv.writer(c)
        rowlist.pop(lift)
        rowlist.pop(1)
        write.writerow(rowlist)
        while co!=a:
            dlist.append(co)
            for p in range(len(fixlist)):
                dlist.append(fixlist[p][co])
            write.writerow(dlist)
            dlist=[]
            co=co+1
            
    with open(path+"LSM_Test/Test"+str(f)+"/Magnet_Result.txt","a",encoding='utf-8') as r:
        r.write("전자석 분석 파일\n\n")
        for l in range(len(fixlist)):
            fixlist[l]=list(filter(None.__ne__,fixlist[l]))
            r.write(rowlist[l+1]+"\n")
            r.write("데이터 개수 : "+str(tlist[l])+"\n")
            r.write("Max : "+str(np.max(fixlist[l]))+"\n")
            r.write("Min : "+str(np.min(fixlist[l]))+"\n")

def saveraw(rawraw):
    with open(path+"LSM_Test/Test"+str(f)+"/Magnet_raw.csv","a",encoding='utf-8') as raw:
        write=csv.writer(raw)
        for ro in range(len(rawraw)):
            write.writerow([ro,rawraw[ro]])

def makerawfix(lst):
    global filterlist, noisef, tempV
    with open(path+"LSM_Test/Test"+str(f)+"/Magnet_raw_all.csv","w",encoding='utf-8') as rawW:
        write=csv.writer(rawW)
        write.writerow(["Num","Raw"])
        for k in range(len(lst)):
            if (lst[k]>4.3 and lst[k]<6) or lst[k]>9:
                filterlist.append(lst[k])
            else:
                pass
        for p in range(1,len(filterlist)):
            if filterlist[p]>8:
                noisef.append(filterlist[p])
            else:
                if tempV==0:
                    if (abs(filterlist[p-1]-filterlist[p])<0.4 or abs(filterlist[p-1]-filterlist[p])>3):
                        noisef.append(filterlist[p-1])
                    else:
                        tempV=filterlist[p-1]
                else:
                    if (abs(filterlist[p-1]-filterlist[p])<0.4 or abs(filterlist[p-1]-filterlist[p])>3):
                        noisef.append(filterlist[p])
                        tempV=0
                    else:
                        pass
        for ra in range(len(noisef)):
            write.writerow([ra,noisef[ra]])
        
            

#------------------------------------------------------------------------------
#Main Code

def main():
    global countflag, countstat, oflag, endcount, autoflag
    time.sleep(3)
    print("Start")
    print("count : 1\n")
    while True:
        GPIO.output(BLUE,True)
        autoflag,value=Ardread()
        if value=="-0.0":
            value="0.0"
        else:
            pass
        try:
            autoflag=int(autoflag)
            value=float(value)
            raw_list.append(value)
            if autoflag==1:
                if endcount!=100:
                    autoflag=int(autoflag)
                    value=float(value)
                    raw_list.append(value)
                    endcount=endcount+1
                else:
                    saveraw(raw_list)
                    makerawfix(raw_list)
                    GPIO.output(RED,True)
                    GPIO.output(GREEN,True)
                    GPIO.output(BLUE,False)
                    dtf(noisef,Pmode_lift)
                    time.sleep(2)
                    GPIO.output(RED,False)
                    GPIO.output(GREEN,False)
                    GPIO.output(BLUE,False)
                    break
            else:
                if countstat==0:
                    if oflag==0:
                        if value>high or value<low:
                            countstat=1
                            oflag=1
                        else:
                            pass
                    elif oflag==1:
                        if value>high or value<low:
                            countstat=1
                        else:
                            oflag=0
                            countstat=0
                elif countstat==1:
                    if oflag==0:
                        if value<high and value>low:
                            countstat=0
                        else:
                            pass
                    elif oflag==1:
                        countflag=countflag+1
                        print("count : ",countflag)
                        oflag=0
                        
        except ValueError:
            pass

    GPIO.cleanup()

#------------------------------------------------------------------------------
#Code Start

if __name__=="__main__":
    main()
    makegraph()