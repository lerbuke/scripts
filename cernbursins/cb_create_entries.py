#!/usr/bin/env python
"""
cb_create_entries.py
Read a text file to create corresponding entries in a server database.
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
    #    print(item)
    #exit();

    # Open the server0.db database
    conn = sqlite3.connect(args.db_path + 'server0.db')
    cur = conn.cursor()

    cur.execute('DELETE FROM local')
    cur.execute('DROP TABLE IF EXISTS provider_0_0')
    cur.execute("""CREATE TABLE "provider_0_0" (
        "id" INTEGER NOT NULL,
        "tag" TEXT,
        "desc" TEXT,
        "desc2" TEXT,
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
        "field2" TEXT,
        "texpro" integer,
        PRIMARY KEY ("id"));""")
    conn.commit()
    jour_mois = 1
    heure_min = 1
    compteur = 1
    for item in list:
        if len(item) >= 3:
            addr_numbers = re.findall(r'[0-9]+', item[1]) # build a list of number found item[1]
            if 'BOOL' == item[2]:
                # ['TelerelaisEclairagePubliqueModeNuit', 'AT %MX4.0', BOOL'] or ['TS00_AllumageGeneral', 'AT %MX10.0', 'BOOL', '0', '1']
                alarm = 1 if (len(item) < 4) else item[3]
                invert = 0 if (len(item) < 5) else item[4]
                if int(addr_numbers[0]) % 2 == 0:
                    address = 12288 + int(int(addr_numbers[0]) / 2)
                    cur.execute("INSERT INTO provider_0_0 (tag,variant,attribute,field0,field1,field2,alarm,invert) VALUES('{}',2,0,2,'{}','{}','{}','{}')".format(item[0], address, int(addr_numbers[1])+1, alarm, invert))
                else:
                    address = 12288 + int((int(addr_numbers[0])-1) / 2)
                    cur.execute("INSERT INTO provider_0_0 (tag,variant,attribute,field0,field1,field2,alarm,invert) VALUES('{}',2,0,2,'{}','{}','{}','{}')".format(item[0], address, int(addr_numbers[1])+8+1, alarm, invert))

            elif 'BYTE' == item[2]:
                # ['TS04_Statuts', 'AT %MB400', 'BYTE', '(* Pointeur pour la comm ADS *)']
                pass

            elif 'INT' == item[2]:
                # ['DureeTestEclairageSecours', 'AT %MW20', 'INT']
                address = 12288 + int(int(addr_numbers[0]) / 2)
                cur.execute("INSERT INTO provider_0_0 (tag,variant,attribute,field0,field1) VALUES('{}',1,0,2,'{}')".format(item[0], address))
                pass

            elif 'DINT' == item[2]:
                # ['TS02_Compteur1', 'AT %MB210', 'DINT']
                address = 12288 + int(int(addr_numbers[0]) / 2)
                cur.execute("INSERT INTO provider_0_0 (tag,variant,attribute,field0,field1,renv0,renv1,renv2) VALUES('{}_LSB',1,0,2,'{}',3,1,{})".format(item[0], address, compteur))
                cur.execute("INSERT INTO provider_0_0 (tag,variant,attribute,field0,field1,renv0,renv1,renv2) VALUES('{}_MSB',1,0,2,'{}',3,2,{})".format(item[0], address+1, compteur))
                cur.execute("INSERT INTO local (tag,variant,renv0,renv1,renv2) VALUES('{}',1,3,3,{})".format(item[0], compteur))
                compteur = compteur + 1
                pass

            elif 'WORD' == item[2]:
                # ['PulseComptageTener', 'AT%MB1000', 'WORD']
                pass

            elif 'DT' == item[2]:
                # ['DateEtHeure', 'AT %MD0', 'DT']
                pass

            elif 'JourMois' == item[2]:
                # ['Ferie02', 'AT %MW802', 'JourMois']
                address = 12288 + int(int(addr_numbers[0]) / 2)
                cur.execute("INSERT INTO provider_0_0 (tag,variant,attribute,field0,field1,renv0,renv1,renv2) VALUES('{}',1,0,2,'{}',1,1,{})".format(item[0], address, jour_mois))
                cur.execute("INSERT INTO local (tag,variant,renv0,renv1,renv2) VALUES('{}_Jour',1,1,2,{})".format(item[0], jour_mois))
                cur.execute("INSERT INTO local (tag,variant,renv0,renv1,renv2) VALUES('{}_Mois',1,1,3,{})".format(item[0], jour_mois))
                jour_mois = jour_mois + 1
                pass

            elif 'HeureMinute' == item[2]:
                # ['HeurePortesProg1EteOff1', 'AT %MW1500', 'HeureMinute', '(* Programme du matin du lundi au jeudi *)']
                address = 12288 + int(int(addr_numbers[0]) / 2)
                cur.execute("INSERT INTO provider_0_0 (tag,variant,attribute,field0,field1,renv0,renv1,renv2) VALUES('{}',1,0,2,'{}',2,1,{})".format(item[0], address, heure_min))
                cur.execute("INSERT INTO local (tag,variant,renv0,renv1,renv2) VALUES('{}_Heure',1,2,2,{})".format(item[0], heure_min))
                cur.execute("INSERT INTO local (tag,variant,renv0,renv1,renv2) VALUES('{}_Min',1,2,3,{})".format(item[0], heure_min))
                heure_min = heure_min + 1

            else:
                #print('Unknown type: ', item[2])
                pass

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
os.system("pause")