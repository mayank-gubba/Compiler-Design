"""CODE BY MAYANK GUBBA
this lexical analyzers finds out all the keywords, special symbols,
operators, constants, variables and comments completely using the technique of
regular expression"""
import re
#list of keywords
keywords=["boolean","class","double", "else", "endif","float", "for","if","int", "long","null","then","while" ]
#regular ex[ression for symbols
symbol = re.compile('[@_!#$&()?}{~:,;]')
#regular exression for operators
operator = re.compile('[%^*+\-/\|<>=]')
file=open('lexical.txt','r')
# defining all the sets
key,sym,op,const,comm,var=set(),set(),set(),set(),set(),set()
a = file.read().split('\n')
for line in a:# iterating through each line
    k=re.findall(r"(?=("+'|'.join(keywords)+r"))",line) #finding the keywords
    key.update(k)
    s=symbol.findall(line) #finding the symbols
    sym.update(s)
    o=operator.findall(line) #finding the operators
    op.update(o)
    c=re.findall(r"\=(.*?);",line) #finding all the constants 
    const.update(c)
    co=re.findall(r"\/\*(.*?)\*\/",line) #finding the comments
    comm.update(co)
    v=[]
    v=re.findall(r'(\bint\b|boolean|float|double|long)',line) #finding the variables
    if len(v)>0:
        v=v[0]
        v1=re.findall(r"(?<="+v+")[^.]*",line)
        var.update(v1)

#printing all the values
print("keywords: ",*list(key),sep=" ")
print("special symbols: ",*list(sym),sep=" ")
print("operators: ",*list(op),sep=" ")
const1=[]
for i in const:
    if i.lstrip("-").isdigit():
        const1.append(i)
print("constants: ",*const1,sep=" ")
print("comments: ",*list(comm),sep=" ")
varf=set()
for i in var:
    i=i.replace(";","")
    for j in i.split(","):
        varf.add(j)
print("variables: ",*list(varf),sep=" ")

file.close()
