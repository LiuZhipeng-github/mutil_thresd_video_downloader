import requests
import os
import subprocess
import time
import multiprocessing
from tqdm import tqdm


def get_url(URL):
    n = URL.split('/')[-1]
    n = int(n.split('.')[0])
    URL = URL.rsplit('/', 1)[0]
    url_list = []
    for i in range(n + 1):
        url = str(URL) + '/' + "{}.ts".format(str(i).rjust(4, "0"))
        # print(str(url))
        url_list.append(url)
    return (url_list)


def video_download(q, url):
    name = str(time.strftime("%m-%d"))
    fpath = "/Users/liuzhipeng/Downloads/电影/学习资料/下载/" + name
    if not os.path.exists(fpath):
        os.mkdir(fpath)
    name = url.rsplit('/')[-1].split(".")[0].rjust(4, "0")
    name = name + '.ts'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.7.6) Gecko/20050225 Firefox/1.0.1',
        'Connection': 'close',

    }
    try:
        response = requests.get(url, headers=headers, timeout=10)
        # print('正在下载:', url)
        open(f'{fpath}/{name}', 'wb').write(response.content)
        # print('下载结束')
    except:
        try:
            response = requests.get(url, headers=headers, timeout=10)
            # print('正在重新下载第一次:', url)
            open(f'{fpath}/{name}', 'wb').write(response.content)
            # print('重新下载第一次结束')
        except:
            try:
                response = requests.get(url, headers=headers, timeout=(3, 10))
                # print('正在重新下载第二次:', url)
                open(f'{fpath}/{name}', 'wb').write(response.content)
                # print('重新下载第二次结束')
            except:
                try:
                    response = requests.get(url, headers=headers, timeout=(3, 10))
                    # print('正在重新下载第三次:', url)
                    open(f'{fpath}/{name}', 'wb').write(response.content)
                    # print('重新下载第三次结束')
                except:
                    q.put(url)
    q.put(url)


def multi(url_list):
    num = len(url_list)
    pool = multiprocessing.Pool(20)
    q = multiprocessing.Manager().Queue()
    for url in url_list:
        pool.apply_async(video_download, args=(q, url))
    pool.close()
    for i in tqdm(range(num)):
        url = q.get()
        result.append(url)


def convert_file(fname):
    name = str(time.strftime("%H-%M-%S"))
    command1 = r'cd /Users/liuzhipeng/Downloads/电影/学习资料/下载/' + fname
    print(command1)
    command2 = f'cat *.ts >n{name}.mp4'
    command = command1 + '&&' + command2
    subprocess.run(command, shell=True)


def delete_files(fpath):
    for filename in os.listdir(fpath):  # 获取文件夹内所有文件的文件名
        if filename.endswith('.ts'):  # 若文件名满足指定条件
            os.remove(os.path.join(fpath, filename))  # 删除符合条件的文件



if __name__ == '__main__':
    URL = input("请输入视频网址")
    while URL != 'q':
        result = []
        name = str(time.strftime("%m-%d"))
        fpath = "/Users/liuzhipeng/Downloads/电影/学习资料/下载/" + name
        url_list = get_url(URL)
        multi(url_list)
        convert_file(name)
        delete_files(fpath)
        if '失败' in result:
            print('\n视频未下全')
        URL = input("\n请输入视频网址")
'''
https://m3u8.pps11.com/wodeshipin_water_m3u8/zipaitoupai/80_20200110170128800/0060.ts
https://m3u8.pps11.com/wodeshipin_water_m3u8/zipaitoupai/80_20200110170128800/0220.ts
'''
# 打包pyinstaller -F -i E:\lfile\ff10.ico Movie_downloader.py
