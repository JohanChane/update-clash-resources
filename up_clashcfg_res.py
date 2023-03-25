#!/usr/bin/env python3
# _*_ coding: UTF-8 _*_

import sys, os

def main():
    system = sys.platform
    home_dir = ''
    if system == 'win32':
        home_dir = os.environ['USERPROFILE']
        cfg_dir = os.path.join(home_dir, '.config/clash')
        script_path = os.path.abspath(os.path.dirname(os.path.realpath(__file__)))
        cmd = f'python {script_path}/update_clashcfg_res/update_clashcfg_res.py -d "{cfg_dir}" {" ".join(sys.argv[1:])}'
        os.system(cmd)
    else:
        home_dir = os.environ['HOME']
        cfg_dir = os.path.join(home_dir, '.config/clash')
        script_path = os.path.abspath(os.path.dirname(os.path.realpath(__file__)))
        cmd = f'python {script_path}/update_clashcfg_res/update_clashcfg_res.py -d "{cfg_dir}" {" ".join(sys.argv[1:])}'
        os.system(cmd)
        os.system('sudo systemctl restart clash')
    
        
if __name__ == '__main__':
    main()
