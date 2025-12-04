# Expense Tracker App

## Overview
Expense Tracker is a Python Flask application that helps users track their daily expenses, categorize spending, set monthly budgets and savings goals, receive smart alerts on overspending, and generate actionable reports. It is designed for personal use and supports a simple form-based browser UI.

---

## Features

- Log daily expenses by category ("Food," "Transport," etc.)
- Set monthly budgets per category (with custom alerts when ~10% left)
- Automatic alerts if the user exceeds their budget, or when budget is nearly depleted
- Reports: total spending per month, budget vs. spending per category

---

## Getting Started

### Prerequisites
- Python 3.9+
- Docker (optional)

### Environment Setup

You may copy `.env.example` to `.env` if you want to use environment variables.

### Local Run

```sh
pip install -r requirements.txt
python app.py
```

### Docker Run

```sh
docker build -t expense-tracker .
docker run -p 5000:5000 expense-tracker
```

---

## Usage

All app features are available via browser forms (no API client needed):
- Add users, categories, expenses, and budgets via the home page.
- View monthly spending and budget status in the "Monthly Report" section.

---

## Test Steps

1. Create categories and users via the web forms.
2. Add budgets per user-category-month via the form.
3. Log expenses and check for alerts (e.g., over budget, <10% remaining).
4. Go to “Monthly Report” for per-category budget status.
5. Try edge cases: duplicate users/categories, zero/negative amounts, logging expense outside budget month. Error messages and alerts are shown for each scenario.

### Edge Case Documentation

- Duplicate users or categories: system prevents creation, shows error.
- Expenses outside budget month: recorded, but only affect relevant monthly report.
- Negative/zero amounts: prevented, with feedback.
- Budget status always visible (“EXCEEDED”, “NEAR LIMIT”, “OK”).

### SQL/ORM

Uses SQLAlchemy for all database operations.

---

## Docker

Dockerfile included; see above for commands.

---

## Contributors

Omkar Mahajan

---

## License

MIT
