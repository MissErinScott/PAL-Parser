### PAL Grammar rules Parser

import ply.yacc as yacc

# Get the token map from the lexer.  This is required.
from PALLexer import tokens
from random import randint
#Global key value dictionaries
#key = Organism ID value = max value of organisms in the model
orgmax = {}
#key = Organism ID value = initial value of organisms in the model
orginitial = {}

#key = Organism ID value = list of dictionaries key = action name and value = population operator
orgpopactions = {}
#key = Organism ID value = list of dictionaries key = action name and value = list [action type,operator,different operator,otherorgid]
orgpopactionnames = {}

#key = Organism ID  value = list of internal species of that organism
orgspecies = {}

#key = internal species ID value = list of actions of that species
speciesactions = {}
#key = Organism ID value = list of species actions of that organism
orgactions = {}

#key = internal species ID value = list of parameters of that species
orgparameters = {}

#key = Organism ID value value key species id value parameter expression
orginitialresets = {}


###Starting rule which specifies the parts of a PAL model
##def p_palmodel_1(p):
##    'palmodel : maxpoplist modelcomponent biospeciesbehaviours parameters actionrates organisms populations'
##    p[0] = p[4] + '\n' + p[5] + '\n' + p[3] + '\n' + addonandoffspecies() + '\n' + p[6]

def p_palmodel_1(p):
    'palmodel : maxpoplist modelcomponent populations organisms initialresets biospeciesbehaviours parameters actionrates'
    p[0] = p[7] + '\n'+ addintialresetparasandactionrates() + '\n' + p[8] + '\n' + p[6] + '\n' + p[3] + '\n' + p[4]

#initial reset rules
def p_intialresets_1(p):
    'initialresets : initialresets initialreset'
    p[0] = p[1] + p[2]

def p_intialresets_2(p):
    'initialresets : initialreset'
    p[0] = p[1]

def p_initialreset(p):
    'initialreset : IDENTIFIER IDENTIFIER EQUALS expression SEMICOLON'
    createorginitialresetdictionary(p)
    p[0] = p[1] + ' ' + p[2] + ' ' + p[3] + ' ' + p[4] + ' ; ' + '\n'

#parameter rules
def p_parameters_1(p):
    'parameters : parameters parameter'
    p[0] = p[1] + p[2]

def p_parameters_2(p):
    'parameters : parameter'
    p[0] = p[1]

def p_parameter(p):
    'parameter : IDENTIFIER EQUALS expression SEMICOLON'
    p[0] = addorganismidtoparameters(p)

#action rate rules
def p_actionrates_1(p):
    'actionrates : actionrates actionrate'
    p[0] = p[1] + p[2]

def p_actionrates_2(p):
    'actionrates : actionrate'
    p[0] = p[1]

def p_actionrate(p):
    'actionrate : IDENTIFIER COLON expression SEMICOLON'
    p[0] = addorganismidtoactions(p)

#same expression rule used in parameters and actionrates
def p_expression_power(p):
    'expression : expression POWER term'
    p[0] = p[1] + p[2] + p[3]

def p_expression(p):
    '''expression : expression PLUS term
                  | expression MINUS term '''
    if p[2] == '+':
        p[0] = p[1] + ' + ' + p[3]
    elif p[2] == '-':
        p[0] = p[1] + ' - ' + p[3]

def p_expression_term(p):
    'expression : term'
    p[0] = p[1]

def p_term_times(p):
    'term : term TIMES factor'
    p[0] = p[1] + ' * ' + p[3]

def p_term_divides(p):
    'term : term DIVIDE factor'
    p[0] = p[1] + ' / ' + p[3]

def p_term_factor(p):
    'term : factor'
    p[0] = p[1]
    
def p_factor(p):
    '''factor : NUMBER
              | IDENTIFIER'''
    p[0] = ' ' + p[1] + ' '

def p_factor2(p):
    'factor : MINUS NUMBER'
    p[0] = ' ' + p[1] + p[2] + ' '
    

def p_factor_expr(p):
    'factor : LEFTBRACKET expression RIGHTBRACKET'
    p[0] = p[1] + ' ' + p[2] + ' ' + p[3]

#For Heaviside step function,fMA and exp
def p_factor_h(p):
    'factor : IDENTIFIER LEFTBRACKET expression RIGHTBRACKET'
    p[0] = p[1] + p[2] + p[3] + p[4]

##def p_expression_power1(p):
##    'expression : expression POWER term'
##    p[0] = p[1] + p[2] + p[3]

#biospecies behaviour rules
def p_biospeciesbehaviours_1(p):
    'biospeciesbehaviours : biospeciesbehaviours biospeciesbehaviour'
    p[0] = p[1] + p[2]

def p_biospeciesbehaviours_2(p):
    'biospeciesbehaviours : biospeciesbehaviour'
    p[0] = p[1]

def p_biospeciesbehaviour(p):
    'biospeciesbehaviour : IDENTIFIER EQUALS bioactions SEMICOLON'
    addtoactiondictionararies(p)
    p[0] = addorganismidtospecies(p)

def p_bioactions_1(p):
    'bioactions : bioactions PLUS bioaction'
    p[0] = p[1] + ' ' + p[2] + ' ' + p[3]

def p_bioactions_2(p):
    'bioactions : bioaction'
    p[0] = p[1]

def p_bioaction_1(p):
    'bioaction : IDENTIFIER baction'
    p[0] = p[1] + ' ' + p[2]

def p_bioaction_2(p):
    'bioaction : LEFTBRACKET IDENTIFIER COMMA NUMBER RIGHTBRACKET baction'
    p[0] = p[1] + ' ' + p[2] + ' ' + p[3] + ' ' + p[4] + p[5]+ ' ' + p[6]

def p_baction(p):
    '''baction : BIOPRODUCT
               | BIOREACTANT
               | BIOMODIFIER
               | BIOACTIVATOR
               | BIOINHIBITOR '''
    p[0] = p[1]

#organism
def p_organisms_1(p):
    'organisms : organisms organism'
    #Add sync between different species organisms
    p[0] = p[1] + '<*> ' + p[2]
    
    
def p_organisms_2(p):
    'organisms : organism'
    p[0] = p[1]

def p_organism(p):
    'organism : IDENTIFIER EQUALS biospeciesmodelcomponent'
    addtoorgspeciesdictionary(p)
    p[0] = makemodelcomponent(p)

def p_biospeciesmodelcomponent_1(p):
    'biospeciesmodelcomponent : biospeciesmodelcomponent biosync bioinitial'
    p[0] = p[1] + ' ' + p[2] + ' ' + p[3]    
def p_biospeciesmodelcomponent_2(p):
    'biospeciesmodelcomponent : bioinitial'
    p[0] = ' ' + p[1] + ' '

def p_bioinitial(p):
    'bioinitial : IDENTIFIER LEFTSQUAREBRACKET NUMBER RIGHTSQUAREBRACKET'
    p[0] = p[1] + ' ' + p[2] + p[3] + p[4]    

def p_biosync(p):
    '''biosync : LEFTANGLEBRACKET TIMES RIGHTANGLEBRACKET
               | LEFTANGLEBRACKET listofids RIGHTANGLEBRACKET '''
    p[0] = p[1] + p[2] + p[3]

#population
def p_populations_1(p):
    'populations : populations population'
#    p[0] = p[1] + p[2]
    createpopactionnamesdictionary()
    p[0] = addonandoffspecies()
    
def p_populations_2(p):
    'populations : population'
    p[0] = p[1]
    
def p_population(p):
    'population : populationid EQUALS popactions SEMICOLON'
    addtopopactiondictionary(p)
    p[0] = p[1] + ' ' + p[2] + ' ' + p[3] + ' ' + p[4] + '\n'

    
#Also used in modelcomponent rules
def p_populationid(p):
    'populationid : IDENTIFIER LEFTDOUBLECURLYBRACKET IDENTIFIER RIGHTDOUBLECURLYBRACKET'
    p[0] = p[1] + ' ' + p[2] + ' '+ p[3] + ' ' + p[4]

def p_popactions_1(p):
    'popactions : popactions PLUS popaction'
    p[0] = p[1] + ' ' + p[2] + ' ' + p[3]
    
def p_popactions_2(p):
    'popactions : popaction'
    p[0] = p[1]   

def p_popaction(p):
    'popaction : IDENTIFIER paction'
    p[0] = p[1] + ' ' + p[2]
    
def p_paction(p):
    ''' paction : PALADDITION
                | PALDELETION
                | PALACTIVATOR '''
    p[0] = p[1]


#population modelcomponent
def p_modelcomponent_1(p):
    ' modelcomponent : modelcomponent palsync popinitial'
    p[0] = p[1] + ' ' + p[2] + ' ' + p[3] + '\n'

def p_modelcomponent_2(p):
    ' modelcomponent : popinitial'
    p[0] = p[1]

def p_popinitial_1(p):
    'popinitial : populationid LEFTDOUBLESQUAREBRACKET NUMBER RIGHTDOUBLESQUAREBRACKET'
    p[0] = p[1] + p[2] + p[3] + p[4]
    global orginitial
    #get popid and split up string
    popid = p[1].split()
    i=1
    #Get the organism name
    for word in popid:
        if i==3 :
            #Add organism name key and initial value
            orginitial[word] = p[3]
        i = i +1
        
def p_palsync(p):
    'palsync : LEFTCURLYBRACKET listofids RIGHTCURLYBRACKET'
    p[0] = p[1] + p[2] + p[3]

def p_listofids_1(p):
    'listofids : listofids COMMA IDENTIFIER'
    p[0] = p[1] + p[2] + p[3]

def p_listofids_2(p):
    'listofids : IDENTIFIER'
    p[0] = p[1]

#Max population
def p_maxpoplist(p):
    'maxpoplist : IDENTIFIER COLON listofmaxpops SEMICOLON'
    p[0] = p[1] + p[2] + p[3] + p[4] + '\n'

def p_listofmaxpops_1(p):
    'listofmaxpops : listofmaxpops COMMA popmax'
    p[0] = p[1] + p[2] + p[3]

def p_listofmaxpops_2(p):
    'listofmaxpops : popmax'
    p[0] = p[1]

def p_popmax(p):
    'popmax : IDENTIFIER LEFTDOUBLECURLYBRACKET IDENTIFIER RIGHTDOUBLECURLYBRACKET NUMBER'
    p[0] = p[1] + p[2] + p[3] + p[4] + ' ' + p[5]
    global orgmax
    orgmax[p[3]] = p[5]
    
# Error rule for syntax errors
def p_error(p):
    if p:
         print("Syntax ERROR at token: ","Type: ", p.type,"Value:" , p.value ,"LineNo: ", p.lineno)
    else:
         print("Syntax error at End Of File")

#Functions used in parser rules

#Create initialresetdicitionary
def createorginitialresetdictionary(p):
    global orgspecies
    global orginitialresets

    internalspeciesname = p[2]
    species = []
    speciesreset = {}

    for orgid in orgspecies:
        species = orgspecies[orgid]
        if internalspeciesname in species:
            speciesreset[internalspeciesname] = p[4]
            if orgid in orginitialresets:
                orginitialresets[orgid].update(speciesreset)
            else:
                orginitialresets[orgid] = speciesreset
    

#Add on and off species
def addonandoffspecies():
    global orgpopactionnames
    global orgmax

    noworgid = ''
    popactions = {}
    result = ''
    actionbefore = False
    

    for nowid in orgmax:
        
        popactions = orgpopactionnames[nowid]

        i=1
        while i < int(orgmax[nowid]) +1:
            onactions,offactions = '',''
            actionbefore=False
            
            for action in popactions:
                infolist=popactions[action]
                if 'async' in infolist:
                    if infolist[1] == '<<<':
                        #Check if an action of this type has been parsed already
                        if onactions == '':
                            onactions,offactions = createdeleteactions(i,nowid,action,actionbefore)
                        else :
                            on,off = createdeleteactions(i,nowid,action,actionbefore)
                            onactions += on
                            offactions += off
                    if infolist[1] == '>>>':
                        #Check if an action of this type has been parsed already
                        if onactions == '':
                            onactions,offactions = createaddactions(i,nowid,action,actionbefore)
                        else :
                            on,off = createaddactions(i,nowid,action,actionbefore)
                            onactions += on
                            offactions += off
                    actionbefore=True
                if 'switch1' in infolist:
                    #Check if an action of this type has been parsed already
                    if onactions == '':
                        onactions,offactions = createsyncdeleteactions(i,nowid,action,infolist[3],actionbefore)
                    else :
                        on,off = createsyncdeleteactions(i,nowid,action,infolist[3],actionbefore)
                        onactions += on
                        offactions += off
                    actionbefore= True
                if 'switch2' in infolist:
                    #Check if an action of this type has been parsed already
                    if onactions == '':
                        onactions,offactions = createsyncaddactions(i,nowid,action,infolist[3],actionbefore)
                    else :
                        on,off = createsyncaddactions(i,nowid,action,infolist[3],actionbefore)
                        onactions += on
                        offactions += off
                    actionbefore= True
                if 'repro1' in infolist:
                    #Check if an action of this type has been parsed already
                    if onactions == '':
                         onactions,offactions = createsyncaddactions(i,nowid,action,infolist[3],actionbefore)
                    else :
                        on,off = createsyncaddactions(i,nowid,action,infolist[3],actionbefore)
                        onactions += on
                        offactions += off
                    actionbefore= True
                if 'repro2' in infolist:
                    #Deal with this type of popaction in internal species actions
                    pass
            
            result += 'On_' + nowid + str(i) + ' = ' + onactions+';' + '\n'
            result += 'Off_' + nowid + str(i) + ' = ' + offactions +';' + '\n'
            i = i+1

    result += '\n'
                       
    return result

#Create delete actions for organism that has a popaction which deletes it
def createdeleteactions(number,organismid,action,actionbefore):
    global orgmax
    
    result1 = ''
    result2 = ''
    
    if actionbefore == False:
        result1 = action + '_' + organismid + str(number) + ' <<'
        result2 = action + '_' + organismid + str(number) + ' >>'
    else:
        result1 = ' + ' + action + '_' + organismid + str(number) + ' <<'
        result2 = ' + ' + action + '_' + organismid + str(number) + ' >>'
            
    return result1,result2

#Create add actions for organism that has a popaction which adds it
def createaddactions(number,organismid,action,actionbefore):
    global orgmax
    
    result1 = ''
    result2 = ''
    
    if actionbefore == False:
        result1 = action + '_' + organismid + str(number) + ' >>'
        result2 = action + '_' + organismid + str(number) + ' <<'
    else:
        result1 = ' + ' + action + '_' + organismid + str(number) + ' >>'
        result2 = ' + ' + action + '_' + organismid + str(number) + ' <<'
            
    return result1,result2  

#Create sync delete actions for organism that has a popaction which deletes it
def createsyncdeleteactions(number,organismid,action,otherorgid,actionbefore):
    global orgmax
    
    result1 = ''
    result2 = ''

    #Find max value for other organism
    otherorgmax = orgmax[otherorgid]
    i = 1
    while i < int(otherorgmax) + 1:
        if actionbefore == False:
            result1 = action + '_' + organismid + str(number) + '_' + otherorgid + str(i) + ' <<'
            result2 = action + '_' + organismid + str(number) + '_' + otherorgid + str(i) + ' >>'
            actionbefore = True
        else :
            result1 += ' + ' + action + '_' + organismid + str(number) + '_' + otherorgid + str(i) + ' <<'
            result2 += ' + ' + action + '_' + organismid + str(number) + '_' + otherorgid + str(i) + ' >>'
        i = i + 1
            
    return result1,result2

#Create sync add actions for organism that has a popaction which adds a new organism
def createsyncaddactions(number,organismid,action,otherorgid,actionbefore):
    global orgmax
    
    result1 = ''
    result2 = ''

    #Find max value for other organism
    otherorgmax = orgmax[otherorgid]
    i = 1
    while i < int(otherorgmax) + 1:
        if actionbefore == False:
            result1 = action + '_' + otherorgid + str(i) + '_' + organismid + str(number) + ' >>'
            result2 = action + '_' + otherorgid + str(i) + '_' + organismid + str(number) + ' <<'
            actionbefore = True
        else :
            result1 += ' + ' + action + '_' + otherorgid + str(i) + '_' + organismid + str(number) + ' >>'
            result2 += ' + ' + action + '_' + otherorgid + str(i) + '_' + organismid + str(number) + ' <<'
        i = i + 1
            
    return result1,result2

#For internal species pop actions
#Create sync add actions for organism that has a popaction which adds a new organism
def createsyncadd2actions(number,organismid,action,otherorgid,actionbefore):
    global orgmax
    
    result1 = ''
    result2 = ''

    #Find max value for other organism
    otherorgmax = orgmax[otherorgid]
    i = 1
    while i < int(otherorgmax) + 1:
        if actionbefore == False:
            result1 = action + '_' + organismid + str(number) + '_' + otherorgid + str(i) + ' >>'
            result2 = action + '_' + organismid + str(number) + '_' + otherorgid + str(i) + ' <<'
            actionbefore = True
        else :
            result1 += ' + ' + action + '_' + organismid + str(number) + '_' + otherorgid + str(i) + ' >>'
            result2 += ' + ' + action + '_' + organismid + str(number) + '_' + otherorgid + str(i) + ' <<'
        i = i + 1
            
    return result1,result2

#Add entry to popactionsdictionary
def addtopopactiondictionary(p):
    #Variables
    global orgpopactions
        
    #Split Popid
    popid = p[1].split()
    #Get organism id from popid
    orgid = popid[2]

    #split the popactions into separate words
    popacts = p[3].split()

    #Add orgid and popactions to dictionary
    orgpopactions[orgid] = makeactionoperatordictionary(popacts)

#Create dictionary of actions and their associated operator
def makeactionoperatordictionary(popacts):
    popactions = {}
    actionname=''

    for word in popacts:
        if '+' == word:
            pass
        if '(' in word or ')' in word or '>' in word or '<' in word:
            popactions[actionname] = word
        else :
            actionname = word
            
    return popactions

#Create popactionnames dictionary
def createpopactionnamesdictionary():
    global orgpopactions
    global orgpopactionnames

    
    for nowid in orgmax:
        #Get organism id from popid
        noworgid = nowid
        popactions = orgpopactions[noworgid]
    
        #Make a dictionary of key actionid and values operators for now organism id
        #All the actions that are associated with the now organism population and all the operators associated with that action
        orgsameactions = {}
        for orgid in orgpopactions:
            acts = orgpopactions[orgid]
            for action in acts:
                if action in orgsameactions:
                    orgsameactions[action].append(acts[action])
                else:
                    orgsameactions[action] = [acts[action]]

        for act in popactions:
            if act in orgsameactions:
                #Find if the action is shared with other population
                if len(orgsameactions[act]) < 2:
                    #This is pop action that is not synchronised with other population
                    makeandaddactiontypedictionary(noworgid,act,'async',orgsameactions[act][0],'none')
                else :
                    i = 0
                    while i < len(orgsameactions[act]):
                        #Find the action and operator associated with now organism population
                        if orgsameactions[act][i] == popactions[act]:
                            sameaction = act
                            sameoperator = orgsameactions[act][i]
                        else:#Find the operator associated with other organism population
                            differentoperator = orgsameactions[act][i]
                        i = i+1
                        #Find out what kind of action is synchronised by what type of operators
                        #Switch action now organism population decrease other organism population increase
                    if sameoperator == '<<<' and differentoperator == '>>>':
                        makeandaddactiontypedictionary(noworgid,act,'switch1',sameoperator,differentoperator)
                        #Switch action now organism population increase other population decrease
                    if sameoperator == '>>>' and differentoperator == '<<<':
                        makeandaddactiontypedictionary(noworgid,act,'switch2',sameoperator,differentoperator)
                        #Reproduction action now organism population increase other population stays the same
                    if sameoperator == '>>>' and differentoperator == '((+))':
                        makeandaddactiontypedictionary(noworgid,act,'repro1',sameoperator,differentoperator)
                        #Reproduction action now organism population stays the same other population increases
                    if sameoperator == '((+))' and differentoperator == '>>>':
                        makeandaddactiontypedictionary(noworgid,act,'repro2',sameoperator,differentoperator)


#Create dictionary of action and their associated type and add to orgpopactionnames dictionary
def makeandaddactiontypedictionary(orgid,actionname,actiontype,sameoperator,differentoperator):
    global orgpopactionnames
    otherorgid=''

    #Find other organisms id
    for key in orgpopactions:
        if actionname in orgpopactions[key]:
            if key == orgid:
                pass
            else:
                otherorgid = key
                
    #If action is type async it will not have a different operator or another organism associated with it
    if actiontype == 'async':
        actioninfolist=[actiontype,sameoperator]
    else:
        actioninfolist=[actiontype,sameoperator,differentoperator,otherorgid]
    
    actiontype = {actionname:actioninfolist}
    if orgid in orgpopactionnames:
        orgpopactionnames[orgid].update(actiontype)
    else:
        orgpopactionnames[orgid] = actiontype


         
#Add and sometimes multiply parameters based on max value for organism.
#Add parameter to orgparameter dictionary only if they are associated to an organism.
#Multiply parameters based on if there are species ids in their expression. 
def addorganismidtoparameters(p):
    #Variables
    addorgid, orgid = isspeciesinparameter(p)
    global orgmax
    global orgparameters
    right = ''

    if addorgid == False:
        right = p[1] + ' ' + p[2] + p[3] + p[4] + '\n' + '\n'

    if addorgid == True:
        #Add parameter to  more than one orgid if needed
        ids = orgid.split()

        a = 0
        while a<len(ids) :
            value = orgmax[ids[a]]
            duplicatepar = False
            #Add parameter to dictonary of organism parameters
            if ids[a] in orgparameters:
                if p[1] in orgparameters[ids[a]]:
                    duplicatepar = True
                    pass
                else:
                    orgparameters[ids[a]].append(p[1])
               
            else:
                orgparameters[ids[a]] = [p[1]]

            
            if duplicatepar == True:
                pass
            else:        
                expression = p[3].split()
                expression2 =''
                i=1
                while i < int(value)+1:
                    expression2=''
                    expression2= addorganismidtospeciesinparameter(expression,i,ids[a])
                    right += p[1] + '_' + ids[a] + str(i) + ' ' + p[2] + expression2 + p[4] + '\n'
                    i = i + 1
            right += '\n'
            a = a + 1

    return right
    
    
#Check if there are species ids in the parameter's expression
# If true - Return true and the organism id the species is assosiated with.
# If false - Return false and the string none. 
def isspeciesinparameter(p):
    #Variables
    global orgspecies
    listofspecies = []
    #split the string of the expression
    expression = p[3].split();

    orgids = ''
    inparameter = False
    

    #Go through each key value pair in orgspecies
    for k, v in orgspecies.items() :
        listofspecies = v
        #Go through each word
        for word in expression:
                #If the word is a species return true and organism id
            if word in listofspecies:
                inparameter = True
                orgids+= k + ' '
                #return True, k
        listofspecies = []
    #No species were found in the parameter return false and string none          
    return inparameter, orgids
                               

#Add organism id to the species in parameter expression 
def addorganismidtospeciesinparameter(string,i,k):
    result = ''
    global orgspecies
    listofspecies = orgspecies[k]

    #Create expression
    for word in string:
        #If the word is an id add org id
        if word in listofspecies:
            word += '_' + k +str(i)
        #If the word is equal to random assign random int range 0 to 6
        if word == 'random':
            word = str(randint(0,10))
        result += ' ' + word   
        
    return result

#Add initial reset parameters and action rates
def addintialresetparasandactionrates():
    result = ''
    result += addinitialresetparameters() + '\n'
    result += addinitialresetactionrates() + '\n'
    return result

#Add initial reset parameters
def addinitialresetparameters():
    global orginitialresets
    global orgmax

    noworgid = ''
    orgspecies = {}
    result = ''
    
    for nowid in orgmax:
        
        orgspecies = orginitialresets[nowid]

        for species in orgspecies:

            i=1
            while i < int(orgmax[nowid]) +1:
                expression = orgspecies[species]
                expression2 = expression.split()
                expression3 = addorganismidtospeciesinparameter(expression2,i,nowid)
                result += 'In'+ species + '_' + nowid + str(i) + ' = ' + expression3 + ';' + '\n'
                i = i + 1
 
    return result


#Add initial reset action rates
def addinitialresetactionrates():
    global orginitialresets
    global orgmax

    noworgid = ''
    orgspecies = {}
    result = ''
    
    for nowid in orgmax:
        
        orgspecies = orginitialresets[nowid]

        for species in orgspecies:

            i=1
            while i < int(orgmax[nowid]) +1:
                result += 'kineticLawOf Initial' + species + '_' + nowid + str(i) + ' : ( fMA(10 * In'+ species + '_' + nowid + str(i) + ')) * Off_' + nowid + str(i) + ';' + '\n'
                i = i + 1
 
    return result

#Add organism ids to action rate id and parts of the expression
def addorganismidtoactions(p):
    #Variables
    global orgmax
    global orgactions
    global orgpopactionnames
    actionslist = []
    actionid = p[1]
    right = ''
    #split the expression into separate words
    expression = p[3].split()
    expression2 = ''
    internalaction = False
  
    
    for orgid, actions in orgactions.items() :               
        actionlist = actions
        if actionid in actionlist:
            internalaction = True
            #Dont' want to print out pop action like internal action
            #This checks for mirrored pop actions
            if checkifpopaction(actionid,orgid) == True:
                #Write sync pop action rates
                popactions = orgpopactionnames[orgid]
                infolist=popactions[actionid]
                j = 1
                while j < (int(orgmax[orgid])+1):
                    expression2 = ''
                    expression2 = addorganismidtoactionexpression(expression,j,orgid)
                    actionRates = createsyncpopactionrates(orgid,actionid,infolist,j,expression2)
                    right += actionRates
                    j = j + 1
            else :#The action is an internal action that is hidden from populations
                j=1
                while j < (int(orgmax[orgid])+1):
                    expression2 = ''
                    #Special case when action contains the word empty do not add * on agent to rate
                    if 'empty' in actionid.lower():
                        expression2 = addorganismidtoactionexpression(expression,j,orgid)
                        right += 'kineticLawOf ' + p[1] + '_' + orgid + str(j) + ' ' + p[2]  + expression2  + p[4] + '\n'
                    else :
                        expression2 = addorganismidtoactionexpression(expression,j,orgid)
                        right += 'kineticLawOf ' + p[1] + '_' + orgid + str(j) + ' ' + p[2] + '(' + expression2 + ' ) * On_' + orgid + str(j) + p[4] + '\n'
                    j = j + 1
    #This checks for hidden popactions
    if internalaction == False:
        for orgid,i in orgmax.items():
            popactions = orgpopactionnames[orgid]
            if actionid in popactions:
                j=1
                while j < (int(i)+1):
                    expression2 = ''
                    expression2 = addorganismidtoactionexpression(expression,j,orgid)
                    right += 'kineticLawOf ' + p[1] + '_' + orgid + str(j) + ' ' + p[2] + '(' + expression2 + ' ) * On_' + orgid + str(j) + p[4] + '\n'
                    j = j + 1
        
    
    right+= '\n'
    return right

#Write actionrates for sync pop actions
def createsyncpopactionrates(orgid,actionid,infolist,number,expression):

    global orgmax
    result = ''

    #Find max value for other organism
    otherorgmax = orgmax[infolist[3]]
    i = 1 
    while i < int(otherorgmax) + 1:
        result += 'kineticLawOf ' + actionid + '_' + orgid + str(number) + '_' + infolist[3] + str(i) +' : ' + '(' + expression + ' ) * On_' + orgid + str(number) + ';' + '\n'
        i = i + 1
    
    return result

#Create actionrate expression and add organism id to speciesids or parameterids specific to the organism
def addorganismidtoactionexpression(string,i,org):
    result = ''
    global orgparameters
    global orgspecies
    listofids = orgspecies[org] + orgparameters[org]

    #Create expression
    for word in string:
        #If the word is an id add org id
        if word in listofids:
            word += '_' + org +str(i)
        result += ' ' + word           
        
    return result

#Add key value pairs to both orgactions and speciesactions  
def addtoactiondictionararies(p):
    #Variables
    global orgspecies
    global speciesactions
    global orgactions
    listofspecies = []
    listofactions = []
    speciesid = p[1]
    # split the actions into separate words
    acts = p[3].split()
    acts2 = ''
    
    #Go through each key value pair in orgspecies
    for k, v in orgspecies.items() :
        listofspecies = v
        #Check if speciesid is same as speciesid in list
        if speciesid in listofspecies:
            listofactions = []
            for word in acts:
                #Add actions to list of actions only if word refers to an action
                if '(' in word or ',' in word or ')' in word or '>' in word or '<' in word or '+' in word or '-' in word or '.' in word:
                    pass
                else :
                    #Add to listofactions
                    listofactions.append(word)
                        
                    #Add org id and action list to orgactions dictionary
                    if k in orgactions:
                        orgactions[k].append(word)
                        #Remove any duplicate actions
                        orgactions[k] = list(set(orgactions[k]))
                    else:
                        orgactions[k] = [word]
                               
            #Add organism id key and species list value pair dictionary                 
            speciesactions[speciesid] = listofactions
                
        listofspecies = []
    

#Add multiple species behaviour based on max value for organism
def addorganismidtospecies(p):
    #Variables
    global orgmax
    global orgspecies
    listofspecies = []
    speciesid = p[1]
    right = ''
    #split the string of bioactions when + occurs
    acts = p[3].split(' + ')
    acts2 = ''
    
    #Go through each key value pair in orgspecies
    for k, v in orgspecies.items() :
        listofspecies = v
        #Check if speciesid is same as speciesid in list
        if speciesid in listofspecies:
            #Go through each key value pair in orgmax
            for key, value in orgmax.items():
                #Check both keys match
                if key == k:
                    j = 1
                    #Print out action rate + _i * max value
                    while j < int(value)+1:
                        acts2 = ''
                        acts2 = addorganismidtospeciesactions(acts,j,key)
                        initialact = addinitialaction(p[1],key,j)
                        #build right hand side
                        right += p[1] + '_' + key + str(j) + ' ' + p[2] + ' '+ acts2 + initialact + p[4] + '\n'
                        j=j+1
        listofspecies = []
        right += '\n'
    return right

#Add initial reset action to reset the species to initial value when it is off
def addinitialaction(speciesname,orgid,orgnumber):
    global orginitialresets
    result = ''
    orgresets = orginitialresets[orgid]
    if speciesname in orgresets:
        expression = orgresets[speciesname].split()
        if str(expression[1]) == speciesname:
            result = ' + Initial' + speciesname + '_' + orgid + str(orgnumber) + ' <<'
        if str(expression[3]) == speciesname:
            result = ' + Initial' + speciesname + '_' + orgid + str(orgnumber) + ' >>'
        
    return result
    

#Add organism id to actions and check for popactions
def addorganismidtospeciesactions(string,i,k):
    #Reset result string variable
    result = ''
    actionbefore = False
    pop = False
    act = ''
    #Look through bioactions and add _i * max value
    for word in string:
        #split action by spaces
        string2 = word.split()
        #Reset if pop action boolean
        pop = False
        for word2 in string2:
            if '(' in word2 or ',' in word2 or ')' in word2 or '>' in word2 or '<' in word2 or '+' in word2:
                pass
            if checkifpopaction(word2,k) == True:
                pop = True
                #Create popactions
                act = writepopaction(word2,k,i,actionbefore,string2)

        if pop == True:
            #Add pop actions to result
            result += ' ' + act
            actionbefore = True
        else:
            #Check if another action was already parsed before this action
            if actionbefore == True:
                #Add choice operator
                result += ' + '
            for word2 in string2:
                if '(' in word2 or ',' in word2 or ')' in word2 or '>' in word2 or '<' in word2 or '+' in word2:
                    pass
                else :
                    word2 += '_' + k +str(i)
                #Add all words of action to result
                result += ' ' + word2
            actionbefore = True
            
    return result

#Check if an internal species action is a pop action
def checkifpopaction(action,orgid):
    global orgpopactionames

    popactions = orgpopactionnames[orgid]
    
    if action in popactions:
        return True
    else:
        return False

#Creates specific pop actions for an internal species
def writepopaction(action,orgid,orgnumber,actionbefore,actionstring):
    global orgpopactions
    global orgpopactionames
    global orgmax
    result1 = ''
    result2 = ''
    operator = ''

    popactions = orgpopactionnames[orgid]

    for word in actionstring:
        if word == '>>' or word =='<<':
            operator = word
    
    if action in popactions:
        infolist=popactions[action]
        if operator == '>>':
            result1,result2 = createsyncadd2actions(orgnumber,orgid,action,infolist[3],actionbefore)
            return result1
        if operator == '<<':
            result1,result2 = createsyncadd2actions(orgnumber,orgid,action,infolist[3],actionbefore)
            return result2
    else:
        return action        
    


#Add organism id key and internal species list value to global variable orgspecies  
def addtoorgspeciesdictionary(p):
    #variables
    global orgspecies
    listofspecies = []
    biospeciesmodelcomponent = p[3].split()# split the biospeciesmodelcomponent into separate words
    for k, v in orgmax.items() :
        #If IDENTIFIER equals Organism IDENTIFIER key
        if p[1] == k:
            for word in biospeciesmodelcomponent:
                #If the word contains < or [ pass
                if '<' in word or '[' in word:
                    pass
                else :#This word is an internal species of organism add to list
                    listofspecies.append(word)
            #Add organism id key and species list value pair                  
            orgspecies[k] = listofspecies
            #Clear local list
            listofspecies = []
            
            
#Make Bio-PEPA model component out of organism components of PAL model
def makemodelcomponent(p):
    #Variables
    global orgmax
    global orginitial
    orgid = p[1]
    biospeciesmodelcomponent = p[3].split()# split the biospeciesmodelcomponent into separate words
    right = ''
    bioid = ''
    
    #Go through each key value pair in orgmax
    for k, v in orgmax.items() :
        #Only print if organism is the same as key organism
        if orgid == k:
            i = 1
            #Multiply organism internal species components to max organism value
            while i < int(v)+1:
                bioid = ''
                #Go through biospeciesmodelcomponent and examine each word
                for word in biospeciesmodelcomponent:
                    #Add org id only if word refers to an internal species
                    if '<' in word or '[' in word:
                        pass
                    else :
                        word += '_' + k + str(i)                     

                    #Add word to bioid even if it has not changed                   
                    bioid += word + ' '
                #Add On and Off components
                if i <= int(orginitial[k]):
                    bioid += '<*> On_' + k + str(i) + ' [1] <*> ' + 'Off_' + k + str(i) + ' [0] '
                else :
                    bioid += '<*> On_' + k + str(i) + ' [0] <*> ' + 'Off_' + k + str(i) + ' [1] '
                #Add a sync symbol between same organism species
                #but do not add to end of string
                i = i + 1
                if i < int(v) + 1:
                    bioid+= '<*> '
                right += bioid
    return right

# Build the parser and name of LALR table
parser = yacc.yacc(tabmodule="parsetab2")

def parse(model):
    result = parser.parse(model)
    return result

