from django.contrib.auth.models import User

from accounts.models import AccountsManager, Address


class AccountsHandler:

    def __init__(self):
        self.accounts_manager = AccountsManager()

    def get_all_users(self) -> User.objects:
        """
        This method returns all the users
        :return: User.objects
        """
        return self.accounts_manager.get_all_users()

    def create_update_vendor(self, data: dict) -> User:
        """
        This method creates or updates a vendor object
        :param data: {
            'email': The username of the vendor
            'password': The password of the vendor
            'role: The user role
        }
        :return: User
        """
        return self.accounts_manager.create_update_vendor(data)

    def generate_otp_for_email(self, email):
        """
        This method generates an OTP for the phone number, sets it to cache and returns it
        :param email: The email of the user
        :return:
        """
        return self.accounts_manager.generate_otp_for_email(email)

    def verify_email_verification_code(self, email, code):
        """
        This function verifies the password reset code
        :param email: The email of the user
        :param code: The code to be verified
        :return:
        """
        return self.accounts_manager.verify_email_verification_code(email, code)

    def change_user_status(self, email, status: bool) -> User:
        """
        This method sets user status to true or False
        :param email: The email of the user
        :param status: The value of the status
        :return: User
        """
        return self.accounts_manager.change_user_status(email, status)

    def create_address(self, data: dict) -> Address:
        """
        This method creates an address object
        :param data: {
            'address_line': The address line,
            'province': The province,
            'city': The city value,
            'street': The street value,
            'created_by': The created by value
        }
        :return: Address
        """
        return self.accounts_manager.create_address(data)

    def get_user_by_email(self, data: dict) -> User or None:
        """
        This method returns a user by email
        :param data: {
            'email': The email value,
        }
        :return: User
        """
        return self.accounts_manager.get_user_by_email(data)

    def get_all_addresses(self):
        """
        This method returns all the address objects
        :return:
        """
        return self.accounts_manager.get_all_addresses()

    def verify_address(self, data: dict) -> True or False:
        """
        This method verify a particular address
        :param data: {
            'address_id': The ID value of the address,
            'verification_code': The verification code of the address,
        }
        :return: Address
        """
        return self.accounts_manager.verify_address(data)

    def create_update_user(self, data: dict) -> User:
        """
        This method creates or updates a vendor object
        :param data: {
            'email': The username of the vendor
            'password': The password of the vendor
            'role: The user role
            'first_name: The first name
            'last_name: The last name
        }
        :return:
        """
        return self.accounts_manager.create_update_user(data)

    def get_profile_address(self, data):
        """
        This method returns the default profile address of a user
        :param data: {
            'user': The user object
        }
        :return:
        """
        return self.accounts_manager.get_profile_address(data)

    def create_profile_address(self, data: dict):
        """
        This method creates a new profile address for a user
        :param data: {
            'title':'',
            'first_name':'',
            'last_name':'',
            'phone':'',
            'other_phone':'',
            'house_number':'',
            'building_name':'',
            'landmark':'',
            'province':'',
            'city':'',
            'street':'',
            'user':''
        }
        :return:
        """
        return self.accounts_manager.create_profile_address(data)

    def get_all_profile_address_of_user(self, data: dict):
        """
        This method returns all the profile address objects of a user
        :param data: {
            'user': The user object
        }
        :return:
        """
        return self.accounts_manager.get_all_profile_address_of_user(data)

    def fetch_account(self, user):
        """
        This method fetches the account of the user.
        :param user:
        :return:
        """
        return self.accounts_manager.fetch_account(user)

    def fetch_contact(self, user):
        """
        This method fetches the contact details of the user.
        :param user:
        :return:
        """
        return self.accounts_manager.fetch_contact(user)