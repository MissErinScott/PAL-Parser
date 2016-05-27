# PAL tokenizer Lexer

import ply.lex as lex

#List of token names.
tokens = (
    'IDENTIFIER',
    'EQUALS',
    'NUMBER',
    'TIMES',
    'PLUS',
    'MINUS',
    'DIVIDE',
    'LEFTBRACKET',
    'RIGHTBRACKET',
    'LEFTCURLYBRACKET',
    'RIGHTCURLYBRACKET',
    'LEFTSQUAREBRACKET',
    'RIGHTSQUAREBRACKET',
    'COLON',
    'SEMICOLON',
    'BIOPRODUCT',
    'BIOREACTANT',
    'BIOMODIFIER',
    'BIOACTIVATOR',
    'BIOINHIBITOR',
    'PALADDITION',
    'PALDELETION',
    'PALACTIVATOR',
    'RIGHTDOUBLECURLYBRACKET',
    'LEFTDOUBLECURLYBRACKET',
    'COMMA',
    'RIGHTDOUBLESQUAREBRACKET',
    'LEFTDOUBLESQUAREBRACKET',
    'LEFTANGLEBRACKET',
    'RIGHTANGLEBRACKET',
    'POWER',
#    'DOUBLEFORWARDSLASH',
    )

#Regular expression rules for simple tokens
t_IDENTIFIER =  r'[a-zA-Z_][a-zA-Z_0-9]*'
t_NUMBER = r'[0-9]+ (\.[0-9]+)?'
t_PALACTIVATOR = r'\(\(\+\)\)'
t_PALADDITION = r'>>>'
t_PALDELETION = r'<<<'
t_BIOMODIFIER = r'\(\.\)'
t_BIOACTIVATOR = r'\(\+\)'
t_BIOINHIBITOR = r'\(-\)'
t_BIOPRODUCT = r'>>'
t_BIOREACTANT = r'<<'
t_RIGHTDOUBLECURLYBRACKET = r'\}\}'
t_LEFTDOUBLECURLYBRACKET = r'\{\{'
t_RIGHTDOUBLESQUAREBRACKET = r'\]\]'
t_LEFTDOUBLESQUAREBRACKET = r'\[\['
t_LEFTCURLYBRACKET = r'\{'
t_RIGHTCURLYBRACKET = r'\}'
t_LEFTSQUAREBRACKET = r'\['
t_RIGHTSQUAREBRACKET = r'\]'
t_LEFTBRACKET = r'\('
t_RIGHTBRACKET = r'\)'
t_EQUALS = r'\='
t_PLUS = r'\+'
t_MINUS = r'-'
t_TIMES = r'\*'
t_DIVIDE = r'/'
t_COLON = r'\:'
t_SEMICOLON = r'\;'
t_COMMA = r','
t_LEFTANGLEBRACKET = r'<'
t_RIGHTANGLEBRACKET = r'>'
t_POWER = r'\^'
#t_DOUBLEFORWARDSLASH = r'//'


# Define a rule so we can track line numbers
def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

# A string containing ignored characters (spaces and tabs)
t_ignore  = ' \t'

# Error handling rule
def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)

# Build the lexer
lexer = lex.lex()

# Test Lexer with test case model
##with open('TestCases/anglebrackets.pal', 'r')as myfile:
##    model=myfile.read()
##    print(model)

##
### Give the lexer some input
##lexer.input(model)
##
### Tokenize
##while True:
##    tok = lexer.token()
##    if not tok: 
##        break      # No more input
##    print(tok.type, tok.value)
##    #print(tok.type, tok.value, tok.lineno, tok.lexpos)



