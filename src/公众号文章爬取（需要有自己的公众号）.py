# 爬取公众号文章（需要用自己的公众号发文章引用目标公众号文章）
# 变量设置：cookie
# 变量设置：referer
# 变量设置：url
import requests
import time
import math
import json
import os

llq_cookie = 'appmsglist_action_3217759925=card; ua_id=NzNTwIJSJQal5iz5AAAAAKoka31A8NTh2jI347VLH8E=; _clck=3vqm6b|1|fud|0; wxuin=42458328816142; uuid=7c6aed5d4a8da88d1e9f3b56fe304855; bizuin=3217759925; ticket=2204c2722f2ead5e629f9f04f8742a6eb8f9a2fe; ticket_id=gh_007083e7ec76; slave_bizuin=3217759925; cert=X8oPsqjmgFS_o_I_6faRi8YTT3pYvG4S; noticeLoginFlag=1; rand_info=CAESINjJ0gzqj072bdkN9dRR9Xh3lp9yNMPrc6BmlpG78RN8; data_bizuin=3217759925; data_ticket=C/aKq/6aYHWKHglTuFzVYSonuwAiCc/JxQTc7oxvG5xFIP+W/STOVkXr2XKPlAt/; slave_sid=VU1qQzY4SHdyc25VaUlabk4xSFN2aTdsSzd1ZDlVNmJVZkdhbm9XWGhsWWRPSjlrTklzR2xKNmQ3MUo0WWZtQWlZS1VMYnUybkprbzhKbWF3NklHVTZDVHdzOUk3Y0ppZVZiMGNWY0NMVF9aa3p0dVl4Q001bElLcHA3QzJoYkExNVBudENUSWFkS3E3STlz; slave_user=gh_007083e7ec76; xid=d18c95b7c6119974a4e3ea7bf060e211; openid2ticket_otR7Lv3zJYOs4i5sgVEg4ZFFzNHA=VRrvvrizloHGWH0BcqxCdCynBtTpWiIqWlSkpzTb9ec=; mm_lang=zh_CN; _clsk=m89mn0|1742458878365|3|1|mp.weixin.qq.com/weheat-agent/payload/record'
referer = 'https://mp.weixin.qq.com/cgi-bin/appmsg?t=media/appmsg_edit_v2&action=edit&isNew=1&type=77&token=681244183&lang=zh_CN&timestamp=1742458877182'
pageSize = 5    # 每页数量
total = 35 * pageSize  # 总记录数

def CreateRequestSession(cookie, page):
    # 计算 begin 参数：若页码从 0 开始，则第 1 页 begin=0，第二页 begin=5，以此类推
    begin = str(page * pageSize)
    session = requests.session()
    url = ("https://mp.weixin.qq.com/cgi-bin/appmsgpublish?"
           "sub=list&search_field=null&begin=" + begin + "&count=5&query=&fakeid=Mzk0MDUyOTg4Mw%3D%3D"
           "&type=101_1&free_publish_type=1&sub_action=list_ex&fingerprint=a84e67ab86fe0a421f8b8d8b4bff292c"
           "&token=681244183&lang=zh_CN&f=json&ajax=1")
    headers = {
        'authority': 'mp.weixin.qq.com',
        'method': 'GET',
        'path': url.split("https://mp.weixin.qq.com")[-1],
        'scheme': 'https',
        'accept': 'application/json, text/javascript, */*; q=0.01',
        'accept-encoding': 'gzip, deflate, br',
        'accept-language': 'zh-CN,zh;q=0.9',
        'cookie': cookie,
        'referer': referer,
        'sec-ch-ua': '"Google Chrome";v="105", "Not)A;Brand";v="8", "Chromium";v="105"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36',
        'x-requested-with': 'XMLHttpRequest'
    }
    response = session.request("GET", url, headers=headers)
    return response

def getGzhWenzhangList(cookie):
    filename = 'gzh_wenzhang_list2.json'
    # 如果文件已存在则读取已有数据，否则初始化为空列表
    if os.path.exists(filename):
        with open(filename, 'r', encoding='utf-8') as f:
            try:
                all_data = json.load(f)
            except json.JSONDecodeError:
                all_data = []
    else:
        all_data = []

    start_time = time.time()
    total_pages = math.ceil(total / pageSize)

    for i in range(total_pages):
        # 传入当前页码 i（从 0 开始）
        response = CreateRequestSession(cookie, i)
        try:
            publish_page_str = response.json()['publish_page']
            data = json.loads(publish_page_str)['publish_list']
        except (KeyError, json.JSONDecodeError) as e:
            print("解析数据出错：", e)
            break

        # 如果返回数据为空，则结束翻页
        if not data:
            print("未获取到更多数据，结束翻页。")
            break

        # 遍历每个数据项，对 publish_info 字段进行处理
        for item in data:
            if 'publish_info' in item and isinstance(item['publish_info'], str):
                try:
                    item['publish_info'] = json.loads(item['publish_info'])
                except json.JSONDecodeError as e:
                    print("解析 publish_info 出错：", e)
                    continue

            if ('publish_info' in item and isinstance(item['publish_info'], dict) and
                    'sent_info' in item['publish_info'] and
                    'time' in item['publish_info']['sent_info']):
                timestamp = item['publish_info']['sent_info']['time']
                readable_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(timestamp))
                item['publish_info']['sent_info']['time_str'] = readable_time

        all_data.extend(data)

        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(all_data, f, ensure_ascii=False, indent=4)

        elapsed_time = time.time() - start_time
        estimated_total_time = (elapsed_time / (i + 1)) * total_pages
        remaining_time = estimated_total_time - elapsed_time
        print(f"进度: {i + 1}/{total_pages} - 剩余预计时间: {time.strftime('%H:%M:%S', time.gmtime(remaining_time))}")

    print(f"总记录数: {len(all_data)}")

if __name__ == '__main__':
    getGzhWenzhangList(llq_cookie)
