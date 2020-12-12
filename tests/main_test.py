import resumpy
import json
import os
import pytest
import tests


@pytest.mark.parametrize(
    'file_path', [tests.get_example_path(), tests.get_schema_path()]
)
def test_example_schema_files(file_path):
    assert os.path.exists(file_path)
    with open(file_path) as cv_file:
        json.load(cv_file)


def test_model_loads_example():
    cv = resumpy.CV(tests.get_logger())
    cv.load(tests.get_example_path(), tests.get_schema_path())


@pytest.mark.parametrize(
    'cv_raw', [tests.get_minimal_cv_raw(), tests.get_reduced_cv_raw()]
)
def test_model_loads_extremes(cv_raw):
    resumpy.model.Model(cv_raw)


@pytest.mark.parametrize('format', ['json', 'yaml'])
def test_dumping(format):
    cv = resumpy.CV(tests.get_logger())
    cv.load(tests.get_example_path(), tests.get_schema_path())
    cv.save(
        'cv_dumped', save_json=format == 'json', save_yaml=format == 'yaml'
    )
    cv_2 = resumpy.CV(tests.get_logger())
    cv_2.load('cv_dumped.' + format, tests.get_schema_path())
    os.remove('cv_dumped.' + format)
    assert cv == cv_2
