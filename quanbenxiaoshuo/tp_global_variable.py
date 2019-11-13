from albums.models import Category


def read_settings_file(request):

    return {
        'WEBNAME': '数据之家',
        'WEBTITLE': '大书包小说网_大书包图书馆_大书包资料馆',
        'WEBKW': '大书包,小说网,图书馆,资料馆',
        'WEBDES': '大书包收藏了大量的小说、图书、和互联网各行各业资料,免费对网友开放,提供免费在线阅读等服务'
    }
