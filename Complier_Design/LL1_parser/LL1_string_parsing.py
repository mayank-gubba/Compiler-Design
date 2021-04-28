"""CODE BY MAYANK GUBBA
for parsing a string for a given grammar."""
import re
import string
def parse(user_input,start_symbol,parsingTable):
        flag = 0
        user_input = user_input + "$"
        stack = []
        stack.append("$")
        stack.append(start_symbol)
        input_len = len(user_input)
        index = 0
        while len(stack) > 0:
                top = stack[len(stack)-1]
                print ("Top =>",top)
                current_input = user_input[index]
                print ("Current_Input => ",current_input)

                if top == current_input:
                        stack.pop()
                        index = index + 1	
                else:	
                        key = top , current_input
                        print (key)
                        if key not in parsingTable:
                                flag = 1		
                                break

                        value = parsingTable[key]
                        if value !='@':
                                value = value[::-1]
                                value = list(value)
                                stack.pop()
                                for element in value:
                                        stack.append(element)
                        else:
                                stack.pop()		

        if flag == 0:
                print ("String accepted!")
        else:
                print ("String not accepted!")



def ll1(follow, productions):
	table = {}
	for key in productions:
		for value in productions[key]:
			if value!='@':
				for element in first(value, productions):
					table[key, element] = value
			else:
				for element in follow[key]:
					table[key, element] = value
	return table

def follow(s, productions, ans):
	if len(s)!=1 :
		return {}
	for key in productions:
		for value in productions[key]:
			f = value.find(s)
			if f!=-1:
				if f==(len(value)-1):
					if key!=s:
						if key in ans:
							temp = ans[key]
						else:
							ans = follow(key, productions, ans)
							temp = ans[key]
						ans[s] = ans[s].union(temp)
				else:
					first_of_next = first(value[f+1:], productions)
					if '@' in first_of_next:
						if key!=s:
							if key in ans:
								temp = ans[key]
							else:
								ans = follow(key, productions, ans)
								temp = ans[key]
							ans[s] = ans[s].union(temp)
							ans[s] = ans[s].union(first_of_next) - {'@'}
					else:
						ans[s] = ans[s].union(first_of_next)
	return ans

def first(s, productions):
        c = s[0]
        ans = set()
        if c.isupper():
                for st in productions[c]:
                        if st == '@' :			
                                if len(s)!=1 :
                                        ans = ans.union( first(s[1:], productions) )
                                else :
                                        ans = ans.union('@')
                        else :	
                                f = first(st, productions)
                                ans = ans.union(x for x in f)
        else:
                ans = ans.union(c)
        return ans


productions=dict()
#grammar = open("grammar1.txt", "r")
grammar = open("grammar2.txt", "r")
#string = open("string1.txt","r")
string = open("string2.txt","r")

first_dict = dict()
follow_dict = dict()
flag = 1
start = ""
for line in grammar:
        l = re.split('->|\||\n',line)
        lhs = l[0]
        rhs = set(l[1:-1])-{''}
        if flag :
                flag = 0
                start = lhs
        productions[lhs] = rhs

for lhs in productions:
        first_dict[lhs] = first(lhs, productions)
for lhs in productions:
        follow_dict[lhs] = set()

follow_dict[start] = follow_dict[start].union('$')

for lhs in productions:
        follow_dict = follow(lhs, productions, follow_dict)

for lhs in productions:
        follow_dict = follow(lhs, productions, follow_dict)

ll1Table = ll1(follow_dict, productions)

check_string = string.read()
parse(check_string,start,ll1Table)

grammar.close()
string.close()
