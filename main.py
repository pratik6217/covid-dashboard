# Importing the important libraries and their Modules.

import streamlit as st 
import requests
import plotly.express as px
import pandas as pd
from cryptography.fernet import Fernet
from PIL import Image
from io import BytesIO
import time
import plotly.graph_objects as go
import threading
import pymongo
import SessionState
import smtplib, ssl
import threading
import datetime
from plotly.subplots import make_subplots
from streamlit.report_thread import add_report_ctx
import random
import base64
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
import joblib
import fbprophet
from fbprophet import Prophet

# Creating a Class for Users.
class account:
	def __init__(self, username):
		self.username = username

# Writitin the code for Home Function.
	def home(self):
		st.title("COVID - 19")
		st.subheader('''Welcome to our COVID - 19 Tracker app 🚑''')
		st.write('Coronavirus is officially a pandemic. Since the first case in december the disease has spread fast reaching almost every corner of the world.'+
         'They said it\'s not a severe disease but the number of people that needs hospital care is growing as fast as the new cases.'+
         'Some governments are taking measures to prevent a sanitary collapse to be able to take care of all these people.'+
         'I\'m tackling this challenge here. Let\'s see how some countries/regions are doing!')
		try:
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
			self.d = { 'Labels' : ['New Confirmed','Total Confirmed', 'New Deaths', 'Total Deaths', 'New Recovered', 'Total Recovered' ], 
			 			'Values' : [ self.summary_response['Global']['NewConfirmed'],
			 						self.summary_response['Global']['TotalConfirmed'],
					 				self.summary_response['Global']['NewDeaths'],
					 				self.summary_response['Global']['TotalDeaths'],
					 				self.summary_response['Global']['NewRecovered'],
					 				self.summary_response['Global']['TotalRecovered'] ]
			}

			# Creating DataFrame from a Dictionary.
			self.df = pd.DataFrame(self.d, index= [0,1,2,3,4,5])

			self.d1 = { 'Labels' : ['New Confirmed', 'New Deaths', 'New Recovered' ], 
			 			'Values' : [ self.summary_response['Global']['NewConfirmed'],
					 				self.summary_response['Global']['NewDeaths'],
					 				self.summary_response['Global']['NewRecovered'] ]
			}
			
			
			# Creating DataFrame from a Dictionary.
			self.df = pd.DataFrame(self.d, index= [0,1,2,3,4,5])
			self.df1 = pd.DataFrame(self.d1, index = [0,1,2])
			# Menu for Home Section.
			self.menu2 = ['Summary', 'COVID NEWS']
			self.option2 = st.selectbox('options', self.menu2)
		except:
			st.error('OOPS Something went wrong :( ')
		
		
		if self.option2 == 'Summary':
			#st.write(self.df.style.background_gradient(cmap = 'Reds'))
			try:
				self.pie_fig = px.pie(self.df, values= self.d['Values'] , names= self.d['Labels'], title= 'Summary of Covid - 19 Cases.') 
				st.write(self.pie_fig)
				st.write()
				st.subheader('Histogram:')
				self.histogram_fig = px.histogram(self.df1, x= self.df1['Labels'], y= self.df1['Values'])
				st.write(self.histogram_fig)
			except:
				st.error('OOPS Something went wrong :( ')
			
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

	
	def visualize(self):
		st.title('Visualization of Covid - 19.')
		st.subheader('Here you can easily view all the current cases, deaths and recoveries in nicely plotted graphs and carry out your    analysis.')
		st.write(' ')
		st.write(' ')
		self.menu1 = ['Scatter Geo Plot', 'Graph', 'Histogram', 'Master Figure']
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
			self.choice = st.selectbox('Options', ['World-Wide', 'Countries'])

			if self.choice == 'Countries':
				self.selected_country = st.selectbox('Countries: ', list(self.countries.keys()))
				
				self.submit = True

				if self.submit:
					# self.df = pd.DataFrame({})
					# print(self.key)
					try:
						# GET Status By Country name.
						self.By_country = f"https://api.covid19api.com/live/country/{self.countries[self.selected_country]}"
						self.by_country_df = pd.read_json(self.By_country)
					except Exception as e:
						st.error(e)
						# print(self.by_country_df)
					try:
						'''self.scatter_geo_fig = px.scatter_geo(self.by_country_df, lat = self.by_country_df['Lat'],
																	lon = self.by_country_df['Lon'],
																	# locations= self.by_country_df['Country'],
																	hover_name= self.by_country_df['Province'],
																	size = self.by_country_df['Active'],
																	# size= self.by_country_df['Confirmed'] - self.by_country_df['Deaths'] - self.by_country_df['Recovered'],
																	color= self.by_country_df['Province'])'''
																	
						#st.write(self.scatter_geo_fig)
						self.map_styles_list = ['carto-positron', 'open-street-map', 'satellite-streets', 'carto-darkmatter', 'stamen-terrain', 'stamen-toner', 'stamen-watercolor']
						self.style = st.selectbox('Map Styles', self.map_styles_list)
						if self.style == 'carto-positron':
							self.mode = st.radio("Select Mode:",
							['Light', 'Dark'])
							if self.mode == 'Dark':
								self.style  = 'dark'
							else:
								self.style = 'carto-positron'
						px.set_mapbox_access_token('pk.eyJ1IjoicHJhdGlrMjYwOSIsImEiOiJja255OWlqbzAxZXRyMm5xbjZ6aTZsNzVsIn0.GidtdkmE4nCW_UaCLtnqaw')
						self.fig = px.scatter_mapbox(self.by_country_df, lat="Lat", lon="Lon",color_discrete_sequence=["Red"], size="Active",
							hover_name = 'Province', hover_data = ['Active'], zoom = 3, height = 300)
						self.fig.update_layout(margin= {"r": 0, "t": 0, "l": 0, "b": 0})
						self.fig.update_layout(mapbox_style = self.style)
						st.write(self.fig)
					except:
						st.error('OOPS Something went wrong :( ')

					
			elif self.choice == 'World-Wide':
				lat1 = []
				lon1 = []
				daily_status = []
				overall_status = []
				active = []
				pop = []
				countries = []
				self.url1 = 'https://corona.lmao.ninja/v2/countries'
				self.response1 = requests.get(self.url1).json()
				for country in self.response1:
					countries.append(country['country'])
					lat1.append(country['countryInfo']['lat'])
					lon1.append(country['countryInfo']['long'])
					daily_status.append( f"Today Cases: {country['todayCases']}, Today Deaths: {country['todayDeaths']}, Today Recovered: {country['todayRecovered']}")
					overall_status.append(f"Cases: {country['cases']}, Deaths: {country['deaths']}, Recovered: {country['recovered']}")
					active.append(country['active'])
					pop.append(country['population'])

				self.df1 = pd.DataFrame({'Country' : countries,
									'Latitude' : lat1,
									'Longitude' : lon1,
									'Daily_Status' : daily_status,
									'Overall_Status' : overall_status,
									'Active' : active,
									'Population' : pop})
				try:
					'''self.figure = px.scatter_geo(self.df1,
											lat = 'Latitude',
											lon = 'Longitude',
											size = 'Active',
											hover_name = self.df1['Country'],
											color = 'Country' )

					st.write(self.figure)'''
					self.map_styles_list = ['carto-positron', 'open-street-map', 'satellite-streets', 'carto-darkmatter', 'stamen-terrain', 'stamen-toner', 'stamen-watercolor']
					self.style = st.selectbox('Map Styles', self.map_styles_list)
					if self.style == 'carto-positron':
						self.mode = st.radio("Select Mode:",
							['Light', 'Dark'])
						if self.mode == 'Dark':
							self.style  = 'dark'
						else:
							self.style = 'carto-positron'
					px.set_mapbox_access_token('pk.eyJ1IjoicHJhdGlrMjYwOSIsImEiOiJja255OWlqbzAxZXRyMm5xbjZ6aTZsNzVsIn0.GidtdkmE4nCW_UaCLtnqaw')
					self.fig = px.scatter_mapbox(self.df1, lat="Latitude", lon="Longitude",color_discrete_sequence=["Red"], hover_name = 'Country',
                  hover_data = ['Active'], zoom = 1, height = 300)
					self.fig.update_layout(mapbox_style = self.style)
					self.fig.update_layout(margin= {"r": 0, "t": 0, "l": 0, "b": 0})
					st.write(self.fig)
				except:
					st.error('OOPS Something went wrong :( ')

		# Graph Visualization.
		elif self.option1 == 'Graph':
			st.title("Graph")
			st.subheader('Here you can see the number of cases in each country marked on the Graph.')
			st.write()
			# Countries Selection i.e Single or Compare.
			menu = ['Scatter Plots', 'Compare Countries']
			self.choice = st.selectbox('Menu:', menu)
			if self.choice == 'Scatter Plots':
				try:
					self.selected_country = st.selectbox('Country: ', list(self.countries.keys()))
						
					if self.selected_country != 'None':
						self.url = f"https://api.covid19api.com/live/country/{self.countries[self.selected_country]}"
						self.df = pd.read_json(self.url)
						self.df = self.df.groupby('Date').sum()
						self.df = self.df.reset_index()

						s = st.beta_columns(4)
						self.c = s[0].checkbox('Confirmed')
						self.d = s[1].checkbox('Deaths')
						self.r = s[2].checkbox('Recovered')
						#self.c = s[0].checkbox('Confirmed')

						figure = go.Figure()
						#figure.add_trace(go.Scatter(x = self.df['Date'], y = self.df['Active']))
						if self.c:
							figure.add_trace(go.Scatter(x = self.df['Date'], y = self.df['Confirmed'], name = 'Confirmed'))
						if self.d:
							figure.add_trace(go.Scatter(x = self.df['Date'], y = self.df['Deaths'], name ='Deaths'))
						if self.r:
							figure.add_trace(go.Scatter(x = self.df['Date'], y = self.df['Recovered'], name = 'Recovered'))
						st.write(figure)
				except:
					st.warning('Please select a Country !!')


			elif self.choice == 'Compare Countries':
				self.selected_country = st.selectbox('Country1: ', list(self.countries.keys()))
				self.compare_country = st.selectbox('Country2:', list(self.countries.keys()))
				self.selected_status = st.selectbox('Options', ['confirmed', 'deaths', 'recovered'])
				
				x = datetime.datetime.now()
				self.date = ''
				for i in str(x):
					if i == ' ':
						self.date += 'T'
					elif i == '.':
						break
					else:
						self.date += i
				self.date += 'Z'
				print(self.date)
				self.submit = st.button('submit')
				self.graph_figure = go.Figure()
				# If country1:
				if self.submit and self.selected_country != 'None':
					try:
						# Url of the Api
						self.graph_url1 = f"https://api.covid19api.com/country/{self.selected_country}/status/{self.selected_status}?from=2020-03-01T00:00:00Z&to{self.date}"
						self.graph_response1 = requests.get(self.graph_url1).json()
						print(self.graph_response1)
						# Initializing empty lists for the x and y values of the Graphs for Country1.
						self.x1 = []
						self.y1 = []
						# Iterating on the response to get the date and nimber of cases.
						for data1 in self.graph_response1:
							self.x1.append(data1['Date'])
							self.y1.append(data1['Cases'])
						self.y1 = list(map(int, self.y1))
						print(self.y1)
						self.graph_figure.add_trace(go.Scatter(x= self.x1,
																	y= self.y1, name= self.selected_country))
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
																	y= self.y2, name= self.compare_country))
					except Exception as e:
						st.error(e)

				if self.submit:
					self.graph_figure.update_layout(
						legend_title = 'Countries',
			    		title = 'Covid 19 Cases',
			    		xaxis_tickformat = '%d %B (%a)<br>%Y'
					)
					st.write(self.graph_figure)

		elif self.option1 == 'Histogram':
			st.title("Histogram")
			st.subheader('Here you can see the number of cases in each country depicted on the histogram.')
			st.write()
			# Countries Selection 
			self.selected_country = st.selectbox('Country: ', list(self.countries.keys()))
			
			if self.selected_country != 'None':
				self.url = f"https://api.covid19api.com/live/country/{self.countries[self.selected_country]}"
				self.response = pd.read_json(self.url)
				self.response['Date'] = pd.to_datetime(self.response['Date']).astype(str)
				
				x = str(datetime.datetime.now()).split(' ')[0] + ' ' + '00:00:00+00:00'
				self.response = self.response[self.response['Date'] == x]
				#st.write(self.response['Date'])
				#st.write(self.response.head())
				self.choice = st.selectbox('Options', ['Full Country', 'States'])
				if self.choice == 'States':
					self.figure = px.histogram(self.response,
										x= self.response['Province'],
										y= self.response['Active'])
					st.write(self.figure)

				elif self.choice == 'Full Country':
					d = {
					'Labels' : ['Confirmed', 'Deaths', 'Recovered'],
					'Cases' : [self.response['Confirmed'].sum(), self.response['Deaths'].sum(), self.response['Recovered'].sum() ]
					}
					self.df = pd.DataFrame(d, index = [0,1,2])
					try:
						self.figure = px.histogram(self.df,
													x = self.df['Labels'],
													y = self.df['Cases']
												)
							
						st.write(self.figure)
					except:
						st.error('OOPS Something went wrong :( ')
						
			else:
				st.warning('Please select a Country !!')

				# elif self.choice == 'By Dates':
				# 	# st.write(self.df.groupby(['Date']).sum())

				# 	self.figure = px.histogram(#self.response,
				# 		x = self.response['Date'],
				# 		y = self.response['Active'],
				# 		color = self.response['Province'] )
				# 	st.write(self.figure)

		
		elif self.option1 == 'Master Figure':
			st.title('Master Plots')
			st.subheader('Here You can find all the graphs grouped together at a single place.')
			st.write()
			self.selected_country = st.selectbox('Country: ', list(self.countries.keys()))
			

			if self.selected_country != 'None':
				self.url = f"https://api.covid19api.com/live/country/{self.countries[self.selected_country]}"
				self.response = pd.read_json(self.url)
				# st.write(self.response.head())

				self.choice = st.selectbox('Menu', ['Master - Scatter', 'Master - Bar', 'Master - Line'])

				if self.choice == 'Master - Scatter':
					try:
						self.response = self.response.groupby('Date').sum()
						self.response.reset_index(inplace = True)
						self.figure = make_subplots(rows= 2, cols= 2)
						self.figure.add_trace(go.Scatter(x= self.response['Date'], y= self.response['Active'], name= "Active"),row=1, col = 1)
						self.figure.add_trace(go.Scatter(x= self.response['Date'], y= self.response['Confirmed'], name = 'Confirmed'),row=1, col = 2)
						self.figure.add_trace(go.Scatter(x= self.response['Date'], y= self.response['Deaths'], name = 'Deaths'),row=2, col = 1)
						self.figure.add_trace(go.Scatter(x= self.response['Date'], y= self.response['Recovered'], name = 'Recovered'),row=2, col = 2)
						st.write(self.figure)
					except:
						st.error('OOPS Something went wrong :( ')

				elif self.choice == 'Master - Bar':
					try:
						self.response = self.response.groupby('Date').sum()
						self.response.reset_index(inplace = True)
						self.figure = make_subplots(rows= 2, cols= 2)
						self.figure.add_trace(go.Bar(x= self.response['Date'], y= self.response['Active'], name= "Active"),row=1, col = 1)
						self.figure.add_trace(go.Bar(x= self.response['Date'], y= self.response['Confirmed'], name = 'Confirmed'),row=1, col = 2)
						self.figure.add_trace(go.Bar(x= self.response['Date'], y= self.response['Deaths'], name = 'Deaths'),row=2, col = 1)
						self.figure.add_trace(go.Bar(x= self.response['Date'], y= self.response['Recovered'], name = 'Recovered'),row=2, col = 2)
						st.write(self.figure)
					except:
						st.error('OOPS Something went wrong :( ')

				elif self.choice == 'Master - Line':
					try:
						self.figure1 = px.line(self.response, x="Date", y="Active", facet_col="Province", facet_col_wrap=2,
				          facet_row_spacing=0.02, # default is 0.07 when facet_col_wrap is used
				          facet_col_spacing=0.08, # default is 0.03
				          height=5000, width= 800,
				          title= f"Covid Cases in {self.selected_country}")
						# fig.for_each_annotation(lambda a: a.update(text=a.text.split("=")[-1]))
						self.figure1.update_yaxes(showticklabels=True)
						st.write(self.figure1)
					except:
						st.error('OOPS Something went wrong :( ')
						
			else:
				st.warning('Please select a Country !!')

	
	def vaccination(self):
		self.client = pymongo.MongoClient('mongodb+srv://admin:admin@password-manager.bl1uj.mongodb.net/myFirstDatabase?retryWrites=true&w=majority')
		self.db = self.client['Vaccination']
		self.pointer = self.db['registration']

		st.title('Welcome to the Vaccination Center.')
		menu = ['Vaccination Details', 'Register']
		self.choice = st.selectbox('Menu:', menu)
		if self.choice == 'Vaccination Details':
			df = pd.read_csv('http://api.covid19india.org/csv/latest/cowin_vaccine_data_statewise.csv')
			st.write('India')
			df2 = df[df['State'] == 'India']
			
			self.figure = make_subplots(rows= 3, cols= 2)
			self.figure.add_trace(go.Scatter(x= df2['Updated On'], y= df2['Total Individuals Registered'], name= "Total Individuals Registered"),row=1, col = 1)
			self.figure.add_trace(go.Scatter(x= df2['Updated On'], y= df2['Total Individuals Vaccinated'], name = 'Total Individuals Vaccinated'),row=1, col = 2)
			self.figure.add_trace(go.Scatter(x= df2['Updated On'], y= df2['Total Covaxin Administered'], name = 'Total Covaxin Administered'),row=3, col = 1)
			self.figure.add_trace(go.Scatter(x= df2['Updated On'], y= df2['Total CoviShield Administered'], name = 'Total CoviShield Administered'),row=3, col = 2)
			st.write(self.figure)
			
			self.states = list(df['State'].unique())
			self.states.remove('India')
			self.state = st.selectbox('State:', self.states)
			state_df = df[df['State'] == self.state]
			
			self.figure1 = make_subplots(rows= 3, cols= 2)
			self.figure1.add_trace(go.Scatter(x= state_df['Updated On'], y= state_df['Total Individuals Registered'], name= "Total Individuals Registered"),row=1, col = 1)
			self.figure1.add_trace(go.Scatter(x= state_df['Updated On'], y= state_df['Total Individuals Vaccinated'], name = 'Total Individuals Vaccinated'),row=1, col = 2)
			self.figure1.add_trace(go.Scatter(x= state_df['Updated On'], y= state_df['Total Covaxin Administered'], name = 'Total Covaxin Administered'),row=3, col = 1)
			self.figure1.add_trace(go.Scatter(x= state_df['Updated On'], y= state_df['Total CoviShield Administered'], name = 'Total CoviShield Administered'),row=3, col = 2)
			st.write(self.figure1)
			
			
		elif self.choice == 'Register':
			st.subheader('Please Fill in this form inorder to register for the vaccination:')
			st.write()
			try:
				# uname = st.beta_columns(2)
				# self.u_name = uname[0].text_input('Please enter your username')

				f_Name, s_Name = st.beta_columns(2)
				self.name = f_Name.text_input('Please enter Your first name:')
				self.surname = s_Name.text_input("PLease enter your Last name:")

				e, p = st.beta_columns(2)
				self.email = e.text_input("Please enter your email:")
				self.phone = p.text_input('Please enter your Phone Number:')

				aadhar, age = st.beta_columns(2)
				self.aadhar_number = aadhar.text_input('Please enter your Aadhar Number:')
				self.Age = age.text_input('Please enter your age:')

				try:
					self.uploaded_file = st.file_uploader('Please upload an image of your aadhar card ( png, jpg, jpeg with Max Size - 250 Kb):', type = ['png', 'jpg', 'jpeg'])
					if self.uploaded_file is not None:
						st.info('Please check your uploaded Image:')
						st.write()
						self.uploaded_image = Image.open(self.uploaded_file)
						st.image(self.uploaded_image)
					# if self.uploaded_file is not None:
					# 	self.file_details = {
					# 					'Name' : self.uploaded_file.name,
					# 					'type' : self.uploaded_file.type,
					# 					'size' : self.uploaded_file.size

					# 	} 
					# 	st.write(self.file_details)
				except Exception as e:
					st.error(e)


				add = st.beta_columns(1)
				self.address = add[0].text_area("Please enter your Address:")

				dis = st.beta_columns(1)
				self.diseases = dis[0].text_area('Please enter all the diseases or allergies you have (Please type NA if None):')


				submit = st.button('submit')
				if submit:
					# if self.u_name == '':
					# 	st.error('Username cannot be blank !!')
					if self.name == '':
						st.error('Name cannot be blank !!')
					elif self.email == '':
						st.error('Email field cannot be blank !!')
					elif self.Age == '':
						st.error('Age cannot be blank !!')
					elif self.aadhar_number == '':
						st.error('Aadhar Number cannot be blank !!')
					elif self.phone == '' or len(self.phone) < 10 or len(self.phone) > 10:
						st.error('Enter a valid Phone Number !!')
					elif self.address == '':
						st.error('Address cannot be blank !!')
					elif self.diseases == '':
						st.error("Please enter NA if you don't have any disease !!")
					else:
						records = self.pointer.find_one({
							'Email' : self.email
							})
						if self.uploaded_file.size > 256000:
							st.error('Please upload the image of size < 250 Kb !!')
						elif records:
							st.error('You have already registered you cannot register again !!')
						else:
							if 'png' in str(self.uploaded_file.type):
								self.img_format = 'png'
							elif 'jpg' in str(self.uploaded_file.type):
								self.img_format = 'jpg'
							elif 'jpeg' in str(self.uploaded_file.type):
								self.img_format = 'jpeg'

							self.img_in_bytes = BytesIO()
							self.uploaded_image.save(self.img_in_bytes, format= self.img_format)

							data = {
								'Name' : self.name + ' ' + self.surname,
								'Email' : self.email,
								'Phone' : self.phone,
								'Age' : self.Age,
								'Aadhar Number' : self.aadhar_number,
								'Image' : self.img_in_bytes.getvalue(),
								'Address' : self.address,
								'Diseases' : self.diseases
							}

							try:
								self.inserted = self.pointer.insert_one(data)
								st.success('You have successfully registered for the vaccination.')
							except Exception as e:
								st.error(e)

							
							# st.write(self.img_in_bytes.getvalue())
							# self.retrieved_img = Image.open(BytesIO(self.img_in_bytes.getvalue()))
							# st.image(self.retrieved_img)

			except Exception as e:
				st.error(e)

	def analysis(self):
		st.title('Welcome to the Ananlysis Center.')
		st.subheader('Here you can view the future number of Estimated cases:')
		st.write(' ')
		menu = ['Confirmed', 'Recovered', 'Deaths']
		self.choice = st.selectbox('Menu:', menu)
		df = pd.read_csv('https://api.covid19india.org/csv/latest/case_time_series.csv')
		data = df
		if self.choice == 'Confirmed':
			data['ds'] = df['Date_YMD']
			data['y'] = df['Total Confirmed']
			data = data.drop(['Date', 'Date_YMD', 'Daily Confirmed', 'Total Confirmed', 'Daily Recovered', 'Total Recovered', 'Daily Deceased', 'Total Deceased'], axis = 1)
			data['ds'] = pd.to_datetime(data['ds'])
			prop = Prophet()
			prop.fit(data)
			#prop = joblib.load('./model.joblib')
		
		elif self.choice == 'Recovered':
			data['ds'] = df['Date_YMD']
			data['y'] = df['Total Recovered']
			data = data.drop(['Date', 'Date_YMD', 'Daily Confirmed', 'Total Confirmed', 'Daily Recovered', 'Total Recovered', 'Daily Deceased', 'Total Deceased'], axis = 1)
			data['ds'] = pd.to_datetime(data['ds'])
			prop = Prophet()
			prop.fit(data)
		
		elif self.choice == 'Deaths':
			data['ds'] = df['Date_YMD']
			data['y'] = df['Total Deceased']
			data = data.drop(['Date', 'Date_YMD', 'Daily Confirmed', 'Total Confirmed', 'Daily Recovered', 'Total Recovered', 'Daily Deceased', 'Total Deceased'], axis = 1)
			data['ds'] = pd.to_datetime(data['ds'])
			prop = Prophet()
			prop.fit(data)
			
		self.period = st.number_input('Please enter the time duration(in days) for predicting the number of cases: ')
		predict = st.button('Predict')
		if predict:
			future = prop.make_future_dataframe(periods = int(self.period))
			future_forecast = prop.predict(future)
			forecast = future_forecast.tail(int(self.period))
			
			#st.write(forecast)
			st.write(fbprophet.plot.plot_plotly(prop, future_forecast, xlabel='Date', ylabel = 'Confirmed'))
		
		

	def help_center(self):
		st.title('Help Centre.')
		st.write()
		self.choice = st.selectbox('Menu', ['General GuideLines', 'Notifications and Helplines'])
		if self.choice == 'General GuideLines':
			st.write("Here's a small gif which displays 7 steps to avoid Coronavirus.")
			gif_runner = st.image('./COVID_WHO.gif')
			st.write()
			st.subheader('More Prevention Measures and helpline number can be found Here:')
			st.write('WHO : ','https://www.who.int/health-topics/coronavirus#tab=tab_2')
			st.write('Indian Helpline Numbers : ','https://www.mohfw.gov.in/pdf/coronvavirushelplinenumber.pdf')

		elif self.choice == 'Notifications and Helplines':
			self.notifications_url = ' https://api.rootnet.in/covid19-in/notifications'
			self.helpline_url = 'https://api.rootnet.in/covid19-in/contacts'

			self.notifications_response = requests.get(self.notifications_url).json()
			self.helpline_response = requests.get(self.helpline_url).json()

			self.title = []
			self.links = {}
			self.helplines = {}
			self.states = []

			for data in self.helpline_response['data']['contacts']['regional']:
				self.states.append(data['loc'])
				self.helplines[data['loc']] = data['number']

			for data in self.notifications_response['data']['notifications']:
				self.title.append(data['title'])
				self.links[data['title']] = data['link']

			st.title('Welcome to the Notifications & Helpline center.')
			st.subheader('Here you can find all the released notifications for Covid so far.')
			st.write(' ')
			st.write(f"Number: {self.helpline_response['data']['contacts']['primary']['number']}")
			st.write(f"Number-Toll-Free: {self.helpline_response['data']['contacts']['primary']['number-tollfree']}")
			st.write(f"Email: {self.helpline_response['data']['contacts']['primary']['email']}")
			st.write(f"Twitter: {self.helpline_response['data']['contacts']['primary']['twitter']}")
			st.write(f"Facebook: {self.helpline_response['data']['contacts']['primary']['facebook']}")


			self.selected_notification = st.selectbox('Notifications:', self.title)
			st.write(self.links[self.selected_notification])
			st.write(' ')
			self.selected_state = st.selectbox('States:', self.states)
			st.write(self.helplines[self.selected_state])

	def raw(self):
		st.title('Data Center')
		st.write(' ')
		self.option = st.selectbox('Menu', ['Statewise History of India', 'Testing Data', 'Compare Data' ])
		if self.option == 'Statewise History of India':
			self.uri = 'https://api.covid19api.com/live/country/India'
			self.df = pd.read_json(self.uri)
			self.df['Date'] = pd.to_datetime(self.df['Date']).astype(str)
			#st.write(self.df['Date'])
			#self.url = 'https://api.rootnet.in/covid19-in/unofficial/covid19india.org/statewise/history'
			self.d = st.date_input('Enter a date:')
			states = []
			self.date = str(self.d) + ' 00:00:00+00:00'
			#st.write(self.date)
			self.df = self.df[self.df['Date'] == self.date]
			self.df = self.df.drop(['ID', 'Country', 'CountryCode', 'City', 'CityCode', 'Lat', 'Lon', 'Date'], axis = 1)
			self.df.reset_index(inplace = True) 
			#st.write(self.df)
			
			#self.response = requests.get(self.url).json()
			#for state in self.response['data']['history'][0]['statewise']:
			#	states.append(state['state'])
			
			st.write(f'Day: {self.d}')
			st.write(f' ⚫ Confirmed: {self.df.sum()["Confirmed"]}')
			st.write(f' ⚫ Recovered: {self.df.sum()["Recovered"]}')
			st.write(f' ⚫ Deaths: {self.df.sum()["Deaths"]}')
			st.write(f' ⚫ Active Number of cases: {self.df.sum()["Active"]}')
			
			states = list(self.df['Province'])
			self.selected_state = st.selectbox('States:', states)

			#details = {}
			#for data in self.response['data']['history']:
			#	details[data['day']] = {'states' : data['statewise'],'Total_data': [data['total']['confirmed'], data['total']['recovered'], data['total']['deaths'], data['total']['active']]}
			#st.write(self.d)
			self.d = str(self.d)
			if self.d:
				#st.write(' ')
				st.write(' ') 
				self.df = self.df[self.df['Province'] == self.selected_state]
				st.write(f'State: {self.selected_state}')
				st.write(f" ⚫ Confirmed: {int(self.df['Confirmed'])}")
				st.write(f" ⚫ Recovered: {int(self.df['Recovered'])}")
				st.write(f" ⚫ Deaths: {int(self.df['Deaths'])}")
				st.write(f" ⚫ Active Number of cases: {int(self.df['Active'])}")				

			else:
				st.info('Sorry, No data found for this day !!')

		elif self.option == 'Testing Data':
			df = pd.read_csv('http://api.covid19india.org/csv/latest/cowin_vaccine_data_statewise.csv')
			
			self.date = st.date_input('Please select a date:')
			#st.write(self.date.day)
			
			self.date = self.date.strftime('%d/%m/%Y')  
			df1 = df[df['Updated On'] == str(self.date)]
			#st.write(str(self.date))
			#st.write(type(self.date))
			st.write('India')
			
			#st.write(df1)
			df2 = df1[df1['State'] == 'India']
			#st.write(df2.columns)
			#st.write(px.scatter(df2, x ='Updated On', y = 'Total Individuals Vaccinated')) 
			try:
				st.write(f'Total Registrations: {int(df2["Total Individuals Registered"])}')
				st.write(f'Total Sessions Conducted: {int(df2["Total Sessions Conducted"])}')
				#st.write(f'Total Sites: {int(df2["Total Sites"])}')
				st.write(f'Total Covaxin Registered: {int(df2["Total Covaxin Administered"])}')
				st.write(f'Total Covishield Registered: {int(df2["Total CoviShield Administered"])}')
				st.write(f'Total Individuals Vaccinated: {int(df2["Total Individuals Vaccinated"])}')
				st.write(f'Total Doses Administered: {int(df2["Total Doses Administered"])}')
			except:
				st.info('Please select a proper date !!')
				
			self.states = list(df['State'].unique())
			self.states.remove('India')
			self.state = st.selectbox('State:', self.states)
			state_df = df[df['State'] == self.state]
			date_df = state_df[state_df['Updated On'] == self.date]
			try:
				st.write(f'Total Registrations: {int(date_df["Total Individuals Registered"])}')
				st.write(f'Total Sessions Conducted: {int(date_df["Total Sessions Conducted"])}')
				#st.write(f'Total Sites: {int(df2["Total Sites"])}')
				st.write(f'Total Covaxin Registered: {int(date_df["Total Covaxin Administered"])}')
				st.write(f'Total Covishield Registered: {int(date_df["Total CoviShield Administered"])}')
				st.write(f'Total Individuals Vaccinated: {int(date_df["Total Individuals Vaccinated"])}')
				st.write(f'Total Doses Administered: {int(date_df["Total Doses Administered"])}')
			except:
				st.info('Please select a proper date !!')
			

		elif self.option == 'Compare Data':
			self.country_url = 'https://corona.lmao.ninja/v2/countries'
			self.rp = requests.get(self.country_url).json()
			self.countries = []
			for country in self.rp:
				self.countries.append(country['country'])

			self.selected_country = st.selectbox("Choose a Country:", self.countries)
			self.selected_country1 = st.selectbox("Choose Another Country:", self.countries)
			self.flag1 = False
			self.flag2 = False

			self.url = f'https://corona.lmao.ninja/v2/countries/{self.selected_country}'
			self.url1 = f'https://corona.lmao.ninja/v2/countries/{self.selected_country1}'

			self.submit = st.button('submit')
			if self.submit:
				if self.selected_country:
					self.flag1 = True
				if self.selected_country1:
					self.flag2 = True

				self.name = st.beta_columns(2)
				self.img = st.beta_columns(2)
				# img[0].image(Image.open(BytesIO(requests.get(response['countryInfo']['flag']).content)))
				# img[1].image(Image.open(BytesIO(requests.get(response1['countryInfo']['flag']).content)))
				self.c = st.beta_columns(2)
				self.d = st.beta_columns(2)
				self.r = st.beta_columns(2)
				self.c1 = st.beta_columns(2)
				self.d1 = st.beta_columns(2)
				self.r1 = st.beta_columns(2)
				self.act = st.beta_columns(2)
				self.cs = st.beta_columns(2)
				self.test = st.beta_columns(2)
				self.pop = st.beta_columns(2)
				self.cont = st.beta_columns(2)

				if self.flag1:
					self.response = requests.get(self.url).json()
					self.name[0].write(f'Country : {self.response["country"]}')
					self.img[0].image(self.response['countryInfo']['flag'])
					st.write(self.response['countryInfo']['flag'])
					st.image(self.response['countryInfo']['flag'])
					self.c[0].write(f'Cases Today : {self.response["todayCases"]}')
					self.d[0].write(f'Deaths Today: {self.response["todayDeaths"]}')
					self.r[0].write(f'Recovered Today: {self.response["todayRecovered"]}')
					self.c1[0].write(f'Total Cases : {self.response["cases"]}')
					self.d1[0].write(f'Total Deaths : {self.response["deaths"]}')
					self.r1[0].write(f'Total Recovered : {self.response["recovered"]}')
					self.act[0].write(f'Active Number of Cases : {self.response["active"]}')
					self.cs[0].write(f'Critical Cases : {self.response["critical"]}')
					self.test[0].write(f'Number of Tests Done : {self.response["tests"]}')
					self.pop[0].write(f'Population of the Country : {self.response["population"]}')
					self.cont[0].write(f'Continent : {self.response["continent"]}')

				if self.flag2:
					self.response1 = requests.get(self.url1).json()
					self.name[1].write(f'Country : {self.response1["country"]}')
					self.img[1].image(self.response1['countryInfo']['flag'])
					self.c[1].write(f'Cases Today: {self.response1["todayCases"]}')
					self.d[1].write(f'Deaths Today: {self.response1["todayDeaths"]}')
					self.r[1].write(f'Recovered Today: {self.response1["todayRecovered"]}')
					self.c1[1].write(f'Total Cases : {self.response1["cases"]}')
					self.d1[1].write(f'Total Deaths : {self.response1["deaths"]}')
					self.r1[1].write(f'Total Recovered : {self.response1["recovered"]}')
					self.act[1].write(f'Active Number of Cases : {self.response1["active"]}')
					self.cs[1].write(f'Critical Cases : {self.response1["critical"]}')
					self.test[1].write(f'Number of Tests Done : {self.response1["tests"]}')
					self.pop[1].write(f'Population of the Country : {self.response1["population"]}')
					self.cont[1].write(f'Continent : {self.response1["continent"]}')




client = pymongo.MongoClient('mongodb+srv://admin:admin@password-manager.bl1uj.mongodb.net/myFirstDatabase?retryWrites=true&w=majority')
db = client['Covid-19']
cursor = db['Login']

session_state = SessionState.get(username= ' ', show= True, login= False, dash_board= False, dash_button= False)

# key = Fernet.generate_key()
# with open('key.key', 'wb') as file:
	# file.write(key)
with open('key.key', 'rb') as file:
	key = file.read()

f = Fernet(key)


def dashboard():
		obj = account(session_state.username)
		main_menu = ['Home', 'Raw Data', 'Visualize', 'Analysis', 'Vaccination', 'Help Center']
		main_option = st.sidebar.selectbox('Menu', main_menu)
		st.sidebar.write()
		Quotes = {
			'Mohamed El-Erian' : '“Hopefully, as companies give more attention to the importance of work-life balance, more and more people will be in a better position to decide and act more holistically on what’s important to them.” ',
			'Cali Williams Yost' : '“Telecommuting, one of many forms of work-life flexibility, should no longer be viewed as a nice-to-have, optional perk mostly used by working moms. These common stereotypes don’t match reality — allowing employees to work remotely is a core business strategy today… We need to de-parent, de-gender, and de-age the perception of the flexible worker.”',
			'Michael Dell' : '“Technology now allows people to connect anytime, anywhere, to anyone in the world, from almost any device. This is dramatically changing the way people work, facilitating 24/7 collaboration with colleagues who are dispersed across time zones, countries, and continents.”',
			'Socrates' : '"The secret of change is to focus all of your energy, not on fighting the old, but on building the new.”',
			'Kiran Mazumdar-Shaw' : '"Ultimately, the greatest lesson that COVID-19 can teach humanity is that we are all in this together."',
			'Steve Maraboli' : '“Life doesn’t get easier or more forgiving, we get stronger and more resilient.”',
			'Greg Kincaid' : '“No matter how much falls on us, we keep plowing ahead. That’s the only way to keep the roads clear.”',
			'Michelle Obama' : '"Women are working more, men are understanding their value as caregivers, women are primary breadwinners—I mean, we could go on and on and on. Things are different. So we can’t keep operating like everything is the same, and that’s what many of us have done. And I think it’s up to us to change the conversation."',
			'Arjun Agarwal' : '"Now is the time for us to look after the people who work for us. When a company steps up at a time like this, it builds loyalty, commitment, and long-lasting teams."',
			'Caryn Sullivan' : '“In the face of adversity, we have a choice. We can be bitter, or we can be better. Those words are my North Star.”',
		}
		
		gif_list = ['./attack_covid19.gif', './social_distance.gif', './sanitizer.gif', './wash_hands.gif', './wear_mask.gif']
		
		st.sidebar.write('Quotes:')
		authors = ['Mohamed El-Erian', 'Cali Williams Yost', 'Michael Dell', 'Socrates', 'Kiran Mazumdar-Shaw', 'Steve Maraboli' ]
		author = random.choice(authors)
		st.sidebar.write('Author : ', author)
		st.sidebar.write('Quote : ', Quotes[author])
		st.sidebar.image(random.choice(gif_list))

		if main_option == 'Home':
			obj.home()
		elif main_option == 'Visualize':
			obj.visualize()
		elif main_option == 'Vaccination':
			obj.vaccination()
		elif main_option == 'Analysis':
			obj.analysis()
		elif main_option == 'Help Center':
			obj.help_center()
		elif main_option == 'Raw Data':
			obj.raw()


@st.cache(allow_output_mutation=True)
def get_base64_of_bin_file(bin_file):
    with open(bin_file, 'rb') as file:
        data = file.read()
    return base64.b64encode(data).decode()

def set_png_as_page_bg(png_file):
    bin_str = get_base64_of_bin_file(png_file)
    page_bg_img = '''
    <style>
    body {
    background-image: url("data:image/png;base64,%s");
    background-size: cover;
    }
    </style>
    ''' % bin_str
    
    st.markdown(page_bg_img, unsafe_allow_html=True)
    return



def send_mail(mail):
	context = ssl.create_default_context()
	port = 465
	email = "Covid19app2609@gmail.com"
	with open("password.key", "r") as file:
		password = file.read()
	
	message = """\
Subject: Registration Succesfull.

This message is to inform you that you have successfully registered with our services.

Thankyou for choosing us :)

On our Platform you can explore everything that you need from news to charts to plots to future predictions all at the same place.

You can even register for the vaccine, so don't forget to visit the vaccination center.

Here is the webiste again in case you missed it:
https://covid--19-dashboard.herokuapp.com/





















Please do not reply to this mail. This a computer generated message !!"""
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

def login():
	st.title("Login")
	st.subheader("Please enter your details:")

	u_name = st.beta_columns(2)
	username = u_name[0].text_input("Username:")

	pass_ = st.beta_columns(2)
	password = pass_[0].text_input("Password:",type = 'password')

	submit = st.beta_columns(4)
	choice = submit[0].button("Login")
	guest_login = submit[1].button('Guest Login')
	
	if choice:
		db_user = cursor.find_one({'username': username})
		if db_user == None:
			st.error('This user does not exists. Please register first !!')
		else:
			if f.decrypt(db_user['password']).decode() != password:
				st.error("Please enter the correct password !!")
			else:
				st.success("Logged in successfully.")
				obj = account(session_state.username)
				session_state.username = username
				st.info(f'Your Dashboard is ready {session_state.username},')
				session_state.dash_button = True
				session_state.show = False
	elif guest_login:
		st.success("Logged in successfully.")
		obj = account(session_state.username)
		session_state.username = 'Guest'
		st.info(f'Your Dashboard is ready {session_state.username},')
		session_state.dash_button = True
		session_state.show = False


# st.title('Welcome to our Covid-19 Tracker App.')
PAGE_CONFIG = {'page_title' : 'Covid-19', 'page_icon': './download.jpeg','layout' : 'centered'}
st.set_page_config(**PAGE_CONFIG)

st.write()
menu = ['Login', 'Register']

if session_state.show:
	#page_bg_img = '''
	#	<style>
	#	body {
	# 	background-image: url("./covid.png");
	# 	background-repeat: no-repeat;
	# 	background-size: cover;
	# 	}
	# </style>'''
	#st.markdown(page_bg_img, unsafe_allow_html=True)
	#set_png_as_page_bg('./covid.png')
	st.title('Covid - 19 WebApp.')
	st.subheader('Welcome to our WebApp, Please login if you are an existing user or register yourself with our services.')
	choice = st.selectbox('Menu', menu)
	if choice == 'Login':
		login()
	elif choice == 'Register':
		register()

if session_state.login:
	# thread = threading.Thread(target= 'dashboard', args= None)
	# thread.start()
	# print(f'Number of Active Connections: {threading.activeCount()}')
	dashboard()

if session_state.dash_button:
	session_state.login = True
	st.button('Go to My Dashborad ->')
	session_state.dash_button = False




