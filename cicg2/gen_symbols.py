#!/usr/bin/env python
"""
Automaticaly add a number of ballasts symbols for a list of buses for an automate identifed by name in the given xml file.
Usage:
    python gen_symbols.py -fn test.tgml -an BUREAU -bu "1,3" -ba 64
    
"""
import argparse, os

parser = argparse.ArgumentParser(description='Génération de symboles 100%.')
parser.add_argument('-fn', '--file_name', required=True, help='Nom du fichier')
parser.add_argument('-an', '--name', required=True, help='Nom de l\'automate')
parser.add_argument('-bu', '--buses', required=True, help='Liste des numéro de bus à générer')
parser.add_argument('-ba', '--ballasts', required=True, type=int, help='Nombre de ballast à générer par bus')


args = parser.parse_args()
print(args)


def add_items(fw, name, buses, ballasts):
    height = 13
    width = 34
    top = 10
    left = 10
    
    for bus in list(buses.split(",")):
        ballast = 0
        while ballast < ballasts:    
            fw.write('    <Component Clip="False"\n')
            fw.write('             ContentHeight="13"\n')
            fw.write('             ContentWidth="34"\n')
            fw.write('             Height="13.0"\n')
            fw.write('             Left="{}"\n'.format(left))
            fw.write('             Name="{}"\n'.format(name))
            fw.write('             Top="{}"\n'.format(top))
            fw.write('             Width="34.0">\n')
            fw.write('    <Rectangle Fill="#C0C0C0"\n')
            fw.write('                 Height="13"\n')
            fw.write('                 Left="0"\n')
            fw.write('                 Opacity="1.0"\n')
            fw.write('                 RadiusX="0.0"\n')
            fw.write('                 RadiusY="0.0"\n')
            fw.write('                 Stroke="#000000"\n')
            fw.write('                 StrokeDashArray="0.0"\n')
            fw.write('                 StrokeWidth="1.0"\n')
            fw.write('                 Top="0"\n')
            fw.write('                 Width="34">\n')
            fw.write('        <Bind Attribute="Fill"\n')
            fw.write('                DynamicUpdates="Enable"\n')
            fw.write('                Name="STATUT_BUS{}_BALLAST{}"\n'.format(bus, ballast))
            fw.write('                PreventDefault="True">\n')
            fw.write('            <ConvertValue AttributeValue="#E0E0E0"\n')
            fw.write('                            Name="GRIS"\n')
            fw.write('                            SignalEqualTo=""\n')
            fw.write('                            SignalLessThan=""/>\n')
            fw.write('            <ConvertValue AttributeValue="#FFFF00"\n')
            fw.write('                            Name="JAUNE"\n')
            fw.write('                            SignalEqualTo="2"/>\n')
            fw.write('            <ConvertValue AttributeValue="#FF0000"\n')
            fw.write('                            Name="ROUGE"\n')
            fw.write('                            SignalEqualTo="4"/>\n')
            fw.write('            <ConvertValue AttributeValue="#BEB078"\n')
            fw.write('                            Name="BRUN"\n')
            fw.write('                            SignalEqualTo="3"/>\n')
            fw.write('            <Expose ExposedAttribute="Name"\n')
            fw.write('                      Name="STATUS"/>\n')
            fw.write('        </Bind>\n')
            fw.write('    </Rectangle>\n')
            fw.write('    <Text Fill="None"\n')
            fw.write('            FontFamily="Arial"\n')
            fw.write('            FontSize="10"\n')
            fw.write('            FontStyle="Normal"\n')
            fw.write('            FontWeight="Normal"\n')
            fw.write('            HorizontalAlign="Center"\n')
            fw.write('            Left="17"\n')
            fw.write('            Opacity="1.0"\n')
            fw.write('            Stroke="#000000"\n')
            fw.write('            TextDecoration="None"')
            fw.write('            Top="1"\n')
            fw.write('            VerticalAlign="Top"><![CDATA[100 %]]><Bind Attribute="Fill"\n')
            fw.write('                Name="VALEUR_BUS{}_BALLAST{}"\n'.format(bus, ballast))
            fw.write('                PreventDefault="True">\n')
            fw.write('            <Script Name="s1"\n')
            fw.write('                      OnDocumentLoad="load"\n')
            fw.write('                      OnMouseMove=""\n')
            fw.write('                      OnSignalChange="signal"><![CDATA[function load(evt)\n')
            fw.write('{\n')
            fw.write('  text = evt.getTarget().getParentNode();\n')
            fw.write('  output = text.getAttribute("Label");\n')
            fw.write('  if(output != "")\n')
            fw.write('    output += " ";\n')
            fw.write('  output += "-- " + text.getAttribute("Unit");\n')
            fw.write('  text.setAttribute("Content", output);\n')
            fw.write('}\n')
            fw.write('\n')
            fw.write('function leftPad(number, targetLength) {\n')
            fw.write('    var output = number + \'\';\n')
            fw.write('    while (output.length < targetLength) {\n')
            fw.write('        output = \'0\' + output;\n')
            fw.write('    }\n')
            fw.write('    return output;\n')
            fw.write('}\n')
            fw.write('\n')
            fw.write('function signal(evt)\n')
            fw.write('{\n')
            fw.write('  text = evt.getTarget().getParentNode();\n')
            fw.write('\n')
            fw.write('  output = "";\n')
            fw.write('\n')
            fw.write('  //alert(evt.getValue());\n')
            fw.write('\n')
            fw.write('  label = text.getAttribute("Label");\n')
            fw.write('  if(label != "")\n')
            fw.write('    output = label + " ";\n')
            fw.write('\n')
            fw.write('  decimals = 0;\n')
            fw.write('\n')
            fw.write('  value = new Number(evt.getValue());\n')
            fw.write('\n')
            fw.write('  switch(evt.getStatus())\n')
            fw.write('  {\n')
            fw.write('    case 0: // Bad quality\n')
            fw.write('      output += "--";\n')
            fw.write('      text.setAttribute("TextDecoration", "None");\n')
            fw.write('      break;\n')
            fw.write('    case 1: // Stored value, uncertain quality\n')
            fw.write('      output += leftPad(value.toFixed(decimals), 3);\n')
            fw.write('      text.setAttribute("TextDecoration", "StrikeThrough");\n')
            fw.write('      break;\n')
            fw.write('    default: // Good quality\n')
            fw.write('      output += leftPad(value.toFixed(decimals), 3);\n')
            fw.write('      text.setAttribute("TextDecoration", "None");\n')
            fw.write('      break;\n')
            fw.write('  }\n')
            fw.write('\n')
            fw.write('  unit = "%";\n')
            fw.write('  if(unit != "")\n')
            fw.write('    output += " " + unit;\n')
            fw.write('\n')
            fw.write('  text.setAttribute("Content", output);\n')
            fw.write('}]]></Script>\n')
            fw.write('            <Expose ExposedAttribute="Name"\n')
            fw.write('                      Name="VALUE"/>\n')
            fw.write('        </Bind>\n')
            fw.write('    </Text>\n')
            fw.write('    <Bind Name="COMMANDE_BUS{}_BALLAST{}">\n'.format(bus, ballast))
            fw.write('        <Expose ExposedAttribute="Name"\n')
            fw.write('                  Name="COMMANDE"/>\n')
            fw.write('    </Bind>\n')
            fw.write('</Component>\n')
            
            ballast=ballast+1
            top = top + height + 10
            if top > 700:
                top = 10
                left = left + width + 10


KEY = "</Layer>"
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
        found = index+1
        break
    index+=1
fw.close()

if found > 0:
    with open (args.file_name,"r") as inp:
        with open ("_"+args.file_name,"w") as ou:
            for a,d in enumerate(inp.readlines()):
                if a==found:
                    add_items(ou, args.name, args.buses, args.ballasts)
                ou.write(d)

    os.remove(args.file_name)
    os.rename("_"+args.file_name, args.file_name)
else:
    print("Scheme id not found.");

