# 解析爬取后的文章数据生成json文件和csv文件

import os
import json
import time
import requests
import csv

# 文件和目录配置
INPUT_JSON = 'gzh_wenzhang_list2.json'
OUTPUT_JSON = 'new_articles.json'
OUTPUT_CSV = 'new_articles.csv'
IMG_DIR = './fengmian_imgs'

# 如果图片保存目录不存在，则创建
if not os.path.exists(IMG_DIR):
    os.makedirs(IMG_DIR)


def download_image(url, save_path):
    try:
        response = requests.get(url, stream=True, timeout=10)
        if response.status_code == 200:
            with open(save_path, 'wb') as f:
                for chunk in response.iter_content(1024):
                    f.write(chunk)
            print(f"图片下载成功：{save_path}")
        else:
            print(f"下载图片失败，状态码：{response.status_code}，URL: {url}")
    except Exception as e:
        print(f"下载图片异常：{e}，URL: {url}")


def timestamp_to_timestr(ts):
    """将时间戳（秒）转换为可读格式"""
    return time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(ts))


def parse_articles():
    # 读取原始 JSON 数据
    with open(INPUT_JSON, 'r', encoding='utf-8') as f:
        data = json.load(f)

    new_articles = []
    article_id = 1

    for record in data:
        publish_info = record.get('publish_info', {})
        appmsgex_list = publish_info.get('appmsgex', [])
        if not appmsgex_list:
            # 无文章信息则跳过
            continue

        # 取第一篇文章的信息（如果有多篇文章，可根据需要扩展处理）
        article_info = appmsgex_list[0]
        title = article_info.get('title', '').strip()
        link = article_info.get('link', '').strip()
        cover_url = article_info.get('cover', '').strip()

        # 获取文章时间：
        # 对于 publish_type 为 101，优先尝试从 sent_info.time_str 获取
        # 对于 publish_type 为 1，则取 publish_info.publish_info.update_time 并转换
        article_time = ''
        publish_type = record.get('publish_type')
        if publish_type == 101:
            sent_info = publish_info.get('sent_info', {})
            article_time = sent_info.get('time_str', '')
        elif publish_type == 1:
            inner_info = publish_info.get('publish_info', {})
            update_time = inner_info.get('update_time')
            if update_time:
                article_time = timestamp_to_timestr(update_time)
            else:
                update_time = article_info.get('update_time')
                if update_time:
                    article_time = timestamp_to_timestr(update_time)

        # 下载封面图片到本地 ./fengmian_imgs/ 目录下，命名为 cover_{id}.jpg
        local_img_path = ""
        if cover_url:
            local_img_path = os.path.join(IMG_DIR, f"cover_{article_id}.jpg")
            download_image(cover_url, local_img_path)
        else:
            print(f"文章【{title}】无封面图片 URL。")

        new_articles.append({
            "id": article_id,
            "title": title,
            "link": link,
            "cover_local": local_img_path,
            "time": article_time
        })
        article_id += 1

    # 保存新的 JSON 数据
    with open(OUTPUT_JSON, 'w', encoding='utf-8') as f:
        json.dump(new_articles, f, ensure_ascii=False, indent=4)
    print(f"共处理 {len(new_articles)} 篇文章，新数据保存在 {OUTPUT_JSON}")

    # 生成 CSV 文件
    with open(OUTPUT_CSV, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ["id", "title", "link", "cover_local", "time"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for article in new_articles:
            writer.writerow(article)
    print(f"CSV 数据也保存在 {OUTPUT_CSV}")


if __name__ == '__main__':
    parse_articles()
