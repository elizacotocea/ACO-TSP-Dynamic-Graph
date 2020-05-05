import operator
import random

class Ant:
    def __init__(self,start,network):
        self.__network= network
        self.__memory=[] #memoria furnicii (lista cu orasele vizitate)
        self.__delta=[] #(matricea de feromon a furnicii)
        self.__listNodesAvailable=[node for node in range(0,self.__network['noNodes'])]  # oraşele pe care le mai poate vizita a k-a furnică la momentul t
        self.__currentNode= start #nodul de pornire
        self.__listNodesAvailable.remove(start)
        self.__memory.append(self.__currentNode)
        self.__Q=1 #cantitatea de feromon lasata de o furnica
        self.__alpha=1 # controlează importanţa urmei (câte furnici au mai trecut pe muchia respectivă)
        self.__beta=2 # controlează importanţa vizibilităţii (cât de aproape se află următorul oraş)
        self.__cost=0 #costul total al drumului parcurs
        self.__eta=[] #1/d, pt a gasi cel mai scurt drum cu cel mai mult feromon
        self.__calculateEta() #vizibilitatea din oraşul i spre oraşul j (atractivitatea alegerii muchiei (i,j))

    #calculam atractivitatea fiecarei muchii, pentru fiecare nod din retea
    def __calculateEta(self):
        for i in range(0,self.__network['noNodes']):
            attractivity=[]
            for j in range(0, self.__network['noNodes']):
                if i != j:
                    attractivity.append(1/self.__network['mat'][i][j])
                else:
                    attractivity.append(0)
            self.__eta.append(attractivity)

    #calculam probabilitatea de tranziţie a furnicii curente situată în oraşul currentNode spre oraşul i
    #returneaza o lista de tupluri (nod, probabilitate)
    def getProbabilitiesOfSelection(self):
        prob={}
        for i in range(0, self.__network['noNodes']):
            prob[i] = 0
        sum=0
        for i in self.__listNodesAvailable:
            #tau^alpha*eta^beta
            sum +=pow(self.__network['pheromone'][self.__currentNode][i],self.__alpha)* pow(self.__eta[self.__currentNode][i],self.__beta)
        for i in self.__listNodesAvailable:
            # tau^alpha*eta^beta/sum(tau^alpha*eta^beta)
            prob[i]=(pow(self.__network['pheromone'][self.__currentNode][i],self.__alpha) * pow(self.__eta[self.__currentNode][i],self.__beta))/sum
        return sorted(prob.items(),key=operator.itemgetter(1))

    #folosit pt selectie
    #crearea unui interval de probabilitati (0,1)
    def getInterval(self,probabilities):
        probSum=0
        rez=[]
        for i in range(0,len(probabilities)):
            probSum= probSum+probabilities[i][1]
            rez.append(probSum)
        return rez

    #alegerea urmatorului oras pe baza unei selectii de tipul roulette selection
    def chooseNextDestination(self):
        probabilities=self.getProbabilitiesOfSelection()
        q0=self.getInterval(probabilities)
        q=random.random()
        next=None
        for i in range(0,len(q0)):
            if (q- q0[i]) <=0:
                next=probabilities[i][0]
                break
        self.__listNodesAvailable.remove(next)
        self.__memory.append(next)
        self.__cost+= self.__network['mat'][self.__currentNode][next]
        self.__currentNode= next
        return next

    #initializare matrice delta, matricea unitara de feromon
    def __initDelta(self):
        for i in range(self.__network['noNodes']):
            list = []
            for j in range(self.__network['noNodes']):
                list.append(0)
            self.__delta.append(list)

    #cream matricea ce contine  cantitatea unitară de feromoni lăsată de furnică pe muchiile parcurse
    #Q – cantitatea de feromon lăsată de furnică=1 (in cazul nostru)
    #supra lungimea (costul) turului efectuat de a furnică
    def updateDelta(self):
        self.__initDelta()
        for node in range(0,len(self.__memory)-1):
            node1=self.__memory[node]
            node2=self.__memory[node+1]
            self.__delta[node1][node2]=self.__Q/self.__cost

    def finishCycle(self):
        self.__cost=self.__cost + self.__network['mat'][self.__memory[len(self.__memory)-1]][self.__memory[0]]
        self.__memory.append(self.__memory[0])

    def getDelta(self,i,j):
        return self.__delta[i][j]

    def getCost(self):
        return self.__cost

    def getRoad(self):
        return self.__memory

    def getListNodesAvailable(self):
        return self.__listNodesAvailable