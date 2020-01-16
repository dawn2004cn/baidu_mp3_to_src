# encoding=gbk
import re
import pinyin
import requests
import lxml.etree as etree

def getHtml(url):
    print(url)
    headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:71.0) Gecko/20100101 Firefox/71.0',
               'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'}
    html = requests.get(url, headers=headers)
    html.encoding = 'gbk'
    text = html.text
    return text


def getdata_total(html):
    tree = etree.HTML(html, parser=etree.HTMLParser(encoding='utf-8'))
    nodes = tree.xpath('//table[@class="t12"]/tr')
    for node in nodes:
        data_total = node.xpath('./td[1]/text()')
        data_total = "".join(data_total)
        print(data_total)

city_info = getHtml('http://pv.sohu.com/cityjson')
print(city_info)  # ������ṹ
'''var returnCitySN = {"cip": "119.137.1.150", "cid": "440300", "cname": "�㶫ʡ������"};'''
addr = city_info.split('=')[1].split(',')[2].split('"')[3]  # ȡ����ַ��Ϣ
print(addr)

#����ת��Ϊ����������ƴ��
f = pinyin.get(addr,format='strip')
print(f)   # �������ַƴ���ṹ
provice = f.split('sheng', 1)[0].replace(' ', '')  # ��ȡʡ��
print(provice)
city = f.split('shi')[0].split('sheng')[1].strip().replace(' ', '')  # ��ȡ����
print(city)
url = 'http://qq.ip138.com/weather/{}/{}.htm'.format(provice, city)
# ����url��֪ĳʡĳ�е�����url��Ϊ�����ʽ
wea_info = getHtml(url)

getdata_total(wea_info)
tianqi_pattern = 'alt="(.+?)"'
tianqi = re.findall(tianqi_pattern, wea_info)  # ��ȡ������Ϣ
print(tianqi)
wendu_pattern = '<td>([-]?\d{1,2}.+)</td>'
wendu = re.findall(wendu_pattern, wea_info)  # ��ȡ�¶���Ϣ
print(wendu)
wind_pattern = '<td>(\W+\d{1,2}.+)</td>'
wind = re.findall(wind_pattern, wea_info)  # ��ȡ������Ϣ
print(wind)

print('λ�ã�', addr)
print('������', tianqi[0])  # ��������������������Ϊtianqi[1],����ȡ6������
print('�¶ȣ�', wendu[0])  # �����¶�
#print('����', wind[0])   # �������
