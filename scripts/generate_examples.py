import cv_generator
import os

if __name__ == '__main__':
    base_path = os.path.dirname(os.path.dirname(__file__))
    CV = cv_generator.CV()
    CV.load(
        os.path.join(base_path, 'cv.example.json'),
        os.path.join(base_path, 'cv.schema.json')
    )
