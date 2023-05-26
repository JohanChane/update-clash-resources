# Update resources in clash configuration

## 说明

通过代理更新 Clash 配置的网络资源, 所以前提是可以翻墙后, 再使用该工具。通常是有一个可以翻墙的 Clash 配置, 再使用该工具。

写这个工具的原因:

-   [Clash 更新这些资源是不走代理的。](https://github.com/Dreamacro/clash/issues/2368)
-   [[Feature] 让providers可以通过代理来更新](https://github.com/Dreamacro/clash/issues/2046)
-   [windows11 error](https://github.com/Fndroid/clash_for_windows_pkg/issues/2384)
-   [[Feature] rule-providers 和 proxy-providers 能不能提供选择直连或代理选项](https://github.com/Dreamacro/clash/issues/1385)

太多以上的之类的问题了。

## update_clashcfg_res

### Requires

平台: `Linux/Windows`

依赖: 

```sh
pip install ruamel.yaml requests
```

## 安装和使用

```sh
git clone https://github.com/JohanChane/update-clash-resources.git --depth 1
cd update-clash-resources/update_clashcfg_res
python ./update_clashcfg_res.py -h
```

## Examples

更新 Windows 平台的 Clash for Windows 的配置:

```PowerShell
# 更新 list 所选的配置的资源。当加载出错时，list 的 index 会是 -1，所以要在没有出错前，运行该程序。
update_clashcfg_res.py -d 'C:/Users/johan/.config/clash' -f 'C:/Users/johan/.config/clash/profiles' -p 'https://127.0.0.1:7890' --is_cfw -n 'config.yaml' -r
```

更新 Linux 平台的 Clash 的配置:

```sh
update_clashcfg_res.py -d ~/.config/clash -f ~/.config/clash -p 'https://127.0.0.1:7890' -n 'config.yaml' -r
update_clashcfg_res.py -d ~/.config/clash -f ~/.config/clash -p 'https://127.0.0.1:7890' -n 'config.yaml' -u '<url>' -r
update_clashcfg_res.py -d ~/.config/clash -f ~/.config/clash -p 'https://127.0.0.1:7890' -n 'config.yaml' -u '$(cat ~/.config/clash_tun/config_url)' -r
```

更新 Linux 平台的 Clash Tun 的配置:

```sh
# 将更新的文件安装到 tun_dir
update_clashcfg_res.py -d 'C:/Users/johan/.config/clash' -n 'myconfig' -p 'https://127.0.0.1:7890' -t '/srv/clash' -r
```

## `update_clashcfg_res` 的进阶用法

### my_up_clashcfg_res.py

该脚本的作用: 使用 `update_clashcfg_res` 时需要输入太多的参数, 而通常每次参数都是一样的, 所以可以在该脚本可以设置一些自己常用的参数。
是会使用 `cfg_dir` 的默认位置更新资源。

比如: [my_up_clashcfg_res.py](./my_up_clashcfg_res.py)

```sh
# In Linux
./my_up_clashcfg_res.py -n config.yaml -r

# In Windows
python ./my_up_clashcfg_res.py -n config.yaml -r
```

## IccRes

[IccRes](https://github.com/JohanChane/IccRes)