from random import randint, random

from Ant import Ant


class AntColony:

    def __init__(self, network, numberOfAnts, generations, dynamic=False):
        self.__network=network #matricea de intrare
        self.__numberOfAnts=numberOfAnts #numarul de furnici dintr-o colonie
        self.__generations=generations #numarul de generatii/epoci dorite
        self.__isMatDynamic=dynamic #se doreste sau nu ca matricea sa fie dinamica
        self.__p = 0.4  # coef de degradare a feromonului

    #initializare colonie
    def __generateAnts(self):
        ants = []
        for i in range(0, self.__numberOfAnts):
            ants.append(Ant(randint(0, self.__network['noNodes']-1) ,self.__network))
        return ants

    #actualizare matrice de feromon cu cantitatile lasate de fiecare furnica in parte
    def __updatePheromoneMatrix(self, colony):
        for i in range(0, len(self.__network['pheromone'])):
            for j in range(0, len(self.__network['pheromone'])):
                #(coeficient de degradare a feromonului)* urma de feromon existenta
                self.__network['pheromone'][i][j] = self.__p * self.__network['pheromone'][i][j]
                for ant in colony:
                    if i in ant.getRoad() and j in ant.getRoad():
                        self.__network['pheromone'][i][j] += ant.getDelta(i, j)*(1-self.__p) #(1-coeficient de degradare a feromonului)* urma de feromon lasata de furnica

    #dinamizare retea
    def __changeDynamicNetwork(self):
        k=randint(1,self.__network['noNodes']-1)
        while k>0:
            i=0
            j=0
            while i==j:
                i = randint(0, self.__network['noNodes']- 1)
                j = randint(0, self.__network['noNodes']- 1)
            rand=randint(0,1)
            if rand== 1:
                num = randint(5,10)
                self.__network['mat'][i][j] += self.__network['mat'][i][j] * num
                self.__network['mat'][j][i] += self.__network['mat'][j][i] * num
            else:
                num = randint(2,3)
                self.__network['mat'][i][j] -= self.__network['mat'][i][j] // num
                self.__network['mat'][j][i] -= self.__network['mat'][j][i] // num
            k -= 1


    def run(self):
        bestCost = float('inf')
        bestPass = []
        contor=0
        for i in range(0, self.__generations):
            ants = self.__generateAnts()
            
            for ant in ants:
                if self.__isMatDynamic and contor == 5:
                    self.__changeDynamicNetwork()
                    print("Network is modified")
                    contor=0

                for node in range(0, self.__network['noNodes'] - 1):
                    ant.chooseNextDestination()
                ant.finishCycle()
                ant.updateDelta()
                if ant.getCost() < bestCost:
                    bestCost = ant.getCost()
                    bestPass = ant.getRoad()

            contor += 1
            self.__updatePheromoneMatrix(ants)
            print("Generation " + str(i+1) + " with path: " +str(bestPass)+" with cost: "+ str(bestCost))

        return bestPass,bestCost