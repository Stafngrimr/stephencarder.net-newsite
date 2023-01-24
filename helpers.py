import os
import requests

from flask import redirect, session, render_template
from functools import wraps

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/index")
        return f(*args, **kwargs)
    return decorated_function

## Let's just add a little comment here to see if I can do something with it on GitHub
