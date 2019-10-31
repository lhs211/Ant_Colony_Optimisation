# -*- coding: utf-8 -*-
"""
Created on Thu Oct 17 20:43:06 2019

@author: Luke
"""
import random as rand
from sys import maxsize

class Ant:
    def __init__(self, num_bins, items):
        # Create empty bins
        self.bins = [0 for i in range(num_bins)]
        # Each Ant has its own items to give out
        self.items = items
        self.fitness = maxsize
        self.path = []
        
    def generate_path(self, P):
        for i in range(len(self.items)):
            bin_choice = choose_bin(P[i])
            self.path.append(*bin_choice)
            self.bins[self.path[-1]] += self.items[i]
    
    def find_path_fitness(self):
        """
        lowest_difference = maxsize
        for i in range(len(self.bins)):
            for j in range(i+1, len(self.bins)):
                if abs(self.bins[i] - self.bins[j]) < lowest_difference:
                    lowest_difference = abs(self.bins[i] - self.bins[j])
        self.fitness = lowest_difference
        """
        self.fitness = max(self.bins) - min(self.bins)
    
    def update_pheromone(self, P):
        """
        """
        for i in range(len(P)): # items
            if self.fitness == 0:
                P[i][self.path[i]] = maxsize
            else:
                P[i][self.path[i]] = 100/self.fitness
    

# could be a method in bin class
def best_fitness(ants):
    """
    """
    best_fitness = maxsize
    for i, ant in enumerate(ants):
        if ant.fitness < best_fitness:
            best_fitness = ant.fitness
    return best_fitness
    
def choose_bin(bin_choices):
    """
    """
    return rand.choices([i for i in range(len(bin_choices))], weights=bin_choices, k=1)
    
def evaporate_pheromone(P, e):
    """
    """
    P = [[e*num_bins for num_bins in num_items] for num_items in P]

def ACO(num_bins = 10,
        num_items = 500,
        max_num_fitness_evals = 10000,
        p = 10,
        evaporation_rate = 0.6):
    
    curr_evals = 0
    items1 = [i for i in range(1, num_items+1)]
    items2 = [(i*i)/2 for i in range(1, num_items+1)]
    # random pheromone over graph
    P = [[1 for j in range(num_bins)] for i in range(num_items)]
    
    while curr_evals <= max_num_fitness_evals:
        ants = []
        for i in range(p):
            curr_ant = Ant(num_bins, items1)
            curr_ant.generate_path(P)
            curr_ant.find_path_fitness()
            ants.append(curr_ant)
            curr_evals += 1
            
        for ant in ants:
            ant.update_pheromone(P)
            
        evaporate_pheromone(P, evaporation_rate)
    
    print(best_fitness(ants), 100*best_fitness(ants)/sum(items1))
    
            
if __name__ == "__main__":
    ACO()
    
    """
    solution to 3 bins 5 items with items1
    bin1:2,3
    bin2:5
    bin3:1,4
    """