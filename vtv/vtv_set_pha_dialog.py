#!/usr/bin/env python
"""
vtv_set_pha_dialog.py

pha: phare

"""
import argparse, os, sys
import re

parser = argparse.ArgumentParser(description='Ajout des propriétés DIALOG et DIALOGTAG aux objects "phares" du fichier SVG du projet VTV.')
parser.add_argument('-svg', '--svg_fn', help='Chemin du fichier svg à modifier')

args = parser.parse_args()
print(args)


try:
    with open (args.svg_fn, "r") as input_file:
        with open ("_"+args.svg_fn, "w", newline='\n') as output_file:
            for line in input_file:
                # Skip writing URL= or TOOLTIP= tags with their value
                if ('n=pha_' not in line):
                    output_file.write(line)
                sb = re.search(r'n=pha_.[^< ]*', line.rstrip())
                if sb != None:
                    key = sb.group()[2:]
                    output_file.write(line + 'DIALOG=3\nDIALOGTAG=' + key + '_cdi\n')
                    
                
    os.remove(args.svg_fn)
    os.rename("_"+args.svg_fn, args.svg_fn)

except IOError as e:
   print("I/O error({0}) exception: {1}".format(e.errno, e.strerror))
   print(traceback.format_exc())
   os.system("pause")
   exit()
except AttributeError as e:
   print("Attribute error exception:", sys.exc_info()[0])
   print(traceback.format_exc())
   os.system("pause")
   exit()
except: #handle other exceptions such as attribute errors
   print("Unexpected error exception:", sys.exc_info()[0])
   print(traceback.format_exc())
   os.system("pause")
   exit()

os.system("pause")