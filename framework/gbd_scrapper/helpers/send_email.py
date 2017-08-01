import sendgrid

class SendgridEmailHelper:
    @staticmethod
    def send_email(scrapper_name, to_email, subject):
        sg = sendgrid.SendGridClient('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')
        message = sendgrid.Mail()
        message.add_to(to_email)
        message.set_subject(subject)
        # message.set_html('{} has completed.'.format(scrapper_name))
        message.set_text('{} has completed.'.format(scrapper_name))
        message.set_from(to_email)
        status, msg = sg.send(message)
        return status
