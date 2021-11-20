import requests
import re
import execjs
import json


class BaiDu_FanYi(object):

    def __init__(self):
        # 设置 url
        self.sign_url = 'https://fanyi.baidu.com/v2transapi?from=zh&to=en'
        self.token_url = 'https://fanyi.baidu.com/'
        self.lan_url = 'https://fanyi.baidu.com/langdetect'
        self.fanyi_url = None
        # 设置请求头
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.82 Safari/537.36',
            'Referer': 'https://fanyi.baidu.com/',
            'Cookie': 'BAIDUID=070900C3687ED8D716A622B72D844144:FG=1; Hm_lvt_64ecd82404c51e03dc91cb9e8c025574=1636719409; __yjs_duid=1_7b81f444ae26e8c4b848367282b895731636719409492; REALTIME_TRANS_SWITCH=1; FANYI_WORD_SWITCH=1; HISTORY_SWITCH=1; SOUND_SPD_SWITCH=1; SOUND_PREFER_SWITCH=1; Hm_lpvt_64ecd82404c51e03dc91cb9e8c025574=1636719410; __yjs_st=2_Y2FlZTAwMjZhYzA3NDVjMDcxNGYwNzdiZjUwZjM0NGFlMzE3YjA3OThhNTAzYjgwMTliNDcxMmQxMGI1MmI0YTJhMGQ2ZTk2ODZhN2ZjNTliYmY3MTdjMzRjYTFmMzkyZDk2ZGUzMWRiZTJlMDA5MjExOTg0YjBkZDE1OTBiMzcxY2UyZGM2NjJmODI2OGU5NWIxNGU3NWY3MDUzY2QwM2M5NWNmMjM0NTE5OGM5OGFmZjQ4NjYxNDI4YWE2MGRkM2U0MWQ1NGQ1ZDE3ZjA3YjE1MTM3OTFhMDVjMjcwNzYwYzA2YTJlZWJmNGY5ZTZkYmIwZTU1MzhkMTVjYWFhZl83XzVhMDQ1YjE3; ab_sr=1.0.1_OWVlYWE5NzE0MDZjYzE5NzVkMTllNTNiNTgyZjVkYWJiMWUyYzcyNGM0ZTQ1ZDY5YjY4OGY1NTMzMmM3YjYwZDE0ZWVlZjQyZTIwMWFjZGJkNjYyM2VkMTdiNDNkZTVlOTEyYjk1OGVmMGIyMTY4YjUzOWRkMjQ0NzM5MzRlMGRjNDI5N2RmMzQ1MmE0NzIyZDFkMjEwYzgxYzQyNjJhZQ=='
        }
        # 设置翻译语言的语种
        self.lan_from = None
        self.lan_to = None
        # 设置会话
        self.session = requests.session()

    # 获取翻译语言是中文还是英文
    def get_lan_detect(self, content):
        # 发送请求
        response = self.session.get(self.lan_url + '?query=' + content, headers=self.headers)
        # 获取返回的数据
        res_json = response.content.decode()
        dict_json = json.loads(res_json)
        self.lan_from = dict_json['lan']
        # 选择语种
        if self.lan_from == 'zh':
            self.lan_to = 'en'
        else:
            self.lan_to = 'zh'

    # 获取 token
    def get_token(self):
        # 发送请求
        response = self.session.get(self.token_url, headers=self.headers)
        # 返回 token
        return re.findall("token: '(.*?)'", response.content.decode())[0]

    # 获取 sign
    def get_sign(self, content):
        # 获取 js 文件翻译成 python 代码
        # with open('fanyi.js', 'rb') as f:
        #     fanyi_js = f.read().decode(encoding='UTF-8')
        context = execjs.compile(self.get_sing_js().encode('utf-8', 'ignore').decode('utf-8', 'ignore'))
        # 返回解析后的 sign
        return context.call('e', content)

    # 运行函数
    def fanyi_run(self):
        content = input('输入翻译内容: ')
        # 获取 lan_from, lan_to
        self.get_lan_detect(content)
        # 获取 sing
        sing = self.get_sign(content)
        # 获取 token
        token = self.get_token()
        # Post 请求参数
        self.data = {
            'from': self.lan_from,
            'to': self.lan_to,
            'query': content.encode(),
            'transtype': 'translang',
            'simple_means_flag': '3',
            'sign': sing,
            'token': token,
            'domain': 'common'
        }
        # 发送翻译请求
        self.fanyi_url = 'https://fanyi.baidu.com/v2transapi' + '?from=' + self.lan_from + '&to=' + self.lan_to
        response = self.session.post(self.fanyi_url, data=self.data, headers=self.headers)
        # 服务器返回的 json 数据
        res_json = response.content.decode()
        # 将 json 字符串转为字典
        dict_result = json.loads(res_json)
        # 解析 json 数据结果
        # 翻译原文
        # fanyi_src = dict_result['trans_result']['data'][0]['src']
        # 翻译结果
        fanyi_result = dict_result['trans_result']['data'][0]['result'][0][1]
        print(f'\n翻译结果=========>  {fanyi_result}\n\n')

    @staticmethod
    def get_sing_js():
        return """
        function n(r, o) {
        for (var t = 0; t < o.length - 2; t += 3) {
            var a = o.charAt(t + 2);
            a = a >= "a" ? a.charCodeAt(0) - 87 : Number(a),
            a = "+" === o.charAt(t + 1) ? r >>> a : r << a,
            r = "+" === o.charAt(t) ? r + a & 4294967295 : r ^ a
        }
        return r
    }

    function e(r) {
        var o = r.match(/[\uD800-\uDBFF][\uDC00-\uDFFF]/g);
        if (null === o) {
            var t = r.length;
            t > 30 && (r = "" + r.substr(0, 10) + r.substr(Math.floor(t / 2) - 5, 10) + r.substr(-10, 10))
        } else {
            for (var e = r.split(/[\uD800-\uDBFF][\uDC00-\uDFFF]/), C = 0, h = e.length, f = []; h > C; C++)
                "" !== e[C] && f.push.apply(f, a(e[C].split(""))),
                C !== h - 1 && f.push(o[C]);
            var g = f.length;
            g > 30 && (r = f.slice(0, 10).join("") + f.slice(Math.floor(g / 2) - 5, Math.floor(g / 2) + 5).join("") + f.slice(-10).join(""))
        }
        var u = "320305.131321201"
          , l = "" + String.fromCharCode(103) + String.fromCharCode(116) + String.fromCharCode(107);
        // u = null !== i ? i : (i = window[l] || "") || "";
        for (var d = u.split("."), m = Number(d[0]) || 0, s = Number(d[1]) || 0, S = [], c = 0, v = 0; v < r.length; v++) {
            var A = r.charCodeAt(v);
            128 > A ? S[c++] = A : (2048 > A ? S[c++] = A >> 6 | 192 : (55296 === (64512 & A) && v + 1 < r.length && 56320 === (64512 & r.charCodeAt(v + 1)) ? (A = 65536 + ((1023 & A) << 10) + (1023 & r.charCodeAt(++v)),
            S[c++] = A >> 18 | 240,
            S[c++] = A >> 12 & 63 | 128) : S[c++] = A >> 12 | 224,
            S[c++] = A >> 6 & 63 | 128),
            S[c++] = 63 & A | 128)
        }
        for (var p = m, F = "" + String.fromCharCode(43) + String.fromCharCode(45) + String.fromCharCode(97) + ("" + String.fromCharCode(94) + String.fromCharCode(43) + String.fromCharCode(54)), D = "" + String.fromCharCode(43) + String.fromCharCode(45) + String.fromCharCode(51) + ("" + String.fromCharCode(94) + String.fromCharCode(43) + String.fromCharCode(98)) + ("" + String.fromCharCode(43) + String.fromCharCode(45) + String.fromCharCode(102)), b = 0; b < S.length; b++)
            p += S[b],
            p = n(p, F);
        return p = n(p, D),
        p ^= s,
        0 > p && (p = (2147483647 & p) + 2147483648),
        p %= 1e6,
        p.toString() + "." + (p ^ m)
    }
        """


if __name__ == '__main__':
    baidu_fanyi = BaiDu_FanYi()
    print('-' * 10 + 'Author: Mr.Yu' + '-' * 10, end='\n\n')
    while True:
        try:
            baidu_fanyi.fanyi_run()
        except Exception as e:
            print('语种还未录入, 请联系开发人员哦~')
            break
