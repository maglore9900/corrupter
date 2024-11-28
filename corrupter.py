import argparse
from PIL import Image
import os
import subprocess
import random

import os

def check_png_exists(file_path):
	#! Get the directory and file name without extension
	directory = os.path.dirname(file_path)
	print(f"directory {directory}")
	file_name_without_ext = os.path.splitext(os.path.basename(file_path))[0]
	print(f"filename {file_name_without_ext}")

	#! Construct the PNG file path
	png_file_path = os.path.join(directory, f"{file_name_without_ext}.png")
	print(f"png_file_path {png_file_path}")

	#! Check if the PNG file exists
	print("png exists")
	return os.path.exists(png_file_path)


def convert_to_png(file_path):
	if check_png_exists(file_path):
		return
	try:
		with Image.open(file_path) as img:
			if img.format == 'PNG':
				print(f'The file "{file_path}" is already a PNG.')
				return

			png_file_path = os.path.splitext(file_path)[0] + '.png'
			img.save(png_file_path, 'PNG')
			print(f'The file "{file_path}" has been converted to "{png_file_path}".')

	except FileNotFoundError:
		print(f'The file "{file_path}" was not found.')
	except Exception as e:
		print(f'An error occurred while processing the file: {e}')

def main():
	parser = argparse.ArgumentParser(description='Convert an image to PNG.')
	parser.add_argument('-f', '--file', required=True, help='The image file to process')
	parser.add_argument('-r', '--repeat', required=False, help='Repeat X times')
	parser.add_argument('-v', '--verbose', required=False, help='Show image modification values')
	parser.add_argument('-mag', '--mag_value', required=False, help='Dissolve blur strength')
	parser.add_argument('-boff', '--boffset_value', required=False, help='Distorted block offset strength')
	parser.add_argument('-lag', '--lag_value', required=False, help='Per-channel scanline lag strength')
	parser.add_argument('-meanabber', '--meanabber_value', required=False, help='Mean chromatic abberation offset')
	parser.add_argument('-stdabber', '--stdabber_value', required=False, help='Std. dev. of chromatic abberation offset (lower values induce longer trails)')
	parser.add_argument('-bheight', '--bheight_value', required=False, help='Average distorted block height')
	parser.add_argument('-bright', '--color_int', required=False, help='Brightness control (0-255)')
	parser.add_argument('-stdoffset', '--stdoffset_value', required=False, help='std. dev. of red-blue channel offset (non-destructive) - Float')

	args = parser.parse_args()
	repeat = int(args.repeat) if args.repeat else 1
	count = 0
	file_path = args.file
	print(f'The provided file is: {file_path}')
	
	file, file_type = file_path.split(".")
	#! file must be png, test and convert if necessary
	if file_type.lower() != "png": convert_to_png(file_path)    
	script_dir = os.path.dirname(os.path.abspath(__file__))
	destination = f"{script_dir}/output/"
	
	#! Path to the corrupter executable
	corrupter_path = os.path.join(script_dir, 'corrupter.exe')
	input_file_path = os.path.join(script_dir, f'{file}.png')
	
 
	while count < repeat:	
		output_file_path = os.path.join(destination, f'corrupt_{file.split('\\')[-1]}_{count}.png')
		mag_value = args.mag_value if args.mag_value else str(random.uniform(1,5))
		boffset_value = args.boffset_value if args.boffset_value else str(random.randint(8,15))
		lag_value = args.lag_value if args.lag_value else str(random.uniform(0.05, 0.02))
		meanabber_value = args.meanabber_value if args.meanabber_value else str(random.randint(5,10))
		stdabber_value = args.stdabber_value if args.stdabber_value else str(random.uniform(5, 10))
		bheight_value = args.bheight_value if args.bheight_value else str(random.randint(1,10))
		stdoffset = args.stdoffset_value if args.stdoffset_value else str(random.uniform(6,10))
		color_int = int(args.color_int) if args.color_int else random.randint(0,100)
		if color_int > 70:
			add_value = '80'
		elif color_int > 60:
			add_value = '50'
		elif color_int > 40:
			add_value = '37'
		elif color_int > 30:
			add_value = '20'
		else:
			add_value = '10'

		if args.verbose:
			print(f"Iteration: {count}")
			print(f"mag value {mag_value}")
			print(f"boffset value {boffset_value}")
			print(f"lag value {lag_value}")
			print(f"meanabber value {meanabber_value}")
			print(f"stabber value {stdabber_value}")
			print(f"bheight value {bheight_value}")
			print(f"add value {add_value}")
			print(f"stdoffset {stdoffset}")
		
		try:
			#! Execute the corrupter file with the following variables
			result = subprocess.run([corrupter_path, '-lag', lag_value, '-meanabber', meanabber_value, '-mag', mag_value, '-stdabber', stdabber_value, '-bheight', bheight_value, '-add', add_value, '-boffset', boffset_value, '-stdoffset', stdoffset,  input_file_path, output_file_path])
			
			if result.returncode == 0:
				print("success")
			else:
				print("failed with return code:", result.returncode)

		except Exception as e:
			print("An error occurred:", e) 
		count += 1
		print("------")

if __name__ == '__main__':
	main()
