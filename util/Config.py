import json
import os

class Config(object):
    def __init__(self):
        self.reload()
        pass

    # 获取配置项
    def get(self, key, module=''):
        if module == '':
            # 判断是否存在该Key
            if key in self.config:
                return str(self.config[key])
            else:
                return None
        else:
            # 判断是否存在module
            if module not in self.config:
                return None
            # 是否存在Key
            if key not in self.config[module]:
                return None

            return str(self.config[module][key])
        pass

    def set(self, key, value, module=''):
        if module == '':
            self.config[key] = value
        else:
            if module in self.config:
                self.config[module][key] = value
            else:
                self.config[module] = {
                    key: value
                }

        file = open('./config.json', 'w')
        json.dump(obj=self.config, fp=file, ensure_ascii=False, indent=4)
        pass

    # 从文件中读取配置对象
    def reload(self):
        configPath = './config.json'
        configFile = open(configPath, encoding='utf-8')
        self.config = json.load(configFile)
