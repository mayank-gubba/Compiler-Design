"""CODE BY MAYANK GUBBA
this code detects the left recurssion of any grammar
the production rules are taken as input for this program"""
#A function to print the final production rules in A->bA' format
def print_prod(prod):
    for i in range(len(prod)):
        print(prod[i][0],end="->")
        for j in range(1,len(prod[i])-1):
            print(prod[i][j],end="/")
        print(prod[i][-1])

print('For A->Aa|b give input as\nA Aa b')
n=int(input('Enter number of production rules:'))
prod=[] #array for storing the production rules of a grammar
for i in range(n):#taking input for each grammar and storing it in an array
    b=list(map(str,input('enter production rules:').split()))
    prod.append(b)
prodf=[] #array to store final production rules
for i in range(len(prod)):
    lr=[j for j in prod[i] if j.startswith(prod[i][0])] 
    if len(lr)>1: #Searching for left recurssion 
        lr=lr[1:] #creating a array for all variables with left recurssion
        lr=[lr[j][1:]+prod[i][0]+"'" for j in range(len(lr))]
        nlr=[j for j in prod[i] if j.startswith(prod[i][0])==False] #An array for no left recurssion
        #modifying the production rule
        nlr=[j+prod[i][0]+"'" for j in nlr]
        lr.append('ε')
        lr.insert(0,prod[i][0]+"'")
        nlr.insert(0,prod[i][0])
        prodf.append(nlr)
        prodf.append(lr)
    else:
        prodf.append(prod[i])

print_prod(prodf)
