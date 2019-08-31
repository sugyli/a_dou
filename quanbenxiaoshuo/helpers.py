import html,re
from html.parser import HTMLParser




def __basereplace(htmlstr):
    #把HTML转义字符 反转义 html.escape转义
    htmlstr = html.unescape(htmlstr)
    htmlstr = htmlstr.replace('\n', '')
    htmlstr = htmlstr.replace('\r', '')
    re_stopwords=re.compile('\u3000', re.I)
    htmlstr =re_stopwords.sub('', htmlstr)

    return htmlstr


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


def descriptionreplace(htmlstr):
    if not isinstance(htmlstr,str):
        return htmlstr
    elif not htmlstr.strip():
        return htmlstr

    htmlstr = __basereplace(htmlstr)

    re_script = re.compile('<\s*script[^>]*>[^<]*<\s*/\s*script\s*>',re.I)  # Script
    re_style = re.compile('<\s*style[^>]*>[^<]*<\s*/\s*style\s*>', re.I)  # style
    re_a=re.compile('<\s*a[^>]*>[^<]*<\s*/\s*a\s*>', re.I)  # a
    htmlstr = re_script.sub('', htmlstr)
    htmlstr = re_style.sub('', htmlstr)
    htmlstr = re_a.sub('', htmlstr)

    #过滤HTML
    htmlstr = strip_tags(htmlstr)
    htmlstr = htmlstr.replace(' ', '')
    #遗漏的HTML转义
    htmlstr = html.escape(htmlstr)

    return htmlstr



def contentreplace(text ,out = True):
    if not isinstance(text,str):
        return text
    elif not text.strip():
        return text

    text=text.replace('\r', '')
    text=text.replace('\t', '')
    re_script = re.compile('<\s*script[^>]*>[^<]*<\s*/\s*script\s*>',re.I)  # Script
    re_style = re.compile('<\s*style[^>]*>[^<]*<\s*/\s*style\s*>', re.I)  # style
    re_a=re.compile('<\s*a[^>]*>[^<]*<\s*/\s*a\s*>', re.I)  # a
    text = re_script.sub('', text)
    text = re_style.sub('', text)
    text = re_a.sub('', text)

    text=text.split('\n')
    html=''
    for row in text:
        row = row.strip()
        row = descriptionreplace(row)
        if row:
            if out:
                html+=f"<p>{row}</p>"
            else:
                html+=f"{row}\n"

    return html
