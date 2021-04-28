import pandas as pd
from State import *

def Read_Input(grammar):
    file_name = "grammar3.txt"       #get file

    file = open(file_name,'r' )
    lines_list = file.readlines()

    for line in lines_list:
        line = line.strip('\n')
        line = line.replace(' ' , '')

        if line !='':
            line_list = line.split('->')   #parse the grammar

            if line_list[0].isupper():

                if '|' in line_list[1]:
                    production_list = line_list[1].split('|')

                    for prod in production_list:
                        grammar.append([line_list[0],prod])
                                              #each terminal has a list of RHS of productions
                else:
                    grammar.append(line_list)      #grammar has list of productions
            else:
                print("Error!")


def Term_Nonterm(grammar , term , non_term ):

    for production in grammar:
        if production[0] not in non_term:   #production[0]=LHS
            non_term.append( production[0] )


        for char in production[1 ]:
            if not char.isupper():

                if char not in term:
                    term.append( char )


def calculate_firstset(grammar , first , term , non_term):
                       #first=dict()
    for t in term:
        first[t] = t
    for nt in non_term:
        first[nt] = set({})  #initialize
    for nt in non_term:
        get_first(nt, grammar, first, term)



def get_first(nonterm , grammar ,first , term):  #nonterm=symbol

    for production in grammar:
        if nonterm in production[0]:
            rhs = production[1]
            first_char = rhs[0]

            #if starts with a term
            if first_char in term:
                first[nonterm].add(first[first_char])
            else:
                if not first[first_char] and   nonterm !=  first_char:  #if starts with nonterm
                    get_first(first_char,grammar,first,term)

                i = 0
                while i <len(rhs) and  'e' in first[rhs[i]]: #if it has a e derivation
                    for symbol in first[rhs[i]]:
                        if 'e' != symbol:
                            first[nonterm].add(symbol)
                    i += 1
                if i == len(rhs):
                    first[nonterm].add('e')     #they all have e derivation
                else:
                    for symbol in  first[rhs[i]]:
                        first[nonterm].add(symbol)


def Get_Augmented( grammar , augment_grammar):

    augment_grammar.append([grammar[0][0]  + "'" ,  grammar[0][0]])  #add augmented grammar
    augment_grammar.extend( grammar )  #add other rules fram original grammar

    return augment_grammar

def Closure(I , augment_grammar , first,non_term):

    while True:
        added = False

        for item in I:
            dot_pos = item[1].index('.')  #item[1]=right hand side #item[0]=left hand side
            if dot_pos == (len(item[1]) - 1):  #if dot is at the end (reduce)
                continue
            next_symbol = item[1][dot_pos + 1] #next symbol after dot
            if next_symbol in non_term:   #if next symbol is nonterm
                for production in augment_grammar:  #add its productions
                    if next_symbol == production[0]:
                        if production[1] == 'e':
                            rhs = 'e.'
                        else:
                            rhs = '.' + production[1]


                        lookahead = []  # calculate look ahead
                        if dot_pos < (len(item[1]) - 2):
                            remainder = item[1][dot_pos + 2]
                            for symbol in first[remainder]:
                                if 'e' == symbol: #e derivation
                                    for elem in item[2]:  #item[2]=lookahead
                                        if elem not in lookahead:
                                            lookahead.append(elem)
                                else:
                                    if symbol not in lookahead:
                                        lookahead.append(symbol)

                        else:
                            lookahead = deepcopy(item[2])

                        newitem = [next_symbol, rhs, lookahead]  # structure of each item

                        if newitem not in I:
                            same_core = False
                            for item_ in I:
                                if item_[0] == newitem[0] and item_[1] == newitem[1]:
                                    same_core = True
                                    for la in lookahead:
                                        if la not in item_[2]:
                                            item_[2].append(la)
                                            added = True

                            if not same_core:
                                I.append(newitem)
                                added = True

        if not added:
            break


def Goto(I,symbol , augment_grammar,first,non_term):

    J = []

    for item in I:
        dot_pos = item[1].index('.')

        if dot_pos < len(item[1]) - 1: #dot is somewhere in the middle
            next_char = item[1][dot_pos + 1]
            if next_char == symbol:  # if symbol is the symbol after dot

                new_rhs = item[1].replace('.' + symbol, symbol + '.')
                new_item = [item[0], new_rhs, item[2]]  #new item made by goto action
                J.append(new_item)

    Closure(J, augment_grammar, first, non_term)

    return J


def isSame(states,newstate,I,Symbol): #checks if new state was made before

    for J in states:
        if J.state == newstate:
            I.update_goto(  Symbol ,J )
            return True

    return False


def init_FirstState(augment_grammar,first,non_term):  #first state

    I0 = [[augment_grammar[0][0], '.' + augment_grammar[0][1], ['$']]]   #first state: startsymbol,.RHS
    Closure(I0, augment_grammar,first,non_term)

    return I0


def Add_States(states , augment_grammar , first , term , non_term):

    first_state = init_FirstState(augment_grammar, first, non_term)

    states.append( State(first_state))
    all_symb = non_term + term

    while True:

        added = False
        for I in states:
            for symbol in all_symb:
                new_state = Goto(I.state, symbol, augment_grammar, first, non_term)  # goto(I,symbol)
                if (new_state != []) and not isSame(states, new_state, I, symbol): #if new state is not empty and it is not repeated
                    s =State(new_state)
                    I.update_goto(symbol, s)
                    s.update_parentName(I, symbol)
                    states.append(s)
                    added = True

        if not added:
            break
        



def get_parse_table(parse_table , states , augmented_grammar):


    for index, I in enumerate(states):
        parse_table.append(I.actions)

        for item in I.state:
            rhs_list = item[1].split('.')
            if rhs_list[1] == '': #is reduce
                prod_no = augmented_grammar.index([item[0], rhs_list[0]])

                for la in item[2]:

                    parse_table[index][la] = -prod_no

    return parse_table

def Print_States(grammar, augment_grammar, term, non_term, first, states):
    state_list = []
    ctr = -1
    repeat = []
    not_print=[]
    to_combine=[]
    combined=[]
    to_print=[]
    for state in states:
        ctr += 1
        items_list = []
        for item in state.state:
            items = item[0] + '->' + item[1]
            items_list.append(items)
            

        if items_list not in repeat:
            repeat.append(items_list)
            count = 0
            for item in state.state:
                count += 1
            to_print.append(ctr)
        else:
            
            to_append=[]
            ctr_append=0
            for item in state.state:
                to_append.append(item[2])
            for item in states[state_list.index(items_list)].state:
                item[2].extend(to_append[ctr_append])
                ctr_append+=1
            not_print.append(ctr)
            to_combine.append(state_list.index(items_list))
            to_print[to_print.index(state_list.index(items_list))]=str(state_list.index(items_list))+str(ctr)
            combined.append(str(state_list.index(items_list))+str(ctr))
        state_list.append(items_list)
    count = 0
    for state in states:
        for i in state.actions:
            if state.actions[i] in to_combine:
                ind = to_combine.index(state.actions[i])
                state.actions[i] = int(combined[ind])
            elif state.actions[i] in not_print:
                ind = not_print.index(state.actions[i])
                state.actions[i] = int(combined[ind])
            elif state.actions[i] == 0:
                state.actions[i] = "accept"
                

    print('*******----DFA-----**********')
    print()
    ctr=-1
    state_ctr=-1
    for state in states:
        ctr+=1
        if ctr not in not_print:
            state_ctr+=1
            print("Item",to_print[state_ctr],":")
            for item in state.state:
                print (item[0] + '->' + item[1] + " " + str(item[2]))
            print()
            print("*---traversals--*")
            for act in state.actions:
                if isinstance(state.actions[act],str):
                    if state.actions[act] == "accept":
                        print("Item",to_print[state_ctr],"--",act,"->",state.actions[act])           
                    else:    
                        print("Item",to_print[state_ctr],"--",act,"->","Item",state.actions[act])
                elif state.actions[act] < 0:
                    print()
                    print("No Traversal!")
                    break
                else:
                    print("Item",to_print[state_ctr],"--",act,"->","Item",state.actions[act])
                    
            print()

    print('*******----PARSING TABLE-----**********')
    print()
    return repeat,not_print,to_combine,to_print,combined

g=[]
terms=[]
nonterms=[]
f=dict()
a=[]
s=[]

p_t=[]

Read_Input(g)

Term_Nonterm(g,terms,nonterms)  #print nonterms and terms
print('\nterms:',terms, '\nnon terms:',   nonterms)


calculate_firstset(g,f,terms,nonterms) #print firstset for nonterms

print('\nfirstsets:')
for nont in nonterms:
    print(nont, '->', f[nont])

augment=Get_Augmented(g,a) #print augmented grammar

print('\naugment grammar:')
for production in augment:
    print(production[0],'->',production[1])

Add_States(s,a,f,terms,nonterms)


Pa_t=get_parse_table(p_t,s,a)


sl,np,tc,tp,c = Print_States(g, a, terms, nonterms, f, s)

np.reverse()
tc.reverse()
c.reverse()
for i in range(len(np)):
    for j in Pa_t[np[i]].keys():
        if j not in Pa_t[tc[i]].keys():
            Pa_t[tc[i]][j] = Pa_t[np[i]][j]
    Pa_t.pop(np[i])

for i in range(len(Pa_t)):
    for j in Pa_t[i]:
        if Pa_t[i][j] == "accept":
            pass
        elif Pa_t[i][j] < 0:
            Pa_t[i][j] = "r" + str(abs(Pa_t[i][j]))
        elif j.isupper():
            pass
        else:
            Pa_t[i][j] = "s" + str(Pa_t[i][j])
            


dfa={}
for i in range(len(tp)):
    dfa[str(tp[i])]=Pa_t[i]

for i in dfa:
    for j in dfa[i]:
        if (isinstance(dfa[i][j],str)) and len(dfa[i][j]) == 2:
            if dfa[i][j][0] == "s":
                if int(dfa[i][j][1:]) in tc:
                        ex = tc.index(int(dfa[i][j][1:]))
                        dfa[i][j] = dfa[i][j][:1] + c[ex]
                elif int(dfa[i][j][1:]) in np:
                        ex = np.index(int(dfa[i][j][1:]))
                        dfa[i][j] = dfa[i][j][:1] + c[ex]
        if (isinstance(dfa[i][j],int)):
            if int(dfa[i][j]) in tc:
                    ex = tc.index(int(dfa[i][j]))
                    dfa[i][j] = str(c[ex])
            elif int(dfa[i][j]) in np:
                    ex = np.index(int(dfa[i][j]))
                    dfa[i][j] = str(c[ex])

df = pd.DataFrame(dfa.values(),index = tp).fillna('  ')
print(df)
print()
print("*******----STRING PARSING-----**********")
print()
string=input('Enter string to parse: ')
string+='$'
stack=['0']
pointer=0
try:
    while True:
        lookahead=string[pointer]
        if dfa[stack[-1]][lookahead][0] =='s':
            act = dfa[stack[-1]][lookahead][1:]
            stack.append(lookahead)
            stack.append(act)
            print(stack)
            pointer+=1
        elif dfa[stack[-1]][lookahead][0] =='r':
            r_no=int(dfa[stack[-1]][lookahead][1])
            to_pop=g[r_no-1][1]
            for i in range(2*len(to_pop)):
                 stack.pop()
            stack.append(g[r_no-1][0])
            stack.append(str(dfa[stack[-2]][g[r_no-1][0]]))
            print(stack)
            
        elif dfa[stack[-1]][lookahead] =='accept':
            print('Succesfull parsing')
            break
except:
    print('Unsuccesfull parsing')

        
    
    
