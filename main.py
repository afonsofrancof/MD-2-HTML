import os
import sys

import ply.lex as lex

states = [
    ('bold', 'exclusive'),
    ('italic', 'exclusive'),
    ('underlined', 'exclusive'),
    ('strikethrough', 'exclusive'),
    ('list', 'exclusive'),
    ('image', 'exclusive'),
    ('header', 'exclusive')
]

tokens = ['BOLD', 'ITL', 'UNDLINE', 'STRIKE',
          'LISTO', 'LISTC',
          'IMAGEO', 'IMAGEC', 'IMAGEPROP',
          'HDR', 'TEXT', 'LINEDOWN']

# Global Variables
headerSize = 0


# formatação: negrito, itálico, sublinhado;
# • vários níveis de títulos;
# • listas de tópicos (items) não-numerados, numerados ou tipo entradas de um dicioná- rio ;
# • inclusão de imagens;
# • inclusão e formatação de tabelas;
# • todos os outros que achar necessário ou a sua imaginação vislumbrar.

# Header
def t_HDR(t):
    r'\@+'
    t.lexer.push_state('header')
    global headerSize
    headerSize = 0
    for character in t.value:
        if character == '@':
            headerSize += 1
    t.lexer.output += "<h" + str(headerSize) + ">"


def t_header_TEXT(t):
    r'.+'
    t.lexer.pop_state()
    t.lexer.output += t.value.strip()
    t.lexer.output += "</h" + str(headerSize) + ">"


# BOLD
def t_bold_BOLD(t):
    r'\$\$'
    t.lexer.pop_state()
    t.lexer.output += "</strong>"


def t_INITIAL_italic_underlined_strikethrough_BOLD(t):
    r'\$\$'
    a = t.lexer.lexstatestack
    if 'bold' in a:
        return t
    else:
        t.lexer.push_state('bold')
        t.lexer.output += "<strong>"


# Italic
def t_italic_ITL(t):
    r'//'
    t.lexer.pop_state()
    t.lexer.output += "</em>"


def t_INITIAL_bold_underlined_strikethrough_ITL(t):
    r'//'
    a = t.lexer.lexstatestack
    if 'italic' in a:
        return t
    else:
        t.lexer.push_state('italic')
        t.lexer.output += "<em>"


# UNDERLINED
def t_underlined_UNDLINE(t):
    r'__'
    t.lexer.pop_state()
    t.lexer.output += "</u>"


def t_INITIAL_bold_italic_strikethrough_UNDLINE(t):
    r'__'
    a = t.lexer.lexstatestack
    if 'underlined' in a:
        return t
    else:
        t.lexer.push_state('underlined')
        t.lexer.output += "<u>"


# STRIKETHROUGH
def t_strikethrough_STRIKE(t):
    r'--'
    t.lexer.pop_state()
    t.lexer.output += "</del>"


def t_INITIAL_bold_italic_underlined_STRIKE(t):
    r'--'
    a = t.lexer.lexstatestack
    if 'strikethrough' in a:
        return t
    else:
        t.lexer.push_state('strikethrough')
        t.lexer.output += "<del>"


# LIST

def t_list_LISTC(t):
    r'\]\ *'
    t.lexer.pop_state()
    match t.lexer.listtype:
        case "num":
            t.lexer.output += '</ol>'
        case "dot":
            t.lexer.output += '</ul>'
        case "dictionary":
            t.lexer.output += '</dl>'
        case _:
            pass
    return t


def t_INITIAL_LISTO(t):
    r'\[\ *\{\ *\w+\}'
    t.lexer.push_state('list')
    for character in r'[{} ':
        t.value = t.value.replace(character, "")
    match t.value:
        case "num":
            t.lexer.listtype = 'num'
            t.lexer.output += '<ol>'
        case "dot":
            t.lexer.listtype = 'dot'
            t.lexer.output += '<ul>'
        case "dictionary":
            t.lexer.listtype = "dictionary"
            t.lexer.output += '<dl>'
        case _:
            pass
    return t


def t_list_TEXT(t):
    r'\ *.+\ *'
    match t.lexer.listtype:
        case "dictionary":
            [word, definition] = t.value.split(":")
            t.lexer.output += '<dt>' + word.strip() + '</dt>'
            t.lexer.output += '<dd>' + definition.strip() + '</dd>'
        case _:
            t.lexer.output += '<li>' + t.value.strip() + '</li>'


# IMAGE

def t_INITIAL_IMAGEO(t):
    r'img\{'
    t.lexer.push_state('image')
    t.lexer.output += '<img '


def t_image_IMAGEC(t):
    r'\}'
    t.lexer.pop_state()
    t.lexer.output += '>'


def t_image_IMAGEPROP(t):
    r'\ *(.+)\ *\=\ *([^\}]+)\ *'
    t.lexer.output += t.value.strip()


# TEXT
def t_ANY_LINEDOWN(t):
    r'(\n\n)'
    t.lexer.output += '\n<br>\n'
    return t


def t_ANY_TEXT(t):
    r'(.|\n)'
    t.lexer.output += t.value
    return t


# ERROR
def t_ANY_error(t):
    print('Invalid Character!')


if len(sys.argv) < 3:
    sys.exit(1)
# Open input file
f = open(sys.argv[1], "r")
# Read input file
text = f.read()
# Close input file
f.close()

lexer = lex.lex()

lexer.input(text)

# Define our variable
lexer.output = ""
lexer.listtype = ""

for tok in lexer:
    pass

# CODE TO BE REMOVED
os.remove(sys.argv[2])
# END OF CODE TO BE REMOVED

# Open output file
outputFile = open(sys.argv[2], "x")
outputFile.write(lexer.output)
outputFile.close()
