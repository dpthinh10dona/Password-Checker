from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field
import uvicorn
import os

# Giả sử hàm logic đã chuyển sang hàm đồng bộ (def thường, bỏ async)
from logic.StrongPasswordGenerator import StrongPasswordGenerator
from logic.StrongPasswordEnhancer import StrongPasswordEnhancer 

app = FastAPI(
    title="TrustMiiBro Password Generator API",
    description="API tạo và nâng cấp mật khẩu an toàn",
    version="1.0.0"
)

# Phục vụ thư mục Web chứa các file tĩnh (CSS, JS, ảnh)
if os.path.exists("Web"):
    app.mount("/Web", StaticFiles(directory="Web"), name="Web")
    # Cho phép truy cập thư mục CSS/JS trực tiếp (để tương thích với href="CSS/home.css" trong home.html)
    app.mount("/CSS", StaticFiles(directory="Web/CSS"), name="CSS")
    app.mount("/JS", StaticFiles(directory="Web/JS"), name="JS")
    app.mount("/picture", StaticFiles(directory="Web/picture"), name="picture")

# Route trả về trang chủ
@app.get("/")
def read_root():
    if os.path.exists("Web/home.html"):
        return FileResponse("Web/home.html")
    return {"message": "Server đang chạy! (Không tìm thấy Web/home.html)"}


# 1. Bảo mật CORS (Thay '*' bằng domain thực tế khi deploy)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # TODO: Đổi thành ["https://yourdomain.com"] khi deploy
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)

# 2. Schema Validation với Pydantic Field
class PasswordRequest(BaseModel):
    uppercase: bool = True
    number: bool = True
    special_character: bool = True
    length: int = Field(default=16, ge=4, le=128, description="Độ dài mật khẩu từ 4 đến 128")
    avoid_ambiguous: bool = False

class EnhanceRequest(PasswordRequest):
    input_password: str = Field(default="", max_length=256, description="Mật khẩu gốc cần nâng cấp")


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