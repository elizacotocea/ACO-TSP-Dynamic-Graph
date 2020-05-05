from random import randint

import numpy as np

def distFct(x1,x2,y1,y2):
    return float(np.sqrt(pow(abs(x1-y1),2) + pow(abs(x2-y2),2)))


def readNetwork(fileName):
    f = open(fileName, "r")
    graph={}
    graph['mat']=[]
    graph['noNodes'] = int(f.readline())
    for i in range(graph['noNodes']):
        line = f.readline()
        atr = line.split(",")
        l = []
        for i in range(0, len(atr)):
            l.append(int(atr[i]))
        graph['mat'].append(l)
    n = graph['noNodes']
    graph['pheromone'] = [[1 / n for j in range(n)] for i in range(n)]
    return graph


def readNetwork2(fileName):
    f = open(fileName, "r")
    graph={}
    f.readline()
    f.readline()
    f.readline()
    line = f.readline()
    atr = line.split(" ")
    graph['noNodes'] = int(atr[2])
    f.readline()
    f.readline()
    ct = 0
    l = []
    graph['mat']=[]
    while ct < graph['noNodes']:
        line = f.readline()
        atr = line.split(" ")
        l.append(atr)
        ct = ct + 1
    for i in range(0, len(l)):
        ll = []
        for j in range(0, len(l)):
            distance = distFct(float(l[i][1]), float(l[i][2]), float(l[j][1]), float(l[j][2]))
            ll.append(distance)
        graph['mat'].append(ll)
    f.readline()
    f.close()
    n = graph['noNodes']
    graph['pheromone'] = [[1 / n for j in range(n)] for i in range(n)]
    return graph

