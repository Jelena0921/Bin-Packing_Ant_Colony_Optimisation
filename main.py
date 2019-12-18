from operator import itemgetter
from time import time

from aco import ACO
from classes import createBinObjects
from classes import generateBinItems


def bpp(bins=10, bpp1=True, items=500):
    """Runs a full bin packing problem trial and prints the results.
    
    :param bins: number of bins
    :param bpp1: boolean spesifying which item weight generation to use
    :param items: number of items
    """
    rules = [
        {'population': 100, 'evaporation': 0.9},
        {'population': 100, 'evaporation': 0.6},
        {'population': 10,  'evaporation': 0.9},
        {'population': 10,  'evaporation': 0.6},
    ]

    for rule in rules:
        print("Current trial Parameters: Population=%d, Evaporation Rate=%.1f" % (
            rule['population'], 
            rule['evaporation']
        ))

        result = runACO(bins, items, rule['population'], rule['evaporation'], bpp1)
        
        print("Fitness AVG: %.1f, MAX: %s, MIN: %s" % (
            result['avgFitness'],
            result['maxFitness'],
            result['minFitness'],
        ))
        print("Time AVG: %.2f, MAX: %.2f, MIN: %.2f\n" % (
            result['avgTime'],
            result['maxTime'],
            result['minTime']
        ))


def runACO(numOfBins, numOfItems, population, evaporation, bpp1=True, numOfTrials=5):
    """Run ACO trial and return an object of the calculated results.
    
    :param numOfBins: number of bins
    :param numOfItems: number of items
    :param population: population size
    :param evaporation: evaporation rate
    :param bpp1: boolean indicating which problem to run
    :param numOfTrials: number of wanted trials for each rule

    :returns: dictionary with results
    """
    results = []
    avgFitness = 0
    avgTime = 0

    # Run 5 trials of the ACO algorithm
    for i in range(numOfTrials):
        bins = createBinObjects(numOfBins)
        items = generateBinItems(quantity=numOfItems, bpp1=bpp1)

        trial = ACO(bins, items, population, evaporation)
        trial.run()

        fitness = trial.bestRun.fitness
        time = trial.runtime

        results.append((fitness, time))
        avgFitness += fitness * 0.2
        avgTime += time * 0.2

    return {
        'avgFitness': avgFitness,
        'maxFitness': max(results, key=itemgetter(0))[0],
        'minFitness': min(results, key=itemgetter(0))[0],
        'avgTime': avgTime,
        'maxTime': max(results, key=itemgetter(1))[1],
        'minTime': min(results, key=itemgetter(1))[1],
    }


if __name__ == "__main__":
    start_time = time()
    
    print("Running Bin-Packing Problem 1\nBPP1 Parameters: 10 Bins and 500 Items\n")
    bpp()
    print("************************************\n")

    print("Running Bin-Packing Problem 2\nBPP2 Parameters: 50 Bins and 500 Items\n")
    bpp(50, False)
    print("************************************\n")

    print("Full program executed in %.2f seconds." % float(time() - start_time))