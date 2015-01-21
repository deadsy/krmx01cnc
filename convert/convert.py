#! /usr/bin/python
#------------------------------------------------------------------------------

import sys

comments = False

#------------------------------------------------------------------------------
# scanner

import ply.lex as lex

# token names
tokens = (
  'A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z',
  'INTEGER',
  'DECIMAL',
  'COMMENT',
)

t_A = r'A|a'
t_B = r'B|b'
t_C = r'C|c'
t_D = r'D|d'
t_E = r'E|e'
t_F = r'F|f'
t_G = r'G|g'
t_H = r'H|h'
t_I = r'I|i'
t_J = r'J|j'
t_K = r'K|k'
t_L = r'L|l'
t_M = r'M|m'
t_N = r'N|n'
t_O = r'O|o'
t_P = r'P|p'
t_Q = r'Q|q'
t_R = r'R|r'
t_S = r'S|s'
t_T = r'T|t'
t_U = r'U|u'
t_V = r'V|v'
t_W = r'W|w'
t_X = r'X|x'
t_Y = r'Y|y'
t_Z = r'Z|z'

t_INTEGER = r'\d+'
t_DECIMAL = r'[+-]*\d*\.\d*'

def t_COMMENT(t):
  r'\(.*\)|[;%].*'
  pass

# A string containing ignored characters (spaces and tabs)
t_ignore  = ' \r\t'

# Define a rule so we can track line numbers
def t_newline(t):
  r'\n'
  t.lexer.lineno += len(t.value)

# Error handling rule
def t_error(t):
  print "illegal character '%s'" % t.value[0]
  t.lexer.skip(1)

# Build the lexer
lexer = lex.lex()

#------------------------------------------------------------------------------
# parser

import ply.yacc as yacc

def p_lines(p):
  '''lines : lines line
           | line'''
  pass

def p_line(p):
  '''line : line_number words
          | words'''
  if len(p) == 3:
    print p[2]
  if len(p) == 2:
    print p[1]

def p_words(p):
  '''words : words word
           | word'''
  if len(p) == 3:
    p[0] = '%s %s' % (p[1], p[2])
  else:
    p[0] = p[1]

def p_line_number(p):
  'line_number : N INTEGER'
  p[0] = None

def p_word(p):
  '''word : general_function
          | tool_selection
          | misc_function
          | feed_rate
          | spindle_speed
          | tool_length_offset_index
          | arc_radius
          | feed_increment
          | dwell_time
          | x_offset
          | y_offset
          | z_offset
          | x_axis
          | y_axis
          | z_axis
          | a_axis
          | b_axis
          | c_axis
          | u_axis
          | v_axis
          | w_axis'''
  p[0] = p[1]

def p_general_function(p):
  'general_function : G INTEGER'
  description = {
    '00': 'rapid move',
    '01': 'linear move',
    '17': 'xy plane',
    '20': 'use inches',
    '21': 'use mm',
    '40': 'cutter compensation off',
    '43': 'tool length offset',
    '49': 'cancel tool length compensation',
    '70': '??',
    '80': 'cancel canned cycle',
    '90': 'abs distance',
    '91': 'inc distance',
    '93': 'feed inverse time',
    '94': 'feed units/min',
    '95': 'feed units/rev',
  }
  if comments and description.has_key(p[2]):
    p[0] = 'g%s (%s)' % (p[2], description[p[2]])
  else:
    p[0] = 'g%s' % p[2]

def p_tool_selection(p):
  'tool_selection : T INTEGER'
  if comments:
    p[0] = 't%s (select tool)' % p[2]
  else:
    p[0] = 't%s' % p[2]


def p_misc_function(p):
  'misc_function : M INTEGER'
  description = {
    '03': 'start spindle clockwise',
    '06': 'tool change',
    '09': 'coolant off',
    '30': 'program end',
  }
  if comments and description.has_key(p[2]):
    p[0] = 'm%s (%s)' % (p[2], description[p[2]])
  else:
    p[0] = 'm%s' % p[2]

def p_feed_rate(p):
  'feed_rate : F DECIMAL'
  p[0] = 'f%s' % p[2]

def p_spindle_speed(p):
  'spindle_speed : S INTEGER'
  p[0] = 's%s' % p[2]

def p_tool_length_offset_index(p):
  'tool_length_offset_index : H INTEGER'
  if comments:
    p[0] = 'h%s (tool length offset index)' % p[2]
  else:
    p[0] = 'h%s' % p[2]

def p_x_axis(p):
  'x_axis : X DECIMAL'
  p[0] = 'x%s' % p[2]

def p_y_axis(p):
  'y_axis : Y DECIMAL'
  p[0] = 'y%s' % p[2]

def p_z_axis(p):
  'z_axis : Z DECIMAL'
  p[0] = 'z%s' % p[2]

def p_a_axis(p):
  'a_axis : A DECIMAL'
  p[0] = 'a%s' % p[2]

def p_b_axis(p):
  'b_axis : B DECIMAL'
  p[0] = 'b%s' % p[2]

def p_c_axis(p):
  'c_axis : C DECIMAL'
  p[0] = 'c%s' % p[2]

def p_u_axis(p):
  'u_axis : U DECIMAL'
  p[0] = 'u%s' % p[2]

def p_v_axis(p):
  'v_axis : V DECIMAL'
  p[0] = 'v%s' % p[2]

def p_w_axis(p):
  'w_axis : W DECIMAL'
  p[0] = 'w%s' % p[2]

def p_x_offset(p):
  'x_offset : I DECIMAL'
  p[0] = 'i%s' % p[2]

def p_y_offset(p):
  'y_offset : J DECIMAL'
  p[0] = 'j%s' % p[2]

def p_z_offset(p):
  'z_offset : K DECIMAL'
  p[0] = 'k%s' % p[2]

def p_dwell_time(p):
  'dwell_time : P DECIMAL'
  p[0] = 'p%s' % p[2]

def p_feed_increment(p):
  'feed_increment : Q DECIMAL'
  p[0] = 'q%s' % p[2]

def p_arc_radius(p):
  'arc_radius : R DECIMAL'
  p[0] = 'r%s' % p[2]

# Error rule for syntax errors
def p_error(p):
  print "syntax error at token", p.type
  # Just discard the token and tell the parser it's okay.
  parser.errok()

parser = yacc.yacc()

#------------------------------------------------------------------------------
# scan for tokens (debug)

def scan(x):
  lexer.input(x)
  while True:
    tok = lexer.token()
    if not tok:
      break
    print tok

#------------------------------------------------------------------------------

def usage():
  print "usage: convert.py <filename>"
  sys.exit(0)

#------------------------------------------------------------------------------

def main():

  if len(sys.argv) < 2:
    usage()
  f = open(sys.argv[1], 'r')
  x = f.read()
  f.close()
  parser.parse(x)
  sys.exit(0)

main()

#------------------------------------------------------------------------------


