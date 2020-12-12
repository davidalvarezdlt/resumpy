import gettext
import os


class Theme:
    theme_name = None
    logger = None
    doc = None

    def __init__(self, theme_name, logger):
        self.theme_name = theme_name
        self.logger = logger

    def set_lang(self, model):
        """Sets the language of the CV.

        Uses the `self.cv.lang` attribute to set the language of the generated
        file. This parameter only affects static labels of the theme, such as
        category titles. In order to translate a theme into another language,
        use Poedit to create its .po and .mo files inside:

        ./locale/<lang_code>/LC_MESSAGES/<theme_name>.po

        You can generate the translation base file <theme_name>.pot by calling:
        ```
            xgettext -o resumpy/themes/locale/<theme_name>.pot
            resumpy/themes/<theme_name>.py
        ```
       """
        os.environ['LANGUAGE'] = model.get('lang')
        localedir = os.path.join(os.path.dirname(__file__), 'themes/locale')
        gettext.bindtextdomain(self.theme_name, localedir)
        gettext.textdomain(self.theme_name)

    def format(self, model):
        """Creates a new `pylatex.Document`.

        Uses the data stored inside `model` to generate a new document using
        the current theme. This method must be implemented by the different
        individual themes

        Returns:
            pylatex.Document: document object that can be converted into a PDF.
        """
        raise NotImplementedError

    @staticmethod
    def create_theme_by_name(theme_name, logger):
        """Returns a theme object given its name.

        Args:
            theme_name (str): name of the theme.
            logger (logging.Logger): logger used inside the theme.

        Returns:
            resumpy.theme.Theme: instance of the theme with name
            `--theme-name`.
        """
        import resumpy.themes
        themes_dict = {
            'sitges': resumpy.themes.ThemeSitges
        }
        return themes_dict[theme_name](logger)
