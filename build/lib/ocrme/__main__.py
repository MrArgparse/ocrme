from PIL import Image
from tomlkit import dumps
import argparse
import dataclasses
import logging
import os
import pytesseract # type: ignore
import tomllib

def parse_ocrme() -> argparse.Namespace:
	parser = argparse.ArgumentParser(prog='ocrme', description='OCR tool')
	parser.add_argument('images', nargs='+', type=str, help='Images to process')
	parser.add_argument('--noexit', action='store_true', help='Prevents console from closing when done')

	return parser.parse_args()

@dataclasses.dataclass(kw_only=True)
class DefaultConfig:
	TesseractPath: str = 'C:/Users/-/AppData/Local/Programs/Tesseract-OCR/tesseract.exe'
	OutputPath: str = os.path.expanduser('~')
	Extensions: list[str] = dataclasses.field(default_factory=list)

def find_images(arg: str, extensions: list[str]) -> list[str]:
	image_files = []

	for root, dirs, filenames in os.walk(arg):

		for filename in filenames:

			if any(filename.endswith(ext) for ext in extensions):
				image_files.append(os.path.join(root, filename))

	return sorted(image_files)

def organize_pics(filenames: list[str], extensions: list[str]) -> list[str]:
	pics = []

	for arg in filenames:
	
		if os.path.isdir(arg):
			pics.extend(find_images(arg, extensions))

		if os.path.isfile(arg) and any(arg.endswith(ext) for ext in extensions):
			pics.append(arg)

	pics.sort()

	return pics

def main() -> None:
	default_config = DefaultConfig(Extensions=[".bmp", ".gif", ".jpg", ".jpeg", ".png"])
	config_path = os.path.join(os.path.expanduser("~"), ".config", "ocrme")
	config_file = os.path.join(config_path, 'ocrme_config.toml')

	if not os.path.isfile(config_file):
		os.makedirs(config_path, exist_ok=True)

		with open(config_file, 'w') as f:
			f.write(dumps(dataclasses.asdict(default_config)))

	try:
		with open(config_file, 'rb') as f:
			config = tomllib.load(f)

		path_to_tesseract = config['TesseractPath']
		output_path = config['OutputPath']
		extensions = config['Extensions']

	except (FileNotFoundError, tomllib.TOMLDecodeError) as e :
		logging.error(f'{type(e).__name__}: {e}')

	args = parse_ocrme()
	pytesseract.pytesseract.tesseract_cmd = path_to_tesseract
	pics = organize_pics(args.images, extensions)

	for pic in pics:
		image_to_convert = pytesseract.image_to_string(Image.open(pic))
		name = os.path.splitext(os.path.basename(pic))[0]

		with open(os.path.join(output_path, f'{name}.txt')) as text_file:
			text_file.write(image_to_convert)

if __name__ == '__main__':
	main()