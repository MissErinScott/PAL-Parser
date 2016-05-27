### PAL Grammar rules Parser

import ply.yacc as yacc

# Get the token map from the lexer.  This is required.
from PALLexer import tokens

###Starting rule which specifies the parts of a PAL model
def p_palmodel_1(p):
    'palmodel : initialresets parameters actionrates biospeciesbehaviours hiddenactionsset organisms populations modelcomponent maxpoplist'
    p[0] = p[9] + '\n' + p[8] + '\n' + p[7] + '\n' + p[6] + '\n' + p[1] + '\n' + p[4] +'\n' + p[2] + '\n'+ p[3]
#Second starting rule as some PAL models will have actionrates for populations
def p_palmodel_2(p):
    'palmodel : initialresets parameters actionrates biospeciesbehaviours hiddenactionsset organisms actionrates populations modelcomponent maxpoplist'
    p[0] = p[10] + '\n' + p[9] + '\n' + p[8] + '\n' + p[6] + '\n' + p[1] + '\n' + p[4] + '\n' + p[2] + '\n'+ p[3] + p[7]

#initial reset rules
def p_intialresets_1(p):
    'initialresets : initialresets initialreset'
    p[0] = p[1] + p[2]

def p_intialresets_2(p):
    'initialresets : initialreset'
    p[0] = p[1]

def p_initialreset(p):
    'initialreset : IDENTIFIER IDENTIFIER EQUALS expression SEMICOLON'
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
    p[0] = p[1] + ' = ' + p[3] + ' ; ' + '\n'

#action rate rules
def p_actionrates_1(p):
    'actionrates : actionrates actionrate'
    p[0] = p[1] + p[2]

def p_actionrates_2(p):
    'actionrates : actionrate'
    p[0] = p[1]

def p_actionrate(p):
    'actionrate : IDENTIFIER COLON expression SEMICOLON'
    p[0] = p[1] + ' : ' + p[3] + ' ; ' + '\n'

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
    p[0] = p[1]

def p_factor2(p):
    'factor : MINUS NUMBER'
    p[0] = p[1] + p[2]


def p_factor_expr(p):
    'factor : LEFTBRACKET expression RIGHTBRACKET'
    p[0] = p[1] + p[2] + p[3]

#For Heaviside step function,fMA,exp
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
    p[0] = p[1] + ' ' + p[2] + ' ' + p[3] + ' ' + p[4] + '\n'

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
    p[0] = p[1] + p[2] + p[3] + ' ' + p[4] + p[5]+ ' ' + p[6]

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
    p[0] = p[1] + p[2]
    
def p_organisms_2(p):
    'organisms : organism'
    p[0] = p[1]

def p_organism(p):
    'organism : IDENTIFIER EQUALS biospeciesmodelcomponent'
    p[0] = p[1] + ' ' + p[2] + ' ' + p[3] + '\n'
    

def p_biospeciesmodelcomponent_1(p):
    'biospeciesmodelcomponent : biospeciesmodelcomponent biosync bioinitial'
    p[0] = p[1] + ' ' + p[2] + ' ' + p[3]
    
def p_biospeciesmodelcomponent_2(p):
    'biospeciesmodelcomponent : bioinitial'
    p[0] = p[1]

def p_bioinitial(p):
    'bioinitial : IDENTIFIER LEFTSQUAREBRACKET NUMBER RIGHTSQUAREBRACKET'
    p[0] = p[1] + p[2] + p[3] + p[4]

def p_biosync(p):
    '''biosync : LEFTANGLEBRACKET TIMES RIGHTANGLEBRACKET
               | LEFTANGLEBRACKET listofids RIGHTANGLEBRACKET '''
    p[0] = p[1] + p[2] + p[3]

#population
def p_populations_1(p):
    'populations : populations population'
    p[0] = p[1] + p[2]
    
def p_populations_2(p):
    'populations : population'
    p[0] = p[1]
    
def p_population(p):
    'population : populationid EQUALS popactions SEMICOLON'
    p[0] = p[1] + ' ' + p[2] + ' ' + p[3] + ' ' + p[4] + '\n'   

def p_populationid(p):
    'populationid : IDENTIFIER LEFTDOUBLECURLYBRACKET IDENTIFIER RIGHTDOUBLECURLYBRACKET'
    p[0] = p[1] + p[2] + p[3] + p[4]

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


#modelcomponent
def p_modelcomponent_1(p):
    ' modelcomponent : modelcomponent palsync popinitial'
    p[0] = p[1] + ' ' + p[2] + ' ' + p[3] + '\n'

def p_modelcomponent_2(p):
    ' modelcomponent : popinitial'
    p[0] = p[1]

def p_popinitial_1(p):
    'popinitial : populationid LEFTDOUBLESQUAREBRACKET NUMBER RIGHTDOUBLESQUAREBRACKET'
    p[0] = p[1] + p[2] + p[3] + p[4]

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
    p[0] = p[1] + p[2] + ' ' + p[3] + p[4] + '\n'

def p_listofmaxpops_1(p):
    'listofmaxpops : listofmaxpops COMMA popmax'
    p[0] = p[1] + p[2] + p[3]

def p_listofmaxpops_2(p):
    'listofmaxpops : popmax'
    p[0] = p[1]

def p_popmax(p):
    'popmax : IDENTIFIER LEFTDOUBLECURLYBRACKET IDENTIFIER RIGHTDOUBLECURLYBRACKET NUMBER'
    p[0] = p[1] + p[2] + p[3] + p[4] + ' ' + p[5]

#Hidden actions set parser does not output this
def p_hiddenactionsset(p):
    'hiddenactionsset : IDENTIFIER IDENTIFIER COLON LEFTCURLYBRACKET listofids RIGHTCURLYBRACKET SEMICOLON'
    pass
    
# Error rule for syntax errors
def p_error(p):
    #raise TypeError("unknown text at "(p.value,))
    #print("Syntax error in input: " + (p.value))
    if p:
         print("Syntax ERROR at token: ","Type: ", p.type,"Value:" , p.value ,"LineNo: ", p.lineno)
         
         # Just discard the token and tell the parser it's okay.
         #parser.errok()
    else:
         print("Syntax error at End Of File")

# Build the parser
parser = yacc.yacc(tabmodule="parsetab1")

def parse(model):
    result = parser.parse(model)
    return result


##with open('TestCases2/onepoponespecies.pal', 'r')as myfile:
##    model=myfile.read()
##    #print('PAL Model:')
##    #print(model)
##    result = parser.parse(model)
##    print('Bio-PEPA Model:')
##    print(result)
