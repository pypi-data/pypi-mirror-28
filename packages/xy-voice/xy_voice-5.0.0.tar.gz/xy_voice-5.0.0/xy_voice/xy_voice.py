import sys
import json
import time
import base64
import urllib.request as req
import urllib.parse as urlp
import requests
import webbrowser
import wave, pyaudio
import pinyinxy1


class xy_speech:
    CU_ID = 'testai'
    API_KEY = 'zbZo970ra5cjjP3IMECPW8lZ'
    API_SECERT = 'L2BN2GRXWiPDqC5HRL8H9hQI5r4Tz2af'
    CHUNK = 1024
    FORMAT = pyaudio.paInt16
    RATE = 16000
    CHANNELS = 1
    RECORD_SECONDS = 5
    URLS = {
        'baidu':'http://www.baidu.com',
        'google':'http://www.google.com',
        'yuanfudao':'http://yuanfudao.com',
        'cat':'http://image.baidu.com/search/index?tn=baiduimage&ps=1&ct=201326592&lm=-1&cl=2&nc=1&ie=utf-8&word=%E7%8C%AB',
        'dog':'https://image.baidu.com/search/index?tn=baiduimage&ipn=r&ct=201326592&cl=2&lm=-1&st=-1&fm=result&fr=&sf=1&fmq=1515408520455_R&pv=&ic=0&nc=1&z=&se=1&showtab=0&fb=0&width=&height=&face=0&istype=2&ie=utf-8&word=%E7%8B%97',
        'xiaoyuan':'http://www.yuanfudao.com/info/emojis'
    }

    def __init__(self):
        '''
        tex	必填	合成的文本，使用UTF-8编码。小于512个中文字或者英文数字。（文本在百度服务器内转换为GBK后，长度必须小于1024字节）
        tok	必填	开放平台获取到的开发者access_token（见上面的“鉴权认证机制”段落）
        cuid	必填	用户唯一标识，用来区分用户，计算UV值。建议填写能区分用户的机器 MAC 地址或 IMEI 码，长度为60字符以内
        ctp	必填	客户端类型选择，web端填写固定值1
        lan	必填	固定值zh。语言选择,目前只有中英文混合模式，填写固定值zh
        spd	选填	语速，取值0-9，默认为5中语速
        pit	选填	音调，取值0-9，默认为5中语调
        vol	选填	音量，取值0-15，默认为5中音量
        per	选填	发音人选择, 0为普通女声，1为普通男生，3为情感合成-度逍遥，4为情感合成-度丫丫，默认为普通女声
        '''
        self.token_url = 'http://openapi.baidu.com/oauth/2.0/token?grant_type=client_credentials&client_id=%s&client_secret=%s'
        self.getvoice_url = 'http://tsn.baidu.com/text2audio?tex=%s&lan=zh&cuid=%s&ctp=1&tok=%s&spd=5&pit=5&vol=5&per=0'
        self.upvoice_url = 'http://vop.baidu.com/server_api'
        self.get_token(self.API_KEY,self.API_SECERT)
        return

    # 获取token
    def get_token(self, api_key, api_secert):
        token_url = self.token_url % (api_key, api_secert)
        r_str = req.urlopen(token_url).read()
        token_data = json.loads(r_str)
        self.token_str = token_data['access_token']
        return True

    # 语音合成
    def text2voice(self, text, filename):
        get_url = self.getvoice_url % (urlp.quote(text), self.CU_ID, self.token_str)
        voice_data = req.urlopen(get_url).read()
        voice_fp = open(filename,'wb+')
        voice_fp.write(voice_data)
        voice_fp.close()
        return True

    # 语音识别
    def voice2text(self, filename):
        data = {}
        data['format'] = 'wav'
        data['rate'] = 16000
        data['channel'] = 1
        data['cuid'] = self.CU_ID
        data['token'] = self.token_str

        wav_fp = open(filename,'rb')
        voice_data = wav_fp.read()
        wav_fp.close()
        data['len'] = len(voice_data)
        data['speech'] = base64.b64encode(voice_data).decode('utf-8')
        result = requests.post(self.upvoice_url, json=data, headers={'Content-Type':'application/json'})
        data_result = result.json()
        if data_result['err_no'] == 0:
            return data_result['result'][0]
        else:
            return -1




    def record(self,filename,to_dir=None):
        if to_dir is None:
            to_dir = "./"

        pa = pyaudio.PyAudio()
        stream = pa.open(format = self.FORMAT,
                         channels = self.CHANNELS,
                         rate = self.RATE,
                         input = True,
                         frames_per_buffer = self.CHUNK)

        print("* recording")

        save_buffer = []
        for i in range(0, int(self.RATE / self.CHUNK * self.RECORD_SECONDS)):
            audio_data = stream.read(self.CHUNK)
            save_buffer.append(audio_data)

        print("* done recording")

        # stop
        stream.stop_stream()
        stream.close()
        pa.terminate()

        if to_dir.endswith('/'):
            file_path = to_dir + filename
        else:
            file_path = to_dir + "/" + filename

        # save file
        wf = wave.open(file_path, 'wb')
        wf.setnchannels(self.CHANNELS)
        wf.setsampwidth(pa.get_sample_size(self.FORMAT))
        wf.setframerate(self.RATE)
        # join 前的类型
        wf.writeframes(b''.join(save_buffer))
        wf.close()

        return file_path

    def browser_open_text(self,text):
        if text is None:
            return
        res = pinyinxy1.get_pinyin(text)
        res = res.replace('-','')
        if res.startswith("baidu") or res.startswith("bai"):
            url = self.URLS['baidu']
        elif res.startswith("guge") or res.startswith("google"):
            url = self.URLS['google']
        elif res.startswith('yuanfudao') or res.startswith('yuan'):
            url = self.URLS['yuanfudao']
        elif res.startswith('xiaoyuan') or res.startswith('xiao'):
            url = self.URLS['xiaoyuan']
        elif res.startswith('cat') or res.startswith('mao'):
            url = self.URLS['cat']
        elif res.startswith('dog') or res.startswith('gou'):
            url = self.URLS['dog']
        else:
            url = "http://www.baidu.com"

        webbrowser.open_new_tab(url)
