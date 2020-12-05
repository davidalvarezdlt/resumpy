import datetime


class Field:
    name = None
    data_type = None
    is_list = None
    nullable = None
    value = None

    def __init__(self, name, data_type, is_list=False, nullable=True):
        self.name = name
        self.data_type = data_type
        self.is_list = is_list
        self.nullable = nullable

    def get(self):
        return self.value

    def load(self, data):
        if self.nullable and self.name not in data:
            self.value = None
        elif self.is_list:
            self.value = [self._load_by_type(item) for item in data[self.name]]
        else:
            self.value = self._load_by_type(data)

    def _load_by_type(self, data):
        if self.data_type == str:
            return data[self.name]
        elif self.data_type == int:
            return int(data[self.name])
        elif self.data_type == float:
            return float(data[self.name])
        elif self.data_type == bool:
            return bool(data[self.name])
        elif self.data_type == datetime.date:
            return datetime.date.fromisoformat(data[self.name])
        else:
            return self.data_type(data if self.is_list else data[self.name])

    def dump(self):
        if self.value is None:
            return None
        elif self.is_list:
            return [self._dump_by_type(item) for item in self.value]
        else:
            return self._dump_by_type()

    def _dump_by_type(self, item=None):
        if self.data_type in [str, int, float, bool]:
            return self.value
        elif self.data_type == datetime.date:
            return self.value.isoformat()
        else:
            return item.dump() if item is not None else self.value.dump()


class ItemBase:

    def __init__(self, data=None):
        if data is not None:
            self.load(data)
            self.validate()

    def load(self, data):
        for attr in dir(self):
            if isinstance(getattr(self, attr), Field):
                getattr(self, attr).load(data)

    def validate(self):
        pass

    def dump(self):
        data = {}
        for attr in dir(self):
            if isinstance(getattr(self, attr), Field):
                data[attr] = getattr(self, attr).dump()
        return data

    def __eq__(self, other):
        return self.dump() == other.dump()


class LinkItem(ItemBase):
    anchor = Field('anchor', str, nullable=False)
    href = Field('href', str, nullable=False)


class RichTextItem(ItemBase):
    anchor = Field('type', str, nullable=False)
    content = Field('content', str, nullable=False)


class BasicInfo(ItemBase):
    name = Field('name', str, nullable=False)
    surnames = Field('surnames', str, nullable=False)
    profession = Field('profession', str, nullable=False)
    birthday = Field('birthday', datetime.date, nullable=False)
    birthplace = Field('birthplace', str, nullable=False)
    residence = Field('residence', str, nullable=False)
    marital_status = Field('marital_status', str, nullable=False)
    biography = Field('biography', str, nullable=False)
    hobbies = Field('hobbies', str, nullable=False)


class ContactInfo(ItemBase):
    email = Field('email', str, nullable=False)
    phone = Field('phone', str, nullable=False)
    personal_website = Field('personal_website', LinkItem, nullable=True)
    twitter = Field('twitter', LinkItem, nullable=True)
    linkedin = Field('linkedin', LinkItem, nullable=True)
    github = Field('github', LinkItem, nullable=True)
    scholar = Field('scholar', LinkItem, nullable=True)


class ExperienceItem(ItemBase):
    institution = Field('institution', str, nullable=True)
    position = Field('position', str, nullable=True)
    date_start = Field('date_start', datetime.date, nullable=True)
    date_end = Field('date_end', datetime.date, nullable=True)
    description = Field('description', RichTextItem, is_list=True)


class EducationItem(ItemBase):
    institution = Field('institution', str, nullable=True)
    degree = Field('degree', str, nullable=True)
    major = Field('major', str, nullable=True)
    date_start = Field('date_start', datetime.date, nullable=True)
    date_end = Field('date_end', datetime.date, nullable=True)
    description = Field('description', str, nullable=True)
    gpa = Field('gpa', float, nullable=True)
    gpa_max = Field('gpa_max', float, nullable=True)
    performance = Field('performance', float, nullable=True)
    promotion_order = Field('promotion_order', str, nullable=True)


class AwardItem(ItemBase):
    institution = Field('institution', str, nullable=True)
    name = Field('name', str, nullable=True)
    date = Field('date', datetime.date, nullable=True)
    description = Field('description', str, nullable=True)
    diploma = Field('diploma', LinkItem, nullable=True)


class PublicationItem(ItemBase):
    title = Field('title', str, nullable=True)
    abstract = Field('abstract', str, nullable=True)
    authors = Field('authors', str, nullable=True)
    conference = Field('conference', str, nullable=True)
    date = Field('date', datetime.date, nullable=True)
    manuscript_link = Field('manuscript_link', LinkItem, nullable=True)
    code_link = Field('code_link', LinkItem, nullable=True)


class LanguageItem(ItemBase):
    name = Field('name', str, nullable=True)
    level = Field('level', str, nullable=True)
    diploma = Field('diploma', LinkItem, nullable=True)


class CourseItem(ItemBase):
    institution = Field('institution', str, nullable=True)
    name = Field('name', str, nullable=True)
    date = Field('date', datetime.date, nullable=True)
    diploma = Field('diploma', LinkItem, nullable=True)


class ProjectItem(ItemBase):
    featured = Field('featured', bool, nullable=True)
    name = Field('name', str, nullable=True)
    description = Field('description', str, nullable=True)
    link = Field('link', LinkItem, nullable=True)


class SkillItem(ItemBase):
    name = Field('name', str, nullable=True)
    type = Field('type', str, nullable=True)
    category = Field('category', str, nullable=True)
    score = Field('score', int, nullable=True)


class CVModel(ItemBase):
    lang = Field('lang', str, nullable=False)
    last_update = Field('last_update', datetime.date, nullable=False)
    basic = Field('basic', BasicInfo, nullable=False)
    contact = Field('contact', ContactInfo, nullable=False)
    experience = Field('experience', ExperienceItem, is_list=True)
    education = Field('education', EducationItem, is_list=True)
    awards = Field('awards', AwardItem, is_list=True)
    publications = Field('publications', PublicationItem, is_list=True)
    languages = Field('languages', LanguageItem, is_list=True)
    courses = Field('courses', CourseItem, is_list=True)
    projects = Field('projects', ProjectItem, is_list=True)
    skills = Field('skills', SkillItem, is_list=True)
