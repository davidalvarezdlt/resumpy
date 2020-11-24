import datetime


class BaseModel:

    def __init__(self, data=None):
        if data is not None:
            self.load(data)

    def load(self, data):
        raise NotImplementedError


class LinkItem(BaseModel):
    anchor = ''
    href = ''

    def load(self, link_item_dict):
        self.anchor = link_item_dict['anchor']
        self.href = link_item_dict['href']


class RichTextItem(BaseModel):
    items = []

    def load(self, rich_text_item_dict):
        self.items = rich_text_item_dict


class BasicInfo(BaseModel):
    name = ''
    surnames = ''
    profession = ''
    birthday = None
    birthplace = ''
    residence = ''
    marital_status = ''
    biography = ''
    hobbies = ''

    def load(self, basic_info_dict):
        self.name = basic_info_dict['name']
        self.surnames = basic_info_dict['surnames']
        self.profession = basic_info_dict['profession']
        self.birthday = datetime.datetime.strptime(
            basic_info_dict['birthday'], '%Y-%m-%d'
        ).date()
        self.birthplace = basic_info_dict['birthplace']
        self.residence = basic_info_dict['residence']
        self.marital_status = basic_info_dict['marital_status']
        self.biography = basic_info_dict['biography']
        self.hobbies = basic_info_dict['hobbies'] \
            if 'hobbies' in basic_info_dict else ''


class ContactInfo(BaseModel):
    email = ''
    phone = ''
    personal_website = None
    twitter = None
    linkedin = None
    github = None
    scholar = None

    def load(self, contact_info_dict):
        self.email = contact_info_dict['email']
        self.phone = contact_info_dict['phone']
        self.personal_website = LinkItem(
            contact_info_dict['personal_website']) \
            if 'personal_website' in contact_info_dict else None
        self.twitter = LinkItem(contact_info_dict['twitter']) \
            if 'twitter' in contact_info_dict else None
        self.linkedin = LinkItem(contact_info_dict['linkedin']) \
            if 'linkedin' in contact_info_dict else None
        self.github = LinkItem(contact_info_dict['github']) \
            if 'github' in contact_info_dict else None
        self.scholar = LinkItem(contact_info_dict['scholar']) \
            if 'scholar' in contact_info_dict else None


class ExperienceItem(BaseModel):
    institution = ''
    position = ''
    date_start = None
    date_end = None
    description = None

    def load(self, experience_item_dict):
        self.institution = experience_item_dict['institution']
        self.position = experience_item_dict['position']
        self.date_start = datetime.datetime.strptime(
            experience_item_dict['date_start'], '%Y-%m-%d').date()
        self.date_end = datetime.datetime.strptime(
            experience_item_dict['date_end'], '%Y-%m-%d').date() \
            if 'date_end' in experience_item_dict else None
        self.description = RichTextItem(experience_item_dict['description']) \
            if 'description' in experience_item_dict else None


class EducationItem(BaseModel):
    institution = ''
    degree = ''
    major = ''
    date_start = None
    date_end = None
    description = None
    gpa = -1
    gpa_max = -1
    performance = -1
    promotion_order = ''

    def load(self, education_item_dict):
        self.institution = education_item_dict['institution']
        self.degree = education_item_dict['degree']
        self.major = education_item_dict[
            'major'] if 'major' in education_item_dict else ''
        self.date_start = datetime.datetime.strptime(
            education_item_dict['date_start'], '%Y-%m-%d').date()
        self.date_end = datetime.datetime.strptime(
            education_item_dict['date_end'], '%Y-%m-%d').date() \
            if 'date_end' in education_item_dict else None
        self.description = RichTextItem(education_item_dict['description']) \
            if 'description' in education_item_dict else ''
        self.gpa = education_item_dict[
            'gpa'] if 'gpa' in education_item_dict else -1
        self.gpa_max = education_item_dict[
            'gpa_max'] if 'gpa_max' in education_item_dict else -1
        self.performance = education_item_dict[
            'performance'] if 'performance' in education_item_dict else -1
        self.promotion_order = education_item_dict['promotion_order'] \
            if 'promotion_order' in education_item_dict else ''


class AwardItem(BaseModel):
    institution = ''
    name = ''
    date = None
    description = ''
    diploma = None

    def load(self, award_item_dic):
        self.institution = award_item_dic['institution']
        self.name = award_item_dic['name']
        self.date = datetime.datetime.strptime(
            award_item_dic['date'], '%Y-%m-%d').date()
        self.description = award_item_dic['description'].rstrip() \
            if 'description' in award_item_dic else ''
        self.diploma = LinkItem(award_item_dic['diploma']) \
            if 'diploma' in award_item_dic else None


class PublicationItem(BaseModel):
    title = ''
    abstract = ''
    authors = ''
    conference = ''
    date = None
    manuscript_link = None
    code_link = None

    def load(self, publication_item_dict):
        self.title = publication_item_dict['title']
        self.abstract = publication_item_dict['abstract'].rstrip()
        self.authors = publication_item_dict['authors']
        self.conference = publication_item_dict['conference']
        self.date = datetime.datetime.strptime(publication_item_dict['date'],
                                               '%Y-%m-%d').date()
        self.manuscript_link = LinkItem(
            publication_item_dict['manuscript_link']) \
            if 'manuscript_link' in publication_item_dict else None
        self.code_link = LinkItem(publication_item_dict['code_link']) \
            if 'code_link' in publication_item_dict else None


class LanguageItem(BaseModel):
    name = ''
    level = ''
    diploma = None

    def load(self, language_item_dict):
        self.name = language_item_dict['name']
        self.level = language_item_dict['level']
        self.diploma = LinkItem(language_item_dict['diploma']) \
            if 'diploma' in language_item_dict else None


class CourseItem(BaseModel):
    institution = ''
    name = ''
    date = None
    diploma = None

    def load(self, course_item_dict):
        self.institution = course_item_dict['institution']
        self.name = course_item_dict['name']
        self.date = datetime.datetime.strptime(
            course_item_dict['date'], '%Y-%m-%d'
        ).date()
        self.diploma = LinkItem(course_item_dict['diploma']) \
            if 'diploma' in course_item_dict else None


class ProjectItem(BaseModel):
    featured = False
    name = ''
    description = ''
    link = None

    def load(self, project_item_dict):
        self.featured = project_item_dict['featured']
        self.name = project_item_dict['name']
        self.description = project_item_dict['description'].rstrip()
        self.link = LinkItem(project_item_dict['link']) \
            if 'link' in project_item_dict else None


class SkillItem(BaseModel):
    name = ''
    type = ''
    category = ''
    score = -1

    def load(self, skill_item_dict):
        self.name = skill_item_dict['name']
        self.type = skill_item_dict[
            'type'] if 'type' in skill_item_dict else ''
        self.category = skill_item_dict[
            'category'] if 'category' in skill_item_dict else ''
        self.score = skill_item_dict[
            'score'] if 'score' in skill_item_dict else -1
