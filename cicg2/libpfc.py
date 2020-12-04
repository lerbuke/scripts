#!/usr/bin/env python
"""

"""
from datetime import datetime, timezone

def create_pfc(name, id, fw):
    utc = datetime.utcnow();
    
    #print(utc.strftime('%Y-%m-%dT%H:%M:%S%Z'))
    fw.write('<?xml version="1.0" encoding="utf-8"?>\n')
    fw.write('<wagoDevice deviceType="750-8212" firmwareIndex="18" copyright="" formatVersion="0.4" creationTool="WagoCfgEngine" creationDateTime="2020-12-03T19:35:48+01:00" creationUtcDateTime="{}" userVersion="" userID="" userComment="" persistency="1">\n'.format(utc.strftime('%Y-%m-%dT%H:%M:%S')))
    fw.write('  <objLst>\n')
    
    fw.write('  </objLst>\n')
    fw.write('  <cliMapSet />\n')
    fw.write('  <objNameMap />\n')
    fw.write('  <ptp />\n')
    fw.write('  <MultiControllerSettings />\n')
    fw.write('</wagoDevice>\n')
    return 0
    
def create_analog_value(pfc, name, desc, unit, min, max, increment):
    return 0
    
    
def create_analog_value_array(pfc, name, nb, start, desc, unit, min, max, increment):
    return 0
    
def create_multiple_value(pfc, name):#, [desc0, desc1, desc2]):
    return 0
    
def create_multiple_value_array(pfc, name, nb, start):#, [desc0, desc1, desc2]):
    return 0
    
    
def end_pfc(pfc):
    return 0
  