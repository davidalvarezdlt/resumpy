import argparse
import cv_generator
import cv_generator.model
import datetime
import random
import requests
import os.path

parser = argparse.ArgumentParser()
parser.add_argument('--repository-name', required=True, help='Name of the Prismic repository')
parser.add_argument('--access-token', required=True, help='Access token of the repository')
parser.add_argument('--language-code', choices=['en-US', 'es-ES'], required=True, help='Language code of the data')
args = parser.parse_args()


class PrismicAPI:
    endpoint = None
    endpoint_ref = None
    token = None
    ref = None

    def __init__(self, repository_name, token):
        self.endpoint = 'https://{}.prismic.io/api/v2/documents/search'.format(repository_name)
        self.endpoint_ref = 'https://{}.prismic.io/api/v2'.format(repository_name)
        self.token = token
        self._init_ref()

    def _init_ref(self):
        api_response = requests.get(self.endpoint_ref, {'access_token': self.token}).json()
        self.ref = api_response['refs'][0]['ref']

    def get_general(self, lang):
        request_args = {
            'access_token': self.token, 'ref': self.ref, 'q': '[[at(document.type, "general")]]', 'lang': lang
        }
        return requests.get(self.endpoint, request_args).json()

    def get_about_me(self, lang):
        request_args = {
            'access_token': self.token, 'ref': self.ref, 'q': '[[at(document.type, "about_me")]]', 'lang': lang
        }
        return requests.get(self.endpoint, request_args).json()

    def get_publications(self, lang):
        request_args = {
            'access_token': self.token, 'ref': self.ref, 'q': '[[at(document.type, "publications_item")]]',
            'orderings': '[my.publications_item.publications_item_date desc]', 'lang': lang
        }
        return requests.get(self.endpoint, request_args).json()

    def get_projects(self, lang):
        request_args = {
            'access_token': self.token, 'ref': self.ref, 'q': '[[at(document.type, "projects_item")]]', 'lang': lang
        }
        return requests.get(self.endpoint, request_args).json()

    @staticmethod
    def load_date(date_str):
        return datetime.datetime.strptime(date_str, '%Y-%m-%d').date()

    @staticmethod
    def load_text(paragraphs):
        return "\n".join([par['text'] for par in paragraphs])


def translate_skills_category(skills_category, lang):
    skills_categories_keys = [
        'Information Technologies', 'Computer Science', 'Electrical Engineering', 'Mathematics', 'Physics',
        'Business', 'Others'
    ]
    en_us = [
        'Information Technologies', 'Computer Science', 'Electrical Engineering', 'Mathematics', 'Physics',
        'Business & Marketing', 'Others'
    ]
    es_es = [
        'Tecnologías de la Información', 'Informática', 'Ingeniería Eléctrica', 'Matemáticas', 'Física',
        'Marketing & Negocios', 'Otros'
    ]
    return {'en-US': en_us, 'es-ES': es_es}[lang][skills_categories_keys.index(skills_category)]


# Create model objects and fill them
cv = cv_generator.CV(None)
cv.lang = args.language_code
cv.last_update = datetime.date.today()

# GET data from the API
prismic = PrismicAPI(args.repository_name, args.access_token)
general_response = prismic.get_general(cv.lang)
about_me_response = prismic.get_about_me(cv.lang)

# Basic
cv.basic.name = about_me_response['results'][0]['data']['about_me_profile_name']
cv.basic.surnames = about_me_response['results'][0]['data']['about_me_profile_surnames']
cv.basic.profession = about_me_response['results'][0]['data']['about_me_profile_profession']
cv.basic.birthday = PrismicAPI.load_date(about_me_response['results'][0]['data']['about_me_profile_birthday'])
cv.basic.birthplace = about_me_response['results'][0]['data']['about_me_profile_birthplace']
cv.basic.residence = about_me_response['results'][0]['data']['about_me_profile_residence']
cv.basic.marital_status = about_me_response['results'][0]['data']['about_me_profile_marital_status']
cv.basic.biography = PrismicAPI.load_text(about_me_response['results'][0]['data']['about_me_profile_biography'])
cv.basic.hobbies = about_me_response['results'][0]['data']['about_me_profile_hobbies']

# Contact
cv.contact.email = 'davidalvarezdlt@gmail.com'
cv.contact.phone = '(+34) 666 77 88 99'
cv.contact.personal_website = cv_generator.model.LinkItem()
cv.contact.personal_website.anchor = 'davidalvarezdlt.com'
cv.contact.personal_website.href = 'https://{}.davidalvarezdlt.com/'.format('en' if cv.lang == 'en-US' else 'es')
cv.contact.twitter = cv_generator.model.LinkItem()
cv.contact.twitter.anchor = 'Twitter'
cv.contact.twitter.href = general_response['results'][0]['data']['general_social_twitter']['url']
cv.contact.linkedin = cv_generator.model.LinkItem()
cv.contact.linkedin.anchor = 'LinkedIn'
cv.contact.linkedin.href = general_response['results'][0]['data']['general_social_linkedin']['url']
cv.contact.github = cv_generator.model.LinkItem()
cv.contact.github.anchor = 'GitHub'
cv.contact.github.href = general_response['results'][0]['data']['general_social_github']['url']
cv.contact.scholar = cv_generator.model.LinkItem()
cv.contact.scholar.anchor = 'Google Scholar'
cv.contact.scholar.href = general_response['results'][0]['data']['general_social_scholar']['url']

# Experience
for experience_item_response in about_me_response['results'][0]['data']['about_me_experience']:
    experience_item = cv_generator.model.ExperienceItem()
    experience_item.institution = experience_item_response['about_me_experience_institution']
    experience_item.position = experience_item_response['about_me_experience_position']
    experience_item.date_start = PrismicAPI.load_date(experience_item_response['about_me_experience_date_start'])
    experience_item.date_end = PrismicAPI.load_date(experience_item_response['about_me_experience_date_end'])
    experience_item.description = PrismicAPI.load_text(experience_item_response['about_me_experience_description'])
    cv.experience.append(experience_item)

# Education
for education_item_response in about_me_response['results'][0]['data']['about_me_education']:
    education_item = cv_generator.model.EducationItem()
    education_item.institution = education_item_response['about_me_education_institution']
    education_item.degree = education_item_response['about_me_education_degree']
    education_item.major = education_item_response['about_me_education_major']
    education_item.date_start = PrismicAPI.load_date(education_item_response['about_me_education_date_start'])
    education_item.date_end = PrismicAPI.load_date(education_item_response['about_me_education_date_end'])
    education_item.description = PrismicAPI.load_text(education_item_response['about_me_education_description'])
    education_item.gpa = education_item_response['about_me_education_gpa']
    education_item.gpa_max = education_item_response['about_me_education_gpa_max']
    education_item.performance = education_item_response['about_me_education_performance']
    education_item.promotion_order = education_item_response['about_me_education_promotion_order']
    cv.education.append(education_item)

# Awards
for awards_item_response in about_me_response['results'][0]['data']['about_me_awards']:
    award_item = cv_generator.model.AwardItem()
    award_item.institution = awards_item_response['about_me_awards_institution']
    award_item.name = awards_item_response['about_me_awards_name']
    award_item.date = PrismicAPI.load_date(awards_item_response['about_me_awards_date'])
    award_item.description = PrismicAPI.load_text(awards_item_response['about_me_awards_description'])
    if 'url' in awards_item_response['about_me_awards_diploma']:
        award_item.diploma = cv_generator.model.LinkItem()
        award_item.diploma.anchor = awards_item_response['about_me_awards_diploma_anchor']
        award_item.diploma.href = awards_item_response['about_me_awards_diploma']['url']
    cv.awards.append(award_item)

# Publications
for publications_item_response in prismic.get_publications(cv.lang)['results']:
    publication_item = cv_generator.model.PublicationItem()
    publication_item.title = publications_item_response['data']['publications_item_title']
    publication_item.abstract = publications_item_response['data']['publications_item_abstract']
    publication_item.authors = publications_item_response['data']['publications_item_authors']
    publication_item.date = PrismicAPI.load_date(publications_item_response['data']['publications_item_date'])
    cv.publications.append(publication_item)

# Languages
for languages_item_response in about_me_response['results'][0]['data']['about_me_languages']:
    language_item = cv_generator.model.LanguageItem()
    language_item.name = languages_item_response['about_me_languages_name']
    language_item.level = languages_item_response['about_me_languages_level']
    if 'url' in languages_item_response['about_me_languages_diploma']:
        language_item.diploma = cv_generator.model.LinkItem()
        language_item.diploma.anchor = languages_item_response['about_me_languages_diploma_anchor']
        language_item.diploma.href = languages_item_response['about_me_languages_diploma']['url']
    cv.languages.append(language_item)

# Courses
for courses_item_response in about_me_response['results'][0]['data']['about_me_courses']:
    course_item = cv_generator.model.CourseItem()
    course_item.institution = courses_item_response['about_me_courses_institution']
    course_item.name = courses_item_response['about_me_courses_name']
    course_item.date = PrismicAPI.load_date(courses_item_response['about_me_courses_date'])
    course_item.diploma = cv_generator.model.LinkItem()
    course_item.diploma.anchor = courses_item_response['about_me_courses_diploma_anchor']
    course_item.diploma.href = courses_item_response['about_me_courses_diploma']['url']
    cv.courses.append(course_item)

# Projects
for projects_item_response in prismic.get_projects(cv.lang)['results']:
    project_item = cv_generator.model.ProjectItem()
    project_item.name = projects_item_response['data']['projects_item_name']
    project_item.description = projects_item_response['data']['projects_item_description']
    project_item.link = cv_generator.model.LinkItem()
    project_item.link.anchor = projects_item_response['data']['projects_item_link_anchor']
    project_item.link.href = projects_item_response['data']['projects_item_link']['url']
    cv.projects.append(project_item)

# Skills
for skills_item_response in about_me_response['results'][0]['data']['about_me_skills']:
    skill_item = cv_generator.model.SkillItem()
    skill_item.name = skills_item_response['about_me_skills_name']
    skill_item.type = skills_item_response['about_me_skills_type']
    skill_item.category = translate_skills_category(skills_item_response['about_me_skills_category'], cv.lang)
    skill_item.score = skills_item_response['about_me_skills_score']
    cv.skills.append(skill_item)

# Dump file
file_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), '..', 'cv.example.{}'.format(cv.lang.lower()))
cv.dump(file_path)
