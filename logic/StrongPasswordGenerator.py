import secrets
import string


async def StrongPasswordGenerator(uppercase: bool,
                                  number: bool,
                                  special_character: bool,
                                  length: int,
                                  avoid_ambiguous: bool = False) -> str:
    if length < 8 or length > 128:
        raise ValueError("Mật khẩu phải có độ dài từ 8 đến 128 ký tự!")

    ambiguous_chars = set("il1Lo0O")
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

    allowed_symbols = "~!?@#$%^&*"
    special_chars = allowed_symbols if special_character else ""
    all_characters = letters_lower + letters_upper + digits + special_chars

    if not all_characters:
        raise ValueError("Bạn phải chọn ít nhất một nhóm ký tự hợp lệ!")

    password = [secrets.choice(letters_lower)]
    if uppercase:
        password.append(secrets.choice(letters_upper))
    if number:
        password.append(secrets.choice(digits))
    if special_character:
        password.append(secrets.choice(special_chars))

    for _ in range(length - len(password)):
        password.append(secrets.choice(all_characters))

    secrets.SystemRandom().shuffle(password)
    return "".join(password)
