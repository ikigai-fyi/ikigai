from flask import Blueprint, render_template

admin = Blueprint("admin", __name__)


@admin.get("/dashboard")
def admin_dashboard():
    return render_template("admin/dashboard.html")
