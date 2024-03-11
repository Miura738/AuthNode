def uuid_parse(uuid: str):
    return uuid.replace('-', '')


def uuid_encode(uuid: str):
    if len(uuid) != 32 or not all(c in '0123456789abcdefABCDEF' for c in uuid):
        raise ValueError("无效的UUID格式")

        # 按照8-4-4-4-12的格式插入连字符
    return f"{uuid[:8]}-{uuid[8:12]}-{uuid[12:16]}-{uuid[16:20]}-{uuid[20:]}"
