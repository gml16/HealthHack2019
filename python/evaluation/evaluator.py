import numpy as np
from matplotlib import pyplot as plt 
from LocalitySensitiveHashing import *

def csv_create_hashing(datafile):
    lsh = LocalitySensitiveHashing(
            datafile = datafile,
            dim = 10,
            r = 50,
            b = 100,
            expected_num_of_clusters = 10,
    )
    lsh.get_data_from_csv()
    lsh.initialize_hash_store()
    lsh.hash_all_data()
    similarity_groups = lsh.lsh_basic_for_neighborhood_clusters()
    coalesced_similarity_groups = lsh.merge_similarity_groups_with_coalescence( similarity_groups )
    merged_similarity_groups = lsh.merge_similarity_groups_with_l2norm_sample_based( coalesced_similarity_groups )
    lsh.write_clusters_to_file( merged_similarity_groups, "clusters.txt" )


def generate_data(filepath):
    # Generate random values.
    values = []
    for _ in range(10):
        values.append([np.random.uniform(10) for _ in range(5)])

    # Write data to selected file.
    with open(filepath, 'w') as file:
        for row in values:
            val = ((str(row))[1:-1]).replace(",", "") + "\n"
            file.write(val)

def main():

    # Load data from data. 
    # filepath = str(input("Input image path:\n> "))
    filepath = "datapoints.txt"
    generate_data(filepath)
    data = np.asarray(np.loadtxt(filepath))
    print(data)

    # Run LSH on the data.
    create_hashing(data)

if __name__ == '__main__':
 main()