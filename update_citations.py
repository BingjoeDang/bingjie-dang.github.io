import os
import json
import requests

# 读取 API Key 并自动去除可能不小心复制到的空格
API_KEY = os.environ.get("SERPAPI_KEY", "").strip()
AUTHOR_ID = "Mfp83rUAAAAJ"

def fetch_from_serpapi():
    print(f"开始通过 SerpApi 获取学者数据 (ID: {AUTHOR_ID})...")
    url = f"https://serpapi.com/search.json?engine=google_scholar_author&author_id={AUTHOR_ID}&api_key={API_KEY}&num=100"

    try:
        response = requests.get(url)
        data = response.json()
        
        # 1. 检查 SerpApi 是否直接返回了错误信息
        if "error" in data:
            print(f"❌ SerpApi 官方报错啦: {data['error']}")
            return
            
        articles = data.get("articles", [])
        
        # 2. 如果没拿到文章，打印出 SerpApi 到底返回了什么鬼东西
        if not articles:
            print("⚠️ 警告：未抓取到文章！SerpApi 返回的原始数据如下：")
            print(json.dumps(data, indent=2, ensure_ascii=False))
            return

        citations_data = []
        for article in articles:
            title = article.get("title", "")
            citations = article.get("cited_by", {}).get("value", 0)
            citations_data.append({
                "title": title,
                "citations": citations
            })

        # 写入本地 JSON 文件
        with open('citations.json', 'w', encoding='utf-8') as f:
            json.dump(citations_data, f, ensure_ascii=False, indent=2)
            
        print(f"✅ 太棒了！成功保存了 {len(citations_data)} 篇文章的引用数据！")

    except Exception as e:
        print(f"❌ 运行过程中发生系统错误: {e}")

if __name__ == "__main__":
    if not API_KEY:
        print("❌ 错误：未找到 SERPAPI_KEY！")
    else:
        fetch_from_serpapi()
