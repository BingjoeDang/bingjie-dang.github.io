import os
import json
import requests

# 1. 从 GitHub Secrets 中安全读取你的 API Key
API_KEY = os.environ.get("SERPAPI_KEY")
AUTHOR_ID = "Mfp83rUAAAAJ" # 你的真实 Google Scholar ID

def fetch_from_serpapi():
    print(f"开始通过 SerpApi 获取学者数据 (ID: {AUTHOR_ID})...")
    
    # 构建 SerpApi 的请求链接 (提取最多 100 篇文章)
    url = f"https://serpapi.com/search.json?engine=google_scholar_author&author_id={AUTHOR_ID}&api_key={API_KEY}&num=100"

    try:
        response = requests.get(url)
        if response.status_code != 200:
            print(f"请求失败，状态码: {response.status_code}, 信息: {response.text}")
            return

        data = response.json()
        articles = data.get("articles", [])
        
        if not articles:
            print("警告：未抓取到任何文章，请检查 ID 或 API 状态。")
            return

        citations_data = []
        for article in articles:
            title = article.get("title", "")
            # SerpApi 返回的引用量格式通常在 cited_by.value 里
            citations = article.get("cited_by", {}).get("value", 0)
            
            citations_data.append({
                "title": title,
                "citations": citations
            })

        # 写入本地 JSON 文件
        with open('citations.json', 'w', encoding='utf-8') as f:
            json.dump(citations_data, f, ensure_ascii=False, indent=2)
            
        print(f"太棒了！成功保存了 {len(citations_data)} 篇文章的引用数据到 citations.json")

    except Exception as e:
        print(f"运行过程中发生错误: {e}")

if __name__ == "__main__":
    if not API_KEY:
        print("错误：未找到 SERPAPI_KEY，请确保你已在 GitHub Secrets 中配置了它！")
    else:
        fetch_from_serpapi()
