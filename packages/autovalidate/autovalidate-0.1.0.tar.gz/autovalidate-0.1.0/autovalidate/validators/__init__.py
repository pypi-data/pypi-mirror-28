class Validator(object):
    def validate(self, path):
        raise NotImplementedError


class ValidationResult(object):
    def __init__(self, path, valid, message=None):
        self.path = path
        self.valid = valid
        self.message = message


class JsonValidator(Validator):
    def validate(self, path):
        import json

        try:
            with open(path) as f:
                json.load(f)
        except (ValueError, RuntimeError) as e:
            return ValidationResult(path, False, str(e))
        else:
            return ValidationResult(path, True)


class YamlValidator(Validator):
    def validate(self, path):
        import yaml

        try:
            with open(path) as f:
                yaml.load(f)
        except (yaml.parser.ParserError, RuntimeError) as e:
            return ValidationResult(path, False, str(e))
        else:
            return ValidationResult(path, True)

validators = {
    '.json': JsonValidator(),
    '.yaml': YamlValidator(),
    '.yml': YamlValidator()
}


def get_validator(extension):
    return validators.get(extension)
