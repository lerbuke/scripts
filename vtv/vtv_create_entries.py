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
import argparse, os, sys, traceback
import sqlite3
from btcsqlbuilder import *

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
    ZONEFCT = 'zof'
    DISJ = 'tbt'
    PHARE = 'pha'

    cameras = []
    automates = []
    supervisions = []
    scenarios = []
    switchs = []
    zonesfct = []
    disjoncteurs = []
    phares = []

    for line in fw:
        value = line.rstrip('\n').split('\t')[1:]
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
        if ZONEFCT in line:
            zonesfct.append(value)
        if DISJ in line:
            disjoncteurs.append(value)
        if PHARE in line:
            phares.append(value)

    fw.close()
    #print(automates)
    #print(cameras)
    #print(supervisions)
    #print(scenarios)
    #print(switchs)

    # Open the server0.db database
    conn = sqlite3.connect(args.db_path + 'server0.db')
    cur = conn.cursor()

    # Delete all MODBUS (0), URL (4) and SNMP (3) providers, provider configurations and replies
    for provider in (0,3,4):
        sql = SqlBuilderSelect('provider', 'providerNbSubId')
        sql.where('providerType={}'.format(provider))
        cur.execute(sql.command())

        nb = cur.fetchone()[0]
        for i in range(0,nb):
            suffix = "_" + str(provider) + "_" + str(i)
            cur.execute(SqlBuilderDrop('provider' + suffix).command())
            cur.execute(SqlBuilderDrop('provider_config' + suffix).command())
            cur.execute(SqlBuilderDrop('provider_reply' + suffix).command())

    # Recreate local table
    cur.execute(SqlBuilderDrop('local').command())

    sql = SqlBuilderCreate('local')
    sql.addInt('id', True, True)
    sql.addText(['tag', 'desc', 'desc2'])
    sql.addInt(['variant', 'alarm', 'prio', 'alarm_txt', 'renv0', 'renv1', 'renv2', 'renv3', 'renv4', 'store', 'texpro'])
    cur.execute(sql.command())


    # Update the number of automates and cameras
    sql = SqlBuilderUpdate('provider')
    sql.set('providerNbSubId', len(automates))
    sql.where('providerType = 0')
    cur.execute(sql.command())

    sql = SqlBuilderUpdate('provider')
    sql.set('providerNbSubId', len(cameras)+len(switchs))
    sql.where('providerType = 3')
    cur.execute(sql.command())

    sql = SqlBuilderUpdate('provider')
    sql.set('providerNbSubId', len(cameras))
    sql.where('providerType = 4')
    cur.execute(sql.command())

    conn.commit()


    sys.stdout.write('Creating {} supervision entries...'.format(len(supervisions)))
    for sup in supervisions:
        # Local
        sql = SqlBuilderInsert('local')
        sql.add('tag', 'blegns_{}_stm'.format(sup[0]))
        sql.add('desc', '{} - Mode d\'exploitation'.format(sup[3]))
        sql.add('desc2', sup[5])
        sql.add('variant', 1)
        sql.add('renv0', 255)
        sql.add('renv1', 5)
        sql.add('texpro', 1)
        cur.execute(sql.command())

        sql = SqlBuilderInsert('local')
        sql.add('tag', 'blegns_{}_tad'.format(sup[0]))
        sql.add('desc', '{} - Mode distant'.format(sup[3]))
        sql.add('desc2', sup[5])
        sql.add('variant', 2)
        sql.add('alarm', 3)
        sql.add('prio', 2)
        sql.add('renv0', 255)
        sql.add('renv1', 1)
        sql.add('texpro', 2)
        cur.execute(sql.command())

        sql = SqlBuilderInsert('local')
        sql.add('tag', 'blegns_{}_tae'.format(sup[0]))
        sql.add('desc', '{} - Mode entretien'.format(sup[3]))
        sql.add('desc2', sup[5])
        sql.add('variant', 2)
        sql.add('alarm', 3)
        sql.add('prio', 2)
        sql.add('renv0', 255)
        sql.add('renv1', 3)
        sql.add('texpro', 2)
        cur.execute(sql.command())

        sql = SqlBuilderInsert('local')
        sql.add('tag', 'blegns_{}_tal'.format(sup[0]))
        sql.add('desc', '{} - Mode local'.format(sup[3]))
        sql.add('desc2', sup[5])
        sql.add('variant', 2)
        sql.add('alarm', 3)
        sql.add('prio', 2)
        sql.add('renv0', 255)
        sql.add('renv1', 2)
        sql.add('texpro', 2)
        cur.execute(sql.command())

        sql = SqlBuilderInsert('local')
        sql.add('tag', 'blegns_{}_tex'.format(sup[0]))
        sql.add('desc', '{} - Communication avec Texpro HS'.format(sup[3]))
        sql.add('desc2', sup[5])
        sql.add('variant', 2)
        sql.add('alarm', 4)
        sql.add('prio', 1)
        sql.add('renv0', 255)
        sql.add('renv1', 4)
        cur.execute(sql.command())

        sql = SqlBuilderInsert('local')
        sql.add('tag', 'blegns_{}_ada'.format(sup[0]))
        sql.add('desc', '{} - Présence alarme'.format(sup[3]))
        sql.add('desc2', sup[5])
        sql.add('variant', 2)
        sql.add('texpro', 1)
        cur.execute(sql.command())

        sql = SqlBuilderInsert('local')
        sql.add('tag', 'blegns_{}_ate'.format(sup[0]))
        sql.add('desc', '{} - Présence alerte'.format(sup[3]))
        sql.add('desc2', sup[5])
        sql.add('variant', 2)
        sql.add('texpro', 1)
        cur.execute(sql.command())

        sql = SqlBuilderInsert('local')
        sql.add('tag', 'blegns_{}_dai'.format(sup[0]))
        sql.add('desc', '{} - Défaut IHM'.format(sup[3]))
        sql.add('desc2', sup[5])
        sql.add('variant', 2)
        sql.add('texpro', 2)
        cur.execute(sql.command())

        sql = SqlBuilderInsert('local')
        sql.add('tag', 'blegns_{}_dam'.format(sup[0]))
        sql.add('desc', '{} - Défaut matériel CI (AT)'.format(sup[3]))
        sql.add('desc2', sup[5])
        sql.add('variant', 2)
        sql.add('texpro', 2)
        cur.execute(sql.command())

        sql = SqlBuilderInsert('local')
        sql.add('tag', 'blegns_{}_dsi'.format(sup[0]))
        sql.add('desc', '{} - Défaut IHM'.format(sup[3]))
        sql.add('desc2', sup[5])
        sql.add('variant', 2)
        sql.add('texpro', 1)
        cur.execute(sql.command())

        sql = SqlBuilderInsert('local')
        sql.add('tag', 'blegns_{}_dsm'.format(sup[0]))
        sql.add('desc', '{} - Défaut matériel CI (AT)'.format(sup[3]))
        sql.add('desc2', sup[5])
        sql.add('variant', 2)
        sql.add('texpro', 1)
        cur.execute(sql.command())

        sql = SqlBuilderInsert('local')
        sql.add('tag', 'blegns_{}_mae'.format(sup[0]))
        sql.add('desc', '{} - Synthèse alertes'.format(sup[3]))
        sql.add('desc2', sup[5])
        sql.add('variant', 2)
        sql.add('texpro', 1)
        cur.execute(sql.command())

        sql = SqlBuilderInsert('local')
        sql.add('tag', 'blegns_{}_med'.format(sup[0]))
        sql.add('desc', '{} - Synthèse alarmes'.format(sup[3]))
        sql.add('desc2', sup[5])
        sql.add('variant', 2)
        sql.add('texpro', 1)
        cur.execute(sql.command())

        sys.stdout.write('.')
    print('Done.')

    sys.stdout.write('Creating {} scenarios entries...'.format(len(scenarios)))
    for sct in scenarios:
        # Local
        sql = SqlBuilderInsert('local')
        sql.add('tag', 'blesct_{}_cda'.format(sct[0]))
        sql.add('desc', '{} - Commande d\'activation'.format(sct[3]))
        sql.add('desc2', sct[5])
        sql.add('variant', 1)
        sql.add('renv0', 2)
        sql.add('renv1', 1)
        sql.add('renv2', sct[1])
        cur.execute(sql.command())

        sql = SqlBuilderInsert('local')
        sql.add('tag', 'blesct_{}_ope'.format(sct[0]))
        sql.add('desc', '{} - Etat opérationnel'.format(sct[3]))
        sql.add('desc2', sct[5])
        sql.add('variant', 1)
        sql.add('renv0', 2)
        sql.add('renv1', 3)
        sql.add('renv2', sct[1])
        sql.add('texpro', 1)
        cur.execute(sql.command())

        sql = SqlBuilderInsert('local')
        sql.add('tag', 'blesct_{}_sta'.format(sct[0]))
        sql.add('desc', '{} - Etat d\'activation'.format(sct[3]))
        sql.add('desc2', sct[5])
        sql.add('variant', 1)
        sql.add('renv0', 2)
        sql.add('renv1', 2)
        sql.add('renv2', sct[1])
        sql.add('texpro', 1)
        cur.execute(sql.command())

        sys.stdout.write('.')
    print('Done.')

    sys.stdout.write('Creating {} zonesfct entries...'.format(len(zonesfct)))
    for zof in zonesfct:
        # Local
        sql = SqlBuilderInsert('local')
        sql.add('tag', 'blezof_{}_std'.format(zof[0]))
        sql.add('desc', '{} - Etat des zones fonction.'.format(zof[3]))
        sql.add('desc2', zof[5])
        sql.add('variant', 2)
        sql.add('texpro', 1)
        cur.execute(sql.command())
        sys.stdout.write('.')
    print('Done.')


    k = 0
    sys.stdout.write('Creating {} automate entries...'.format(len(automates)))
    for aut in automates:
        sql = SqlBuilderCreate('provider_0_{}'.format(k))
        sql.addInt('id', True, True)
        sql.addText(['tag', 'desc', 'desc2'])
        sql.addInt(['variant', 'attribute', 'alarm', 'prio', 'alarm_txt', 'invert', 'renv0', 'renv1', 'renv2', 'renv3', 'renv4', 'immediate', 'store'])
        sql.addReal(['scale', 'factor'])
        sql.addText(['field0', 'field1'])
        sql.addInt('texpro')
        cur.execute(sql.command())

        sql = SqlBuilderCreate('provider_config_0_{}'.format(k))
        sql.addInt('id', True, True)
        sql.addText(['name', 'field0', 'field1', 'field2', 'field3', 'field4', 'field5'])
        cur.execute(sql.command())

        sql = SqlBuilderCreate('provider_reply_0_{}'.format(k))
        sql.addInt('id', True, True)
        sql.addText(['tag', 'desc', 'desc2'])
        sql.addInt(['variant', 'alarm', 'prio', 'alarm_txt', 'renv0', 'renv1', 'renv2', 'renv3', 'renv4', 'store', 'texpro'])
        cur.execute(sql.command())

        sql = SqlBuilderInsert('provider_0_{}'.format(k))
        sql.add('tag', 'bletbt_{}_dsj'.format(aut[0]))
        sql.add('desc', '{} - Défaut disjoncteur'.format(disjoncteurs[k][3]))
        sql.add('desc2', disjoncteurs[k][5])
        sql.add('variant', 2)
        sql.add('attribute', 1)
        sql.add('alarm', 4)
        sql.add('invert', 1)
        sql.add('field0', 1)
        sql.add('field1', 0)
        sql.add('renv0', 20)
        sql.add('renv1', k+1)
        sql.add('texpro', 1)
        cur.execute(sql.command())

        conn.commit()

        if aut[0] == "29" or aut[0] == "scot":
            None
        elif aut[0] == "13":
            sql = SqlBuilderInsert('provider_0_{}'.format(k))
            sql.add('tag', 'blepha_{}_sti'.format(131))
            sql.add('desc', '{} - Etat Phare IR'.format(phares[k][3]))
            sql.add('desc2', phares[k][5])
            sql.add('variant', 2)
            sql.add('attribute', 1)
            sql.add('field0', 0)
            sql.add('field1', 0)
            sql.add('texpro', 1)
            cur.execute(sql.command())

            sql = SqlBuilderInsert('provider_0_{}'.format(k))
            sql.add('tag', 'blepha_{}_cdi'.format(131))
            sql.add('desc', '{} - Commande d\'allumage du phare infrarouge'.format(phares[k][3]))
            sql.add('desc2', phares[k][5])
            sql.add('variant', 2)
            sql.add('attribute', 0)
            sql.add('renv0', 200)
            sql.add('renv1', phares[k][4])
            sql.add('renv4', aut[1])
            sql.add('field0', 0)
            sql.add('field1', 0)
            cur.execute(sql.command())

            sql = SqlBuilderInsert('provider_0_{}'.format(k))
            sql.add('tag', 'blepha_{}_sti'.format(132))
            sql.add('desc', '{} - Etat Phare IR'.format(phares[k+9][3]))
            sql.add('desc2', phares[k+9][5])
            sql.add('variant', 2)
            sql.add('attribute', 1)
            sql.add('field0', 0)
            sql.add('field1', 1)
            sql.add('texpro', 1)
            cur.execute(sql.command())

            sql = SqlBuilderInsert('provider_0_{}'.format(k))
            sql.add('tag', 'blepha_{}_cdi'.format(132))
            sql.add('desc', '{} - Commande d\'allumage du phare infrarouge'.format(phares[k+9][3]))
            sql.add('desc2', phares[k+9][5])
            sql.add('variant', 2)
            sql.add('attribute', 0)
            sql.add('renv0', 200)
            sql.add('renv1', phares[k+9][4])
            sql.add('renv4', aut[1])
            sql.add('field0', 0)
            sql.add('field1', 1)
            cur.execute(sql.command())
        else:
            sql = SqlBuilderInsert('provider_0_{}'.format(k))
            sql.add('tag', 'blepha_{}_sti'.format(aut[0]))
            sql.add('desc', '{} - Etat Phare IR'.format(phares[k][3]))
            sql.add('desc2', phares[k][5])
            sql.add('variant', 2)
            sql.add('attribute', 1)
            sql.add('field0', 0)
            sql.add('field1', 0)
            sql.add('texpro', 1)
            cur.execute(sql.command())

            sql = SqlBuilderInsert('provider_0_{}'.format(k))
            sql.add('tag', 'blepha_{}_cdi'.format(aut[0]))
            sql.add('desc', '{} - Commande d\'allumage du phare infrarouge'.format(phares[k][3]))
            sql.add('desc2', phares[k][5])
            sql.add('variant', 2)
            sql.add('attribute', 0)
            sql.add('renv0', 200)
            sql.add('renv1', phares[k][4])
            sql.add('renv4', aut[1])
            sql.add('field0', 0)
            sql.add('field1', 0)
            cur.execute(sql.command())

        sql = SqlBuilderInsert('provider_config_0_{}'.format(k))
        sql.add('name', 'bleaut_{}'.format(aut[0]))
        sql.add('field0', aut[2])
        sql.add('field1', 502)
        sql.add('field2', 500)
        sql.add('field3', 1)
        cur.execute(sql.command())

        sql = SqlBuilderInsert('provider_reply_0_{}'.format(k))
        sql.add('tag', 'bleaut_{}_dsc'.format(aut[0]))
        sql.add('desc', '{} - Défaut com. Automate'.format(aut[3]))
        sql.add('desc2', aut[5])
        sql.add('variant', 2)
        sql.add('alarm', 4)
        sql.add('renv0', 1)
        sql.add('renv1', 1)
        sql.add('renv2', k+1)
        sql.add('texpro', 1)
        cur.execute(sql.command())

        # Local
        sql = SqlBuilderInsert('local')
        sql.add('tag', 'bleaut_{}_dac'.format(aut[0]))
        sql.add('desc', '{} - Défaut com. automate'.format(aut[3]))
        sql.add('desc2', aut[5])
        sql.add('variant', 2)
        sql.add('alarm', 3)
        sql.add('prio', 2)
        sql.add('renv0', 1)
        sql.add('renv1', 2)
        sql.add('renv2', k+1)
        sql.add('texpro', 2)
        cur.execute(sql.command())

        sql = SqlBuilderInsert('local')
        sql.add('tag', 'bleaut_{}_ada'.format(aut[0]))
        sql.add('desc', '{} - Présence alarme'.format(aut[3]))
        sql.add('desc2', aut[5])
        sql.add('variant', 2)
        sql.add('texpro', 1)
        cur.execute(sql.command())

        sql = SqlBuilderInsert('local')
        sql.add('tag', 'bleaut_{}_dai'.format(aut[0]))
        sql.add('desc', '{} - Défaut insta'.format(aut[3]))
        sql.add('desc2', aut[5])
        sql.add('variant', 2)
        sql.add('texpro', 2)
        cur.execute(sql.command())

        sql = SqlBuilderInsert('local')
        sql.add('tag', 'bleaut_{}_dsi'.format(aut[0]))
        sql.add('desc', '{} - Défaut insta'.format(aut[3]))
        sql.add('desc2', aut[5])
        sql.add('variant', 2)
        sql.add('texpro', 1)
        cur.execute(sql.command())

        sql = SqlBuilderInsert('local')
        sql.add('tag', 'bletbt_{}_dac'.format(aut[0]))
        sql.add('desc', '{} - Défaut com. Disjoncteur'.format(disjoncteurs[k][3]))
        sql.add('desc2', disjoncteurs[k][5])
        sql.add('variant', 2)
        sql.add('alarm', 3)
        sql.add('prio', 1)
        sql.add('renv0', 1)
        sql.add('renv1', 2)
        sql.add('renv2', k+1)
        sql.add('texpro', 2)
        cur.execute(sql.command())

        sql = SqlBuilderInsert('local')
        sql.add('tag', 'bletbt_{}_dsc'.format(aut[0]))
        sql.add('desc', '{} - Défaut com. Disjoncteur'.format(disjoncteurs[k][3]))
        sql.add('desc2', disjoncteurs[k][5])
        sql.add('variant', 2)
        sql.add('alarm', 4)
        sql.add('renv0', 1)
        sql.add('renv1', 2)
        sql.add('renv2', k+1)
        sql.add('texpro', 1)
        cur.execute(sql.command())

        sql = SqlBuilderInsert('local')
        sql.add('tag', 'bletbt_{}_daj'.format(aut[0]))
        sql.add('desc', '{} - Défaut disjoncteur'.format(disjoncteurs[k][3]))
        sql.add('desc2', disjoncteurs[k][5])
        sql.add('variant', 2)
        sql.add('alarm', 3)
        sql.add('prio', 1)
        sql.add('renv0', 21)
        sql.add('renv1', k+1)
        sql.add('texpro', 2)
        cur.execute(sql.command())

        if aut[0] == "29" or aut[0] == "scot":
            None
        elif aut[0] == "13":
            sql = SqlBuilderInsert('local')
            sql.add('tag', 'blepha_{}_ope'.format(131))
            sql.add('desc', '{} - Etat opérationnel'.format(phares[k][3]))
            sql.add('desc2', phares[k][5])
            sql.add('variant', 1)
            sql.add('renv0', 1)
            sql.add('renv1', 3)
            sql.add('renv2', k+1)
            sql.add('texpro', 1)
            cur.execute(sql.command())

            sql = SqlBuilderInsert('local')
            sql.add('tag', 'blepha_{}_ope'.format(132))
            sql.add('desc', '{} - Etat opérationnel'.format(phares[k+9][3]))
            sql.add('desc2', phares[k+9][5])
            sql.add('variant', 1)
            sql.add('renv0', 1)
            sql.add('renv1', 3)
            sql.add('renv2', k+1)
            sql.add('texpro', 1)
            cur.execute(sql.command())

        else:
            sql = SqlBuilderInsert('local')
            sql.add('tag', 'blepha_{}_ope'.format(aut[0]))
            sql.add('desc', '{} - Etat opérationnel'.format(phares[k][3]))
            sql.add('desc2', phares[k][5])
            sql.add('variant', 1)
            sql.add('renv0', 1)
            sql.add('renv1', 3)
            sql.add('renv2', k+1)
            sql.add('texpro', 1)
            cur.execute(sql.command())

        k+=1
        sys.stdout.write('.')
    print('Done.')

    k = 0
    sys.stdout.write('Creating {} camera entries...'.format(len(cameras)))
    for cam in cameras:
        for no in [3,4]:
            sql = SqlBuilderCreate('provider_{}_{}'.format(no, k))
            sql.addInt('id', True, True)
            sql.addText(['tag', 'desc', 'desc2'])
            sql.addInt(['variant', 'attribute', 'alarm', 'prio', 'alarm_txt', 'invert', 'renv0', 'renv1', 'renv2', 'renv3', 'renv4', 'immediate', 'store'])
            sql.addReal(['scale', 'factor'])
            sql.addInt(['texpro', 'field0', 'field1'])
            cur.execute(sql.command())

            sql = SqlBuilderCreate('provider_config_{}_{}'.format(no, k))
            sql.addInt('id', True, True)
            sql.addText(['name', 'field0', 'field1', 'field2', 'field3'])
            cur.execute(sql.command())

            sql = SqlBuilderCreate('provider_reply_{}_{}'.format(no, k))
            sql.addInt('id', True, True)
            sql.addText(['tag', 'desc', 'desc2'])
            sql.addInt(['variant', 'alarm', 'prio', 'alarm_txt', 'renv0', 'renv1', 'renv2', 'renv3', 'renv4', 'store', 'texpro'])
            cur.execute(sql.command())

        conn.commit()

        sql = SqlBuilderInsert('provider_3_{}'.format(k))
        sql.add('tag', 'blecad_{}_st1'.format(cam[0]))
        sql.add('desc', '{} - Défaut port com. 1'.format(cam[3]))
        sql.add('desc2', cam[5])
        sql.add('variant', 2)
        sql.add('attribute', 1)
        sql.add('alarm', 0)
        sql.add('field0', '1.3.6.1.2.1.2.2.1.8.1')
        sql.add('field1', 1)
        cur.execute(sql.command())

        sql = SqlBuilderInsert('provider_config_3_{}'.format(k))
        sql.add('name', 'blecad_{}'.format(cam[0]))
        sql.add('field0', cam[2])
        sql.add('field3', 5000)
        cur.execute(sql.command())

        sql = SqlBuilderInsert('provider_reply_3_{}'.format(k))
        sql.add('tag', 'blecad_{}_dsc'.format(cam[0]))
        sql.add('desc', '{} - Défaut com. caméra'.format(cam[3]))
        sql.add('desc2', cam[5])
        sql.add('variant', 2)
        sql.add('alarm', 4)
        sql.add('renv0', 1)
        sql.add('renv1', 1)
        sql.add('renv2', 101+k)
        sql.add('texpro', 1)
        cur.execute(sql.command())

        sql = SqlBuilderInsert('provider_config_4_{}'.format(k))
        sql.add('name', 'blecad_{}'.format(cam[0]))
        sql.add('field0', 'admin')
        sql.add('field1', 'A1vtv204')
        sql.add('field2', 3000)
        cur.execute(sql.command())

        # Local
        sql = SqlBuilderInsert('local')
        sql.add('tag', 'blecad_{}_dac'.format(cam[0]))
        sql.add('desc', '{} - Défaut com. caméra'.format(cam[3]))
        sql.add('desc2', cam[5])
        sql.add('variant', 2)
        sql.add('alarm', 3)
        sql.add('prio', 0)
        sql.add('renv0', 1)
        sql.add('renv1', 2)
        sql.add('renv2', 101+k)
        sql.add('texpro', 2)
        cur.execute(sql.command())

        # Provider_4_x
        sql = SqlBuilderInsert('provider_4_{}'.format(k))
        sql.add('tag', 'blecad_{}_co'.format(cam[0]))
        sql.add('desc', '{} - Caméra en mode couleur'.format(cam[3]))
        sql.add('desc2', cam[5])
        sql.add('variant', 2)
        sql.add('attribute', 2)
        sql.add('renv0', 201)
        sql.add('renv1', cam[4])
        sql.add('renv4', 3 if 1==int(cam[1]) else 5)
        sql.add('field0', 'http://{}/stw-cgi/image.cgi?msubmenu=camera&action=set&DayNightMode=Color'.format(cam[2]))
        cur.execute(sql.command())

        sql = SqlBuilderInsert('provider_4_{}'.format(k))
        sql.add('tag', 'blecad_{}_bw'.format(cam[0]))
        sql.add('desc', '{} - Caméra en mode nb'.format(cam[3]))
        sql.add('desc2', cam[5])
        sql.add('variant', 2)
        sql.add('attribute', 2)
        sql.add('renv0', 202)
        sql.add('renv1', cam[4])
        sql.add('renv4', 4 if 1==int(cam[1]) else 6)
        sql.add('field0', 'http://{}/stw-cgi/image.cgi?msubmenu=camera&action=set&DayNightMode=BW'.format(cam[2]))
        cur.execute(sql.command())

        k+=1
        sys.stdout.write('.')
    print('Done.')

    swi_num = 0
    sys.stdout.write('Creating {} switch entries...'.format(len(switchs)))
    for swi in switchs:
        sql = SqlBuilderCreate('provider_3_{}'.format(k))
        sql.addInt('id', True, True)
        sql.addText(['tag', 'desc', 'desc2'])
        sql.addInt(['variant', 'attribute', 'alarm', 'prio', 'alarm_txt', 'invert', 'renv0', 'renv1', 'renv2', 'renv3', 'renv4', 'immediate', 'store'])
        sql.addReal(['scale', 'factor'])
        sql.addInt('texpro')
        sql.addText(['field0', 'field1'])
        cur.execute(sql.command())

        sql = SqlBuilderCreate('provider_config_3_{}'.format(k))
        sql.addInt('id', True, True)
        sql.addText(['name', 'field0', 'field1', 'field2', 'field3'])
        cur.execute(sql.command())

        sql = SqlBuilderCreate('provider_reply_3_{}'.format( k))
        sql.addInt('id', True, True)
        sql.addText(['tag', 'desc', 'desc2'])
        sql.addInt(['variant', 'alarm', 'prio', 'alarm_txt', 'renv0', 'renv1', 'renv2', 'renv3', 'renv4', 'store', 'texpro'])
        cur.execute(sql.command())

        conn.commit()

        if swi[0] == "scot1" or swi[0] == "scot2" :
            sql = SqlBuilderInsert('provider_3_{}'.format(k))
            sql.add('tag', 'bleolm_{}_ds1'.format(swi[0]))
            sql.add('desc', '{} - Défaut port com. 1'.format(swi[3]))
            sql.add('desc2', swi[5])
            sql.add('variant', 2)
            sql.add('attribute', 1)
            sql.add('alarm', 4)
            sql.add('renv0', 10)
            sql.add('renv1', swi_num+1)
            sql.add('renv2', 1)
            sql.add('field0', '1.3.6.1.2.1.2.2.1.8.10303')
            sql.add('field1', 1)
            sql.add('texpro', 1)
            cur.execute(sql.command())

            sql = SqlBuilderInsert('provider_3_{}'.format(k))
            sql.add('tag', 'bleolm_{}_ds2'.format(swi[0]))
            sql.add('desc', '{} - Défaut port com. 2'.format(swi[3]))
            sql.add('desc2', swi[5])
            sql.add('variant', 2)
            sql.add('attribute', 1)
            sql.add('alarm', 4)
            sql.add('renv0', 10)
            sql.add('renv1', swi_num+1)
            sql.add('renv2', 2)
            sql.add('field0', '1.3.6.1.2.1.2.2.1.8.10304')
            sql.add('field1', 1)
            sql.add('texpro', 1)
            cur.execute(sql.command())
        else:
            sql = SqlBuilderInsert('provider_3_{}'.format(k))
            sql.add('tag', 'bleolm_{}_ds1'.format(swi[0]))
            sql.add('desc', '{} - Défaut port com. 1'.format(swi[3]))
            sql.add('desc2', swi[5])
            sql.add('variant', 2)
            sql.add('attribute', 1)
            sql.add('alarm', 4)
            sql.add('renv0', 10)
            sql.add('renv1', swi_num+1)
            sql.add('renv2', 1)
            sql.add('field0', '1.3.6.1.2.1.2.2.1.8.1')
            sql.add('field1', 1)
            sql.add('texpro', 1)
            cur.execute(sql.command())

            sql = SqlBuilderInsert('provider_3_{}'.format(k))
            sql.add('tag', 'bleolm_{}_ds2'.format(swi[0]))
            sql.add('desc', '{} - Défaut port com. 2'.format(swi[3]))
            sql.add('desc2', swi[5])
            sql.add('variant', 2)
            sql.add('attribute', 1)
            sql.add('alarm', 4)
            sql.add('renv0', 10)
            sql.add('renv1', swi_num+1)
            sql.add('renv2', 2)
            sql.add('field0', '1.3.6.1.2.1.2.2.1.8.2')
            sql.add('field1', 1)
            sql.add('texpro', 1)
            cur.execute(sql.command())

        sql = SqlBuilderInsert('provider_config_3_{}'.format(k))
        sql.add('name', 'bleolm_{}'.format(swi[0]))
        sql.add('field0', swi[2])
        sql.add('field3', 5000)
        cur.execute(sql.command())

        sql = SqlBuilderInsert('provider_reply_3_{}'.format(k))
        sql.add('tag', 'bleolm_{}_dsl'.format(swi[0]))
        sql.add('desc', '{} - Défaut com. switch'.format(swi[3]))
        sql.add('desc2', swi[5])
        sql.add('variant', 2)
        sql.add('alarm', 4)
        sql.add('renv0', 1)
        sql.add('renv1', 1)
        sql.add('renv2', 101+k)
        sql.add('texpro', 1)
        cur.execute(sql.command())

        # Local
        sql = SqlBuilderInsert('local')
        sql.add('tag', 'bleolm_{}_dal'.format(swi[0]))
        sql.add('desc', '{} - Défaut com. switch'.format(swi[3]))
        sql.add('desc2', swi[5])
        sql.add('variant', 2)
        sql.add('alarm', 3)
        sql.add('prio', 2)
        sql.add('renv0', 1)
        sql.add('renv1', 2)
        sql.add('renv2', 101+k)
        sql.add('texpro', 2)
        cur.execute(sql.command())

        sql = SqlBuilderInsert('local')
        sql.add('tag', 'bleolm_{}_da1'.format(swi[0]))
        sql.add('desc', '{} - Défaut port com. 1'.format(swi[3]))
        sql.add('desc2', swi[5])
        sql.add('variant', 2)
        sql.add('alarm', 3)
        sql.add('prio', 1)
        sql.add('renv0', 12)
        sql.add('renv1', swi_num+1)
        sql.add('renv2', 1)
        sql.add('texpro', 2)
        cur.execute(sql.command())

        sql = SqlBuilderInsert('local')
        sql.add('tag', 'bleolm_{}_da2'.format(swi[0]))
        sql.add('desc', '{} - Défaut port com. 2'.format(swi[3]))
        sql.add('desc2', swi[5])
        sql.add('variant', 2)
        sql.add('alarm', 3)
        sql.add('prio', 1)
        sql.add('renv0', 12)
        sql.add('renv1', swi_num+1)
        sql.add('renv2', 2)
        sql.add('texpro', 2)
        cur.execute(sql.command())

        sql = SqlBuilderInsert('local')
        sql.add('tag', 'bleolm_{}_def'.format(swi[0]))
        sql.add('desc', '{} - Défaut technique switch'.format(swi[3]))
        sql.add('desc2', swi[5])
        sql.add('variant', 2)
        sql.add('alarm', 4)
        sql.add('renv0', 11)
        sql.add('renv1', swi_num+1)
        cur.execute(sql.command())

        k+=1
        swi_num+=1
        sys.stdout.write('.')
    print('Done.')

    conn.commit()
    conn.close()
except IOError as e:
   print("I/O error({0}): {1} / Line {2}".format(e.errno, e.strerror))
   print(traceback.format_exc())
   os.system("pause")
   exit()
except sqlite3.Error as er:
   #print(sqlite3_errmsg(conn))
   print(traceback.format_exc())
   os.system("pause")
   exit()
except: #handle other exceptions such as attribute errors
   print("Unexpected error:", sys.exc_info()[0])
   print(traceback.format_exc())
   os.system("pause")
   exit()

os.system("pause")