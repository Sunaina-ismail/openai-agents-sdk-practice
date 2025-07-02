import copy

#! Shallow Copy
original = [[1, 2], [3, 4]]
shallow = copy.copy(original)

shallow[0][0] = 100

print(original)  #? [[100, 2], [3, 4]] → original is affected!


original = [[1, 2], [3, 4]]
deep = copy.deepcopy(original)

deep[0][0] = 100

print(original)  # [[1, 2], [3, 4]] → original is NOT affected