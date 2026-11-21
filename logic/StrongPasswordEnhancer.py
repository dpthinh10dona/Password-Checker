import secrets
import string


async def StrongPasswordEnhancer(input_password: str,
                                 uppercase: bool,
                                 number: bool,
                                 special_character: bool,
                                 length: int,
                                 avoid_ambiguous: bool = False) -> str:
    if length < 8 or length > 128:
        raise ValueError("Mật khẩu phải có độ dài từ 8 đến 128 ký tự!")

    ambiguous_chars = set("il1Lo0O")
    base_word = input_password.strip()

    if avoid_ambiguous:
        base_word = "".join(c for c in base_word if c not in ambiguous_chars)
        if not base_word:
            base_word = "secure"

    letters_lower = "".join(
        c for c in string.ascii_lowercase
        if not (avoid_ambiguous and c in ambiguous_chars)
    )
    letters_upper = "".join(
        c for c in string.ascii_uppercase
        if not (avoid_ambiguous and c in ambiguous_chars)
    ) if uppercase else ""
    digits = "".join(
        c for c in string.digits
        if not (avoid_ambiguous and c in ambiguous_chars)
    ) if number else ""
    special_chars = "~!?@#$%^&*" if special_character else ""
    all_pool = letters_lower + letters_upper + digits + special_chars

    if not all_pool:
        raise ValueError("Hãy chọn ít nhất một nhóm ký tự để nâng cấp!")

    # Giữ tối đa phần từ gốc nhưng luôn chừa chỗ cho các nhóm ký tự
    # bắt buộc. Lặp lại vì việc cắt chuỗi có thể loại một ký tự đại diện.
    base_word = base_word[:length]
    while True:
        required_groups = [letters_lower]
        if uppercase:
            required_groups.append(letters_upper)
        if number:
            required_groups.append(digits)
        if special_character:
            required_groups.append(special_chars)

        missing_groups = [
            group for group in required_groups
            if group and not any(c in group for c in base_word)
        ]
        max_base_length = length - len(missing_groups)
        if len(base_word) <= max_base_length:
            break
        base_word = base_word[:max_base_length]

    extra_chars = [secrets.choice(group) for group in missing_groups]
    remaining_count = length - len(base_word) - len(extra_chars)
    for _ in range(remaining_count):
        extra_chars.append(secrets.choice(all_pool))

    secrets.SystemRandom().shuffle(extra_chars)
    half = len(extra_chars) // 2
    prefix = "".join(extra_chars[:half])
    suffix = "".join(extra_chars[half:])
    return f"{prefix}{base_word}{suffix}"
