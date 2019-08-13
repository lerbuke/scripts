#!/usr/bin/env python3
"""
Read for a complete API: https://dabuttonfactory.com/fr/api
"""
import certifi
import urllib3
import urllib3.request
import sys
import argparse
import json
import re
from collections import defaultdict

parser = argparse.ArgumentParser(description='Génération de bouton pour supervision.')
parser.add_argument('-if', '--infile', default='default.json', help='Nom du bouton')
parser.add_argument('-fne', '--file_name_extension', default="gif", help='Nom de l''extension du fichier')
parser.add_argument('-bw', '--button_width', default=200, help='Largeur en pixels du button')
parser.add_argument('-bh', '--button_height', default=34, help='Hauteur en pixels du button')
args = parser.parse_args()
print(args)
     

def CONSTANT_DEFAULT_PARAMS():
    DEFAULT_PARAMS = {
    't' : 'TOTO', # Texte
    'f' : 'Calibri', # Police d'écriture (Calibri)
    'tc' : 'fff', # Couleur du texte (#000)
    'ts' : 20, # Taille du texte (12)
    'tshs' : 0, # Distance entre le texte et son ombre (0)
    'tshc' : '777', # Couleur de l'ombre du texte (#777)
    'c' : 0, # Arrondi des coins ou côtés (0)
    'bgt' : 'unicolored', # Type d'arrière-plan (unicolored) 
    'bgc' : '#3d85c6', # Couleur d'arrière-plan selon le type 'bgt' (#00f)
    'ebgc' : '0ff', # Couleur d'arrière-plan selon le type 'bgt' (#0ff)
    'bs' : 0, # Taille de la bordure (0)
    'bc' : '888', # Couleur de la bordure (#888)
    'shs' : 0, # Taille de l’ombre du bouton (0)    
    'shc' : '666', # Couleur de l’ombre du bouton (#666)    
    'sho' : 'se', # Orientation de l’ombre du bouton (se)    
    'be' : 0, # «Effet bulle» ; reflet de forme elliptique sur la moitié supérieure du bouton (0)        
    'hp' : 12, # Marge entre le texte et les extrémités gauche et droite du bouton (12)    
    'vp' : 10, # Marge entre le texte et les extrémités haut et bas du bouton (10)   
    'w' : args.button_width, # Largeur (taille horizontale) du bouton {none)   
    'h' : args.button_height # Hauteur (taille verticale) du bouton (none)
    }  
    return DEFAULT_PARAMS
    
URL = "https://DaButtonFactory.com/button." + args.file_name_extension + "?"


# Create a button image file
def create_button(http, filename, params):
    try:
        r = http.request('GET', URL + params)
        if 200 == r.status:
            with open(filename, "wb") as file:                
                file.write(r.data)
        else:
            print("Failed to create {} file. Status code: {} ".format(filename, r.status))
        
    except: #handle other exceptions such as attribute errors
       print("Unexpected error: {}".format(sys.exc_info()[0]))
       exit()
       
def main():    
    http = urllib3.PoolManager(cert_reqs='CERT_REQUIRED',ca_certs=certifi.where())           
    data = json.loads(open(args.infile, encoding='utf-8').read())
    
    for key, settings in data.items():
        # key: filename without extension, settings: settings dict.
        params = CONSTANT_DEFAULT_PARAMS()
        fn = key + "." + args.file_name_extension    
        print("\nCreating {}...".format(fn))
        
        for kk, dv in settings.items():
            if kk in params.keys():                
                params[kk] = data[key][kk]
                if None == params[kk]:                    
                    del params[kk]
                    print("Removed {}".format(kk))
                else:
                    print("{}={}".format(kk, params[kk]))
            
        create_button(http, fn, urllib3.request.urlencode(params))

if __name__ == '__main__':
    main()
