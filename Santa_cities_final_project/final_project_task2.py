import pandas as pd
import math
import random
import time
import numpy as np

ps=100
nog=30

#benchmark= pd.read_csv('output_task1.csv')
benchmark= pd.read_csv('output_test.csv')

def check_dup(benchmark,child):
    size=len(benchmark)
    while True:
        if size%2!=0:
            for i in range(size,2):
                for j in range(size):
                    if i!=size-1:
                        if benchmark[i+1]==child[j+1] or benchmark[i-1]==child[j-1] or \
                            benchmark[i-1]==child[j+1] or benchmark[i+1]==child[j-1]:
                            swap_num=random.choice(range(0,j)+range(j+1,end))
                            child[j], child[swap_num] = child[swap_num], child[j]
                    else:
                        if (benchmark[i-1]==child[j-1] or benchmark[i-1]==child[j+1]) and j!=size-1:
                            swap_num=random.choice(range(0,j)+range(j+1,end))
                            child[j], child[swap_num] = child[swap_num], child[j]
                        if benchmark[i-1]==child[j-1]  and j==size-1:
                            swap_num=random.choice(range(0,j)+range(j+1,end))
                            child[j], child[swap_num] = child[swap_num], child[j]
            
            return child
            break
        if size%2==0:
            for i in range(size,2):
                for j in range(size):
                    if benchmark[i+1]==child[j+1] or benchmark[i-1]==child[j-1] or \
                        benchmark[i-1]==child[j+1] or benchmark[i+1]==child[j-1]:
                        swap_num=random.choice(range(0,j)+range(j+1,end))
                        child[j], child[swap_num] = child[swap_num], child[j]

            return child 
            break

        


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
    pop_size=ps
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
        #math.sqrt((data.loc[i-1,'x']-data.loc[i,'x'])**2+(data.loc[i-1,'y']-data.loc[i,'y'])**2)
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
    #print(parent1)
    parent2=population[parent2_idx]
    return parent1, parent2, parent1_idx, parent2_idx


def crossover(parent1, parent2):
    """
    Partially Mapped Crossover(pmx)
    """
    size=len(parent1)
    child1=[]
    child2=[]
    x = random.randrange(size)
    y = random.randrange(size)
    if x > y:
        x,y = y,x
    p1Parts = parent1[x:y+1]
    #momCityIds = crossMom.getCityIds()
    p2Parts = parent2[x:y+1]
    p1Map = dict(zip(p1Parts, p2Parts))
    p2Map = dict(zip(p2Parts, p1Parts))
    for i in range(x):
        if parent1[i] in p2Parts:
            parent1[i]=p2Map[parent1[i]]
        child1.append(parent1[i])
    #extend to the part of parent 2 we want to copy
    child1.extend(p2Parts)
    for j in range(y+1, size):
        if parent1[j] in p2Parts:
            parent1[j]=p2Map[parent1[j]]
        child1.append(parent1[j])

    # create second child
    for i in range(x):
        if parent2[i] in p1Parts:
            parent2[i]=p1Map[parent2[i]]
        child2.append(parent2[i])
     #extend to the part of parent 1 we want to copy

    child2.extend(p1Parts)
    for j in range(y+1, size):
        if parent2[j] in p1Parts:
            parent2[j]=p1Map[parent2[j]]
        child2.append(parent2[j])

    #print('child1: ',child1)
    #print('child2: ',child2)
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
    population_size=len(population)
    #newChildren=[]
    parent1 , parent2, parent1_idx, parent2_idx = pick_parents(population,data)
    #print(parent1)
    if random.random() <= MUTATION_RATE:
        parent1 = mutation(parent1)
        parent2 = mutation(parent2)
    #if random.random() > CROSSOVER_RATE:
    child1, child2 = crossover(parent1, parent2)
    child1 = check_dup(benchmark,child1)
    child2 = check_dup(benchmark,child2)
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
    NUMBER_OF_GENERATIONS=nog
    ip=0
    totalTime=0
    inital_dis=distance(data['id'],data)
    #print(inital_dis)
    populations=population(data)
    #print(populations)
    for x in range(NUMBER_OF_GENERATIONS):
        #print('run time is: ', x)
        ip+=1
        starttime=time.time()
        evolve(populations,data)
        endtime=time.time()
        totalTime+=endtime - starttime
        print('Runtime: ', (x+1), '  Steptime:', round(endtime - starttime,2),'  Total Time: ', round(totalTime,2))
        if(ip%10==1 and ip!=1):
                scores=score(populations,data)
                index=scores.index(max(scores))
                final_dis=distance(populations[index],data)
                
                print('\n----- Interm Report -----')
                print('Total Time: ', round(totalTime/60,2),'mins')
                print("inital distance is: ",round(inital_dis,2))
                print("final distance is:",round(final_dis,2))
                print("Distance improved:",round((((inital_dis-final_dis)*100)/inital_dis),2), '%')
                print("Number of Cities:", ((data.size/3)-1), 'Population Size:',ps, ' Total Iteration:', x)
                print('\n') 
    #find min distance after evlove
    scores=score(populations,data)
    index=scores.index(max(scores))
    result=pd.DataFrame(populations[index])
    result.to_csv("output_task2.csv", index=False,header=False)
    final_dis=distance(populations[index],data)
    #print("inital distance is: ",inital_dis)
    #print("final distance is:",final_dis)
    print('\n----- Final Report Task 2 -----')
    print('Total Time: ', round(totalTime/60,2),'mins')
    print("inital distance is: ",round(inital_dis,2))
    print("final distance is:",round(final_dis,2))
    print("Distance improved:",round((((inital_dis-final_dis)*100)/inital_dis),2), '%')
    print("Number of Cities:", ((data.size/3)-1), 'Population Size:',ps, ' Total Iteration:', nog)

genetic()
