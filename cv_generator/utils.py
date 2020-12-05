import datetime


def escape_link(href):
    _latex_special_chars = {'%': r'\%'}
    return ''.join(_latex_special_chars.get(c, c) for c in str(href))


def get_language_score(language_level):
    """Assigns a numeric value to each CEFR language level.

    Args:
        language_level (string): language level in CEFR format.
    """
    return {'A1': 40, 'A2': 50, 'B1': 60, 'B2': 70, 'C1': 80, 'C2': 90,
            'Native': 100}[language_level]


def get_age(birthday):
    """Converts the birthdate into an age.

    Returns:
        int: age of the person.
    """
    today = datetime.date.today()
    return today.year - birthday.year - (
            (today.month, today.day) < (birthday.month, birthday.day)
    )


def get_skills_categories(skills):
    categories_list = []
    for item in skills:
        if item.category is not None and item.category not in categories_list:
            categories_list.append(item.category)
    return categories_list


def filter_skills_by_category(skills, category):
    """Filters the skills by category.

    Args:
        category (string): identifier of the category of the skills to
            return.

    Returns:
        list: list of skills belonging to `category`.
    """
    return [
        s for s in skills if category is None or s.category == category
    ]
