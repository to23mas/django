import os
import sib_api_v3_sdk
from sib_api_v3_sdk.rest import ApiException

def send_registration_email(username: str, user_email: str, verify_url: str):
	configuration = sib_api_v3_sdk.Configuration()
	configuration.api_key['api-key'] = os.getenv('BREVO_KEY')

	api_instance = sib_api_v3_sdk.TransactionalEmailsApi(sib_api_v3_sdk.ApiClient(configuration))
	subject = "Potvrzení registrace"
	sender = {
		"name":"Django",
		"email": os.getenv('BREVO_SENDER'),
	}

	html_content = f'''<html><body>
	<h1>Pro dokončení registrace je potřeba kliknout na link níže</h1>
	<br /><br />
	<a href="{verify_url}">Potvrdit registraci</a>
	</body></html>'''

	to = [{"email": user_email, "name": username}]
	send_smtp_email = sib_api_v3_sdk.SendSmtpEmail(to=to, bcc=None, cc=None, headers=None, html_content=html_content, sender=sender, subject=subject)

	try:
		api_response = api_instance.send_transac_email(send_smtp_email)
		print(api_response)
	except ApiException as e:
		print("Exception when calling SMTPApi->send_transac_email: %s\n" % e)

