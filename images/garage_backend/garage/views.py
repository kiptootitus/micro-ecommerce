# Create your views here.
import logging
from html import escape
from io import BytesIO

from django.http import HttpResponse
from django.template.loader import get_template
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from xhtml2pdf import pisa

from accounts.accounts_handler import AccountsHandler
from config_master import COOKIES_EXPIRY_SECONDS, COOKIES_SECURE, DOMAIN

log = logging.getLogger(__name__)


class TestView(APIView):
    # add permission to check if user is authenticated
    permission_classes = (AllowAny,)

    # 1. List all
    def post(self, request, *args, **kwargs):
        log.info('Visiting the test view')
        log.info('=============================================================')
        test_cookie = request.COOKIES.get('test_cookie')
        log.info(f'The value of test_cookie = {str(test_cookie)}')
        log.info('=============================================================')
        response = Response({'message': 'success'}, status=status.HTTP_200_OK)
        response.set_cookie('test_cookie', '2000', max_age=COOKIES_EXPIRY_SECONDS, secure=COOKIES_SECURE,
                            domain=DOMAIN)
        return response


class APIBaseView(APIView):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.context_dict = {}
        self.accounts_handler = AccountsHandler()

    def validate_arguments(self, name_list: list, data):
        """
        This function validates if values passed in the name list are passed in the data
        :param name_list: The name that we are looking for
        :param data: The data passed in the request
        :return:
        """
        required_arguments = {}
        for name in name_list:
            if not data.get(name):
                log.error(f'{str(name)} was not passed in the argument')
                required_arguments[name] = 'This field is required.'
        return required_arguments


def render_to_pdf(template_src, context_dict):
    """
    This function renders a html template file and converts the html file to a PDF for download
    :param template_src: The path of the html template file
    :param context_dict: The Context to render
    :return:
    """
    template = get_template(template_src)
    html = template.render(context_dict)
    result = BytesIO()

    pdf = pisa.pisaDocument(BytesIO(html.encode("UTF-8")), result)
    if not pdf.err:
        return HttpResponse(result.getvalue(), content_type='application/pdf')
    return HttpResponse('We had some errors<pre>%s</pre>' % escape(html))