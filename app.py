from flask import (
    Flask,
    flash,
    redirect,
    render_template,
    request,
    url_for,
)

"""
Minimal, self‑contained expense tracker.

The goal of this module is to keep the implementation easy to read and
interview‑friendly rather than production‑ready. Data is held entirely in
Python lists so that the focus stays on request handling and basic logic.
"""


app = Flask(__name__)
# A fixed key is fine for a demo app; in a real deployment use an env var.
app.config["SECRET_KEY"] = "demo-secret-key"


# ---------------------------------------------------------------------------
# In‑memory "models"
# ---------------------------------------------------------------------------

users: list[dict] = []
categories: list[dict] = []
expenses: list[dict] = []
budgets: list[dict] = []


def next_id(sequence: list[dict]) -> int:
    """Return the next integer identifier for a list of dicts."""
    return (sequence[-1]["id"] + 1) if sequence else 1


# ---------------------------------------------------------------------------
# Home
# ---------------------------------------------------------------------------

@app.route("/", methods=["GET"])
def index():
    """Landing page with navigation to all forms."""
    return render_template("index.html")


# ---------------------------------------------------------------------------
# User management
# ---------------------------------------------------------------------------

@app.route("/add_user", methods=["GET", "POST"])
def add_user_form():
    """Create a new logical user for tracking expenses."""
    if request.method == "POST":
        username = (request.form.get("username") or "").strip()
        email = (request.form.get("email") or "").strip()

        if not username or not email:
            flash("Both name and email are required.", "danger")
            return render_template("add_user.html")

        users.append(
            {
                "id": next_id(users),
                "username": username,
                "email": email,
            }
        )
        flash("User has been added.", "success")
        return redirect(url_for("index"))

    return render_template("add_user.html")


# ---------------------------------------------------------------------------
# Categories
# ---------------------------------------------------------------------------

@app.route("/add_category", methods=["GET", "POST"])
def add_category_form():
    """Define a new spending category such as Groceries or Rent."""
    if request.method == "POST":
        name = (request.form.get("name") or "").strip()
        if not name:
            flash("Category name cannot be empty.", "danger")
            return render_template("add_category.html")

        categories.append(
            {
                "id": next_id(categories),
                "name": name,
            }
        )
        flash("Category saved.", "success")
        return redirect(url_for("index"))

    return render_template("add_category.html")


# ---------------------------------------------------------------------------
# Expenses
# ---------------------------------------------------------------------------

@app.route("/add_expense_form", methods=["GET", "POST"])
def add_expense_form():
    """Record a single expense entry."""
    if request.method == "POST":
        try:
            expense = {
                "id": next_id(expenses),
                "user_id": int(request.form.get("user_id")),
                "category_id": int(request.form.get("category_id")),
                "amount": float(request.form.get("amount")),
                "description": (request.form.get("description") or "").strip(),
                "date": request.form.get("date"),
            }
        except (TypeError, ValueError):
            flash("Please provide valid numeric values.", "danger")
            return render_template(
                "add_expense.html", users=users, categories=categories
            )

        if expense["amount"] <= 0:
            flash("Amount must be greater than zero.", "danger")
            return render_template(
                "add_expense.html", users=users, categories=categories
            )

        expenses.append(expense)
        flash("Expense recorded.", "success")
        return redirect(url_for("index"))

    return render_template("add_expense.html", users=users, categories=categories)


# ---------------------------------------------------------------------------
# Budgets
# ---------------------------------------------------------------------------

@app.route("/set_budget", methods=["GET", "POST"])
def set_budget_form():
    """Configure a monthly budget for a user and category combination."""
    if request.method == "POST":
        try:
            budget_amount = float(request.form.get("amount"))
            alert_threshold = float(request.form.get("alert_threshold") or 10)
            user_id = int(request.form.get("user_id"))
            category_id = int(request.form.get("category_id"))
        except (TypeError, ValueError):
            flash("Please supply valid numeric values for budget and threshold.", "danger")
            return render_template(
                "set_budget.html", users=users, categories=categories
            )

        month = (request.form.get("month") or "").strip()
        if not month:
            flash("Month is required (format YYYY-MM).", "danger")
            return render_template(
                "set_budget.html", users=users, categories=categories
            )

        budget = {
            "id": next_id(budgets),
            "user_id": user_id,
            "category_id": category_id,
            "amount": budget_amount,
            "month": month,
            "alert_threshold": alert_threshold,
        }
        budgets.append(budget)

        flash("Budget stored.", "success")
        return redirect(url_for("index"))

    return render_template("set_budget.html", users=users, categories=categories)


# ---------------------------------------------------------------------------
# Reporting
# ---------------------------------------------------------------------------

def _expenses_for(user_id: int, month: str) -> list[dict]:
    """Subset of expenses belonging to a user in a given YYYY-MM month."""
    return [
        e
        for e in expenses
        if e["user_id"] == user_id and (e.get("date") or "").startswith(month)
    ]


def _summarise_by_category(expense_list: list[dict]) -> dict[int, float]:
    """Return mapping of category_id -> total amount."""
    totals: dict[int, float] = {}
    for entry in expense_list:
        cat_id = entry["category_id"]
        totals[cat_id] = totals.get(cat_id, 0.0) + entry["amount"]
    return totals


def _find_budget(user_id: int, category_id: int, month: str) -> dict | None:
    """Return matching budget dict or None if none configured."""
    for b in budgets:
        if b["user_id"] == user_id and b["category_id"] == category_id and b["month"] == month:
            return b
    return None


@app.route("/report", methods=["GET", "POST"])
def report_form():
    """
    Show a per‑category summary for a user and month, including budget status.
    """
    data = None

    if request.method == "POST":
        try:
            user_id = int(request.form.get("user_id"))
        except (TypeError, ValueError):
            flash("Select a user to generate a report.", "danger")
            return render_template("report.html", users=users, data=None)

        month = (request.form.get("month") or "").strip()
        if not month:
            flash("Month is required (format YYYY-MM).", "danger")
            return render_template("report.html", users=users, data=None)

        monthly_expenses = _expenses_for(user_id, month)
        total_spent = sum(e["amount"] for e in monthly_expenses)

        per_category = _summarise_by_category(monthly_expenses)
        category_rows: list[dict] = []

        for cat_id, spent in per_category.items():
            category_name = next(
                (c["name"] for c in categories if c["id"] == cat_id),
                "Unlabelled",
            )
            budget_row = _find_budget(user_id, cat_id, month)
            budget_amount = budget_row["amount"] if budget_row else 0.0

            status = "OK"
            if budget_amount > 0:
                threshold = budget_row.get("alert_threshold", 10.0)
                remaining_ratio_trigger = 1 - (threshold / 100.0)
                if spent > budget_amount:
                    status = "EXCEEDED"
                elif spent >= budget_amount * remaining_ratio_trigger:
                    status = "NEAR LIMIT"

            category_rows.append(
                {
                    "category": category_name,
                    "spent": spent,
                    "budget": budget_amount,
                    "status": status,
                }
            )

        data = {"total": total_spent, "categories": category_rows}

    return render_template("report.html", users=users, data=data)


if __name__ == "__main__":
    app.run(debug=True)