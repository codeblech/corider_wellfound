from email_validator import validate_email, EmailNotValidError


def validate_email_format(email):
    try:
        validate_email(email)
        return True
    except EmailNotValidError:
        return False
