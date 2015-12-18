import sys
from core.sintax import parse_code

try:

   source_file = sys.argv[1]

except:

   print "Indica el archivo con el codigo fuente"
   sys.exit()

file_obj = open(source_file)

source = file_obj.read()

file_obj.close()

program = parse_code(source + "\n")

for defi in program["defs"]:
   print defi

for proc in program["procs"]:
   print "\n - %s" % (proc["name"])

   for instruct in proc["instructions"]:
      print instruct