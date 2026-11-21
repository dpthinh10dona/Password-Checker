from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field
import uvicorn
import os
from pathlib import Path

# Giả sử hàm logic đã chuyển sang hàm đồng bộ (def thường, bỏ async)
from logic.StrongPasswordGenerator import StrongPasswordGenerator
from logic.StrongPasswordEnhancer import StrongPasswordEnhancer 

app = FastAPI(
    title="TrustMiiBro Password Generator API",
    description="API tạo và nâng cấp mật khẩu an toàn",
    version="1.0.0"
)

BASE_DIR = Path(__file__).resolve().parent
WEB_DIR = BASE_DIR / "Web"

# Phục vụ thư mục Web chứa các file tĩnh (CSS, JS, ảnh)
if WEB_DIR.exists():
    app.mount("/Web", StaticFiles(directory=WEB_DIR), name="Web")
    # Cho phép truy cập thư mục CSS/JS trực tiếp (để tương thích với href="CSS/home.css" trong home.html)
    app.mount("/CSS", StaticFiles(directory=WEB_DIR / "CSS"), name="CSS")
    app.mount("/JS", StaticFiles(directory=WEB_DIR / "JS"), name="JS")
    app.mount("/picture", StaticFiles(directory=WEB_DIR / "picture"), name="picture")

# Route trả về trang chủ
@app.get("/")
def read_root():
    home_page = WEB_DIR / "home.html"
    if home_page.exists():
        return FileResponse(home_page)
    return {"message": "Server đang chạy! (Không tìm thấy Web/home.html)"}


# Frontend mặc định chạy cùng origin nên không cần CORS. Khi tách frontend,
# khai báo danh sách origin, phân tách bằng dấu phẩy, qua biến môi trường.
allowed_origins = [
    origin.strip()
    for origin in os.getenv("ALLOWED_ORIGINS", "").split(",")
    if origin.strip()
]
if allowed_origins:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=allowed_origins,
        allow_credentials=True,
        allow_methods=["GET", "POST"],
        allow_headers=["*"],
    )

# 2. Schema Validation với Pydantic Field
class PasswordRequest(BaseModel):
    uppercase: bool = True
    number: bool = True
    special_character: bool = True
    length: int = Field(default=16, ge=8, le=128, description="Độ dài mật khẩu từ 8 đến 128")
    avoid_ambiguous: bool = False

class EnhanceRequest(PasswordRequest):
    input_password: str = Field(default="", max_length=128, description="Mật khẩu gốc cần nâng cấp")


@app.post("/generate", status_code=status.HTTP_200_OK)
async def api_generate_password(request: PasswordRequest):
    try:
        # Nếu hàm logic không còn async, bỏ await ở đây
        password = await StrongPasswordGenerator(
            uppercase=request.uppercase,
            number=request.number,
            special_character=request.special_character,
            length=request.length,
            avoid_ambiguous=request.avoid_ambiguous
        )
        return {"password": password}
    
    except ValueError as ve:
        # Hứng lỗi nghiệp vụ (ví dụ: người dùng bỏ chọn tất cả option)
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail=str(ve)
        )
    except Exception as e:
        # Hứng lỗi hệ thống không lường trước
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
            detail="Đã xảy ra lỗi hệ thống, vui lòng thử lại sau."
        )


@app.post("/enhance", status_code=status.HTTP_200_OK)
async def api_enhance_password(request: EnhanceRequest):
    try:
        enhanced = await StrongPasswordEnhancer(
            input_password=request.input_password,
            uppercase=request.uppercase,
            number=request.number,
            special_character=request.special_character,
            length=request.length,
            avoid_ambiguous=request.avoid_ambiguous
        )
        return {"password": enhanced}
    
    except ValueError as ve:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail=str(ve)
        )
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
            detail="Đã xảy ra lỗi hệ thống, vui lòng thử lại sau."
        )


if __name__ == "__main__":
    uvicorn.run("backend:app", host="127.0.0.1", port=8000, reload=True)
