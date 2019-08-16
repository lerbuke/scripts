#!/usr/bin/env python
"""
Automaticaly add lamps symbols in .fxd files, usually edited within the FlexEdit application.
"""
import argparse, os

parser = argparse.ArgumentParser(description='Génération de lampes pour expo.')
parser.add_argument('-fn', '--file_name', required=True, help='Nom du fichier y compris l''extension .fxd')
parser.add_argument('-sid', '--scheme_id', required=True, help='Identifiant du schéma dans lequel les symboles de lampes seront générés')
parser.add_argument('-s', '--start_value', required=True, type=int, help='Adresse de départ du premier cadre de symbole de lampes (PDI)')
parser.add_argument('-st', '--start_cmd_value', required=True, type=int, help='Adresse de départ de commande (PDO)')
parser.add_argument('-c', '--count_value', required=True, type=int, help='Nombre de symboles à générer')

args = parser.parse_args()
print(args)


def add_items(fw):
    k = args.start_value
    kCmd = args.start_cmd_value
    top = 0
    left = 0
    index = 1
    while k < args.start_value + (2*args.count_value) :

        fw.write("    object Group: TFlexGroup\n")
        fw.write("      Height = 55000\n")
        fw.write("      Layer = Layer2\n")
        fw.write("      Left = {}\n".format(left))
        fw.write("      Top = {}\n".format(top))
        fw.write("      Width = 85500\n")

        # Cadre externe
        fw.write("    object Picture: TFlexPicture\n")
        fw.write("      FrameIndex = 0\n")
        fw.write("      Height = 55000\n")
        fw.write("      ID = 1064\n")
        fw.write("      Layer = Layer1\n")
        fw.write("      Left = 0\n")
        fw.write("      property Picture\n")
        fw.write("       Graphic = { }\n")
        fw.write("       LinkName = imghw2\\cadre_expo.gif\n")
        fw.write("      end\n")
        fw.write("      Top = 0\n")
        fw.write("      Width = 85500\n")
        fw.write("    end\n")

        # Cadre ballast
        fw.write("      object {}:TFlexMultiPicControl\n".format(k))
        fw.write("      AutoSize = True\n")
        fw.write("      FrameIndex = 0\n")
        fw.write("      Height = 14000\n")
        fw.write("      IsError = False\n")
        fw.write("      Layer = Layer2\n")
        fw.write("      Left = 52750\n")
        fw.write("      property Picture\n")
        fw.write("        Graphic = { }\n")
        fw.write("        LinkName = imghw2\\rect_gris.gif\n")
        fw.write("      end\n")
        fw.write("      Top = 21500\n")
        fw.write("      UserData = (\n")
        fw.write("        'URL1=imghw2\\rect_jaune.gif'\n")
        fw.write("        'URL2=imghw2\\rect_brun.gif'\n")
        fw.write("        'URL3=imghw2\\rect_rouge.gif' )\n")
        fw.write("      Width = 28000\n")
        fw.write("      end\n")

        # Ballast
        fw.write("      object {}: TFlexMyText\n".format(k+1))
        fw.write("      AutoSize = True\n")
        fw.write("     property Font\n")
        fw.write("        Charset = 0\n")
        fw.write("        Color = -2147483640\n")
        fw.write("        Name = Verdana\n")
        fw.write("        Size = 8000\n")
        fw.write("        Style = [fsBold]\n")
        fw.write("      end\n")
        fw.write("      Height = 13000\n")
        fw.write("      IsError = False\n")
        fw.write("      Layer = Layer2\n")
        fw.write("      Left = 54750\n")
        fw.write("      Text = (\n")
        fw.write("        '000' )\n")
        fw.write("        Top = 21500\n")
        fw.write("        UserData = (\n")
        fw.write("        'FORMAT=%03.0f')\n")
        fw.write("        Width = 24000\n")
        fw.write("      end\n")

        # Command conf
        fw.write("      object {}: TFlexMyText\n".format(kCmd))
        fw.write("      AutoSize = True\n")
        fw.write("      property Font\n")
        fw.write("        Charset = 0\n")
        fw.write("        Color = -2147483640\n")
        fw.write("        Name = Verdana\n")
        fw.write("        Size = 8000\n")
        fw.write("        Style = [fsBold]\n")
        fw.write("      end\n")
        fw.write("      Height = 13000\n")
        fw.write("      ID = 1054\n")
        fw.write("      IsError = False\n")
        fw.write("      Layer = Layer1\n")
        fw.write("      Left = 54500\n")
        fw.write("      Text = (\n")
        fw.write("        '000' )\n")
        fw.write("      Top = 38000\n")
        fw.write("      UserData = (\n")
        fw.write("        'FORMAT=%03.0f'\n")
        fw.write("        'CLICK=1' )\n")
        fw.write("      Width = 24000\n")
        fw.write("      end\n")

        fw.write("      object bidon1: TFlexText\n")
        fw.write("      AutoSize = True\n")
        fw.write("      property Font\n")
        fw.write("        Charset = 0\n")
        fw.write("        Color = -2147483640\n")
        fw.write("        Name = Verdana\n")
        fw.write("        Size = 8000\n")
        fw.write("        Style = [fsBold]\n")
        fw.write("      end\n")
        fw.write("      Height = 13000\n")
        fw.write("      ID = 1055\n")
        fw.write("      Layer = Layer1\n")
        fw.write("      Left = 3750\n")
        fw.write("      Text = (\n")
        fw.write("        'CONF' )\n")
        fw.write("      Top = 38000\n")
        fw.write("      Width = 34000\n")
        fw.write("      end\n")

        fw.write("      object bidon2: TFlexText\n")
        fw.write("      AutoSize = True\n")
        fw.write("      property Font\n")
        fw.write("        Charset = 0\n")
        fw.write("        Color = -2147483640\n")
        fw.write("        Name = Verdana\n")
        fw.write("        Size = 8000\n")
        fw.write("       Style = [fsBold]\n")
        fw.write("      end\n")
        fw.write("      Height = 13000\n")
        fw.write("      ID = 1056\n")
        fw.write("      Layer = Layer1\n")
        fw.write("      Left = 3750\n")
        fw.write("      Text = (\n")
        fw.write("        'ETAT' )\n")
        fw.write("      Top = 20000\n")
        fw.write("      Width = 33000\n")
        fw.write("      end\n")

        fw.write("      object label: TFlexText\n")
        fw.write("      AutoSize = True\n")
        fw.write("      property Font\n")
        fw.write("        Charset = 0\n")
        fw.write("        Color = -2147483640\n")
        fw.write("        Name = Verdana\n")
        fw.write("        Size = 8000\n")
        fw.write("        Style = [fsBold]\n")
        fw.write("      end\n")
        fw.write("      Height = 13000\n")
        fw.write("      ID = 1057\n")
        fw.write("      Layer = Layer1\n")
        fw.write("      Left = 3750\n")
        fw.write("      Text = (\n")
        fw.write("        'LAMPE {}' )\n".format(index))
        fw.write("      Top = 3000\n")
        fw.write("      Width = 54000\n")
        fw.write("      end\n")

        fw.write("    end\n")

        index = index + 1
        k=k+2
        kCmd = kCmd + 1
        if (index-1) % 10 == 0:
            top = top + 60000
            left = 0
        else:
            left = left + 90000



# document
#   object Layer1: TFlexLayer
#   end
#   ...
#   object Layern: TFlexLayer
#   end
#   object number: TFlexScheme
#       object Object1: (TFlexMultiPicControl | TFlexMyText | TFlexPicture)
#       end
#       ...
#       object Objectn: (TFlexMultiPicControl | TFlexMyText | TFlexPicture)
#       end
#   end
# end
# Append to existing file

KEY = "object " + args.scheme_id + ": TFlexScheme"
try:
    fw = open(args.file_name, "r")
except IOError as e:
   print("I/O error({0}): {1}".format(e.errno, e.strerror))
   exit()
except: #handle other exceptions such as attribute errors
   print("Unexpected error:", sys.exc_info()[0])
   exit()

index = 0
found = 0
for line in fw:
    line.strip().split('\n')
    if KEY in line:
        if (KEY == "object"):
            found = index
            break
        KEY = "object"
    index+=1
fw.close()

if found > 0:
    with open (args.file_name,"r") as inp:
        with open ("_"+args.file_name,"w") as ou:
            for a,d in enumerate(inp.readlines()):
                if a==found:
                    add_items(ou)
                ou.write(d)

    os.remove(args.file_name)
    os.rename("_"+args.file_name, args.file_name)
else:
    print("Scheme id not found.");

