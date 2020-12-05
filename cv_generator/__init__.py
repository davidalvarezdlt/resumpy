from .model import LinkItem, RichTextItem, BasicInfo, ContactInfo, \
    ExperienceItem, EducationItem, AwardItem, PublicationItem, LanguageItem,\
    CourseItem, ProjectItem, SkillItem
import datetime
import json
import jsonschema
import os
import yaml


class CV:
    lang = ''
    last_update = None
    basic = None
    contact = None
    experience = []
    education = []
    awards = []
    publications = []
    languages = []
    courses = []
    projects = []
    skills = []

    def load(self, cv_file_path, cv_schema_path):
        cv_raw = CV.load_raw_data(cv_file_path)
        CV.validate_raw_data(cv_raw, cv_schema_path)
        self.lang = cv_raw['lang']
        self.last_update = datetime.datetime.strptime(
            cv_raw['last_update'], '%Y-%m-%d'
        ).date()
        self.basic = BasicInfo(cv_raw['basic'])
        self.contact = ContactInfo(cv_raw['contact']) \
            if 'contact' in cv_raw else None
        self.experience = [
            ExperienceItem(experience_item) for experience_item in
            cv_raw['experience']
        ] if 'experience' in cv_raw else []
        self.education = [
            EducationItem(education_item) for education_item in
            cv_raw['education']
        ] if 'experience' in cv_raw else []
        self.awards = [
            AwardItem(awards_item) for awards_item in cv_raw['awards']
        ] if 'awards' in cv_raw else []
        self.publications = [
            PublicationItem(publications_item) for publications_item in
            cv_raw['publications']
        ] if 'publications' in cv_raw else []
        self.languages = [
            LanguageItem(languages_item) for languages_item in
            cv_raw['languages']
        ] if 'languages' in cv_raw else []
        self.courses = [
            CourseItem(courses_item) for courses_item in
            cv_raw['courses']
        ] if 'courses' in cv_raw else []
        self.projects = [
            ProjectItem(projects_item) for projects_item in
            cv_raw['projects']
        ] if 'projects' in cv_raw else []
        self.skills = [
            SkillItem(skills_item) for skills_item in cv_raw['skills']
        ] if 'skills' in cv_raw else []

    def sort(self):
        """Sorts the elements of the model following predefined principles.
        """
        self.projects = sorted(self.projects, key=lambda x: not x.featured)

    def dump(self, cv_file_path, save_json=True, save_yaml=True):
        """Dumps the object into JSON and YAML files.

        Args:
            cv_file_path (string): path to the file where the data should be
                stored, without extension.
            save_json (bool): whether to save the JSON version of the CV.
            save_yaml (bool): whether to save the YAML version of the CV.
        """
        cv_raw_json = json.dumps(self.__dict__(), indent=2)
        if save_json:
            open(cv_file_path + '.json', 'wt').write(cv_raw_json)
        if save_yaml:
            cv_raw_yaml = yaml.dump(
                json.loads(cv_raw_json), allow_unicode=True, sort_keys=False
            )
            open(cv_file_path + '.yaml', 'wt').write(cv_raw_yaml)

    def __dict__(self):
        return CV._to_dict_helper({
            'lang': self.lang,
            'last_update': self.last_update,
            'basic': self.basic.__dict__,
            'contact': self.contact.__dict__,
            'experience': [item.__dict__ for item in self.experience],
            'education': [item.__dict__ for item in self.education],
            'awards': [item.__dict__ for item in self.awards],
            'publications': [item.__dict__ for item in self.publications],
            'languages': [item.__dict__ for item in self.languages],
            'courses': [item.__dict__ for item in self.courses],
            'projects': [item.__dict__ for item in self.projects],
            'skills': [item.__dict__ for item in self.skills],
        })

    def __eq__(self, other):
        return self.__dict__() == other.__dict__()

    @staticmethod
    def load_raw_data(cv_file_path):
        """Loads the input JSON or YAML file.

        Loads the input data inside the `self._cv_file` attribute of the class.

        Args:
            cv_file_path (str): path the the input JSON or YAML file.
        """
        file_extension = os.path.splitext(os.path.basename(cv_file_path))[1]
        if file_extension not in ['.json', '.yaml']:
            exit('The extension of the input file is not compatible.')
        if not os.path.exists(cv_file_path):
            exit('It has not been possible to read the input file. Make sure '
                 'that you provide a path relative to the execution folder or,'
                 ' if not, provide an absolute path to your JSON or YAML '
                 'file.')
        if file_extension == '.json':
            return json.load(open(cv_file_path))
        else:
            return yaml.full_load(open(cv_file_path))

    @staticmethod
    def validate_raw_data(cv_raw, cv_schema_path):
        """Validates input CV data using `cv.schema.json`.

        Validates the input CV file using the schema provided in
        `cv.schema.json`, which follows the JSONSchema protocol.

        Args:
            cv_schema_path (str): path to the 'cv.schema.json' schema file
        """
        if not os.path.exists(cv_schema_path):
            exit('The file cv.schema.json has not been found. Verify that you'
                 'have not deleted it accidentally.')
        jsonschema.validate(cv_raw, json.load(open(cv_schema_path)))

    @staticmethod
    def _to_dict_helper(cv_raw):
        cv_raw_cleaned = {}
        for k, v in cv_raw.items():
            if type(cv_raw[k]) == dict:
                cv_raw_cleaned[k] = CV._to_dict_helper(cv_raw[k])
            elif type(cv_raw[k]) == list:
                cv_raw_cleaned[k] = [
                    CV._to_dict_helper(list_item) for list_item in cv_raw[k]
                ]
            elif isinstance(cv_raw[k], (datetime.date, datetime.datetime)):
                cv_raw_cleaned[k] = cv_raw[k].isoformat()
            elif isinstance(cv_raw[k], LinkItem):
                cv_raw_cleaned[k] = {
                    'anchor': cv_raw[k].anchor, 'href': cv_raw[k].href
                }
            elif isinstance(cv_raw[k], RichTextItem):
                cv_raw_cleaned[k] = [item for item in cv_raw[k].items]
            elif v is not None and v != -1 and v != '':
                cv_raw_cleaned[k] = v
        return cv_raw_cleaned
