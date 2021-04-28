"""CODE BY MAYANK GUBBA
to find the firsts of any grammar"""
print('For A->Aa|b give input as\nA Aa b\nNOTE: instead of epsilon use $')
n=int(input('Enter the number of production rules: '))
d=dict()
#for loop to take grammar input
for i in range(n):
    l=list(map(str,input().split()))
    d[l[0]]=list(l[1:])
f=dict()
#finding all the firsts for each production rule
for p,r in d.items():
    temp=[]
    for j in r:
        if j[0].islower() or j[0]=='$':
            temp.append(j[0])
        elif j[0].isupper():
            for k in j:
                if k.isupper():
                    temp.append(k)
    f[p]=temp
#removing the first which contain other production rules
for p,r in f.items():
    for j in r:
        if j[0].isupper():
            for i in f[j[0]]:
                f[p].append(i)
                if '$' in f[j[0]]:
                    if len(j)>1:
                        f[p].append(j[1])
for i in f:
    f[i]=[k for k in f[i] if not k.isupper()]
    f[i]=set(f[i])

for i,j in f.items():
    print(i,'=',j)
