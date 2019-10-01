#!/usr/bin/env python
"""
vtv_create_entries.py
Read a csv file to create corresponding entries in database.
aut: automate
cad: camera
pha: phare
tbt: disjoncteur
gns: gestionnaire niveau supervision
sct: scénarios CT
"""
import argparse, os, sys
import sqlite3

parser = argparse.ArgumentParser(description='Création des données dans la base server0.db du projet VTV.')
parser.add_argument('-fn', '--file_name', default='vtv_instances.txt', help='Nom du fichier txt')
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
    SWITCH = 'olm'
    MACHINE = 'map'
    ZONEFCT = 'zof'

    cameras = []
    automates = []
    supervisions = []
    scenarios = []
    switchs = []
    machines = []
    zonesfct = []

    for line in fw:
        value = line.rstrip().split('\t')[1:6]
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
        if MACHINE in line:
            machines.append(value)
        if ZONEFCT in line:
            zonesfct.append(value)

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
        cur.execute("INSERT INTO local (tag,desc,variant,texpro) VALUES('blegns_{}_stm','{} - Mode d''exploitation',1,1)".format(sup[0],sup[3]))
        cur.execute("INSERT INTO local (tag,desc,variant,alarm,prio,renv0,renv1,texpro) VALUES('blegns_{}_tad','{} - Mode distant',2,3,3,255,1,2)".format(sup[0],sup[3]))
        cur.execute("INSERT INTO local (tag,desc,variant,alarm,prio,renv0,renv1,texpro) VALUES('blegns_{}_tae','{} - Mode entretien',2,3,3,255,3,2)".format(sup[0],sup[3]))
        cur.execute("INSERT INTO local (tag,desc,variant,alarm,prio,renv0,renv1,texpro) VALUES('blegns_{}_tal','{} - Mode local',2,3,3,255,2,2)".format(sup[0],sup[3]))
        cur.execute("INSERT INTO local (tag,desc,variant,alarm,prio,renv0,renv1) VALUES('blegns_{}_tex','{} - Communication avec Texpro HS',2,2,1,255,4)".format(sup[0],sup[3]))

        cur.execute("INSERT INTO local (tag,desc,variant,texpro) VALUES('blegns_{}_ada','{} - Présence alarme',2,1)".format(sup[0], sup[3]))
        cur.execute("INSERT INTO local (tag,desc,variant,texpro) VALUES('blegns_{}_ate','{} - Présence alerte',2,1)".format(sup[0], sup[3]))
        cur.execute("INSERT INTO local (tag,desc,variant,texpro) VALUES('blegns_{}_dai','{} - Défaut IHM',2,2)".format(sup[0], sup[3]))
        cur.execute("INSERT INTO local (tag,desc,variant,texpro) VALUES('blegns_{}_dam','{} - Défaut matériel CI (AT)',2,2)".format(sup[0], sup[3]))
        cur.execute("INSERT INTO local (tag,desc,variant,texpro) VALUES('blegns_{}_dsi','{} - Défaut IHM',2,1)".format(sup[0], sup[3]))
        cur.execute("INSERT INTO local (tag,desc,variant,texpro) VALUES('blegns_{}_dsm','{} - Défaut matériel CI (AT)',2,1)".format(sup[0], sup[3]))
        cur.execute("INSERT INTO local (tag,desc,variant,texpro) VALUES('blegns_{}_mae','{} - Synthèse alertes',2,1)".format(sup[0], sup[3]))
        cur.execute("INSERT INTO local (tag,desc,variant,texpro) VALUES('blegns_{}_med','{} - Synthèse alarmes',2,1)".format(sup[0], sup[3]))

        sys.stdout.write('.')
    print('Done.')

    sys.stdout.write('Creating {} scenarios entries...'.format(len(scenarios)))
    for sct in scenarios:
        # Local
        cur.execute("INSERT INTO local (tag,desc,variant,renv0,renv1,renv2) VALUES('blesct_{}_cda','{} - Commande d''activation',1,2,1,{})".format(sct[0],sct[3],sct[1]))
        cur.execute("INSERT INTO local (tag,desc,variant,renv0,renv1,renv2,texpro) VALUES('blesct_{}_ope','{} - Etat opérationnel',1,2,3,{},1)".format(sct[0],sct[3],sct[1]))
        cur.execute("INSERT INTO local (tag,desc,variant,renv0,renv1,renv2,texpro) VALUES('blesct_{}_sta','{} - Etat d''activation',1,2,2,{},1)".format(sct[0],sct[3],sct[1]))
        sys.stdout.write('.')
    print('Done.')

    sys.stdout.write('Creating {} machine entries...'.format(len(machines)))
    for map in machines:
        # Local
        cur.execute("INSERT INTO local (tag,desc,variant,texpro) VALUES('blemap_{}_st1','{} - Etat connexion physique',2,1)".format(map[0],map[3]))
        sys.stdout.write('.')
    print('Done.')

    sys.stdout.write('Creating {} zonesfct entries...'.format(len(zonesfct)))
    for zof in zonesfct:
        # Local
        cur.execute("INSERT INTO local (tag,desc,variant,texpro) VALUES('blezof_{}_std','{} - Etat des zones fonction.',2,1)".format(zof[0],zof[3]))
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

        cur.execute("INSERT INTO provider_0_{} (tag,desc,variant,attribute,alarm,prio,invert,field0,field1,renv0,renv1,texpro) VALUES('bletbt_{}_dsj','{} - Défaut disjoncteur',2,1,2,1,1,1,0,20,{},1)".format(k,aut[0],aut[3].replace("IO", "DISJ"),k+1))
        conn.commit()
        conn.commit()
        if aut[0] == "29" or aut[0] == "scot":
            None
        elif aut[0] == "13":
            cur.execute("INSERT INTO provider_0_{} (tag,desc,variant,attribute,field0,field1,texpro) VALUES('blepha_{}_sti','{} - Etat Phare IR',2,1,0,0,1)".format(k,131,"PHARE 131"))
            cur.execute("INSERT INTO provider_0_{} (tag,desc,variant,attribute,renv0,renv1,renv4,field0,field1) VALUES('blepha_{}_cdi','{} - Commande d''allumage du phare infrarouge',2,0,200,{},{},0,0)".format(k,131,"PHARE 131",aut[4],aut[1]))
            cur.execute("INSERT INTO provider_0_{} (tag,desc,variant,attribute,field0,field1,texpro) VALUES('blepha_{}_sti','{} - Etat Phare IR',2,1,0,1,1)".format(k,132,"PHARE 132"))
            cur.execute("INSERT INTO provider_0_{} (tag,desc,variant,attribute,renv0,renv1,renv4,field0,field1) VALUES('blepha_{}_cdi','{} - Commande d''allumage du phare infrarouge',2,0,200,{},{},0,1)".format(k,132,"PHARE 132",aut[4],aut[1]))
        else:
            cur.execute("INSERT INTO provider_0_{} (tag,desc,variant,attribute,field0,field1,texpro) VALUES('blepha_{}_sti','{} - Etat Phare IR',2,1,0,0,1)".format(k,aut[0],aut[3].replace("IO", "PHARE")))
            cur.execute("INSERT INTO provider_0_{} (tag,desc,variant,attribute,renv0,renv1,renv4,field0,field1) VALUES('blepha_{}_cdi','{} - Commande d''allumage du phare infrarouge',2,0,200,{},{},0,0)".format(k,aut[0],aut[3].replace("IO", "PHARE"),aut[4],aut[1]))

        cur.execute("INSERT INTO provider_config_0_{} (name,field0,field1,field2,field3) VALUES('bleaut_{}','{}',502,500,1)".format(k,aut[0],aut[2]))
        cur.execute("INSERT INTO provider_reply_0_{} (tag,desc,variant,alarm,prio,renv0,renv1,renv2,texpro) VALUES('bleaut_{}_dsc','{} - Défaut com. Automate',2,2,1,1,1,{},1)".format(k,aut[0],aut[3],k+1))

        # Local
        cur.execute("INSERT INTO local (tag,desc,variant,alarm,prio,renv0,renv1,renv2,texpro) VALUES('bleaut_{}_dac','{} - Défaut com. automate',2,3,3,1,2,{},2)".format(aut[0],aut[3],k+1))
        cur.execute("INSERT INTO local (tag,desc,variant,texpro) VALUES('bleaut_{}_ada','{} - Présence alarme',2,1)".format(aut[0],aut[3]))
        cur.execute("INSERT INTO local (tag,desc,variant,texpro) VALUES('bleaut_{}_dai','{} - Défaut insta',2,2)".format(aut[0],aut[3]))
        cur.execute("INSERT INTO local (tag,desc,variant,texpro) VALUES('bleaut_{}_dsi','{} - Défaut insta',2,1)".format(aut[0],aut[3]))
        cur.execute("INSERT INTO local (tag,desc,variant,alarm,prio,renv0,renv1,renv2,texpro) VALUES('bletbt_{}_dac','{} - Défaut com. Disjoncteur',2,3,3,1,2,{},2)".format(aut[0],aut[3].replace("IO", "DISJ"),k+1))
        cur.execute("INSERT INTO local (tag,desc,variant,alarm,prio,renv0,renv1,renv2,texpro) VALUES('bletbt_{}_dsc','{} - Défaut com. Disjoncteur',2,2,1,1,2,{},1)".format(aut[0],aut[3].replace("IO", "DISJ"),k+1))
        cur.execute("INSERT INTO local (tag,desc,variant,alarm,prio,renv0,renv1,texpro) VALUES('bletbt_{}_daj','{} - Défaut disjoncteur',2,3,3,21,{},2)".format(aut[0],aut[3].replace("IO", "DISJ"),k+1))
        if aut[0] == "29" or aut[0] == "scot":
            None
        elif aut[0] == "13":
            cur.execute("INSERT INTO local (tag,desc,variant,renv0,renv1,renv2,texpro) VALUES('blepha_{}_ope','{} - Etat opérationnel',1,1,3,{},1)".format(131,"PHARE 131",k+1))
            cur.execute("INSERT INTO local (tag,desc,variant,renv0,renv1,renv2,texpro) VALUES('blepha_{}_ope','{} - Etat opérationnel',1,1,3,{},1)".format(132,"PHARE 132",k+1))
        else:
            cur.execute("INSERT INTO local (tag,desc,variant,renv0,renv1,renv2,texpro) VALUES('blepha_{}_ope','{} - Etat opérationnel',1,1,3,{},1)".format(aut[0],aut[3].replace("IO", "PHARE"),k+1))

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

        cur.execute("INSERT INTO provider_3_{} (tag,desc,variant,attribute,alarm,field0,field1) VALUES('blecad_{}_st1','{} - Défaut port com. 1',2,1,2,'1.3.6.1.2.1.2.2.1.8.1',1)".format(k,cam[0],cam[3]))
        cur.execute("INSERT INTO provider_config_3_{} (name,field0,field3) VALUES('blecad_{}','{}',5000)".format(k, cam[0],cam[2]))
        cur.execute("INSERT INTO provider_reply_3_{} (tag,desc,variant,alarm,prio,renv0,renv1,renv2,texpro) VALUES('blecad_{}_dsc','{} - Défaut com. caméra',2,2,1,1,1,{},1)".format(k,cam[0],cam[3],101+k))

        # Local
        cur.execute("INSERT INTO local (tag,desc,variant,alarm,prio,renv0,renv1,renv2,texpro) VALUES('blecad_{}_dac','{} - Défaut com. caméra',2,3,3,1,2,{},2)".format(cam[0],cam[3],101+k))

        # Provider_4_0
        cur.execute("INSERT INTO provider_4_0 (tag,desc,variant,attribute,renv0,renv1,renv4,field0) VALUES('blecad_{}_co','{} - Caméra en mode couleur',2,2,201,{},{},'http://{}/stw-cgi/image.cgi?msubmenu=camera&action=set&DayNightMode=Color')".format(cam[0],cam[3],cam[4], 3 if 1==int(cam[1]) else 5, cam[2]))
        cur.execute("INSERT INTO provider_4_0 (tag,desc,variant,attribute,renv0,renv1,renv4,field0) VALUES('blecad_{}_bw','{} - Caméra en mode nb',2,2,202,{},{},'http://{}/stw-cgi/image.cgi?msubmenu=camera&action=set&DayNightMode=BW')".format(cam[0],cam[3],cam[4], 4 if 1==int(cam[1]) else 6, cam[2]))

        k+=1
        sys.stdout.write('.')
    print('Done.')

    swi_num = 0
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

        cur.execute("INSERT INTO provider_3_{} (tag,desc,variant,attribute,alarm,renv0,renv1,renv2,field0,field1,texpro) VALUES('bleolm_{}_ds1','{} - Défaut port com. 1',2,1,2,10,{},1,'1.3.6.1.2.1.2.2.1.8.1',1,1)".format(k,swi[0],swi[3],swi_num+1))
        cur.execute("INSERT INTO provider_3_{} (tag,desc,variant,attribute,alarm,renv0,renv1,renv2,field0,field1,texpro) VALUES('bleolm_{}_ds2','{} - Défaut port com. 2',2,1,2,10,{},2,'1.3.6.1.2.1.2.2.1.8.2',1,1)".format(k,swi[0],swi[3],swi_num+1))
        cur.execute("INSERT INTO provider_config_3_{} (name,field0,field3) VALUES('bleolm_{}','{}',5000)".format(k,swi[0],swi[2]))
        cur.execute("INSERT INTO provider_reply_3_{} (tag,desc,variant,alarm,prio,renv0,renv1,renv2,texpro) VALUES('bleolm_{}_dsl','{} - Défaut com. switch',2,2,1,1,1,{},1)".format(k,swi[0],swi[3],101+k))

        # Local
        cur.execute("INSERT INTO local (tag,desc,variant,alarm,prio,renv0,renv1,renv2,texpro) VALUES('bleolm_{}_dal','{} - Défaut com. switch',2,3,3,1,2,{},2)".format(swi[0],swi[3],101+k))
        cur.execute("INSERT INTO local (tag,desc,variant,alarm,prio,renv0,renv1,renv2,texpro) VALUES('bleolm_{}_da1','{} - Défaut port com. 1',2,3,3,12,{},1,2)".format(swi[0],swi[3],swi_num+1))
        cur.execute("INSERT INTO local (tag,desc,variant,alarm,prio,renv0,renv1,renv2,texpro) VALUES('bleolm_{}_da2','{} - Défaut port com. 1',2,3,3,12,{},2,2)".format(swi[0],swi[3],swi_num+1))
        cur.execute("INSERT INTO local (tag,desc,variant,alarm,prio,renv0,renv1) VALUES('bleolm_{}_def','{} - Défaut technique switch',2,2,1,11,{})".format(swi[0],swi[3],swi_num+1))

        k+=1
        swi_num+=1
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