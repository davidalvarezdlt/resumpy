import argparse
import resumpy.themes
import logging
import os
import random

# Create the ArgumentParse and parse the arguments inside `args`
parser = argparse.ArgumentParser(description='Run Resumpy')
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

# Create a logging.Logger object to be used in the execution
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - [%(levelname)s] %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger('resumpy')
logger.propagate = True

# Define required files and folders
base_path = os.path.dirname(os.path.dirname(__file__))
cv_schema_path = os.path.join(base_path, 'cv.schema.json')
file_name = args.filename if args.filename \
    else '{}-{}'.format(args.theme, random.randint(1, 1E6))
file_path = os.path.join(os.getcwd(), '{}'.format(file_name))

# Create a new CV object with the data provided in the --cv-file argument
cv = resumpy.CV(logger)
cv.load(args.cv_file, cv_schema_path)
cv.generate(args.theme, file_path, args.keep_tex)
