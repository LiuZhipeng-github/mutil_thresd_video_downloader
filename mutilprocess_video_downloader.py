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




import requests, json, re
from lxml import etree
import time
import random
import multiprocessing
from tqdm import tqdm
def first_parser(url, count):
    # count += 1
    # if count > 35:
    #     return
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.7.6) Gecko/20050225 Firefox/1.0.1',
        'cookie':'_zap=83d13343-c555-4c7e-9d25-d4beed6363a0; d_c0="AECfJtEDHhKPTrcek-vRQp5DaW5SZpah9RA=|1604031911"; tst=r; q_c1=23c89145e9c94c41ba4630d954bb6603|1609314769000|1606187870000; OUTFOX_SEARCH_USER_ID_NCOO=1100231894.8855052; _xsrf=6282e484-acef-421a-862b-47f0daed8660; z_c0="2|1:0|10:1610006006|4:z_c0|92:Mi4xNnJ6QUF3QUFBQUFBUUo4bTBRTWVFaVlBQUFCZ0FsVk45Z3ZrWUFEc1o3LWVLWkNvdXBHMEtraTctTGJLaXZmZDB3|96762af11b891068ce36b8dab2991ac53b88d76cdd47ec4e8cc242cd3c64612c"; capsion_ticket="2|1:0|10:1610006008|14:capsion_ticket|44:NzE1ZTdlYzc0N2JjNDNiY2IxZjEyMmMwNTIwZmVjOTU=|f130f23f0a74243a11e6b2b21c5de3ad0a1ba54bead92af7be300e0c6e0ed4dc"; Hm_lvt_98beee57fd2ef70ccdd5ca52b9740c49=1610005447,1610005489,1610005529,1610068584; SESSIONID=7qqw06PudaXb9G6EoORNRH44o3aGbnjBn1hPOgMSTpI; JOID=W1sUAUOKmL_I0khCP4HTqwIPQFclt-vNteN0EEnv8-Wp4Q5-eLtlQZzZQEM2lQHXdvwTU-jnk3JYRd1YM7MW3Y8=; osd=UlgXAUODm7zI0kFBPIHTogEMQFcstOjNtep3E0nv-uaq4Q53e7hlQZXaQ0M2nALUdvwaUOvnk3tbRt1YOrAV3Y8=; KLBRSID=cdfcc1d45d024a211bb7144f66bda2cf|1610088529|1610085115; Hm_lpvt_98beee57fd2ef70ccdd5ca52b9740c49=1610088530'}
    headers2 = {
        'User-Agent': 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.7.6) Gecko/20050225 Firefox/1.0.1',
        'cookie':'_zap=83d13343-c555-4c7e-9d25-d4beed6363a0; d_c0="AECfJtEDHhKPTrcek-vRQp5DaW5SZpah9RA=|1604031911"; z_c0="2|1:0|10:1606097679|4:z_c0|92:Mi4xNnJ6QUF3QUFBQUFBUUo4bTBRTWVFaVlBQUFCZ0FsVk5EMm1vWUFEcUpVSzVBdTl2cDcxb0l5SVM2VmNwb0hNSUJB|848ee6613753c85ca554d4a672c8fe5db3cbba9493de956c5533d9bbf2647fde"; tst=r; q_c1=23c89145e9c94c41ba4630d954bb6603|1609314769000|1606187870000; OUTFOX_SEARCH_USER_ID_NCOO=1100231894.8855052; _xsrf=6282e484-acef-421a-862b-47f0daed8660; Hm_lvt_98beee57fd2ef70ccdd5ca52b9740c49=1609751972,1609896113,1609896215,1609898091; SESSIONID=vSBrtPGWbJ97i7RfMWgVrQOXmcYVB4LOApCDVbNP705; JOID=U1oRA0uOGrjRRDpMMo9YoRiUOFAl-0_-ozFpDWHtU4fiLQwdUi8ASY9GP042wfJSKudMy8bLBFwcX4hF7MibxGw=; osd=U1scA0mOG7XRRjpNP49aoRmZOFIl-kL-oTFoAGHvU4bvLQ4dUyIAS49HMk40wfNfKuVMysvLBlwdUohH7MmWxG4=; Hm_lpvt_98beee57fd2ef70ccdd5ca52b9740c49=1609898119; KLBRSID=fb3eda1aa35a9ed9f88f346a7a3ebe83|1609898206|160989616'
    }
    # r = requests.get(url, headers=random.choice([headers,headers2]))
    # print(random.choice([headers,headers2])
    r = requests.get(url, headers=headers)
    r.raise_for_status()
    # r.encoding = r.apparent_encoding
    r.encoding = ('utf-8')
    first_layer = json.loads(r.text)
    # print(first_layer)
    is_end = first_layer['paging']['is_end']
    next_url = first_layer['paging']['next']
    if is_end:
        return
    # print('data++++++++++++++++++++',first_layer['data'])
    for data in first_layer['data']:
        # print(data)
        try:
            tem_dic = {'author_id': data['target']['id'], 'commit_time': data['target']['created'],
                       'comment_count': data['target']['comment_count'],
                       'type': data['target']['type']}
        except:
            tem_dic = {'author_id': data['target']['id'], 'commit_time': data['target']['created_time'],
                       'comment_count': data['target']['comment_count'],
                       'type': data['target']['type']}

        result.append(tem_dic)
        print(tem_dic)
    next_url = next_url.replace('http','https')
    print(next_url)
    
    return first_parser(next_url, count)


def join_url():
    # print(result)
    url_list = []
    for i in result:
        if i['comment_count'] != 0:
            url = f'https://www.zhihu.com/api/v4/{i["type"]}s/{i["author_id"]}/root_comments?order=normal&limit=20&offset=0&status=open'
            url_list.append(url)
    return url_list


def second_parse(q,url): 
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.7.6) Gecko/20050225 Firefox/1.0.1',
        'Connection': 'close',
    }
    r = requests.get(url, headers=headers)
    # r.raise_for_status()
    r.encoding = ('utf-8')
    # print('+++++++++++++++++++++++++++++++++++++++++++++++++++++')
    second_layer = json.loads(r.text)
    gender_dic = {'1': '男', '-1': '匿名', '0': '女'}
    try:
      is_end = second_layer['paging']['is_end']
      next_url = second_layer['paging']['next']
      for data in second_layer['data']:
          if '<p>' in data['content']:
              data['content'] = re.findall('<p>(.+?)</p>', data['content'])[0]
          comment_tem = {'commenter_id': data['id'], 'content': data['content'],'created_time':time.strftime('%Y%m%d%H%S',time.gmtime(data['created_time'])),'gender':gender_dic[str(data['author']['member']['gender'])]}
          comments_result.append(comment_tem)
          print(comment_tem)
      if is_end:
          pass
      else:
          rest_comment(next_url)
    except:
      print('该评论被折叠')

def rest_comment(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.7.6) Gecko/20050225 Firefox/1.0.1',
        'Connection': 'close',

    }
    gender_dic = {'1':'男','-1':'匿名','0':'女'}
    r = requests.get(url, headers=headers)
    r.raise_for_status()
    r.encoding = ('utf-8')
    second_layer = json.loads(r.text)
    is_end = second_layer['paging']['is_end']
    next_url = second_layer['paging']['next']
    for data in second_layer['data']:
        if '<p>' in data['content']:
            data['content'] = re.findall('<p>(.+?)</p>', data['content'])[0]
        comment_tem = {'commenter_id': data['id'], 'content': data['content'],'created_time':time.strftime('%Y%m%d%H%S',time.gmtime(data['created_time'])),'gender':gender_dic[str(data['author']['member']['gender'])]}
        comments_result.append(comment_tem)
        print(comment_tem)
    if is_end:
        pass
    else:
        return rest_comment(next_url)


def to_csv():
    df = pd.DataFrame(comments_result)
    df.to_csv('result.csv')


def multi(url_list):
    num = len(url_list)
    pool = multiprocessing.Pool(6)
    q = multiprocessing.Manager().Queue()
    for url in url_list:
        pool.apply_async(second_parse, args=(q,url))
    pool.close()
    pool.join()
    # for i in tqdm(range(num)):
    #     url = q.get()
    #     result.append(url)

if __name__ == '__main__':
    comments_result = []
    result = []
    count = 0
    # url = 'https://www.zhihu.com/api/v4/topics/19564862/feeds/top_activity?include=data%5B%3F%28target.type%3Dtopic_sticky_module%29%5D.target.data%5B%3F%28target.type%3Danswer%29%5D.target.content%2Crelationship.is_authorized%2Cis_author%2Cvoting%2Cis_thanked%2Cis_nothelp%3Bdata%5B%3F%28target.type%3Dtopic_sticky_module%29%5D.target.data%5B%3F%28target.type%3Danswer%29%5D.target.is_normal%2Ccomment_count%2Cvoteup_count%2Ccontent%2Crelevant_info%2Cexcerpt.author.badge%5B%3F%28type%3Dbest_answerer%29%5D.topics%3Bdata%5B%3F%28target.type%3Dtopic_sticky_module%29%5D.target.data%5B%3F%28target.type%3Darticle%29%5D.target.content%2Cvoteup_count%2Ccomment_count%2Cvoting%2Cauthor.badge%5B%3F%28type%3Dbest_answerer%29%5D.topics%3Bdata%5B%3F%28target.type%3Dtopic_sticky_module%29%5D.target.data%5B%3F%28target.type%3Dpeople%29%5D.target.answer_count%2Carticles_count%2Cgender%2Cfollower_count%2Cis_followed%2Cis_following%2Cbadge%5B%3F%28type%3Dbest_answerer%29%5D.topics%3Bdata%5B%3F%28target.type%3Danswer%29%5D.target.annotation_detail%2Ccontent%2Chermes_label%2Cis_labeled%2Crelationship.is_authorized%2Cis_author%2Cvoting%2Cis_thanked%2Cis_nothelp%2Canswer_type%3Bdata%5B%3F%28target.type%3Danswer%29%5D.target.author.badge%5B%3F%28type%3Dbest_answerer%29%5D.topics%3Bdata%5B%3F%28target.type%3Danswer%29%5D.target.paid_info%3Bdata%5B%3F%28target.type%3Darticle%29%5D.target.annotation_detail%2Ccontent%2Chermes_label%2Cis_labeled%2Cauthor.badge%5B%3F%28type%3Dbest_answerer%29%5D.topics%3Bdata%5B%3F%28target.type%3Dquestion%29%5D.target.annotation_detail%2Ccomment_count%3B&limit=10&after_id=00.00000'
    url = 'http://www.zhihu.com/api/v4/topics/19564862/feeds/essence?include=data%5B%3F%28target.type%3Dtopic_sticky_module%29%5D.target.data%5B%3F%28target.type%3Danswer%29%5D.target.content%2Crelationship.is_authorized%2Cis_author%2Cvoting%2Cis_thanked%2Cis_nothelp%3Bdata%5B%3F%28target.type%3Dtopic_sticky_module%29%5D.target.data%5B%3F%28target.type%3Danswer%29%5D.target.is_normal%2Ccomment_count%2Cvoteup_count%2Ccontent%2Crelevant_info%2Cexcerpt.author.badge%5B%3F%28type%3Dbest_answerer%29%5D.topics%3Bdata%5B%3F%28target.type%3Dtopic_sticky_module%29%5D.target.data%5B%3F%28target.type%3Darticle%29%5D.target.content%2Cvoteup_count%2Ccomment_count%2Cvoting%2Cauthor.badge%5B%3F%28type%3Dbest_answerer%29%5D.topics%3Bdata%5B%3F%28target.type%3Dtopic_sticky_module%29%5D.target.data%5B%3F%28target.type%3Dpeople%29%5D.target.answer_count%2Carticles_count%2Cgender%2Cfollower_count%2Cis_followed%2Cis_following%2Cbadge%5B%3F%28type%3Dbest_answerer%29%5D.topics%3Bdata%5B%3F%28target.type%3Danswer%29%5D.target.annotation_detail%2Ccontent%2Chermes_label%2Cis_labeled%2Crelationship.is_authorized%2Cis_author%2Cvoting%2Cis_thanked%2Cis_nothelp%2Canswer_type%3Bdata%5B%3F%28target.type%3Danswer%29%5D.target.author.badge%5B%3F%28type%3Dbest_answerer%29%5D.topics%3Bdata%5B%3F%28target.type%3Danswer%29%5D.target.paid_info%3Bdata%5B%3F%28target.type%3Darticle%29%5D.target.annotation_detail%2Ccontent%2Chermes_label%2Cis_labeled%2Cauthor.badge%5B%3F%28type%3Dbest_answerer%29%5D.topics%3Bdata%5B%3F%28target.type%3Dquestion%29%5D.target.annotation_detail%2Ccomment_count%3B&limit=10&offset=0'
    first_parser(url, count)
    url_list =join_url()
    print(url_list)
    multi(url_list)
    # to_csv()
    print(f'已完成任务，本次共爬取{len(comments_result)}条内容')



