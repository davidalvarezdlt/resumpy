import datetime
import json
import jsonschema
import os
import logging
import yaml
from .model import BasicInfo, ContactInfo, ExperienceInfo, EducationInfo, AwardsInfo, ProjectsInfo, CoursesInfo, \
    PublicationsInfo, LanguagesInfo, SkillsInfo, MiscInfo
from .theme import BaseTheme


class CV:
    _cv_file: dict
    _cv_schema: dict

    lang: str
    last_update: datetime.date
    basic: BasicInfo
    contact: ContactInfo
    experience: ExperienceInfo
    education: EducationInfo
    awards: AwardsInfo
    projects: ProjectsInfo
    courses: CoursesInfo
    publications: PublicationsInfo
    languages: LanguagesInfo
    skills: SkillsInfo
    misc: MiscInfo

    logger: logging.Logger

    def __init__(self, cv_file_path: str, cv_schema_path: str, logger: logging.Logger):
        self.logger = logger
        self._load_raw_data(cv_file_path)
        self._validate_raw_data(cv_schema_path)
        self._load_data()

    def _load_raw_data(self, cv_file_path: str):
        """Loads the input JSON or YAML file

        Loads the input data inside the `self._cv_file` attribute of the class.

        Args:
            cv_file_path (str): path the the input JSON or YAML file.
        """
        try:
            with open(cv_file_path, 'rb') as cv_file_obj:
                file_extension = os.path.splitext(os.path.basename(cv_file_path))[1]
                if file_extension not in ['.json', '.yaml']:
                    raise ValueError
                self._cv_file = json.load(cv_file_obj) if file_extension == '.json' else yaml.full_load(cv_file_obj)
        except ValueError:
            self.logger.error('The extension of the input file is not compatible.')
            exit()
        except FileNotFoundError:
            self.logger.error(
                'It has not been possible to read the input file. Make sure that you provide a path relative to the '
                'execution folder or, if not, provide an absolute path to your JSON or YAML file.'
            )
            exit()

    def _validate_raw_data(self, cv_schema_path: str):
        """Validates input CV data using `cv.schema.json`.

        Validates the input CV file using the schema provided in `cv.schema.json`, which follows the JSONSchema
        protocol.

        Args:
            cv_schema_path (str): path to the 'cv.schema.json' schema file
        """
        try:
            with open(cv_schema_path) as cv_schema_obj:
                self._cv_schema = json.load(cv_schema_obj)
            jsonschema.validate(self._cv_file, self._cv_schema)
            self.logger.info('CV validated using cv.schema.json')
        except FileNotFoundError:
            self.logger.error('The file cv.schema.json has not been found. Verify that you have not deleted it '
                              'accidentally.')
            exit()
        except jsonschema.exceptions.ValidationError:
            self.logger.error('The input file does not follow the schema provided in cv.schema.json')
            exit()

    def _load_data(self):
        """Load class-specific attributes from `self._cv_file` attribute

        Loads the different sections of the input file inside class-specific parameters to be consumed by the
        `cv_generator.themes.BaseTheme`.
        """
        self.lang = self._cv_file['lang']
        self.last_update = datetime.datetime.strptime(self._cv_file['last_update'], '%d/%m/%Y').date()
        self.basic = BasicInfo(self._cv_file['basic'])
        self.contact = ContactInfo(self._cv_file['contact']) if 'contact' in self._cv_file else None
        self.experience = ExperienceInfo(self._cv_file['experience']) if 'experience' in self._cv_file else None
        self.education = EducationInfo(self._cv_file['education']) if 'education' in self._cv_file else None
        self.awards = AwardsInfo(self._cv_file['awards']) if 'awards' in self._cv_file else None
        self.projects = ProjectsInfo(self._cv_file['projects']) if 'projects' in self._cv_file else None
        self.courses = CoursesInfo(self._cv_file['courses']) if 'courses' in self._cv_file else None
        self.publications = PublicationsInfo(self._cv_file['publications']) if 'publications' in self._cv_file else None
        self.languages = LanguagesInfo(self._cv_file['languages']) if 'languages' in self._cv_file else None
        self.skills = SkillsInfo(self._cv_file['skills']) if 'skills' in self._cv_file else None
        self.misc = MiscInfo(self._cv_file['misc']) if 'misc' in self._cv_file else None
