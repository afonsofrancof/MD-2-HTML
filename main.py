import ply.lex as lex

states = [
    ('bold', 'exclusive'),
    ('italic', 'exclusive'),
]

tokens = ['BOLD', 'ITL']


# BOLD
def t_INITIAL_BOLD(t):
    r'**'
    t.lexer.push_state('bold')
    print(t.lexer.lexstateinfo)
def t_bold_BOLD(t):
    r'**'
    t.lexer.pop_state()

def t_italic_BOLD(t):
    r'**'
    t.lexer.push_state('bold')

def t_INITIAL_ITL(t):
    r'//'
    t.lexer.push_state('italic')

def t_italic_itl(t):
    r'//'
    t.lexer.pop_state()

def t_ANY_error(t):
    print('Invalid Character!')


lexer = lex.lex()
