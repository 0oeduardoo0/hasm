def is_id_operand(op):
   if op["type"] == "id":
      return True

   return False

def is_array_pointer_operand(op):
   if op["type"] == "array_pointer":
      return True

   return False

def is_array_operand(op):
   if op["type"] == "array":
      return True

   return False

def is_string_operand(op):
   if op["type"] == "string":
      return True

   return False

def is_numeric_operand(op):
   if op["type"] == "integer" or op["type"] == "float":
      return True

   return False

def is_integer_operand(op):
   if op["type"] == "integer":
      return True

   return False

def make_nil():
   op = {
        "type": "nil"
      , "value": None
   }

   return op

def make_string(value):
   op = {
        "type": "string"
      , "value": value
   }

   return op

def make_integer(value):
   op = {
        "type": "integer"
      , "value": value
   }

   return op

def make_float(value):
   op = {
        "type": "float"
      , "value": value
   }

   return op