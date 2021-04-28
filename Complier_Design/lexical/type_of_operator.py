"""CODE BY MAYANK GUBBA
this lexical analyser uses regular expression to find out
the type of operator of data that is given as input"""
import re
t=int(input('enter the number of test cases: '))
for i in range(t):
    s=input("enter operator/data: ")
    if (re.match('^\*$',s)):
        print('multiplication operator')
    elif (re.match('^\+$',s)):
        print('addition operator')
    elif (re.match('^-$',s)):
        print('subtraction operator')
    elif (re.match('^/$',s)):
        print('division operator')
    elif (re.match('^>*$',s)):
        print('greater than operator')
    elif (re.match('^<*$',s)):
        print('less than operator')
    elif (re.match('^[0-9]+$',s)):
        print('integer data')
    elif (re.match('^[a-zA-z]+$',s)):
        print('alphabetical data')
    else:
        print('alphanumeric data')
