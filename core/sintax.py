import ply.yacc as yacc
from lexer import tokens

program = {
     "procs": []
   , "defs": []
}

instructions = []

def p_program(p):
   """program : definitions procedures"""

def p_procedures(p):
   """procedures : procedure procedures
                 | empty"""

def p_procedure(p):
   """procedure : id instruc_end lkey instruc_end instructions rkey instruc_end"""

   global instructions

   proc = {
        "name": p[1]
      ,"instructions": instructions
   }

   program["procs"].append(proc)
   instructions = []

def p_instructions(p):
   """instructions : instruc instructions
                   | empty"""

def p_instruc(p):
   """instruc : id operands instruc_end"""
   
   instruc = {
        "name": p[1]
      , "operands": p[2]
   }

   instructions.append(instruc)

def p_definitions(p):
   """definitions : definition definitions
                  | empty"""

def p_definition(p):
   """definition : point id operands instruc_end"""
   
   definition = {
        "name": p[2]
      , "operands": p[3]
   }

   program["defs"].append(definition)

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
      , "value": p[1]
   }

def p_intruct_end(p):
   """instruc_end : newline"""
   p[0] = p[1]
   
   p.lexer.lineno += len(p[1])

def p_empty(p):
   """empty : """
   pass

#def p_error(p):
#   print "Error de sintaxis"

parser = yacc.yacc()

def parse_code(code):

   result = parser.parse(code)
   return program