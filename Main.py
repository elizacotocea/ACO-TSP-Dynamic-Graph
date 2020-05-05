from AntColony import AntColony
from FileReader import readNetwork, readNetwork2


def main():
    dynamic = True
    while True:
        print("1. Run")
        print("0. Exit")
        cmd = input()
        if cmd == "1":
            #fileName="50p_easy_01_tsp.txt"
            #fileName="50p_medium_01_tsp.txt"
            #fileName="50p_hard_01_tsp.txt"
            fileName = "100p_fricker26.txt"
            #fileName = "150p_eil51.txt"
            network=readNetwork(fileName)
            print("Insert the number of ants in a colony:")
            ants = int(input())
            print("Insert the number of gens: ")
            gens = int(input())
            antColony = AntColony(network,ants, gens, dynamic)
            sol=antColony.run()
            path = sol[0]
            cost = sol[1]
            print("Result for "+str(ants)+" and "+str(gens)+" generations:")
            print("Number of cities: "+str(network['noNodes']))
            print("Best path found: "+str(path))
            print("Best cost found: "+str(cost))
        else:
            break
main()