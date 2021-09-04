from selenium import webdriver
import time
import re
import csv

options = webdriver.ChromeOptions()
options.add_argument('--ignore-certificate-errors')
options.add_argument('--ignore-ssl-errors')


driver=webdriver.Chrome(r'C:\Users\dgarb\OneDrive\Documents\Data Science Bootcamp April\Python\lecture notes\Selenium\chromedriver_win32\chromedriver.exe')

#driver=webdriver.Chrome(r'C:\Users\dgarb\OneDrive\Documents\Data Science Bootcamp April\Python\lecture notes\Selenium\chromedriver_win32\chromedriver.exe',chrome_options=options)

#get number of pages from first page

first_page =r'https://www.petfinder.com/search/cats-for-adoption/us/ny/new-york-city/?attribute%5B0%5D=Special+needs&distance=25&include_transportable=0'
driver.get(first_page)
time.sleep(2)

#find number of pages

page_info = driver.find_element_by_xpath('//*[@id="page-select_List_Box_Btn"]/div/div[1]').text
print('page_info: ',page_info)
pages = re.findall('[0-9]+',page_info)
print('pages ',pages)

#find start and end page

start_page = int(pages[0])
end_page = int(pages[1])
print('start_page: ',start_page,'*****','end_page: ',end_page)

#create list of page urls

page_urls = []

# the start url is the first_page
for num in range(start_page,end_page +1):
	url = first_page + '&page=' + str(num)
	page_urls.append(url)

#print('page_urls')
#create empty list to collect failed_urls
failed_urls= []

for index, page_url in enumerate(page_urls):

	csv_file = open('petfinder_specneeds_all.csv','w',encoding= 'utf-8',newline='')
	writer=csv.writer(csv_file)

	try:
		driver.get(page_url)
	except:
		continue
	time.sleep(2)

	print('*'*50)
	print("Page= ",index + 1)
	print('-'*50)

	#to get a list of the urls for each cat on the page

	try:

		animals = driver.find_element_by_xpath('//div[@class="animalSearchBody"]')
		cats = animals.find_elements_by_xpath('.//pfdc-pet-card')

		CatsList=[]
		for cat in cats:
			catbox = cat.find_element_by_xpath('.//a[@class="petCard-link"]').get_attribute('href')
			CatsList.append(catbox)

		for cat_url in CatsList:
			try:
				driver.get(cat_url)

				#Sleep
				time.sleep(2)
				cat_dict = {}
				
				#cat name
				cat_name = driver.find_element_by_xpath('//span[@data-test="Pet_Name"]').text
				cat_dict['cat_name'] = cat_name
				
				#Image and Video Section
				image_list = driver.find_elements_by_xpath('//div[@class="petCarousel-nav"]//button')

				images=[]
				videos=[]
				for image in image_list:
					image.get_attribute('aria-label')


					if 'video' in image.get_attribute('aria-label'):
						image_type = 'video'
						videos.append(image.get_attribute('aria-label'))
					else:
						images.append(image.get_attribute('aria-label'))
				num_images = len(images)
				num_videos = len(videos)
				cat_dict['num_images'] = num_images
				cat_dict['num_videos'] = num_videos


				#Kitty Demographics Section
				
				try:
					age = driver.find_element_by_xpath('//span[@data-test="Pet_Age"]').text
				except:
					None
				cat_dict['age'] = age
				
				try:
					breed = driver.find_element_by_xpath('//span[@data-test="Pet_Breeds"]').text
				except:
					breed = None
					
				cat_dict['breed'] = breed
				try:
					color = driver.find_element_by_xpath('//span[@data-test="Pet_Primary_Color"]').text
				except:
					color = None
				cat_dict['color'] = color

				try:
					size = driver.find_element_by_xpath('//span[@data-test="Pet_Full_Grown_Size"]').text
				except:
					size = None
				cat_dict['size'] = size

				try:
					sex = driver.find_element_by_xpath('//span[@data-test="Pet_Sex"]').text
				except:
					sex = None
				cat_dict['sex'] = sex


				#About section of page: results in a dictionary

				#About labels
				about_labels_objects = driver.find_elements_by_xpath('//div[@data-test="Pet_About_Section"]//dt')
				about_labels = [element.text.lower() for element in about_labels_objects]
				#print('cat_name = ',cat_name, '***', 'about_labels = ',about_labels)

				#About content
				about_content_objects = driver.find_elements_by_xpath('//div[@data-test="Pet_About_Section"]//dd')
				about_content = [element.text for element in about_content_objects]

				#About dictionary
				about_tuples = list(zip(about_labels,about_content))
				
				cat_dict['characteristics'] = None
				cat_dict['coat_length'] = None
				cat_dict['house-trained'] = None
				cat_dict['health']= None
				cat_dict['good in a home with'] = None
				cat_dict['adoption fee'] = None
				cat_dict['prefers a home without'] = None
					  
				for k,v in about_tuples:
					cat_dict[k] = v
				
				#Pet Story Section
				try:
					pet_story_section = driver.find_element_by_xpath('//div[@class="card-section"][@data-test="Pet_Story_Section"]').text
					story_list = pet_story_section.split('\n')
					pet_story_num_words = sum( [len(list_) for list_ in [list_.split(' ') for list_ in story_list] ])

				except:
					pet_story_num_words = None
				

				
				
				
				cat_dict['pet_story_num_words'] = pet_story_num_words

				#Rescue Group

				try:
					rescue_group = driver.find_element_by_xpath('//span[@itemprop="name"]').text
				except:
					rescue_group = None
				
				cat_dict['rescue_group'] = rescue_group
				
				#indicating things unique to this file
				cat_dict['days_on_petfinder'] = 'All'
				cat_dict['special_needs'] = 'Yes'
				
				print(cat_dict)
				
				writer.writerow(cat_dict.values())
			except:
				continue
	except:
		continue


			
			










