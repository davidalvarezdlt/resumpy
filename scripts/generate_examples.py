import resumpy
import resumpy.themes
import logging
import os

# Create the CV object
base_path = os.path.dirname(os.path.dirname(__file__))
CV = resumpy.CV(logging.getLogger('resumpy'))
CV.load(
    os.path.join(base_path, 'cv.example.json'),
    os.path.join(base_path, 'cv.schema.json')
)

# Generate the CV using the different themes
for theme_name in resumpy.themes.__themes_names__:
    file_path = os.path.join(
        base_path, 'examples', theme_name + '-example'
    )
    CV.generate(theme_name, file_path, keep_tex=False)
