#!/usr/bin/env python
"""
cb_create_entries.py
Read a text file to create corresponding entries in database.
"""
import argparse, os, sys
import sqlite3, re

parser = argparse.ArgumentParser(description='Création des données dans la base server0.db du projet cern bursins.')
parser.add_argument('-fn', '--file_name', default='_mapping beckhoff.txt', help='Nom du fichier de mapping')
parser.add_argument('-dbp', '--db_path', default='./server_db/', help='Chemin de la base de données server0.db')

args = parser.parse_args()
print(args)

try:
    list = []
    # Open the file and create list
    fw = open(args.file_name, "r")
    fw.readline()
    for line in fw:
        value = line.rstrip().replace(': ', '').replace(';', '').split('\t')
        if value[0] != '' and value[0] != '(*':
            list.append(value)
    fw.close()
    
    #for item in list:
     #   print(item)
    
 
    
    # Open the server0.db database
    conn = sqlite3.connect(args.db_path + 'server0.db')
    cur = conn.cursor()
 
    cur.execute('DROP TABLE IF EXISTS provider_0_0')
    cur.execute("""CREATE TABLE "provider_0_0" (
        "id" INTEGER NOT NULL,
        "tag" TEXT,
        "desc" TEXT,
        "variant" INTEGER,
        "attribute" INTEGER,
        "alarm" INTEGER,
        "prio" INTEGER,
        "alarm_txt" INTEGER,
        "invert" INTEGER,
        "renv0" INTEGER,
        "renv1" INTEGER,
        "renv2" INTEGER,
        "renv3" INTEGER,
        "renv4" INTEGER,
        "immediate" INTEGER,
        "store" INTEGER,
        "scale" REAL,
        "factor" REAL,
        "field0" TEXT,
        "field1" TEXT,
        "texpro" integer,
        PRIMARY KEY ("id"));""")
    conn.commit()
    
    for item in list:    
        if len(item) >= 3:
            desc = ''
            addr_numbers = re.findall(r'[0-9]+', item[1]) # build a list of number found item[1]
            if len(addr_numbers) == 2:
                if 'BOOL' == item[2]:
                    # ['TelerelaisEclairagePubliqueModeNuit', 'AT %MX4.0', BOOL']                
                    address = 12288 + 8 * int(addr_numbers[0]) + int(addr_numbers[1])
                    cur.execute("INSERT INTO provider_0_0 (tag,desc,variant,attribute,alarm,field0,field1,texpro) VALUES('{}','{}',2,0,0,0,'{}',0)".format(item[0], desc, address))
                    
                elif 'BYTE' == item[2]:  
                    # ['TS04_Statuts', 'AT %MB400', 'BYTE', '(* Pointeur pour la comm ADS *)']
                    if len(item) == 4:
                        desc=item[3]
                    
                elif 'INT' == item[2]:
                    # ['DureeTestEclairageSecours', 'AT %MW20', 'INT']
                    pass
                    
                elif 'DINT' == item[2]:
                    # ['TS02_Compteur1', 'AT %MB210', 'DINT']
                    pass
                    
                elif 'WORD' == item[2]:
                    # ['PulseComptageTener', 'AT%MB1000', 'WORD']
                    pass
                    
                elif 'DT' == item[2]:
                    # ['DateEtHeure', 'AT %MD0', 'DT']
                    pass
                    
                elif 'JourMois' == item[2]:
                    # ['Ferie02', 'AT %MW802', 'JourMois']
                    pass
                    
                elif 'HeureMinute' == item[2]:
                    # ['HeurePortesProg1EteOff1', 'AT %MW1500', 'HeureMinute', '(* Programme du mation du lundi au jeudi *)']
                    if len(item) == 4:
                        desc=item[3]
                    
                else:
                    print('Unknown type: ', item[2])
                
    conn.commit()
    conn.close()
    
except IOError as e:
   print("I/O error({0}): {1}".format(e.errno, e.strerror))
   print(traceback.format_exc())
   os.system("pause")
   exit()
except sqlite3.Error as er:
   print(sqlite3_errmsg(conn))
   print(traceback.format_exc())
   os.system("pause")
   exit()
except: #handle other exceptions such as attribute errors
   print("Unexpected error:", sys.exc_info()[0])
   print(traceback.format_exc())
   os.system("pause")
   exit()
   
print("Done.")