import os
import json
import requests

API_KEY = os.environ.get("SERPAPI_KEY", "").strip()
AUTHOR_ID = "Mfp83rUAAAAJ"

def main():
    print(f"开始抓取，使用的 ID: {AUTHOR_ID}")
    citations_data = []
    # 新增：用于存储总引用量和 h-index 的字典
    author_stats = {"total_citations": 0, "h_index": 0}

    if not API_KEY:
        print("❌ 致命错误：未找到 SERPAPI_KEY，请检查 GitHub Secrets！")
        return

    try:
        for start in [0, 40]:
            url = f"https://serpapi.com/search.json?engine=google_scholar_author&author_id={AUTHOR_ID}&hl=en&api_key={API_KEY}&start={start}&num=40"
            print(f"正在向 SerpApi 发送请求 (起始位置: 第 {start+1} 篇)...")
            response = requests.get(url)
            data = response.json()

            if "error" in data:
                print(f"❌ SerpApi 官方报错: {data['error']}")
                break
                
            # 【核心新增】：在第一页抓取时，提取作者的总引用和 H-index
            if start == 0 and "cited_by" in data and "table" in data["cited_by"]:
                for row in data["cited_by"]["table"]:
                    if "citations" in row:
                        author_stats["total_citations"] = row["citations"].get("all", 0)
                    elif "h_index" in row:
                        author_stats["h_index"] = row["h_index"].get("all", 0)
                print(f"📊 抓取到作者统计数据：总引用 {author_stats['total_citations']}, H-index {author_stats['h_index']}")

            if "articles" not in data:
                print("⚠️ 当前页未找到 articles 字段，可能已经到底了。")
                break
            else:
                articles = data["articles"]
                print(f"✅ 当前页成功获取到 {len(articles)} 篇文章的数据！")
                for article in articles:
                    title = article.get("title", "")
                    citations = article.get("cited_by", {}).get("value", 0)
                    citations_data.append({"title": title, "citations": citations})
                
                if len(articles) < 20:
                    break

    except Exception as e:
        print(f"❌ 请求过程中发生代码异常: {e}")

    # 简单去重
    unique_data = {item['title']: item['citations'] for item in citations_data}
    final_articles = [{"title": k, "citations": v} for k, v in unique_data.items()]

    # 【核心新增】：重构 JSON 格式，现在它不仅包含文章数组，还包含作者统计信息
    output_json = {
        "stats": author_stats,
        "articles": final_articles
    }

    print(f"正在保存 citations.json 文件...")
    with open('citations.json', 'w', encoding='utf-8') as f:
        json.dump(output_json, f, ensure_ascii=False, indent=2)
    print("✅ 文件保存完毕！")

if __name__ == "__main__":
    main()
