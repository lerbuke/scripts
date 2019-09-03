#!/usr/bin/env python3
"""
"""
from intrans_ctools import check_file
from intrans_ctools import exec_cmd

if __name__ == '__main__':
    sub = [
        's/font-size:14px/font-size:11px/g',
        's/font-size:17px/font-size:11px/g',
        's/line-height:31px/line-height:20px/g',
        's/line-height:32px/line-height:22px/g',
        's/line-height:42px/line-height:32px/g',
        's/height:31px/height:20px/g',
        's/height:32px/height:22px/g',
        's/height:42px/height:32px/g',
        's/top:14px/top:10px/g',
        's/top:13px/top:8px/g',
        's/font-family:Roboto,Arial,Helvetica/font-family:Verdana/g'
        ]
    
    FILEPATH = "server_www_ok/dhtmlx/skins/material/dhtmlx.css"
    BACK_FILEPATH = "server_www_ok/dhtmlx/skins/material/original_dhtmlx.css"
    
    exec_cmd("cp " + FILEPATH + " " + BACK_FILEPATH)
    cmd = "sed "
    for s in sub:
        cmd += "-e '" + s + "' "
    cmd += BACK_FILEPATH + " > " + FILEPATH
    
    exec_cmd(cmd)
