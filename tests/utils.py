import cv_generator
import cv_generator.model as model
import os


def get_example_cv():
    base_path = os.path.dirname(os.path.dirname(__file__))
    cv = cv_generator.CV()
    cv.load(
        os.path.join(base_path, 'cv.example.json'),
        os.path.join(base_path, 'cv.schema.json')
    )
    return cv


def get_minimal_cv():
    cv = cv_generator.CV()
    cv.basic = model.BasicInfo()
