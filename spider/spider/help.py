from scrapy.selector import Selector
import requests,traceback
from urllib import parse




noneedurl = [
    '../../kh/nk/index.htm',
    '../../wuxia/nk/index.htm',
    'zqs/index.htm',
    'zqs9/index.htm',
    'zqs10/index.htm',
    'gsct/index.htm',
]
def start_urls():
    url = 'http://www.my2852.com/yq/c/chaofeng/index.htm'
    headers={"User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:52.0) Gecko/20100101 Firefox/52.0"}
    res = requests.get(url, headers=headers)
    if res.status_code == 200:
        selector=Selector(text=res.content.decode('gbk','ignore'))
        all_href = selector.css(".jz table a::attr(href)").extract()
        if not all_href:
            all_href=selector.css("td table a::attr(href)").extract()

        if not all_href:
            all_href=selector.css("center>table:nth-child(1)>tr a::attr(href)").extract()

        if not all_href:
            all_href=selector.css("div>table:nth-child(2)>tr a::attr(href)").extract()


        all_href =  list(set(all_href))
        full_all_href = []
        for href in all_href:
            if 'index.htm' in href and href not in noneedurl:
                full_all_href.append(parse.urljoin(url, href))
            else:
                print(f"这个 {href} 不添加")

        return full_all_href
    else:
        raise Exception('start_urls 方法 网络请求失败')


def parse_info(response,author):
    try:
        novel_dict={}
        novel_dict['author']= author

        novel_dict['name']= \
            response.css(
                "div table tr:nth-child(2) td font::text").extract_first("").strip()


        if not novel_dict['name']:
            novel_dict['name']= \
                response.css(
                    "div table tr:nth-child(2) td span::text").extract_first(
                    "").strip()

        if not novel_dict['name']:
            novel_dict['name']=\
                response.css(
                    "table.tb2 .td3::text").extract_first("").strip()

        if not novel_dict['name']:
            novel_dict['name']=\
                response.css(
                    "table.tb2 .td3>span::text").extract_first("").strip()


        if not novel_dict['name']:
            novel_dict['name']=\
                response.css(
                    "table .tdw::text").extract()[0].strip()


        return novel_dict

    except Exception:
        raise Exception(traceback.format_exc())

