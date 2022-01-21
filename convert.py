from fpdf import FPDF
import sys
import argparse

class ChordSheet:
	def __init__(self):
		self.title = ""
		self.artist = ""
		self.album = ""
		self.key = ""
		self.scan = []
		self.chords = {}
		self.lyrics = {}

	def print_data(self):
		print('Title:', self.title)
		print('Artist', self.artist)
		print('Album:', self.album)
		print('Key:', self.key)
		print('Scan:', self.scan)
		print('Chords:', self.chords)
		print('Lyrics:', self.lyrics)

def main():
	# get command line arguments

	parser = argparse.ArgumentParser(prog="convert.py", 
		description="Convert TXT Chord Sheets to PDFs")
	parser.add_argument('filepath', type=str, nargs=1, 
		help="path to chordsheet txt file")
	parser.add_argument('-w', dest='width', type=float, default=3.5, 
		help="specify column width (3.5 inch by default)")
	parser.add_argument('--fsize', dest='font_size', type=float, default=9,
		help="lyric font size (default 9 pt font)")
	parser.add_argument('--l-margin', dest='left_margin', type=float, default=0.15,
		help="set left and right margin (default 0.15 in)")
	parser.add_argument('--top-margin', dest='top_margin', type=float, default=0.25,
		help="set top and bottom margin (default 0.25 in)")
	parser.add_argument('--no-cols', dest='no_cols', action='store_const',
						const=True, default=False,
		help="add flag for no columns")

	args = parser.parse_args()

	col_width = args.width # in
	col_space = 0.5 # in

	# begin generating pdf from txt

	pdf = FPDF(unit='in')

	pdf.set_margins(left=args.left_margin, top=args.top_margin)
	pdf.add_page()

	pdf.set_font("Courier", size=12)

	song = ChordSheet()

	with open(args.filepath[0], 'r') as txtfile:
		cur_part = ''
		for line in txtfile.readlines():
			if not line:
				continue
			try:
				[key, val] = line.split(':')
				if key == 'chord' and cur_part:
					song.chords[cur_part].append(val.rstrip())
				elif key == 'lyric' and cur_part:
					song.lyrics[cur_part].append(val.rstrip())
				elif key == 'part':
					cur_part = val.strip('[] \n')
					song.chords[cur_part] = []
					song.lyrics[cur_part] = []
				elif key == 'title':
					song.title = val.strip()
				elif key == 'artist':
					song.artist = val.strip()
				elif key == 'album':
					song.album = val.strip()
				elif key == 'key':
					song.key = val.strip()
				elif key == 'scan':
					song.scan = [v.strip() for v in val.split(',')]
				else:
					print("Error! Malformed Data!")
			except:
				pass

	# check for malformed data
	if not song.scan:
		print("Error! No scan detected!")
		return

	print("File Processed, Generating PDF...")
	# song.print_data()

	if song.title:
		pdf.set_font("Courier", 'B', size=16)
		pdf.cell(0, 0.25, txt=song.title, ln=1)
	if song.artist:
		pdf.set_font("Courier", size=14)
		pdf.cell(0, 0.2, txt=f"Artist: {song.artist}", ln=1)
	if song.key:
		pdf.set_font("Courier", size=14)
		pdf.cell(0, 0.2, txt=f"Key: {song.key}", ln=1)

	top_y = pdf.get_y()
	cur_x = pdf.get_x()
	lyric_size = args.font_size
	h = round(lyric_size / 72, 2)
	bottom = 11 - pdf.t_margin - (h*3)

	for p in song.scan:
		if pdf.get_y() > bottom:
			if pdf.get_x() > col_width or args.no_cols:
				pdf.add_page()
			else:
				pdf.set_xy(pdf.l_margin + col_width + col_space, top_y)


		pdf.set_font("Courier", 'B', size=lyric_size)
		pdf.cell(col_width, h, txt="", ln=1)
		pdf.set_x(cur_x)
		
		pdf.cell(col_width, h + 0.02, txt=f"[{p}]", ln=1)
		pdf.set_x(cur_x)

		for chord, lyric in zip(song.chords[p], song.lyrics[p]):
			pdf.set_font("Courier", 'B', size=lyric_size)
			pdf.cell(col_width, h, txt=chord, ln=1)
			pdf.set_x(cur_x)
			pdf.set_font("Courier", size=lyric_size)
			pdf.cell(col_width, h, txt=lyric, ln=1)
			pdf.set_x(cur_x)


			if pdf.get_y() > bottom:
				if pdf.get_x() > col_width or args.no_cols:
					pdf.add_page()
				else:
					pdf.set_xy(pdf.l_margin + col_width + col_space, top_y)
			cur_x = pdf.get_x()

	pdf.output(args.filepath[0].replace('.txt', '.pdf'), 'F')

if __name__ == "__main__":
	main()
