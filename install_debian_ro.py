#!/usr/bin/env python
"""
"""
import os, sys, subprocess
import argparse
from pathlib import Path

parser = argparse.ArgumentParser(description='Configuration debian en RO')
parser.add_argument('-addr', '--address', default='192.168.1.192', help='IP Address')
parser.add_argument('-nw', '--network', default='192.168.1.0', help='Network')
parser.add_argument('-brd', '--broadcast', default='192.168.1.255', help='Broadcast')
parser.add_argument('-ns', '--nameserver', default='192.168.1.1', help='Name Server')
parser.add_argument('-nm', '--netmask', default='255.255.255.0', help='NetMask')
parser.add_argument('-gw', '--gateway', default='192.168.1.1', help='Gateway')
parser.add_argument('-all', action='store_true', help='Install all')
parser.add_argument('-core', action='store_true', help='Core installation')
parser.add_argument('-chrome', action='store_true', help='Install Google Chrome Web Browser')
parser.add_argument('-maria', action='store_true', help='Install MariaDB')
parser.add_argument('-net', action='store_true', help='Network installation')
parser.add_argument('-samba', action='store_true', help='Install Samba')
parser.add_argument('-webmin', action='store_true', help='Install Webmin')
args = parser.parse_args()
print(args)

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

def install_read_only_core():
    exec_cmd("apt-get -y install man autoconf libtool ftp gcc make ntp bzip2 xz-utils pkg-config zlib1g-dev g++ patch rsync git cmake sudo openssh-server busybox-syslogd vim net-tools")
    exec_cmd("apt-get -y remove --purge triggerhappy anacron dbus dphys-swapfile xserver-common lightdm libx11* rsyslog doc-debian-fr doc-linux-fr-text wamerican aspell")
    exec_cmd("git config --global core.editor vim")
    exec_cmd("su --login btc -c 'git config --global core.editor vim'")
    
    # Replace set mouse=a by set mouse=r and add set paste.
    check_file("/usr/share/vim/vim80/defaults.vim")
    exec_cmd("sed -i '/set mouse=/ s/a/r/' /usr/share/vim/vim80/defaults.vim")
    exec_cmd("grep -q -F 'set paste' /usr/share/vim/vim80/defaults.vim || echo '\\nset paste' >> /usr/share/vim/vim80/defaults.vim")

    # PermitRootLogin=yes.
    check_file("/etc/ssh/sshd_config")
    exec_cmd("sed -i '/PermitRootLogin/ s/#PermitRootLogin prohibit-password/PermitRootLogin=Yes/' /etc/ssh/sshd_config")

    exec_cmd("systemctl restart ssh")

    # Change driftfile /var/lib/ntp/ntp.drift to driftfile /var/tmp/ntp.drift.
    check_file("/etc/ntp.conf")
    exec_cmd("sed -i '/driftfile/ s#/var/lib/ntp/ntp.drift#/var/tmp/ntp.drift#' /etc/ntp.conf")

    exec_cmd("rm -rf /var/lib/dhcp/ /var/run /var/spool /var/lock")
    exec_cmd("ln -s /tmp /var/lib/dhcp")
    exec_cmd("ln -s /tmp /var/run")
    exec_cmd("ln -s /tmp /var/spool")
    exec_cmd("ln -s /tmp /var/lock")

    exec_cmd("rm /var/lib/systemd/random-seed")
    exec_cmd("ln -s /tmp/random-seed /var/lib/systemd/random-seed")

    # add ExecStartPre=/bin/echo "" >/tmp/lstriprandom-seed after RemainAfterExit=yes in [Service]
    check_file("/lib/systemd/system/systemd-random-seed.service")
    exec_cmd("sed -i '/RemainAfterExit/ s#yes#yes\\nExecStartPre=/bin/echo \"\" >/tmp/lstriprandom-seed#' /lib/systemd/system/systemd-random-seed.service")

    # UUID=9bb21983-9189-4f16-b224-d07b0e63147f /               ext4    defaults,noatime,ro,errors=remount-ro 0       1
    # tmpfs           /tmp            tmpfs   nosuid,nodev         0       0
    # tmpfs           /var/log        tmpfs   nosuid,nodev         0       0
    # tmpfs           /var/tmp        tmpfs   nosuid,nodev         0       0
    check_file("/etc/fstab")
    #replace from 'errors=remount-ro to the EOL (other options, dump & pass) with 'errors=remount-ro,defaults,noatime,ro 0       1'
    exec_cmd("sed -i 's/errors=remount-ro.*/errors=remount-ro,defaults,noatime,ro 0       1/' /etc/fstab")
    exec_cmd("grep -q -F 'tmpfs           /tmp' /etc/fstab || echo 'tmpfs           /tmp            tmpfs   nosuid,nodev         0       0' >> /etc/fstab")
    exec_cmd("grep -q -F 'tmpfs           /var/log' /etc/fstab || echo 'tmpfs           /var/log        tmpfs   nosuid,nodev         0       0' >> /etc/fstab")
    exec_cmd("grep -q -F 'tmpfs           /var/tmp' /etc/fstab || echo 'tmpfs           /var/tmp        tmpfs   nosuid,nodev         0       0' >> /etc/fstab")

    exec_cmd("chmod a+rwx /tmp")

    check_file("/etc/sysctl.conf")

    # désactivation de ipv6 pour toutes les interfaces
    exec_cmd("sed -i '/net.ipv6.conf.all.disable_ipv6/d' /etc/resolv.conf") # remove the line that contains net.ipv6.conf.all.disable_ipv6
    exec_cmd("echo '\\nnet.ipv6.conf.all.disable_ipv6 = 1' >> /etc/sysctl.conf")

    # désactivation de l’auto configuration pour toutes les interfaces
    exec_cmd("sed -i '/net.ipv6.conf.all.autoconf/d' /etc/resolv.conf") # remove the line that contains net.ipv6.conf.all.autoconf
    exec_cmd("echo '\\nnnet.ipv6.conf.all.autoconf = 0' >> /etc/sysctl.conf")

    # désactivation de ipv6 pour les nouvelles interfaces (ex:si ajout de carte réseau)
    exec_cmd("sed -i '/net.ipv6.conf.default.disable_ipv6/d' /etc/resolv.conf") # remove the line that contains net.ipv6.conf.default.disable_ipv6
    exec_cmd("echo '\\nnet.ipv6.conf.default.disable_ipv6 = 1' >> /etc/sysctl.conf")

    # désactivation de l’auto configuration pour les nouvelles interfaces
    exec_cmd("sed -i '/net.ipv6.conf.default.autoconf/d' /etc/resolv.conf") # remove the line that contains net.ipv6.conf.default.autoconf
    exec_cmd("echo '\\nnet.ipv6.conf.default.autoconf = 0' >> /etc/sysctl.conf")

    check_file("/lib/systemd/system/systemd-tmpfiles-setup.service")
    exec_cmd("sed -i '/ExecStart/ s#$# --exclude-prefix=/var/lib --exclude-prefix=/var/spool#' /lib/systemd/system/systemd-tmpfiles-setup.service")



def install_network():
    # auto eth0
    # iface eth0 inet static
    # address 192.168.1.192
    # netmask 255.255.255.0
    # network 192.168.1.0
    # broadcast 192.168.1.255
    # gateway 192.168.1.254
    check_file("/etc/network/interfaces")
    exec_cmd("sed -i 's/allow-hotplug ens33/allow-hotplug ens33\\nauto ens33/' /etc/network/interfaces")
    exec_cmd("sed -i 's/dhcp/static\\n\\taddress " + args.address + "\\n\\tnetmask " + args.netmask + "\\n\\tnetwork " + args.network + "\\n\\tbroadcast " + args.broadcast + "\\n\\tgateway " + args.gateway + "\\n/' /etc/network/interfaces")

    # nameserver 192.168.1.254
    check_file("/etc/resolv.conf")
    exec_cmd("sed -i '/nameserver*/d' /etc/resolv.conf") # remove the line that contains nameserver
    exec_cmd("echo '\\nnameserver " + args.nameserver + "' >> /etc/resolv.conf")


def install_chrome():
    exec_cmd("apt-get update")
    exec_cmd("apt-get -y install xfonts-base xserver-xorg-input-all xinit xserver-xorg xserver-xorg-video-all chromium chromium-l10n fonts-liberation2 fonts-dejavu-core xfonts-100dpi xfonts-75dpi x11-touchscreen-calibrator psmisc")
    exec_cmd("rm -rf /root/.config/chromium")
    exec_cmd("mkdir -p /root/.config")
    exec_cmd("ln -s /tmp/chromium /root/.config/chromium")

    check_file("/etc/X11/Xsession")
    exec_cmd("sed -i '/ERRFILE=/ s#$HOME#/tmp#' /etc/X11/Xsession")

    exec_cmd("echo '#! /bin/sh' > /etc/init.d/startx")
    exec_cmd("echo '\n### BEGIN INIT INFO'  >> /etc/init.d/startx")
    exec_cmd("echo '# Provides:          startx'  >> /etc/init.d/startx")
    exec_cmd("echo '# Required-Start:    $remote_fs $network'  >> /etc/init.d/startx")
    exec_cmd("echo '# Required-Stop:     $remote_fs'  >> /etc/init.d/startx")
    exec_cmd("echo '# Default-Start:     2 3 4 5'  >> /etc/init.d/startx")
    exec_cmd("echo '# Default-Stop:'  >> /etc/init.d/startx")
    exec_cmd("echo '# Short-Description: startx'  >> /etc/init.d/startx")
    exec_cmd("echo '### END INIT INFO'  >> /etc/init.d/startx")
    exec_cmd("echo '\n# Carry out specific functions when asked to by the system'  >> /etc/init.d/startx")
    exec_cmd("echo 'case \"$1\" in'  >> /etc/init.d/startx")
    exec_cmd("echo '  start)'  >> /etc/init.d/startx")
    exec_cmd("echo '    echo \"Starting startx \"'  >> /etc/init.d/startx")
    exec_cmd("echo '    export XAUTHORITY=\"/tmp/.Xauthority\"'  >> /etc/init.d/startx")
    exec_cmd("echo '    /usr/bin/startx /root/start &'  >> /etc/init.d/startx")
    exec_cmd("echo '    ;;'  >> /etc/init.d/startx")
    exec_cmd("echo '  stop)'  >> /etc/init.d/startx")
    exec_cmd("echo '    echo \"Stopping startx\"'  >> /etc/init.d/startx")
    exec_cmd("echo '    /usr/bin/killall Xorg'  >> /etc/init.d/startx")
    exec_cmd("echo '    ;;'  >> /etc/init.d/startx")
    exec_cmd("echo '  *)'  >> /etc/init.d/startx")
    exec_cmd("echo '    echo \"Usage: /etc/init.d/startx {start|stop}\"'  >> /etc/init.d/startx")
    exec_cmd("echo '    exit 1'  >> /etc/init.d/startx")
    exec_cmd("echo '    ;;'  >> /etc/init.d/startx")
    exec_cmd("echo 'esac'  >> /etc/init.d/startx")
    exec_cmd("echo '\nexit 0'  >> /etc/init.d/startx")

    exec_cmd("chmod 755 /etc/init.d/startx")
    exec_cmd("update-rc.d startx defaults")

    exec_cmd("echo 'xrandr --output Virtual1 --mode 1280x1024' > /root/start")
    exec_cmd("echo 'sleep 10' >> /root/start")
    exec_cmd("echo 'rm -rf /tmp/chromium' >> /root/start")
    exec_cmd("echo 'mkdir -p /tmp/chromium' >> /root/start")
    exec_cmd("echo 'chromium --no-sandbox --no-proxy-server --incognito --app=https://google.com --disable-session-crashed-bubble --kiosk' >> /root/start")
    exec_cmd("echo 'rm -rf /tmp/chromium' >> /root/start")
    exec_cmd("echo '#chromium --no-sandbox --no-proxy-server --incognito --start-fullscreen --app=https://google.com --disable-session-crashed-bubble' >> /root/start")
    exec_cmd("chmod u+x /root/start")

def install_mariadb():
    exec_cmd("sudo apt-get -y install mariadb-server")
    if not Path("/var/lib/mysql").is_symlink():
        exec_cmd("systemctl stop mariadb")
        exec_cmd("mv /var/lib/mysql /data", [0,1])
        exec_cmd("ln -s /data/mysql /var/lib/mysql", [0,1])
        exec_cmd("systemctl start mariadb")

    check_file("/etc/mysql/mariadb.conf.d/50-server.cnf")
    exec_cmd("sed -i '/bind-address/ s/127.0.0.1/0.0.0.0/' /etc/mysql/mariadb.conf.d/50-server.cnf")

def install_samba():
    exec_cmd("apt-get -y install samba")

    # printing = bsd
    if 1 == exec_cmd("grep -q -F 'printing = bsd' /etc/samba/smb.conf", [0,1]):
        exec_cmd("sed -i '/\[global\]/a    printing = bsd' /etc/samba/smb.conf")

    # printcap name = /dev/null
    if 1 == exec_cmd("grep -q -F 'printcap name = /dev/null' /etc/samba/smb.conf", [0,1]):
        exec_cmd("sed -i '/printing = bsd/a    printcap name = /dev/null' /etc/samba/smb.conf")

    # log level = 0
    if 1 == exec_cmd("grep -q -F 'log level = 0' /etc/samba/smb.conf", [0,1]):
        exec_cmd("sed -i '/Accounting ####/a    log level = 0' /etc/samba/smb.conf")

    # Comment log file =
    exec_cmd("sed -e '/log file =/  s/^#*/#/' /etc/samba/smb.conf")

    exec_cmd("sed -i '/Share Definitions/,$d' /etc/samba/smb.conf") # Remove all from Share Definitions line to EOF

    if 1 == exec_cmd("grep -q -F '[data]' /etc/samba/smb.conf", [0,1]):
        exec_cmd("echo '[data]' >> /etc/samba/smb.conf")
        exec_cmd("echo '   comment = Some useful files' >> /etc/samba/smb.conf")
        exec_cmd("echo '   read only = no' >> /etc/samba/smb.conf")
        exec_cmd("echo '   locking = no' >> /etc/samba/smb.conf")
        exec_cmd("echo '   path = /data' >> /etc/samba/smb.conf")
        exec_cmd("echo '   guest ok = yes' >> /etc/samba/smb.conf")
        exec_cmd("echo '   force user = root' >> /etc/samba/smb.conf")
        exec_cmd("echo '   force group = root' >> /etc/samba/smb.conf")

    exec_cmd("rm -rf /var/lib/samba/")
    exec_cmd("ln -s /tmp /var/lib/samba")

    exec_cmd("rm -rf /var/cache/samba/")
    exec_cmd("ln -s /tmp /var/cache/samba")

    exec_cmd("systemctl disable nmbd.service")

    check_file("/lib/systemd/system/smbd.service")
    exec_cmd("sed -i '/ExecStart=/i ExecStartPre=/bin/mkdir -p /var/lib/samba/private' /lib/systemd/system/smbd.service")


def install_webmin():
    exec_cmd("apt-get -y install perl libnet-ssleay-perl openssl libauthen-pam-perl libpam-runtime libio-pty-perl apt-show-versions python")
    exec_cmd("wget http://prdownloads.sourceforge.net/webadmin/webmin_1.890_all.deb")
    exec_cmd("dpkg --install webmin_1.890_all.deb")
    exec_cmd("rm -f webmin_1.890_all.deb")
    exec_cmd("rm /var/webmin/miniserv.error")
    exec_cmd("ln -s /tmp/miniserv.error /var/webmin/miniserv.error")

def main():
#global init
    exec_cmd("mount -n -o remount,rw /")
    exec_cmd("apt-get update")
    exec_cmd("apt-get upgrade -y")
    exec_cmd("apt-get dist-upgrade")
#eng global init

    if args.all:
        args.core = args.net = args.chrome = args.maria = args.samba = args.webmin = True

    if args.core:
        install_read_only_core()

    if args.net:
        install_network()

    if args.maria:
        install_mariadb()

    if args.samba:
        install_samba()

    if args.webmin:
        install_webmin()

    if args.chrome:
        install_chrome()

#global cleanup

    exec_cmd("systemctl disable apt-daily.timer")
    exec_cmd("systemctl disable apt-daily-upgrade.timer")
    exec_cmd("systemctl disable apt-daily.service")
    exec_cmd("systemctl disable apt-daily-upgrade.service")
    exec_cmd("systemctl disable cron.service")

    exec_cmd("rm -f /etc/cron.weekly/man-db")
    exec_cmd("rm -f /etc/cron.daily/man-db")
    exec_cmd("rm -f /etc/cron.daily/bsdmainutils")
    exec_cmd("rm -f /etc/cron.daily/apt*")
    exec_cmd("rm -f /etc/cron.daily/passwd")
    exec_cmd("rm -f /etc/cron.daily/dpkg")
    exec_cmd("rm -f /etc/cron.daily/exim*")
    
    exec_cmd("apt-get -y autoremove")
    exec_cmd("apt-get -y autoremove --purge")
    exec_cmd("apt-get clean")
    exec_cmd("apt-get autoclean")

#end global cleanup

if __name__ == '__main__':
    main()
