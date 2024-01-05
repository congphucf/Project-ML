import random
# f = open('myfile.txt',"r")
# for k in range(1,9):
#     for i in range(10):
#         tmp = f.readline().split()
#         print(tmp[0], tmp[1])
f = open('location.txt', "r")

a = []
for k in range(24):
    tmp=f.readline().split()
    print(tmp)
    a.append([tmp[0], tmp[1]])
print(a)
f.close()

with open('test.txt', 'w') as p:
    for k in range(80):
        tmp = random.choice(a)
        p.write(f"{tmp[0]} {tmp[1]}\n")