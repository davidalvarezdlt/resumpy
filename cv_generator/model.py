import datetime


class LinkItem:
    anchor: str
    href: str

    def __init__(self, link_item_dict: dict):
        self.anchor = link_item_dict['anchor']
        self.href = link_item_dict['href']


class BasicInfo:
    name: str
    surnames: str
    location: str
    birthday: datetime.date
    profession: str
    nationality: str
    biography: str

    def __init__(self, basic_info_dict: dict):
        self.name = basic_info_dict['name']
        self.surnames = basic_info_dict['surnames']
        self.location = basic_info_dict['location']
        self.birthday = datetime.datetime.strptime(basic_info_dict['birthday'], '%d/%m/%Y').date()
        self.profession = basic_info_dict['profession']
        self.nationality = basic_info_dict['nationality']
        self.biography = basic_info_dict['biography']

    def get_age(self):
        today = datetime.date.today()
        return today.year - self.birthday.year - ((today.month, today.day) < (self.birthday.month, self.birthday.day))


class ContactInfo:
    email: str
    phone: str
    personal_website: LinkItem
    twitter: LinkItem
    linkedin: LinkItem
    github: LinkItem
    scholar: LinkItem

    def __init__(self, contact_info_dict: dict):
        self.email = contact_info_dict['email']
        self.phone = contact_info_dict['phone']
        self.personal_website = LinkItem(contact_info_dict['website']) if 'website' in contact_info_dict else None
        self.twitter = LinkItem(contact_info_dict['twitter']) if 'twitter' in contact_info_dict else None
        self.linkedin = LinkItem(contact_info_dict['linkedin']) if 'linkedin' in contact_info_dict else None
        self.github = LinkItem(contact_info_dict['github']) if 'github' in contact_info_dict else None
        self.scholar = LinkItem(contact_info_dict['scholar']) if 'scholar' in contact_info_dict else None


class ExperienceItem:
    position: str
    institution: str
    date_start: datetime.date
    date_end: datetime.date
    description: str

    def __init__(self, experience_item_dict: dict):
        self.position = experience_item_dict['position']
        self.institution = experience_item_dict['institution']
        self.date_start = datetime.datetime.strptime(experience_item_dict['date_start'], '%d/%m/%Y').date()
        self.date_end = datetime.datetime.strptime(experience_item_dict['date_end'], '%d/%m/%Y').date() \
            if 'date_end' in experience_item_dict else None
        self.description = experience_item_dict['description'].rstrip()


class ExperienceInfo:
    items: list

    def __init__(self, experience_info_dict: dict):
        self.items = [ExperienceItem(experience_item) for experience_item in experience_info_dict]


class EducationItem:
    name: str
    specialization: str
    institution: str
    date_start: datetime.date
    date_end: datetime.date
    gpa: float
    gpa_max: float
    performance: float
    description: str

    def __init__(self, education_item_dict: dict):
        self.name = education_item_dict['name']
        self.specialization = education_item_dict['specialization'] if 'specialization' in education_item_dict else None
        self.institution = education_item_dict['institution']
        self.date_start = datetime.datetime.strptime(education_item_dict['date_start'], '%d/%m/%Y').date()
        self.date_end = datetime.datetime.strptime(education_item_dict['date_end'], '%d/%m/%Y').date() \
            if 'date_end' in education_item_dict else None
        self.gpa = education_item_dict['gpa'] if 'gpa' in education_item_dict else None
        self.gpa_max = education_item_dict['gpa_max'] if 'gpa_max' in education_item_dict else None
        self.performance = education_item_dict['performance'] if 'performance' in education_item_dict else None
        self.description = education_item_dict['description'].rstrip()


class EducationInfo:
    items: list

    def __init__(self, education_info_dict: dict):
        self.items = [EducationItem(education_item) for education_item in education_info_dict]


class AwardItem:
    name: str
    institution: str
    date: datetime.date
    description: str
    link: LinkItem

    def __init__(self, award_item_dic: dict):
        self.name = award_item_dic['name']
        self.institution = award_item_dic['institution']
        self.date = datetime.datetime.strptime(award_item_dic['date'], '%d/%m/%Y').date()
        self.description = award_item_dic['description'].rstrip() if 'description' in award_item_dic else None
        self.link = LinkItem(award_item_dic['link']) if 'link' in award_item_dic else None


class AwardsInfo:
    items: list

    def __init__(self, awards_info_dict: dict):
        self.items = [AwardItem(award_item) for award_item in awards_info_dict]


class CourseItem:
    name: str
    institution: str
    date: datetime.date
    diploma: LinkItem

    def __init__(self, course_item_dict: dict):
        self.name = course_item_dict['name']
        self.institution = course_item_dict['institution']
        self.date = datetime.datetime.strptime(course_item_dict['date'], '%d/%m/%Y').date()
        self.diploma = LinkItem(course_item_dict['diploma']) if 'diploma' in course_item_dict else None


class CoursesInfo:
    items: list

    def __init__(self, courses_info_dict: dict):
        self.items = [CourseItem(course_item) for course_item in courses_info_dict]


class ProjectItem:
    name: str
    description: str
    link: LinkItem

    def __init__(self, project_item_dict: dict):
        self.name = project_item_dict['name']
        self.description = project_item_dict['description'].rstrip()
        self.link = LinkItem(project_item_dict['link']) if 'link' in project_item_dict else None


class ProjectsInfo:
    items: list

    def __init__(self, projects_info_dict: dict):
        self.items = [ProjectItem(project_item_dict) for project_item_dict in projects_info_dict]


class PublicationItem:
    title: str
    abstract: str
    date: datetime.date
    comment: str
    manuscript_link: LinkItem
    code_link: LinkItem

    def __init__(self, publication_item_dict: dict):
        self.title = publication_item_dict['title']
        self.abstract = publication_item_dict['abstract'].rstrip() if 'abstract' in publication_item_dict else None
        self.date = datetime.datetime.strptime(publication_item_dict['date'], '%d/%m/%Y').date()
        self.comment = publication_item_dict['comment'] if 'comment' in publication_item_dict else None
        self.manuscript_link = LinkItem(publication_item_dict['manuscript_link']) \
            if 'manuscript_link' in publication_item_dict else None
        self.code_link = LinkItem(publication_item_dict['code_link']) \
            if 'code_link' in publication_item_dict else None


class PublicationsInfo:
    items: list

    def __init__(self, publications_info_dict: dict):
        self.items = [PublicationItem(publication_item_dict) for publication_item_dict in publications_info_dict]


class LanguageItem:
    name: str
    level: str
    score: int

    def __init__(self, language_item_dict: dict):
        self.name = language_item_dict['name']
        self.level = language_item_dict['level']
        self.score = language_item_dict['score'] if 'score' in language_item_dict else None


class LanguagesInfo:
    items: list

    def __init__(self, languages_info_dict: dict):
        self.items = [LanguageItem(language_item_dict) for language_item_dict in languages_info_dict]


class SkillItem:
    name: str
    category: str
    score: int
    highlighted: bool

    def __init__(self, skill_item_dict: dict):
        self.name = skill_item_dict['name']
        self.category = skill_item_dict['category'] if 'category' in skill_item_dict else None
        self.score = skill_item_dict['score'] if 'score' in skill_item_dict else None
        self.highlighted = skill_item_dict['highlighted'] if 'highlighted' in skill_item_dict else None


class SkillsInfo:
    items: list

    def __init__(self, skills_info_dict: dict):
        self.items = [SkillItem(skill_item_dict) for skill_item_dict in skills_info_dict]

    def get_categories(self) -> list:
        categories_list = []
        for item in self.items:
            if item.category is not None and item.category not in categories_list:
                categories_list.append(item.category)
        return categories_list

    def filter(self, category: str = None, highlighted: bool = None) -> list:
        return [item for item in self.items if (category is None or item.category == category) and
                (highlighted is None or item.highlighted == highlighted)]


class MiscInfo:
    hobbies: str

    def __init__(self, misc_info_dict: dict):
        self.hobbies = misc_info_dict['hobbies'] if 'hobbies' in misc_info_dict else None
