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
    """Returns a list containing unique category names set in the skills.

    Args:
        skills (list of SkillItem): list containing SkillItem object models.

    Returns:
        list of str: list containing the identifiers of the different
        categories.
    """
    cat_list = []
    for item in skills:
        if item.get('category') and item.get('category') not in cat_list:
            cat_list.append(item.get('category'))
    return cat_list


def filter_skills_by_category(skills, category):
    """Filters the skills by category.

    Args:
        skills (list of SkillItem): list containing SkillItem object models.
        category (string): identifier of the category of the skills to
            return.

    Returns:
        list of SkillItem: list of skills belonging to `category`.
    """
    return [
        s for s in skills if category is None or s.get('category') == category
    ]
