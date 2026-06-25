# NodeBB-Robot-Topic-Post


`.env` introduction
```
NODEBB_URL="place your nodebb website url. example:http://localhost:4567" 
NODEBB_TOKEN="place your nodebb website token.uid need to set 0"
OPENROUTER_API_KEY = "if you have openai compatible key,also need to replace openai website api at main.py #72 url = "https://openrouter.ai/api/v1/chat/completions" "

TARGET_CID=
TARGET_UID=
TARGET_ARTICLE_URL = ""
```

```
pip install -r requirements.txt
```

```
cp .env.example .env
```

```
python main.py
```
