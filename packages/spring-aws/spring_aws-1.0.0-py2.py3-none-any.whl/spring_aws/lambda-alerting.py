from __future__ import print_function
import sendgrid
import os
import json
from sendgrid.helpers.mail import *

# SCRIPT CONSTANTS

sg = sendgrid.SendGridAPIClient(apikey=os.environ.get('SENDGRID_API_KEY'))
from_email = Email("aaron.humphrey@spring.co.nz")
to_email = Email("jiwan@spring.co.nz")


def format_message(msg, msg_type):
    alarm_name = msg['AlarmDescription']
    reason = msg['NewStateReason']
    alarm_time = msg['StateChangeTime']
    state = msg['NewStateValue']

    prefix = ''
    status = ''
    if state == 'ALARM':
        prefix = 'PROBLEM'
        status = 'is down'
    elif state == 'OK':
        prefix = 'INFO'
        status = 'is back online'

    if msg_type == 'subject':
        return prefix + ': ' + alarm_name + ' ' + status
    elif msg_type == 'content':
        return """
        ISSUE! {alarm_name!s} {status!s}
        Issue occured at: {alarm_time!s}

        Thanks
        Jiwan
        """.format(**locals())


def lambda_handler(event, context):
    message = event['Records'][0]['Sns']['Message']
    message_digest = json.loads(message)

    # print("Received event: " + json.dumps(event, indent=2))
    subject = format_message(message_digest, 'subject')
    content = Content("text/plain", format_message(message_digest, 'content'))
    mail = Mail(from_email, subject, to_email, content)

    response = sg.client.mail.send.post(request_body=mail.get())
    print(response.status_code)
    print(response.body)
    print(response.headers)
