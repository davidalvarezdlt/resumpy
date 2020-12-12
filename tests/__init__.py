import logging
import os

base_path = os.path.join(os.path.dirname(__file__), '..')


def get_example_path():
    return os.path.join(base_path, 'cv.example.json')


def get_schema_path():
    return os.path.join(base_path, 'cv.example.json')


def get_cls_path(theme_name):
    return os.path.join(
        base_path, 'resumpy', 'themes', 'cls', theme_name + '.cls'
    )


def get_logger():
    return logging.getLogger('resumpy')


def get_minimal_cv_raw():
    return {
        'lang': 'en',
        'last_update': '2000-01-01',
        'basic': {
            'name': 'John',
            'surnames': 'Snow',
            'profession': 'TV Star'
        },
        'contact': {
            'email': 'john@snow.com',
            'phone': '+1 666 777 888'
        },
        'experience': []
    }


def get_reduced_cv_raw():
    return {
        'lang': 'en',
        'last_update': '2000-01-01',
        'basic': {
            'name': 'John',
            'surnames': 'Snow',
            'profession': 'TV Star'
        },
        'contact': {
            'email': 'john@snow.com',
            'phone': '+1 666 777 888'
        },
        'experience': [{
            'institution': 'Game of Thrones',
            'position': 'Main Character',
            'date_start': '2000-01-01'
        }],
        'education': [{
            'institution': 'The Great Wall',
            'degree': 'Night\'s Watch',
            'date_start': '2000-01-01'
        }],
        'awards': [{
            'institution': 'Daenerys Awards',
            'name': 'Night with Daenerys',
            'date': '2000-01-01'
        }],
        'publications': [{
            'title': 'How to be a king of The North',
            'authors': 'John Snow',
            'date': '2000-01-01'
        }],
        'languages': [{
            'name': 'English',
            'level': 'Native'
        }],
        'courses': [{
            'institution': 'Targaryen Family',
            'name': 'Ride a dragon 101',
            'date': '2000-01-01'
        }],
        'projects': [{
            'name': 'The Great Wall 2.0'
        }],
        'skills': [{
            'name': 'Kill white walkers'
        }]
    }
