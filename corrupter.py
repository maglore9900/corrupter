import argparse
from PIL import Image
import os
import subprocess
import random

def convert_to_png(file_path):
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

	args = parser.parse_args()

	file_path = args.file
	print(f'The provided file is: {file_path}')
	
	file, file_type = file_path.split(".")
	if file_type.lower() != "png":
		convert_to_png(file_path)    
	script_dir = os.path.dirname(os.path.abspath(__file__))
	destination = f"{script_dir}/output/"
	
	# Path to the corrupter executable
	corrupter_path = os.path.join(script_dir, 'corrupter.exe')
	
	# Paths for input and output files
	input_file_path = os.path.join(script_dir, f'{file}.png')
	output_file_path = os.path.join(destination, f'corrupt_{file}.png')
	mag_value = str(random.randint(1,6) )
	boffset_value = str(random.randint(5,10))
	print(f"mag value {mag_value}")
	print(f"boffset value {boffset_value}")
	lag_value = str(random.uniform(0.005, 0.01))
	print(f"lag value {lag_value}")
	try:
		# Pass each component of the command as a separate argument
		result = subprocess.run([corrupter_path, '-lag', lag_value, '-mag', mag_value, '-boffset', boffset_value,  input_file_path, output_file_path])
		
		if result.returncode == 0:
			print("success")
		else:
			print("failed with return code:", result.returncode)

	except Exception as e:
		print("An error occurred:", e) 

if __name__ == '__main__':
	main()
