import time
import threading
from colorama import  init,Fore,Back,Style
import os
import sys
import json
import keyboard
import configparser
def log(text, end='\n'):
    print(f'[~] ' + text, end=end)
def success(text, end='\n'):
    print(f'{Fore.GREEN}[+] ' + text, end=end)
def error(text, end='\n'):
    print(f'{Fore.RED}[-] ' + text, end=end)
def cls():
    os.system('cls' if os.name == 'nt' else 'clear')
if __name__ == "__main__":
    config = {}
    init(autoreset=True)
    nowtime = int(time.strftime("%H", time.localtime()))
    if nowtime < 12:
        t = '上午'
    elif nowtime < 18:
        t = '下午'
    else:
        t = '晚上'
    log("——————————————")
    log(Fore.GREEN + t + f'好，旅行者。')
    log(f'{Fore.YELLOW}现在是' + time.strftime("%H:%M:%S", time.localtime()) + '。')
    log("正在检测环境……")
    if os.path.exists('config.json'):
        with open('config.json','r',encoding='utf-8') as f:
            config = f.read()
            if config == '':
                log("配置文件为空，正在创建配置文件……")
                with open('config.json','w',encoding='utf-8') as f:
                    result = {
                        "server": '0.0.0.0',
                        "port": 12345,
                        "game": '',
                        "mongodb": '',
                        "gc": '',
                        "game_version": ''
                    }
                    f.write(json.dumps(result))
                success("配置文件创建成功，请重新启动程序。")
                log('程序将在5秒后退出。')
                time.sleep(5)
                sys.exit()
            else:
                config = json.loads(config)
                success("检测完成。")
                time.sleep(2)
                cls()
                success('准备就绪。')
                success('服务器监听地址:' + config['server'])
                success('服务器监听端口:' + str(config['port']))
                success('游戏路径:' + config['game'])
                success('MongoDB端口:' + config['mongodb'])
                success('游戏版本:' + config['game_version'])
                time.sleep(2)
                cls()
                log('正在启动服务器……')

                # 配置检测
                if config['game'] == '':
                    error('游戏路径为空，请先配置游戏路径。')
                    gamepath = input('[~] 请输入游戏路径(YuanShen.exe所在的文件夹 末尾要带\)：')
                    if gamepath == '':
                        error('游戏路径不能为空！')
                        error('程序将在3秒后退出。')
                        time.sleep(3)
                        sys.exit()
                    else:
                        with open('config.json','r',encoding='utf-8') as f:
                            config = json.loads(f.read())
                            config['game'] = gamepath
                            with open('config.json','w',encoding='utf-8') as f:
                                f.write(json.dumps(config))
                        success('游戏路径已配置，重启程序生效。')
                        error('程序将在3秒后退出。')
                        time.sleep(3)
                        sys.exit()
                elif config['mongodb'] == '':
                    error('MongoDB端口为空！')
                    mongodbpath = input('[~] 请输入MongoDB 端口(n: 默认配置)：')
                    if mongodbpath == 'n':
                        success('已跳过，即将使用默认配置: 27017')
                        with open('config.json','r+',encoding='utf-8') as f:
                            config = json.loads(f.read())
                            config['mongodb'] = '27017'
                            with open('config.json','w',encoding='utf-8') as f:
                                f.write(json.dumps(config))
                        success('MongoDB端口已配置，重启程序生效。')
                        pass
                    else:
                        with open('config.json','r+',encoding='utf-8') as f:
                            config = json.loads(f.read())
                            config['mongodb'] = mongodbpath
                            with open('config.json','w',encoding='utf-8') as f:
                                f.write(json.dumps(config))
                        success('MongoDB端口已配置，重启程序生效。')
                        error('程序将在3秒后退出。')
                        time.sleep(3)
                        sys.exit()
                elif config['gc'] == '':
                    error('割草机路径为空！')
                    gcpath = input('[~] 请输入割草机路径(n: 自动下载)：')
                    if gcpath == 'n':
                        success('已跳过，即将下载割草机。')
                        download_gc()
                    else:
                        with open('config.json','r+',encoding='utf-8') as f:
                            config = json.loads(f.read())
                            config['gc'] = gcpath
                            with open('config.json','w',encoding='utf-8') as f:
                                f.write(json.dumps(config))
                        success('割草机路径已配置，重启程序生效。')
                        error('程序将在3秒后退出。')
                        time.sleep(3)
                        sys.exit()
                elif config['game_version'] == '':
                    log('正在获取游戏版本……')
                    configa = configparser.ConfigParser()
                    configa.read(config['game'] + 'config.ini')
                    game_version = configa.get('general', 'game_version')
                    success('游戏版本获取成功。')
                    with open('config.json','r+',encoding='utf-8') as f:
                        config = json.loads(f.read())
                        config['game_version'] = game_version
                        with open('config.json','w',encoding='utf-8') as f:
                            f.write(json.dumps(config))
                    success('游戏版本：' + game_version)

                # 配置检测完成
                else:
                    success('配置检测完成。')
                    time.sleep(1)
                    success('正在启动游戏服务器……')

                    time.sleep(1)
                    success('游戏已启动。')
                    time.sleep(1)
                    success('正在连接MongoDB……')
                    time.sleep(1)


                    


    else:
        log("正在创建配置文件……")
        with open('config.json','w',encoding='utf-8') as f:
            result = {
                "server": '0.0.0.0',
                "port": 12345,
                "game": '',
                "mongodb": '',
                "gc": '',
                "game_version": ''
            }
            f.write(json.dumps(result))
        success("配置文件创建成功，请重新启动程序。")
        error('程序将在3秒后退出。')
        time.sleep(3)
        sys.exit()













"""
                                                                                       ██                
                                                                                   ██                
                                                                                   ██                
                                                                                   ██                
                                                                                   ███               
                                                                                  ████               
                                                                                  ████               
            █                                             █                       █████              
           ██                                             ██                     ██████              
          ████                                           ███                    ████████             
        ████████                                       ████████               ████████████           
     █████████████████████████████████████████████████████████████         ██████████████████        
        █████████             ████                     ███████                  ████████             
         ███████            ███████                      ███   ██                 ████               
         ███████  ███████     ████     ███████            █████████  ███████      ███      ████████  
         ███████  █████████████████████████████  ███████████████████ ████████████████████████████████
         ███████  ███████              ███████   ██████ █████████████████████     ████     ████████  
         ███████  ███████              ███████   ██████ ██████       ████████    ███████   ████████  
         ███████  ████████████████████ ███████   ██████ ██████ ████  ██████████████████████████████  
         ███████  ███████              ███████   ██████ ████████████ ██████████████████████████████  
         ███████  ███████              ███████   ██████ ██████ █████ ████████   ████████   ████████  
        ████████  ████████████████████████████   ██████ ██████ █████ ████████     █████    ████████  
        ███████   ██████     ███████   ███████   ██████ ██████ █████ ██████████████████████████████  
        ███████   ██         ███████             ██████ ██████ ████  ██████████████████████████████  
        ██████      █████    ███████   ██████    █████  ██████ ███   ███████      ████      ███████  
       ██████  █████████████ ███████ █████████████████  ██████       ████        ██████        ████  
      █████  ██████████████  ██████  ████████████████   ██████                ████████████           
     █████   ██████          ███████         ███████    ██████              ████████████████         
    ███        ████          ██████          ████       ██████                 ██████████            
  █                  ████    ██████     ███             █████                   ████████             
                             ████                       ████                     ██████              
                             ██                         ██                       ██████              
                                                                                  ████               
                                                                                  ████               
                                                                                  ████               
                                                                                   ███               
                                                                                   ██                
                                                                                   ██                
                                                                                   ██                
                                                                                   ██                
                                                                                   ██                
                                                                                   ██                
"""