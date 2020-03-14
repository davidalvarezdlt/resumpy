import gettext
import os
import pylatex


class BaseTheme:
    theme_name = None
    cv = None
    doc = None
    logger = None

    def __init__(self, theme_name, cv, logger):
        self.theme_name = theme_name
        self.cv = cv
        self.logger = logger
        self.doc = pylatex.Document(documentclass=self.theme_name)

    def set_lang(self):
        """Sets the language of the CV.

        Uses the `self.cv.lang` attribute to set the language of the generated file. This parameter only affects static
        labels of the theme, such as category titles. In order to translate the template to another language,
        let's say Russian, create a new .po (and its compiled .mo file) inside:

        ./locale/ru/LC_MESSAGES/base.po

        Notice that this file already contains translation items. In order not to break previous translations,
        use the commands `xgettext` (to generate a new base.pot file) and `msgmerge` to merge with the current ones.

        For example, being inside the folder 'cv_generator/themes`, run the following command on the terminal:

        ```
            xgettext -d base -o locale/base.pot sitges.py developer.py
        ```

        This will generate a new `base.pot` file inside `./locale` with all the strings contained inside the _(
        'MY_TRANSLATION_TEXT_ID') funciton. Then, mix with the current one using:

        ```
            msgmerge --update locales/en/LC_MESSAGES/base.po locales/base.pot
        ```

        This will update the `locales/en/LC_MESSAGES/base.po` with the new translation fields. Now, you can edit the
        translation file using an editor such as Poedit.
       """
        localedir = os.path.join(os.path.dirname(__file__), 'themes', 'locale')
        gettext.translation('base', localedir=localedir, languages=[self.cv.lang]).install()

    def get_cls_path(self):
        """Returns full path to `.cls` file of the theme.

        Returns:
            cls_path (str): absolute path to the `.cls` file of the current theme.
        """
        return os.path.join(os.path.dirname(__file__), 'themes', 'cls', self.theme_name + '.cls')

    def format(self):
        """Creates a new `pylatex.Document`.

        Uses the data stored inside `self.cv` to generate a new document. This method must be implemented by any
        individual theme.

        Returns:
            doc (pylatex.Document): document to be stored in disk.
        """
        raise NotImplemented
