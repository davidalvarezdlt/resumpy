_latex_special_chars = {
    '%': r'\%',
}


def escape_link(href):
    return ''.join(_latex_special_chars.get(c, c) for c in str(href))
