import logging

from django.core.mail import EmailMultiAlternatives

from communications.communications_handler import CommunicationsHandler
from communications.smtp_mail import SMTPMail
from config_master import STATUS_PENDING

log = logging.getLogger(__name__)


class Communicate:
    def __init__(self,
                 message_to: str,
                 message_from: str,
                 message_type: str,
                 message: str or EmailMultiAlternatives,
                 vendor: str = None,
                 subject: str = '') -> None:
        """
        This method is called when creating an object of the class
        :param message_to: The address of the recipient of a message e.g. email address, phone number
        :param message_from: The app, script or user that is sending the message
        :param message_type: The type of message to be sent ie SMS, EMAIL
        :param message: The message content
        :param vendor: The preferred vendor to send the message e.g. smtp_mail
        :param subject: The subject of a message.
        """
        log.info('Communicate class initialized')
        self.message_from = message_from
        self.message_to = message_to
        self.message_type = message_type
        self.message = message
        self.vendor = vendor
        self.email_map = {'smtp_mail': SMTPMail, }
        self.vendor_object = None
        self.vendor_name = None
        self.subject = subject
        self.communications_handler = CommunicationsHandler()

    def select_vendor(self, vendor: str = None) -> True or False:
        """
        This method selects between various vendors that will be responsible for sending the message
        :param vendor: The preferred vendor to send the message. Options are text_local, smtp_mail, mail_chimp
        :return: True is the selection was successful else False
        """
        log.info('Selecting communication vendor')
        if vendor:
            self.vendor = vendor
        self.vendor = self.vendor if self.vendor else 'smtp_mail'

        if self.vendor in self.email_map:
            self.vendor_object = self.email_map[self.vendor]()
        else:
            log.error("The vendor you selected does not exist! Vendor choices are text_local, smtp_mail, mail_chimp")
            return False
        log.info('Selecting communication vendor was successful')
        return True

    def send(self, ) -> {}:
        """
        This method send a message using the selected vendor, saves the response and returns the response to the
        calling function
        :return: Dictionary of response
        """
        log.info('Sending message')
        data = {
            'subject': self.subject,
            'message_from': self.message_from,
            'message_to': self.message_to,
            'message': self.message,
            'type': self.message_type,
            'created_by': 'communications.utils.Communicate.send',
            'vendor': self.vendor,
        }
        vendor_selected = self.select_vendor(vendor=self.vendor)
        if not vendor_selected:
            log.error('Could not select a vendor')
            data['status'] = STATUS_PENDING
            self.communications_handler.create_communication(data)
        else:
            response = self.vendor_object.process(data)
            data.update(response)
            if 'error' in data:
                log.error('An error occurred while sending the message')
            else:
                log.info('Message has been sent successfully')
        self.communications_handler.create_communication(data)
        return data