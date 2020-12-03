#!/usr/bin/env python
"""
Automaticaly add 100% symbols in the given xml file.
"""
import argparse, os

parser = argparse.ArgumentParser(description='Génération de symboles 100%.')
parser.add_argument('-fn', '--file_name', required=True, help='Nom du fichier')
parser.add_argument('-c', '--count_value', required=True, type=int, help='Nombre de symboles à générer')

args = parser.parse_args()
print(args)


def add_items(fw):
    k = 0
    top = 10
    left = 10
    height = 13
    width = 34
    while k < args.count_value:    
        fw.write('    <Component Clip="False"')
        fw.write('             ContentHeight="13"')
        fw.write('             ContentWidth="34"')
        fw.write('             Height="13.0"')
        fw.write('             Left="{}"'.format(left))
        fw.write('             Name="ADUPLIQUER"')
        fw.write('             Top="{}"'.format(top))
        fw.write('             Width="34.0">')
        fw.write('    <Rectangle Fill="#C0C0C0"')
        fw.write('                 Height="13"')
        fw.write('                 Left="0"')
        fw.write('                 Opacity="1.0"')
        fw.write('                 RadiusX="0.0"')
        fw.write('                 RadiusY="0.0"')
        fw.write('                 Stroke="#000000"')
        fw.write('                 StrokeDashArray="0.0"')
        fw.write('                 StrokeWidth="1.0"')
        fw.write('                 Top="0"')
        fw.write('                 Width="34">')
        fw.write('        <Bind Attribute="Fill"')
        fw.write('                DynamicUpdates="Enable"')
        fw.write('                Name="STATUS_B1_1"')
        fw.write('                PreventDefault="True">')
        fw.write('            <ConvertValue AttributeValue="#E0E0E0"')
        fw.write('                            Name="GRIS"')
        fw.write('                            SignalEqualTo=""')
        fw.write('                            SignalLessThan=""/>')
        fw.write('            <ConvertValue AttributeValue="#FFFF00"')
        fw.write('                            Name="JAUNE"')
        fw.write('                            SignalEqualTo="2"/>')
        fw.write('            <ConvertValue AttributeValue="#FF0000"')
        fw.write('                            Name="ROUGE"')
        fw.write('                            SignalEqualTo="4"/>')
        fw.write('            <ConvertValue AttributeValue="#BEB078"')
        fw.write('                            Name="BRUN"')
        fw.write('                            SignalEqualTo="3"/>')
        fw.write('            <Expose ExposedAttribute="Name"')
        fw.write('                      Name="STATUS"/>')
        fw.write('        </Bind>')
        fw.write('    </Rectangle>')
        fw.write('    <Text Fill="None"')
        fw.write('            FontFamily="Arial"')
        fw.write('            FontSize="10"')
        fw.write('            FontStyle="Normal"')
        fw.write('            FontWeight="Normal"')
        fw.write('            HorizontalAlign="Center"')
        fw.write('            Left="17"')
        fw.write('            Opacity="1.0"')
        fw.write('            Stroke="#000000"')
        fw.write('            TextDecoration="None"')
        fw.write('            Top="1"')
        fw.write('            VerticalAlign="Top"><![CDATA[100 %]]><Bind Attribute="Fill"')
        fw.write('                Name="VALUE_B1_1"')
        fw.write('                PreventDefault="True">')
        fw.write('            <Script Name="s1"')
        fw.write('                      OnDocumentLoad="load"')
        fw.write('                      OnMouseMove=""')
        fw.write('                      OnSignalChange="signal"><![CDATA[function load(evt)')
        fw.write('{')
        fw.write('  text = evt.getTarget().getParentNode();')
        fw.write('  output = text.getAttribute("Label");')
        fw.write('  if(output != "")')
        fw.write('    output += " ";')
        fw.write('  output += "-- " + text.getAttribute("Unit");')
        fw.write('  text.setAttribute("Content", output);')
        fw.write('}')
        fw.write('')
        fw.write('function leftPad(number, targetLength) {')
        fw.write('    var output = number + '';')
        fw.write('    while (output.length < targetLength) {')
        fw.write('        output = '0' + output;')
        fw.write('    }')
        fw.write('    return output;')
        fw.write('}')
        fw.write('')
        fw.write('function signal(evt)')
        fw.write('{')
        fw.write('  text = evt.getTarget().getParentNode();')
        fw.write('  ')
        fw.write('  output = "";')
        fw.write('  ')
        fw.write('  //alert(evt.getValue());')
        fw.write('  ')
        fw.write('  label = text.getAttribute("Label");')
        fw.write('  if(label != "")')
        fw.write('    output = label + " ";')
        fw.write('  ')
        fw.write('  decimals = 0;')
        fw.write(' ')
        fw.write('  value = new Number(evt.getValue());')
        fw.write('')
        fw.write('  switch(evt.getStatus())')
        fw.write('  {')
        fw.write('    case 0: // Bad quality')
        fw.write('      output += "--";')
        fw.write('      text.setAttribute("TextDecoration", "None");')
        fw.write('      break;')
        fw.write('    case 1: // Stored value, uncertain quality')
        fw.write('      output += leftPad(value.toFixed(decimals), 3);')
        fw.write('      text.setAttribute("TextDecoration", "StrikeThrough");')
        fw.write('      break;')
        fw.write('    default: // Good quality')
        fw.write('      output += leftPad(value.toFixed(decimals), 3);')
        fw.write('      text.setAttribute("TextDecoration", "None");')
        fw.write('      break;')
        fw.write('  }')
        fw.write('  ')
        fw.write('  unit = "%";')
        fw.write('  if(unit != "")')
        fw.write('    output += " " + unit;')
        fw.write('   ')
        fw.write('  text.setAttribute("Content", output);')
        fw.write('}]]></Script>')
        fw.write('            <Expose ExposedAttribute="Name"')
        fw.write('                      Name="VALUE"/>')
        fw.write('        </Bind>')
        fw.write('    </Text>')
        fw.write('    <Bind Name="COMMANDE_B1_1">')
        fw.write('        <Expose ExposedAttribute="Name"')
        fw.write('                  Name="COMMANDE"/>')
        fw.write('    </Bind>')
        fw.write('</Component> ')
        
        k=k+1
        top = top + height + 10
        if top > 100:
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

