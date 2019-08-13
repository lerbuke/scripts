#!/usr/bin/env python3
"""
"""
from intrans_ctools import check_file
from intrans_ctools import exec_cmd

if __name__ == '__main__':
    #exec_cmd("sed -i 's/errors=remount-ro/defaults,noatime,ro,errors=remount-ro/' /etc/fstab")
    #exec_cmd("sed -i 's/errors=remount-ro.*/defaults,noatime,ro,errors=remount-ro 0       1/'/etc/fstab")
    
    # Replace from matched string to EOL 
    exec_cmd("sed -i 's/errors=remount-ro.*/errors=remount-ro,defaults,noatime,ro 0       1/' sed_test_files/fstab")
      
      

