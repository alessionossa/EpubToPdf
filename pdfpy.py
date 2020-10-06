import pdfkit
import os
from PyPDF2 import PdfFileMerger
from PyPDF2.utils import PdfReadError
from bs4 import BeautifulSoup as bs


class PdfEngine(object):

	"""
		This class carries operations on pdf files.

		It has the following methods:

		convert() --- Which converts each of the markup file
		passed in to pdf. Markup file should be html

		combine() --- Which merges all of the pdf files created by
		the convert method, creating a new file.

		del_pdf() --- Which deletes all the pdf files created by
		the convert method.

	"""

	#def __init__(self, markup_files, style_files, pdf_files, directory):
	def __init__(self, markup_files, pdf_files, directory):
		self.markup_files = markup_files
		#self.style_files = style_files
		self.pdf_files = pdf_files
		self.directory = directory

	def convert(self):
		
		with open(self.markup_files[1]) as fp:
			first_html = bs(fp, 'html.parser')
		
		viewport_str = first_html.find("meta", {"name":"viewport"})['content']
		viewport_str_arr = viewport_str.split(',')
		viewport = {}
		for view_str in viewport_str_arr:
			name, val = view_str.split('=')
			viewport[name.strip()]= val.strip()

		print(viewport)

		for each in self.markup_files:

			# Prevent conversion process from showing terminal updates

			"""
			options = {
				'quiet': None,
				'margin-bottom': '0',
				'margin-left': '0',
				'margin-right': '0',
				'margin-top': '0'
			}
			"""
			# 641/96*25,4 = 169.5979166667mm
			options = {
				'quiet': None,
				'viewport-size': viewport['width']+'x'+viewport['height'],
				'page-width': str(int(viewport['width'])+2)+'px',
				'page-height': str(int(viewport['height'])+2)+'px',
				'margin-bottom': '0',
				'margin-left': '0',
				'margin-right': '0',
				'margin-top': '0',
				'disable-smart-shrinking': None
			}

			#print(options)

			pdfkit.from_file(each, "{}.pdf".format(self.markup_files.index(each)),
							 options=options)

		print('--- Sections converted to pdf')

	def combine(self):

		merger = PdfFileMerger()

		for pdf in self.pdf_files:
			try:
				merger.append(pdf, import_bookmarks=False)
			except PdfReadError:
				pass

		merger.write("{}.pdf".format(self.directory))

		print('--- Sections combined together in a single pdf file')

		merger.close()

	def del_pdf(self):
			for each in self.pdf_files:
				os.remove(each)
			print('--- Individual pdf files deleted from directory')
