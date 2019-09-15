import html,re,emoji,random,os,sys
from html.parser import HTMLParser


filterstr = \
"""
落l霞x小x说s=Www*luoxia*com
落l霞x小x说=Www*luoxia*com
落`霞-小`说www，luoxia，com
落·霞^小·说wWW…luoxia…com…
落l霞x小x说s=www*luoxia*Com
落#霞#小#说#www#luoxia#com
落^霞^小^说…
落l霞x小x说s
落l霞x小x说
"""



class MLStripper(HTMLParser):
    """
    过滤html方法
    """

    def __init__(self, *, convert_charrefs=True):
        self.convert_charrefs = convert_charrefs
        self.reset()
        self.fed = []

    def handle_data(self, d):
        self.fed.append(d)

    def get_data(self):
        text = ''
        for row in self.fed:
            if row.strip():
                text += row

        return text

def strip_tags(html):
    """
    过滤html方法实现
    """
    if html is None:
        return ""
    s = MLStripper()
    s.feed(html)
    return s.get_data()

def __basereplace(htmlstr):
    #把HTML转义字符 反转义 html.escape转义
    #htmlstr = html.unescape(htmlstr)
    htmlstr = htmlstr.replace('\r', '').replace('\t', '')
    re_stopwords=re.compile('\u3000', re.I)
    htmlstr =re_stopwords.sub('', htmlstr)

    return htmlstr


def descriptionreplace(htmlstr):
    if not isinstance(htmlstr,str):
        return htmlstr
    elif not htmlstr.strip():
        return htmlstr

    htmlstr = __basereplace(htmlstr)
    htmlstr = htmlstr.replace('\n', '')

    re_script = re.compile('<\s*script[^>]*>[^<]*<\s*/\s*script\s*>',re.I)  # Script
    re_style = re.compile('<\s*style[^>]*>[^<]*<\s*/\s*style\s*>', re.I)  # style
    re_a = re.compile('<\s*a[^>]*>[^<]*<\s*/\s*a\s*>', re.I)  # a
    htmlstr = re_script.sub('', htmlstr)
    htmlstr = re_style.sub('', htmlstr)
    htmlstr = re_a.sub('', htmlstr)

    #过滤HTML
    #htmlstr = strip_tags(htmlstr)
    #过滤emoji
    htmlstr = emoji.demojize(htmlstr)
    #过滤空格
    htmlstr = htmlstr.replace(' ', '')
    #遗漏的HTML转义
    htmlstr = html.unescape(htmlstr)
    htmlstr = html.escape(htmlstr)


    return htmlstr

#使用内容过滤会自动加emoji 输出的时候
def contentreplace(text ,out = True):
    if not isinstance(text,str):
        return text
    elif not text.strip():
        return text

    text = __basereplace(text)
    re_script = re.compile('<\s*script[^>]*>[^<]*<\s*/\s*script\s*>',re.I)  # Script
    re_style = re.compile('<\s*style[^>]*>[^<]*<\s*/\s*style\s*>', re.I)  # style
    re_a=re.compile('<\s*a[^>]*>[^<]*<\s*/\s*a\s*>', re.I)  # a
    text = re_script.sub('', text)
    text = re_style.sub('', text)
    text = re_a.sub('', text)

    text=text.split('\n')
    html=''
    i = 0
    l = int(len(text)*0.3)
    l  = l if l > 3 else 3

    for row in text:
        i += 1
        row = row.strip()
        row = descriptionreplace(row)
        if row:
            if out:
                if l == i:
                    html+=f"<p>$$$$$$1{row}$$$$$$2</p>"
                else:
                    html+=f"<p>{row}</p>"
            else:
                html+=f"{row}\n\r"

    if out:
        html = re.sub(r':[a-zA-Z0-9_]+?:', '', html)
        html = customfilterstr(html)
        #emoji的处理
        e = [
            ':thumbs_up:',
            ':ghost:',
            ':fire:',
            ':monkey:',
            ':dog:',
            ':poodle:',
            ':mouse:',
            ':rat:',
            ':rabbit:',
            ':red_apple:'
        ]
        html = \
            html.replace('$$$$$$1',str(random.choice(e))).replace('$$$$$$2', str(random.choice(e)))
        html = emoji.emojize(html)
        html = html.replace('口','𥁐')

    return html



def customfilterstr(htmlstr,filterstr=filterstr):
    filterstr = filterstr.split('\n')
    filterstr = [row for row in filterstr if row.strip()]
    #filterstr = list(set(filterstr))
    filterstr = [i for n, i in enumerate(filterstr) if i not in filterstr[:n]]

    for s in filterstr:
        htmlstr = htmlstr.replace(s, '')

    return htmlstr
