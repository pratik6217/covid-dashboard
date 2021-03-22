import smtplib, ssl


def send_mail(mail):
	context = ssl.create_default_context()
	port = 465
	email = "passvault6217@gmail.com"
	with open("password.key", "r") as file:
		password = f.decrypt(file.read().encode()).decode()
	
	message = """\
Subject: Registration Succesfull.

This message is to inform you that you have successfully registered with our services.

Thankyou for choosing us :)"""
	receiver = mail
	try:
		server = smtplib.SMTP_SSL("smtp.gmail.com", port, context = context)
		server.ehlo()
   		#server.starttls(context = context)
		
		server.login(email, password)
		server.ehlo()

		server.sendmail(email, receiver, message)
	except Exception as e:
		st.error(e)
	finally:
		server.quit()