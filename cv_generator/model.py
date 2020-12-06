import datetime
import copy


class Field:
    name = None
    data_type = None
    is_list = None
    nullable = None
    value = None

    def __init__(self, name, data_type, is_list=False, nullable=True,
                 value=None):
        self.name = name
        self.data_type = data_type
        self.is_list = is_list
        self.nullable = nullable
        self.value = value

    def load(self, data):
        if self.nullable and self.name not in data or data[self.name] is None:
            self.value = None
        elif self.is_list:
            self.value = [self._load_by_type(item) for item in data[self.name]]
        else:
            self.value = self._load_by_type(data)

    def _load_by_type(self, data):
        if self.data_type == str:
            return data[self.name]
        if self.data_type == int:
            return int(data[self.name])
        if self.data_type == float:
            return float(data[self.name])
        if self.data_type == bool:
            return bool(data[self.name])
        if self.data_type == datetime.date:
            return datetime.date.fromisoformat(data[self.name])
        return self.data_type(data if self.is_list else data[self.name])

    def dump(self):
        if self.value is None:
            return None
        if self.is_list:
            return [self._dump_by_type(item) for item in self.value]
        return self._dump_by_type()

    def _dump_by_type(self, item=None):
        if self.data_type in [str, int, float, bool]:
            return self.value
        if self.data_type == datetime.date:
            return self.value.isoformat()
        return item.dump() if item is not None else self.value.dump()


class ItemBase:

    def __init__(self, data=None):
        if data is not None:
            self.load(data)

    def load(self, data):
        for attr in dir(self):
            if isinstance(getattr(self, attr), Field):
                setattr(self, attr, copy.deepcopy(getattr(self, attr)))
                getattr(self, attr).load(data)

    def get(self, *args):
        obj = self
        for arg in list(args):
            obj = getattr(obj, arg).value
        return obj

    def dump(self):
        data = {}
        for attr in dir(self):
            if isinstance(getattr(self, attr), Field):
                attr_data = getattr(self, attr).dump()
                if attr_data:
                    data[attr] = attr_data
        return data

    def __eq__(self, other):
        return self.dump() == other.dump()


class LinkItem(ItemBase):
    anchor = Field('anchor', str, nullable=False)
    href = Field('href', str, nullable=False)


class RichTextItem(ItemBase):
    type = Field('type', str, nullable=False)
    content = Field('content', str, nullable=False)


class BasicInfo(ItemBase):
    name = Field('name', str, nullable=False)
    surnames = Field('surnames', str, nullable=False)
    profession = Field('profession', str, nullable=False)
    birthday = Field('birthday', datetime.date)
    birthplace = Field('birthplace', str)
    residence = Field('residence', str)
    marital_status = Field('marital_status', str)
    biography = Field('biography', str)
    hobbies = Field('hobbies', str)


class ContactInfo(ItemBase):
    email = Field('email', str, nullable=False)
    phone = Field('phone', str, nullable=False)
    website = Field('website', LinkItem)
    twitter = Field('twitter', LinkItem)
    linkedin = Field('linkedin', LinkItem)
    github = Field('github', LinkItem)
    scholar = Field('scholar', LinkItem)


class ExperienceItem(ItemBase):
    institution = Field('institution', str, nullable=False)
    position = Field('position', str, nullable=False)
    date_start = Field('date_start', datetime.date, nullable=False)
    date_end = Field('date_end', datetime.date)
    description = Field('description', RichTextItem, is_list=True)


class EducationItem(ItemBase):
    institution = Field('institution', str, nullable=False)
    degree = Field('degree', str, nullable=False)
    major = Field('major', str)
    date_start = Field('date_start', datetime.date, nullable=False)
    date_end = Field('date_end', datetime.date)
    description = Field('description', str)
    gpa = Field('gpa', float)
    gpa_max = Field('gpa_max', float)
    performance = Field('performance', float)
    promotion_order = Field('promotion_order', str)


class AwardItem(ItemBase):
    institution = Field('institution', str, nullable=False)
    name = Field('name', str, nullable=False)
    date = Field('date', datetime.date, nullable=False)
    description = Field('description', str)
    diploma = Field('diploma', LinkItem)


class PublicationItem(ItemBase):
    title = Field('title', str, nullable=False)
    abstract = Field('abstract', str)
    authors = Field('authors', str, nullable=False)
    conference = Field('conference', str)
    date = Field('date', datetime.date, nullable=False)
    manuscript_link = Field('manuscript_link', LinkItem)
    code_link = Field('code_link', LinkItem)


class LanguageItem(ItemBase):
    name = Field('name', str, nullable=False)
    level = Field('level', str)
    diploma = Field('diploma', LinkItem)


class CourseItem(ItemBase):
    institution = Field('institution', str, nullable=False)
    name = Field('name', str, nullable=False)
    date = Field('date', datetime.date, nullable=False)
    diploma = Field('diploma', LinkItem)


class ProjectItem(ItemBase):
    featured = Field('featured', bool)
    name = Field('name', str, nullable=False)
    description = Field('description', str)
    link = Field('link', LinkItem)


class SkillItem(ItemBase):
    name = Field('name', str, nullable=False)
    type = Field('type', str)
    category = Field('category', str)
    score = Field('score', int)


class Model(ItemBase):
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
