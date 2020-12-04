#!/usr/bin/env python
"""
"""
from libpfc import Pfc

import os

  
def main():
       
    pfc = Pfc('BUREAU', 240096, 18)
    pfc.create_analog_value_array(64, 0, 'VALEUR_BUS1_BALLAST', '', 'Valeur du bus 1 ballast', 98, 0, 100, 1)
    pfc.create_analog_value_array(64, 0, 'COMMANDE_BUS1_BALLAST', '', 'Commande pour le bus 1 ballast', 98, 0, 100, 1)
    pfc.create_multiple_value_array(64, 0, 'STATUT_BUS1_BALLAST', '', 'Statut du bus 1 ballast', ['ETEINT', 'ALLUME', 'SOURCE HS', 'BALLAST HS'])
    pfc.create_analog_value_array(64, 0, 'VALEUR_BUS2_BALLAST', '', 'Valeur du bus 1 ballast', 98, 0, 100, 1)
    pfc.create_analog_value_array(64, 0, 'COMMANDE_BUS2_BALLAST', '', 'Commande pour le bus 1 ballast', 98, 0, 100, 1)
    pfc.create_multiple_value_array(64, 0, 'STATUT_BUS2_BALLAST', '', 'Statut du bus 1 ballast', ['ETEINT', 'ALLUME', 'SOURCE HS', 'BALLAST HS'])
    pfc.create_analog_value_array(64, 0, 'VALEUR_BUS3_BALLAST', '', 'Valeur du bus 1 ballast', 98, 0, 100, 1)
    pfc.create_analog_value_array(64, 0, 'COMMANDE_BUS3_BALLAST', '', 'Commande pour le bus 1 ballast', 98, 0, 100, 1)
    pfc.create_multiple_value_array(64, 0, 'STATUT_BUS3_BALLAST', '', 'Statut du bus 1 ballast', ['ETEINT', 'ALLUME', 'SOURCE HS', 'BALLAST HS'])
    pfc.end()
    
if __name__ == '__main__':
    main()    