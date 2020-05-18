#!/usr/bin/python3.6

import sys
import re
import matplotlib.pyplot as plt
from scipy.stats.stats import pearsonr

####parse shadow log#####
def is_initialization(line):
    if(re.search("(Created)|(Setup)", line) == None):
        return False
    return True

def is_correct_node(line, name):
    if(re.search("\[" + name + "[^0-9]", line) == None):
        return False
    return True

def is_node(line):
    if(re.search("\[node", line) == None):
        return False
    return True

def parse_line(line):
    a = re.search("\[node.*", line)
    if(a != None):
        aux = line[a.start():-1]
        #print(aux[aux.index(" ")+1:])
        return re.split(",|;", aux[aux.index(" ")+1:])
    return []


####parse server log#####
def split_line_client(line,dic,size):
    return get_client(line.split(" ")[10],dic,size)

def get_client(info,dic,size):
    if info.split(",")[5] not in dic:
        dic[info.split(",")[5]]=[float(0)]*size
    return info.split(",")[5];

def get_write_bytes(line): 
    return line.split(" ")[12].split("=")[1]

def is_transfer(line):
    a = re.search("\[tgen-transfer*", line)
    if(a != None):
        return True
    else:
        return False

if len(sys.argv) != 3:
    print("./parse.py <logfile> <logserver>")
else:

    dic={}
    dic2={}
    f = open(sys.argv[2], "r")
    l = f.readlines()
    ultimaLinha=l[-1]
    aux=ultimaLinha.split(" ")[1].split(":")
    size=(int(aux[0])*60*60+int(aux[1])*60+int(aux[2]))
    f.close()            


    f = open(sys.argv[2], "r")
    for i in f.readlines():
        #adicionar os clientes ao dicionario
        if(is_transfer(i)):
            split_line_client(i,dic,size)
    f.close()
          
    
    f = open(sys.argv[2], "r")
    for i in f.readlines():
        #adicionar transferencias ao dicionario
        if(not is_initialization(i)):
            if(is_transfer(i)):
                for x in dic:
                    if(x==split_line_client(i,dic,size)):
                        aux=i.split(" ")[1].split(":")
                        time=(int(aux[0])*60*60+int(aux[1])*60+int(aux[2]))
                        dic[x][time]=float(get_write_bytes(i))
    f.close()
    
    for cli in dic:
        f = open(sys.argv[1], "r")
        l = []
        for i in f.readlines():
            if(not is_initialization(i)):
                if(is_correct_node(i, cli)):
                    l.append(parse_line(i))
        l = l[:-1]
        #plt.ylabel(l[0][1])
        data = [float(x[1]) for x in l[1:] if x != []]
        dic2[cli]=data
        f.close()

    #must create the images directory    
    for x in dic: 
        plt.plot(dic[x])
        plt.savefig("images/sent_to_"+x)
        plt.close()

    for x in dic2: 
        plt.plot(dic2[x])
        plt.savefig("images/"+x+"_received.png")
        plt.close()


    dic3={} 
    for x in dic:
        dic3[x]=[]


    # will group the information. Example: [1][2][3][4]=[10] with fator = 4    
    fator=5
    for x in dic:
        i=0
        while i<len(dic[x]):
            addded_bytes=0
            j=0
            while j+i<len(dic[x]) and j<fator:
                addded_bytes=addded_bytes+dic[x][i+j]
                j=j+1
                i=i+1
            dic3[x].append(addded_bytes)
    dic4={} 
    for x in dic:
        dic4[x]=[]   

    for x in dic2:
        i=0
        while i<len(dic2[x]):
            addded_bytes=0
            j=0
            while j+i<len(dic2[x]) and j<fator:
                addded_bytes=addded_bytes+dic2[x][i+j]
                j=j+1
                i=i+1
            dic4[x].append(addded_bytes)

    print("victim name (the one where the flow was injected):")
    victim_name = input("> ")
    for x in dic3:
        if x==victim_name:
            for y in dic4:
                if(len(dic3[x])>len(dic4[y])):
                    for i in range(len(dic3[x])-len(dic4[y])):
                        dic4[y].append(float(0))
                if(len(dic2[y])>len(dic[x])):
                    for i in range(len(dic4[y])-len(dic3[x])):
                        dic3[x].append(float(0))
                print(x+"(serverside)"+" - "+"(clientside) "+y)
                print(pearsonr(dic3[x],dic4[y])[0])
    '''
    for i in range(len(dic["victim"])):
        print(dic["victim"][i] ,end='')
        print( " - " ,end='')
        print(dic2["victim"][i])

    '''







