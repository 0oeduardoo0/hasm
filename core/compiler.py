import sys
import ply.yacc as yacc
from lexer import tokens

program = {
     "procs": {}
   , "headers": []
}

instructions = []

def p_program(p):
   """program : headers procedures"""

def p_procedures(p):
   """procedures : procedure procedures
                 | empty"""

def p_procedure(p):
   """procedure : id lkey instructions rkey"""

   global instructions

   program["procs"][p[1]] = instructions
   instructions = []

def p_instructions(p):
   """instructions : instruc instructions
                   | empty"""

def p_instruc(p):
   """instruc : id operands point_comma"""
   
   instruc = {
        "name": p[1]
      , "operands": p[2]
      , "lineno": p.lexer.lineno - 1
   }

   instructions.append(instruc)

def p_headers(p):
   """headers : header headers
                  | empty"""

def p_header(p):
   """header : point id operands point_comma"""
   
   header = {
        "name": p[2]
      , "operands": p[3]
      , "lineno": p.lexer.lineno
   }

   program["headers"].append(header)

def p_operands_double(p):
   """operands : operand comma operand"""
   p[0] = [p[1], p[3]]

def p_operands_single(p):
   """operands : operand"""
   p[0] = [p[1], None]

def p_operands_empty(p):
   """operands : empty"""
   p[0] = [None, None]

def p_operand_id(p):
   """operand : id"""
   
   p[0] = {
        "type":"id"
      , "value":p[1]
   }

def p_operand_int(p):
   """operand : integer"""
   
   p[0] = {
        "type":"integer"
      , "value":int(p[1])
   }

def p_operand_float(p):
   """operand : float"""

   p[0] = {
        "type": "float"
      , "value": float(p[1])
   }

def p_operand_string(p):
   """operand : string"""
   
   p[0] = {
        "type": "string"
      , "value": p[1].replace("\"","")
   }

def p_operand_array_pointer(p):
   """operand : lbrack id comma integer rbrack"""
   
   p[0] = {
        "type": "array_pointer"
      , "value": p[2]
      , "index": int(p[4])
   }

def p_operand_array_with_lenght(p):
   """operand : lbrack integer rbrack"""
   
   p[0] = {
        "type": "array"
      , "value": [None] * int(p[2])
   }

def p_operand_array(p):
   """operand : lbrack rbrack"""
   
   p[0] = {
        "type": "array"
      , "value": []
   }

def p_empty(p):
   """empty : """
   pass

def p_error(p):
   print "HASM 0.1"
   print "Fatal: sintax error at line %s unexpected t_%s '%s'" % (p.lexer.lineno, p.type, p.value)
   sys.exit()

parser = yacc.yacc()

def parse_code(code):
   code += "\n"
   result = parser.parse(code)
   return program