import requests
from requests.exceptions import RequestException
import re, json
from multiprocessing import Pool

def get_one_page(url):
    header = {
        'User-Agent':'user-agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
            +'(KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36'
    }
    try:
        response = requests.get(url, headers = header)
        if response.status_code == 200:
            return response.text
        print('false')
    except RequestException:
        return None


def parse_one_page(html):
    pattren = re.compile('<dd>.*?board-index.*?>(\d+)</i>.*?data-src="(.*?)".*?name"><a.*?>(.*?)'
                         +'</a>.*?star">(.*?)</p>.*?releasetime">(.*?)</p>.*?integer">'
                         +'(.*?)</i>.*?fraction">(\d+)</i>.*?</dd>',re.S)
    items = re.findall(pattren, html)
    for item in items:
        yield {
            'index':item[0],
            'image':item[1],
            'title':item[2],
            'actor':item[3].strip()[3:],
            'time':item[4].strip()[5:],
            'score':item[5]+item[6]
        }

def write_to_file(content):
    with open('result.txt','a',encoding='utf-8') as f:
        f.write(json.dumps(content, ensure_ascii=False)+'\n')

def main(offset):
    url = 'http://maoyan.com/board/4' + '?offset=' + str(offset)
    html = get_one_page(url)
    for item in parse_one_page(html):
        print(item)
        write_to_file(item)


if __name__ == '__main__':
    pool = Pool()
    #pool.map(main,  [i*10 for i in range(10)])
    for i in range(10):
        pool.apply_async(main, args=(i*10,))
    pool.close()
    pool.join()
    print('All done')
