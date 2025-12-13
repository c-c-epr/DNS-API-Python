# FastAPI DNS Lookup API

一個使用 **FastAPI** 實作的 DNS 查詢 API，可讓使用者指定：

- 🌐 網域（domain）
- 🧾 DNS Record 類型（A / AAAA / MX / TXT / NS / CNAME）
- 🖧 DNS Resolver（任意 DNS Server IP）

此專案特別適合用於：

- DNS 封鎖 / 污染比對
- 台灣與國外 DNS 行為分析
- Cloudflare Worker 無法直接查 DNS 時的後端補查服務

---

## ✨ 功能特色

- ✅ RESTful API 設計
- ✅ 可自由指定 DNS Resolver（不限制來源）
- ✅ 支援多種常見 DNS Record 類型
- ✅ 內建 Swagger / OpenAPI 文件
- ✅ 可直接部署於 **Zeabur（不需 Docker）**

---

## 📦 專案結構

```text
.
├── main.py              # FastAPI 主程式
└── requirements.txt     # Python 相依套件
```

---

## 🧩 環境需求

- Python 3.8+

---

## 🔧 安裝套件

```bash
pip install -r requirements.txt
```

`requirements.txt` 內容：

```txt
fastapi
uvicorn
dnspython
```

---

## ▶️ 本地啟動方式

```bash
uvicorn main:app --reload
```

啟動後可在以下位置存取：

- API Base URL：http://127.0.0.1:8000
- Swagger UI：http://127.0.0.1:8000/docs

---

## 🚀 API 使用說明

### Endpoint

```
GET /dns/lookup
```

### Query Parameters

| 參數     | 必填 | 說明                            | 範例            |
| -------- | ---- | ------------------------------- | --------------- |
| domain   | ✅   | 要查詢的網域                    | google.com      |
| type     | ❌   | DNS Record 類型（預設 A）       | A / MX / TXT    |
| resolver | ❌   | DNS Resolver IP（預設 8.8.8.8） | 101.101.101.101 |

---

### 範例請求

```text
/dns/lookup?domain=google.com&type=A&resolver=1.1.1.1
```

### 範例回應

```json
{
  "domain": "google.com",
  "type": "A",
  "resolver": "1.1.1.1",
  "records": ["142.250.72.14"]
}
```

---

## ☁️ 部署到 Zeabur（不使用 Docker）

1. 將專案推送至 GitHub
2. 在 Zeabur 建立新專案
3. 新增 **Python Service**
4. 指定 GitHub Repository
5. 設定啟動指令（Start Command）：

```bash
uvicorn main:app --host 0.0.0.0 --port $PORT
```

⚠️ 注意事項：

- 一定要使用 `$PORT`
- `--host` 必須是 `0.0.0.0`

部署完成後即可透過 Zeabur 提供的網域存取 API。

---

## 🔐 安全性提醒

本 API **不限制 DNS Resolver 來源**，適合研究與內部使用。

若未來要公開給不特定使用者，建議加入：

- API Key 驗證
- Rate Limiting
- 封鎖 Private IP Resolver（127.0.0.0/8、10.0.0.0/8 等）

---

## 🧠 延伸功能建議

- 🔁 一次查詢多個 DNS Resolver 並比較結果
- ⚡ 加入快取機制（Memory / Redis / D1）
- 📊 回傳 TTL、Response Time
- ☁️ 與 Cloudflare Worker 搭配使用

---

## 📄 License

MIT License
