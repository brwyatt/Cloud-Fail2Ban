class format_dict(dict):
    def __missing__(self, key):
        return '{'+key+'}'


def compile_regex(regex, subs):
    if type(subs) is not format_dict and type(subs) is dict:
        subs = format_dict(subs)
    compiled_regex = regex % subs
    if compiled_regex == regex:  # No substitutions made
        return regex
    else:  # We made a substitution
        return compile_regex(compiled_regex, subs)
