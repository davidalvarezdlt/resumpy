import argparse
import cv_generator.themes
import logging
import os
import random

# Create the ArgumentParse and parse the arguments inside `args`
parser = argparse.ArgumentParser(description='Run CV Generator')
parser.add_argument(
    '--cv-file', required=True,
    help='Relative or absolute path to the raw .json or .yaml resume file'
)
parser.add_argument(
    '--theme', choices=['sitges'],
    help='Name of the theme of the generated resume'
)
parser.add_argument(
    '--filename', required=False, help='Generated file name, without extension'
)
parser.add_argument(
    '--keep-tex', action='store_true',
    help='Keep LaTeX files used to generate the resume'
)
args = parser.parse_args()

# Define required files and folders
base_path = os.path.dirname(os.path.dirname(__file__))
cv_schema_path = os.path.join(base_path, 'cv.schema.json')

# Create a logging.Logger object to be used in the execution
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - [%(levelname)s] %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger('cv_generator')
logger.propagate = True

# Create a new CV object with the data provided in the --cv-file argument
cv = cv_generator.CV(logger).load(args.cv_file, cv_schema_path)
cv.sort_data()

# Get the child class of cv_generator.themes.BaseTheme to use
themes_dict = {'sitges': cv_generator.themes.ThemeSitges}
theme = themes_dict[args.theme](cv, logger)

# Define the name (and path) of the generated file random.randint(1, 10E6)
file_name = args.filename if args.filename \
    else '{}-{}'.format(theme.theme_name, random.randint(1, 1E6))
file_path = os.path.join(base_path, 'generated_documents') + os.sep + \
            '{}'.format(file_name)

# Save the generated document in generated_file_path
theme.save(file_path, args.keep_tex)
logger.info(
    'File {}.pdf generated inside /generated_documents'.format(file_name)
)
