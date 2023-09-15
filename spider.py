import json
import urllib.request
import urllib.parse
import bs4
import requests
import os
import re
from bs4 import BeautifulSoup
import unittest
base_url = 'https://www.luogu.com.cn/problem/list?'

headers = {'user-agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.71 Safari/537.36',
           'cookie':'__client_id=9fe16574d480d22ea1cc6af92852628cff235079; login_referer=https%3A%2F%2Fwww.luogu.com.cn%2Fproblem%2Flist%3Fdifficulty%3D1%26page%3D1; _uid=1091654; C3VK=e25db2',
           'referer':'https://www.luogu.com.cn/problem/P1035'}
pagenum = {
    '入门':1,'普及−':2,'普及/提高−':3,'普及+/提高':4,'提高+/省选−':5,'省选/NOI−':6,'NOI/NOI+/CTSC':7
}


p_list = [] #存放待爬取的题目序号
global difficulty,keyword
data = {
    'difficulty':'',
    'keyword':''
}


def main(difficulty,keyword):
    url = category_search(difficulty,keyword,1)
    getList(url)
    getMD()
# def search(diff,keystr):
#     data.setdefault('difficulty',diff)
#     data.setdefault('keyword',keystr)
#     last_url = urllib.parse.urlencode(data)
#     url = base_url+last_url
#     print(url)
#     return url

def category_search(dnum,keyword,pnum):
    value1 = pagenum[dnum]
    key = {#传入参数，拼成完整网址
        'difficulty':value1,
        'keyword': keyword,
        'page':pnum
    }
    last_url = urllib.parse.urlencode(key)
    url = base_url+last_url
    return url

def getList(url): #设定难度，得到该难度下的第一页（最多50题）

    request = urllib.request.Request(url=url,headers=headers)
    response = urllib.request.urlopen(request)
    content = response.read().decode('utf-8')
    soup = BeautifulSoup(content, 'html.parser')
    links = soup.find_all('a')

    for link in links:
        if("=" not in link.get('href')):
            p_list.append(link.get('href'))
    print(p_list)

def getMD():#爬取对应题目和题解，并保存本地
    for link in p_list:
        p_url = 'https://www.luogu.com.cn/problem/'+link
        p_response = requests.get(url=p_url,headers=headers)
        if str(p_response.text).find("Exception") != -1:
            print("爬取失败")
            continue
        else:
            p_response.encoding = 'utf-8'
            soup = BeautifulSoup(p_response.text, 'html.parser')
            links = soup.find_all('article')


            for one  in links:

                links2 = soup.find_all('h1')
                qname = str(links2[0])[4:-5]
                #对创建文件时非法字符进行处理
                if '?' in qname:
                    qname=qname.replace('?','？')
                if '*' in qname:
                    qname=qname.replace('*','x')
                if '/' in qname:
                    qname=qname.replace('/','÷')
                if ':' in qname:
                    qname=qname.replace(':','：')
                filename = str(link) + '-'+qname
                # print(filename)
                os.mkdir('G:\Spider result\ '+filename,777)
                f = open('G:\Spider result\ '+filename+'\ ' + filename+'.md',mode='w+',encoding='utf-8')
                f.write(str(one))
                f.close()

            a_url = 'https://www.luogu.com.cn/problem/solution/'+link
            a_response = requests.get(url=a_url, headers=headers)
            bs = BeautifulSoup(a_response.text,'html.parser')
            core = bs.select('script')[0]
            script = str(core)
            index1 = script.index('"')
            index2 = script.index('"', index1 + 1)
            script = script[index1 + 1: index2]
            decodedStr = urllib.parse.unquote(script)
            map1 = json.loads(decodedStr)
            solutions = map1["currentData"]["solutions"]["result"]
            if len(solutions) >0:#党题目存在题解时保存，否则继续
                bestSolution = solutions[0]
                f_solution = open('G:\Spider result\ ' + filename + '\ ' + filename + '-'+'题解.md', mode='w+', encoding='utf-8')
                f_solution.write(str(bestSolution))
                print(link+"题目和题解保存完成！")
                f_solution.close()
            else:
                print(link+"题目保存完成，无题解！")
                continue


if __name__ == '__main__':
    main(difficulty=difficulty,keyword=keyword)







