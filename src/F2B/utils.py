class format_dict(dict):
    def __missing__(self, key):
        return '{'+key+'}'


def format_all(string, subs):
    if type(subs) is not format_dict and type(subs) is dict:
        subs = format_dict(subs)
    new_string = string % subs
    if new_string == string:  # No substitutions needed
        return string
    else:  # We made a substitution
        return format_all(new_string, subs)
