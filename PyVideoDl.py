#!/usr/bin python3
# -*- coding: utf-8 -*-
#
# PyVideo-dl : Python script for downloading youtube videos
# 
# Copyright 2016 Chiheb Nexus
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#  
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
# MA 02110-1301, USA.
#########################################################################

from urllib.request import urlopen
from urllib.parse import parse_qs
from os import getlogin, path 

__version__ = 0.2
__author__ = "Chiheb Nexus"

class PyVideoDl:
	"""
	TODO: [ ] Add download speed
		  [ ] Add download path
		  [ ] Fix Youtube copyrighted video download 
		  [ ] FIX list_formats
		  [ ] Improve methods!
	"""
	def __init__(self):

		url = input("Enter your video URL: ")
		try:
			new_url = self.format_url(url)
			print("\t[+] Searching for video informations ...")
			title, quality, v_type, direct_url = self.return_informations(new_url)
			print("\t[+] Printing video informations")
			final_video_url, final_v_type = self.format_quality_and_type(title, quality, v_type, direct_url)
			final_extension = self.return_extension(final_v_type)
			final_title = title + final_extension
			print("\t[+] Start downloading ...\n")
			self.download_video(final_video_url, final_title)
		except Exception:
			self.exit_app()

	def exit_app(self):
		"""
		Exit app by exit(0)
		"""
		print("\tThere is a problem when loading video informations!\n\
\tCheck your link. Or,Maybe your video is protected by Youtube Copyright or maybe\n\
\tyou have a problem with your internet connection.\n\
\tWe will fix this SH*T in the next version.\n\
\tCurrent version is: {0}\n\
\tAuthor: {1}\n\
\tProgram wil be closed ...".format(__version__, __author__))
		import sys
		sys.exit(0)

	def format_url(self, url):
		"""
		Return new form of URL 
		"""
		new_url = url.split("v=")

		return "https://www.youtube.com/get_video_info?video_id={0}".format(new_url[-1:][0])

	def convert_length(self, length):
		"""
		Return video length in MB
		"""
		return "{0:5.2f}MB".format(float(length)/ 1000000)

	def return_extension(self, v_type):
		"""
		Return the good extension for the file 
		"""
		list_formats = ["webm", "mp4", "flv", "3gp"]
		i = 0
		right_format_found = False 

		for right_format in list_formats:

			if right_format in v_type:
				right_format_found = True

				return "."+right_format
				break

		if not right_format_found:
			print("Didn't found the right_format! Program will shutdown!\n")
			self.exit_app()

	def format_quality_and_type(self, title, quality, v_type, direct_url):
		"""
		Manage qualities and types then return choice
		"""
		print("\n\tVideo title: \x1B[32;10m{0}\x1B[0m".format(title))

		for i in range(len(quality)):
			response = urlopen(direct_url[i])

			length = 0
			try:
				length = int(response.info()["Content-length"])
			except Exception:
				print("Can't get video length!\nExit application!\n")
				self.exit_app()

			print("\n\t>--\x1B[33;10m[{0}]\x1B[0m\n\tQuality: \x1B[37;10m{1}\x1B[0m\n\tVideo type: \x1B[37;10m{2}\x1B[0m\n\
\tLength: \x1B[37;10m{3}\x1B[0m\n\t--<"
				.format(i+1, quality[i], v_type[i], self.convert_length(length)))

		while True:
			try:
				final_format = int(input("\tPlease choose your format number: "))
				if ((final_format >= 1) and (final_format <= len(quality))):

					return direct_url[final_format-1], v_type[final_format-1]
					break;
				else:
					print("\tOut of range! Please choose again\n")
			except ValueError:
				print("\tPlease choose a valid format number!\n")

	def return_informations(self, new_url):
		"""
		Return: 
			- Video title
			- Video file name
			- Video qualities
			- Video type
			- Direct URL 
		"""
		try:
			response = urlopen(new_url)
			data = response.read()
			info = parse_qs(str(data))
			title = info['title'][0]
			stream_map = info['url_encoded_fmt_stream_map'][0]
			v_info = stream_map.split(",")
			quality, v_type, direct_url = [], [], []
		except Exception:
			self.exit_app()

		for video in v_info:
			item = parse_qs(video)
			quality.append(item['quality'][0])
			v_type.append(item['type'][0])
			direct_url.append(item['url'][0])

		return title, quality, v_type, direct_url

	def download_video(self, direct_url, fname):
		"""
		Using direct_url and fname
		"""
		response = urlopen(direct_url)
		length = int(response.info()["Content-length"])
		path_file = "/home/"+getlogin()

		with open(path.join(path_file, fname), "wb+") as my_file:

			done = 0
			# FIXME: Buffer size
			buffer_size = 1024
			buff = response.read(buffer_size)
			while buff:
				my_file.write(buff)
				done += buffer_size
				per = r'{0:3.2f}%'.format(done * 100/length)
				percent = "["+per+"]"
				conv_length = self.convert_length(length)
				print("\r\t\x1B[33;10mDownloading:\x1B[0m \x1B[32;10m{0}\x1B[0m\t{1} of{2}"
					.format(fname, percent, conv_length), end = "")
				buff = response.read(buffer_size)
				
				
		my_file.close()
		print("\n")

##### Test ######

if __name__ == '__main__':
	myapp = PyVideoDl()


