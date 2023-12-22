from flask import Blueprint, jsonify, render_template

from .services import get_dashboard_cards

admin = Blueprint("admin", __name__)


@admin.get("/dashboard")
def admin_dashboard():
    return render_template("admin/dashboard.html", cards=get_dashboard_cards())


@admin.get("/metrics")
def ep_get_metrics():
    return jsonify({"metrics": get_dashboard_cards()})
