"""CODE BY MAYANK GUBBA
to find the operator precendence table
the code uses the associativity and precedence rules to find the
operator relation table"""

import pandas
file=open('operator_precedence_grammar.txt','r')
varl=set()
tl=set()
opl={}
lineno=0

#reading the file and seperating the variables,terminal and operators
#adding the lineno to operators of precedence and priority
for line in file:
    lineno+=1
    line=line.rstrip('\n')
    line=line.split(' ')
    l=list(line)
    for i in line:
        i = i.replace('\n', '')
        if i.isupper():
            varl.add(i)
        else:
            if i.isalpha():
                tl.add(i)
            elif i==('->'):
                pass
            else:
                opl[i]=[lineno]
                n=l.index(i)
                if i=='+' or i=='*' or i=='^' or i=='**' or l[n-1]==l[0]:
                    opl[i].append('r')
                else:
                    opl[i].append('l')

#adding terminals,operators and $ to single list
lt=[]
lt.extend(tl)
lt.extend(opl)
lt.append('$')
matrix=[]

#using the rules of operator precedence creating a 2x2 matrix for table
for i in range(0,len(lt)):
    matrix.append([])
    for j in range(0,len(lt)):
        if i==j:
            if lt[i]=='$' or lt[i] in tl:
                matrix[i].append('-')
            else:
                if opl[lt[i]][1]=='l':
                    matrix[i].append('<.')
                else:
                    matrix[i].append('.>')
        else:
            if lt[i] in tl or lt[j]=='$':
                matrix[i].append('.>')
            elif lt[i]=='$' or lt[j] in tl:
                matrix[i].append('<.')
            else:
                if opl[lt[i]][0] >= opl[lt[j]][0]:
                    matrix[i].append('.>')
                else:
                    matrix[i].append('<.')
    
#printing the matrix using pandas library for making a table
table = pandas.DataFrame(matrix, lt, lt)
print('Operator Precedence Table')
print(table)

file.close()
