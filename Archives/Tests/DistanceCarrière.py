import pdb
import numpy as np


cost_deletion = 3
cost_insertion = 2
cost_substitution = 1

def OptimalMatching_dict(s1, s2):
    calulated = {}
    lenstr1 = len(s1)
    lenstr2 = len(s2)
    min_cost = min(cost_deletion, cost_insertion)
     
    for i in range(-1, lenstr1+1):
        calulated[(i,-1)] = (i + 1)*min_cost
    for j in range(-1, lenstr2+1):
        calulated[(-1, j)] = (j + 1)*min_cost
  
    for i in range(lenstr1):
        for j in range(lenstr2):
            if s1[i] == s2[j]:
                calulated[(i,j)] = calulated[(i-1,j-1)] # always substitution : cost = 0 because they are the same
            else:
                calulated[(i,j)] = min(
                           calulated[(i-1,j)] + cost_deletion, # deletion
                           calulated[(i,j-1)] + cost_insertion, # insertion
                           calulated[(i-1,j-1)] + cost_insertion # substitution
                          )
#    pdb.set_trace()
    cost = np.zeros((lenstr1 + 1, lenstr2 + 1), dtype=int)
    for indices, value in calulated.iteritems():
      cost[indices[0], indices[1]] = value
        
    return calulated[lenstr1-1,lenstr2-1]


def OptimalMatching(s1, s2):
    assert isinstance(cost_deletion, int)
    assert isinstance(cost_insertion, int)
    assert isinstance(cost_substitution, int)
    lenstr1 = len(s1)
    lenstr2 = len(s2)
    cost = np.zeros((lenstr1 + 1, lenstr2 + 1), dtype=int)
    
    # initialization : comparaison with a null sequence
    min_cost = min(cost_deletion, cost_insertion)
    for i in range(lenstr1 + 1):
        cost[i, 0] = i*min_cost
    for j in range(lenstr2 + 1):
        cost[0, j] = j*min_cost

    for el1 in range(lenstr1):
        for el2 in range(lenstr2):
            if s1[el1] == s2[el2]:
                cost[el1 + 1, el2 + 1] = cost[el1, el2] # cost = 0 because they are the same
            else:
                cost[el1 + 1, el2 + 1] = min(
                                           cost[el1, el2 + 1] + cost_deletion, # deletion
                                           cost[el1 + 1, el2] + cost_insertion, # insertion
                                           cost[el1, el2] + cost_substitution # substitution
                                          )
    return cost[lenstr1, lenstr2]

def levenshtein2(source, target):
    if len(source) < len(target):
        return levenshtein(target, source)
 
    # So now we have len(source) >= len(target).
    if len(target) == 0:
        return len(source)
 
    # We call tuple() to force strings to be used as sequences
    # ('c', 'a', 't', 's') - numpy uses them as values by default.
    source = np.array(tuple(source))
    target = np.array(tuple(target))
 
    # We use a dynamic programming algorithm, but with the
    # added optimization that we only need the last two rows
    # of the matrix.
    previous_row = np.arange(target.size + 1)
    for s in source:
        # Insertion (target grows longer than source):
        current_row = previous_row + cost_insertion
 
        # Substitution or matching:
        # Target and source items are aligned, and either
        # are different (cost of 1), or are the same (cost of 0).
        current_row[1:] = np.minimum(
                current_row[1:],
                np.add(previous_row[:-1], target != s) + cost_substitution
                )
 
        # Deletion (target grows shorter than source):
        current_row[1:] = np.minimum(
                current_row[1:],
                current_row[0:-1] + cost_deletion)
 
        previous_row = current_row
 
    return previous_row[-1]


def levenshtein(a,b):
    "Calculates the Levenshtein distance between a and b."
    n, m = len(a), len(b)
    if n > m:
        # Make sure n <= m, to use O(min(n,m)) space
        a, b = b, a
        n, m = m, n
        
    current = range(n + 1)
    for i in range(1, m + 1):
        previous = current
        current = [i] + [0]*n
        for j in range(1, n + 1):
            add = previous[j] + cost_insertion
            delete = current[j - 1] + cost_deletion
            change = previous[j - 1]
            if a[j - 1] != b[i - 1]:
                change = change + cost_substitution
            current[j] = min(add, delete, change)
            
    return current[n]
    

if __name__ == '__main__':
    from GenerateCareersTests import RandomCareers
    test = RandomCareers(2, 10, 5)
    seq1 = test[0]
    seq2 = test[1]
    OptimalMatching(seq1, seq2)
    OptimalMatching_dict(seq1, seq2)
    
# TEST: 
n = 10000
seq1 = [x for x in range(n)]
seq2 = [3] + seq1
set = (OptimalMatching(seq1, seq2))

n = 36
seq1 = [x for x in range(n)]
seq2 = seq1.copy()
seq3 = seq1.copy()
seq2[25] = 0
seq3[12] = 1
tt1 = OptimalMatching(seq1, seq2)
tt2 = OptimalMatching(seq1, seq3)

pdb.set_trace()
assert OptimalMatching(seq1, seq2) == OptimalMatching(seq1, seq3)

seq1 = [5, 2, 3, 2, 5, 1, 3, 3, 3, 1, 3, 3]
seq2 = [2, 5, 4, 2, 4, 5, 1, 5, 1, 3, 4, 2]

print (OptimalMatching(seq1, seq2))


# TEST: 
n = 36
seq1 = [x for x in range(n)]
seq2 = [3] + seq1
print (OptimalMatching(seq1, seq2))




