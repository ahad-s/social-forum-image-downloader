import Tkinter
import urllib2
import base64
import ImageTk
from PIL import Image
import cStringIO
from cStringIO import StringIO


class Test():

	def __init__(self):
		self.url = "https://1.t.4cdn.org/sci/1421353731414s.jpg"

	def gui(self):
		self.root = Tkinter.Tk()

		self.root.geometry('500x500+100+100')

		self.bot_frame = Tkinter.Frame()

		self.bot_frame.pack()

		self.show_thumbnail(self.url)

		Tkinter.mainloop()

	def show_thumbnail(self, thumbnailurl):
		a = urllib2.urlopen(thumbnailurl).read()
		encoded = cStringIO.StringIO(base64.b64decode(a))
		self.current_thumbnail = encoded

		t = Image.open(self.current_thumbnail)

		# test = open("testing.gif", "wb")
		# test.write(base64.decodestring(self.current_thumbnail))
		# test.close()

		# thumbnail = ImageTk.PhotoImage(data=self.current_thumbnail)
		# self.image_thumbnail = Tkinter.Label(self.bot_frame, image = thumbnail)
		# self.image_thumbnail.pack(side="left")

# i = Image.open("s_test.jpg")
# i.show()

a = Test()
a.gui()