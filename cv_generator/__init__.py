from .model import BasicInfo, ContactInfo, ExperienceItem, EducationItem, \
    AwardItem, PublicationItem, LanguageItem, CourseItem, ProjectItem, \
    SkillItem, LinkItem
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
        cv_raw = self._load_raw_data(cv_file_path)
        self._validate_raw_data(cv_raw, cv_schema_path)
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

    def _load_raw_data(self, cv_file_path):
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
        return json.load(
            open(cv_file_path, 'rb')) if file_extension == '.json' else \
            yaml.full_load(open(cv_file_path, 'rb'))

    def dump(self, cv_file_path):
        """Dumps the object into JSON and YAML files.

        Args:
            cv_file_path (string): path to the file where the data should be
                stored, without extension.
        """
        cv_raw = CV._dump_cleaner({
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
        cv_raw_json = json.dumps(cv_raw, indent=2, ensure_ascii=False,
                                 default=CV._dump_handler)
        cv_raw_yaml = yaml.dump(json.loads(cv_raw_json), allow_unicode=True,
                                sort_keys=False)
        open(cv_file_path + '.json', 'wt').write(cv_raw_json)
        open(cv_file_path + '.yaml', 'wt').write(cv_raw_yaml)

    def _validate_raw_data(self, cv_raw, cv_schema_path):
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

    def sort_data(self):
        """Sorts the elements of the model following predefined principles.
        """
        self.projects = sorted(self.projects, key=lambda x: not x.featured)

    def get_age(self):
        """Converts the birthdate into an age.

        Returns:
            int: age of the person.
        """
        today = datetime.date.today()
        return today.year - self.basic.birthday.year - (
                (today.month, today.day) <
                (self.basic.birthday.month, self.basic.birthday.day)
        )

    def get_language_score(self, language_level):
        """Assings a numeric value to each CEFR language level.

        Args:
            language_level (string): language level in CEFR format.
        """
        return {'A1': 40, 'A2': 50, 'B1': 60, 'B2': 70, 'C1': 80, 'C2': 90,
                'Native': 100}[language_level]

    def get_skills_categories(self):
        categories_list = []
        for item in self.skills:
            if item.category is not None and \
                    item.category not in categories_list:
                categories_list.append(item.category)
        return categories_list

    def filter_skills_by_category(self, category):
        """Filters the skills by category.

        Args:
            category (string): identifier of the category of the skills to
                return.

        Returns:
            list: list of skills belonging to `category`.
        """
        return [item for item in self.skills if
                (category is None or item.category == category)]

    @staticmethod
    def _dump_cleaner(cv_raw):
        """Cleans invalid elements before dumping them.

        Used when dumping the data. Instead of filling a document with invalid
        values, this function removes those attributes which do not have a
        valid value.

        Args:
            cv_raw (dict): raw document with invalid attributes.

        Returns:
            dict: document without invalid attributes.
        """
        cv_raw_cleaned = {}
        for k, v in cv_raw.items():
            if type(cv_raw[k]) == dict:
                cv_raw_cleaned[k] = CV._dump_cleaner(cv_raw[k])
            if type(cv_raw[k]) == list:
                cv_raw_cleaned[k] = [CV._dump_cleaner(list_item) for list_item
                                     in cv_raw[k]]
            elif v is not None and v != -1 and v != '':
                cv_raw_cleaned[k] = v
        return cv_raw_cleaned

    @staticmethod
    def _dump_handler(o):
        if isinstance(o, (datetime.date, datetime.datetime)):
            return o.isoformat()
        elif isinstance(o, LinkItem):
            return {'anchor': o.anchor, 'href': o.href}
