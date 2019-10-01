#!/usr/bin/env python
"""
vtv_set_properties.py
Remove all existing URL and TOOLTIP properties in the svg file.
Add URL and TOOLTIP read from the cvs file.
aut: automate
cad: camera
pha: phare
tbt: disjoncteur
gns: gestionnaire niveau supervision
sct: scénarios CT
"""
import argparse, os, sys
import re

parser = argparse.ArgumentParser(description='Ajout de la propriété URL aux objets camera du fichier SVG Cameras du projet VTV.')
parser.add_argument('-fn', '--file_name', default='vtv_instances.txt', help='Nom du fichier texte')
parser.add_argument('-svg', '--svg_fn', help='Chemin du fichier svg à modifier')

args = parser.parse_args()
print(args)


def work(o, list, line):
    if len(o) != 3:
        raise NameError('Length of \'' + o + '\' must equals 3.')

    sb = re.search(r'n=ble' + o + '_.[^< ]*', line.rstrip()) # i.e. 'n=blepha_65' or 
    if sb != None:
        id = sb.group()[9:]
        for item in list:
            if id == item[0]:
                tooltip = item[3]
                index = sb.span()[1]      
                print (sb, id, line[:index] + '\nTOOLTIP=' + tooltip + line[index:])
                output_file.write(line[:index] + '\nTOOLTIP=' + tooltip + line[index:])
                break
     
try:
    # Open the cvs file and extract needed info into lists
    # Each item of the list if composed by a list of
    #  id, ?, ip address, tooltip,
    AUTOMATE = 'aut'
    CAMERA = 'cad'
    DISJONCTEUR = 'tbt'
    PHARE = 'pha'
    SWITCH = 'olm'

    automates = []
    cameras = []
    disjoncteurs = []
    phares = []
    switches = []

    with open (args.file_name,"r") as cam_file:
        for line in cam_file:
            value = line.rstrip().split('\t')[1:6]
            if AUTOMATE in line:
                automates.append(value)
            if CAMERA in line:
                cameras.append(value)
            if DISJONCTEUR in line:
                disjoncteurs.append(value)
            if PHARE in line:
                phares.append(value)
            if SWITCH in line:
                switches.append(value)
                
    print(phares)                    

    with open (args.svg_fn, "r") as input_file:
        with open ("_"+args.svg_fn, "w", newline='\n') as output_file:
            for line in input_file:
                # Skip writing URL= or TOOLTIP= tags with their value
                if ('URL=' not in line) and ('TOOLTIP=' not in line) and ('n=ble'+PHARE+'_' not in line) and ('n=ble'+SWITCH+'_' not in line) and ('n=ble'+AUTOMATE+'_' not in line) and ('n=ble'+DISJONCTEUR+'_' not in line):
                    output_file.write(line)
                else:
                    if 'URL=' in line:
                        output_file.write(re.sub(r'URL=.[^<]*', '', line))
                    elif 'TOOLTIP=' in line:
                        output_file.write(re.sub(r'TOOLTIP=.[^<]*', '', line))

                # Automate
                work(AUTOMATE, automates, line)

                # Camera
                sb = re.search(r'MSVGTAG=ble'+AUTOMATE+'_\d+_dsc', line)
                if sb != None:
                    id = re.search(r'\d+', sb.group()).group()
                    for cam in cameras:
                        if id in cam[0]:
                            ip_addr = cam[2]
                            output_file.write('URL=http://'+ip_addr+'/stw-cgi/video.cgi?msubmenu=stream&amp;action=view&amp;Profile=1&amp;CodecType=MJPEG&amp;Resolution=800x600&amp;FrameRate=10&amp;CompressionLevel=10\n')
                            tooltip = cam[3]
                            output_file.write('TOOLTIP=' + tooltip + '\n')
                            break

                # Disjoncteur
                work(DISJONCTEUR, disjoncteurs, line)

                # Phare
                work(PHARE, phares, line)
               
                # Switch
                work(SWITCH, switches, line)
                
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
