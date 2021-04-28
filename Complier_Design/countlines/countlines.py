f=open('countlines.txt','rt')
n=0
for i in f:
    n+=1
print(n)
f.close()
