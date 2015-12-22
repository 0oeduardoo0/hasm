import sys

from core.compiler import parse_code
from vm import vm

try:

   source_file = sys.argv[1]

except:

   print "High Assembler (HASM) 0.1"
   print "Coded By Eduardo B <ms7rbeta@gmail.com>"

   sys.exit()

file_obj = open(source_file)
source   = file_obj.read()

file_obj.close()

program_tree = parse_code(source)
vm.execute_prog(program_tree)