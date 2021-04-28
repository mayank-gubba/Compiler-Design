"""CODE BY MAYANK GUBBA
to find the parsing table of a grammar using pandas library
to create a parsing table in form of table"""
import re
import string
import pandas as pd 

def ll1(follow, productions):
	
	print ("\nParsing Table\n")

	table = {}
	for key in productions:
		for value in productions[key]:
			if value!='@':
				for element in first(value, productions):
					table[key, element] = value
			else:
				for element in follow[key]:
					table[key, element] = value

	new_table = {}
	for pair in table:
		new_table[pair[1]] = {}

	for pair in table:
		new_table[pair[1]][pair[0]] = table[pair]

	print (pd.DataFrame(new_table).fillna('-'))
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
grammar = open("grammar1.txt", "r")
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

grammar.close()
