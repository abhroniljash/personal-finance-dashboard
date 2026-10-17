

from flask import (
    Flask, render_template, request,
    redirect, url_for, make_response
)
from flask_sqlalchemy import SQLAlchemy
from datetime import date, datetime
from sqlalchemy import func
import csv
import io

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///expenses.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

CATEGORIES = ["Food", "Transport", "Rent", "Utilities", "Other"]


class Expense(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(120), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    category = db.Column(db.String(50), nullable=False)
    date = db.Column(db.Date, nullable=False, default=date.today)


with app.app_context():
    db.create_all()


def get_filtered_expenses(args):
    query = Expense.query

    start = args.get("start", "").strip()
    end = args.get("end", "").strip()
    category = args.get("category", "").strip()

    if start:
        try:
            query = query.filter(
                Expense.date >= date.fromisoformat(start)
            )
        except ValueError:
            pass

    if end:
        try:
            query = query.filter(
                Expense.date <= date.fromisoformat(end)
            )
        except ValueError:
            pass

    if category in CATEGORIES:
        query = query.filter(Expense.category == category)

    return query.order_by(
        Expense.date.desc(), Expense.id.desc()
    ).all()


@app.route("/")
def index():
    expenses = get_filtered_expenses(request.args)
    total = sum(exp.amount for exp in expenses)

    category_totals = {}
    daily_totals = {}

    for expense in expenses:
        category_totals[expense.category] = (
            category_totals.get(expense.category, 0)
            + expense.amount
        )

        day = expense.date.isoformat()
        daily_totals[day] = (
            daily_totals.get(day, 0) + expense.amount
        )

    return render_template(
        "index.html",
        expenses=expenses,
        total=total,
        categories=CATEGORIES,
        selected_category=request.args.get("category", ""),
        start=request.args.get("start", ""),
        end=request.args.get("end", ""),
        category_labels=list(category_totals.keys()),
        category_values=list(category_totals.values()),
        day_labels=sorted(daily_totals.keys()),
        day_values=[
            daily_totals[day]
            for day in sorted(daily_totals.keys())
        ]
    )


@app.route("/add", methods=["POST"])
def add():
    description = request.form.get("description", "").strip()
    category = request.form.get("category", "").strip()
    amount_text = request.form.get("amount", "").strip()
    date_text = request.form.get("date", "").strip()

    if not description or len(description) > 120:
        return "Enter a description of 1-120 characters.", 400

    if category not in CATEGORIES:
        return "Please select a valid category.", 400

    try:
        amount = float(amount_text)
        expense_date = (
            date.fromisoformat(date_text)
            if date_text else date.today()
        )

        if not 0 < amount < float("inf"):
            raise ValueError

    except (ValueError, OverflowError):
        return "Enter a valid positive amount and date.", 400

    expense = Expense(
        description=description,
        amount=round(amount, 2),
        category=category,
        date=expense_date
    )

    db.session.add(expense)
    db.session.commit()

    return redirect(url_for("index"))


@app.route("/delete/<int:expense_id>", methods=["POST"])
def delete(expense_id):
    expense = db.get_or_404(Expense, expense_id)

    db.session.delete(expense)
    db.session.commit()

    return redirect(url_for("index"))


@app.route("/export")
def export():
    expenses = get_filtered_expenses(request.args)

    output = io.StringIO()
    writer = csv.writer(output)

    writer.writerow(["Date", "Description", "Category", "Amount"])

    for expense in expenses:
        writer.writerow([
            expense.date.isoformat(),
            expense.description,
            expense.category,
            f"{expense.amount:.2f}"
        ])

    response = make_response("\ufeff" + output.getvalue())
    response.headers["Content-Type"] = "text/csv; charset=utf-8"
    response.headers["Content-Disposition"] = (
        "attachment; filename=expenses.csv"
    )

    return response


if __name__ == "__main__":
    app.run(debug=True, port=4848)

