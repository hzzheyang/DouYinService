import json
from pprint import pprint
import time
import hashlib
import requests
import base64
# from apps.infos import models
from apps.infos import models


class DouYinTools():
    def __init__(self):

        self.byteTable1 ="D6 28 3B 71 70 76 BE 1B A4 FE 19 57 5E 6C BC 21 B2 14 37 7D 8C A2 FA 67 55 6A 95 E3 FA 67 78 ED 8E 55 33 89 A8 CE 36 B3 5C D6 B2 6F 96 C4 34 B9 6A EC 34 95 C4 FA 72 FF B8 42 8D FB EC 70 F0 85 46 D8 B2 A1 E0 CE AE 4B 7D AE A4 87 CE E3 AC 51 55 C4 36 AD FC C4 EA 97 70 6A 85 37 6A C8 68 FA FE B0 33 B9 67 7E CE E3 CC 86 D6 9F 76 74 89 E9 DA 9C 78 C5 95 AA B0 34 B3 F2 7D B2 A2 ED E0 B5 B6 88 95 D1 51 D6 9E 7D D1 C8 F9 B7 70 CC 9C B6 92 C5 FA DD 9F 28 DA C7 E0 CA 95 B2 DA 34 97 CE 74 FA 37 E9 7D C4 A2 37 FB FA F1 CF AA 89 7D 55 AE 87 BC F5 E9 6A C4 68 C7 FA 76 85 14 D0 D0 E5 CE FF 19 D6 E5 D6 CC F1 F4 6C E9 E7 89 B2 B7 AE 28 89 BE 5E DC 87 6C F7 51 F2 67 78 AE B3 4B A2 B3 21 3B 55 F8 B3 76 B2 CF B3 B3 FF B3 5E 71 7D FA FC FF A8 7D FE D8 9C 1B C4 6A F9 88 B5 E5"
        self.STUB = ""
        self.cookies = "install_id=2119508445641277; ttreq=1$d4449484e9bca1c94de939e3f32544bb750458dc; passport_csrf_token=17eee33dcb95a35643cf6cf206520ce0; tt_webid=590a2d7dcb2f9c53e61e3d5a78303bf5; d_ticket=874ff6c9ee4ba589c65cadc587bd6c6c84b18; odin_tt=64f6c44bb868930111885ae5cb41071a9823b5187f99cb65cc1733ffda9ed5f60a1e23be62f19e298c0307c39a2aa176f0236b2d5d666c708de63130c62f8925; sid_guard=70ac71940abdbfc417fd1923ab800d3a%7C1592279181%7C5184000%7CSat%2C+15-Aug-2020+03%3A46%3A21+GMT; uid_tt=37f7256a3a8740bdf557f43464b9c4bd; sid_tt=70ac71940abdbfc417fd1923ab800d3a; sessionid=70ac71940abdbfc417fd1923ab800d3a"


    def getXGon(self, url, stub, cookies):
        NULL_MD5_STRING = "00000000000000000000000000000000"
        sb = ""
        if len(url) < 1:
            sb = NULL_MD5_STRING
        else:
            sb = self.encryption(url)
        if len(stub) < 1:
            sb += NULL_MD5_STRING
        else:
            sb += stub
        if len(cookies) < 1:
            sb += NULL_MD5_STRING
        else:
            sb += self.encryption(cookies)
        index = cookies.index("sessionid=")
        if index == -1:
            sb += NULL_MD5_STRING
        else:
            sessionid = cookies[index + 10:]
            if sessionid.__contains__(';'):
                endIndex = sessionid.index(';')
                sessionid = sessionid[:endIndex]
            sb += self.encryption(sessionid)
        return sb

    def encryption(self, url):
        obj = hashlib.md5()
        obj.update(url.encode("UTF-8"))
        secret = obj.hexdigest()
        return secret.lower()

    def initialize(self, data):
        myhex = 0
        byteTable2 = self.byteTable1.split(" ")
        for i in range(len(data)):
            hex1 = 0
            if i==0:
                hex1= int(byteTable2[int(byteTable2[0],16)-1],16)
                byteTable2[i]=hex(hex1)
                # byteTable2[i] = Integer.toHexString(hex1);
            elif i==1:
                temp=   int("D6",16)+int("28",16)
                if temp>256:
                    temp-=256
                hex1 = int(byteTable2[temp-1],16)
                myhex = temp
                byteTable2[i] = hex(hex1)
            else:
                temp = myhex+int(byteTable2[i], 16)
                if temp > 256:
                    temp -= 256
                hex1 = int(byteTable2[temp - 1], 16)
                myhex = temp
                byteTable2[i] = hex(hex1)
            if hex1*2>256:
                hex1 = hex1*2 - 256
            else:
                hex1 = hex1*2
            hex2 = byteTable2[hex1 - 1]
            result = int(hex2,16)^int(data[i],16)
            data[i] = hex(result)
        for i in range(len(data)):
            data[i] = data[i].replace("0x", "")
        return data

    def handle(self, data):
        for i in range(len(data)):
            byte1 = data[i]
            if len(byte1) < 2:
                byte1 += '0'
            else:
                byte1 = data[i][1] + data[i][0]
            if i < len(data) - 1:
                byte1 = hex(int(byte1, 16) ^ int(data[i + 1], 16)).replace("0x", "")
            else:
                byte1 = hex(int(byte1, 16) ^ int(data[0], 16)).replace("0x", "")
            byte1 = byte1.replace("0x", "")
            a = (int(byte1, 16) & int("AA", 16)) / 2
            a = int(abs(a))
            byte2 = ((int(byte1, 16) & int("55", 16)) * 2) | a
            byte2 = ((byte2 & int("33", 16)) * 4) | (int)((byte2 & int("cc", 16)) / 4)
            byte3 = hex(byte2).replace("0x", "")
            if len(byte3) > 1:
                byte3 = byte3[1] + byte3[0]
            else:
                byte3 += "0"
            byte4 = int(byte3, 16) ^ int("FF", 16)
            byte4 = byte4 ^ int("14", 16)
            data[i] = hex(byte4).replace("0x", "")
        return data

    def get_gorgon(self, timeMillis, inputBytes):
        data1 = []
        data1.append("3")
        data1.append("61")
        data1.append("41")
        data1.append("10")
        data1.append("80")
        data1.append("0")
        data2 = self.inputs(timeMillis, inputBytes)
        data2 = self.initialize(data2)
        data2 = self.handle(data2)
        for i in range(len(data2)):
            data1.append(data2[i])

        xGorgonStr = ""
        for i in range(len(data1)):
            temp = data1[i] + ""
            if len(temp) > 1:
                xGorgonStr += temp
            else:
                xGorgonStr += "0"
                xGorgonStr += temp
        return xGorgonStr

    def inputs(self, timeMillis, inputBytes):
        result = []
        for i in range(4):
            if inputBytes[i] < 0:
                temp = hex(inputBytes[i]) + ''
                temp = temp[6:]
                result.append(temp)
            else:
                temp = hex(inputBytes[i]) + ''
                result.append(temp)
        for i in range(4):
            result.append("0")
        for i in range(4):
            if inputBytes[i + 32] < 0:
                result.append(hex(inputBytes[i + 32]) + '')[6:]
            else:
                result.append(hex(inputBytes[i + 32]) + '')
        for i in range(4):
            result.append("0")
        tempByte = hex(int(timeMillis)) + ""
        tempByte = tempByte.replace("0x", "")
        for i in range(4):
            a = tempByte[i * 2:2 * i + 2]
            result.append(tempByte[i * 2:2 * i + 2])
        for i in range(len(result)):
            result[i] = result[i].replace("0x", "")
        return result

    def strToByte(self, str):
        length = len(str)
        str2 = str
        bArr = []
        i = 0
        while i < length:
            # bArr[i/2] = b'\xff\xff\xff'+(str2hex(str2[i]) << 4+str2hex(str2[i+1])).to_bytes(1, "big")
            a = str2[i]
            b = str2[1 + i]
            c = ((self.str2hex(a) << 4) + self.str2hex(b))
            bArr.append(c)
            i += 2
        return bArr

    def str2hex(self,s):
        odata = 0
        su = s.upper()
        for c in su:
            tmp = ord(c)
            if tmp <= ord('9'):
                odata = odata << 4
                odata += tmp - ord('0')
            elif ord('A') <= tmp <= ord('F'):
                odata = odata << 4
                odata += tmp - ord('A') + 10
        return odata

    def get_global_search_data(self, keywork, curosr):
        data_dict = {
            'user_list': []
        }
        ts = str(time.time()).split(".")[0]
        rticket = str(time.time() * 1000).split(".")[0]
        cursor = curosr * 10
        k = 'cursor={}&keyword={}&count=10&type=1&is_pull_refresh=1&hot_search=0&search_source=&search_id=&query_correct_type=1'\
            .format(cursor, keywork)
        hl = hashlib.md5()
        hl.update(str(k).encode(encoding='utf-8'))
        sign2 = hl.hexdigest().upper()
        url = 'https://aweme-hl.snssdk.com/aweme/v1/discover/search/?os_api=23&device_type=MI%205s&device_platform=android&ssmix=a&iid=1028786593992525&manifest_version_code=100501&dpi=320&uuid=008796760665134&version_code=100500&app_name=aweme&cdid=9039c8c0-66b3-4992-a2ca-e1a90e98d3ba&version_name=10.5.0&ts={}&openudid=75f0c9390fb221d9&device_id=78804984545944&resolution=800*1280&os_version=6.0.1&language=zh&device_brand=Xiaomi&app_type=normal&ac=wifi&update_version_code=10509900&aid=1128&channel=tengxun_new&_rticket={}'.format(
            ts, rticket)

        params = url[url.index('?') + 1:]
        s = self.getXGon(params, self.STUB, self.cookies)
        gorgon = self.get_gorgon(ts, self.strToByte(s))
        global_search_headers = {
            'X-SS-STUB': sign2,
            'Accept-Encoding': 'gzip',
            'X-SS-REQ-TICKET': rticket,
            'sdk-version': '1',
            'Cookie': self.cookies,
            'x-tt-token': '0070ac71940abdbfc417fd1923ab800d3a9ef0a53f584a09126dabb112d9b1000f04168e8e2016ab12848bb30a01bdbf9514',
            'X-Gorgon': gorgon,
            'X-Khronos': ts,
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'Content-Length': '138',
            'Host': 'aweme-hl.snssdk.com',
            'Connection': 'Keep-Alive',
            'User-Agent': 'okhttp/3.10.0.1',
        }
        data = {
            'cursor': '{}'.format(cursor),
            'keyword': '{}'.format(keywork),
            'count': '10',
            'type': '1',
            'is_pull_refresh': '1',
            'hot_search': '0',
            'search_source': '',
            'search_id': '',
            'query_correct_type': '1'
        }

        response = requests.post(url, headers=global_search_headers, data=data, verify=False)
        datas = json.loads(response.text)['user_list']
        if datas != '':
            for index, data in enumerate(datas):
                # uid (用于跳转)
                base_dict = {'uid': data['user_info']['uid']}
                authorinfo = models.Author.objects.filter(author_uid=base_dict['uid'])
                if authorinfo.exists():
                    pass
                else:
                    # short_id (抖音id)
                    base_dict['short_id'] = data['user_info']['short_id']

                    base_dict['author_name'] = data['user_info']['nickname']
                    try:
                        gender = data['user_info']['gender']
                        if gender is 0:
                            base_dict['author_gender'] = '未知'
                        elif gender is 1:
                            base_dict['author_gender'] = '男'
                        elif gender is 2:
                            base_dict['author_gender'] = '女'
                    except:
                        base_dict['gender'] = '未知'

                    # 签名
                    signature = data['user_info']['signature']
                    content = ''
                    for i in signature:
                        content = content + i.strip()
                        base_dict['signature'] = content

                    # 粉丝数
                    try:
                        base_dict['author_fans_num'] = data['user_info']['follower_count']
                    except:
                        base_dict['author_fans_num'] = 0

                    # 获赞数
                    try:
                        base_dict['author_favorited'] = data['user_info']['total_favorited']
                    except:
                        base_dict['author_favorited'] = '未知'

                    # 作品数
                    base_dict['author_aweme_count'] = data['user_info']['aweme_count']
                    # 抖音号
                    base_dict['author_unique_id'] = data['user_info']['unique_id']
                    # sec_uid
                    base_dict['sec_uid'] = data['user_info']['sec_uid']

                    data_dict['user_list'].append(base_dict)

            return ({
                'status': 0,
                'msg': '请求成功',
                'results': data_dict,
            })

        elif data == '':
            return ({
                'status': 1,
                'msg': '抖音爬虫发生错误',
            })

    def get_fans_list(self, uid, sec_user_id, max_time, fan_psc, id):
        data_dict = {
            'fans_list': []
        }

        ts = str(time.time()).split(".")[0]
        rticket = str(time.time() * 1000).split(".")[0]
        url = 'https://aweme-hl.snssdk.com/aweme/v1/user/follower/list/?user_id={}&' \
              'sec_user_id={}&max_time={}' \
              '&count=10&offset=0&source_type=1&address_book_access=1&gps_access=1&vcd_count=0' \
              '&os_api=23&device_type=MI%205s&device_platform=android&ssmix=a&iid=1028786593992525' \
              '&manifest_version_code=100501&dpi=320&uuid=008796760665134&version_code=100500&app_name=aweme' \
              '&cdid=9039c8c0-66b3-4992-a2ca-e1a90e98d3ba&version_name=10.5.0&ts=1591177984' \
              '&openudid=75f0c9390fb221d9&device_id=78804984545944&resolution=800*1280&os_version=6.0.1' \
              '&language=zh&device_brand=Xiaomi&app_type=normal&ac=wifi&update_version_code=10509900&aid=1128' \
              '&channel=tengxun_new&_rticket={}'.format(uid, sec_user_id, max_time, rticket)

        params = url[url.index('?') + 1:]
        s = self.getXGon(params, self.STUB, self.cookies)
        gorgon = self.get_gorgon(ts, self.strToByte(s))
        get_fans_headers = {
            "X-Gorgon": gorgon,
            "X-Khronos": ts,
            "sdk-version": "1",
            "Accept-Encoding": "gzip",
            "X-SS-REQ-TICKET": rticket,
            "User-Agent": "ttnet okhttp/3.10.0.2",
            "Host": "api3-core-c-lf.amemv.com",
            "Cookie": self.cookies,
            "Connection": "Keep-Alive",
            "x-tt-token": "00c6a430522b3ed5db456f8fd621dd6386366c966556c2162dfa8d62a1802a64f6c265554f0ef0ceadfb6be24ba6ee4c9a30"
        }
        try:
            req = requests.get(url, headers=get_fans_headers, verify=False)
            response = json.loads(req.text)
            data_dict['offset'] = response['offset']
            data_dict['min_time'] = response['min_time']
            datas = response['followers']
            for data in datas:
                base_dict = {}
                try:
                    gender = data['gender']
                    if gender is 0:
                        base_dict['gender'] = '未知'
                    elif gender is 1:
                        base_dict['gender'] = '男'
                    elif gender is 2:
                        base_dict['gender'] = '女'
                except:
                    base_dict['gender'] = '未知'

                a = data['nickname']
                d = base64.b64encode(a.encode('utf-8'))
                base_dict['fan_name'] = str(d, 'utf-8')

                base_dict['fan_sec_uid'] = data['sec_uid']
                base_dict['fan_uid'] = data['uid']
                base_dict['department'] = id

                data_dict['fans_list'].append(base_dict)

            return data_dict

        except Exception as f:
            return {
                'fans_list': []
            }






