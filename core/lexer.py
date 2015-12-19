import ply.lex as lex

tokens = (
   'id',
   'integer',
   'float',
   'string',
   'rbrack',
   'lbrack',
   'comment',
   'comma',
   'point',
   'point_comma',
   'newline',
   'lkey',
   'rkey',
)

t_ignore = ' \t'

t_id  = r'(\w+)'
t_integer = r'([0-9]+)'
t_float   = r'([0-9]+)(\.)([0-9]+)'
t_string  = r'(\".*?\")'
t_rbrack  = r'\]'
t_lbrack  = r'\['
t_comma   = r'\,'
t_point   = r'\.'
t_point_comma = r'\;'
#t_newline = r'\n+'
t_lkey = r'\{'
t_rkey = r'\}'

def t_ignore_comment(t):
   r'\#.*'
   pass

def t_ignore_newline(t):
   r'\n+'
   t.lexer.lineno += len(t.value)
   pass

def t_error(t):
   print "Simbolo ilegal '%s'" % (t.value[0])
   t.lexer.skip(1)

lexer = lex.lex()

def parse_tokens(input):

   lexer.input(input)

   while 1:

      tok = lexer.token()

      if not tok:
         break

      print tok