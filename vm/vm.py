import sys

from core import types

# ---------------------------
# Instruc set helpers

def unlik_value_by_reference(op):
   if types.is_numeric_operand(op):
      if types.is_integer_operand(op):
         return types.make_integer(op["value"])
      else:
         return types.make_float(op["value"])
   else:
      return types.make_string(op["value"])

def operand_real_value(op):

   if not op:
      return types.make_nil()

   if types.is_id_operand(op):
      
      if reg_exists(op):
         return unlik_value_by_reference(reg_value(op, None))

      handle_error("registre '%s' dont exists" % (op["value"]))
      return types.make_nil()

   elif types.is_array_pointer_operand(op):
      
      if reg_exists(op):

         try:
         
            r = unlik_value_by_reference(reg_value(op, None))

            if not types.is_array_operand(r):
               handle_fatal_error("'%s' is not an array" % (op["value"]))

            r = r["value"][op["index"]]
         
         except:
            
            handle_error("%s[%s] index out of range" % (op["value"], op["index"]))
            return types.make_nil()

         return r

      handle_error("registre '%s' dont exists" % (op["value"]))
      return types.make_nil()

   else:

      return unlik_value_by_reference(op)

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

      if debug:
         print ""
         raw_input(" ~ %s << %s" % (reg["value"], mode))

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
   lo = args["operands"][0]
   ro = args["operands"][1]
   return [lo, ro]

# ---------------------------

# ---------------------------
# Instruc set

def aritmetic_operations_instruc(args, operation):
   lo, ro = parse_instruct_args(args)

   if operation == "inc" or operation == "dec":
      expects_1_operands(lo, ro)
   else:
      expects_2_operands(lo, ro)

   if not types.is_id_operand(lo):
      handle_fatal_error("%s : left operand must be an identifier" % (operation))

   real_lo = operand_real_value(lo)

   if not types.is_numeric_operand(real_lo):
      handle_fatal_error("%s : only works with numeric operands" % (operation))

   if operation == "inc":
      real_lo["value"] += 1
   elif operation == "dec":
      real_lo["value"] -= 1
   else:

      ro = operand_real_value(ro)

      if not types.is_numeric_operand(ro):
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

   if not types.is_id_operand(lo):
      handle_fatal_error("var : left operand must be an identifier")

   ro = operand_real_value(ro)

   reg_value(lo, ro)

def call_instruc(args):
   lo, ro = parse_instruct_args(args)

   expects_1_operands(lo, ro)

   if not types.is_id_operand(lo):
      handle_fatal_error("var : left operand must be an identifier")

   execute_proc(lo["value"])

def mov_instruc(args):
   lo, ro = parse_instruct_args(args)

   expects_2_operands(lo, ro)

   if not types.is_id_operand(lo) and not types.is_array_pointer_operand(lo):
      handle_fatal_error("mov : left operand must be a registre")

   if not reg_exists(lo):
      handle_fatal_error("mov : left operand '%s' don't exists" % (lo["value"]))

   ro = operand_real_value(ro)

   if types.is_array_pointer_operand(lo):

      real_lo = reg_value(lo, None)
      real_lo["value"][lo["index"]] = ro
      reg_value(lo, real_lo)

   else:

      reg_value(lo, ro)

def push_instruc(args):
   lo, ro = parse_instruct_args(args)

   expects_2_operands(lo, ro)

   if not types.is_id_operand(lo):
      handle_fatal_error("push : left operand must be a registre")

   if not reg_exists(lo):
      handle_fatal_error("push : left operand '%s' don't exists" % (lo["value"]))

   real_lo = operand_real_value(lo)

   if not types.is_array_operand(real_lo):
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

   if types.is_string_operand(lo):


      lo["value"] = lo["value"].replace("\\n","\n")

      if ro != None:
         ro = operand_real_value(ro)
         lo["value"] = lo["value"].replace("\\$", str(ro["value"]))

   sys.stdout.write(str(lo["value"]))
   sys.stdout.flush()

def inp_instruc(args):
   lo, ro = parse_instruct_args(args)

   expects_2_operands(lo, ro)

   if not types.is_id_operand(lo) and not types.is_array_pointer_operand(lo):
      handle_fatal_error("inp : left operand must be a registre")

   if not reg_exists(lo):
      handle_fatal_error("inp : left operand '%s' don't exists" % (lo["value"]))

   input = raw_input(ro["value"])

   ro = types.make_string(input)

   if types.is_array_pointer_operand(lo):

      real_lo = reg_value(lo, None)
      real_lo["value"][lo["index"]] = ro
      reg_value(lo, real_lo)

   else:

      reg_value(lo, ro)

def cmp_instruc(args):
   global regs

   lo, ro = parse_instruct_args(args)

   expects_2_operands(lo, ro)

   lo = operand_real_value(lo)
   ro = operand_real_value(ro)

   if lo["value"] < ro["value"]:
      r = types.make_integer(0)

   elif lo["value"] == ro["value"]:
      r = types.make_integer(1)

   else:
      r = types.make_integer(2)

   regs["cmp_result"] = r

def jb_instruct(args):
   global regs

   lo, ro = parse_instruct_args(args)

   expects_1_operands(lo, ro)

   try:

      cmp_result = regs["cmp_result"]

   except:

      handle_error("jb : cmp instruct must be executed before")
      return

   if cmp_result["value"] == 0:
      execute_proc(lo["value"])

def je_instruct(args):
   global regs

   lo, ro = parse_instruct_args(args)

   expects_1_operands(lo, ro)

   try:

      cmp_result = regs["cmp_result"]

   except:

      handle_error("je : cmp instruct must be executed before")
      return

   if cmp_result["value"] == 1:
      execute_proc(lo["value"])

def ja_instruct(args):
   global regs

   lo, ro = parse_instruct_args(args)

   expects_1_operands(lo, ro)

   try:

      cmp_result = regs["cmp_result"]

   except:

      handle_error("ja : cmp instruct must be executed before")
      return

   if cmp_result["value"] == 2:
      execute_proc(lo["value"])

def jd_instruct(args):
   global regs

   lo, ro = parse_instruct_args(args)

   expects_1_operands(lo, ro)

   try:

      cmp_result = regs["cmp_result"]

   except:

      handle_error("jd : cmp instruct must be executed before")
      return

   if cmp_result["value"] != 1:
      execute_proc(lo["value"])

def jbe_instruct(args):
   global regs

   lo, ro = parse_instruct_args(args)

   expects_1_operands(lo, ro)

   try:

      cmp_result = regs["cmp_result"]

   except:

      handle_error("jbe : cmp instruct must be executed before")
      return

   if cmp_result["value"] == 0 or cmp_result["value"] == 1:
      execute_proc(lo["value"])

def jae_instruct(args):
   global regs

   lo, ro = parse_instruct_args(args)

   expects_1_operands(lo, ro)

   try:

      cmp_result = regs["cmp_result"]

   except:

      handle_error("jae : cmp instruct must be executed before")
      return

   if cmp_result["value"] == 2 or cmp_result["value"] == 1:
      execute_proc(lo["value"])

def type_instruc(args):
   lo, ro = parse_instruct_args(args)

   expects_2_operands(lo, ro)

   if not types.is_id_operand(lo) and not types.is_array_pointer_operand(lo):
      handle_fatal_error("type : left operand must be a registre")

   if not reg_exists(lo):
      handle_fatal_error("type : left operand '%s' don't exists" % (lo["value"]))

   type = ro["value"]
   real_lo = operand_real_value(lo)

   try:

      if type == "integer":

         new = types.make_integer(int(real_lo["value"]))

      elif type == "float":

         new = types.make_float(float(real_lo["value"]))

      elif type == "string":

         new = types.make_string(str(real_lo["value"]))

      elif type == "nil":

         new = types.make_nil()

      else:

         handle_fatal_error("type : Unknown type '%s'" % (type))
         return

   except:

      handle_fatal_error("type : Invalid value for '%s'" % (type))
      return

   reg_value(lo, new)


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
   , "cmp": cmp_instruc
   , "jb" : jb_instruct
   , "je" : je_instruct
   , "ja" : ja_instruct
   , "jd" : jd_instruct
   , "jbe": jbe_instruct
   , "jae": jae_instruct
   , "call": call_instruc
   , "push": push_instruc
   , "type": type_instruc
}

# ----------------------------
# Haders set

def debug_header(args):
   global debug

   lo, ro = parse_instruct_args(args)

   expects_1_operands(lo, ro)

   if not types.is_integer_operand(lo):
      handle_fatal_error("debug : first operand must be an integer")

   if lo["value"] == 1:
      debug = True
   else:
      debug = False

def start_header(args):
   global main_proc

   lo, ro = parse_instruct_args(args)

   expects_1_operands(lo, ro)

   if not types.is_id_operand(lo):
      handle_fatal_error("start : first operand must be an identifier")

   main_proc = lo["value"]

header_set = {
     "debug": debug_header
   , "start": start_header
}

# ----------------------------

lineno = 0
debug  = False
main_proc = "main"
prog_tree = None
regs = {
     "ax": types.make_nil()
   , "bx": types.make_nil()
   , "cx": types.make_nil()
   , "dx": types.make_nil()
}

def handle_error(error):
   global lineno

   print "Error: %s, on line %s" % (error, lineno)

def handle_fatal_error(error):
   global lineno

   print "Fatal: %s, on line %s" % (error, lineno)
   sys.exit()

def execute_header(header):
   global lineno

   lineno = header["lineno"]

   try:

      header_handle = header_set[header["name"]]

   except:

      handle_fatal_error("Unknown header '%s'" % (header["name"]))

   header_handle(header)

def execute_instruc(instruc):
   global lineno

   lineno = instruc["lineno"]

   if debug:

      print ""
      print " ~ Registres"
      print ""

      for reg in regs:
         print "   %s : %s" % (reg, regs[reg])

      print ""
      print " ~ Instruc %s at line %s" % (instruc["name"], lineno)
      print ""
      print "   - l operand: %s" % instruc["operands"][0]
      raw_input("   - r operand: %s" % instruc["operands"][1])

   try:

      instruc_caller = instruc_set[instruc["name"]]

   except:

      handle_fatal_error("Unknown instruction '%s'" % (instruc["name"]))

   instruc_caller(instruc)

def execute_proc(proc):
   global prog_tree
   
   if debug:

      print ""
      raw_input(" ~ Executing procedure %s " % proc)

   try:

      proc = prog_tree["procs"][proc]

   except:

      handle_fatal_error("Undefined procedure '%s'" % (proc))   

   for instruc in proc:

      execute_instruc(instruc)

def execute_prog(pt):
   global prog_tree
   global main_proc

   prog_tree = pt

   for header in prog_tree["headers"]:
      execute_header(header)

   execute_proc(main_proc)