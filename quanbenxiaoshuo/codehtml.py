import re,html
from pygments.formatter import Formatter
from pygments import highlight
from pygments.lexers import get_lexer_by_name
from pygments.lexers import guess_lexer
from pygments.token import Text, STANDARD_TYPES

from quanbenxiaoshuo import helpers
def _get_ttype_class(ttype):
    fname = STANDARD_TYPES.get(ttype)
    if fname:
        return fname
    aname = ''
    while fname is None:
        aname = '-' + ttype[-1] + aname
        ttype = ttype.parent
        fname = STANDARD_TYPES.get(ttype)
    return fname + aname

def _line_num_tag_gen():
    line_num = 0
    def result():
        nonlocal line_num
        line_num += 1
        return f'<div class="line-numbers"><div class="line-num" data-line-num="{line_num}"></div></div>'
    return result

class HtmlLiFormatter(Formatter):
    def __init__(self, **options):
        Formatter.__init__(self, **options)

    def _get_css_class(self, ttype):
        """Return the css class of this token type prefixed with
        the classprefix option."""
        ttypeclass = _get_ttype_class(ttype)
        if ttypeclass:
            return ttypeclass
        return ''

    def html_encode(self, value):
        if '<' in value:
            value = value.replace('<', '&lt;')
        if '>' in value:
            value = value.replace('>', '&gt;')
        return value

    def _get_css_classes(self, ttype):
        """Return the css classes of this token type prefixed with
        the classprefix option."""
        cls = self._get_css_class(ttype)
        while ttype not in STANDARD_TYPES:
            ttype = ttype.parent
            cls = self._get_css_class(ttype) + ' ' + cls
        return cls

    def format(self, tokensource, outfile):
        get_line_num_tag = _line_num_tag_gen()
        line_start_tag = '<li class="line">'
        line_end_tag = '</li>'

        code_tags = ['<ol class="code-container">']
        num_tags = ['<ol class="num-container">']

        line_value = ''

        outfile.write('<div class="code">')

        # 预处理
        temp_tokensource = []
        for ttype, value in tokensource:
            value = value.replace(' ', '&nbsp;')
            if ttype == Text and '\n' in value:
                values = re.findall(pattern='([^\n]*)(\n)([^\n]*)', string=value)

                for i in values:
                    for k in i:
                        if k != '':
                            temp_tokensource.append((ttype, k))
            else:
                temp_tokensource.append((ttype, value))

        for ttype, value in temp_tokensource:
            ttype_class = self._get_css_classes(ttype)

            value = self.html_encode(value)

            if value != '\n':
                line_value += f'<span class="{ttype_class}">{value}</span>'

            else:
                num_tags.append(get_line_num_tag())
                code_tags.append(f'{line_start_tag}<div class="highlight-code"><div class="code-line">{line_value}</div></div>{line_end_tag}\n')

                line_value = ''
        num_tags.append('</ol>')
        code_tags.append('</ol>')

        outfile.write(f'{"".join(num_tags)}{"".join(code_tags)}')
        outfile.write('</div>\n')


def code_to_html(match):
    #处理规则中的内容
    html = filter_htmlsbycode(match.group(0))

    type_and_content=re.findall(pattern='``````([\s\S]+?)``````'
                                , string=html)

    if len(type_and_content)>0:

        formatter = HtmlLiFormatter(linenos=True, style='colorful')
        code_content = type_and_content[0]

        substring=highlight(code=code_content
                            , lexer=guess_lexer(code_content)
                            , formatter=formatter)
        return substring

    return match.string

def filter_htmlsbycode(htmlstr):
    if not isinstance(htmlstr,str):
        return htmlstr
    htmlstr=html.unescape(htmlstr)
    # 先过滤CDATA
    re_cdata=re.compile('//<!\[CDATA\[[^>]*//\]\]>', re.I)  # 匹配CDATA
    re_script=re.compile('<\s*script[^>]*>[^<]*<\s*/\s*script\s*>', re.I)  # Script
    re_style=re.compile('<\s*style[^>]*>[^<]*<\s*/\s*style\s*>', re.I)  # style
    re_br=re.compile('<br\s*?/?>', re.I)  # 处理换行
    re_p=re.compile('</p>', re.I)  # 处理换行

    re_h=re.compile('</?\w+[^>]*>')  # HTML标签
    re_comment=re.compile('<!--[^>]*-->')  # HTML注释
    re_stopwords=re.compile('\u3000')  # 去除无用的'\u3000'字符

    s=re_p.sub('\n', htmlstr)

    s=re_cdata.sub('', s)  # 去掉CDATA
    s=re_script.sub('', s)  # 去掉SCRIPT
    s=re_style.sub('', s)  # 去掉style
    s=re_br.sub('\n', s)  # 将br转换为换行
    s=re_h.sub('', s)  # 去掉HTML 标签
    s=re_comment.sub('', s)  # 去掉HTML注释
    s=re_stopwords.sub('', s)
    # 去掉多余的空行
    blank_line=re.compile('\n+')
    s=blank_line.sub('\n', s)
    #s=replaceCharEntity(s)  # 替换实体
    return s

##替换常用HTML字符实体.
#使用正常的字符替换HTML中特殊的字符实体.
#你可以添加新的实体字符到CHAR_ENTITIES中,处理更多HTML字符实体.
#@param htmlstr HTML字符串.
def replaceCharEntity(htmlstr):
    CHAR_ENTITIES={'nbsp':' ',
                   '160':' ',
                    'lt':'<',
                   '60':'<',
                    'gt':'>',
                   '62':'>',
                    'amp':'&',
                   '38':'&',
                    'quot':'"'
                    ,'34':'"',}

    re_charEntity=re.compile(r'&#?(?P<name>\w+);')
    sz=re_charEntity.search(htmlstr)
    while sz:
        entity=sz.group()#entity全称，如&gt;
        key=sz.group('name')#去除&;后entity,如&gt;为gt
        try:
            htmlstr=re_charEntity.sub(CHAR_ENTITIES[key],htmlstr,1)
            sz=re_charEntity.search(htmlstr)
        except KeyError:
            #以空串代替
            htmlstr=re_charEntity.sub('',htmlstr,1)
            sz=re_charEntity.search(htmlstr)
    return htmlstr

def md_to_html(mdstr):
    #匹配到了进入code_to_html
    return re.sub(pattern='``````([\s\S]+?)``````', repl=code_to_html, string=mdstr)


# if __name__ == '__main__':
#
#     mdstr = """
#     ``````
#     </p>
#     <p style="white-space: normal;">
#         #!/bin/bash&nbsp;
#     </p>
#     <p style="white-space: normal;">
#         while true ; do
#     </p>
#     <p style="white-space: normal;">
#         <br/>
#     </p>
#     <p style="white-space: normal;">
#         &nbsp; id=`ps -ef | grep cpulimit | grep -v &quot;grep&quot; | awk &#39;{print $10}&#39; | tail -1`
#     </p>
#     <p style="white-space: normal;">
#         <br/>
#     </p>
#     <p style="white-space: normal;">
#         &nbsp; nid=`ps aux | awk &#39;{ if ( $3 &gt; 75 ) print $2 }&#39; | head -1`
#     </p>
#     <p style="white-space: normal;">
#         <br/>
#     </p>
#     <p style="white-space: normal;">
#         &nbsp; if [ &quot;${nid}&quot; != &quot;&quot; ] &amp;&amp; [ &quot;${nid}&quot; != &quot;${id}&quot; ] ; then
#     </p>
#     <p style="white-space: normal;">
#         <br/>
#     </p>
#     <p style="white-space: normal;">
#         &nbsp; &nbsp; cpulimit -p ${nid} -l 75 &amp;
#     </p>
#     <p style="white-space: normal;">
#         <br/>
#     </p>
#     <p style="white-space: normal;">
#         &nbsp; &nbsp; echo &quot;[`date`] CpuLimiter run for ${nid} `ps -ef | grep ${nid} | awk &#39;{print $8}&#39; | head -1`&quot; &gt;&gt; /root/cpulimit-log.log
#     </p>
#     <p style="white-space: normal;">
#         &nbsp; fi
#     </p>
#     <p style="white-space: normal;">
#         &nbsp; sleep 3
#     </p>
#     <p style="white-space: normal;">
#         done
#     </p>
#     <p style="white-space: normal;">
#     ``````
#     我是个垃圾
#     blank_line=re.compile('\n+')
#     s=blank_line.sub('\n', s)
#     s=replaceCharEntity(s)  # 替换实体
#     blank_line=re.compile('\n+')
#     s=blank_line.sub('\n', s)
#     s=replaceCharEntity(s)  # 替换实体
#
#     """
#     print(md_to_html(mdstr))
