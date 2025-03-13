import random


def generate_random_string(length: int = 6) -> str:
    """
    Generates a random string of the given length
    :param length: The length of the string to generate
    :return: The generated string
    """
    return ''.join(random.choices('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789', k=length))
#