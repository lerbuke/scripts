#!/usr/bin/env python
"""
vtv_create_entries.py
Read a csv file to create corresponding entries in database.
auto: automate
cad: camera
pha: phare
dis: disjoncteur
gns: gestionnaire niveau supervision
sct: scénarios CT
"""
import argparse, os, sys
import sqlite3

parser = argparse.ArgumentParser(description='Création des données dans la base server0.db du projet VTV.')
parser.add_argument('-fn', '--file_name', default='vtv_instances.csv', help='Nom du fichier csv')
parser.add_argument('-dbp', '--db_path', default='./server_db/', help='Chemin de la base de données server0.db')

args = parser.parse_args()
print(args)

try:
    # Open the file and create automate and camera lists
    fw = open(args.file_name, "r")
    CAMERA = 'cad'
    AUTOMATE = 'aut'
    SUPERVISION = 'gns'
    SCENARIO = 'sct'
    SWITCH = 'swi'

    cameras = []
    automates = []
    supervisions = []
    scenarios = []
    switchs = []

    for line in fw:
        value = line.rstrip().split(';')[1:4]
        if CAMERA in line:
            cameras.append(value)
        if AUTOMATE in line:
            automates.append(value)
        if SUPERVISION in line:
            supervisions.append(value)
        if SCENARIO in line:
            scenarios.append(value)
        if SWITCH in line:
            switchs.append(value)

    fw.close()
    #print(automates)
    #print(cameras)
    #print(supervisions)
    #print(scenarios)
    #print(switchs)

    # Open the server0.db database
    conn = sqlite3.connect(args.db_path + 'server0.db')
    cur = conn.cursor()

    # Delete all MODBUS (0) and SNMP (3) providers, provider configurations and replies
    for provider in (0,3):
        cur.execute("SELECT providerNbSubId FROM provider WHERE providerType={}".format(provider))
        nb = cur.fetchone()[0]
        for i in range(0,nb):
            suffix = "_" + str(provider) + "_" + str(i)
            cur.execute('DROP TABLE IF EXISTS provider' + suffix)
            cur.execute('DROP TABLE IF EXISTS provider_config' + suffix)
            cur.execute('DROP TABLE IF EXISTS provider_reply' + suffix)

    # Recreate local table
    cur.execute("DROP TABLE IF EXISTS local")
    cur.execute("""CREATE TABLE local (
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
        );""")

    cur.execute("DROP TABLE IF EXISTS provider_4_0")
    cur.execute("""CREATE TABLE provider_4_0 (
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
          "texpro" integer,
          PRIMARY KEY ("id")
        );""")

    # Update the number of automates and cameras
    cur.execute("UPDATE provider SET providerNbSubId = {} WHERE providerType = 0".format(len(automates)))
    cur.execute("UPDATE provider SET providerNbSubId = {} WHERE providerType = 3".format(len(cameras)+len(switchs)))
    cur.execute("UPDATE provider SET providerNbSubId = 1 WHERE providerType = 4")
    conn.commit()


    sys.stdout.write('Creating {} supervision entries...'.format(len(supervisions)))
    for sup in supervisions:
        # Local
        cur.execute("INSERT INTO local (tag,desc,variant,alarm,texpro) VALUES('gns_{}_dam','Défaut matériel sur l''automate du CT',2,1,2)".format(sup[0]))
        cur.execute("INSERT INTO local (tag,desc,variant,alarm,texpro) VALUES('gns_{}_dsm','Défaut matériel sur l''automate du CT',2,1,1)".format(sup[0]))
        cur.execute("INSERT INTO local (tag,desc,variant,texpro) VALUES('gns_{}_stm','Mode d''exploitation',1,1)".format(sup[0]))
        cur.execute("INSERT INTO local (tag,desc,variant,renv0,renv1,texpro) VALUES('gns_{}_tad','Mode distant',2,255,1,2)".format(sup[0]))
        cur.execute("INSERT INTO local (tag,desc,variant,alarm,renv0,renv1,texpro) VALUES('gns_{}_tae','Mode entretien',2,1,255,3,2)".format(sup[0]))
        cur.execute("INSERT INTO local (tag,desc,variant,alarm,renv0,renv1,texpro) VALUES('gns_{}_tal','Mode local',2,1,255,2,2)".format(sup[0]))
        cur.execute("INSERT INTO local (tag,desc,variant,alarm,renv0,renv1) VALUES('gns_{}_tex','Communication avec Texpro HS',2,1,255,4)".format(sup[0]))
        sys.stdout.write('.')
    print('Done.')

    sys.stdout.write('Creating {} scenarios entries...'.format(len(scenarios)))
    for sct in scenarios:
        # Local
        cur.execute("INSERT INTO local (tag,desc,variant,renv0,renv1,renv2) VALUES('sct_{}_cda','Commande d''activation',1,2,1,{})".format(sct[0],sct[1]))
        cur.execute("INSERT INTO local (tag,desc,variant,renv0,renv1,renv2,texpro) VALUES('sct_{}_ope','Etat opérationnel',1,2,3,{},1)".format(sct[0],sct[1]))
        cur.execute("INSERT INTO local (tag,desc,variant,renv0,renv1,renv2,texpro) VALUES('sct_{}_sta','Etat d''activation',1,2,2,{},1)".format(sct[0],sct[1]))
        sys.stdout.write('.')
    print('Done.')

    k = 0
    sys.stdout.write('Creating {} automate entries...'.format(len(automates)))
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

        cur.execute("INSERT INTO provider_0_{} (tag,desc,variant,attribute,alarm,invert,field0,field1,texpro) VALUES('dis_{}_sti','Défaut disjoncteur',2,1,1,1,1,0,1)".format(k,aut[0]))
        conn.commit()
        cur.execute("INSERT INTO provider_0_{} (tag,desc,variant,attribute,renv4,field0,field1) VALUES('pha_{}_cdi','Commande d''allumage du phare infrarouge',2,0,{},0,0)".format(k,aut[0],aut[1]))
        conn.commit()
        cur.execute("INSERT INTO provider_0_{} (tag,desc,variant,attribute,alarm,field0,field1,texpro) VALUES('pha_{}_sti','Etat Phare IR',2,1,1,0,0,1)".format(k,aut[0]))
        cur.execute("INSERT INTO provider_config_0_{} (name,field0,field1,field2,field3) VALUES('aut_{}','{}',502,500,1)".format(k,aut[0],aut[2]))
        cur.execute("INSERT INTO provider_reply_0_{} (tag,desc,variant,alarm,renv0,renv1,renv2,texpro) VALUES('aut_{}_dsc','Défaut com. Automate',2,1,1,1,{},1)".format(k,aut[0],k+1))

        # Local
        cur.execute("INSERT INTO local (tag,desc,variant,alarm,prio,renv0,renv1,renv2,texpro) VALUES('aut_{}_dac','Défaut communication automate / CT',2,1,3,1,2,{},2)".format(aut[0],k+1))
        cur.execute("INSERT INTO local (tag,desc,variant,alarm,prio,renv0,renv1,renv2,texpro) VALUES('dis_{}_dac','Défaut com. Disjoncteur',2,1,3,1,2,{},2)".format(aut[0],k+1))
        cur.execute("INSERT INTO local (tag,desc,variant,alarm,prio,renv0,renv1,renv2,texpro) VALUES('dis_{}_dsc','Défaut com. Disjoncteur',2,1,3,1,2,{},1)".format(aut[0],k+1))
        cur.execute("INSERT INTO local (tag,desc,variant,renv0,renv1,renv2,texpro) VALUES('pha_{}_ope','Etat opérationnel',1,1,3,{},1)".format(aut[0],k+1))

        k+=1
        sys.stdout.write('.')
    print('Done.')

    k = 0
    sys.stdout.write('Creating {} camera entries...'.format(len(cameras)))
    for cam in cameras:
        cur.execute("""CREATE TABLE "provider_3_{}" (
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
            "texpro" integer,
            "field0" TEXT,
            "field1" TEXT,
            PRIMARY KEY ("id")
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

        cur.execute("INSERT INTO provider_3_{} (tag,variant,attribute,alarm,field0,field1) VALUES('cad_{}_com',2,1,1,'1.3.6.1.2.1.2.2.1.8.1',1)".format(k, cam[0]))
        cur.execute("INSERT INTO provider_config_3_{} (name,field0,field3) VALUES('cad_{}','{}',5000)".format(k, cam[0],cam[2]))
        cur.execute("INSERT INTO provider_reply_3_{} (tag,desc,variant,alarm,prio,renv0,renv1,renv2,texpro) VALUES('cad_{}_dsc','Défaut com. caméra',2,1,1,1,1,{},1)".format(k, cam[0], 101+k))

        # Local
        cur.execute("INSERT INTO local (tag,desc,variant,alarm,prio,renv0,renv1,renv2,texpro) VALUES('cad_{}_dac','Défaut com. caméra',2,1,3,1,2,{},2)".format(cam[0],101+k))

        # Provider_4_0
        cur.execute("INSERT INTO provider_4_0 (tag,desc,variant,attribute,renv4,field0) VALUES('cad_{}_bw','caméra en mode nb',2,2,{},'http://{}/stw-cgi/image.cgi?msubmenu=camera&action=set&DayNightMode=BW')".format(cam[0], 4 if 1==int(cam[1]) else 6, cam[2]))
        cur.execute("INSERT INTO provider_4_0 (tag,desc,variant,attribute,renv4,field0) VALUES('cad_{}_co','caméra en mode couleur',2,2,{},'http://{}/stw-cgi/image.cgi?msubmenu=camera&action=set&DayNightMode=Color')".format(cam[0], 3 if 1==int(cam[1]) else 5, cam[2]))
        
        k+=1
        sys.stdout.write('.')
    print('Done.')

    sys.stdout.write('Creating {} switch entries...'.format(len(switchs)))
    for swi in switchs:
        cur.execute("""CREATE TABLE "provider_3_{}" (
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
            "texpro" integer,
            "field0" TEXT,
            "field1" TEXT,
            PRIMARY KEY ("id")
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

        cur.execute("INSERT INTO provider_3_{} (tag,variant,attribute,alarm,field0,field1) VALUES('swi_{}_com',2,1,1,'1.3.6.1.2.1.2.2.1.8.1',1)".format(k, swi[0]))
        cur.execute("INSERT INTO provider_config_3_{} (name,field0,field3) VALUES('swi_{}','{}',5000)".format(k, swi[0],swi[2]))
        cur.execute("INSERT INTO provider_reply_3_{} (tag,desc,variant,alarm,prio,renv0,renv1,renv2,texpro) VALUES('swi_{}_dsc','Défaut com. switch',2,1,1,1,1,{},1)".format(k, swi[0], 101+k))

        # Local
        cur.execute("INSERT INTO local (tag,desc,variant,alarm,prio,renv0,renv1,renv2,texpro) VALUES('swi_{}_dac','Défaut com. switch',2,1,3,1,2,{},2)".format(swi[0],101+k))

        k+=1
        sys.stdout.write('.')
    print('Done.')
    
    conn.commit()
    conn.close()
except IOError as e:
   print("I/O error({0}): {1}".format(e.errno, e.strerror))
   os.system("pause")
   exit()
except sqlite3.Error as er:
   print(sqlite3_errmsg(conn))
   os.system("pause")
   exit()
except: #handle other exceptions such as attribute errors
   print("Unexpected error:", sys.exc_info()[0])
   os.system("pause")
   exit()

os.system("pause")