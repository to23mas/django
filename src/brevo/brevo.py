import os
import sib_api_v3_sdk
from sib_api_v3_sdk.rest import ApiException
import logging

logger = logging.getLogger(__name__)

def send_registration_email(username: str, user_email: str, verify_url: str):
	configuration = sib_api_v3_sdk.Configuration()
	configuration.api_key['api-key'] = os.getenv('BREVO_KEY')

	if not os.getenv('BREVO_KEY'):
		logger.error("BREVO_KEY environment variable is not set")
		return

	api_instance = sib_api_v3_sdk.TransactionalEmailsApi(sib_api_v3_sdk.ApiClient(configuration))
	subject = "Potvrzení registrace"
	sender = {
		"name":"Django",
		"email": os.getenv('BREVO_SENDER'),
	}

	if not os.getenv('BREVO_SENDER'):
		logger.error("BREVO_SENDER environment variable is not set")
		return

	html_content = f'''<html><body>
	<h1>Pro dokončení registrace je potřeba kliknout na link níže</h1>
	<br /><br />
	<a href="{verify_url}">Potvrdit registraci</a>
	</body></html>'''

	to = [{"email": user_email, "name": username}]
	send_smtp_email = sib_api_v3_sdk.SendSmtpEmail(to=to, bcc=None, cc=None, headers=None, html_content=html_content, sender=sender, subject=subject)

	try:
		api_response = api_instance.send_transac_email(send_smtp_email)
		logger.info(f"Registration email sent successfully to {user_email}")
		return True
	except ApiException as e:
		logger.error(f"Failed to send registration email to {user_email}: {str(e)}")
		return False

def send_password_reset_email(username: str, user_email: str, reset_url: str):
	configuration = sib_api_v3_sdk.Configuration()
	configuration.api_key['api-key'] = os.getenv('BREVO_KEY')

	if not os.getenv('BREVO_KEY'):
		logger.error("BREVO_KEY environment variable is not set")
		return

	api_instance = sib_api_v3_sdk.TransactionalEmailsApi(sib_api_v3_sdk.ApiClient(configuration))
	subject = "Obnovení hesla"
	sender = {
		"name":"Django",
		"email": os.getenv('BREVO_SENDER'),
	}

	if not os.getenv('BREVO_SENDER'):
		logger.error("BREVO_SENDER environment variable is not set")
		return

	html_content = f'''<html><body>
	<h1>Pro obnovení hesla klikněte na link níže</h1>
	<br /><br />
	<a href="{reset_url}">Obnovit heslo</a>
	</body></html>'''

	to = [{"email": user_email, "name": username}]
	send_smtp_email = sib_api_v3_sdk.SendSmtpEmail(to=to, bcc=None, cc=None, headers=None, html_content=html_content, sender=sender, subject=subject)

	try:
		api_response = api_instance.send_transac_email(send_smtp_email)
		logger.info(f"Password reset email sent successfully to {user_email}")
		return True
	except ApiException as e:
		logger.error(f"Failed to send password reset email to {user_email}: {str(e)}")
		return False

