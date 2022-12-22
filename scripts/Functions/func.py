from flask import abort
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps
from flask_login import current_user


# password hasher for securely storing passwords
def hash_password(password):
    hashed_password = generate_password_hash(
        password,
        method='pbkdf2:sha256',
        salt_length=8
    )
    return hashed_password


def admin_only(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated:
            return abort(403)
        elif current_user.id != 1:
            return abort(403)
        return f(*args, **kwargs)
    return decorated_function
