import random as rand
from operator import itemgetter
from statistics import mean, stdev
from sys import maxsize
import matplotlib.pyplot as plt

def generate_path(P, items):
    """
    Generates a path through the construction graph
    
    PARAMETERS:
        P ([[int]]): The Pheromone Matrix
        
        items ([int]): The items to be placed in bins
        
    RETURNS:
        path ([int]): The generated path through the construction graph
        
        bins (dict<int, int>): The bins and their respective weights at the end of a path
    """
    path = []
    bins = {} # give bins keys based on the order they are visited in
    
    for i in range(len(P)):
        chosen_bin = rand.choices([x for x in range(len(P[i]))], weights=P[i], k=1)[0]
        path.append(chosen_bin)
        bins.setdefault(chosen_bin, 0) # if bin is not yet visited, set its weight to 0
        bins[chosen_bin] += items[i]
    
    return path, bins

def find_fitness(bins):
    """
    Finds the fitness of a solution
    
    PARAMETERS:
        bins (dict<int, int>): The bins and their respective final weights
        
    RETURNS:
        (int): The difference between the largest and smallest value in the dictionary
    """
    return max(bins.items(), key=itemgetter(1))[1] - min(bins.items(), key=itemgetter(1))[1]

def update_pheromone(P, path, fitness):
    """
    Updates the Pheromone Matrix based on the path taken
    
    PARAMETERS:
        P ([[int]]): The Pheromone Matrix
        
        path ([int]): A generated path through the construction graph
        
        fitness (int): The corresponding fitness of the path
    """
    for i in range(len(path)):
        P[i][path[i]] += 100 / fitness

def evaporate_pheromone(P, e):
    """
    Evaporates Pheromone on the matrix to allow for exploration
    
    PARAMETERS:
        P ([[int]]): The Pheromone Matrix
        
        e (float): The evaporation rate
    """
    for i in range(len(P)):
        for j in range(len(P[0])):
            P[i][j] *= 1-e
            
def show_results(results, title, parameters):
    """
    Displays the results of an experiment on a bar chart
    
    PARAMETERS:
        results ([[int]], float): The minimum fitness values from an experiment
        
        title (Str): Filename to save graph as
        
        parameters ((Str)): The parameter combination of each bar
    """
    *fitness, lowest = zip(*results)
    y_pos = range(len(parameters))
    error = []
    means = []
    for experiment in fitness[0]:
        means.append(mean(experiment))
        error.append(stdev(experiment))
    
    # get the figure
    f = plt.figure()
    plt.rc('text', usetex=True)
    plt.rc('font', family='serif')
    plt.bar(y_pos, means, yerr=error, align='center', alpha=0.5)
    plt.ylim(bottom=min(means)-min(means)*0.5)
    plt.xticks(y_pos, parameters)
    plt.ylabel(r'Average Fitness of Best Solution', fontsize=11)
    plt.xlabel(r'Parameter Combination', fontsize=11)
    plt.show()
    
    # save as PDF
    f.savefig(title + ".pdf", bbox_inches='tight')

def run_experiment(num_bins, p, e, items):
    """
    Performs an experiment based on the parameters
    
    PARAMETERS:
        num_bins (int): The number of bins to place on the construction graph
        p (int): The number of ants in each population
        e (float): The evaporation rate of the Pheromone
        items ([int]): The items to be placed into the bins
        
    Returns:
        ([int], float): The minimum fitness values from an experiment
    """
    MAX_EVALS = 10000
    TRIALS = 5
    
    best_cheat_fitness = [maxsize for z in range(TRIALS)]
    best_trial_fitness = []
    for i in range(TRIALS):
        rand.seed()
        P = [[rand.random() for y in range(num_bins)] for x in range(len(items))]
        curr_evals = 0

        while curr_evals < MAX_EVALS:
            paths = []
            for j in range(p):
                curr_path, curr_bins = generate_path(P, items)
                curr_fitness = find_fitness(curr_bins)
                paths.append((curr_fitness, curr_path))
                
                if curr_fitness < best_cheat_fitness[i]:
                    best_cheat_fitness[i] = curr_fitness
            curr_evals += p
            
            for (fitness, path) in paths:
                update_pheromone(P, path, fitness)
                
            evaporate_pheromone(P, e)
        best_trial_fitness.append(min(paths, key = lambda t: t[0])[0])
            
    return best_trial_fitness, mean(best_cheat_fitness)

if __name__ == "__main__":
    NUM_ITEMS = 500
    items1 = [i for i in range(1, NUM_ITEMS+1)]
    items2 = [(i*i)/2 for i in range(1, NUM_ITEMS+1)]
    results = []
    PARAMETERS = ('p=100, e=0.9', 'p=100, e=0.6', 'p=10, e=0.9', 'p=10, e=0.6')
    title = r"BinPackingProblem1"
    
    # BPP1
    results.append(run_experiment(num_bins=10, p=100, e=0.9, items=items1))
    results.append(run_experiment(num_bins=10, p=100, e=0.6, items=items1))
    results.append(run_experiment(num_bins=10, p=10, e=0.9, items=items1))
    results.append(run_experiment(num_bins=10, p=10, e=0.6, items=items1))
    
    show_results(results, title, PARAMETERS)
    print(results)
    results = []
    title = r"BinPackingProblem2"
    
    # BPP2
    results.append(run_experiment(num_bins=50, p=100, e=0.9, items=items2))
    results.append(run_experiment(num_bins=50, p=100, e=0.6, items=items2))
    results.append(run_experiment(num_bins=50, p=10, e=0.9, items=items2))
    results.append(run_experiment(num_bins=50, p=10, e=0.6, items=items2))
    
    show_results(results, title, PARAMETERS)
    print(results)