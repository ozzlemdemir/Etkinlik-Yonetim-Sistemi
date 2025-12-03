from functools import wraps
from flask import session, redirect, url_for, flash

def role_required(allowed_roles=None):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            role = session.get("role")
            user_id = session.get("user_id")

            if not user_id:
                flash("Lütfen giriş yapın.", "danger")
                return redirect(url_for("app_routes.login"))

            if allowed_roles and role not in allowed_roles:
                flash("Bu sayfaya erişim izniniz yok!", "danger")
                if role == "admin":
                    return redirect(url_for("app_routes.admin_dashboard"))
                else:
                    return redirect(url_for("app_routes.index"))

            return f(*args, **kwargs)
        return decorated_function
    return decorator
