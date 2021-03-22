
class home:
	def home(self):
		st.title("COVID - 19")
		st.subheader('''Welcome to our COVID - 19 Tracker app 🚑''')
		st.write('Coronavirus is officially a pandemic. Since the first case in december the disease has spread fast reaching almost every corner of the world.'+
         'They said it\'s not a severe disease but the number of people that needs hospital care is growing as fast as the new cases.'+
         'Some governments are taking measures to prevent a sanitary collapse to be able to take care of all these people.'+
         'I\'m tackling this challenge here. Let\'s see how some countries/regions are doing!')

		st.write()
		self.summary_url = "https://api.covid19api.com/summary"
		self.summary_response = requests.get(self.summary_url).json()
		
		self.s_new_confirmed = self.summary_response['Global']['NewConfirmed']
		self.s_total_confirmed = self.summary_response['Global']['TotalConfirmed']
		
		self.s_new_deaths = self.summary_response['Global']['NewDeaths']
		self.s_total_deaths = self.summary_response['Global']['TotalDeaths']

		self.s_new_recovered = self.summary_response['Global']['NewRecovered']
		self.s_total_recovered = self.summary_response['Global']['TotalRecovered']


		# Creating a Dictionary to convert it into a Dataframe to visualize it using plotly pie chart.
		# self.index = ['NewConfirmed','TotalConfirmed', 'NewDeaths', 'TotalDeaths', 'NewRecovered', 'TotalRecovered' ]
		self.d = { 'Labels' : ['NewConfirmed','TotalConfirmed', 'NewDeaths', 'TotalDeaths', 'NewRecovered', 'TotalRecovered' ], 
		 			'Values' : [ self.summary_response['Global']['NewConfirmed'],
		 						self.summary_response['Global']['TotalConfirmed'],
				 				self.summary_response['Global']['NewDeaths'],
				 				self.summary_response['Global']['TotalDeaths'],
				 				self.summary_response['Global']['NewRecovered'],
				 				self.summary_response['Global']['TotalRecovered'] ]
		}

		# Creating DataFrame from a Dictionary.
		self.df = pd.DataFrame(self.d, index= [0,1,2,3,4,5])

		# Menu for Home Section.
		self.menu2 = ['Summary', 'COVID NEWS']
		self.option2 = st.selectbox('options', self.menu2)

		if self.option2 == 'Summary':
			self.pie_fig = px.pie(self.df, values= self.d['Values'] , names= self.d['Labels'], title= 'Summary of Covid - 19 Cases.') 
			st.write(self.pie_fig)
		elif self.option2 == 'COVID NEWS':

			# Reading the apiKey from the file.
			with open('gnews_apiKey', 'r') as self.file:
				self.apiKey = self.file.read()

			# Gnews api supported languages and their codes.
			self.language = {
				'Arabic': 'ar',
				'German': 'de',
				'Greek': 'el',
				'English': 'en',
				'Spanish': 'es',
				'French': 'fr',
				'Hebrew': 'he',
				'Hindi': 'hi',
				'Italian': 'it',
				'Japanese': 'ja',
				'Malayalam': 'ml',
				'Marathi': 'mr',
				'Dutch': 'nl',
				'Norwegian': 'no',
				'Portuguese': 'pt',
				'Romanian': 'ro',
				'Russian': 'ru',
				'Swedish': 'sv',
				'Tamil': 'ta',
				'Telugu': 'te',
				'Ukrainian': 'uk',
				'Chinese': 'zh'
			}
			
			# Gnews supported Countries and their codes.
			self.country = {
				'Australia': 'au',
				'Brazil': 'br',
				'Canada':'ca',
				'Switzerland':'ch',
				'China': 'cn',
				'Germany': 'de',
				'Egypt': 'eg',
				'Spain': 'es',
				'France': 'fr',
				'United Kingdom': 'gb',
				'Greece': 'gr',
				'Hong Kong': 'hk',
				'Ireland': 'ie',
				'Israel': 'il',
				'India': 'in',
				'Italy': 'it',
				'Japan': 'jp',
				'Netherlands': 'nl',
				'Norway': 'no',
				'Peru': 'pe',
				'Philippines': 'ph',
				'Pakistan': 'pk',
				'Portugal': 'pt',
				'Romania': 'ro',
				'Russian Federation': 'ru',
				'Sweden	': 'se',
				'Singapore': 'sg',
				'Taiwan, Province of China': 'tw',
				'Ukraine': 'ua',
				'United States': 'us'
				}

			# Setting the search to COVID 19 to always get news about COVID 19.
			self.search = 'COVID 19'
			st.write()

			# Country Select for the news
			self.selected_country = st.selectbox('Country:', list(self.country.keys()))
			# Language Select for the news.
			self.selected_language = st.selectbox('Language:', list(self.language.keys()))
			self.submit = st.button('submit')

			# Validating the submit button.
			if self.submit:
				# Validating the data entries.
				if self.selected_country and self.search:
					# Gnews Api URL.
					self.url = 'https://gnews.io/api/v4/search?q={search}&token={apiKey}&lang={lang}&country={country}'.format(search= self.search, apiKey= self.apiKey, lang= self.language[self.selected_language],country= self.country[self.selected_country])
					# Storing the response of the api in json format in response variable.
					self.response = requests.get(self.url).json()
					st.write('Total items found = ', self.response['totalArticles'])
					# Validating the number of articles.
					if self.response and self.response['totalArticles'] > 0:
						# Iteraing through the articles key of the response dictionary.
						for self.news in self.response['articles']:
							try:
								# Creating an image variable and storing the retrieved image in bytes form.
								self.img = Image.open(BytesIO(requests.get(self.news['image']).content))
								st.subheader('Title : {title}'.format(title= self.news['title']))
								st.subheader('Author : {author}'.format(author= self.news['source']['name']))
								# img = requests.get(news['image'])
								# Displaying the Image.
								st.image(self.img)
								st.write('Description : ', self.news['description'])
								st.write('Content : ', self.news['content'])
								st.write("Article Url : ", self.news['url'])
								# st.write("Image_url : ", news['image'])
								st.write("Published At : ", self.news['publishedAt'])
								st.write()
							except Exception as e:
								continue

					elif self.response['totalArticles'] == 0:
						st.info("No News Found !!")
				else:
					st.warning("Please select or enter the values !!")