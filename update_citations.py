import os
import json
import requests

API_KEY = os.environ.get("SERPAPI_KEY", "").strip()
AUTHOR_ID = "Mfp83rUAAAAJ"

def main():
    print(f"开始抓取，使用的 ID: {AUTHOR_ID}")
    
    # 初始化一个空列表，确保无论发生什么，都有数据可以写入文件
    citations_data = []

    if not API_KEY:
        print("❌ 致命错误：未找到 SERPAPI_KEY，请检查 GitHub Secrets！")
    else:
        try:
            url = f"https://serpapi.com/search.json?engine=google_scholar_author&author_id={AUTHOR_ID}&api_key={API_KEY}&num=100"
            print("正在向 SerpApi 发送请求...")
            response = requests.get(url)
            data = response.json()

            # 1. 检查 API 是否直接报错
            if "error" in data:
                print(f"❌ SerpApi 官方报错: {data['error']}")
            # 2. 检查是否有文章数据
            elif "articles" not in data:
                print("⚠️ 未找到 articles 字段，API 返回的真实数据是：")
                print(json.dumps(data, indent=2, ensure_ascii=False))
            # 3. 成功拿到数据
            else:
                articles = data["articles"]
                print(f"✅ 成功获取到 {len(articles)} 篇文章的数据！")
                for article in articles:
                    title = article.get("title", "")
                    citations = article.get("cited_by", {}).get("value", 0)
                    citations_data.append({"title": title, "citations": citations})

        except Exception as e:
            print(f"❌ 请求过程中发生代码异常: {e}")

    # 【核心修复】：无论成功还是失败，强制生成 citations.json 文件，彻底消灭 128 错误！
    print("正在保存 citations.json 文件...")
    with open('citations.json', 'w', encoding='utf-8') as f:
        json.dump(citations_data, f, ensure_ascii=False, indent=2)
    print("✅ 文件保存完毕！")

if __name__ == "__main__":
    main()
