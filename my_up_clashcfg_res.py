#!/usr/bin/env python3
# _*_ coding: UTF-8 _*_

import sys, os

SCRIPT_PATH = os.path.abspath(os.path.dirname(os.path.realpath(__file__)))
PATH_OF_UPDATE_CLASHCFG_RES = os.path.join(SCRIPT_PATH, "update_clashcfg_res.py")
SC_HOST = r"sub.xeton.dev"

def main():
    system = sys.platform
    home_dir = ""
    if system == "win32":
        #home_dir = os.environ["USERPROFILE"]
        #cfg_dir = os.path.join(home_dir, ".config/clash")
        cfg_dir = r"D:\PortableProgramFiles\Clash.for.Windows\data"
        profile_dir = os.path.join(cfg_dir,  "profiles")
        cmd = f'python {PATH_OF_UPDATE_CLASHCFG_RES} -d "{cfg_dir}" -p "{profile_dir}" --is-cfw -P "https://127.0.0.1:7890" -t 5 -H {SC_HOST} {" ".join(sys.argv[1:])}'
        os.system(cmd)
    else:
        home_dir = os.environ["HOME"]
        cfg_dir = os.path.join(home_dir, ".config/clash_tun")
        profile_dir = cfg_dir
        cmd = f'python {PATH_OF_UPDATE_CLASHCFG_RES} -d "{cfg_dir}" -p "{profile_dir}" -T "/srv/clash" -t 5 -H {SC_HOST} {" ".join(sys.argv[1:])}' 
        os.system(cmd)
        os.system("sudo systemctl restart clash")
        
if __name__ == "__main__":
    main()
