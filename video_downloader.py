'''
https://m3u8.pps11.com/wodeshipin_water_m3u8/zipaitoupai/80_20200110170128800/0220.ts
https://m3u8.pps11.com/wodeshipin_water_m3u8/zipaitoupai/80_20200110170128800/0010.ts
'''
import requests
import os,sys
from concurrent.futures import ThreadPoolExecutor
# import urllib3.contrib.pyopenssl
from subprocess import run



def get_url(name,URL):

    x = input("请输入要下载的ts数:")
    x = int(x)

    url_list = []
    for i in range(x+1):
        url = URL+"{}.ts".format(str(i).rjust(4, "0"))
        print(url)
        name_ = url.split("/")[-1]
        url_list.append(url)
        name.append(name_)
    return(url_list)


def video_download(url,x):
    if not os.path.exists(fpath):
        os.mkdir(fpath)
    print(url)
    name = url.split("/")[-1]
    headers = {
            'User-Agent': 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.7.6) Gecko/20050225 Firefox/1.0.1',
            'Connection': 'close',

        }

    try:
        response = requests.get(url,headers=headers,timeout=10)

        print('正在下载:', url)
        open(f'{fpath}/{name}', 'wb').write(response.content)

        print('下载结束')
    except:
        try:
            print('正在重新下载第一次:', url)
            response = requests.get(url, headers=headers, timeout=10)
            open(f'{fpath}/{name}', 'wb').write(response.content)
            print('重新下载第一次结束')
        except:
            try:
                print('正在重新下载第二次:', url)
                response = requests.get(url, headers=headers, timeout=12)
                open(f'{fpath}/{name}', 'wb').write(response.content)
                print('重新下载第二次结束')
            except:
                try:
                    print('正在重新下载第三次:', url)
                    response = requests.get(url, headers=headers, timeout=15)
                    open(f'{fpath}/{name}', 'wb').write(response.content)
                    print('重新下载第三次结束')
                except:
                    x=x+1
                    print(url + "下载失败",x)

def multi(url_list):
    pool = ThreadPoolExecutor(max_workers=50)
    x=0
    for url in url_list:
        pool.submit(video_download, url,x)
    pool.shutdown()


def convert_file(fname):
    command2 = f'cat *.ts >new{fname}.mp4'
    ret = run(command2, shell=True)
    print(ret)

def delete_files():
    for filename in os.listdir(fpath):  # 获取文件夹内所有文件的文件名
        if filename.endswith('.ts') :  # 若文件名满足指定条件
            os.remove(os.path.join(fpath, filename))  # 删除符合条件的文件
            print("{} deleted.".format(filename))  ##输出提示


if __name__ == '__main__':
    URL = input("请输入视频网址")
    # urllib3.contrib.pyopenssl.inject_into_urllib3()
    name=[]
    fpath = r"/Users/liuzhipeng/Downloads/电影/学习资料/下载"
    fio=input('请输入文件名：')
    filename = '\ '[:-1]+fio
    url_list=get_url(name,URL)
    multi(url_list)
    print("最终结束")
    convert_file(filename)
    delete_files()



#打包
