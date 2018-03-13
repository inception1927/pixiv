from bs4 import *
from urllib.request import *
from urllib.error import *
from http import cookiejar
import requests
import re
import os

headers = {
    'Host': 'accounts.pixiv.net',
    'Origin': 'https://accounts.pixiv.net',
    'Referer': 'https: // accounts.pixiv.net / login'
               '?lang = zh & source = pc & view_type = page & ref = wwwtop_accounts_index',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'
                  ' AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36',
    'X-Requested-With': 'XMLHttpRequest'
}
local_path = 'F:/pixiv/'

base_url = 'https://accounts.pixiv.net/login?lang=zh&source=pc&view_type=page&ref=wwwtop_accounts_index'
login_url = 'https://accounts.pixiv.net/api/login?lang=zh'
target_url = 'https://www.pixiv.net/search.php?s_mode=s_tag&word=%E5%AE%AB%E5%9B%AD%E8%96%B0'
main_url = 'http://www.pixiv.net'

session = requests.session()


def login():
    html = session.get(base_url, headers=headers)
    soup = BeautifulSoup(html.text, 'lxml')
    postkey = soup.find('input', {'name': 'post_key'})['value']
    data = {
        'pixiv_id': '1303283743@qq.com', 'password': 'wan5072598',
        'post_key': postkey, 'source': 'pc', 'ref': 'wwwtop_accounts_index',
        'return_to': 'https://www.pixiv.net/'
    }
    p = session.post(login_url, data=data, headers=headers)
    print(p)


def ranking():
    #searchPage = session.get('https://www.pixiv.net/search.php?s_mode=s_tag&word=イリヤ10000users入り')
    searchPage = session.get('https://www.pixiv.net/ranking.php?mode=daily&content=illust')
    soup = BeautifulSoup(searchPage.text, 'lxml')
    #s = soup.find_all('a', {'href': re.compile('/member_illust')})
    s = soup.find_all('img', {'class': '_thumbnail ui-scroll-view'})
    cnt = findLast()
    for author in s:
        count = author.parent.next_sibling
        img = author['data-src']
        pattern = re.compile('img/.*p0')
        try:
            ss = pattern.findall(img)[0]
        except BaseException as e:
            continue
        if count is None:
            ori = 'https://i.pximg.net/img-original/' + ss + '.png'
            download(ori, cnt)
            cnt += 1
        elif int(count.text) < 5:
            for i in range(int(count.text)):
                newss = ss[:len(ss) - 1] + str(i)
                ori = 'https://i.pximg.net/img-original/' + newss + '.png'
                download(ori, cnt)
                cnt += 1


def download(url, cnt):
    if not os.path.exists(local_path):
        os.mkdir(local_path)
    refer = getRefer(url)
    head = headers
    head['Referer'] = refer
    try:
        req = Request(url, None, head)
        res = urlopen(req)
        rstream = res.read()
        res.close()
    except HTTPError:
        url = url.replace('.png', '.jpg')
        req = Request(url, None, head)
        res = urlopen(req)
        rstream = res.read()
        res.close()
    with open(local_path+'%s.png' % cnt, 'wb') as f:
        f.write(rstream)


def findLast():
    if len(os.listdir(local_path)) > 0:
        s = os.listdir(local_path)
        ls = []
        for i in s:
            ls.append(int(i[:-4]))
        ls.sort()
        return ls[-1]+1
    else:
        return 0


def getRefer(url):
    reference = "http://www.pixiv.net/member_illust.php?mode=manga_big&illust_id="
    reg = r'.+/(\d+)_p'
    return reference + re.findall(reg, url)[0] + url[-1] + '&page=0'


if __name__ == '__main__':
    login()
    ranking()
    #search('イリヤ10000users入り')
    #search('イリヤ1000users入り')


