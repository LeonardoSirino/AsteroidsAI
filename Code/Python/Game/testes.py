a = [[1,2], [2,3], [4,5]]
a.insert(1, [])
a.__delitem__(0)

print(a)