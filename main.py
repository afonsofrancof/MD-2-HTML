import ply.lex as lex

states = [
    ('bold', 'exclusive'),
    ('italic', 'exclusive'),
]

tokens = ['BOLD', 'ITL', 'TEXT']


# BOLD
def t_bold_BOLD(t):
    r'\*\*'
    t.lexer.pop_state()
    print("</b>", end="")

def t_italic_BOLD(t):
    r'\*\*'
    a = t.lexer.lexstatestack
    if 'bold' in a:
        pass
    else:
        t.lexer.push_state('bold')
        print("<b>", end="")

def t_BOLD(t):
    r'\*\*'
    t.lexer.push_state('bold')
    print("<b>", end="")



#Italic

def t_italic_ITL(t):
    r'//'
    t.lexer.pop_state()
    print("</i>", end="")

def t_bold_ITL(t):
    r'//'
    a = t.lexer.lexstatestack
    if 'italic' in a:
        pass
    else:
        t.lexer.push_state('italic')
        print("<i>", end="")

def t_ITL(t):
    r'//'
    t.lexer.push_state('italic')
    print("<i>", end="")

#TEXT
def t_ANY_TEXT(t):
    r'(.|\n)'
    print(t.value, end="")
    pass
#ERROR
def t_ANY_error(t):
    print('Invalid Character!')


lexer = lex.lex()

f = open("a.txt", "r")
text = f.read()
lexer.input(text)
f.close()

for tok in lexer:
    pass
