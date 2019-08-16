#!/usr/bin/env python
"""
vtv_create_entries.py
Read the csv file and create corresponding entries in database
"""
import argparse, os, sys
import sqlite3

parser = argparse.ArgumentParser(description='Création des données dans la base vtv.')
parser.add_argument('-fn', '--file_name', default='vtv_instances.csv', help='Nom du fichier csv')

args = parser.parse_args()
print(args)


try:
    fw = open(args.file_name, "r")
    conn = sqlite3.connect('db\server0.db')

   
    cur = conn.cursor()
    # Delete all MODBUS (0) and SNMP (3) providers, provider configurations and replies
    for provider in (0,3):
        cur.execute("SELECT providerNbSubId FROM provider WHERE providerType={}".format(provider))
        nb = cur.fetchone()[0]

        range = (0, nb-1)
        for i in range: 
            suffix = "_" + str(provider) + "_" + str(i)
            cur.execute('DROP TABLE IF EXISTS provider' + suffix)
            cur.execute('DROP TABLE IF EXISTS provider_config' + suffix)
            cur.execute('DROP TABLE IF EXISTS provider_reply' + suffix)
        print(cur.fetchone())
       
    CAMERA = 'cad'
    AUTOMATE = 'aut'
    cameras = []
    automates = []   
    for line in fw:
        value = line.rstrip().split(';')[1]
        if CAMERA in line:
            cameras.append(value)
        if AUTOMATE in line:
            automates.append(value)
    fw.close()


    cur.execute("UPDATE provider SET providerNbSubId = {} WHERE providerType = 0".format(len(automates)))
    cur.execute("UPDATE provider SET providerNbSubId = {} WHERE providerType = 3".format(len(cameras)))

    k = 0
    sys.stdout.write('Creating camera entries...')
    for cam in cameras:
        cur.execute("""CREATE TABLE 'provider_3_{}' (
            'id' INTEGER NOT NULL,
            'tag' TEXT,
            'desc' TEXT,
            'variant' INTEGER,
            'attribute' INTEGER,
            'alarm' INTEGER,
            'prio' INTEGER,
            'alarm_txt' INTEGER,
            'invert' INTEGER,
            'renv0' INTEGER,
            'renv1' INTEGER,
            'renv2' INTEGER,
            'renv3' INTEGER,
            'renv4' INTEGER,
            'immediate' INTEGER,
            'store' INTEGER,
            'scale' REAL,
            'factor' REAL,
            'texpro' integer,
            'field0' TEXT,
            'field1' TEXT,
            PRIMARY KEY ('id')
            );""".format(k))
        
            
        cur.execute("""CREATE TABLE "provider_config_3_{}" (
            "id" INTEGER NOT NULL,
            "name" TEXT,
            "field0" TEXT,
            "field1" TEXT,
            "field2" TEXT,
            "field3" TEXT,
            PRIMARY KEY ("id")
            );""".format(k))       
            
        cur.execute("""CREATE TABLE "provider_reply_3_{}" (
            "id" INTEGER NOT NULL,
            "tag" TEXT,
            "desc" TEXT,
            "variant" INTEGER,
            "alarm" INTEGER,
            "prio" INTEGER,
            "alarm_txt" INTEGER,
            "renv0" INTEGER,
            "renv1" INTEGER,
            "renv2" INTEGER,
            "renv3" INTEGER,
            "renv4" INTEGER,
            "store" INTEGER,
            "texpro" integer,
            PRIMARY KEY ("id")
            );""".format(k))
            
        conn.commit()
        
        cur.execute("INSERT INTO provider_3_{} (tag,variant,attribute,alarm,field0,field1) VALUES('cad_{}_com',2,1,1,'1.3.6.1.2.1.2.2.1.8.1',1)".format(k, cam))
        cur.execute("INSERT INTO provider_config_3_{} (name,field3) VALUES('cad_{}', 5000)".format(k, cam))
        cur.execute("INSERT INTO provider_reply_3_{} (tag,desc,variant,alarm,prio,renv0,renv1,renv2,texpro) VALUES('cad_{}_dsc','Défaut com. caméra',2,1,1,1,1,{},1)".format(k, cam, 101+k))
                    
        k+=1
        sys.stdout.write('.')
    print('Done.')
    
    k = 0
    for aut in automates:
        cur.execute("""CREATE TABLE "provider_0_{}" (
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
            PRIMARY KEY ("id")
            );""".format(k))
        
        cur.execute("""CREATE TABLE "provider_config_0_{}" (
            "id" INTEGER NOT NULL,
            "name" TEXT,
            "field0" TEXT,
            "field1" TEXT,
            "field2" TEXT,
            "field3" TEXT,
            "field4" TEXT,
            "field5" TEXT,
            PRIMARY KEY ("id")
            );""".format(k))
        
        cur.execute("""CREATE TABLE "provider_reply_0_{}" (
            "id" INTEGER NOT NULL,
            "tag" TEXT,
            "desc" TEXT,
            "variant" INTEGER,
            "alarm" INTEGER,
            "prio" INTEGER,
            "alarm_txt" INTEGER,
            "renv0" INTEGER,
            "renv1" INTEGER,
            "renv2" INTEGER,
            "renv3" INTEGER,
            "renv4" INTEGER,
            "store" INTEGER,
            "texpro" integer,
            PRIMARY KEY ("id")
            );""".format(k))
            
        conn.commit()
        
        cur.execute("INSERT INTO provider_0_{} (tag,desc,variant,attribute,alarm,invert,field0,field1,texpro) VALUES('dis_{}_sti','Défaut disjoncteur',2,1,1,1,1,0,1)".format(k,aut))
        conn.commit()
        cur.execute("INSERT INTO provider_0_{} (tag,desc,variant,attribute,renv4,field0,field1) VALUES('pha_{}_cdi','Commande dallumage du phare infrarouge',2,0,{},0,0)".format(k,aut,k+1))
        conn.commit()
        cur.execute("INSERT INTO provider_0_{} (tag,desc,variant,attribute,alarm,field0,field1,texpro) VALUES('pha_{}_sti','Etat Phare IR',2,1,1,0,0,1)".format(k,aut))
        conn.commit()
        cur.execute("INSERT INTO provider_config_0_{} (name,field1,field2,field3) VALUES('aut_{}',502,500,1)".format(k,aut))
        cur.execute("INSERT INTO provider_reply_0_{} (tag,desc,variant,alarm,renv0,renv1,renv2,texpro) VALUES('aut_{}_dsc','Défaut com. Automate',2,1,1,1,{},1)".format(k,aut,k+1))
    
        k+=1
        sys.stdout.write('.')
    print('Done.')
    
    #for cam in cameras:    
    print(len(cameras))
    print(cameras)
    print(automates)
    conn.commit()
    conn.close()
except IOError as e:
   print("I/O error({0}): {1}".format(e.errno, e.strerror))
   exit()
except: #handle other exceptions such as attribute errors
   print("Unexpected error:", sys.exc_info()[0])
   exit()
   