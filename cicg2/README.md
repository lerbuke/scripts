# Scripts CICG2

Pour générer les bus avec leur ballasts pour un automate dans un fichier existant, on utilise le scripts gen_symbols.py.

Exemple d'utlisation: 
On désire générer dans le fichier test.tgml 3 bus avec 64 ballasts par bus pour un automate nommé AUTOMATE.

```
C:\>python gen_symbols.py -fn test.tgml -an MON_AUTOMATE -bu 3 -ba 64
Namespace(file_name='test.tgml', name='MON_AUTOMATE', buses=3, ballasts=64)
```

