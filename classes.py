import numpy as np
import random

class Ant(object):
    """Ant class, stores its route and fitness information."""
    route = []
    bins = []
    fitness = -1

    def distributePheromones(self, graph):
        """Distributes pheromones on the graph."""
        pheromoneUpdate = 100.0 / self.fitness
        previousBin = 0
        for newBin, item in self.route:
            graph.graph[previousBin, item, newBin] += pheromoneUpdate
            previousBin = newBin

    def copy(self):
        """Creates a copy of an ant object."""
        ant = Ant()
        ant.bins = self.bins.copy()
        ant.route = [r for r in self.route]
        ant.fitness = self.fitness
        return ant


class Bin(object):
    """Bin class, holds items and current fitness."""
    totalWeight = 0
    items = []

    def addItem(self, item):
        """Add an item to the bin and increase its total weight."""
        self.items.append(item)
        self.totalWeight += item

    def copy(self):
        """Creates a copy of a bin object."""
        binCopy = Bin()
        binCopy.totalWeight = self.totalWeight
        binCopy.items = [item for item in self.items]
        return binCopy

    def empty(self):
        """Reset the contents of the bin."""
        self.items = []
        self.totalWeight = 0


class Graph(object):
    """Graph class, represents structure which contains the pheromone values for 
    every possible decision made by the ants."""  
    def __init__(self, bins, items):
        self.graph = np.random.rand(bins, items, bins)

    def evaporate(self, evaporation):
        """Reduce the pheromone weights across the graph."""
        self.graph *= evaporation


def generateBinItems(quantity=500, bpp1=True):
    """This function creates an array of bin weights."""
    if bpp1:
        return [i for i in range(1, quantity+1)]
    return [(i**2)/2 for i in range(1,quantity+1)]


def createBinObjects(n):
    """Creates and returns a list of Bin objects"""
    bins = []
    for i in range(n):
    	bins.append(Bin())
    return bins