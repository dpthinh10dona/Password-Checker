import string
import secrets

async def StrongPasswordGenerator(uppercase: bool, 
                                  number: bool, 
                                  special_character: bool, 
                                  length: int,
                                  avoid_ambiguous: bool = False) -> str:
    # 1. Kiểm tra giới hạn độ dài theo requirement (8 -> 128)
    if length < 8 or length > 128:
        return "Lỗi: Mật khẩu phải có độ dài từ 8 đến 128 ký tự!"
      
    ambiguous_chars = set("il1Lo0O")
      
    # 2. Xây dựng tập ký tự dựa theo tùy chọn của user
    letters_lower = "".join(c for c in string.ascii_lowercase if not (avoid_ambiguous and c in ambiguous_chars))
    letters_upper = "".join(c for c in string.ascii_uppercase if not (avoid_ambiguous and c in ambiguous_chars)) if uppercase else ""
    digits = "".join(c for c in string.digits if not (avoid_ambiguous and c in ambiguous_chars)) if number else ""
    
    # Chỉ lấy đúng tập ký tự đặc biệt được phép: ~!?@#$%^&*
    allowed_symbols = "~!?@#$%^&*"
    special_chars = "".join(c for c in allowed_symbols if not (avoid_ambiguous and c in ambiguous_chars)) if special_character else ""
    
    all_characters = letters_lower + letters_upper + digits + special_chars
    
    if not all_characters:
        return "Lỗi: Bạn phải chọn ít nhất một nhóm ký tự hợp lệ!"

    # 3. Đảm bảo có ít nhất 1 ký tự đại diện từ mỗi nhóm người dùng đã tích chọn
    password = []
    
    if letters_lower:
        password.append(secrets.choice(letters_lower))
    if uppercase and letters_upper:
        password.append(secrets.choice(letters_upper))
    if number and digits:
        password.append(secrets.choice(digits))
    if special_character and special_chars:
        password.append(secrets.choice(special_chars))
        
    # 4. Lấp đầy phần còn lại
    remaining = length - len(password)
    for _ in range(remaining):
        password.append(secrets.choice(all_characters))
    
    # 5. Xáo trộn ngẫu nhiên
    secrets.SystemRandom().shuffle(password)
    
    return "".join(password)