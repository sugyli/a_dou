String.prototype.format = function() {
    var c = this;
    for (var b = 0,
    a = arguments.length; b < a; b++) {
        c = c.replace("{" + (b) + "}", arguments[b])
    }
    return (c)
};
var Cookie = {
  Set: function() {
      var name = arguments[0],
      value = escape(arguments[1]),
      days = (arguments.length > 2) ? arguments[2] : 365,
      path = (arguments.length > 3) ? arguments[3] : "/";
      with(new Date()) {
          setDate(getDate() + days);
          days = toUTCString()
      }
      document.cookie = "{0}={1};expires={2};path={3}".format(name, value, days, path)
  },
  Get: function() {
      var a = document.cookie.match(new RegExp("[\b^;]?" + arguments[0] + "=([^;]*)(?=;|\b|$)", "i"));
      return a ? unescape(a[1]) : a
  },
  Delete: function() {
      var a = arguments[0];
      document.cookie = a + "=1 ; expires=Fri, 31 Dec 1900 23:59:59 GMT;"
  }
};


function tj(){
    var _hmt = _hmt || [];
    (function() {
      var hm = document.createElement("script");
      hm.src = "https://hm.baidu.com/hm.js?13c857eb9c008d0221f93dd89794c1e0";
      var s = document.getElementsByTagName("script")[0];
      s.parentNode.insertBefore(hm, s);
    })();
}

function pushdata(){
    (function(){
        var bp = document.createElement('script');
        var curProtocol = window.location.protocol.split(':')[0];
        if (curProtocol === 'https') {
            bp.src = 'https://zz.bdstatic.com/linksubmit/push.js';
        }
        else {
            bp.src = 'http://push.zhanzhang.baidu.com/push.js';
        }
        var s = document.getElementsByTagName("script")[0];
        s.parentNode.insertBefore(bp, s);
    })();
}
