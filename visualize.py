	
class visualise:
	def visualize(self):
		st.title('Visualization of Covid - 19.')
		st.subheader('Here you can easily view all the current cases, deaths and recoveries in nicely plotted graphs and carry out your analysis.')
		st.write()
		self.menu1 = ['Scatter Geo Plot', 'Graph']
		self.option1 = st.selectbox('Options', self.menu1)

		# Initializing an empty list to store the name of all the countries.
		self.countries = {'None' : None}
		# self.countries_slug = []
		# Url to get all the names of the countries from the api.
		self.countries_url = "https://api.covid19api.com/countries"
		self.countries_response = requests.get(self.countries_url).json()
		# Looping through the response and storing the names of the countries in a list.
		for self.country in self.countries_response:
			self.countries[self.country['Country']] = self.country['Slug']
		

		if self.option1 == 'Scatter Geo Plot':
			st.title("Scatter Geo Plot")
			st.subheader('Here you can see the number of cases in each country marked on the map.')
			st.write()
			self.selected_country = st.selectbox('Countries: ', list(self.countries.keys()))
			self.selected_status = st.selectbox('Options', ['confirmed', 'deaths', 'recovered'])
			self.submit = st.button('submit')

			if self.submit:
				# self.df = pd.DataFrame({})
				# print(self.key)
				try:
					# GET Status By Country name.
					self.By_country = f"https://api.covid19api.com/country/{self.countries[self.selected_country]}/status/{self.selected_status}"
					self.by_country_df = pd.read_json(self.By_country)
				except Exception as e:
					st.error(e)
					# print(self.by_country_df)
				self.scatter_geo_fig = px.scatter_geo(self.by_country_df, lat = self.by_country_df['Lat'],
															lon = self.by_country_df['Lon'],
															# locations= self.by_country_df['Country'],
															hover_name= self.by_country_df['Country'],
															size= self.by_country_df['Cases'],
															color= self.by_country_df['Country'])
				st.write(self.scatter_geo_fig)

		# Graph Visualization.
		elif self.option1 == 'Graph':
			st.title("Graph")
			st.subheader('Here you can see the number of cases in each country marked on the Graph.')
			st.write()
			# Countries Selection i.e Single or Compare.
			self.selected_country = st.selectbox('Country1: ', list(self.countries.keys()))
			self.compare_country = st.selectbox('Country2:', list(self.countries.keys()))
			self.selected_status = st.selectbox('Options', ['confirmed', 'deaths', 'recovered'])
			
			self.submit = st.button('submit')
			self.graph_figure = go.Figure()
			# If country1:
			if self.submit and self.selected_country != 'None':
				try:
					# Url of the Api
					self.graph_url1 = f"https://api.covid19api.com/country/{self.countries[self.selected_country]}/status/{self.selected_status}"
					self.graph_response1 = requests.get(self.graph_url1).json()
					# Initializing empty lists for the x and y values of the Graphs for Country1.
					self.x1 = []
					self.y1 = []
					# Iterating on the response to get the date and nimber of cases.
					for data1 in self.graph_response1:
						self.x1.append(data1['Date'])
						self.y1.append(data1['Cases'])
					self.graph_figure.add_trace(go.Scatter(x= self.x1,
																y= self.y1))
				except Exception as e:
					st.error(e)

			#If Country2:
			if self.submit and self.compare_country != 'None':
				try:
					# Url of the Api.
					self.graph_url2 = f"https://api.covid19api.com/country/{self.countries[self.compare_country]}/status/{self.selected_status}"
					self.graph_response2 = requests.get(self.graph_url2).json()
					# Initializing empty lists for the x and y values of the Graphs for Country 2.
					self.x2 = []
					self.y2 = []
					# Iterating on the response to get the date and nimber of cases.
					for data2 in self.graph_response2:
						self.x2.append(data2['Date'])
						self.y2.append(data2['Cases'])
					self.graph_figure.add_trace(go.Scatter(x= self.x2,
																y= self.y2))
				except Exception as e:
					st.error(e)

			if self.submit:
				self.graph_figure.update_layout(
	    			title = 'Covid 19 Cases' + ' in ' + self.selected_country,
	    			xaxis_tickformat = '%d %B (%a)<br>%Y'
				)
				st.write(self.graph_figure)