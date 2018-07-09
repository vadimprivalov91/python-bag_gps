__author__ = "Nikita Titov"
__copyright__ = "Copyright (c) 2015 Lamonte. All rights reserved."
__credits__ = ["Nikita Titov"]
__email__ = "nmtitov@nmtitov.com"

import logging
from twilio import TwilioRestException
from twilio.rest import TwilioRestClient
from lamonte import settings

sid = settings.TWILIO_ACCOUNT_SID
auth_token = settings.TWILIO_AUTH_TOKEN
from_ = settings.TWILIO_NUMBER
client = TwilioRestClient(sid, auth_token)


def send_sms(phone, body):
    try:
        client.messages.create(to=phone, from_=from_, body=body)
    except TwilioRestException as e:
        logging.exception(e)
