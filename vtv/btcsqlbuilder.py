#!/usr/bin/env python
"""
btcsqlbuilder.py

"""
import argparse, os, sys, traceback
import sqlite3
from enum import Enum

sys.stderr = open('./cmds.txt', 'w', newline='\r\n')

parser = argparse.ArgumentParser(description='Création des données dans la base server0.db du projet VTV.')
#parser.add_argument('-fn', '--file_name', default='vtv_instances.txt', help='Nom du fichier txt')
parser.add_argument('-dbp', '--db_path', default='./server_db/', help='Chemin de la base de données server0.db')

args = parser.parse_args()
print(args)

class Type(Enum):
     CREATE = 1
     DROP = 2
     INSERT = 3
     UPDATE = 4
     SELECT = 5


###############################################################################
class SqlBuilder:
    def __init__(self, table, type):
        self.type = type
        self.table = table
        self.dict = {}
        if type == Type.CREATE:
            self.cmd = 'CREATE TABLE ' + table
        elif type ==  Type.DROP:
            self.cmd = 'DROP TABLE IF EXISTS ' + table
        elif type ==  Type.INSERT:
            self.cmd = 'INSERT INTO ' + table
        elif type ==  Type.UPDATE:
            self.cmd = 'UPDATE ' + table
        elif type ==  Type.SELECT:
            self.cmd = 'SELECT '

    def command(self):
        sys.stderr.write(self.cmd +'\n')
        return self.cmd

###############################################################################
class SqlBuilderCreate(SqlBuilder):

    def __init__(self, table):
        SqlBuilder.__init__(self, table, Type.CREATE)

    def primaryKey(self, tag):
        for key in self.dict:
            if -1 != self.dict[key].find('PRIMARY KEY'):
                raise('Primary key already exists.')
        
        self.dict[tag] += ' PRIMARY KEY'

    def addText(self, tag):
        self.dict[tag] = 'TEXT'

    def addInt(self, tag, not_null=False):
        self.dict[tag] = 'INTEGER NOT NULL' if not_null else 'INTEGER'
        
    def addReal(self, tag):
        self.dict[tag] = 'REAL'

    def command(self):
        if len(self.dict) > 0:
            self.cmd += ' ('
            for tag in self.dict:
                self.cmd += '"' + tag + '" ' + self.dict[tag] + ','
            self.cmd = self.cmd[:-1]
            self.cmd += ')'
        return super().command()

###############################################################################
class SqlBuilderDrop(SqlBuilder):

    def __init__(self, table):
        SqlBuilder.__init__(self, table, Type.DROP)

###############################################################################
class SqlBuilderInsert(SqlBuilder):

    def __init__(self, table):
        SqlBuilder.__init__(self, table, Type.INSERT)

    def add(self, tag, value):
        self.dict[tag] = str(value)

    def command(self):
        if len(self.dict) == 0:
            raise('Nothing to insert.')

        self.cmd += ' ('
        for tag in self.dict:
            self.cmd += '"' + tag + '",'
        self.cmd = self.cmd[:-1]
        self.cmd += ') VALUES('

        for tag in self.dict:
            self.cmd += '"' + self.dict[tag]  + '",'
        self.cmd = self.cmd[:-1]
        self.cmd += ')'

        return super().command()

###############################################################################
class SqlBuilderUpdate(SqlBuilder):

    def __init__(self, table):
        SqlBuilder.__init__(self, table, Type.UPDATE)

    def set(self, tag, value):
        if -1 == self.cmd.find('SET'):
            self.cmd += ' SET "' + tag + '" = "' + str(value) + '"'
            
    def where(self, condition):
        if self.cmd.find('SET') > 0 and -1 == self.cmd.find('WHERE'):
            self.cmd += ' WHERE ' + condition
            
###############################################################################
class SqlBuilderSelect(SqlBuilder):

    def __init__(self, table, what):
        SqlBuilder.__init__(self, table, Type.SELECT)
        self.cmd += what + ' FROM ' + self.table

    def where(self, condition):
        if -1 == self.cmd.find('WHERE'):
            self.cmd += ' WHERE ' + condition
            

if __name__ == '__main__':
    #conn = sqlite3.connect(args.db_path + 'server0.db')
    #cur = conn.cursor()
    cur = 0

    provider = 2

    try:
        sql = SqlBuilderCreate('local')
        sql.addInt('id')
        sql.addText('tag')
        sql.addText('desc')
        sql.addText('desc2')
        sql.addInt('variant')
        sql.addInt('alarm')
        sql.addInt('prio')
        sql.addInt('alarm_txt')
        sql.addInt('renv0')
        sql.addInt('renv1')
        sql.addInt('renv2')
        sql.addInt('renv3')
        sql.addInt('renv4')
        sql.addInt('store')
        sql.addInt('textpro')
        print(sql.command())

        sql = SqlBuilderDrop('provider')
        print(sql.command())

        sql = SqlBuilderInsert('local')
        sql.add('tag', 'blegns_{}_stm')
        sql.add('desc', '{} - Mode d''exploitation')
        sql.add('desc2', '{}')
        sql.add('variant', 1)
        sql.add('renv0', 255)
        sql.add('renv1', 5)
        sql.add('texpro', 1)
        print(sql.command())

        sql = SqlBuilderUpdate('provider')
        sql.set('providerNbSubId', 'toto')
        sql.where('providerType={}'.format(provider))
        print(sql.command())
        
        sql = SqlBuilderSelect('provider', 'providerNbSubId')
        sql.where('providerType={}'.format(provider))
        print(sql.command())

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

    #os.system("pause")