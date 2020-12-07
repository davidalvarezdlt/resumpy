import tests
import cv_generator.themes
import pytest
import os.path


def test_themes_in_init():
    assert len(cv_generator.themes.__themes_names__) == \
           len(cv_generator.themes.__all__)


@pytest.mark.parametrize('theme_name', cv_generator.themes.__themes_names__)
def test_cls_exist(theme_name):
    assert os.path.exists(tests.get_cls_path(theme_name))


@pytest.mark.parametrize('theme_name', cv_generator.themes.__themes_names__)
def test_themes_loads_example(theme_name):
    cv = cv_generator.CV(tests.get_logger())
    theme = cv_generator.theme.Theme.create_theme_by_name(
        theme_name, tests.get_logger()
    )
    cv.load(tests.get_example_path(), tests.get_schema_path())
    theme.format(cv.model)


@pytest.mark.parametrize('theme_name', cv_generator.themes.__themes_names__)
@pytest.mark.parametrize(
    'cv_raw', [tests.get_minimal_cv_raw(), tests.get_reduced_cv_raw()]
)
def test_themes_loads_extremes(theme_name, cv_raw):
    model = cv_generator.model.Model(cv_raw)
    theme = cv_generator.theme.Theme.create_theme_by_name(
        theme_name, tests.get_logger()
    )
    theme.format(model)
