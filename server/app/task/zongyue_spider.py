# -*- coding: utf-8 -*-
# @Time    : 2020/11/7 8:25 下午
# @Author  : xu.junpeng

import urllib.request
import time
from bs4 import BeautifulSoup


class Spider():
    def __init__(self, start_page, end_page, url=None):
        self.url = url or "https://tieba.baidu.com/p/7065584369?pn={}"
        self.start_page = start_page
        self.end_page = end_page
        self.headers = {
            'Connection': 'keep-alive',
            'Accept': '*/*',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36',
            'X-Requested-With': 'XMLHttpRequest',
            'Referer': 'http://c.tieba.baidu.com/f?ie=utf-8&kw=%E7%BA%B5%E6%9C%88%E5%85%AD%E5%8F%AA%E9%B9%85&fr=search',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'Cookie': """BIDUPSID=C2A78D239BC405CED7525FB88989A9B8; PSTM=1565175488; TIEBA_USERTYPE=8def743958a4e05f1006f310; \BAIDUID=8549F498475D4F4949EEEB4F54BE5B39FG=1; BDSFRCVID=GRFOJexroG3oFEO
rEzU1JRGlC2KK0gOTDYLEOwXPsp3LGJLVN4vPEG0Pt_U-mEt-J8jwogKK0gOTH6KF_2uxOjjg8UtVJeC6EG0Ptf8g0M5; H_BDCLCKID_SF=tbkD_C-MfIvDqTrP-trf5DCShUFsqPrRB2Q-XPoO3KOosl5OKxo03f-p04JQ35jiWbRM2MbgylRp8P3y0bb2DUA1
y4vpWj3qLgTxoUJ2XMKVDq5mqfCWMR-ebPRiJPb9Qg-qahQ7tt5W8ncFbT7l5hKpbt-q0x-jLTnhVn0MBCK0hI0ljj82e5PVKgTa54cbb4o2WbCQ2f7O8pcN2b5oQTteQ4o9bfQEQRvZbq3s0KovOIJTXpOUWfAkXpJvQnJjt2JxaqRCBDb-Vh5jDh3MBpQDhtoJ
exIO2jvy0hvctn3cShPCyUjrDRLbXU6BK5vPbNcZ0l8K3l02V-bIe-t2XjQhDNtDt60jfn3aQ5rtKRTffjrnhPF3LlKUXP6-hnjy3b7yKq5v-q50StJ_0xJSLTDUyN3MWh3RymJ42-39LPO2hpRjyxv4X60B0-oxJpOJXaILWl52HlFWj43vbURvD--g3-AqBM5d
tjTO2bc_5KnlfMQ_bf--QfbQ0hOhqP-jBRIEoK0hJC-2bKvPKITD-tFO5eT22-usQRIO2hcHMPoosIOvQxocKxLh3tjZQfbQ0briaKJjBMbUoqRHXnJi0btQDPvxBf7pBJnqbp5TtUJM_UKzhfoMqfTbMlJyKMnitIv9-pPKWhQrh459XP68bTkA5bjZKxtq3mkj
bPbDfn028DKuDTtajj3QeaRabK6aKC5bL6rJabC3sUoDXU6q2bDeQNby0fQ9-eTE-CjFLq3SEIooyT3JXp0vWtv4WbbvLT7johRTWqR48CbC0MonDh83Bn_L2xQJHmLOBt3O5hvvhb3O3MA-yUKmDloOW-TB5bbPLUQF5l8-sq0x0bOte-bQXH_E5bj2qRI8_DI5
3f; MCITY=-131%3A; delPer=0; PSINO=1; ZD_ENTRY=baidu; BDUSS=VNVaTN5SlJWaFFLSFNqa2x1M21SajQtczFVVnl-b1RtTlhXa2Y5OEJmV1Q4YVZmRVFBQUFBJCQAAAAAAAAAAAEAAAAbp3I6yse12MfywLS1xAAAAAAAAAAAAAAAAAAAAAAAAAAAA
AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAJNkfl-TZH5fO; TIEBAUID=7a4a7b316d50c52d5ea62017; STOKEN=76bd4f2ff9b9c11d935ad6c21ceb1a555caa919a3a86a9782325680000eb586b; Cuid=8549F498475D4F4949EEEB4F5
4BE5B39%3AFG%3D1; Appid=tieba; Appkey=appkey; DeviceType=20; Extension-Version=2.2; LCS-Header-Version=1; BDRCVFR[feWj1Vr5u3D]=I67x6TjHwwYf0; H_PS_PSSID=32817_32617_1462_32793_7547_31253_32723_322
30_7517_7605_32117_32719; Hm_lvt_98b9d8c2fd6608d564bf2ac2ae642948=1602118627,1602138484,1602379744,1602383433; 980592411_FRSVideoUploadTip=1; st_key_id=17; st_data=3e83c1a07e160934969f87fbaf01de69
1f829fd5365ade452649cfd9bcf6b28cdbb12975c12f05866773c6610461a95c26ce12a08dc2343b93e0e140963cc37d6fcb4c15094e29e05a76604f93c108b9357908344250f93e6783314f8bfd50fe5007432babf23d10a9210b023cceec7c3798
001dfa69d41912a69e659b6e5f3c; st_sign=ce764681; Hm_lpvt_98b9d8c2fd6608d564bf2ac2ae642948=1602383457"""
        }
        self.request = urllib.request.urlopen
        self.data = []

    def process(self, page):
        soup_html = BeautifulSoup(self.request(self.url.format(page)))
        page_content = soup_html.find_all('div', attrs={'class': 'd_post_content j_d_post_content'})
        for item in page_content:
            print(item.text)
            self.data.append(item.text)

    def run(self):
        for page in range(self.start_page, self.end_page):
            try:
                self.process(page)
                print(page)
                time.sleep(0.01)
            except Exception as e:
                print(e)

if __name__ == '__main__':
    A = Spider(8,9)
    A.run()