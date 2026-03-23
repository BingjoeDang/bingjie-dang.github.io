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
        return

    try:
        # 分页循环抓取：start=0抓前20篇，start=20抓后20篇（总共覆盖40篇）
        for start in [0, 20]:
            url = f"https://serpapi.com/search.json?engine=google_scholar_author&author_id={AUTHOR_ID}&hl=en&api_key={API_KEY}&start={start}&num=20"
            print(f"正在向 SerpApi 发送请求 (起始位置: 第 {start+1} 篇)...")
            response = requests.get(url)
            data = response.json()

            if "error" in data:
                print(f"❌ SerpApi 官方报错: {data['error']}")
                break
            elif "articles" not in data:
                print("⚠️ 当前页未找到 articles 字段，可能已经到底了。")
                break
            else:
                articles = data["articles"]
                print(f"✅ 当前页成功获取到 {len(articles)} 篇文章的数据！")
                for article in articles:
                    title = article.get("title", "")
                    citations = article.get("cited_by", {}).get("value", 0)
                    citations_data.append({"title": title, "citations": citations})
                
                # 如果这一页返回的文章少于20篇，说明所有文章已抓完，提前结束翻页
                if len(articles) < 20:
                    break

    except Exception as e:
        print(f"❌ 请求过程中发生代码异常: {e}")

    # 简单去重（防止分页边界偶发的重复）
    unique_data = {item['title']: item['citations'] for item in citations_data}
    final_citations_data = [{"title": k, "citations": v} for k, v in unique_data.items()]

    print(f"正在保存 citations.json 文件，本次共成功抓取并汇总了 {len(final_citations_data)} 篇文章！")
    with open('citations.json', 'w', encoding='utf-8') as f:
        json.dump(final_citations_data, f, ensure_ascii=False, indent=2)
    print("✅ 文件保存完毕！")

if __name__ == "__main__":
    main()
