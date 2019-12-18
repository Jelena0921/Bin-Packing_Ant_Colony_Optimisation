from random import random
from time import time
from itertools import repeat
from matplotlib import pyplot as plt

from classes import Graph
from classes import Ant

class ACO(object):
    def __init__(self, bins, items, population, evaporation, limit=10000):
        self.bins = bins
        self.items = items

        self.ants = []
        for i in range(population):
            self.ants.append(Ant());

        self.graph = Graph(len(bins), len(items))

        self.evaporation = evaporation
        self.limit = limit

        self.numOfEvaluations = 0
        self.ran = False
        self.runtime = 0
        self.bestRun = None
        self.avgFitness = []

    def run(self):
        """Runs a full ACO run."""
        self.ran = False
        self.bestFits = []
        self.avgFitness = []
        startTime = time()

        while self.numOfEvaluations < self.limit:
            self.explore()

        for ant in self.ants:
            if self.bestRun and ant.fitness < self.bestRun.fitness:
                    self.bestRun = ant.copy()
            elif not self.bestRun:
                self.bestRun = ant.copy()

        self.ran = True
        self.runtime = time() - startTime

    def explore(self):
        """Create a route for all ants and evaporate the graph."""
        self.ants = [*map(self.createPath, self.ants)]
        best = None
        for ant in self.ants:
            ant.distributePheromones(self.graph)
        fitnesses = [ant.fitness for ant in self.ants]
        self.bestFits.append(min(fitnesses) / sum(self.items))
        self.avgFitness.append(sum(fitnesses) / len(fitnesses))
        self.graph.evaporate(self.evaporation)

    def createPath(self, ant):
        """Reset the bins and create a route for the given ant.
        
        :param ant: ant object
        :returns: ant with new path
        """
        for b in self.bins:
            b.empty()

        currentBin = 0
        ant.route = []
        for item in enumerate(self.items):
            currentBin, item = self.nextBin(currentBin, item)
            ant.route.append((currentBin, item))

        ant.fitness = self.getCurrentFitness()
        ant.bins = self.bins.copy()

        self.numOfEvaluations += 1
        
        return ant

    def nextBin(self, currentBin, item):
        """Get the index of the next bin to place the item in.
        
        :param currentBin: index of the current bin
        :param item: item weight
        :returns: next bin index 
        """
        column = self.graph.graph[currentBin][item[0]].tolist()
        total = sum(column)
        threshold = total * random()

        current = 0.0
        for index, weight in enumerate(column):
            if current + weight >= threshold:
                self.bins[index].addItem(item[1])
                return index, item[0]
            current += weight

    def getCurrentFitness(self):
        """Calculate the fitness of the current bin configuration.
        
        :returns: current fitness
        """
        maxWeight = self.bins[0].totalWeight
        minWeight = self.bins[0].totalWeight

        for b in self.bins:
            if b.totalWeight > maxWeight:
                maxWeight = b.totalWeight
            if b.totalWeight < minWeight:
                minWeight = b.totalWeight

        return maxWeight - minWeight


if __name__ == '__main__':
    from classes import createBinObjects
    from classes import generateBinItems

    val = input("Please select BPP problem. Write 1 to run BPP1, 2 to run BPP2. ")
    
    if val == "1":
        bins = createBinObjects(10)
        items = generateBinItems(quantity=500)
    elif val == "2":
        bins = createBinObjects(50)
        items = generateBinItems(quantity=500, bpp1=False)

    print("Running single ACO trial with %d bins and %d items." 
        % (len(bins), len(items)))

    population = int(input("Spesify population size: "))
    evaporation = float(input("Spesify evaporation rate: "))

    trial = ACO(bins, items, population, evaporation)
    trial.run()

    print("Run took %d seconds." % int(trial.runtime))
    print("Best fitness: %d" % trial.bestRun.fitness)

    plt.plot(trial.avgFitness)
    plt.xlabel('Generation of the Average Fitness calculation')
    plt.ylabel('Average Fitness Value')
    plt.show()
