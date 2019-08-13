#!/usr/bin/env python3
"""
Collection of intransigent tools (means that the application is exited on error)
"""
import os, sys, subprocess



# check if 'file' exists, exit if not the case.
def check_file(file):
    if not os.path.exists(file):
        sys.stderr.write('ERROR: \'' + file + '\' not found in the system.\n')
        exit(-1)
        
# Execute a given command, exit if status not in the list of accepted return codes, else return the returned code.

def exec_cmd(cmd, accepted_return_codes=[0]):
    try:
        print('\n\n > > > > ', cmd, '\n^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^')
        output = ''
        process = subprocess.Popen(cmd, shell=True, stderr=subprocess.PIPE)

        while True:
            out = process.stderr.readline()
            if out == b'' and process.poll() != None:
                break
            if out != b'':
                output = out.decode(sys.stdout.encoding)
                sys.stdout.write(output)
                sys.stdout.flush()

        if process.returncode not in accepted_return_codes:
            print('Returned code', process.returncode, 'is not in accepted return code list', accepted_return_codes, '.')
            exit(process.returncode)

        return process.returncode
        
    except KeyboardInterrupt as ke:
        sys.stdout.write('\nABORTED BY USER {}\n'.format(str(ke)))
        sys.stdout.flush()
        exit(-1)
        
    except Exception as e:
        sys.stdout.write('\nEXCEPTION status: {}\n'.format(str(e)))
        sys.stdout.flush()
        exit(-1)
    
if __name__ == '__main__':
    exec_cmd('dir')
    exec_cmd('git status', [128])
    exec_cmd('dir /w')   