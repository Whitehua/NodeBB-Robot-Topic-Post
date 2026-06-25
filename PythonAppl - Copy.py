# -*- coding: gbk -*-
import os
import time
import sys
import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv

# 加载 .env 文件中的变量
load_dotenv()

class NodeBBAutoPoster:
    def __init__(self):
        """
        初始化 NodeBB 自动发帖器（带 AI 摘要功能）
        """
        self.base_url = os.getenv("NODEBB_URL", "http://localhost:4567").rstrip('/')
        self.nodebb_token = os.getenv("NODEBB_TOKEN")
        self.openrouter_key = os.getenv("OPENROUTER_API_KEY")
        self.cid = os.getenv("TARGET_CID", "1")
        self.uid = os.getenv("TARGET_UID", "1")        
        
        # NodeBB 请求头
        self.nodebb_headers = {
            "Authorization": f"Bearer {self.nodebb_token}",
            "Content-Type": "application/json",
            "Accept": "application/json"
        }

    def crawl_article(self, target_url):
        """
        爬取目标 URL 的文章并提取纯文本
        """
        print(f"[+] 正在爬取目标网页: {target_url}")
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        }
        try:
            response = requests.get(target_url, headers=headers, timeout=15)
            response.raise_for_status()
            response.encoding = response.apparent_encoding
        except Exception as e:
            print(f"[-] 网页爬取失败: {e}")
            return None, None

        soup = BeautifulSoup(response.text, 'html.parser')
        
        # 提取标题
        title = ""
        if soup.h1:
            title = soup.h1.get_text().strip()
        elif soup.title:
            title = soup.title.get_text().strip()
        else:
            title = "未命名抓取文章"

        # 清理干扰标签（脚本、样式、导航等）
        for script in soup(["script", "style", "nav", "footer", "header", "aside"]):
            script.decompose()
            
        # 定位正文区域并提取纯文本
        article_body = soup.find('article') or soup.find('div', class_=lambda c: c and ('content' in c or 'article' in c or 'post' in c)) or soup.body
        text_content = article_body.get_text(separator='\n', strip=True)
        
        return title, text_content

    def summarize_with_openai(self, text):
        """
        调用 OpenAI API 将长文本简化为 100-150 字的摘要
        """
        print("[+] 正在调用 OpenAI API 生成内容摘要...")
        url = "https://openrouter.ai/api/v1/chat/completions"
        headers = {
            "Authorization": f"Bearer {self.openrouter_key}",
            "Content-Type": "application/json"
        }
        
        # 截取前 4000 个字符发送给 AI，防止超出普通模型 Token 限制
        truncated_text = text[:12000]
        prompt = f"请将以下文章内容简化，提取核心信息，输出为中文，字数严格限制在 100字 到 150字 之间：\n\n{truncated_text}"
        
        payload = {
            "model": "openrouter/free", # 可根据需求更改为 gpt-4o 或其他模型
            "messages": [
                {"role": "system", "content": "你是一个精准的内容总结助手。"},
                {"role": "user", "content": prompt}
            ],
            "temperature": 0.7
        }
        
        try:
            response = requests.post(url, json=payload, headers=headers, timeout=30)
            response.raise_for_status()
            result = response.json()
            summary = result['choices'][0]['message']['content'].strip()
            print(f"[√] AI 摘要生成完成，当前字数: {len(summary)}字")
            return summary
        except Exception as e:
            print(f"[-] OpenAI API 调用失败: {e}")
            if hasattr(e, 'response') and e.response is not None:
                print(f"[-] 错误详情: {e.response.text}")
            return None

    def post_topic(self, title, summary_content, original_url):
        """
        调用 NodeBB API 发布摘要主题
        """
        api_url = f"{self.base_url}/api/v3/topics"
        
        # 组装最终的 Markdown 帖文内容
        final_content = f"\n\n{summary_content}\n\n---\n> *原文链接: [{original_url}]({original_url})*"
        
        payload = {
            "cid": self.cid,
            "_uid": self.uid,
            "title": f"【资讯】 {title}",
            "content": final_content
        }
        
        print(f"[+] 正在尝试向 NodeBB 发帖，目标版块 CID: {self.cid}")
        try:
            response = requests.post(api_url, json=payload, headers=self.nodebb_headers, timeout=10)
            
            # 兼容旧版本 NodeBB 的 v1 路由
            if response.status_code == 404:
                print("[!] v3 API 未响应，正在尝试 v1 API 备用路由...")
                fallback_url = f"{self.base_url}/api/v1/topics"
                payload["_uid"] = 1  
                response = requests.post(fallback_url, json=payload, headers=self.nodebb_headers, timeout=10)

            if response.status_code in [200, 201, 202]:
                res_data = response.json()
                topic_data = res_data.get('payload', res_data)
                slug = topic_data.get('slug', '')
                print(f"[√] 发帖成功！")
                if slug:
                    print(f"[√] 帖子链接: {self.base_url}/topic/{slug}")
                return True
            else:
                print(f"[-] 发帖失败，状态码: {response.status_code}")
                print(f"[-] 错误响应信息: {response.text}")
                return False
        except Exception as e:
            print(f"[-] NodeBB API 请求发生异常: {e}")
            return False

if __name__ == "__main__":
    poster = NodeBBAutoPoster()
    url = os.getenv("TARGET_ARTICLE_URL")
    if not url:
        print("[!] 请在 .env 文件中设置 TARGET_ARTICLE_URL")
        sys.exit(1)
        
    # 1. 爬取并提取网页纯文本
    title, article_text = poster.crawl_article(url)
    
    if title and article_text:
        # 2. 调用 OpenAI 生成规定字数内的摘要
        summary = poster.summarize_with_openai(article_text)
        
        if summary:
            # 3. 将摘要与原文链接发布到 NodeBB
            poster.post_topic(title, summary, url)
        else:
            print("[-] 脚本终止：未能成功生成 AI 摘要。")
    else:
        print("[-] 脚本终止：未能成功获取文章内容。")