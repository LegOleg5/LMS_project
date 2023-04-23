import random


def generate_code():
    symbols = '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ!#$%&()*+-?@_~'
    code = ''
    for _ in range(16):
        code += symbols[random.randint(0, 75)]
    return code
