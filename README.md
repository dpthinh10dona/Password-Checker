<div align="center">
  <img src="Web/picture/homeicon.png" alt="Trust Mii Broo Logo" width="120"/>
  <h1>Trust Mii Broo</h1>
  <p><strong>Advanced Password Security & Generator Studio</strong></p>
  
  [![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
  [![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi)](https://fastapi.tiangolo.com/)
  [![HTML5](https://img.shields.io/badge/HTML5-E34F26?style=for-the-badge&logo=html5&logoColor=white)](https://developer.mozilla.org/en-US/docs/Glossary/HTML5)
  [![CSS3](https://img.shields.io/badge/CSS3-1572B6?style=for-the-badge&logo=css3&logoColor=white)](https://developer.mozilla.org/en-US/docs/Web/CSS)
  [![JavaScript](https://img.shields.io/badge/JavaScript-F7DF1E?style=for-the-badge&logo=javascript&logoColor=black)](https://developer.mozilla.org/en-US/docs/Web/JavaScript)
</div>

---

**Trust Mii Broo** là một giải pháp toàn diện giúp người dùng đánh giá mức độ an toàn của mật khẩu, phát hiện rò rỉ dữ liệu (data breaches), và tạo ra các mật khẩu có độ bảo mật cao thông qua thuật toán thông minh.

## ✨ Tính năng nổi bật (Key Features)

- 🛡️ **Phân tích độ mạnh (Strength Checker):** Sử dụng thuật toán [zxcvbn](https://github.com/dropbox/zxcvbn) từ Dropbox để đánh giá thực tế khả năng chống brute-force và thời gian bẻ khóa (crack time).
- 🚨 **Kiểm tra rò rỉ (Breach Detection):** Tích hợp API của `Have I Been Pwned` (k-anonymity). Chỉ băm (hash) SHA-1 mật khẩu tại trình duyệt và gửi 5 ký tự đầu tiên lên server, đảm bảo **mật khẩu của bạn không bao giờ rời khỏi thiết bị**.
- 🎲 **Trình tạo mật khẩu ngẫu nhiên (Zero-Knowledge Generator):** Sinh mật khẩu siêu việt dựa trên các tiêu chí tùy chỉnh (độ dài, chữ hoa, chữ thường, số, ký tự đặc biệt).
- 🧠 **AI Password Enhancer:** Biến một từ khóa dễ nhớ (Base Word) thành một mật khẩu phức tạp nhưng vẫn giữ được cốt lõi để bạn dễ dàng ghi nhớ.
- 🎨 **Modern & Adaptive UI:** Giao diện tối giản, sang trọng (Glassmorphism), hỗ trợ đa giao diện (Dark, Light, Lofi, Chill, Eco).

---

## 🛠 Công nghệ sử dụng (Tech Stack)

### Frontend (Client-side)
- Thuần HTML5, CSS3, Vanilla JavaScript (Không framework cồng kềnh, tối ưu hiệu suất).
- CSS Variables cho hệ thống Theme động.
- Trải nghiệm UI Glassmorphism hiện đại.

### Backend (Server-side)
- **Framework:** FastAPI (Python) - Nhanh, chuẩn RESTful, tích hợp sẵn Swagger UI.
- **Server:** Uvicorn (ASGI server hiệu năng cao).
- **Core Logic:** Các module Python xử lý chuỗi (String manipulation), sinh số ngẫu nhiên an toàn sinh trắc (Cryptographically secure RNG).

---

## 📂 Cấu trúc mã nguồn (Project Structure)

```bash
Trust-Mii-Broo/
├── backend.py                     # API Router & FastAPI Application entrypoint
├── logic/
│   ├── StrongPasswordGenerator.py # Thuật toán sinh mật khẩu ngẫu nhiên
│   └── StrongPasswordEnhancer.py  # Thuật toán cường hóa từ khóa (Base word)
└── Web/                           # Frontend Assets
    ├── home.html                  # Giao diện chính (Dashboard)
    ├── CSS/
    │   └── home.css               # Stylesheet (bao gồm Theme Engine)
    ├── JS/
    │   └── home.js                # Xử lý logic Client (Leak check, API calls, Themes)
    └── picture/                   # Tài nguyên hình ảnh, Logo
```

---

## 🚀 Hướng dẫn cài đặt & Chạy (Getting Started)

### 1. Yêu cầu hệ thống (Prerequisites)
- [Python 3.10](https://www.python.org/downloads/) trở lên.
- Trình duyệt web hiện đại (Chrome, Edge, Firefox, Safari).

### 2. Thiết lập môi trường Backend
Mở Terminal/PowerShell tại thư mục gốc của dự án:

```powershell
# Tạo môi trường ảo (Virtual Environment)
python -m venv .venv

# Kích hoạt môi trường ảo (Dành cho Windows PowerShell)
.\.venv\Scripts\Activate.ps1
# (Dành cho macOS/Linux: source .venv/bin/activate)

# Cài đặt các thư viện phụ thuộc
python -m pip install -r requirements.txt
```

### 3. Khởi chạy ứng dụng

FastAPI phục vụ cả API và frontend, vì vậy chỉ cần chạy một server:

```powershell
uvicorn backend:app --reload
```

👉 Mở giao diện tại **`http://127.0.0.1:8000`**. Tài liệu API tương tác nằm tại **`http://127.0.0.1:8000/docs`**.

---

## ☁️ Deploy trên Vercel

Dự án đã khai báo `backend:app` là entrypoint trong `pyproject.toml`, nên không cần Build Command hay Output Directory.

### Cách 1: Deploy bằng Git

1. Push repository lên GitHub, GitLab hoặc Bitbucket.
2. Vào [vercel.com/new](https://vercel.com/new) và import repository.
3. Giữ nguyên cấu hình Vercel tự nhận diện, sau đó chọn **Deploy**.
4. Kiểm tra trang chủ và endpoint `/docs` trên preview URL.

Mỗi lần push sau đó sẽ tự tạo một deployment mới.

### Cách 2: Deploy bằng Vercel CLI

```powershell
npm install --global vercel
vercel login
vercel
```

Lệnh `vercel` tạo preview deployment. Sau khi kiểm tra thành công, deploy production:

```powershell
vercel --prod
```

Frontend và API chạy cùng domain nên không cần CORS. Chỉ khi tách frontend sang domain khác, thêm biến môi trường `ALLOWED_ORIGINS` trong Vercel, ví dụ:

```text
ALLOWED_ORIGINS=https://app.example.com,https://preview.example.com
```

---

## 📖 Tài liệu API (API Reference)

Backend cung cấp các endpoints RESTful chuẩn chỉnh:

### 1. `POST /generate`
Sinh một mật khẩu hoàn toàn mới từ đầu.

**Request Body:**
```json
{
  "uppercase": true,
  "number": true,
  "special_character": true,
  "length": 16,
  "avoid_ambiguous": false
}
```

**Response:**
```json
{
  "password": "aG7!pQ2@xL9#vR4s"
}
```

### 2. `POST /enhance`
Cường hóa một từ khóa (Base word) do người dùng cung cấp.

**Request Body:**
```json
{
  "input_password": "dragon",
  "uppercase": true,
  "number": true,
  "special_character": true,
  "length": 16,
  "avoid_ambiguous": false
}
```

**Response:**
```json
{
  "password": "!Ddragon4@k8pQ"
}
```

---

## 🔒 Lưu ý bảo mật (Security Best Practices)
- ⚠️ **Base words:** Từ khóa nền (Base word) thường dễ đoán. Khuyến khích sử dụng tính năng **Generate from Scratch** để có độ bảo mật tuyệt đối.
- 🔑 **Password Manager:** Mật khẩu do hệ thống sinh ra nên được lưu trữ trong một trình quản lý mật khẩu an toàn (như Bitwarden, 1Password).
- 🌐 **Môi trường Production:** 
  - Đảm bảo triển khai Backend với chứng chỉ **HTTPS/SSL/TLS**.
  - Trong tệp `backend.py`, cấu hình `allow_origins` của CORS Middleware thay vì để `["*"]` hãy đặt chính xác domain của frontend để tránh rủi ro CSRF/XSS.

---

<div align="center">
  <sub>Được thiết kế và phát triển với ❤️ bởi đội ngũ Trust Mii Broo.</sub>
</div>
