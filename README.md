# Mini Expense Tracker

## Project description

This folder contains a compact Flask project that demonstrates the basics of
tracking personal spending. The application is intentionally kept lightweight:
it does not use a database or authentication layer, and it stores everything in
simple Python lists that live in memory while the server is running.

---

## What you can do with it

- Set up simple user profiles.
- Create named spending categories (for example: Groceries, Commute, Subscriptions).
- Capture individual expenses linked to a user, category, and date.
- Define monthly budgets per user and category, with a configurable alert
  threshold (percentage of the budget that, once reached, should start warning).
- View a monthly breakdown that compares spending against budgets and marks
  each category as **OK**, **NEAR LIMIT**, or **EXCEEDED**.

All interaction happens through standard HTML pages rendered by Flask—there is
no JavaScript framework or separate API consumer involved.

---

## How to run it locally

### Requirements

- Python 3.9 or higher

### Setup and launch

From inside the `Expense_Tracker_App` directory, run:

```sh
pip install -r requirements.txt
python app.py
```

After the server starts, open `http://127.0.0.1:5000/` in your browser.

---

## Running with Docker

If you prefer to run the app in a container, a simple `Dockerfile` is included.
From inside the `Expense_Tracker_App` directory:

```sh
docker build -t mini-expense-tracker .
docker run -p 5000:5000 mini-expense-tracker
```

Then open `http://127.0.0.1:5000/` in your browser as usual.

---

## Navigating the interface

- **Home** – central hub with buttons for every action.
- **Create user** – make a profile with a display name and email address.
- **Add category** – define labels that you will assign expenses to.
- **Add expense** – choose a user and category, provide an amount, and
  optionally a short note and date.
- **Set monthly budget** – configure a monthly limit and alert threshold
  percentage for a given user+category pair.
- **View monthly summary** – choose a user and month; the app aggregates all
  recorded expenses and shows how they compare to any budgets you have set.

Because storage is in memory only, data is cleared every time you stop and
restart the Flask process.

---

## Test steps to validate the app

1. **Start the server**  
   - Install dependencies and run `python app.py`, then open `http://127.0.0.1:5000/`.
2. **Create basic data**  
   - Use **Create user** to add at least one user.  
   - Use **Add category** to create a few categories (for example: Groceries, Transport).
3. **Configure budgets**  
   - Open **Set monthly budget**, choose a user and one of the categories.  
   - Set a budget amount (for example: 1000) and keep the default alert threshold (10%).  
4. **Log expenses below the limit**  
   - Use **Add expense** to record one or more expenses for that user/category/month whose total is clearly below the budget.  
   - Go to **View monthly summary**, pick the same user and month, and confirm:  
     - The **overall total** matches the sum of the expenses.  
     - The category row shows the right **Spent**, **Budget**, and status `OK`.  
5. **Log expenses near the alert threshold**  
   - Add more expenses so that total spending for that category is close to the budget (for a 1000 budget and 10% threshold, aim around 900–1000).  
   - Refresh **View monthly summary** and confirm the status changes to `NEAR LIMIT`.  
6. **Exceed the budget**  
   - Add another expense that pushes total spending above the budget.  
   - Check **View monthly summary** again; the status should now read `EXCEEDED`.  
7. **Try a different month**  
   - Create another budget for the same user/category but a different month.  
   - Add expenses in that other month and verify that the report only includes expenses for the selected month.

---

## Edge cases to validate

- **Missing required fields**  
  - Leave required form inputs (like username, email, category name, amount, or month) blank and submit.  
  - Expected: the app flashes an error message and does not create the record.
- **Non-numeric or negative amounts**  
  - Enter text instead of a number, or an amount `<= 0`, in the **Add expense** or **Set monthly budget** forms.  
  - Expected: the app refuses to save and shows an error message asking for valid numeric values.
- **Reports with no expenses**  
  - Run **View monthly summary** for a user/month where no expenses were recorded.  
  - Expected: total spending is `0` and the table will either be empty or show no categories for that period.
- **Budgets not configured**  
  - Log expenses for a category/month without creating a budget first.  
  - Expected: in **View monthly summary**, spending is still shown, but the budget column is `0` and the status remains `OK` (no budget to compare against).
- **Multiple budgets for different months**  
  - Configure budgets for the same user/category but different months, then log expenses in each month.  
  - Expected: the report for each month should only use the matching budget for that specific month.

---

## Additional notes

- The code favors readability over completeness—error handling, security, and
  persistence are kept minimal on purpose.
- You can evolve this into a more realistic system by wiring it up to a real
  database (for example, through SQLAlchemy) and adding user authentication,
  migrations, and tests.
