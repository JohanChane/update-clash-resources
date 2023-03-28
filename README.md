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

### 常用用法

```sh
## In Windows
# 更新当前使用的配置的资源
python ./update_clashcfg_res.py -d 'C:/Users/<user>/.config/clash' -p 'https://127.0.0.1:7890'
# 更新名为 `config.yaml` 配置的资源
python ./update_clashcfg_res.py -d 'C:/Users/<user>/.config/clash' -n 'config.yaml' -p 'https://127.0.0.1:7890'

## In Linux
# 更新 `<cfg_dir>/config.yaml` 配置的资源
./update_clashcfg_res.py -d '/home/<user>/.config/clash' -c 'config.yaml' -p 'https://127.0.0.1:7890'
```

## `update_clashcfg_res` 的进阶用法

### up_clashcfg_res.py

该脚本的作用: 使用 `update_clashcfg_res` 时需要输入太多的参数, 而通常每次参数都是一样的, 所以可以在该脚本可以设置一些自己常用的参数。
是会使用 `cfg_dir` 的默认位置更新资源。

```sh
# Clash for Windows in Windows. cfg_dir 的参数是 `-d C:/Users/<user>/.config/clash`
python ./up_clashcfg_res.py -n "config.yaml" -p "https://127.0.0.1:7890"
# Clash in Linux. cfg_dir 的参数是 `-d ~/.config/clash`
python ./up_clashcfg_res.py -c "config.yaml" -p "https://127.0.0.1:7890"
```

如果想添加更多的默认值, 可以这样改:

```sh
cmd = f'python {script_path}/update_clashcfg_res/update_clashcfg_res.py -d "{cfg_dir}" <在此处添加更多的默认值> {" ".join(sys.argv[1:])}'

# for example
cmd = f'python {script_path}/update_clashcfg_res/update_clashcfg_res.py -d "{cfg_dir}" -n "config.yaml" -p "https://127.0.0.1:7890" {" ".join(sys.argv[1:])}'
```

比如我在 Windows 上使用 `Clash for Windows`, 在 Linux 上使用 `clash tun`。所以这个脚本我会改成这样 [my_up_clashcfg_res.py](./my_up_clashcfg_res.py)。

```sh
# In Linux
./my_up_clashcfg_res.py -c config.yaml -r

# In Windows
python ./my_up_clashcfg_res.py -n config.yaml -r
```

## IccRes

[IccRes](https://github.com/JohanChane/IccRes)
