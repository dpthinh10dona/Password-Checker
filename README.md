# Trust Mii Broo – Password Checker & Generator

Ứng dụng web giúp kiểm tra độ mạnh mật khẩu, kiểm tra mật khẩu có xuất hiện trong các vụ rò rỉ phổ biến hay không, đồng thời sinh hoặc nâng cấp mật khẩu theo tiêu chí người dùng chọn.

## Tính năng

- Đánh giá độ mạnh và ước tính thời gian bẻ mật khẩu bằng [zxcvbn](https://github.com/dropbox/zxcvbn).
- Kiểm tra mật khẩu rò rỉ qua dịch vụ Pwned Passwords theo cơ chế k-anonymity: trình duyệt chỉ gửi 5 ký tự đầu của mã băm SHA-1, không gửi mật khẩu thô.
- Sinh mật khẩu mới theo độ dài và các nhóm ký tự: chữ hoa, số, ký tự đặc biệt.
- Nâng cấp mật khẩu từ một **base word**: giữ base word trong kết quả và bổ sung các nhóm ký tự đã chọn.
- Tùy chọn loại bỏ ký tự dễ nhầm như `I`, `l`, `O`, `0`.

## Công nghệ

- Frontend: HTML, CSS, JavaScript thuần
- Backend: Python, FastAPI, Uvicorn
- Thư viện frontend: zxcvbn (CDN)

## Cấu trúc dự án

```text
.
├── backend.py                     # FastAPI API
├── logic/
│   ├── StrongPasswordGenerator.py # Sinh mật khẩu từ đầu
│   └── StrongPasswordEnhancer.py  # Nâng cấp từ base word
└── Web/
    ├── home.html                  # Giao diện chính
    ├── CSS/home.css
    ├── JS/home.js
    └── picture/
```

## Cài đặt và chạy

Yêu cầu: Python 3.10+.

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install fastapi "uvicorn[standard]"
```

Mở một terminal để chạy API:

```powershell
uvicorn backend:app --reload
```

API sẽ chạy tại `http://127.0.0.1:8000` và tài liệu tương tác có tại `http://127.0.0.1:8000/docs`.

Mở terminal thứ hai để phục vụ frontend:

```powershell
python -m http.server 5500 --directory Web
```

Sau đó truy cập `http://127.0.0.1:5500/home.html`.

> Frontend hiện gọi backend tại `http://127.0.0.1:8000`. Hãy chạy cả hai dịch vụ khi phát triển cục bộ.

## Sử dụng Password Generator

### From Scratch

Chọn độ dài và các loại ký tự muốn có, sau đó bấm **Generate**. Mật khẩu luôn có chữ thường; nếu bật các tùy chọn còn lại, kết quả sẽ có ít nhất một chữ hoa, số hoặc ký tự đặc biệt tương ứng.

### From Input

Nhập base word, chọn độ dài và các tiêu chí trong chính tab **From Input**, rồi bấm **Generate**. Ví dụ, với `dragon`, bật chữ hoa, số và ký tự đặc biệt, kết quả có thể là `?3Ddragon@x7K`.

Nếu bật **Avoid Tricky**, các ký tự dễ nhầm sẽ được loại khỏi phần được sinh thêm; các ký tự đó trong base word cũng được loại để tuân theo tùy chọn này.

## API

### `POST /generate`

Sinh mật khẩu mới.

```json
{
  "uppercase": true,
  "number": true,
  "special_character": true,
  "length": 16,
  "avoid_ambiguous": false
}
```

Phản hồi:

```json
{
  "password": "aG7!pQ2@xL9#vR4s"
}
```

### `POST /enhance`

Nâng cấp base word theo các tiêu chí đã chọn.

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

Phản hồi:

```json
{
  "password": "!Ddragon4@k8pQ"
}
```

## Lưu ý bảo mật

- Đừng dùng mật khẩu sinh ra cho nhiều tài khoản quan trọng.
- Base word thường dễ đoán; hãy ưu tiên dùng trình quản lý mật khẩu và mật khẩu ngẫu nhiên, dài.
- Khi triển khai production, giới hạn `allow_origins` trong CORS ở `backend.py` thành domain frontend thực tế thay vì `*`.

## Giấy phép

Chưa có giấy phép được khai báo. Hãy thêm tệp `LICENSE` trước khi phát hành hoặc chia sẻ công khai.
