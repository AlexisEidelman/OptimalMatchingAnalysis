import numpy as np
import pandas as pd
import random 



def RandomCareers(nb_observations, career_length, nb_modalities):
    list2 = {}
    for i in range(nb_observations - 1) :
        list2[i] = [random.randint(1, nb_modalities) for k in range(career_length)]
    return list2

if __name__ == '__main__':
    print(RandomCareers(10, 12, 5))

    