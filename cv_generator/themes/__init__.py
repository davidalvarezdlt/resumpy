import cv_generator
import gettext
import logging
import os
import pylatex
from pylatex import Command
import random


class BaseTheme:
    theme_name: str
    cv: cv_generator.CV
    doc: pylatex.Document

    logger: logging.Logger

    def __init__(self, theme_name: str, cv: cv_generator.CV, logger: logging.Logger):
        self.theme_name = theme_name
        self.cv = cv
        self.logger = logger
        self.doc = pylatex.Document(documentclass=self.theme_name)

    def set_lang(self):
        """Sets the language of the CV.

        Uses the `self.cv.lang` attribute to set the language of the generated file. This parameter only affects to the
        fixed texts of the theme, such as category titles. In order to translate the template to another language,
        let's say Russian, create a new .po (and compiled .mo) inside:

        ./locale/ru/LC_MESSAGES/base.po

        Notice that this file already contains translation items. In order not to break previous translations,
        use the commands `xgettext` (to generate a new base.pot file) and `msgmerge` to merge with the current ones.

        For example, being inside the folder 'cv_generator/themes`, run the following command on the terminal:

        ```
            xgettext -d base -o locales/base.pot __init__.py
        ```

        This will generate a new `base.pot` file inside `./locale` with all the strings contained inside the _(
        'MY_TRANSLATION_TEXT_ID') funciton. Then, mix with the current one using:

        ```
            msgmerge --update locales/en/LC_MESSAGES/base.po locales/base.pot
        ```

        This will update the `locales/en/LC_MESSAGES/base.po` with the new translation fields. Now, you can edit the
        translation file using an editor such as Poedit.
       """
        localedir = os.path.dirname(__file__) + os.sep + 'locale'
        gettext.translation('base', localedir=localedir, languages=[self.cv.lang]).install()

    def get_cls_path(self):
        """Returns full path to `.cls` file of the theme.

        Returns:
            cls_path (str): absolute path to the `.cls` file of the current theme.
        """
        basepath = os.path.dirname(__file__)
        return basepath + os.sep + 'cls' + os.sep + self.theme_name + '.cls'

    def format(self) -> pylatex.Document:
        """Creates a new `pylatex.Document`.

        Uses the data stored inside `self.cv` to generate a new document. This method must be implemented by any
        individual theme.

        Returns:
            doc (pylatex.Document): document to be stored in disk.
        """
        raise NotImplemented


class ThemeSitges(BaseTheme):
    class ExperienceItem(pylatex.base_classes.Environment):
        _latex_name = 'experienceitem'

    class EducationItem(pylatex.base_classes.Environment):
        _latex_name = 'educationitem'

    class AwardItem(pylatex.base_classes.Environment):
        _latex_name = 'awarditem'

    class LanguageItem(pylatex.base_classes.Environment):
        _latex_name = 'languageitem'

    class PublicationItem(pylatex.base_classes.Environment):
        _latex_name = 'publicationitem'

    class MultiCommandContainer(pylatex.base_classes.Container):
        def dumps(self):
            return self.dumps_content()

    def __init__(self, cv: cv_generator.CV, logger: logging.Logger):
        super(ThemeSitges, self).__init__('sitges', cv, logger)

    def format(self) -> pylatex.Document:
        self.set_lang()
        self._format_basic()
        with self.doc.create(pylatex.MiniPage(width=r"0.62\textwidth", pos='t')):
            self._format_experience()
            self._format_eductation()
            self._format_awards()
            self._format_publications()
        self.doc.append(pylatex.HFill())
        with self.doc.create(pylatex.MiniPage(width=r"0.32\textwidth", pos='t')):
            self._format_info()
            self._format_languages()
            self._format_courses()
            self._format_skills()
            self._format_hobbies()
        return self.doc

    def _format_basic(self):
        full_name = '{} {}'.format(self.cv.basic.name, self.cv.basic.surnames)
        self.doc.append(pylatex.base_classes.command.Command('name', full_name))
        self.doc.append(pylatex.base_classes.command.Command('profession', self.cv.basic.profession))
        if self.cv.contact.github:
            self.doc.append(Command('github', [self.cv.contact.github.href, self.cv.contact.github.anchor]))
        if self.cv.contact.linkedin:
            self.doc.append(Command('linkedin', [self.cv.contact.linkedin.href, self.cv.contact.linkedin.anchor]))
        if self.cv.contact.twitter:
            self.doc.append(Command('twitter', [self.cv.contact.twitter.href, self.cv.contact.twitter.anchor]))
        if self.cv.contact.personal_website:
            self.doc.append(
                Command('website', [self.cv.contact.personal_website.href, self.cv.contact.personal_website.anchor]))
        self.doc.append(pylatex.base_classes.command.Command('cvheader'))

    def _format_experience_subtitle(self, experience_item: ExperienceItem):
        container = self.MultiCommandContainer()
        container.append(experience_item.date_start.strftime('%B %Y'))
        container.append(pylatex.NoEscape('\\,-\\,'))
        if experience_item.date_end:
            container.append(experience_item.date_end.strftime('%B %Y'))
        else:
            container.append(_('SITGES_DATES_NOW'))
        return container

    def _format_experience(self):
        if self.cv.experience and len(self.cv.experience.items) > 0:
            self.doc.append(pylatex.base_classes.command.Command('cvsection', _('SITGES_EXPERIENCE_TITLE')))
            for experience_item in self.cv.experience.items:
                experience_subtitle = self._format_experience_subtitle(experience_item)
                self.doc.append(
                    self.ExperienceItem(
                        arguments=[experience_item.position, experience_item.institution, experience_subtitle],
                        data=experience_item.description
                    )
                )
                self.doc.append(Command('bigskip'))

    def _format_education_subtitle(self, education_item: EducationItem):
        container = self.MultiCommandContainer()
        if education_item.specialization is not None:
            container.append(Command('textbf', education_item.specialization))
        if education_item.gpa is not None:
            if len(container) > 0:
                container.append(Command('quad'))
                container.append('|')
                container.append(Command('quad'))
            container.append(Command('textbf', _('SITGES_GPA_LABEL')))
            container.append(pylatex.NoEscape(':\\,'))
            container.append(education_item.gpa)
        if education_item.gpa_max is not None:
            container.append(pylatex.NoEscape('\\,/\\,'))
            container.append(education_item.gpa_max)
        if education_item.performance is not None:
            if len(container) > 0:
                container.append(Command('quad'))
                container.append('|')
                container.append(Command('quad'))
            container.append(Command('textbf', _('SITGES_PERFORMANCE_LABEL')))
            container.append(pylatex.NoEscape(':\\,{}\\%'.format(education_item.performance)))
        return container

    def _format_eductation(self):
        if self.cv.education and len(self.cv.education.items) > 0:
            self.doc.append(pylatex.base_classes.command.Command('cvsection', _('SITGES_EDUCATION_TITLE')))
            for i, education_item in enumerate(self.cv.education.items):
                education_subtitle = self._format_education_subtitle(education_item)
                self.doc.append(
                    self.EducationItem(
                        arguments=[education_item.institution, education_item.name, education_subtitle],
                        data=education_item.description
                    )
                )
                self.doc.append(Command('bigskip'))

    def _format_award_subtitle(self, award_item: AwardItem):
        container = self.MultiCommandContainer()
        container.append(award_item.date.strftime('%B %Y'))
        container.append(Command('quad'))
        container.append('|')
        container.append(Command('quad'))
        container.append(award_item.institution)
        return container

    def _format_awards(self):
        if self.cv.awards and len(self.cv.awards.items) > 0:
            self.doc.append(pylatex.base_classes.command.Command('cvsection', _('SITGES_AWARDS_TITLE')))
            for i, awards_item in enumerate(self.cv.awards.items):
                award_subtitle = self._format_award_subtitle(awards_item)
                self.doc.append(
                    self.AwardItem(
                        arguments=[awards_item.name, award_subtitle],
                        data=awards_item.description
                    )
                )
                self.doc.append(Command('bigskip'))

    def _format_publication_subtitle(self, publication_item: PublicationItem):
        container = self.MultiCommandContainer()
        if publication_item.comment:
            container.append(publication_item.comment)
        if publication_item.manuscript_link:
            if len(container) > 0:
                container.append(Command('quad'))
                container.append(pylatex.NoEscape('\\,|\\,'))
                container.append(Command('quad'))
            container.append(Command('texttt', Command('href', [publication_item.manuscript_link.href,
                                                                publication_item.manuscript_link.anchor])))
        if publication_item.code_link:
            if len(container) > 0:
                container.append(Command('quad'))
                container.append(pylatex.NoEscape('\\,|\\,'))
                container.append(Command('quad'))
            container.append(Command('texttt', Command('href', [publication_item.code_link.href,
                                                                publication_item.code_link.anchor])))
        return container

    def _format_publications(self):
        if self.cv.publications and len(self.cv.publications.items) > 0:
            self.doc.append(pylatex.base_classes.command.Command('cvsection', _('SITGES_PUBLICATIONS_TITLE')))
            for i, publication_item in enumerate(self.cv.publications.items):
                publication_comment = self._format_publication_subtitle(publication_item)
                self.doc.append(
                    self.PublicationItem(
                        arguments=[publication_item.title, publication_item.date.strftime('%B %Y'), publication_comment],
                        data=publication_item.abstract
                    )
                )

    def _format_info(self):
        self.doc.append(Command('cvsidebarsection', ''))
        self.doc.append(Command('detailitem', ['\\faFlag', _('SITGES_LOCATION_LABEL'), self.cv.basic.location]))
        self.doc.append(Command('detailitem', ['\\faCalendar', _('SITGES_AGE_LABEL'), self.cv.basic.get_age()]))
        self.doc.append(Command('detailitem', ['\\faGlobe', _('SITGES_NATIONALITY_LABEL'), self.cv.basic.nationality]))
        self.doc.append(Command('detailitem', ['\\faEnvelope', _('SITGES_EMAIL_LABEL'), self.cv.contact.email]))
        self.doc.append(Command('detailitem', ['\\faPhone', _('SITGES_PHONE_LABEL'), self.cv.contact.phone]))

    def _format_languages(self):
        self.doc.append(Command('cvsidebarsection', _('SITGES_LANGUAGES_TITLE')))
        for i, languages_item in enumerate(self.cv.languages.items):
            self.doc.append(
                Command('languageitem', [languages_item.name, languages_item.level, languages_item.score])
            )
            if i < len(self.cv.languages.items) - 1:
                self.doc.append(Command('medskip'))

    def _format_courses(self):
        if self.cv.courses and len(self.cv.courses.items) > 0:
            self.doc.append(Command('cvsidebarsection', _('SITGES_COURSES_TITLE')))
            for i, courses_item in enumerate(self.cv.courses.items):
                course_diploma = Command('href', [courses_item.diploma.href, courses_item.diploma.anchor])
                self.doc.append(
                    Command('courseitem', [courses_item.name, courses_item.institution, course_diploma])
                )
                if i < len(self.cv.languages.items) - 1:
                    self.doc.append(Command('medskip'))

    def _format_skills(self):
        self.doc.append(Command('cvsidebarsection', _('SITGES_SKILLS_TITLE')))
        skills_categories = self.cv.skills.get_categories()
        for i, (skills_category) in enumerate(skills_categories):
            skills_items = self.cv.skills.filter(category=skills_category)
            skills_str = ', '.join([skill_item.name for skill_item in skills_items])
            self.doc.append(Command('skillset', [skills_category, skills_str]))
            if i < len(self.cv.skills.items) - 1:
                self.doc.append(Command('medskip'))

    def _format_hobbies(self):
        if self.cv.misc.hobbies:
            self.doc.append(Command('cvsidebarsection', _('SITGES_HOBBIES_TITLE')))
            self.doc.append(Command('footnotesize', self.cv.misc.hobbies))


class ThemeDeveloper(BaseTheme):
    class BarChart(pylatex.base_classes.Environment):
        _latex_name = 'barchart'

    class EntryList(pylatex.base_classes.Environment):
        _latex_name = 'entrylist'

    def __init__(self, cv: cv_generator.CV, logger: logging.Logger):
        super(ThemeDeveloper, self).__init__('developer', cv, logger)

    def format(self) -> pylatex.Document:
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

    def _format_skills(self):
        skills_highlighted_list = self.cv.skills.filter(highlighted=True)
        if len(skills_highlighted_list) > 0:
            if len(skills_highlighted_list) > 5:
                skills_highlighted_list = random.sample(skills_highlighted_list, 5)
                self.logger.warning('There are more than 5 highligthed skills, only 5 random will be chosen.')
            bubble_skills = ['{}/{}'.format(int(skill_highlighted.score * (6 / 100)), skill_highlighted.name) for
                             skill_highlighted in skills_highlighted_list]
            self.doc.append(pylatex.position.Center(data=Command('bubbles', ', '.join(bubble_skills))))

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
            self.doc.append(Command('icon', ['MapMarker', 12, self.cv.basic.location]))
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
                self.doc.append(Command('icon', ['Globe', 12, Command('href',
                                                                      [self.cv.contact.personal_website.href,
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

    def _format_experience(self):
        if self.cv.experience and len(self.cv.experience.items) > 0:
            self.doc.append(Command('cvsect', _('DEVELOPER_EXPERIENCE_TITLE')))
            entry_list = self.EntryList()
            for experience_item in self.cv.experience.items:
                experience_item_date_start = experience_item.date_start.strftime('%m/%Y')
                experience_item_date_end = experience_item.date_end.strftime('%m/%Y') \
                    if experience_item.date_end is not None else _('DEVELOPER_DATES_NOW')
                experience_period = '{} - {}'.format(experience_item_date_start, experience_item_date_end)
                experience_item_args = [experience_period, experience_item.position,
                                        experience_item.institution, experience_item.description]
                entry_list.append(Command('entry', experience_item_args))
            self.doc.append(entry_list)

    def _format_education(self):
        if self.cv.education and len(self.cv.education.items) > 0:
            self.doc.append(Command('cvsect', _('DEVELOPER_EDUCATION_TITLE')))
            entry_list = self.EntryList()
            for education_item in self.cv.education.items:
                education_item_date_start = education_item.date_start.strftime('%m/%Y')
                education_item_date_end = education_item.date_end.strftime('%m/%Y') \
                    if education_item.date_end is not None else _('DEVELOPER_DATES_NOW')
                education_period = '{} - {}'.format(education_item_date_start, education_item_date_end)
                education_item_args = [education_period, education_item.name, education_item.institution,
                                       education_item.description]
                entry_list.append(Command('entry', education_item_args))
            self.doc.append(entry_list)

    def _format_awards(self):
        if self.cv.awards and len(self.cv.awards.items) > 0:
            self.doc.append(Command('cvsect', _('DEVELOPER_AWARDS_TITLE')))
            entry_list = self.EntryList()
            for award_item in self.cv.awards.items:
                award_item_date = award_item.date.strftime('%B %Y')
                award_item_args = [award_item_date, award_item.name, award_item.institution, award_item.description]
                entry_list.append(Command('entry', award_item_args))
            self.doc.append(entry_list)

    def _format_publications(self):
        if self.cv.publications and len(self.cv.publications.items) > 0:
            self.doc.append(Command('cvsect', _('DEVELOPER_PUBLICATIONS_TITLE')))
            entry_list = self.EntryList()
            for publication_item in self.cv.publications.items:
                publication_item_date = publication_item.date.strftime('%B %Y')
                publication_item_args = [publication_item_date, publication_item.title, '', publication_item.abstract]
                entry_list.append(Command('entry', publication_item_args))
            self.doc.append(entry_list)

    def _format_courses(self):
        if self.cv.courses and len(self.cv.courses.items) > 0:
            self.doc.append(Command('cvsect', _('DEVELOPER_COURSES_TITLE')))
            entry_list = self.EntryList()
            for course_item in self.cv.courses.items:
                course_item_date = course_item.date.strftime('%B %Y')
                course_item_args = [course_item_date, course_item.name, course_item.institution, '']
                entry_list.append(Command('entry', course_item_args))
            self.doc.append(entry_list)

    def _format_languages(self):
        with self.doc.create(pylatex.MiniPage(width='0.5\\textwidth', pos='t')):
            self.doc.append(Command('cvsect', _('DEVELOPER_LANGUAGES_TITLE')))
            self.doc.append(pylatex.NewLine())
            for language_item in self.cv.languages.items:
                self.doc.append(pylatex.NoEscape('\\textbf{{{}}} - {}'.format(language_item.name, language_item.level)))
                self.doc.append(pylatex.NewLine())

    def _format_hobbies(self):
        if self.cv.misc.hobbies:
            with self.doc.create(pylatex.MiniPage(width='0.5\\textwidth', pos='t')):
                self.doc.append(Command('cvsect', _('DEVELOPER_HOBBIES_TITLE')))
                self.doc.append(pylatex.NewLine())
                self.doc.append(self.cv.misc.hobbies)
