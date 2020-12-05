import cv_generator
import json
import os
import pytest


def _get_example_path():
    return os.path.join(os.path.dirname(__file__), '..', 'cv.example.json')


def _get_schema_path():
    return os.path.join(os.path.dirname(__file__), '..', 'cv.example.json')


@pytest.mark.parametrize(
    'file_path', [_get_example_path(), _get_schema_path()]
)
def test_example_schema_files(file_path):
    assert os.path.exists(file_path)
    with open(file_path) as cv_file:
        json.load(cv_file)


def test_example_loads():
    cv = cv_generator.CV()
    cv.load(_get_example_path(), _get_schema_path())


def test_dumping_json():
    cv = cv_generator.CV()
    cv.load(_get_example_path(), _get_schema_path())
    cv.save('cv_dumped', save_yaml=False)
    cv_2 = cv_generator.CV()
    cv_2.load('cv_dumped.json', _get_schema_path())
    os.remove('cv_dumped.json')
    assert cv == cv_2


def test_dumping_yaml():
    cv = cv_generator.CV()
    cv.load(_get_example_path(), _get_schema_path())
    cv.save('cv_dumped', save_json=False)
    cv_2 = cv_generator.CV()
    cv_2.load('cv_dumped.yaml', _get_schema_path())
    os.remove('cv_dumped.yaml')
    assert cv == cv_2
