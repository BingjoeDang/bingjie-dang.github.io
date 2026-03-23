import json
from scholarly import scholarly

def fetch_citations():
    author_id = 'Mfp83rUAAAAJ' # 你的真实 Google Scholar ID
    print(f"开始抓取学者数据 (ID: {author_id})...")
    
    try:
        author = scholarly.search_author_id(author_id)
        scholarly.fill(author, sections=['publications'])
        
        citations_data = []
        for pub in author['publications']:
            title = pub['bib']['title']
            citations = pub.get('num_citations', 0)
            citations_data.append({
                "title": title,
                "citations": citations
            })
            
        with open('citations.json', 'w', encoding='utf-8') as f:
            json.dump(citations_data, f, ensure_ascii=False, indent=2)
            
        print(f"成功更新了 {len(citations_data)} 篇文章的引用数据到 citations.json")
        
    except Exception as e:
        print(f"抓取失败: {e}")

if __name__ == "__main__":
    fetch_citations()
