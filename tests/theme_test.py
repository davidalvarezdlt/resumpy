import cv_generator.themes
import pytest
import os.path

base_path = os.path.join(os.path.dirname(__file__), '..')


def test_themes_in_init():
    assert len(cv_generator.themes.__themes_names__) == len(
        cv_generator.themes.__all__)


@pytest.mark.parametrize('theme_name', cv_generator.themes.__themes_names__)
def test_cls_exist(theme_name):
    assert os.path.exists(os.path.join(
        base_path, 'cv_generator', 'themes', 'cls', theme_name + '.cls'
    ))
