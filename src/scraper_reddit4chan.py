import os
import urllib
import Tkinter
import urllib2
from bs4 import BeautifulSoup
import threading
import time
import re
import itertools
import base64
from PIL import ImageTk, Image

import cPickle
import requests
import requests.auth
import json

from kmeans import Comment, KMeansText


"""
~ INCLUDE COPY FROM CLIPBOARD UPON FOCUS IN WINDOW
"""

class ChanDownload(object):

	def __init__(self, dl_dir, reddit_crawler = None):
		self.dl_dir = dl_dir
		self.to_open = dl_dir
		self.bg_colour = "white"
		self.current_thumbnail = ""
		self.reddit_crawler = reddit_crawler

	# assigns GUI to be used throughout program
	def newtkinter(self):

		self.main_win=Tkinter.Tk()
		self.main_win.title("Reddit/Chan Image Downloader")
		self.main_win.resizable(width=0, height=0)
		self.main_win.configure(bg=self.bg_colour)
		# self.main_win.iconbitmap("image_downloader_icon.ico") ######## FIND A GOOD ICON FOR PROGRAM

		self.top_frame = Tkinter.Frame()
		self.mid_frame = Tkinter.Frame()
		self.mid_ish_frame = Tkinter.Frame()
		self.bot_frame = Tkinter.Frame()


		self.prompt_label = Tkinter.Label(self.top_frame, text="Enter (Reddit/4chan) url: ", 
										relief = "raised", bg = self.bg_colour)

		url_entry_width = 197 - self.prompt_label.winfo_reqwidth()
		self.url_entry = Tkinter.Entry(self.top_frame, width=url_entry_width)

		self.foldername_label = Tkinter.Label(self.mid_frame, text="Enter folder name:", # set it so that if you hover it makes a box saying "empty = (default dir)", draw a canvas
											relief = "raised", bg = self.bg_colour)

		folder_entry_width = 150 - self.foldername_label.winfo_reqwidth()
		self.foldername_entry = Tkinter.Entry(self.mid_frame, width=folder_entry_width+10)


		self.foldername_label.bind("<Enter>", lambda x: self.folder_hover_callback(True))
		self.foldername_label.bind("<Return>", lambda y: self.folder_hover_callback(False))


		self.prompt_label.pack(side='left')
		self.url_entry.pack(side='left')

		self.foldername_label.pack(side='left')
		self.foldername_entry.pack(side='left')


		self.download_status = Tkinter.StringVar()

		self.dl_status_label = Tkinter.Label(self.mid_ish_frame, textvariable=self.download_status, bg = self.bg_colour)

		self.dl_status_label.pack(side="left")



		self.clear_button = Tkinter.Button(self.bot_frame, text="Clear", command=self.clear_entry)

		self.download_button = Tkinter.Button(self.bot_frame, text="Begin Download", command=self.download_thread_start)

		self.folder_button = Tkinter.Button(self.bot_frame, text="Open Download Folder", command=self.open_dl_folder)

		self.reddit_random_button = Tkinter.Button(self.bot_frame, text="Download randomly with MACHINE LEARNING!", command=self.open_dl_folder)



		#REPLACE .PACK WITH .GRID TO PUT THUMBNAIL/PREVIEW ON THE LEFT SIDE OF BUTTONS
		#THIS WORKS, JUST HAVE TO UPDATE IMAGES WITH self.image_thumbnail.config in the method


		self.download_button.config(width=40,height=2, bg = "yellow")
		self.download_button.pack(side="top")

		self.clear_button.config(width=40,height=2, bg = "cyan")
		self.clear_button.pack()

		self.reddit_random_button.config(width=40, height=2, bg = "cyan")
		self.reddit_random_button.pack(side="bottom")

		self.folder_button.config(width=40, height=2, bg = "yellow")
		self.folder_button.pack(side="bottom")


		self.top_frame.pack(fill="x")
		self.mid_frame.pack(fill="x")
		self.mid_ish_frame.pack()
		self.bot_frame.pack()

		Tkinter.mainloop()

	# TEST FEATURE FOR NOW, USE FOR SOMETHING ELSE LATER
	def folder_hover_callback(self, on = False):
		# print "Hovered at {}".format(time.localtime()[3:6]) # selects hour/minute/second
		pass



	# retrieves the image URLs in a list to be parsed later and used
	def get_thumbnails(self):
		soup = self.get_soup()

		thumbnail_url_list = []

		for a in soup.find_all("a","fileThumb"):
			regex = 'src="(.+?)"'
			p = re.compile(regex)
			results = re.findall(p, str(a.contents))
			thumbnail_url_list.append(results[0][2:])

		return thumbnail_url_list



	# clears GUI for text
	def clear_entry(self):
		self.url_entry.delete(0, Tkinter.END)

	# parses raw URL that the user enters and returns as a list
	def get_url(self):
		self.thread_url=self.url_entry.get()

		getUrl = self.thread_url

		#GET THREAD ID + INITIALIZE URL

		url = []

		if "//" in getUrl:
			url.append(getUrl)
			url.append(getUrl.split("/")[5])
			url.append(getUrl.split("/")[3])
		else:
			url.append("http://"+getUrl)
			url.append(getUrl.split("/")[3])
			url.append(getUrl.split("/")[1])

		return url

	def get_soup(self):
		url = self.get_url()
		html = urllib2.urlopen(url[0]).read()
		soup = BeautifulSoup(html, "lxml")

		return soup

	def get_images(self):

		soup = self.get_soup()

		# add all image urls to a list
		imgurl=[]

		for b in soup.find_all("a","fileThumb"):
			imgurl.append(b['href'])
		return imgurl

	def get_foldername(self):
		url = self.get_url()
		folder_name = ""
		if (self.foldername_entry.get() == ""):
			folder_name = str(url[1])
		else:
			folder_name = str(self.foldername_entry.get())
		return folder_name


	# put foldername_entry as param in make_dir 
	# default foldername_entry to str(url[1])

	# makes a directory of the name specified, otherwise folder is thread ID
	def make_dir(self):
		# make directory if it doesnt exist
		url = self.get_url()

		folder_name = self.get_foldername()

		if not (os.path.isdir(self.dl_dir+str(url[2])+"/"+folder_name)):
			os.makedirs(self.dl_dir+str(url[2])+"/"+folder_name)


	# starts new thread so UI doesn't freeze as the user presses download
	def download_thread_start(self):
		downT = threading.Thread(target = self.download)
		downT.start()


	def show_thumbnail(self, thumbnailurl):
		a = urllib2.urlopen(thumbnailurl).read()
		encoded = base64.b64encode(a)
		self.current_thumbnail = encoded

		thumbnail = ImageTk.PhotoImage(data=self.current_thumbnail)
		self.image_thumbnail = Tkinter.Label(self.bot_frame, image = thumbnail)
		self.image_thumbnail.pack(side="left")

	# retrieves parsed thread URL and list of image URLs and downloads/saves it to computer
	def download(self):

		self.download_status.set("Beginning download...")
		
		self.make_dir()

		imgurl_list = self.get_images()

		url = self.get_url()

		self.to_open = self.dl_dir + url[2] + "\\" + url[1] + "\\"

		thumbnail_urls = self.get_thumbnails()

		folder_name = self.get_foldername()

		if "reddit.com/r/" in url:
			# print links from k-means
			return 


		print "opening...", self.to_open


		#goes through every photo in list and downloads it
		for imgurl, thumbnailurl in zip(imgurl_list, thumbnail_urls):
			try:
				# self.show_thumbnail("http://{0}".format(thumbnailurl))

				imgurl_name=(imgurl.split("/"))[4] #Isolates image file name

				if not (os.path.isfile(self.dl_dir+str(url[2])+"/"+folder_name+"/"+imgurl_name)):

					req = urllib2.Request("http:" + imgurl)
					f = urllib2.urlopen(req)

					self.download_status.set("Downloading {}...".format(imgurl_name))

					pic_file=open(self.dl_dir+str(url[2])+"/"+folder_name+"/"+imgurl_name,"wb")
					pic_file.write(f.read())
					pic_file.close()
				else:
					print "%s already exists." % imgurl_name

			except urllib2.HTTPError, e:
				pass
				# print "HTTP Error: " + e.code
				
			except urllib2.URLError, e:
				pass
				# print "URL Error: " + e.code

		self.download_status.set("Finished!")
		print "Downloading finished!"

	def open_dl_folder(self):
		os.system("explorer "+self.to_open)




class Reddit():
	def __init__(self):
		pass

	def get_archived_data(self):
		url = "http://www.redditarchive.com/?d="
		# urlformat = "www.redditarchive.com/?d=MONTH+DATE,+FULL_YEAR 
		months = ['january', 'february', 'march', 'april', 'may', 'june', 'july', 'august', 'september', 'october', 'november', 'december']
		dates = [str(i) for i in range(1, 32)]
		years = ['2016', '2015', '2014', '2013', '2012']

		months = ['may']

		archive_reddit_links = []

		num_days = 0

		for y in years:
			for m in months:
				for d in dates:
					print "archiving", m, d, y + "..."
					try:
						archive_page_html = urllib2.urlopen(url+m+"+"+d+",+"+y).read()
						archive_reddit_links.extend(self.get_all_reddit_links(archive_page_html))
						num_days += 1

						print "archieved day successfully with [%d] links..." % len(archive_reddit_links)
					except Exception as e:
						# print e.strerror
						print "archive day failed"
						# most likely too many requests
						x = open("last_archieve.txt", "wb")
						x.write(y + "--" + m + "--" + d)
						x.close()
						self.pickle_archived_data(archive_reddit_links, (m,d,y))
						return

		self.pickle_archived_data(archive_reddit_links, (m,d,y))

		# stores urldata, not the html file (i.e. it stores l = urllib2.urlopen(url))

	def pickle_archived_data(self, data_list, date):
		w = open('archived_reddit_urls/urls_' + date[0] + "_" + date[1] + "_" + date[2] + '_.txt', "wb")

		for l in data_list:
			# print "writing...", l
			l = l.encode("ascii", "ignore")
			w.write(l + "\n")

		w.close()


	def retrieve_archived_pickled_urls(self, date):
		r = open('archived_reddit_urls/urls_' + date[0] + "_" + date[1] + "_" + date[2] + '_.txt', "rb")
		lines = r.readlines()

		links_list = [l for l in lines]

		r.close()

		return links_list

	# returns list of all reddit links on page
	def get_all_reddit_links(self, html):
		links = []
		soup = BeautifulSoup(html, "lxml")
		for s in soup.find_all("a", target="_new"):
			url = s['href']
			if "reddit.com/r/" in url:
				links.append(url)
		return list(set(links)) # trivial way of uniqifying links


	def get_access_token(self, url = "http://www.reddit.com/" ):

		# retrieve from reddit dev page
		client_id = ""
		secret = ""
		user_agent = ""
		user = ""
		pw = ""

		client_auth = requests.auth.HTTPBasicAuth(client_id, secret)
		post_data = {"grant_type": "password", 
					"username": user, 
					"password": pw}
		header = {"User-Agent": user_agent}

		j = requests.post(url + "api/v1/access_token", 
							auth = client_auth, data = post_data, headers = header).json()
		# gives {access_token: token, expires_in:time, scope:?, token_type:('bearer')}

		print j

		access_token = j['access_token']
		token_type = j['token_type']
		expires_in = j['expires_in']

		return (access_token, token_type, user_agent)

	def get_comments(self, url, token, token_type, user_agent):

		comment_list = [] # list of Comment objects

		header = {"Authorization": token_type + " " + access_token, 
				"User-Agent": user_agent}
		resp = requests.get("https://oauth.reddit.com/api/v1/me", headers=header)

		# print "------------"

		resp = requests.get(temp, headers=header)
		l = resp.json()
		d = l[1]
		for k, v in d.items():
			if k == 'body':
				comment_list.append(Comment(v)) 

		# x = open("commentsjson.txt", "wb+")
		# x.write(str(l))
		# x.close()

		return comment_list

	def run_crawler(self):
		links = self.retrieve_archived_pickled_urls()
		tokens = self.get_access_token()

		master_comment_list = []

		for link in links:
			time.sleep(1) # in place to avoid making too many api calls
			print "retrieving comments for [%s]" % link
			comments = get_comments(link, tokens)
			master_comment_list.extend(comments)

		# uncomment this line to save comments to file as a list
		# self.pickle_dump_comments(master_comment_list)

		return master_comment_list # list of comments, i.e. list of strings	


	def pickle_dump_comments(self, comments):
		cPickle.dump(comments, open('comments_dump.p', 'wb+'))

	def pickle_retrieve_comments(self):
		master_comment_list = cPickle.load(open('comments_dump.p', 'rb+'))
		return master_comment_list # strings



if __name__=="__main__":
	# download_dir = "" # this can be changed, TODO: allow user to set this manually/change default
	# chd=ChanDownload(download_dir).newtkinter()

	test_url = 'https://oauth.reddit.com/r/redditdev/comments/2ysj31/how_do_i_request_the_frontpage_from_the_reddit_api/'

	reddit = Reddit()
	# reddit.get_fresh_comments()
	# reddit.get_archived_data()
	tokens = reddit.get_access_token()
	all_comments = reddit.run_crawler()
