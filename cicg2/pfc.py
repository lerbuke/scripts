#! python3
import sys, os, pathlib
sys.path.insert(0, '')

os.chdir(pathlib.Path(__file__).parent)

from libpfc import Pfc


def main():
    bureau = Pfc('BUREAU', 240096, 17)
    bureau.create_analog_value_array(64, 0, 'VALEUR_BUS1_BALLAST', '', 'Valeur du bus 1 ballast', 98, 0, 100, 1)
    bureau.create_analog_value_array(64, 0, 'COMMANDE_BUS1_BALLAST', '', 'Commande pour le bus 1 ballast', 98, 0, 100, 1)
    bureau.create_multiple_value_array(64, 0, 'STATUT_BUS1_BALLAST', '', 'Statut du bus 1 ballast', ['ETEINT', 'ALLUME', 'SOURCE HS', 'BALLAST HS'])
    bureau.create_analog_value_array(64, 0, 'VALEUR_BUS2_BALLAST', '', 'Valeur du bus 1 ballast', 98, 0, 100, 1)
    bureau.create_analog_value_array(64, 0, 'COMMANDE_BUS2_BALLAST', '', 'Commande pour le bus 1 ballast', 98, 0, 100, 1)
    bureau.create_multiple_value_array(64, 0, 'STATUT_BUS2_BALLAST', '', 'Statut du bus 1 ballast', ['ETEINT', 'ALLUME', 'SOURCE HS', 'BALLAST HS'])
    bureau.create_analog_value_array(64, 0, 'VALEUR_BUS3_BALLAST', '', 'Valeur du bus 1 ballast', 98, 0, 100, 1)
    bureau.create_analog_value_array(64, 0, 'COMMANDE_BUS3_BALLAST', '', 'Commande pour le bus 1 ballast', 98, 0, 100, 1)
    bureau.create_multiple_value_array(64, 0, 'STATUT_BUS3_BALLAST', '', 'Statut du bus 1 ballast', ['ETEINT', 'ALLUME', 'SOURCE HS', 'BALLAST HS'])
    bureau.create_multiple_value('EXPLOITATION_CICG', '', 'Mode exploitation CICG', ['HORS EXPLOITATION', 'EN EXPLOITATION'])
    bureau.create_multiple_value('EXPLOITATION_AUDITORIUM_D', '', 'Mode exploitation Auditorium D', ['HORS EXPLOITATION', 'EN EXPLOITATION'])
    bureau.create_multiple_value('EXPLOITATION_AUDITORIUM_D_BIS', '', 'Mode exploitation Auditorium D bis', ['HORS EXPLOITATION', 'EN EXPLOITATION'])
    bureau.create_multiple_value('EXPLOITATION_SALLES_S1', '', 'Mode exploitation Salles -1', ['HORS EXPLOITATION', 'EN EXPLOITATION'])
    bureau.create_multiple_value('EXPLOITATION_SALLES_02', '', 'Mode exploitation Salles +2', ['HORS EXPLOITATION', 'EN EXPLOITATION'])
    bureau.create_multiple_value('EXPLOITATION_SALLES_03', '', 'Mode exploitation Salles +3', ['HORS EXPLOITATION', 'EN EXPLOITATION'])
    bureau.create_multiple_value('EXPLOITATION_RESTAURANT', '', 'Mode exploitation Restaurant Violetta Parra', ['HORS EXPLOITATION', 'EN EXPLOITATION'])
    bureau.create_multiple_value('EXPLOITATION_VIP', '', 'Mode exploitation VIP', ['HORS EXPLOITATION', 'EN EXPLOITATION'])
    bureau.create_multiple_value('EXPLOITATION_WANGARI_MAATHAI', '', 'Mode exploitation Wangari Maathai', ['HORS EXPLOITATION', 'EN EXPLOITATION'])
    bureau.create_multiple_value('EXPLOITATION_NETTOYAGE', '', 'Mode exploitation Nettoyage', ['HORS EXPLOITATION', 'EN EXPLOITATION'])

    bureau.create_zone('ZONE_S1_ELLA_MAILLARD_1', 'Zone S1 Ella Maillard 1', ['AUTO', 'FORCE', 'COCKTAIL'],  ['Plafond', 'Bandeau'])
    bureau.create_zone('ZONE_S1_ELLA_MAILLARD_2', 'Zone S1 Ella Maillard 2', ['AUTO', 'FORCE'],  ['Plafond', 'Bandeau'])
    bureau.create_zone('ZONE_S1_ELLA_MAILLARD_3', 'Zone S1 Ella Maillard 3', ['AUTO', 'FORCE'],  ['Plafond', 'Bandeau'])
    bureau.create_zone('ZONE_S1_SALON', 'Zone S1 Salon', ['AUTO', 'FORCE'],  ['Plafond', 'Bandeau'])
    bureau.create_zone('ZONE_S1_ASCENSEURS', 'Zone S1 ASCENCEURS', ['AUTO', 'FORCE'],  ['Plafond', 'Bandeau'])

    bureau.create_zone('ZONE_00_SALON_BAR_LEMAN', 'Zone 00 Salon Bar Leman', ['AUTO', 'FORCE', 'COCKTAIL'],  ['Plafond', 'Bandeau'])
    bureau.create_zone('ZONE_00_BAR_LEMAN', 'Zone 00 Bar Leman', ['AUTO', 'FORCE', 'COCKTAIL'],  ['Plafond', 'Bandeau'])
    bureau.create_zone('ZONE_00_RUTH_DREIFUSS', 'Zone 00 Ruth Dreifuss', ['AUTO', 'FORCE'],  ['Plafond', 'Bandeau'])
    bureau.create_zone('ZONE_00_SALLE_6', 'Zone 00 Salle 6', ['AUTO', 'FORCE', 'SALLE'],  ['Plafond', 'Bandeau'])
    bureau.create_zone('ZONE_00_SALLE_7', 'Zone 00 Salle 7', ['AUTO', 'FORCE', 'SALLE'],  ['Plafond', 'Bandeau'])
    bureau.create_zone('ZONE_00_SALLE_8', 'Zone 00 Salle 8', ['AUTO', 'FORCE', 'SALLE'],  ['Plafond', 'Bandeau'])
    bureau.create_zone('ZONE_00_CIRCULATION_SALLES', 'Zone 00 Circulation Salles', ['AUTO', 'FORCE', 'SALLE'],  ['Plafond', 'Bandeau'])
    bureau.create_zone('ZONE_00_ACCEUIL', 'Zone 00 Acceuil', ['AUTO', 'FORCE', 'ETEINT'],  ['Plafond', 'Bandeau'])
    bureau.create_zone('ZONE_00_ESCALIERS', 'Zone 00 Escaliers', ['AUTO', 'FORCE'],  ['Plafond', 'Bandeau'])

    bureau.create_multiple_value('FORCAGE_S1', '', 'Zone eclairage forcee au niveau S1', ['INACTIF', 'ACTIF'])
    bureau.create_multiple_value('FORCAGE_00', '', 'Zone eclairage forcee au niveau 00', ['INACTIF', 'ACTIF'])
    bureau.create_multiple_value('FORCAGE_01', '', 'Zone eclairage forcee au niveau 01', ['INACTIF', 'ACTIF'])
    bureau.create_multiple_value('FORCAGE_02', '', 'Zone eclairage forcee au niveau 02', ['INACTIF', 'ACTIF'])
    bureau.create_multiple_value('FORCAGE_03', '', 'Zone eclairage forcee au niveau 03', ['INACTIF', 'ACTIF'])
    bureau.create_multiple_value('FORCAGE_CICG', '', 'Zone eclairage forcee au CICG', ['INACTIF', 'ACTIF'])

    bureau.create_multiple_value('METTRE_EN_AUTO', '', 'Mettre en Auto', ['ANNULER', 'APPLIQUER'])
    bureau.create_multiple_value('ETEINDRE_LE_CENTRE', '', 'Eteindre le centre', ['ANNULER', 'APPLIQUER'])

    bureau.create_notification_class('NOTIFICATION_CLASS_ALARM_0', '', [100, 100, 100],  [1, 1, 1]);

    bureau.create_binary_value_alarm('BUS1_DEFAUT_SOURCE', '', 'Defaut source lumineuse sur Bus DALI 1', 0, ['Defaut source lumineuse sur Bus DALI 1', '', 'Aucun defaut']);
    bureau.create_binary_value_alarm('BUS1_DEFAUT_BALLAST', '', 'Defaut ballast sur Bus DALI 1', 0, ['Defaut ballast sur Bus DALI 1', '', 'Aucun defaut']);
    bureau.create_binary_value_alarm('BUS2_DEFAUT_SOURCE', '', 'Defaut source lumineuse sur Bus DALI 2', 0, ['Defaut source lumineuse sur Bus DALI 2', '', 'Aucun defaut']);
    bureau.create_binary_value_alarm('BUS2_DEFAUT_BALLAST', '', 'Defaut ballast sur Bus DALI 2', 0, ['Defaut ballast sur Bus DALI 2', '', 'Aucun defaut']);

    bureau.create_multiple_value('COCKTAIL_S1', '', 'Zone eclairage en mode cocktail au niveau S1', ['INACTIF', 'ACTIF'])
    bureau.create_multiple_value('COCKTAIL_00', '', 'Zone eclairage en mode cocktail au niveau 00', ['INACTIF', 'ACTIF'])
    bureau.create_multiple_value('COCKTAIL_01', '', 'Zone eclairage en mode cocktail 01', ['INACTIF', 'ACTIF'])
    bureau.create_multiple_value('COCKTAIL_02', '', 'Zone eclairage en mode cocktail 02', ['INACTIF', 'ACTIF'])

    bureau.end()

if __name__ == '__main__':
    main()




