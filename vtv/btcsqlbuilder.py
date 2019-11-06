#!/usr/bin/env python
"""
btcsqlbuilder.py

"""
import os, sys, traceback
from enum import Enum

sys.stderr = open('./cmds.txt', 'w', newline='\r\n')

"""
Base class that prepare the command string based on the type and tyble name
given in argument.
NOTE: There is non-sense to instantiate directly this class
(abstract class concept as in C++ doesn't exists) and we must instantiate only
derivated classes.
"""
class SqlBuilder:

    class Type(Enum):
     CREATE = 1
     DROP = 2
     INSERT = 3
     UPDATE = 4
     SELECT = 5

    # Ctor.
    def __init__(self, table, type):
        self.type = type
        self.table = table
        self.dict = {}
        if type == self.Type.CREATE:
            self.cmd = 'CREATE TABLE ' + table
        elif type ==  self.Type.DROP:
            self.cmd = 'DROP TABLE IF EXISTS ' + table
        elif type ==  self.Type.INSERT:
            self.cmd = 'INSERT INTO ' + table
        elif type ==  self.Type.UPDATE:
            self.cmd = 'UPDATE ' + table
        elif type ==  self.Type.SELECT:
            self.cmd = 'SELECT '

    # Returns the command string.
    def command(self):
        sys.stderr.write(self.cmd +'\n')
        return self.cmd

"""
Class that build a CREATE command string for a table with specific type fields.
Usage example:
    sql = SqlBluiderCreate('tableName')
    sql.addInt('id0') # add 'id0' field as INTEGER
    sql.addInt('id1', False, True) # add 'id1' field as INTEGER PRIMARY KEY
    sql.addInt('id2', primaryKey=True) # same as 'id1' field
    sql.addInt('id3', True, True) # add 'id3' field as INTEGER NOT NULL PRIMARY KEY
    sql.addInt(['riri', 'fifi', 'loulou']) # add these 3 fields as INTEGER
    sql.addText('t') # add 't' field as TEXT
    sql.addText(['t1', 't2']) # add these 2 fields as TEXT
    print(sql.command())

NOTE: take care with string value including apostrophe char ('): the string value must be given between "", like
      "Besoin d'air" or the apostrophe char must be escaped like 'Besoin d\'air'.
"""
class SqlBuilderCreate(SqlBuilder):

    # Ctor.
    def __init__(self, table):
        SqlBuilder.__init__(self, table, SqlBuilder.Type.CREATE)

    # Private member that append typed field(s) with specifics attributes (NOT NULL, PRIMARY KEY) to the command string.
    def __append(self, field, type, notNull=False, primaryKey=False):
        # Check arguments type. The field type is not checked.
        if isinstance(type, str) == False or isinstance(notNull, bool) == False or isinstance(primaryKey, bool) == False:
            raise('Bad parameter type.')

        # Create a field list.
        if isinstance(field, list):
            fields = field
        else:
            fields = [field]

        # Append each field with the NOT NUL attribute if set.
        for tag in fields:
            self.dict[tag] = type
            if notNull == True:
                self.dict[tag] += ' NOT NULL'

        # Append the primary key if set to the first entry only.
        if primaryKey == True:
            self.__primaryKey(fields[0])

    # Private method that append the primary key to the specified field only if not already exists in one other field of the dict.
    def __primaryKey(self, field):
        for key in self.dict:
            if -1 != self.dict[key].find('PRIMARY KEY'):
                raise('Primary key already exists.')
        self.dict[field] += ' PRIMARY KEY'

    # Public method to add a field of type TEXT.
    def addText(self, field, notNull=False, primaryKey=False):
        self.__append(field, 'TEXT', notNull, primaryKey)

    # Public method to add a field of type INTEGER.
    def addInt(self, field, notNull=False, primaryKey=False):
        self.__append(field, 'INTEGER', notNull, primaryKey)

    # Public method to add a field of type REAL.
    def addReal(self, field, notNull=False, primaryKey=False):
        self.__append(field, 'REAL', notNull, primaryKey)

    # Overrided method that finalize the build of the command string before calling the base method.
    def command(self):
        if len(self.dict) > 0:
            self.cmd += ' ('
            for field in self.dict:
                self.cmd += field + ' ' + self.dict[field] + ','
            self.cmd = self.cmd[:-1]
            self.cmd += ')'
        return super().command()


"""
Class that build a DROP command string for a table.
"""
class SqlBuilderDrop(SqlBuilder):

    # Ctor.
    def __init__(self, table):
        SqlBuilder.__init__(self, table, SqlBuilder.Type.DROP)

"""
Class that build an INSERT command string for a table.
Example:
    sql = SqlBuilderInsert('local')
    sql.add('tag', 'toto')
    sql.add('desc', 'Mode d\'exploitation')
    sql.add('desc2', 'De nuit')
    sql.add('variant', 1)
    sql.add('renv0', 255)
    sql.add('renv1', 5)
    sql.add('texpro', 1)
    print(sql.command())
"""
class SqlBuilderInsert(SqlBuilder):

    # Ctor.
    def __init__(self, table):
        SqlBuilder.__init__(self, table, SqlBuilder.Type.INSERT)

    # Add the key and its value in the dict.
    def add(self, field, value):
        if isinstance(value, str) == True:
            self.dict[field] = '"' + value + '"'
        else:
            self.dict[field] = '{}'.format(value)

    # Overrided method that finalize the build of the command string before calling the base method.
    def command(self):
        if len(self.dict) == 0:
            raise('Nothing to insert.')

        # Add field list
        self.cmd += ' ('
        for field in self.dict:
            self.cmd += field + ','
        self.cmd = self.cmd[:-1]

        # Add value list
        self.cmd += ') VALUES('
        for field in self.dict:
            self.cmd += self.dict[field] + ','
        self.cmd = self.cmd[:-1] + ')'

        return super().command()

"""
Class that build an UPDATE command string for a table.
Usage example:
    sql = SqlBuilderUpdate('provider')
    sql.set('providerNbSubId', 47)
    sql.where('providerType = 0')
    print(sql.command())
"""
class SqlBuilderUpdate(SqlBuilder):

    # Ctor.
    def __init__(self, table):
        SqlBuilder.__init__(self, table, SqlBuilder.Type.UPDATE)

    # Build the command string with the SET field and value.
    def set(self, field, value):
        if -1 == self.cmd.find('SET'):
            self.cmd += ' SET ' + field + ' = '
            if isinstance(value, str) == True:
                self.cmd += '"' + value + '"'
            else:
                self.cmd += '{}'.format(value)
        else:
            raise('SET already exists in the command string.')

    # Build the command string with the WHERE condition.
    def where(self, condition):
        if self.cmd.find('SET') > 0 and -1 == self.cmd.find('WHERE'):
            self.cmd += ' WHERE ' + condition
        else:
            raise('SET not exists yet or WHERE already in the command string.')

"""
Class that build an SELECT command string for a table.
Example:
    sql = SqlBuilderSelect('provider', 'providerNbSubId')
    sql.where('providerType={}'.format(provider))
    print(sql.command())
"""
class SqlBuilderSelect(SqlBuilder):

    # Ctor.
    def __init__(self, table, what):
        SqlBuilder.__init__(self, table, SqlBuilder.Type.SELECT)
        self.cmd += what + ' FROM ' + self.table

    # Build the command string with the WHERE condition.
    def where(self, condition):
        if -1 == self.cmd.find('WHERE'):
            self.cmd += ' WHERE ' + condition

"""
Main for basic tests.
"""
if __name__ == '__main__':
    provider = 2

    try:
        sql = SqlBuilderCreate('local')
        sql.addInt(['id', 'toto', 'tata'], True, True)
        sql.addText('field')
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
        sql.add('field', 'blegns_{}_stm'.format(10))
        sql.add('desc', '{} - Mode d\'exploitation'.format(121))
        sql.add('desc2', '{}'.format(32))
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