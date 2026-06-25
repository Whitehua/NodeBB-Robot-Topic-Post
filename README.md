# NodeBB AI Summarizer & Poster 🚀

这是一个用 **Python** 编写的自动化工具，旨在利用 AI 技术自动抓取/输入文章，生成精炼的摘要，并将其作为主题或推文（Post）自动发布到 **NodeBB** 论坛上。

该工具对运行环境和 AI 供应商提供了极高的兼容性，适合用于内容聚合、社区自动化运营等场景。

---

## ✨ 核心特性

* **智能摘要**：对接大语言模型，自动提炼长文章的核心观点。
* **多 API 兼容**：原生支持 **OpenAI** 格式的标准 API，并完美兼容 **OpenRouter**，轻松切换数百种商用或开源大模型。
* **跨平台支持**：得益于 Python 的跨平台特性，支持在以下架构和系统中完美运行：
    * **架构**：X86/64, ARM64 (如树莓派、Apple Silicon)
    * **系统**：Windows, Linux (如 Ubuntu, Debian, CentOS)
* **轻量高效**：配置简单，通过配置文件或环境变量即可快速启动。

---

## 🖥️ 平台兼容性

| 操作系统 (OS) | 架构 (Architecture) | 状态 (Status) |
| :--- | :--- | :--- |
| **Linux** | X86_64 / ARM64 | 🟢 完美支持 (推荐) |
| **Windows** | X86_64 | 🟢 完美支持 |
| **macOS** | X86_64 / ARM64 (M系列) | 🟢 完美支持 |

---

## 🛠️ 快速开始

### 1. 克隆仓库

```bash
git clone https://github.com/Whitehua/NodeBB-Robot-Topic-Post.git
cd NodeBB-Robot-Topic-Post
```

### 2. 安装依赖
确保你的系统已安装 Python 3.8+。使用 pip 安装必要的依赖：

```Bash
pip install -r requirements.txt
```

注意 (ARM64/Linux 用户)：如果在某些轻量级 Linux 环境下提示编译失败，请先确保系统安装了 python3-dev 和 build-essential。

### 3. 配置环境
在项目根目录下创建一个 .env 文件（或复制 .env.example），并填入你的配置信息：

```
cp .env.example .env
```

`.env` introduction
```
NODEBB_URL="place your nodebb website url. example:http://localhost:4567" 
NODEBB_TOKEN="place your nodebb website token.uid need to set 0"
OPENROUTER_API_KEY = "if you have openai compatible key,also need to replace openai website api at main.py #72 url = "https://openrouter.ai/api/v1/chat/completions" "

TARGET_CID=
TARGET_UID=
TARGET_ARTICLE_URL = ""
```

### 4. 运行工具
运行主程序来启动文章总结与发布任务：

```
python main.py
```

## ⚙️ NodeBB API 准备工作
为了让工具能够成功在 NodeBB 上发布内容，请确保：

登录 NodeBB 后台（ACP）。

进入 插件 (Plugins) -> API Write (或者内置的 Web API)。

生成一个针对特定用户或管理员的 Token，并确保该用户拥有在指定 CID（板块）发帖的权限。

## 🤝 贡献与反馈
欢迎提交 Issue 或 Pull Request 来帮助改进这个项目！

Fork 本仓库

创建你的特性分支 (git checkout -b feature/AmazingFeature)

提交你的修改 (git commit -m 'Add some AmazingFeature')

推送到分支 (git push origin feature/AmazingFeature)

提交 Pull Request

📄 开源协议
本项目采用 AGPL V3.0 License 开源协议。
