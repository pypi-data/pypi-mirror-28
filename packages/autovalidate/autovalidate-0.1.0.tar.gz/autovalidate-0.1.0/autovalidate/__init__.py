import os

from autovalidate.validators import get_validator


def autovalidate(directory):
    for root, dirs, files in os.walk(directory):
        for filename in files:
            basename, ext = os.path.splitext(filename)
            validator = get_validator(ext)
            if validator is None:
                continue
            yield validator.validate(os.path.join(root, filename))
