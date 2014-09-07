import pdb

cost_deletion = 2
cost_insertion = 2
cost_substitution = 1

def OptimalMatching(s1, s2):
    d = {}
    lenstr1 = len(s1)
    lenstr2 = len(s2)
    
    for i in range(-1, lenstr1+1):
        d[(i,-1)] = i+1
    for j in range(-1, lenstr2+1):
        d[(-1,j)] = j+1
 
    for i in range(lenstr1):
        for j in range(lenstr2):
            if s1[i] == s2[j]:
                d[(i,j)] = d[(i-1,j-1)] # always substitution : cost = 0 because they are the same
            else:
                d[(i,j)] = min(
                           d[(i-1,j)] + cost_deletion, # deletion
                           d[(i,j-1)] + cost_insertion, # insertion
                           d[(i-1,j-1)] + cost_substitution # substitution
                          )
    return d[lenstr1-1,lenstr2-1]

seq1 = [5, 2, 3, 2, 5, 1, 3, 3, 3, 1, 3, 3]
seq2 = [2, 5, 4, 2, 4, 5, 1, 5, 1, 3, 4, 2]

print OptimalMatching(seq1, seq2)
