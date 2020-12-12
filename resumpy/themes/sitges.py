import resumpy
import resumpy.theme
import resumpy.utils
import gettext
import pylatex
import pylatex.lists
from pylatex import Command, UnsafeCommand


class ThemeSitges(resumpy.theme.Theme):
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
        packages = [
            pylatex.package.Package('textpos', options=['absolute,overlay'])
        ]

    class MultiCommandContainer(pylatex.base_classes.Container):
        def dumps(self):
            return self.dumps_content()

    def __init__(self, logger):
        super(ThemeSitges, self).__init__('sitges', logger)

    def format(self, model):
        self.set_lang(model)
        doc = pylatex.Document(documentclass=self.theme_name)
        doc += self._format_last_update(model)
        doc += self._format_basic(model)
        doc.append(Command('columnratio', '0.63'))
        with doc.create(self.Paracol(arguments=[2])):
            if model.get('experience'):
                doc += self._format_experience(model)
            if model.get('education'):
                doc += self._format_education(model)
            if model.get('publications'):
                doc += self._format_publications(model)
            if model.get('awards'):
                doc += self._format_awards(model)
            doc.append(Command('switchcolumn'))
            doc += self._format_info(model)
            if model.get('languages'):
                doc += self._format_languages(model)
            if model.get('courses'):
                doc += self._format_courses(model)
            if model.get('skills'):
                doc += self._format_skills(model)
            if model.get('projects'):
                doc += self._format_projects(model)
            if model.get('basic', 'hobbies'):
                doc += self._format_hobbies(model)
        return doc

    def _format_last_update(self, model):
        last_update = gettext.gettext('SITGES_LAST_UPDATE_LABEL') + ' ' + \
                      model.get('last_update').strftime('%B %Y')
        return [self.LastUpdateItem(
            arguments=['20.5cm'],
            data=['(0cm,0.2cm)', pylatex.position.FlushRight(
                data=Command('lastupdate', last_update)
            )]
        )]

    def _format_basic(self, model):
        basic_items = [
            Command('name', model.get('basic', 'name') + ' ' + model.get(
                'basic', 'surnames')
                    ),
            Command('profession', model.get('basic', 'profession'))
        ]
        for link in ['scholar', 'github', 'linkedin', 'twitter', 'website']:
            if model.get('contact', link):
                basic_items.append(Command(link, [
                    model.get('contact', link, 'href'),
                    model.get('contact', link, 'anchor')
                ]))
        return basic_items

    def _format_experience(self, model):
        experience_items = [Command(
            'cvsection', gettext.gettext('SITGES_EXPERIENCE_TITLE')
        )]
        for experience_item in model.get('experience'):
            experience_subtitle = '{} - {}'.format(
                experience_item.get('date_start').strftime('%B %Y'),
                experience_item.get('date_end').strftime('%B %Y')
                if experience_item.get('date_end')
                else gettext.gettext('SITGES_DATES_NOW')
            )
            experience_items.append(
                self.ExperienceItem(
                    arguments=[
                        experience_item.get('position'),
                        experience_item.get('institution'),
                        experience_subtitle
                    ],
                    data=self._format_rich_text(
                        experience_item.get('description')
                    )
                )
            )
            experience_items.append(Command('bigskip'))
        return experience_items

    def _format_education(self, model):
        education_items = [Command(
            'cvsection', gettext.gettext('SITGES_EDUCATION_TITLE')
        )]
        for education_item in model.get('education'):
            education_period = '{} - {}'.format(
                education_item.get('date_start').strftime('%B %Y'),
                education_item.get('date_end').strftime('%B %Y')
                if education_item.get('date_end')
                else gettext.gettext('SITGES_DATES_NOW')
            )
            education_subtitle = self.MultiCommandContainer()
            if education_item.get('major'):
                education_subtitle.append(
                    Command('textbf', education_item.get('major'))
                )
            if education_item.get('gpa'):
                if len(education_subtitle) > 0:
                    education_subtitle.append(Command('quad'))
                    education_subtitle.append('|')
                    education_subtitle.append(Command('quad'))
                education_subtitle.append(
                    Command('textbf', gettext.gettext('SITGES_GPA_LABEL'))
                )
                education_subtitle.append(pylatex.NoEscape(':\\,'))
                education_subtitle.append(education_item.get('gpa'))
            if education_item.get('gpa_max'):
                education_subtitle.append(pylatex.NoEscape('\\,/\\,'))
                education_subtitle.append(education_item.get('gpa_max'))
            if education_item.get('performance'):
                if len(education_subtitle) > 0:
                    education_subtitle.append(Command('quad'))
                    education_subtitle.append('|')
                    education_subtitle.append(Command('quad'))
                education_subtitle.append(Command(
                    'textbf', gettext.gettext('SITGES_PERFORMANCE_LABEL')
                ))
                education_subtitle.append(pylatex.NoEscape(
                    ':\\,{}\\%'.format(education_item.get('performance'))
                ))
            education_items.append(self.EducationItem(
                arguments=[
                    education_item.get('institution'),
                    education_period,
                    education_item.get('degree'),
                    education_subtitle
                ],
                data=self._format_rich_text(education_item.get('description'))
            ))
            education_items.append(Command('bigskip'))
        return education_items

    def _format_publications(self, model):
        publications_items = [Command(
            'cvsection', gettext.gettext('SITGES_PUBLICATIONS_TITLE')
        )]
        for publication_item in model.get('publications'):
            publication_subtitle = self.MultiCommandContainer()
            if publication_item.get('authors'):
                publication_subtitle.append(publication_item.get('authors'))
            for link_id in ['manuscript_link', 'code_link']:
                if publication_item.get(link_id):
                    if len(publication_subtitle) > 0:
                        publication_subtitle.append(Command('quad'))
                        publication_subtitle.append(
                            pylatex.NoEscape('\\,|\\,')
                        )
                        publication_subtitle.append(Command('quad'))
                    publication_subtitle.append(
                        Command('texttt', UnsafeCommand('href', [
                            resumpy.utils.escape_link(
                                publication_item.get(link_id, 'href')
                            ),
                            pylatex.utils.escape_latex(
                                publication_item.get(link_id, 'anchor')
                            )
                        ]))
                    )
            publications_items.append(self.PublicationItem(
                arguments=[
                    publication_item.get('title'),
                    publication_item.get('date').strftime('%B %Y'),
                    publication_item.get('conference'),
                    publication_subtitle
                ]
            ))
        return publications_items

    def _format_awards(self, model):
        awards_items = [Command(
            'cvsection', gettext.gettext('SITGES_AWARDS_TITLE')
        )]
        for award_item in model.get('awards'):
            award_subtitle = self.MultiCommandContainer()
            award_subtitle.append(award_item.get('date').strftime('%B %Y'))
            award_subtitle.append(Command('quad'))
            award_subtitle.append('|')
            award_subtitle.append(Command('quad'))
            award_subtitle.append(award_item.get('institution'))
            if award_item.get('diploma') is not None:
                award_subtitle.append(Command('quad'))
                award_subtitle.append(pylatex.NoEscape('\\,|\\,'))
                award_subtitle.append(Command('quad'))
                award_subtitle.append(Command('texttt', UnsafeCommand('href', [
                    resumpy.utils.escape_link(
                        award_item.get('diploma', 'href')
                    ),
                    pylatex.utils.escape_latex(
                        award_item.get('diploma', 'anchor')
                    )
                ])))
            awards_items.append(
                self.AwardItem(
                    arguments=[award_item.get('name'), award_subtitle],
                    data=award_item.get('description')
                )
            )
            awards_items.append(Command('bigskip'))
        return awards_items

    def _format_info(self, model):
        info_items = [
            Command('cvsidebarsection', ''),
            Command('detailitem', [
                '\\faEnvelope',
                gettext.gettext('SITGES_EMAIL_LABEL'),
                model.get('contact', 'email')
            ]),
            Command('detailitem', [
                '\\faPhone',
                gettext.gettext('SITGES_PHONE_LABEL'),
                model.get('contact', 'phone')
            ])
        ]
        if model.get('basic', 'birthday'):
            info_items.append(Command('detailitem', [
                '\\faCalendar',
                gettext.gettext('SITGES_AGE_LABEL'),
                resumpy.utils.get_age(model.get('basic', 'birthday'))
            ]))
        if model.get('basic', 'birthplace'):
            info_items.append(Command('detailitem', [
                '\\faGlobe',
                gettext.gettext('SITGES_NATIONALITY_LABEL'),
                model.get('basic', 'birthplace')
            ]))
        if model.get('basic', 'residence'):
            info_items.append(Command('detailitem', [
                '\\faFlag',
                gettext.gettext('SITGES_LOCATION_LABEL'),
                model.get('basic', 'residence')
            ]))
        return info_items

    def _format_languages(self, model):
        languages_items = [Command(
            'cvsidebarsection', gettext.gettext('SITGES_LANGUAGES_TITLE')
        )]
        for i, languages_item in enumerate(model.get('languages')):
            languages_items.append(Command('languageitem', [
                languages_item.get('name'),
                languages_item.get('level'),
                resumpy.utils.get_language_score(
                    languages_item.get('level')
                ) / 100
            ]))
            if i < len(model.get('languages')) - 1:
                languages_items.append(Command('medskip'))
        return languages_items

    def _format_courses(self, model):
        courses_items = [Command(
            'cvsidebarsection', gettext.gettext('SITGES_COURSES_TITLE')
        )]
        for i, courses_item in enumerate(model.get('courses')):
            diploma_link = UnsafeCommand('href', [
                resumpy.utils.escape_link(
                    courses_item.get('diploma', 'href')
                ),
                pylatex.utils.escape_latex(
                    courses_item.get('diploma', 'anchor')
                )
            ]) if courses_item.get('diploma') else ''
            courses_items.append(Command('courseitem', [
                courses_item.get('name'),
                courses_item.get('institution'),
                diploma_link
            ]))
            if i < len(model.get('languages')) - 1:
                courses_items.append(Command('medskip'))
        return courses_items

    def _format_skills(self, model):
        skills_items = [Command(
            'cvsidebarsection', gettext.gettext('SITGES_SKILLS_TITLE')
        )]
        for i, skills_category in enumerate(
                resumpy.utils.get_skills_categories(model.get('skills'))
        ):
            skills_filtered = resumpy.utils.filter_skills_by_category(
                model.get('skills'), skills_category
            )
            skills_str = ', '.join([s.get('name') for s in skills_filtered])
            skills_items.append(
                Command('skillset', [skills_category, skills_str])
            )
            if i < len(model.get('skills')) - 1:
                skills_items.append(Command('medskip'))
        return skills_items

    def _format_projects(self, model):
        projects_items = [Command(
            'cvsidebarsection', gettext.gettext('SITGES_PROJECTS_TITLE')
        )]
        for i, project_item in enumerate(model.get('projects')):
            project_link = UnsafeCommand('href', [
                resumpy.utils.escape_link(
                    project_item.get('link', 'href')
                ),
                pylatex.utils.escape_latex(
                    project_item.get('link', 'anchor')
                )
            ]) if project_item.get('link') else ''
            project_item = Command('projectitem', [
                project_item.get('name'),
                project_link,
                project_item.get('description')
            ])
            projects_items += [project_item, Command('bigskip')]
        return projects_items

    def _format_hobbies(self, model):
        return [
            Command(
                'cvsidebarsection', gettext.gettext('SITGES_HOBBIES_TITLE')
            ),
            Command('footnotesize', model.get('basic', 'hobbies'))
        ]

    def _format_rich_text(self, rich_text_items):
        container = self.MultiCommandContainer()
        if rich_text_items is None:
            return container
        for item in rich_text_items:
            if item.get('type') == 'paragraph':
                container.append(item.get('content'))
            elif item.get('type') == 'itemize':
                itemize = pylatex.lists.Itemize()
                for itemize_item in item.get('content'):
                    itemize.add_item(itemize_item)
                container.append(itemize)
        return container
