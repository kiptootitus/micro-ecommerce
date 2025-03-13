import logging

from django.contrib.auth.models import User
from django.core.mail import EmailMessage
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.views import View

from communications.utils import Communicate
from config_master import MAIL_SUBJECT, TEXT_CONTENT, NOREPLY_MAIL, TYPE_EMAIL, COD, CURRENCY_SYMBOL, \
    ORDER_CONFIRMATION_SUBJECT, ORDER_SELLER_SUBJECT, ORDER_FAILURE_SUBJECT, ORDER_IN_PROGRESS_SUBJECT, \
    RESET_PASSWORD_SUBJECT

log = logging.getLogger(__name__)

text_content = 'to be updated'


def queue_mail(msg):
    msg.send()


def get_internal_mail_list():
    MAIL_LIST = []
    user_obj = User.objects.filter(groups__name='Internal Staff Group').all()
    for user in user_obj:
        MAIL_LIST.append(user.username)
    return MAIL_LIST


class SendMail(View):
    def __init__(self, **kwargs):
        """
        This is the constructor of the class SendMail
        :param kwargs:
        """
        super().__init__(**kwargs)
        log.info('SendMail class initialized')
        self.additional_arguments = {}

    def send(self, subject, body, to_address):
        """
        This method sends an email to the user
        :param subject: The subject of the email
        :param body: The body content of the email
        :param to_address: The address to send the email to
        :return:
        """
        email = EmailMessage(subject, body, to=[to_address])
        email.send()

    def send_msg(self, msg: EmailMultiAlternatives or EmailMessage, function_name: str) -> None:
        """
        This method creates a communications object which is used to send the email message
        :param function_name: The name of the function sending the email
        :param msg: An EmailMultiAlternatives object
        :return: None
        """
        communicate = Communicate(
            message_to=msg.to[0],
            message_from=f'utils.send_mail.{str(function_name)}',
            message_type=TYPE_EMAIL,
            message=msg,
            vendor='smtp_mail',
            subject=msg.subject
        )
        communicate.send()

    def send_email_verification(self, data):
        """
        This function sends an email verification when a user registers an account
        :param data: {''
        :return:
        """

        html_message = render_to_string('email/email_verification.html', data)
        msg = EmailMultiAlternatives(MAIL_SUBJECT, TEXT_CONTENT, NOREPLY_MAIL, to=[data.get('email')], )
        msg.attach_alternative(html_message, "text/html")
        self.send_msg(msg, 'send_email_verification')

    def send_password_reset_email(self, data):
        """
        This function sends password reset email
        :param data: {
            'reset_password_token':'',
        }
        :return:
        """
        reset_password_token = data.get('reset_password_token')

        html_message = render_to_string('email/password_reset.html', data)
        msg = EmailMultiAlternatives(RESET_PASSWORD_SUBJECT, TEXT_CONTENT, NOREPLY_MAIL,
                                     to=[reset_password_token.user.email], )
        msg.attach_alternative(html_message, "text/html")
        self.send_msg(msg, 'send_email_verification')

    def send_order_confirmation(self, context_dict):
        """
        This function sends an email to the user when the order is confirmed
        To send mails on successful orders
        Send html to both customer and Office mail(to ship medicine)
        :param context_dict: {'order_id': order_id, }
        :return:
        """
        to_address = context_dict.get('email')
        context_dict['COD'] = COD
        context_dict['CURRENCY_SYMBOL'] = CURRENCY_SYMBOL
        html_message = render_to_string('email/mail_order.html', context_dict)
        SUBJECT = ORDER_CONFIRMATION_SUBJECT + " ORDER ID :" + str(context_dict.get('order_id'))
        msg = EmailMultiAlternatives(SUBJECT, text_content, NOREPLY_MAIL, to=[to_address], **self.additional_arguments)
        msg.attach_alternative(html_message, "text/html")
        self.send_msg(msg, 'send_order_confirmation')

    def send_order_to_seller(self, context_dict):
        context_dict['COD'] = COD
        seller_email = context_dict['orders'].last().vendor.active_business_type_account().email
        html_message = render_to_string('email/mail_order_seller.html', context_dict)
        SUBJECT = ORDER_SELLER_SUBJECT + ".ID :" + str(context_dict.get('order_id'))
        msg = EmailMultiAlternatives(SUBJECT, text_content, NOREPLY_MAIL, to=[seller_email])
        msg.attach_alternative(html_message, "text/html")
        self.send_msg(msg, 'send_refund_confirmation_mail')

    def send_order_failure(self, context_dict):
        """
        This function sends an email to the user when the order is failed
        :param context_dict: {'email': Email}
        :return:
        """
        to_address = context_dict.get('email')
        html_message = render_to_string('email/mail_order_failure.html', context_dict)
        msg = EmailMultiAlternatives(ORDER_FAILURE_SUBJECT, text_content, NOREPLY_MAIL, to=[to_address],
                                     **self.additional_arguments)
        msg.attach_alternative(html_message, "text/html")
        self.send_msg(msg, 'send_order_failure')

    def send_order_inprogress(self, context_dict):
        """
            To send mails on failed orders
        """

        to_address = context_dict.get('email')
        html_message = render_to_string('email/mail_order_inprogress.html', context_dict)
        #         MAIL_LIST=get_internal_mail_list()
        #         CALL_CENTRE_LIST=get_call_centre_mail_list()
        #         MAIL_LIST.extend(CALL_CENTRE_LIST)
        #         msg = EmailMultiAlternatives(ORDER_INPROGRESS_SUBJECT, text_content, NOREPLY_MAIL, to=[to_address],bcc=MAIL_LIST)
        msg = EmailMultiAlternatives(ORDER_IN_PROGRESS_SUBJECT, text_content, NOREPLY_MAIL, to=[to_address],
                                     **self.additional_arguments)
        msg.attach_alternative(html_message, "text/html")
        self.send_msg(msg, 'send_order_inprogress')