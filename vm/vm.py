import sys

# ---------------------------
# Instruc set helpers

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

def operand_real_value(op):
   if is_id_operand(op):
      
      if reg_exists(op):
         return reg_value(op, None)

      handle_error("registre '%s' dont exists" % (op["value"]))
      return {"type":"nil","value":None}

   elif is_array_pointer_operand(op):
      
      if reg_exists(op):

         try:
         
            r = reg_value(op, None)

            if not is_array_operand(r):
               handle_fatal_error("'%s' is not an array" % (op["value"]))

            r = r["value"][op["index"]]
         
         except:
            
            handle_error("%s[%s] index out of range" % (op["value"], op["index"]))
            return {"type":"nil","value":None}

         return r

      handle_error("registre '%s' dont exists" % (op["value"]))
      return {"type":"nil","value":None}

   else:

      return op

def reg_exists(reg):
   global regs

   try:

      regs[reg["value"]]

   except:

      return False

   return True

def reg_value(reg, mode):
   global regs
   
   if mode == None:
      return regs[reg["value"]]
   else:
      regs[reg["value"]] = mode

def expects_2_operands(lo, ro):
   if lo == None or ro == None:
      handle_fatal_error("instruction : expects two operands")

def expects_1_operands(lo, ro):
   if ro != None:
      handle_fatal_error("instruction : expects a single operand")

def not_expects_operands(lo, ro):
   if lo != None or ro != None:
      handle_fatal_error("instruction : not expects operands")

def parse_instruct_args(args):
   return [args["operands"][0], args["operands"][1]]

# ---------------------------

# ---------------------------
# Instruc set

def aritmetic_operations_instruc(args, operation):
   global regs

   lo, ro = parse_instruct_args(args)

   if operation == "inc" or operation == "dec":
      expects_1_operands(lo, ro)
   else:
      expects_2_operands(lo, ro)

   if not is_id_operand(lo):
      handle_fatal_error("%s : left operand must be an identifier" % (operation))

   real_lo = operand_real_value(lo)

   if not is_numeric_operand(real_lo):
      handle_fatal_error("%s : only works with numeric operands" % (operation))

   if operation == "inc":
      real_lo["value"] += 1
   elif operation == "dec":
      real_lo["value"] -= 1
   else:
      
      ro = operand_real_value(ro)

      if not is_numeric_operand(ro):
         handle_fatal_error("%s : only works with numeric operands" % (operation))

      if operation == "add":
         real_lo["value"] += ro["value"]
      elif operation == "sub":
         real_lo["value"] -= ro["value"]
      elif operation == "mul":
         real_lo["value"] *= ro["value"]
      elif operation == "div":
         real_lo["value"] /= ro["value"]
      elif operation == "pow":
         real_lo["value"] = real_lo["value"] ** ro["value"]
      elif operation == "sqr":
         real_lo["value"] = real_lo["value"] ** (1.0 / ro["value"])

   reg_value(lo, real_lo)

def inc_instruc(args):
   aritmetic_operations_instruc(args, "inc")

def dec_instruc(args):
   aritmetic_operations_instruc(args, "dec")

def add_instruc(args):
   aritmetic_operations_instruc(args, "add")

def sub_instruc(args):
   aritmetic_operations_instruc(args, "sub")

def mul_instruc(args):
   aritmetic_operations_instruc(args, "mul")

def div_instruc(args):
   aritmetic_operations_instruc(args, "div")

def pow_instruc(args):
   aritmetic_operations_instruc(args, "pow")

def sqr_instruc(args):
   aritmetic_operations_instruc(args, "sqr")

def var_instruc(args):
   lo, ro = parse_instruct_args(args)

   expects_2_operands(lo, ro)

   if not is_id_operand(lo):
      handle_fatal_error("var : left operand must be an identifier")

   ro = operand_real_value(ro)

   reg_value(lo, ro)

def call_instruc(args):
   lo, ro = parse_instruct_args(args)

   expects_1_operands(lo, ro)

   if not is_id_operand(lo):
      handle_fatal_error("var : left operand must be an identifier")

   execute_proc(lo["value"])

def mov_instruc(args):
   lo, ro = parse_instruct_args(args)

   expects_2_operands(lo, ro)

   if not is_id_operand(lo) and not is_array_pointer_operand(lo):
      handle_fatal_error("mov : left operand must be a registre")

   if not reg_exists(lo):
      handle_fatal_error("mov : left operand '%s' don't exists" % (lo["value"]))

   ro = operand_real_value(ro)

   if is_array_pointer_operand(lo):

      real_lo = reg_value(lo, None)
      real_lo["value"][lo["index"]] = ro
      reg_value(lo, real_lo)

   else:

      reg_value(lo, ro)

def push_instruc(args):
   lo, ro = parse_instruct_args(args)

   expects_2_operands(lo, ro)

   if not is_id_operand(lo):
      handle_fatal_error("push : left operand must be a registre")

   if not reg_exists(lo):
      handle_fatal_error("push : left operand '%s' don't exists" % (lo["value"]))

   real_lo = operand_real_value(lo)

   if not is_array_operand(real_lo):
      handle_fatal_error("push : left operand must be an array")

   ro = operand_real_value(ro)

   real_lo["value"].append(ro)

   reg_value(lo, real_lo)

def raw_instruc(args):
   lo, ro = parse_instruct_args(args)

   expects_1_operands(lo ,ro)

   lo = operand_real_value(lo)

   print lo

def out_instruc(args):
   lo, ro = parse_instruct_args(args)

   lo = operand_real_value(lo)

   if ro != None:
      ro = operand_real_value(ro)
      lo["value"] = lo["value"].replace("\\$", str(ro["value"]))

   sys.stdout.write(lo["value"].replace("\\n","\n"))
   sys.stdout.flush()

def inp_instruc(args):
   lo, ro = parse_instruct_args(args)

   expects_2_operands(lo, ro)

   if not is_id_operand(lo) and not is_array_pointer_operand(lo):
      handle_fatal_error("inp : left operand must be a registre")

   if not reg_exists(lo):
      handle_fatal_error("inp : left operand '%s' don't exists" % (lo["value"]))

   input = raw_input(ro["value"])

   ro = {"type":"string", "value":input}

   if is_array_pointer_operand(lo):

      real_lo = reg_value(lo, None)
      real_lo["value"][lo["index"]] = ro
      reg_value(lo, real_lo)

   else:

      reg_value(lo, ro)

def ext_instruc(args):
   lo, ro = parse_instruct_args(args)

   not_expects_operands(lo, ro)
   sys.exit()


instruc_set = {
     "var": var_instruc
   , "mov": mov_instruc
   , "raw": raw_instruc
   , "out": out_instruc
   , "inp": inp_instruc
   , "ext": ext_instruc
   , "inc": inc_instruc
   , "dec": dec_instruc
   , "add": add_instruc
   , "sub": sub_instruc
   , "mul": mul_instruc
   , "div": div_instruc
   , "pow": pow_instruc
   , "sqr": sqr_instruc
   , "call": call_instruc
   , "push": push_instruc
}

# ----------------------------

lineno = 0
prog_tree = None
regs = {
     "fx": None
   , "px": None
   , "rx": None
}

def handle_error(error):
   global lineno

   print "Error: %s, on line %s" % (error, lineno)

def handle_fatal_error(error):
   global lineno

   print "Fatal: %s, on line %s" % (error, lineno)
   sys.exit()

#def execute_header(header):

def execute_instruc(instruc):
   global lineno

   lineno = instruc["lineno"]

   try:

      instruc_caller = instruc_set[instruc["name"]]

   except:

      handle_fatal_error("Unknown instruction '%s'" % (instruc["name"]))

   instruc_caller(instruc)

def execute_proc(proc):
   global prog_tree
   global lineno
   
   try:

      proc = prog_tree["procs"][proc]

   except:

      handle_fatal_error("Undefined procedure '%s'" % (proc))

   for instruc in proc:
      execute_instruc(instruc)

def execute_prog(pt):
   global prog_tree

   prog_tree = pt

#   for header in prog_tree["headers"]:
#      execute_header(header)

   execute_proc("main")