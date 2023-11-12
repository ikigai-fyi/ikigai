from flask import Blueprint, render_template

admin = Blueprint("admin", __name__)


@admin.get("/dashboard")
def admin_dashboard():
    cards = [
        {"title": "Title", "content": "Value"},
    ]
    return render_template("admin/dashboard.html", cards=cards)
