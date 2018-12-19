import pandas as pd
import math
import random
import numpy as np
import copy
def read_data():
    """
    read data from csv file
    """
    #df=pd.read_csv('santa_cities.csv')
    df=pd.read_csv('test.csv')
    df.set_index('id')

    return df

def population(data):
    """
    randomly switch the id and append it to population
    and set up population size.
    """
    population=[]
    pop_size=100
    id=data['id']
    for i in range(pop_size):
        population.append(random.sample(list(id), len(id)))
    #population=random.sample(list(data['id']), pop_size)

    return population

def distance(path,data):
    """
    calculate euclidean distance in each close node and get final score
    """
    data=data.reindex(path)
    data=data.reset_index(drop=True)
    distance=0
    for i in range(1,len(data)):
        distance=distance+math.sqrt((data.loc[i-1,'x']-data.loc[i,'x'])**2+(data.loc[i-1,'y']-data.loc[i,'y'])**2)
        #np.linalg.norm(data.loc[i-1]-data.loc[i])
    distance=distance+math.sqrt((data.loc[0,'x']-data.loc[len(data)-1,'x'])**2+(data.loc[0,'y']-data.loc[len(data)-1,'y'])**2)
    return distance

def score(population,data):
    """
    return score list for all the population
    """
    scores=[]
    for i in range(len(population)):
        scores.append(1/distance(population[i],data))
    return scores

def pick_parents(population,data):
    scores=score(population,data)
    prob=[float(i)/sum(scores) for i in scores]
    parent1_idx,parent2_idx=np.random.choice(len(population),2, p=prob)
    parent1=population[parent1_idx]
    parent2=population[parent2_idx]
    return parent1, parent2, parent1_idx, parent2_idx



def crossover(parent1, parent2):
    """
    Partially Mapped Crossover(pmx)
    """
    size=len(parent1)
    #child1=[]
    #child2=[]
    child1 = []
    childP1 = []
    childP2 = []
    x = random.randrange(size)
    y = random.randrange(size)
    if x > y:
        x,y = y,x
    #p1Parts = parent1[x:y+1]
    #p2Parts = parent2[x:y+1]
    """
    p1Map = dict(zip(p1Parts, p2Parts))
    p2Map = dict(zip(p2Parts, p1Parts))
    for i in range(x):
        while parent1[i] in p2Parts:
            parent1[i]=p2Map[parent1[i]]
            #print('parent i :',parent1[i])
        child1.append(parent1[i])
    #extend to the part of parent 2 we want to copy
    child1.extend(p2Parts)
    for j in range(y+1, size):
        while parent1[j] in p2Parts:
            parent1[j]=p2Map[parent1[j]]
        child1.append(parent1[j])
        #print(child1)
    # create second child
    for i in range(x):
        while parent2[i] in p1Parts:
            parent2[i]=p1Map[parent2[i]]
        child2.append(parent2[i])
     #extend to the part of parent 1 we want to copy

    child2.extend(p1Parts)
    for j in range(y+1, size):
        while parent2[j] in p1Parts:
            parent2[j]=p1Map[parent2[j]]
        child2.append(parent2[j])
    """
    for i in range(x, y-1):
        childP1.append(parent1[i])
        
    childP2 = [item for item in parent2 if item not in childP1]

    child1 = childP1 + childP2

    child2 = []
    childP3 = []
    childP4 = []
    x = random.randrange(size)
    y = random.randrange(size)
    if x > y:
        x,y = y,x
    for i in range(x, y-1):
        childP3.append(parent2[i])
        
    childP4 = [item for item in parent1 if item not in childP3]

    child2 = childP3 + childP4

    return child1, child2

def mutation(parent):
    """
    randomly choose 1% of parent and mutate this part.
    """
    mut_percent=0.01
    size=len(parent)

    index = random.randint(0,int(size-(mut_percent*size+1)))
    mut_part=parent[index:index+int(size-(mut_percent*size+1))]
    mut_part=random.sample(mut_part,len(mut_part))
    for i in range(index,index+int(mut_percent*size+1)):
        parent[i]=mut_part[i-index]
    return parent

def evolve(population,data):
    MUTATION_RATE=0.4
    #CROSSOVER_RATE=0.5
    #population_size=len(population)
    #newChildren=[]
    parent1 , parent2, parent1_idx, parent2_idx = pick_parents(population,data)
    #print(parent1)
    if random.random() <= MUTATION_RATE:
        parent1 = mutation(parent1)
        parent2 = mutation(parent2)
    #if random.random() > CROSSOVER_RATE:
    child1, child2 = crossover(parent1, parent2)
    #else:
        #child1, child2 = parent1, parent2
    #if distance(child1, data)<distance(parent1,data): 
    population[parent1_idx]=child1
    #if distance(child2, data)<distance(parent2, data):   
    population[parent2_idx]=child2
    #print(child1)
    #print(child2)
    return None
    
def genetic():
    data=read_data()
    #print(data)
    NUMBER_OF_GENERATIONS=100
    inital_dis=distance(data['id'],data)
    #print(inital_dis)
    populations=population(data)
    #print(populations)
    for x in range(NUMBER_OF_GENERATIONS):
        print('run time is: ', x)
        evolve(populations,data)
    #find min distance after evlove
    scores=score(populations,data)
    index=scores.index(max(scores))
    result=pd.DataFrame(populations[index])
    result.to_csv("output_test.csv", index=False,header=False)
    final_dis=distance(populations[index],data)
    print("inital distance is: ",inital_dis)
    print("final distance is:",final_dis)

genetic()
