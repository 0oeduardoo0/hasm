
# parsetab.py
# This file is automatically generated. Do not edit.
_tabversion = '3.2'

_lr_method = 'LALR'

_lr_signature = 'C"r\x1ak\x96D?\xd8L\x97a\xac\xb3\xbd\x18'
    
_lr_action_items = {'newline':([7,10,12,13,14,15,16,17,18,24,25,27,31,33,],[-19,20,-16,-17,20,-12,-15,-14,-13,20,-11,-19,20,20,]),'string':([7,23,27,],[13,13,13,]),'point':([0,1,20,22,],[2,2,-18,-10,]),'float':([7,23,27,],[12,12,12,]),'lkey':([20,21,],[-18,24,]),'rkey':([20,26,28,29,30,32,34,],[-18,-19,-19,-6,33,-5,-7,]),'comma':([12,13,15,16,17,],[-16,-17,23,-15,-14,]),'integer':([7,23,27,],[16,16,16,]),'id':([0,1,2,4,5,6,7,8,20,22,23,26,27,28,34,35,],[-19,-19,7,10,-9,-8,17,10,-18,-10,17,27,17,27,-7,-4,]),'$end':([0,1,3,4,5,6,8,9,11,19,20,22,35,],[-19,-19,0,-19,-9,-8,-19,-1,-3,-2,-18,-10,-4,]),}

_lr_action = { }
for _k, _v in _lr_action_items.items():
   for _x,_y in zip(_v[0],_v[1]):
      if not _x in _lr_action:  _lr_action[_x] = { }
      _lr_action[_x][_k] = _y
del _lr_action_items

_lr_goto_items = {'definition':([0,1,],[1,1,]),'operands':([7,27,],[14,31,]),'instruc_end':([10,14,24,31,33,],[21,22,26,34,35,]),'program':([0,],[3,]),'empty':([0,1,4,7,8,26,27,28,],[5,5,11,18,11,29,18,29,]),'operand':([7,23,27,],[15,25,15,]),'definitions':([0,1,],[4,6,]),'procedures':([4,8,],[9,19,]),'instruc':([26,28,],[28,28,]),'procedure':([4,8,],[8,8,]),'instructions':([26,28,],[30,32,]),}

_lr_goto = { }
for _k, _v in _lr_goto_items.items():
   for _x,_y in zip(_v[0],_v[1]):
       if not _x in _lr_goto: _lr_goto[_x] = { }
       _lr_goto[_x][_k] = _y
del _lr_goto_items
_lr_productions = [
  ("S' -> program","S'",1,None,None,None),
  ('program -> definitions procedures','program',2,'p_program','/home/eduardo/.lsc/core/sintax.py',12),
  ('procedures -> procedure procedures','procedures',2,'p_procedures','/home/eduardo/.lsc/core/sintax.py',15),
  ('procedures -> empty','procedures',1,'p_procedures','/home/eduardo/.lsc/core/sintax.py',16),
  ('procedure -> id instruc_end lkey instruc_end instructions rkey instruc_end','procedure',7,'p_procedure','/home/eduardo/.lsc/core/sintax.py',19),
  ('instructions -> instruc instructions','instructions',2,'p_instructions','/home/eduardo/.lsc/core/sintax.py',32),
  ('instructions -> empty','instructions',1,'p_instructions','/home/eduardo/.lsc/core/sintax.py',33),
  ('instruc -> id operands instruc_end','instruc',3,'p_instruc','/home/eduardo/.lsc/core/sintax.py',36),
  ('definitions -> definition definitions','definitions',2,'p_definitions','/home/eduardo/.lsc/core/sintax.py',46),
  ('definitions -> empty','definitions',1,'p_definitions','/home/eduardo/.lsc/core/sintax.py',47),
  ('definition -> point id operands instruc_end','definition',4,'p_definition','/home/eduardo/.lsc/core/sintax.py',50),
  ('operands -> operand comma operand','operands',3,'p_operands_double','/home/eduardo/.lsc/core/sintax.py',60),
  ('operands -> operand','operands',1,'p_operands_single','/home/eduardo/.lsc/core/sintax.py',64),
  ('operands -> empty','operands',1,'p_operands_empty','/home/eduardo/.lsc/core/sintax.py',68),
  ('operand -> id','operand',1,'p_operand_id','/home/eduardo/.lsc/core/sintax.py',72),
  ('operand -> integer','operand',1,'p_operand_int','/home/eduardo/.lsc/core/sintax.py',80),
  ('operand -> float','operand',1,'p_operand_float','/home/eduardo/.lsc/core/sintax.py',88),
  ('operand -> string','operand',1,'p_operand_string','/home/eduardo/.lsc/core/sintax.py',96),
  ('instruc_end -> newline','instruc_end',1,'p_intruct_end','/home/eduardo/.lsc/core/sintax.py',104),
  ('empty -> <empty>','empty',0,'p_empty','/home/eduardo/.lsc/core/sintax.py',110),
]
