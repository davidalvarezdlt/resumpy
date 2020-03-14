import cv_generator
import cv_generator.utils
import pylatex
from pylatex import Command, UnsafeCommand


class ThemeSitges(cv_generator.BaseTheme):
    class Paracol(pylatex.base_classes.Environment):
        _latex_name = 'paracol'

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

    class ProjectItem(pylatex.base_classes.Environment):
        _latex_name = 'projectitem'

    class LastUpdateItem(pylatex.base_classes.Environment):
        _latex_name = 'textblock*'
        packages = [pylatex.package.Package('textpos', options=['absolute,overlay'])]

    class MultiCommandContainer(pylatex.base_classes.Container):
        def dumps(self):
            return self.dumps_content()

    def __init__(self, cv, logger):
        super(ThemeSitges, self).__init__('sitges', cv, logger)

    def format(self):
        self.set_lang()
        self._format_last_update()
        self._format_basic()
        self.doc.append(Command('columnratio', '0.63'))
        with self.doc.create(self.Paracol(arguments=[2])):
            self._format_experience()
            self._format_eductation()
            self._format_awards()
            self._format_publications()
            self.doc.append(Command('switchcolumn'))
            self._format_info()
            self._format_languages()
            self._format_courses()
            self._format_projects()
            self._format_skills()
            self._format_hobbies()
        return self.doc

    def _format_last_update(self):
        last_update = self.cv.last_update.strftime('%B %d, %Y')
        self.doc.append(self.LastUpdateItem(
            arguments=['20.5cm'],
            data=['(0cm,0.2cm)', pylatex.position.FlushRight(data=Command('lastupdate', last_update))]
        ))

    def _format_basic(self):
        full_name = '{} {}'.format(self.cv.basic.name, self.cv.basic.surnames)
        self.doc.append(pylatex.base_classes.command.Command('name', full_name))
        self.doc.append(pylatex.base_classes.command.Command('profession', self.cv.basic.profession))
        if self.cv.contact.scholar:
            self.doc.append(Command('scholar', [self.cv.contact.scholar.href, self.cv.contact.scholar.anchor]))
        if self.cv.contact.github:
            self.doc.append(Command('github', [self.cv.contact.github.href, self.cv.contact.github.anchor]))
        if self.cv.contact.linkedin:
            self.doc.append(Command('linkedin', [self.cv.contact.linkedin.href, self.cv.contact.linkedin.anchor]))
        if self.cv.contact.twitter:
            self.doc.append(Command('twitter', [self.cv.contact.twitter.href, self.cv.contact.twitter.anchor]))
        if self.cv.contact.personal_website:
            self.doc.append(
                Command('website', [self.cv.contact.personal_website.href, self.cv.contact.personal_website.anchor]))
        self.doc.append(pylatex.base_classes.command.Command('cvheader', '9th of January of 2020'))

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

    def _format_experience_subtitle(self, experience_item):
        container = self.MultiCommandContainer()
        container.append(experience_item.date_start.strftime('%B %Y'))
        container.append(pylatex.NoEscape('\\,-\\,'))
        if experience_item.date_end:
            experience_time = round((experience_item.date_end - experience_item.date_start).days / 30)
            container.append(experience_item.date_end.strftime('%B %Y'))
            container.append(pylatex.NoEscape('\\,'))
            container.append('({} months)'.format(experience_time))
        else:
            container.append(_('SITGES_DATES_NOW'))
        return container

    def _format_eductation(self):
        if self.cv.education and len(self.cv.education.items) > 0:
            self.doc.append(pylatex.base_classes.command.Command('cvsection', _('SITGES_EDUCATION_TITLE')))
            for i, education_item in enumerate(self.cv.education.items):
                education_item_date_start = education_item.date_start.strftime('%B %Y')
                education_item_date_end = education_item.date_end.strftime('%B %Y') \
                    if education_item.date_end is not None else _('DEVELOPER_DATES_NOW')
                education_period = '{} - {}'.format(education_item_date_start, education_item_date_end)
                education_subtitle = self._format_education_subtitle(education_item)
                self.doc.append(
                    self.EducationItem(
                        arguments=[education_item.institution, education_period, education_item.name,
                                   education_subtitle],
                        data=education_item.description
                    )
                )
                self.doc.append(Command('bigskip'))

    def _format_education_subtitle(self, education_item):
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

    def _format_award_subtitle(self, award_item):
        container = self.MultiCommandContainer()
        container.append(award_item.date.strftime('%B %Y'))
        container.append(Command('quad'))
        container.append('|')
        container.append(Command('quad'))
        container.append(award_item.institution)
        if award_item.link is not None:
            href_escaped = cv_generator.utils.escape_link(award_item.link.href)
            anchor_escaped = pylatex.utils.escape_latex(award_item.link.anchor)
            container.append(Command('quad'))
            container.append(pylatex.NoEscape('\\,|\\,'))
            container.append(Command('quad'))
            container.append(Command('texttt', UnsafeCommand('href', [href_escaped, anchor_escaped])))
        return container

    def _format_publications(self):
        if self.cv.publications and len(self.cv.publications.items) > 0:
            self.doc.append(pylatex.base_classes.command.Command('cvsection', _('SITGES_PUBLICATIONS_TITLE')))
            for i, publication_item in enumerate(self.cv.publications.items):
                publication_comment = self._format_publication_subtitle(publication_item)
                self.doc.append(
                    self.PublicationItem(
                        arguments=[publication_item.title, publication_item.date.strftime('%B %Y'),
                                   publication_comment],
                        data=publication_item.abstract
                    )
                )
                self.doc.append(Command('bigskip'))

    def _format_publication_subtitle(self, publication_item):
        container = self.MultiCommandContainer()
        if publication_item.comment:
            container.append(publication_item.comment)
        if publication_item.manuscript_link:
            if len(container) > 0:
                container.append(Command('quad'))
                container.append(pylatex.NoEscape('\\,|\\,'))
                container.append(Command('quad'))
            href_escaped = cv_generator.utils.escape_link(publication_item.manuscript_link.href)
            anchor_escaped = pylatex.utils.escape_latex(publication_item.manuscript_link.anchor)
            container.append(Command('texttt', UnsafeCommand('href', [href_escaped, anchor_escaped])))
        if publication_item.code_link:
            if len(container) > 0:
                container.append(Command('quad'))
                container.append(pylatex.NoEscape('\\,|\\,'))
                container.append(Command('quad'))
            href_escaped = cv_generator.utils.escape_link(publication_item.code_link.href)
            anchor_escaped = pylatex.utils.escape_latex(publication_item.code_link.anchor)
            container.append(Command('texttt', UnsafeCommand('href', [href_escaped, anchor_escaped])))
        return container

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
                href_escaped = cv_generator.utils.escape_link(courses_item.diploma.href)
                anchor_escaped = pylatex.utils.escape_latex(courses_item.diploma.anchor)
                course_diploma = UnsafeCommand('href', [href_escaped, anchor_escaped])
                self.doc.append(
                    Command('courseitem', [courses_item.name, courses_item.institution, course_diploma])
                )
                if i < len(self.cv.languages.items) - 1:
                    self.doc.append(Command('medskip'))

    def _format_projects(self):
        if self.cv.projects and len(self.cv.projects.items) > 0:
            self.doc.append(Command('cvsidebarsection', _('SITGES_PROJECTS_TITLE')))
            for i, project_item in enumerate(self.cv.projects.items):
                project_subtitle = self._format_project_subtitle(project_item)
                project_item = Command('projectitem', [project_item.name, project_subtitle, project_item.description])
                self.doc.append(project_item)
                self.doc.append(Command('bigskip'))

    def _format_project_subtitle(self, project_item):
        container = self.MultiCommandContainer()
        href_escaped = cv_generator.utils.escape_link(project_item.link.href)
        anchor_escaped = pylatex.utils.escape_latex(project_item.link.anchor)
        container.append(Command('texttt', UnsafeCommand('href', [href_escaped, anchor_escaped])))
        return container

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
