import random
import string


def convert_django_choices_to_str(choices_list: list) -> str:
    """
    This method converts a django choices field into a string representation
    :param choices_list: List of lists
    :return: str
    """
    output_string = ''
    for choice in choices_list:
        output_string += f'{str(choice[0])}, '
    return output_string


class OutOfStockException(Exception):
    pass


class PaymentErrorException(Exception):
    pass


class InvalidInputException(Exception):
    pass


def generate_random_string(length: int) -> str:
    """
    This method creates random string of length
    :param length: The number of characters
    :return: string
    """
    return ''.join((random.choice(string.ascii_lowercase) for _ in range(length)))