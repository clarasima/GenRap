from marshmallow import ValidationError, validate

def validate_url_or_false(value):
    if value is not False:
        if not isinstance(value, str) or not validate.URL()(value):
            raise ValidationError("Must be a valid URL or false.")

def format_errors(errors):
    error_strings = []
    for field, messages in errors.items():
        for message in messages:
            error_strings.append(f"Field '{field}' - {message}")
    return "\n".join(error_strings)
