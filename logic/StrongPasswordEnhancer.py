import string
import secrets
import asyncio

async def StrongPasswordEnhancer(input_password: str,
                                 uppercase: bool, 
                                 number: bool, 
                                 special_character: bool, 
                                 length: int,
                                 avoid_ambiguous: bool = False) -> str:
    
    ambiguous_chars = set("il1Lo0O")
    
    base_word = input_password.strip()
    
    if avoid_ambiguous:
        base_word = "".join(c for c in base_word if c not in ambiguous_chars)
        if not base_word:
            base_word = "secure"

    # 2. Định nghĩa các tập ký tự theo luật hiển thị trên UI
    letters_lower = "".join(c for c in string.ascii_lowercase if not (avoid_ambiguous and c in ambiguous_chars))
    letters_upper = "".join(c for c in string.ascii_uppercase if not (avoid_ambiguous and c in ambiguous_chars)) if uppercase else ""
    digits = "".join(c for c in string.digits if not (avoid_ambiguous and c in ambiguous_chars)) if number else ""
    
    # Giới hạn tập ký tự đặc biệt thân thiện
    special_chars = "~!?@#$%^&*" if special_character else ""
    
    # 3. Gom các ký tự gia vị bắt buộc phải có
    extra_chars = []
    if uppercase and letters_upper and not any(c in letters_upper for c in base_word):
        extra_chars.append(secrets.choice(letters_upper))
    if number and digits and not any(c in digits for c in base_word):
        extra_chars.append(secrets.choice(digits))
    if special_character and special_chars and not any(c in special_chars for c in base_word):
        extra_chars.append(secrets.choice(special_chars))
        
    # 4. Tính toán độ dài mục tiêu
    min_required_length = len(base_word) + len(extra_chars)
    target_length = max(length, min_required_length)
    
    all_pool = letters_lower + letters_upper + digits + special_chars
    if not all_pool:
        return "Lỗi: Hãy chọn ít nhất một nhóm ký tự để nâng cấp!"
        
    # Bổ sung nốt số ký tự còn thiếu
    remaining_count = target_length - min_required_length
    for _ in range(remaining_count):
        extra_chars.append(secrets.choice(all_pool))
        
    # Trộn tập ký tự thêm vào
    secrets.SystemRandom().shuffle(extra_chars)
    
    # Kẹp chuỗi gốc base_word vào giữa các ký tự bổ sung
    half = len(extra_chars) // 2
    prefix = "".join(extra_chars[:half])
    suffix = "".join(extra_chars[half:])
    
    final_password = f"{prefix}{base_word}{suffix}"
    
    return final_password[:target_length]
