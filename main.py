from tqdm import tqdm
import zipfile
import time
import threading
from colorama import  init,Fore,Back,Style
import os
import sys
import json
import keyboard
import configparser
import requests
import re
import subprocess
import webbrowser
def log(text, end='\n'):
    print(f'[~] ' + text, end=end)
def success(text, end='\n'):
    print(f'{Fore.GREEN}[+] ' + text, end=end)
def error(text, end='\n'):
    print(f'{Fore.RED}[-] ' + text, end=end)
def ask(text, end='\n'):
    print(f'{Fore.YELLOW}[?] ' + text, end=end)
def warn(text, end='\n'):
    print(f'{Fore.YELLOW}[!] ' + text, end=end)
def cls():
    os.system('cls' if os.name == 'nt' else 'clear')
def download_gc():
    cls()
    log("即将开始下载服务端")
    log("正在获取版本列表……")
    gamelist = []
    request = requests.get('https://raw.githubusercontent.com/CTCAKE/GC-Tools/refs/heads/main/gamelist.json')
    if request.status_code == 200:
        gamelist = json.loads(request.text)
        log("请选择游戏版本：")
        for i in range(len(gamelist)):
            log(str(i+1) + '. ' + gamelist[i]['version'])
        game_version = input("请输入游戏版本编号：")
        if game_version.isdigit():
            game_version = int(game_version)
            if game_version > 0 and game_version <= len(gamelist):
                log('已选择游戏版本：' + gamelist[game_version-1]['version'])
                if config['game_version'] != gamelist[game_version-1]['version']:
                    ask(f'选择的服务端版本({gamelist[game_version-1]['version']})与您的游戏版本({config['game_version']})不一致，是否继续？(y/n)')
                    i = input()
                    if i == 'y':
                        request = requests.get('https://raw.githubusercontent.com/CTCAKE/GC-Tools/refs/heads/main/reslist.json')
                        if request.status_code == 200:
                            reslist = json.loads(request.text)
                            success('res文件较大，请前往网盘自行下载！')
                            success('下载链接:' + reslist[game_version-1]['url'])
                            success('下载完成后，请将文件移动至gc文件夹中。')
                            warn('请不要重命名文件。')
                            s = '.'
                            while os.path.exists('gc/res_' + gamelist[game_version-1]['version'] + '.zip') == False:
                                s += '.'
                                log('等待文件' + s, end='\r')
                                time.sleep(1)
                            success('已检测到文件，正在解压！')
                            zip_path = 'gc/res_' + gamelist[game_version-1]['version'] + '.zip'
                            extract_path = 'gc/' + gamelist[game_version-1]['version'] + '/res'
                            if os.path.exists(extract_path) == False:
                                os.mkdir(extract_path)
                            #with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                                #zip_ref.extractall(extract_path)
                            success('解压完成！')
                            with open('config.json','w',encoding='utf-8') as f:
                                config['gc'] = 'gc/'
                                f.write(json.dumps(config))
                            log('配置文件已更新！')
                            time.sleep(2)
                            cls()
                            log('——下载服务端——')
                            ask(f'请选择下载渠道(g[需魔法]/p[123盘]):')
                            i = input()
                            if i == 'g':
                                request = requests.get(gamelist[game_version-1]['url'], stream=True)
                                if request.status_code == 200:
                                    with open('gc/' + gamelist[game_version-1]['version'] + '.zip', 'wb') as f:
                                        log('正在下载服务端……')
                                        for chunk in request.iter_content(chunk_size=1024):
                                            if chunk:
                                                f.write(chunk)
                                                size = os.path.getsize('gc/' + gamelist[game_version-1]['version'] + '.zip')
                                                log(str(round(size/1024/1024,2)) + 'MB / ' + gamelist[game_version-1]['size'], end='\r')
                                    success('\n下载完成！')
                                    time.sleep(2)
                                    cls()
                                    log('正在解压服务端……')
                                    zip_path = 'gc/' + gamelist[game_version-1]['version'] + '.zip'
                                    extract_path = 'gc/' + gamelist[game_version-1]['version']
                                    if os.path.exists(extract_path) == False:
                                        os.mkdir(extract_path)
                                    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                                        zip_ref.extractall(extract_path)
                                    success('解压完成！')
                                    time.sleep(2)
                                    cls()
                                    main()
                            elif i == 'p':
                                cls()
                                success('下载链接:' + gamelist[game_version-1]['url_pan'])
                                success('下载完成后，请将文件移动至gc文件夹中。')
                                warn('请不要重命名文件。')
                                s = '.'
                                while os.path.exists('gc/' + gamelist[game_version-1]['version'] + '.zip') == False:
                                    s += '.'
                                    log('等待文件' + s, end='\r')
                                    time.sleep(1)
                                success('已检测到文件，正在解压！')
                                zip_path = 'gc/' + gamelist[game_version-1]['version'] + '.zip'
                                extract_path = 'gc/' + gamelist[game_version-1]['version']
                                if os.path.exists(extract_path) == False:
                                    os.mkdir(extract_path)
                                with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                                    zip_ref.extractall(extract_path)
                                success('解压完成！')
                    else:
                        error('程序将在5秒后退出。')
                        time.sleep(5)
                        sys.exit()
        else:
            error('输入错误！')
            time.sleep(2)
            main()

    else:
        error("网络连接错误：状态码：" + str(request.status_code))
        log("程序将在5秒后退出。")
        time.sleep(5)
        sys.exit()
def run_jar(gamelist, i):
    os.system('cd gc/' + gamelist[int(i)-1] + ' && java -jar grasscutter.jar')         
def start_server():
    log('正在获取服务器列表……')
    gamelist = []
    for file in os.listdir('gc'):
        if os.path.isdir('gc/' + file):
            gamelist.append(file)
    if len(gamelist) == 0:
        error('未找到服务器文件，请先下载服务端。')
        log('程序将在5秒后退出。')
        time.sleep(5)

    success('发现服务器列表：')
    for i in range(len(gamelist)):
        log(str(i+1) + '. ' + gamelist[i])
    ask('请输入您要启动的服务器序号：')
    i = input()
    if i.isdigit() == False:
        error('输入错误!')
        time.sleep(2)
        main()
    if int(i) > len(gamelist):
        error('输入错误!')
        time.sleep(2)
        main()
    else:
        log('正在启动服务器……')
        with open(config['gc'] + '/' + gamelist[int(i)-1] + '/config.json','r',encoding='utf-8') as f:
            configa = json.load(f)
            configa['databaseInfo']['server']['connectionUri'] = 'mongodb://localhost:' + config['mongodb']
            configa['databaseInfo']['game']['connectionUri'] = 'mongodb://localhost:' + config['mongodb']
            with open(config['gc'] + '/' + gamelist[int(i)-1] + '/config.json','w',encoding='utf-8') as f:
                f.write(json.dumps(configa))
            success('Mongodb端口已修改为' + config['mongodb'])
        threading.Thread(target=run_jar, args=(gamelist,i,)).start()
        log('服务器正在启动……')
        
    pass
def download_genshin():
    webbrowser.open('https://files.hk4e.com/?game=hk4e&utm_source=blog')
    main()
def main():
    cls()
    success('欢迎使用！')
    log('本程序的所有资源均来自休比(3186565462)的Grasscutter服务端。')
    log('请选择您要进行的操作：')
    log('1. 启动服务器')
    log('2. 下载/安装服务端')
    log('3. 下载原神本体')
    ask('请选择：')
    i = input()
    if i == '1':
        cls()
        log('正在启动服务器……')
        start_server()
    elif i == '2':
        cls()
        download_gc()
    elif i == '3':
        cls()
        download_genshin()

def scan_java():
    # 获取JAVA版本
    log('正在获取JAVA版本……')
    java_version = os.popen('java -version 2>&1').read()
    match = re.search(r'version "(\d+\.\d+\.\d+)', java_version)
    match.group(1)
    if match.group(1):
        success('发现JAVA 版本：' + match.group(1))
        if match.group(1) < '17':
            error('JAVA版本过低，请使用JAVA17及以上版本。')
            time.sleep(3)
            main()
        with open('config.json','r',encoding='utf-8') as f:
            config = json.load(f)
            config['java'] = 'java' # 已经有环境变量了，不需要设置路径
            with open('config.json','w',encoding='utf-8') as f:
                json.dump(config,f,indent=4)
    else:
        error('未找到JAVA，请手动输入JAVA位置。')
        log('3秒后返回。')
        time.sleep(3)
        main()

if __name__ == "__main__": #一些自检和初始化
    config = {}
    init(autoreset=True)
    nowtime = int(time.strftime("%H", time.localtime()))
    if nowtime < 12:
        t = '上午'
    elif nowtime < 18:
        t = '下午'
    else:
        t = '晚上'
    log(Fore.GREEN + t + f'好，旅行者。')
    log(f'{Fore.YELLOW}现在是' + t + time.strftime("%H:%M", time.localtime()) + '。')
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
                        "game_version": '',
                        "java": ''
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
                        time.sleep(2)
                        main()
                    else:
                        with open('config.json','r',encoding='utf-8') as f:
                            config = json.loads(f.read())
                            config['game'] = gamepath
                            with open('config.json','w',encoding='utf-8') as f:
                                f.write(json.dumps(config))
                        success('游戏路径配置已生效。')
                        time.sleep(2)
                        main()
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
                        success('MongoDB端口已配置。')
                        time.sleep(2)
                        main()
                        pass
                    else:
                        with open('config.json','r+',encoding='utf-8') as f:
                            config = json.loads(f.read())
                            config['mongodb'] = mongodbpath
                            with open('config.json','w',encoding='utf-8') as f:
                                f.write(json.dumps(config))
                        success('MongoDB端口已配置。')
                        error('3秒后返回')
                        time.sleep(3)
                        main()
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
    else:
        log("正在创建配置文件……")
        with open('config.json','w',encoding='utf-8') as f:
            result = {
                "server": '0.0.0.0',
                "port": 12345,
                "game": '',
                "mongodb": '',
                "gc": '',
                "game_version": '',
                "java": ''
            }
            f.write(json.dumps(result))
        success("配置文件创建成功，请重新启动程序。")
        error('程序将在3秒后退出。')
        time.sleep(3)
        sys.exit()
    #获取java版本
    if config['java'] == '':
        error('Java路径为空！')
        javapath = input('[~] 请输入Java路径(n: 自动搜索)：')
        if javapath == 'n':
            success('已跳过，即将搜索Java。')
            scan_java()
        else:
            with open('config.json','r+',encoding='utf-8') as f:
                config = json.loads(f.read())
                config['java'] = javapath
                with open('config.json','w',encoding='utf-8') as f:
                    f.write(json.dumps(config))
            success('Java路径已配置，重启程序生效。')
    main()



