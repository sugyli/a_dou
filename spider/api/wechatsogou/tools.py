

def _replace_str_html(s):
    """替换html‘&quot;’等转义内容为正常内容

    Args:
        s: 文字内容

    Returns:
        s: 处理反转义后的文字
    """
    html_str_list = [
        ('&#39;', '\''),
        ('&quot;', '"'),
        ('&amp;', '&'),
        ('&yen;', '¥'),
        ('amp;', ''),
        ('&lt;', '<'),
        ('&gt;', '>'),
        ('&nbsp;', ' '),
        ('\\', '')
    ]
    for i in html_str_list:
        s = s.replace(i[0], i[1])
    return s

def replace_html(data):
    if isinstance(data, dict):
        return dict([(replace_html(k), replace_html(v)) for k, v in data.items()])
    elif isinstance(data, list):
        return [replace_html(l) for l in data]
    elif isinstance(data, str):
        return _replace_str_html(data)
    else:
        return data

def list_or_empty(content, contype=None):
    assert isinstance(content, list), 'content is not list: {}'.format(content)

    if content:
        return contype(content[0]) if contype else content[0]
    else:
        if contype:
            if contype == int:
                return 0
            elif contype == str:
                return ''
            elif contype == list:
                return []
            else:
                raise Exception('only can deal int str list')
        else:
            return ''

def get_first_of_element(element, sub, contype=None):
    """抽取lxml.etree库中elem对象中文字

    Args:
        element: lxml.etree.Element
        sub: str

    Returns:
        elem中文字
    """
    content = element.xpath(sub)
    return list_or_empty(content, contype)

def format_image_url(url):
    if isinstance(url, list):
        return [format_image_url(i) for i in url]

    if url.startswith('//'):
        url = 'https:{}'.format(url)
    return url

def get_elem_text(elem):
    """抽取lxml.etree库中elem对象中文字

    Args:
        elem: lxml.etree库中elem对象

    Returns:
        elem中文字
    """
    if elem != '':
        return ''.join([node.strip() for node in elem.itertext()])
    else:
        return ''


def may_int(i):
    try:
        return int(i)
    except Exception:
        return i
