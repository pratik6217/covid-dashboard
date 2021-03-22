import streamlit as st

def register():
# Page Title
	st.title("Register")
	st.subheader("Please enter your details:")

#Creating Containers for First and last names.
	first_name, last_name = st.beta_columns(2)
	name = first_name.text_input("First Name:")
	surname = last_name.text_input("Last Name:")

	e = st.beta_columns(1)
	email = e[0].text_input("Email:")

	u, ph = st.beta_columns(2)
	username = u.text_input("Username:")
	phone = ph.text_input("Phone:")
  

	p1, p2 = st.beta_columns(2)
	password1 = p1.text_input("Password:", type = 'password')
	password2 = p2.text_input("Re-enter Password:", type = 'password')

	space = st.beta_columns(3)
	agree = space[0].checkbox("I agree")
	submit = space[2].button("submit")

	if submit:
		if agree:
			if password1 == password2:
				exists = cursor.find_one({'username': username})
				if exists:
					st.error("This username already exists !!")
				else:
					db_insert = cursor.insert_one({
					'name': name + ' ' + surname,
					'username': username,
					'password': f.encrypt(password1.encode()),
					'email': email,
					'phone': int(phone),
					})

					if db_insert:
						try:
							send_mail(email)
						except Exception as e:
							st.error(e)

						st.success("Succesfully Registered.")
					else:
						st.error('Something went wrong !!')

			else:
				st.error("The two passwords did not match !!")
		else:
			st.warning("Please select the 'agree' checkbox !!")
