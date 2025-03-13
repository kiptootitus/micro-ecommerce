import brevo_python
import datetime
import json
import logging
import pandas as pd
from brevo_python.rest import ApiException
from config_master import STATUS_PENDING, SEND_BLUE_API_KEY, STATUS_FAILED, WEBSITE_NAME, \
    SEND_BLUE_SENDER_EMAIL, DOMAIN, STATUS_SENT, TZ
from django.core.mail import EmailMultiAlternatives
from django.urls import reverse
from django.utils.timezone import now

log = logging.getLogger(__name__)


class SendBlue:
    """
    This is a wrapper class for the SendBlue emailing.
    """

    def __init__(self, ) -> None:
        """
        Initialize the SendBlue class.
        """
        log.info('SendBlue class initialized')
        self.response = {'status': STATUS_PENDING}
        configuration = brevo_python.Configuration()
        configuration.api_key['api-key'] = SEND_BLUE_API_KEY
        self.api_instance = brevo_python.TransactionalEmailsApi(brevo_python.ApiClient(configuration))
        self.campaign_api = brevo_python.EmailCampaignsApi(brevo_python.ApiClient(configuration))
        self.sender = {"name": f"Kenneth from {WEBSITE_NAME}", "email": SEND_BLUE_SENDER_EMAIL}
        self.contacts_api = brevo_python.ContactsApi(brevo_python.ApiClient(configuration))
        # self.list_api = brevo_python.ListsApi(brevo_python.ApiClient(configuration))

    def process(self, data: dict) -> dict:
        """
        Process the data dictionary and send the SMS message.
        :param data: {
            'message_to': '+1234567890',
            'message': 'Hello World'
            'subject': The subject of the mail,
            'name': The name of the user,
            }
        :return: dict
        """
        if data.get('message') and isinstance(data['message'], dict) and data['message'].get(
                'handler') == 'initiate_campaign_mail':
            return self.initiate_campaign_mail(data)
        return self.send_smtp_mail(data)

    def initiate_campaign_mail(self, data):
        """
        This method calls the methods that will create campaign, create a list and add contacts to that list
        """
        extras = data.get('extras') or {}
        email_list = self.create_list(data)

        if isinstance(email_list, str):
            self.response['status'] = STATUS_FAILED
            self.response['error'] = email_list
            self.response['extras'] = extras
            return self.response
        # failed_emails_df=self.add_contacts_to_list({
        #     'id':email_list.id,
        #     'emails':data.get('message_to'),
        # })
        data['list_id'] = email_list.id
        extras['list_id'] = email_list.id

        campaign_response = self.create_email_campaign(data)
        if isinstance(campaign_response, str):
            self.response['status'] = STATUS_FAILED
            self.response['error'] = campaign_response
            self.response['extras'] = extras
            return self.response

        data['campaign_id'] = campaign_response.id
        extras['campaign_id'] = campaign_response.id

        self.add_multiple_contacts_to_send_blue(data)
        self.response['status'] = STATUS_PENDING
        self.response['extras'] = extras

        return self.response

    def send_smtp_mail(self, data):
        """
        This method sends smt mail to users
        """
        smtp_email_arguments = {
            'subject': data.get('subject'),
            'sender': self.sender,

        }

        if isinstance(data.get('message_to'), list):
            to = []
            for email in data.get('message_to'):
                to.append({'email': email})
            smtp_email_arguments['bcc'] = to

        else:
            to = [
                {
                    "email": data.get('message_to'),
                }
            ]
            smtp_email_arguments['to'] = to

        if data.get('message') and isinstance(data.get('message'), EmailMultiAlternatives):
            message = data.get('message')
            data['message'] = message.alternatives[0][0]
            smtp_email_arguments['html_content'] = message.alternatives[0][0]
        else:
            smtp_email_arguments['template_id'] = data['message'].get('template_id')
            smtp_email_arguments['params'] = data['message'].get('params')

        send_smtp_email = brevo_python.SendSmtpEmail(**smtp_email_arguments)

        try:
            response = self.api_instance.send_transac_email(send_smtp_email)

            extras = data.get('extras') or {}
            extras['message_id'] = response.message_id
            self.response['status'] = STATUS_SENT
            self.response['send_time'] = datetime.datetime.now(TZ)
        except ApiException as e:
            logging.exception(e)
            self.response['status'] = STATUS_FAILED
            self.response['error'] = str(e)
        return self.response

    def create_email_campaign(self, data):
        """
        This method is used to create an email campaign
        :param data: {
            'message_to': '+1234567890',
            'message': 'Hello World'
            'subject': The subject of the mail,
            'name': The name of the user,
            }
        :return: dict
        """
        log.info('Creating email campaign ')
        campaign_email_arguments = {
            'subject': data.get('subject'),
            'sender': self.sender,
            'name': f'{str(data.get("subject"))} - campaign - {str(now())}',
            'recipients': {'listIds': [data.get('list_id')]}
        }

        if data.get('message') and isinstance(data.get('message'), EmailMultiAlternatives):
            message = data.get('message')
            data['message'] = message.alternatives[0][0]
            campaign_email_arguments['html_content'] = message.alternatives[0][0]
        else:
            campaign_email_arguments['template_id'] = data['message'].get('template_id')
            campaign_email_arguments['params'] = data['message'].get('params')

        mail_campaigns = brevo_python.CreateEmailCampaign(**campaign_email_arguments)

        try:
            api_response = self.campaign_api.create_email_campaign(mail_campaigns)
            return api_response
        except ApiException as e:
            log.error("Exception when calling EmailCampaignsApi->create_email_campaign: %s\n" % e)
            return str(e)

    def send_email_campaign(self, campaign_id):
        """
        This method sends an email campaign
        """
        response = {
            'campaign_id': campaign_id,
        }
        try:
            self.campaign_api.send_email_campaign_now(campaign_id)
            response['status'] = STATUS_SENT
        except ApiException as e:
            log.error("Exception when calling EmailCampaignsApi->send_email_campaign_now: %s\n" % e)
            response['status'] = STATUS_FAILED
            response['error'] = str(e)
        return response

    def add_contacts_to_send_in_blue(self, data):
        """
        This method adds contacts to send in blue
        """
        create_campaign_arguments = {
            'email': data.get('email'),
            'update_enabled': True,
            'list_ids': [4, 7, 6],
            'attributes': {
                'FIRSTNAME': data.get('firstname')
            }
        }
        create_contact = brevo_python.CreateContact(**create_campaign_arguments)
        try:
            api_response = self.contacts_api.create_contact(create_contact)
            return api_response
        except ApiException as e:
            print("Exception when calling ContactsApi->create_contact: %s\n" % e)

    def create_list(self, data):
        """
        This method creates a list
        """
        log.info('Creating list for the email campaign')
        name = f'{str(data.get("subject"))} list - {str(now())}'[:50]
        create_list = brevo_python.CreateList(name=name, folder_id=1)

        try:
            api_response = self.contacts_api.create_list(create_list)
            return api_response
        except ApiException as e:
            log.error("Exception when calling ContactsApi->create_list: %s\n" % e)
            return str(e)

    def add_contacts_to_list(self, data):
        """
        This method adds contacts to a list
        """
        list_id = data.get('id')
        contact_emails = brevo_python.AddContactToList()
        number_of_emails_to_add = 150
        emails = data.get('emails')
        contact_emails.emails = emails[:number_of_emails_to_add]
        data['emails'] = emails[number_of_emails_to_add:]
        combined_df = pd.DataFrame()
        try:
            api_response = self.contacts_api.add_contact_to_list(list_id, contact_emails)
            failed_emails_dict = {
                'emails': api_response.contacts.failure,
            }
            response_pd = pd.DataFrame(failed_emails_dict)
            combined_df = pd.concat([combined_df, response_pd])

        except ApiException as e:
            log.error("Exception when calling ListsApi->add_contact_to_list: %s\n" % e)
        log.info(
            f'Finished adding emails {len(emails[:number_of_emails_to_add])} to list. Remaining count {str(len(data["emails"]))}')
        if data['emails']:
            split_contact_response = self.add_contacts_to_send_in_blue(data)
            combined_df = pd.concat([combined_df, split_contact_response])
        return combined_df

    def add_multiple_contacts_to_send_blue(self, data):
        """
        This method adds email contacts to send in blue
        """
        campaign_id = data.get('campaign_id')
        email_df = pd.DataFrame({'email': data.get('message_to')})
        json_body = json.loads(email_df.to_json(orient='records'))
        request_contact_import = brevo_python.RequestContactImport()
        request_contact_import.json_body = json_body
        request_contact_import.notify_url = f'{str(DOMAIN)}{reverse("send_blue_send_campaign", kwargs={"campaign_id": campaign_id})}'
        request_contact_import.list_ids = [data.get('list_id')]
        request_contact_import.email_blacklist = False
        request_contact_import.sms_blacklist = False
        request_contact_import.update_existing_contacts = True

        try:
            api_response = self.contacts_api.import_contacts(request_contact_import)
            return api_response
        except ApiException as e:
            log.error("Exception when calling ContactsApi->import_contacts: %s\n" % e)