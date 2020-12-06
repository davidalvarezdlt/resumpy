import cv_generator
import json
import os
import logging
import pytest

base_path = os.path.join(os.path.dirname(__file__), '..')
example_path = os.path.join(base_path, 'cv.example.json')
schema_path = os.path.join(base_path, 'cv.example.json')
logger = logging.getLogger('cv_generator')


@pytest.mark.parametrize('file_path', [example_path, schema_path])
def test_example_schema_files(file_path):
    assert os.path.exists(file_path)
    with open(file_path) as cv_file:
        json.load(cv_file)


def test_example_loads():
    cv = cv_generator.CV(logger)
    cv.load(example_path, schema_path)


def test_dumping_json():
    cv = cv_generator.CV(logger)
    cv.load(example_path, schema_path)
    cv.save('cv_dumped', save_yaml=False)
    cv_2 = cv_generator.CV(logger)
    cv_2.load('cv_dumped.json', schema_path)
    os.remove('cv_dumped.json')
    assert cv == cv_2


def test_dumping_yaml():
    cv = cv_generator.CV(logger)
    cv.load(example_path, schema_path)
    cv.save('cv_dumped', save_json=False)
    cv_2 = cv_generator.CV(logger)
    cv_2.load('cv_dumped.yaml', schema_path)
    os.remove('cv_dumped.yaml')
    assert cv == cv_2
