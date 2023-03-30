#!/usr/bin/env python3
# _*_ coding: UTF-8 _*_

"""
Update resources in clash configuration with proxy

Usage:
    update_clashcfg_res.py -d <cfg_dir> [[-c <cfg_rel_path>] | [-f <profile_path>] [-n <cfg_name>]] [-p <proxy>]

Options:
    -h --help                   Get help.
    -d <cfg_dir>                clash 的配置路径。
    -c <cfg_rel_path>           clash 的配置的相对路径。如果不指定则会选择 `profiles/list.yml` 所选的配置文件。
    -f <profile_path>           profiles 的绝对路径。如果不指定则是默认的 profile 路径。
    -n <cfg_name>               clash 的配置文件的名称。会根据 `profiles/list.yml` 的 `name` 所对应的配置文件。`name` 可以同名，所以要注意。
    -p <proxy>                  使用代理更新。比如：`-p https://127.0.0.1:7890`。
    -t <tun_dir>                将更新好的安装到该目录。
    -i <timeout>                连接的超时时间

Examples:
    # 更新 list 所选的配置的资源。当加载出错时，list 的 index 会是 -1，所以要在没有出错前，运行该程序。
    update_clashcfg_res.py -d 'C:/Users/johan/.config/clash' -p 'https://127.0.0.1:7890'
    # 更新 list 配置的 name 对应的配置的资源
    update_clashcfg_res.py -d 'C:/Users/johan/.config/clash' -n 'myconfig' -p 'https://127.0.0.1:7890'
    # 更新 `config.yaml` 配置的资源
    update_clashcfg_res.py -d 'C:/Users/johan/.config/clash' -c 'config.yaml' -p 'https://127.0.0.1:7890'
    # 非默认的 profile 路径
    update_clashcfg_res.py -d 'C:/Users/johan/.config/clash' -f 'C:/Users/johan/Desktop/profiles' -n 'config_mobile.yaml'
    # 更新 rule-providers
    update_clashcfg_res.py -d 'C:/Users/johan/.config/clash' -n 'myconfig' -p 'https://127.0.0.1:7890' -r
    # 将更新的文件安装到 tun_dir
    update_clashcfg_res.py -d 'C:/Users/johan/.config/clash' -n 'myconfig' -p 'https://127.0.0.1:7890' -t '/srv/clash'

"""

import sys, os, getopt, requests

import ruamel.yaml as rmyaml

def update_res(sections, cfg_dir, *, cfg_rel_path=None, profile_path=None, cfg_name=None, proxy=None, timeout=None):
    cfg_path, cfg_url = get_cfg_path(cfg_dir, profile_path, cfg_rel_path, cfg_name)
    
    session = requests.Session()
    session.headers.update({'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'})
    if proxy:
        protocol, address = proxy.split('://')
        session.proxies = {
            protocol: address
        }
    if timeout:
        session.timeout = timeout
    
    # 更新从 url 导入的配置
    if cfg_url:
        #response = session.get(cfg_url)
        with session.get(cfg_url) as response:
            with open(cfg_path, 'wb') as f:
                f.write(response.content)
        print(f'Updated cfg "{cfg_path}"')
        
    updated_res = []
    res = []
    for s in sections:
        res = get_net_res(cfg_path, [s])
        updated_res += update_net_res(session, res, s, cfg_dir)
    print(f'Updated resource(s) needed by "{cfg_path}"')
    return updated_res

def get_cfg_path(cfg_dir, profile_path=None, cfg_rel_path=None, cfg_name=None):
    yaml = rmyaml.YAML(typ='safe')

    cfg_path = ''
    cfg_url = ''
    if not cfg_rel_path:
        # ## 从 list.yml 中选择配置
        # ### 读取 list.yml
        if not profile_path:
            # 选择 profile 的默认路径
            profile_path = os.path.join(cfg_dir, './profiles')

        list_path = os.path.join(profile_path, './list.yml')
        if not os.path.exists(list_path):
            sys.stderr.write(f'list.yml: {list_path} isn\'t exist!\n')
            sys.exit(os.EX_USAGE)

        with open(list_path, 'r', encoding='utf-8') as f:
            list_data = yaml.load(f)

        # ### 如果指定 cfg_name 则使用 cfg_name 所对应的配置
        if cfg_name:
            for x in list_data['files']:
                if x['name'] == cfg_name:
                    cfg_path = os.path.join(cfg_dir, f'profiles/{x["time"]}')
                    cfg_url = x['url']
        # ### 如果没有指定 cfg_name 则当前选定的配置
        else:
            list_index = list_data['index']
            if list_index < 0:
                sys.stderr.write('Please select your profile.')
                sys.exit(os.EX_USAGE)
            cfg_rel_path = list_data['files'][list_index]['time']
            cfg_path = os.path.join(cfg_dir, 'profiles/' + cfg_rel_path)
            cfg_url = list_data['files'][list_index]['url']
    else:
        cfg_path = os.path.join(cfg_dir, cfg_rel_path)

    if not os.path.exists(cfg_path):
        sys.stderr.write(f'cfg_path: {cfg_path} isn\'t exists.')
        sys.exit(os.EX_USAGE)

    return cfg_path, cfg_url

def get_net_res(cfg_path, sections):
    # ## 加载 cfg
    yaml = rmyaml.YAML(typ='safe')
    with open(cfg_path, 'r', encoding='utf-8') as f:
        cfg_data = yaml.load(f)

    net_res = []
    for s in sections:
        # ## 取出 section 的数据
        s_data = cfg_data[s]

        # ## 将 type == 'http' 的项的 url 和 path 放入 net_res
        # network resource
        for i in s_data.values():
            if i['type'] == 'http':
                net_res.append([i['url'], i['path']])

    return net_res

def update_net_res(session, net_res, section, cfg_dir):
    # ## 下载 net_res 里的资源
    # 保存环境
    oldcwd = os.getcwd()
    os.chdir(cfg_dir)
    
    updated_res = []
    for i in net_res:
        dirpath = os.path.dirname(i[1])
        if not os.path.exists(dirpath):
            os.makedirs(dirpath)
        
        #response = session.get(i[0])
        with session.get(i[0]) as response:
            if section == 'proxy-providers':
                yaml_data = rmyaml.safe_load(response.content.decode('utf-8'))
                try:
                    yaml_data['proxies']
                except KeyError:
                    print(f'Updated failed: didn\'t write the content to "{i[1]}", for "{i[0]}" hasn\'t "proxies" key')
                    return updated_res

            with open(i[1], 'wb') as f:
                f.write(response.content)
            print(f'Updated successfully: {i[1]}, {i[0]}')
            updated_res.append(i)

    # 恢复环境
    os.chdir(oldcwd)

    return updated_res;

# net_res_files 的路径 src_cfg_dir 是相对路径
def install_proxy_providers(net_res_files, src_cfg_dir, dest_cfg_dir):
    for x in net_res_files:
        src_file = os.path.join(src_cfg_dir, x)
        dest_file = os.path.join(dest_cfg_dir, x)
        if not os.path.exists(os.path.dirname(dest_file)):
            os.system(f'sudo -u nobody mkdir -p {os.path.dirname(dest_file)}')
        os.system(f'sudo install -o nobody -g nobody -m 0644 {src_file} {dest_file}')

def usage():
    print(__doc__)

def main():
    # ## parse args
    try:
        opts, args = getopt.getopt(sys.argv[1:], 'd:c:f:n:p:i::t:rh', ['', '', '', '', '', 'help'])
    except getopt.GetoptError:
        usage()
        sys.exit(os.EX_USAGE)

    cfg_dir = None
    profile_path = None
    cfg_rel_path = None
    cfg_name = None
    proxy = None
    does_update_rules = False
    tun_dir = ''
    timeout = None

    for opt, arg in opts:
        if opt in ('-h', '--help'):
            usage()
            sys.exit()
        elif opt in ('-d'):
            cfg_dir = arg
        elif opt in ('-f'):
            profile_path = arg
        elif opt in ('-c'):
            cfg_rel_path = arg
        elif opt in ('-n'):
            cfg_name = arg
        elif opt in ('-p'):
            proxy = arg
        elif opt in ('-i'):
            timeout = arg
        elif opt in ('-r'):
            does_update_rules = True
        elif opt in ('-t'):
            tun_dir = arg
        else:
            usage()
            sys.exit(os.EX_USAGE)

    # ## 更新资源
    sections = ['proxy-providers']
    if does_update_rules:
        sections.append('rule-providers')
    net_res = update_res(sections, cfg_dir, cfg_rel_path=cfg_rel_path, profile_path=profile_path, cfg_name=cfg_name, proxy=proxy, timeout=timeout)
    if len(net_res) == 0:
        return -1

    if tun_dir:
        # ## updated files
        updated_files = [x[1] for x in net_res]

        # ## install updated files to <tun_dir>
        src_cfg_dir = cfg_dir
        dest_cfg_dir = tun_dir
        install_proxy_providers(updated_files, src_cfg_dir, dest_cfg_dir)
        print(f'Installed updated files {updated_files} from "{src_cfg_dir}" to "{dest_cfg_dir}"')

if __name__ == '__main__':
    main()
