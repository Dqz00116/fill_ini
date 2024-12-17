# fill_ini  
[![made-with-python](https://img.shields.io/badge/Made%20with-Python3-1f425f.svg)](https://www.python.org/) [![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)  

- [English](README.md)
- [中文](README.zh-CN.md)

`fill_ini` is a `.ini` configuration tool that allows you to quickly switch between different configurations for multiple `.ini` files using a JSON configuration file.

The core logic is implemented using *line-by-line reading* combined with *regular expression matching*, which supports modifying `.ini` files with duplicate keys, such as Unreal project configuration files.

## Usage Instructions  

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
                    "Mode2": "Value2"
                },
                "KeyName2": 1
            }
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
    "Mode": {
        "Mode1": 1,
        "Mode2": 2
    }
}
```

- **`Mode`**: The mode to switch to. Modes need to be defined in `enum_config.json`, and the enumeration name should be specified when using it.  
- **`Path`**: The path where the `.ini` files are located. Currently, only modifying multiple `.ini` files in a single path is supported.  
- **`Ini`**: The specific configuration parameters:  
    - **`FileName`**: The name of the `.ini` file.  
    - **`SectionName`**: The name of the section where key-value pairs need to be modified.  
    - **`KeyName`**: The key that needs to be modified.  
    - **`Mode`** *(optional)*: If multiple modes are defined as shown in the example, you can specify the corresponding value for each mode.  
