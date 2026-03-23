import os
import json
import requests

API_KEY = os.environ.get("SERPAPI_KEY", "").strip()
AUTHOR_ID = "Mfp83rUAAAAJ"

def main():
    print(f"开始抓取，使用的 ID: {AUTHOR_ID}")
    citations_data = []

    if not API_KEY:
        print("❌ 致命错误：未找到 SERPAPI_KEY，请检查 GitHub Secrets！")
    else:
        try:
            # 【核心修复】：去掉了触发 Bug 的 &num=100，并加上 &hl=en 确保语言匹配
            url = f"https://serpapi.com/search.json?engine=google_scholar_author&author_id={AUTHOR_ID}&hl=en&api_key={API_KEY}"
            print("正在向 SerpApi 发送稳定版请求...")
            response = requests.get(url)
            data = response.json()

            if "error" in data:
                print(f"❌ SerpApi 官方报错: {data['error']}")
            elif "articles" not in data:
                print("⚠️ 未找到 articles 字段，API 返回的真实数据是：")
                print(json.dumps(data, indent=2, ensure_ascii=False))
            else:
                articles = data["articles"]
                print(f"✅ 成功获取到 {len(articles)} 篇文章的数据！")
                for article in articles:
                    title = article.get("title", "")
                    citations = article.get("cited_by", {}).get("value", 0)
                    citations_data.append({"title": title, "citations": citations})

        except Exception as e:
            print(f"❌ 请求过程中发生代码异常: {e}")

    print("正在保存 citations.json 文件...")
    with open('citations.json', 'w', encoding='utf-8') as f:
        json.dump(citations_data, f, ensure_ascii=False, indent=2)
    print("✅ 文件保存完毕！")

if __name__ == "__main__":
    main()
