# WeChatArticleDownloader

微信公众号文章列表采集工具

## 📖 项目简介

基于 Python 实现的微信公众号文章采集工具，支持：

- 自动分页爬取公众号文章元数据
- 解析文章标题/链接/发布时间/封面图
- 生成结构化JSON和CSV文件
- 自动下载文章封面图片

## 🚀 功能特性

| 功能模块  | 说明                                       |
|-------|------------------------------------------|
| 分页爬取  | 支持自定义分页大小，自动计算翻页逻辑                       |
| 数据持久化 | 原始数据保存为JSON，解析后数据支持JSON/CSV双格式输出         |
| 封面下载  | 自动下载文章封面图片至本地目录，保留图片原始尺寸                 |
| 时间格式化 | 自动将Unix时间戳转换为可读时间格式（YYYY-MM-DD HH:MM:SS） |
| 异常处理  | 自动跳过无效数据条目，支持断点续爬                        |

## 📦 文件说明

```   
.
├── 公众号文章爬取（需要有自己的公众号）\.py    # 主爬虫程序
├── 公众号文章爬取（需要有自己的公众号）解析\.py  # 数据解析程序
├── gzh_wenzhang_list2\.json                # 原始数据存储
├── new_articles\.json                      # 解析后结构化数据
├── new_articles\.csv                       # CSV格式数据
└── fengmian_imgs/                         # 封面图片存储目录
```  

## 🛠 使用说明

### 环境要求

- Python 3.8+
- 依赖库：`requests`, `json`, `csv`, `time`, `os`, `math`

```bash
pip install requests
```

### 配置步骤

1. **获取Cookie**  
   使用Chrome开发者工具登录[微信公众号平台](https://mp.weixin.qq.com)，复制完整Cookie值替换`llq_cookie`变量

2. **配置参数**
   ```python
   # 在爬虫文件中修改以下参数
   llq_cookie = 'your_cookie_here'  # 必填
   pageSize = 5                     # 每页条数（建议不超过10）
   total = 35 * pageSize            # 预估总文章数
   ```

3. **运行爬虫**
   ```bash
   python 公众号文章爬取（需要有自己的公众号）.py
   ```

4. **解析数据**
   ```bash
   python 公众号文章爬取（需要有自己的公众号）解析.py
   ```

### 输出示例

**JSON字段说明**

```json
{
  "id": 1,
  "title": "文章标题示例",
  "link": "https://mp.weixin.qq.com/s/xxx",
  "cover_local": "./fengmian_imgs/cover_1.jpg",
  "time": "2024-03-15 14:30:00"
}
```

## ⚠️ 注意事项

1. 需要**自有公众号**，通过发表引用文章爬取第三方公众号文章列表
2. Cookie有效期约2小时，过期需重新获取
3. 高频请求可能导致账号异常，建议：
    - 设置`time.sleep()`增加延时
    - 控制`pageSize`不超过10
    - 每日采集次数不超过50次

## 📜 免责声明

本项目仅用于学习交流，请严格遵守微信公众平台使用协议。使用者应对采集行为负全部责任，开发者不承担任何法律风险。

----
🔄 最后更新：2024-03-18 | 📧 问题反馈：1136660162@qq.com

#### 联系作者：  
![img.png](assets/img.png)
