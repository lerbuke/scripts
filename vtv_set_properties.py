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
parser.add_argument('-fn', '--file_name', default='vtv_instances.csv', help='Nom du fichier csv')
parser.add_argument('-svg', '--svg_fn', help='Chemin du fichier svg à modifier')

args = parser.parse_args()
print(args)


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
    keys = ['URL=', 'TOOLTIP=', 'n=pha_', 'n=olm_']
    
    with open (args.file_name,"r") as cam_file:  
        for line in cam_file:
            value = line.rstrip().split(';')[1:6]
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
    
    with open (args.svg_fn, "r") as input_file:
        with open ("_"+args.svg_fn, "w", newline='\n') as output_file:
            for line in input_file:
                # Skip writing URL= or TOOLTIP= tags with their value
                if ('URL=' not in line) and ('TOOLTIP=' not in line) and ('n=pha_' not in line) and ('n=olm_' not in line) and ('n=aut_' not in line) and ('n=tbt_' not in line):
                    output_file.write(line)
                else:
                    if 'URL=' in line:
                        output_file.write(re.sub(r'URL=.[^<]*', '', line))
                    elif 'TOOLTIP=' in line:
                        output_file.write(re.sub(r'TOOLTIP=.[^<]*', '', line))                                       
                                                
                # Automate                   
                sb = re.search(r'n=aut_.[^< ]*', line)
                if sb != None:
                    id = sb.group()[6:]
                    for aut in automates:
                        if id in aut[0]:
                            tooltip = aut[3]
                            index = sb.span()[1]
                            output_file.write(line[:index:] + '\nTOOLTIP=' + tooltip.replace('"','') + line[index:] +'\n')              
                            break                 
                            
                # Camera                    
                sb = re.search(r'MSVGTAG=cad_\d+_dsc', line)
                if sb != None:
                    id = re.search(r'\d+', sb.group()).group()
                    for cam in cameras:
                        if id in cam[0]:
                            ip_addr = cam[2]
                            output_file.write('URL=http://'+ip_addr+'/stw-cgi/video.cgi?msubmenu=stream&amp;action=view&amp;Profile=1&amp;CodecType=MJPEG&amp;Resolution=800x600&amp;FrameRate=10&amp;CompressionLevel=10\n')
                            tooltip = cam[3]
                            output_file.write('\nTOOLTIP=' + tooltip + '\n')
                            break                                           
                    
                # Disjoncteur                   
                sb = re.search(r'n=tbt_.[^< ]*', line)
                if sb != None:
                    id = sb.group()[6:]
                    for dis in disjoncteurs:
                        if id in dis[0]:
                            tooltip = dis[3]
                            index = sb.span()[1]
                            output_file.write(line[:index:] + '\nTOOLTIP=' + tooltip.replace('"','') + line[index:] +'\n')              
                            break          
                            
                # Phare                  
                sb = re.search(r'n=pha_.[^< ]*', line)
                if sb != None:
                    id = sb.group()[6:]
                    for pha in phares:
                        if id in pha[0]:
                            tooltip = pha[3]
                            index = sb.span()[1]
                            output_file.write(line[:index:] + '\nTOOLTIP=' + tooltip.replace('"','') + line[index:] +'\n')              
                            break 
                
                # Switch                   
                sb = re.search(r'n=olm_.[^< ]*', line)
                if sb != None:
                    id = sb.group()[6:]
                    for swi in switches:
                        if id in swi[0]:
                            tooltip = swi[3]
                            index = sb.span()[1]
                            output_file.write(line[:index:] + '\nTOOLTIP=' + tooltip.replace('"','') + line[index:] +'\n')              
                            break                 
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