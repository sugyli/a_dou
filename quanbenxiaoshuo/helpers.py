import html,re




def __basereplace(htmlstr):
    #把HTML转义字符 反转义
    htmlstr = html.unescape(htmlstr)
    htmlstr = htmlstr.replace('\n', '')
    htmlstr = htmlstr.replace('\r', '')
    htmlstr = htmlstr.replace(' ', '')

    re_stopwords=re.compile('\u3000', re.I)
    htmlstr =re_stopwords.sub('', htmlstr)

    return htmlstr

def descriptionreplace(htmlstr):
    if not isinstance(htmlstr,str):
        return htmlstr
    htmlstr = __basereplace(htmlstr)
    re_script = re.compile('<\s*script[^>]*>[^<]*<\s*/\s*script\s*>',re.I)  # Script
    re_style = re.compile('<\s*style[^>]*>[^<]*<\s*/\s*style\s*>', re.I)  # style
    re_cdata = re.compile(r'<[^>]+>', re.I)

    htmlstr = re_script.sub('', htmlstr)
    htmlstr = re_style.sub('', htmlstr)
    htmlstr = re_cdata.sub('', htmlstr)

    return htmlstr

