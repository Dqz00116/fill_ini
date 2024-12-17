# fill_ini
[![made-with-python](https://img.shields.io/badge/Made%20with-Python3-1f425f.svg)](https://www.python.org/) [![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

- [English](README.md)
- [中文](README.zh-CN.md)

`fill_ini` 是一个`.ini`配置工具，通过配置json文件可以对多个`.ini`文件快捷切换不同的配置。

核心逻辑使用 逐行读取 + 正则表达式匹配 的方式实现，支持修改存在重复Key的`.ini`文件，例如虚幻项目的配置配置文件。

## 使用说明

```json
// config.json
{
    "Mode": "Mode1",
    "Path": "",
    "Ini": {
        "FileName1": {
            "SectionName1": {
                "KeyName1": {
                    "Mode1": "Value1",
                    "Mode2": "Value2",
                },
                "KeyName2": 1
        },
        "FileName2": {
            "SectionName2": {
                ...
            }
        }
    }
}
```
```json
// enum_config.json
{
    "Mode" : {
        "Mode1" : 1,
        "Mode2" : 2
    }
}
```

- `Mode`: 切换的模式，模式需要在`enum_config.json`中定义，使用时填写枚举名
- `Path`: `.ini`文件所在的路径，目前只支持修改单个路径下的多个`.ini`文件
- `Ini` : 具体的配置参数
    - `FileName`: `.ini`文件的名称
    - `SectionName`: 需要修改键值对的节的名称 
    - `KeyName`: 需要修改的键
    - `Mode`(可选的): 如果按照示例中的格式定义了多个Mode，可以指定不同Mode下对饮的值
