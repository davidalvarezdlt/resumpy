import pylatex
from pylatex import Command
import random
import cv_generator


class ThemeDeveloper(cv_generator.BaseTheme):
    class BarChart(pylatex.base_classes.Environment):
        _latex_name = 'barchart'

    class EntryList(pylatex.base_classes.Environment):
        _latex_name = 'entrylist'

    def __init__(self, cv, logger):
        super(ThemeDeveloper, self).__init__('developer', cv, logger)

    def format(self):
        self.set_lang()
        self._format_header()
        self._format_experience()
        self._format_education()
        self._format_awards()
        self._format_courses()
        self._format_publications()
        self._format_languages()
        self._format_hobbies()
        return self.doc

    def _format_header(self):
        self.doc.append(Command('headername', self.cv.basic.name + ' ' + self.cv.basic.surnames))
        self.doc.append(
            pylatex.base_classes.Arguments(pylatex.NoEscape('\\\\ \\huge' + ' ' + self.cv.basic.profession))
        )
        self.doc.append(pylatex.NewLine())
        with self.doc.create(pylatex.MiniPage(width='0.60\\textwidth', pos='c')):
            self.doc.append(Command('cvsect', _('DEVELOPER_BIOGRAPHY_TITLE')))
            self.doc.append(pylatex.NewLine())
            self.doc.append(self.cv.basic.biography)
            self._format_skills()
        self.doc.append(pylatex.HFill())
        with self.doc.create(pylatex.MiniPage(width='0.30\\textwidth', pos='c')):
            self.doc.append(Command('icon', ['MapMarker', 12, self.cv.basic.residence]))
            self.doc.append(pylatex.NewLine())
            self.doc.append(Command('icon', ['Phone', 12, self.cv.contact.phone]))
            self.doc.append(pylatex.NewLine())
            self.doc.append(Command('icon', ['At', 12, self.cv.contact.email]))
            if self.cv.contact.personal_website or self.cv.contact.twitter or self.cv.contact.linkedin or \
                    self.cv.contact.github:
                self.doc.append(pylatex.NewLine())
                self.doc.append(pylatex.VerticalSpace('0.25cm'))
                self.doc.append(pylatex.NewLine())
            if self.cv.contact.personal_website:
                self.doc.append(Command('icon', ['Globe', 12,
                                                 Command('href', [self.cv.contact.personal_website.href,
                                                                  self.cv.contact.personal_website.anchor])]))
                self.doc.append(pylatex.NewLine())
            if self.cv.contact.twitter:
                self.doc.append(Command('icon', ['Twitter', 12, Command('href', [self.cv.contact.twitter.href,
                                                                                 self.cv.contact.twitter.anchor])]))
                self.doc.append(pylatex.NewLine())
            if self.cv.contact.linkedin:
                self.doc.append(Command('icon', ['Linkedin', 12, Command('href', [self.cv.contact.linkedin.href,
                                                                                  self.cv.contact.linkedin.anchor])]))
                self.doc.append(pylatex.NewLine())
            if self.cv.contact.github:
                self.doc.append(Command('icon', ['Github', 12, Command('href', [self.cv.contact.github.href,
                                                                                self.cv.contact.github.anchor])]))
        self.doc.append(pylatex.VerticalSpace('0.50cm'))
        self.doc.append(pylatex.NewLine())

    def _format_skills(self):
        skills_highlighted_list = self.cv.filter_skills_by_category(None)
        if len(skills_highlighted_list) > 0:
            if len(skills_highlighted_list) > 5:
                skills_highlighted_list = random.sample(skills_highlighted_list, 5)
                self.logger.warning('There are more than 5 highligthed skills, only 5 random will be chosen.')
            bubble_skills = ['{}/{}'.format(int(skill_highlighted.score * (6 / 100)), skill_highlighted.name) for
                             skill_highlighted in skills_highlighted_list]
            self.doc.append(pylatex.position.Center(data=Command('bubbles', ', '.join(bubble_skills))))

    def _format_experience(self):
        if self.cv.experience and len(self.cv.experience) > 0:
            self.doc.append(Command('cvsect', _('DEVELOPER_EXPERIENCE_TITLE')))
            entry_list = self.EntryList()
            for experience_item in self.cv.experience:
                experience_item_date_start = experience_item.date_start.strftime('%m/%Y')
                experience_item_date_end = experience_item.date_end.strftime('%m/%Y') \
                    if experience_item.date_end is not None else _('DEVELOPER_DATES_NOW')
                experience_period = '{} - {}'.format(experience_item_date_start, experience_item_date_end)
                experience_item_args = [experience_period, experience_item.position,
                                        experience_item.institution, experience_item.description]
                entry_list.append(Command('entry', experience_item_args))
            self.doc.append(entry_list)

    def _format_education(self):
        if self.cv.education and len(self.cv.education) > 0:
            self.doc.append(Command('cvsect', _('DEVELOPER_EDUCATION_TITLE')))
            entry_list = self.EntryList()
            for education_item in self.cv.education:
                education_item_date_start = education_item.date_start.strftime('%m/%Y')
                education_item_date_end = education_item.date_end.strftime('%m/%Y') \
                    if education_item.date_end is not None else _('DEVELOPER_DATES_NOW')
                education_period = '{} - {}'.format(education_item_date_start, education_item_date_end)
                education_item_args = [
                    education_period, education_item.degree, education_item.institution, education_item.description
                ]
                entry_list.append(Command('entry', education_item_args))

            self.doc.append(entry_list)

    def _format_awards(self):
        if self.cv.awards and len(self.cv.awards) > 0:
            self.doc.append(Command('cvsect', _('DEVELOPER_AWARDS_TITLE')))
            entry_list = self.EntryList()
            for award_item in self.cv.awards:
                award_item_date = award_item.date.strftime('%B %Y')
                award_item_args = [award_item_date, award_item.name, award_item.institution, award_item.description]
                entry_list.append(Command('entry', award_item_args))
            self.doc.append(entry_list)

    def _format_publications(self):
        if self.cv.publications and len(self.cv.publications) > 0:
            self.doc.append(Command('cvsect', _('DEVELOPER_PUBLICATIONS_TITLE')))
            entry_list = self.EntryList()
            for publication_item in self.cv.publications:
                publication_item_date = publication_item.date.strftime('%B %Y')
                publication_item_args = [publication_item_date, publication_item.title, '', publication_item.abstract]
                entry_list.append(Command('entry', publication_item_args))
            self.doc.append(entry_list)

    def _format_courses(self):
        if self.cv.courses and len(self.cv.courses) > 0:
            self.doc.append(Command('cvsect', _('DEVELOPER_COURSES_TITLE')))
            entry_list = self.EntryList()
            for course_item in self.cv.courses:
                course_item_date = course_item.date.strftime('%B %Y')
                course_item_args = [course_item_date, course_item.name, course_item.institution, '']
                entry_list.append(Command('entry', course_item_args))
            self.doc.append(entry_list)

    def _format_languages(self):
        with self.doc.create(pylatex.MiniPage(width='0.5\\textwidth', pos='t')):
            self.doc.append(Command('cvsect', _('DEVELOPER_LANGUAGES_TITLE')))
            self.doc.append(pylatex.NewLine())
            for language_item in self.cv.languages:
                self.doc.append(pylatex.NoEscape('\\textbf{{{}}} - {}'.format(language_item.name, language_item.level)))
                self.doc.append(pylatex.NewLine())

    def _format_hobbies(self):
        if self.cv.basic.hobbies:
            with self.doc.create(pylatex.MiniPage(width='0.5\\textwidth', pos='t')):
                self.doc.append(Command('cvsect', _('DEVELOPER_HOBBIES_TITLE')))
                self.doc.append(pylatex.NewLine())
                self.doc.append(self.cv.basic.hobbies)
