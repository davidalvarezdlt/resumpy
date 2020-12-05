from cv_generator.model import CVModel
import cv_generator.themes
import json
import jsonschema
import os
import yaml


class CV:
    model = None
    logger = None

    def __init__(self, logger):
        self.logger = logger

    def load(self, cv_file_path, cv_schema_path):
        file_extension = os.path.splitext(os.path.basename(cv_file_path))[1]
        if file_extension not in ['.json', '.yaml']:
            exit('The extension of the input file is not compatible.')

        if not os.path.exists(cv_file_path):
            exit('It has not been possible to read the input file. Make sure '
                 'that you provide a path relative to the execution folder or,'
                 ' if not, provide an absolute path to your JSON or YAML '
                 'file.')

        if file_extension == '.json':
            cv_raw = json.load(open(cv_file_path))
        else:
            cv_raw = yaml.full_load(open(cv_file_path))

        # CV Schema Validation
        if not os.path.exists(cv_schema_path):
            exit('The file cv.schema.json has not been found. Verify that you'
                 'have not deleted it accidentally.')
        jsonschema.validate(cv_raw, json.load(open(cv_schema_path)))

        # Creates the model
        self.model = CVModel(cv_raw)

    def save(self, cv_file_path, save_json=True, save_yaml=True):
        """Dumps the object into JSON and YAML files.

        Args:
            cv_file_path (string): path to the file where the data should be
                stored, without extension.
            save_json (bool): whether to save the JSON version of the CV.
            save_yaml (bool): whether to save the YAML version of the CV.
        """
        cv_raw_json = json.dumps(self.model.dump(), indent=2)
        if save_json:
            open(cv_file_path + '.json', 'wt').write(cv_raw_json)
        if save_yaml:
            cv_raw_yaml = yaml.dump(
                json.loads(cv_raw_json), allow_unicode=True, sort_keys=False
            )
            open(cv_file_path + '.yaml', 'wt').write(cv_raw_yaml)

    def generate(self, theme_name, file_path, keep_tex):
        themes_dict = {'sitges': cv_generator.themes.ThemeSitges}
        theme = themes_dict[theme_name](self, self.logger)
        theme.save(file_path, keep_tex)
