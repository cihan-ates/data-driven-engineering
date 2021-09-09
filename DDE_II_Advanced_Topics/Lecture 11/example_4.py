# -*- coding: utf-8 -*-
"""
Created on Thu Jul  8 15:28:46 2021
@author: cihan

"""
import datetime
import random
import genetic

'''
Problem Definition:
    
    operate on numbers to reach a lucky number; say 35.
    
    allowed operations:
        
        * basics: +, -, *
        * others: ^
'''   

# Measure of fitness:    
def get_fitness(genes, expectedTotal, fnEvaluate):
    result = fnEvaluate(genes)
    if result != expectedTotal:
        fitness = expectedTotal - abs(result - expectedTotal)
    else:
        fitness = 1000 - len(genes)
    return fitness


##############################################################################
##############################################################################

def create(numbers, operations, minNumber, maxNumber):
    genes = [random.choice(numbers)]
    count = random.randint(minNumber, maxNumber+1)
    while count > 1:
        count -=1
        genes.append(random.choice(operations))
        genes.append(random.choice(numbers))
    return genes
    
##############################################################################
##############################################################################
    
def mutate(genes, numbers, operations, minNumbers, maxNumbers, fnGetFitness):
    count = random.randint(1, 10)
    initialFitness = fnGetFitness(genes)
    while count > 0:
        count -= 1
        if fnGetFitness(genes) > initialFitness:
            return
        numberCount = (1 + len(genes)) / 2
        
        appending = numberCount < maxNumbers and \
            random.randint(0, 100) == 0
        if appending:
            genes.append(random.choice(operations))
            genes.append(random.choice(numbers))
            continue
        removing = numberCount > minNumbers and \
            random.randint(0, 20) == 0
        if removing:
            index = random.randrange(0, len(genes) - 1)
            del genes[index]
            del genes[index]
            continue
        index = random.randrange(0, len(genes))
        genes[index] = random.choice(operations) \
            if (index & 1) == 1 else random.choice(numbers)

##############################################################################
##############################################################################


# Evaluating the equation:
def evaluate(genes, prioritizedOperations):
    equation = genes[:]
    for operationSet in prioritizedOperations:
        iOffset = 0
        for i in range(1, len(equation), 2):
            i += iOffset
            opToken = equation[i]
            if opToken in operationSet:
                leftOperand = equation[i - 1]
                rightOperand = equation[i + 1]
                equation[i - 1] = operationSet[opToken](leftOperand, rightOperand)
                del equation[i + 1]
                del equation[i]
                iOffset += -2
    return equation[0]


##############################################################################
##############################################################################

# Helpers:
def add(a, b):
    return a + b
def subtract(a, b):
    return a - b
def multiply(a, b):
    return a * b

def display(candidate, startTime):
    timeDiff = datetime.datetime.now() - startTime
    print("{0}\t{1}\t{2}".format(
        (' '.join(map(str, [i for i in candidate.Genes]))),
        candidate.Fitness,
        timeDiff))
        
##############################################################################
##############################################################################




          
# Equation generator class:

def EquationGenerator():
        operations = ['^', '+', '-', '*']
        prioritizedOperations = [{'^': lambda a, b: a ** b},
                                 {'*': multiply},
                                 {'+': add,
                                  '-': subtract}]
        optimalLengthSolution = [6, '^', 2, '-', 1]
        solve(operations, prioritizedOperations, optimalLengthSolution)
        
def solve(operations, prioritizedOperations, optimalLengthSolution):
    numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9]
    expectedTotal = evaluate(optimalLengthSolution, prioritizedOperations)
    
    minNumbers = (1 + len(optimalLengthSolution)) / 2
    maxNumbers = 6 * minNumbers
    startTime = datetime.datetime.now()
    
    def fnDisplay(candidate):
        display(candidate, startTime)
    def fnEvaluate(genes):
        return evaluate(genes, prioritizedOperations)
    def fnGetFitness(genes):
        return get_fitness(genes, expectedTotal, fnEvaluate)
    def fnCreate():
        return create(numbers, operations, minNumbers, maxNumbers)
    def fnMutate(child):
        mutate(child, numbers, operations, minNumbers, maxNumbers, fnGetFitness)

    optimalFitness = fnGetFitness(optimalLengthSolution)
    genetic.get_best(fnGetFitness, None, optimalFitness, None,
                        fnDisplay, fnMutate, fnCreate, maxAge=50)

Case = EquationGenerator()   
  
    