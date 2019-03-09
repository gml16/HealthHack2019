import numpy as np
from matplotlib import pyplot as plt 
from nearpy import Engine
from nearpy.hashes import RandomBinaryProjections

def categorize(engine, query):
    # Illnesses:
    ill = ['Herpes', 'Syphillis', 'HPV', 'HIV']

    # Get nearest points.
    nearest = engine.neighbours(query)

    # Return results.
    if len(nearest) == 0:
        print("Sample suggests host is healthy!")
        return
    for candidate in nearest:
        index = int(candidate[-2][-1])
        value = float(candidate[-1])
        print("Sample suggests presence of %s with distance %.2f" % (ill[index], value))

"""
Sets correspond to regions which represent diseases.
When testing for a given input, if it falls inside a region, flag as that illness.
-> otherwise flag as healthy / probably the closest..? 
"""
def create_hashing(sets):

    # Dimension of the vector space.
    dimension = len(sets[0][0]) 

    # Create a random binary hash with 10 bits
    rbp = RandomBinaryProjections('rbp', 10)

    # Create engine with pipeline configuration
    engine = Engine(dimension, lshashes=[rbp])

    # Index all our values (set their data to a unique string). 
    for index,s in enumerate(sets):
        for v in s:
            engine.store_vector(v, 'data_%d' % index)

    return engine

def main():
    # Each set represents data from a particular disease we are modelling.
    sets = 4
    # Number of dimension represents the amt of data used in evaluating disease.
    dimension = 10

    # Generate data. 
    data = [[np.random.randn(dimension) for _ in range(100)] for n in range(sets)]

    # Run LSH on the data.
    engine = create_hashing(data)
    categorize(engine, np.random.randn(dimension))



if __name__ == '__main__':
 main()