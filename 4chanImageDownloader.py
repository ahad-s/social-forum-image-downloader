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

"""
TODO:
INCLUDE COPY FROM CLIPBOARD UPON FOCUS IN WINDOW
"""

class ChanDownload():

	def __init__(self, dl_dir):
		self.dl_dir = dl_dir
		self.bg_colour = "white"
		self.current_thumbnail = ""

	def newtkinter(self):

		self.main_win=Tkinter.Tk()
		self.main_win.title("4chan Image Downloader")
		self.main_win.resizable(width=0, height=0)
		self.main_win.configure(bg=self.bg_colour)
		# self.main_win.iconbitmap("image_downloader_icon.ico") ######## FIND A GOOD ICON FOR PROGRAM

		self.top_frame = Tkinter.Frame()
		self.mid_frame = Tkinter.Frame()
		self.mid_ish_frame = Tkinter.Frame()
		self.bot_frame = Tkinter.Frame()


		self.prompt_label = Tkinter.Label(self.top_frame, text="Enter 4chan url: ", 
										relief = "raised", bg = self.bg_colour)

		url_entry_width = 150 - self.prompt_label.winfo_reqwidth()
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

		self.folder_button = Tkinter.Button(self.bot_frame, text="Open Folder", command=self.open_dl_folder)



		#REPLACE .PACK WITH .GRID TO PUT THUMBNAIL/PREVIEW ON THE LEFT SIDE OF BUTTONS
		#THIS WORKS, JUST HAVE TO UPDATE IMAGES WITH self.image_thumbnail.config in the method


		self.download_button.config(width=30,height=2, bg = "yellow")
		self.download_button.pack(side="top")

		self.clear_button.config(width=30,height=2, bg = "cyan")
		self.clear_button.pack()

		self.folder_button.config(width=30, height=2, bg = "yellow")
		self.folder_button.pack(side="bottom")

		self.top_frame.pack(fill="x")
		self.mid_frame.pack(fill="x")
		self.mid_ish_frame.pack()
		self.bot_frame.pack()

		Tkinter.mainloop()

	# TEST FEATURE FOR NOW, USE FOR SOMETHING ELSE LATER
	def folder_hover_callback(self, on = False):
		print "Hovered at {}".format(time.localtime()[3:6]) # selects hour/minute/second


	def get_thumbnails(self):
		soup = self.get_soup()

		thumbnail_url_list = []

		for a in soup.find_all("a","fileThumb"):
			regex = 'src="(.+?)"'
			p = re.compile(regex)
			results = re.findall(p, str(a.contents))
			thumbnail_url_list.append(results[0][2:])

		return thumbnail_url_list



	def clear_entry(self):
		self.url_entry.delete(0, Tkinter.END)

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
		html = urllib2.urlopen(url[0])
		soup = BeautifulSoup(html)

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

	def make_dir(self):
		# make directory if it doesnt exist
		url = self.get_url()

		folder_name = self.get_foldername()

		if not (os.path.isdir(self.dl_dir+str(url[2])+"/"+folder_name)):
			os.makedirs(self.dl_dir+str(url[2])+"/"+folder_name)


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

	def download(self):

		self.download_status.set("Beginning download...")
		
		imgurl_list = self.get_images()

		url = self.get_url()

		thumbnail_urls = self.get_thumbnails()

		folder_name = self.get_foldername()

		self.make_dir()

		#goes through every photo in list and downloads it
		for imgurl, thumbnailurl in zip(imgurl_list, thumbnail_urls):
			try:
				# self.show_thumbnail("http://{0}".format(thumbnailurl)) ## DISABLED TEMPORARILY WHILE FIXING IMAGE DISPLAY

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

		finished=True # exclude this later on

		if finished:
			self.download_status.set("Finished!")
		print "Downloading finished!"

	def open_dl_folder(self):
		print self.dl_dir+"\\"+self.thread_url.split("/")[-4]+"\\"+self.get_foldername()
		os.system("explorer "+self.dl_dir+self.thread_url.split("/")[-4]+"\\"+self.get_foldername())


if __name__=="__main__":
	download_dir = "c:\\4chan\\downloads\\"
	chd=ChanDownload(download_dir).newtkinter()
