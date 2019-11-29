from scrapy.selector import Selector
import requests,traceback
from urllib import parse
import re,helpers,emoji,html




noneedurl = [
    '../../kh/nk/index.htm',
    '../../wuxia/nk/index.htm',
    'zqs/index.htm',
    'zqs9/index.htm',
    'zqs10/index.htm',
    'gsct/index.htm',
]



def start_urls():
    url = 'http://www.my2852.com/yq/c/chuanshang/index.htm'
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


def parse_info(response):
    try:
        author = '川上'
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


        return novel_dict , author

    except Exception:
        raise Exception(traceback.format_exc())




def get_rep_html(html):

    return "$$$$$${}$$$$$$".format(html)


def get_endrep_html(html):

    return "$$$$$$end{}$$$$$$".format(html)


def handle_content(htmlstr):

    def rep_html(html,htmlstr):
        rep_html = get_rep_html(html)
        rep_endhtml = get_endrep_html(html)

        rex_html = "(<\s*{}[^>]*>)".format(html)
        compile_html = re.compile(rex_html, re.I)
        htmlstr = compile_html.sub(rep_html, htmlstr)

        rex_endhtml = "(<\s*/\s*{}\s*>)".format(html)
        compile_endhtml = re.compile(rex_endhtml, re.I)
        return compile_endhtml.sub(rep_endhtml, htmlstr)

    htmlstr = rep_html('p',htmlstr)
    htmlstr = rep_html('table',htmlstr)
    htmlstr = rep_html('tbody',htmlstr)
    htmlstr = rep_html('tr',htmlstr)
    htmlstr = rep_html('td',htmlstr)

    # 过滤
    htmlstr=htmlstr \
        .replace('\r', '') \
        .replace('\t', '') \
        .replace('\n', '') \
        .replace('𠴂', '口') \
        .replace('&#134402;', '口').strip()

    # 过滤空格
    re_stopwords=re.compile('\u3000', re.I)
    htmlstr=re_stopwords.sub('', htmlstr)
    re_stopwords2=re.compile('\xa0', re.I)
    htmlstr=re_stopwords2.sub('', htmlstr)
    # 过滤垃圾
    re_script=re.compile('<\s*script[^>]*>[^<]*<\s*/\s*script\s*>',
                         re.I)  # Script
    re_style=re.compile('<\s*style[^>]*>[^<]*<\s*/\s*style\s*>', re.I)  # style
    re_a=re.compile('<\s*a[^>]*>', re.I)  # a
    re_enda=re.compile('<\s*/\s*a\s*>', re.I)  # a


    htmlstr=re_script.sub('', htmlstr)
    htmlstr=re_style.sub('', htmlstr)
    htmlstr=re_a.sub('', htmlstr)
    htmlstr=re_enda.sub('', htmlstr)

    # 过滤HTML
    htmlstr=helpers.strip_tags(htmlstr)
    # 转译emoji
    htmlstr=emoji.demojize(htmlstr)
    # 遗漏的HTML转义
    htmlstr=html.unescape(htmlstr)
    htmlstr=html.escape(htmlstr)
    htmlstr=htmlstr.strip()
    return htmlstr


def reduction_content(content):
    rs = content\
        .replace(get_rep_html('p'),'<p>')\
        .replace(get_endrep_html('p'),'</p>') \
        .replace(get_rep_html('table'), '<div class=\"table\">') \
        .replace(get_endrep_html('table'), '</div>') \
        .replace(get_rep_html('tbody'), '') \
        .replace(get_endrep_html('tbody'), '') \
        .replace(get_rep_html('tr'), '<div class=\"table-tr\">') \
        .replace(get_endrep_html('tr'), '</div>') \
        .replace(get_rep_html('td'), '<div class=\"table-td\">') \
        .replace(get_endrep_html('td'), '</div>')

    return rs
