import argparse
import cv_generator.themes
import logging
import os
import random
import shutil

# Create the ArgumentParse and parse the arguments inside `args`
parser = argparse.ArgumentParser(description='Run CVGenerator')
parser.add_argument('--cv-file', required=True, help='Path of the global configuration file')
parser.add_argument('--theme', choices=['sitges', 'developer'], help='Path of the global configuration file')
parser.add_argument('--filename', required=False, type=str, help='Generated file name, without extension')
parser.add_argument('--keep-tex', action='store_true', help='Avoid removing the intermediate .tex file')
args = parser.parse_args()

# Define required files and folders
base_path = os.path.dirname(os.path.dirname(__file__))
cv_schema_path = os.path.join(base_path, 'cv.schema.json')

# Create a logging.Logger object to be used in the execution
logging.basicConfig(level=logging.INFO, format='%(asctime)s - [%(levelname)s] %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
logger = logging.getLogger('cv_generator')
logger.propagate = True

# Create a new CV object with the data provided in the --cv-file argument
cv = cv_generator.CV(args.cv_file, cv_schema_path, logger)

# Get the child class of cv_generator.themes.BaseTheme to use
themes_dict = {'sitges': cv_generator.themes.ThemeSitges, 'developer': cv_generator.themes.ThemeDeveloper}
theme = themes_dict[args.theme](cv, logger)

# Define the name (and path) of the generated file random.randint(1, 10E6)
generated_file_name = args.filename if args.filename else '{}-{}'.format(theme.theme_name, random.randint(1, 1E6))
generated_file_path = os.path.join(base_path, 'generated_documents') + os.sep + '{}'.format(generated_file_name)

# Get the document calling the `BaseTheme.format()` method and store it in `generated_file_path`
shutil.copy(theme.get_cls_path(), os.path.dirname(generated_file_path))
theme.format().generate_pdf(generated_file_path, clean_tex=not args.keep_tex)
if not args.keep_tex:
    os.remove(os.path.join(os.path.dirname(generated_file_path), os.path.basename(theme.get_cls_path())))
logger.info('File {}.pdf generated inside /generated_documents'.format(generated_file_name))
