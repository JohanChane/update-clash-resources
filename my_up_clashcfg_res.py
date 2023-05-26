#!/usr/bin/env python3
# _*_ coding: UTF-8 _*_

import sys, os

SCRIPT_PATH = os.path.abspath(os.path.dirname(os.path.realpath(__file__)))
PATH_OF_UPDATE_CLASHCFG_RES = os.path.join(SCRIPT_PATH, "update_clashcfg_res.py")

def main():
    system = sys.platform
    home_dir = ""
    if system == "win32":
        home_dir = os.environ["USERPROFILE"]
        cfg_dir = os.path.join(home_dir, ".config/clash")
        profile_dir = os.path.join(cfg_dir,  "profiles")
        cmd = f'python {PATH_OF_UPDATE_CLASHCFG_RES} -d "{cfg_dir}" -f "{profile_dir}" --is_cfw -p "https://127.0.0.1:7890" -i 5 {" ".join(sys.argv[1:])}'
        os.system(cmd)
    else:
        home_dir = os.environ["HOME"]
        cfg_dir = os.path.join(home_dir, ".config/clash_tun")
        profile_dir = cfg_dir
        cmd = f'python {PATH_OF_UPDATE_CLASHCFG_RES} -d "{cfg_dir}" -f "{profile_dir}" -t "/srv/clash" -i 5 {" ".join(sys.argv[1:])}'
        os.system(cmd)
        os.system("sudo systemctl restart clash")
        
if __name__ == "__main__":
    main()
