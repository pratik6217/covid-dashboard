def login():

	st.title("Login")
	st.subheader("Please enter your details:")

	u_name = st.beta_columns(2)
	username = u_name[0].text_input("Username:")

	passs = st.beta_columns(2)
	password = passs[0].text_input("Password:",type = 'password')

	submit = st.beta_columns(2)
	choice = submit[0].button("Login")
	
	if choice:
		db_user = cursor.find_one({'username': username})
		if db_user == None:
			st.error('This user does not exists. Please register first !!')
		else:
			if f.decrypt(db_user['password']).decode() != password:
				st.error("Please enter the correct password !!")
			else:
				st.success("Logged in successfully.")