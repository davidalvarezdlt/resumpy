def escape_link(href):
    _latex_special_chars = {'%': r'\%'}
    return ''.join(_latex_special_chars.get(c, c) for c in str(href))
