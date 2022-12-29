from secrets import token_hex

def gen_rule():
    return token_hex(16)

