import resumpy.model
import resumpy.theme
import json
import jsonschema
import os
import shutil
import yaml


class CV:
    model = None
    logger = None

    def __init__(self, logger):
        self.logger = logger

    def load(self, cv_file_path, cv_schema_path):
        """Loads the data given in a text file into the model object.

        Args:
            cv_file_path (str): path to the file containing the CV data.
            cv_schema_path (str): path to the schema file used to validate
            `cv_file_path`.
        """

        # Verify cv_schema_path
        file_extension = os.path.splitext(os.path.basename(cv_schema_path))[1]
        if file_extension != '.json':
            self.logger.error('The extension of --theme is invalid.')
            exit()
        if not os.path.exists(cv_schema_path):
            self.logger.error('File provided in --theme is invalid.')
            exit()

        # Verify cv_file_path
        file_extension = os.path.splitext(os.path.basename(cv_file_path))[1]
        if file_extension not in ['.json', '.yaml']:
            self.logger.error('The extension of --cv-file is invalid.')
            exit()
        if not os.path.exists(cv_file_path):
            self.logger.error('File provided in --theme is invalid.')
            exit()

        # Read, validate and load CV data
        cv_raw = json.load(open(cv_file_path)) if file_extension == '.json' \
            else yaml.full_load(open(cv_file_path))
        jsonschema.validate(cv_raw, json.load(open(cv_schema_path)))
        self.model = resumpy.model.Model(cv_raw)

    def save(self, cv_file_path, save_json=True, save_yaml=True):
        """Dumps the loaded CV into JSON and YAML files.

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
        """Generates the CV using the data loaded in the CV and the theme named
        `theme_name`.

        Args:
            theme_name (str): name of the theme to use.
            file_path (str): path where the generated file should be stored.
            keep_tex (bool): whether to keep the generated .tex file.
        """
        theme_obj = resumpy.theme.Theme.create_theme_by_name(
            theme_name, self.logger
        )

        # Copy .cls file into the folder
        cls_path = os.path.join(
            os.path.dirname(__file__), 'themes', 'cls', theme_name + '.cls'
        )
        shutil.copy(cls_path, os.path.dirname(file_path))

        # Get doc object
        doc = theme_obj.format(self.model)
        doc.generate_pdf(file_path, clean_tex=not keep_tex)

        # Remove .tex file if specified
        if not keep_tex:
            os.remove(os.path.join(
                os.path.dirname(file_path), os.path.basename(cls_path)
            ))

    def __eq__(self, other):
        return self.model.dump() == other.model.dump()
