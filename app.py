from flask import Flask, request, jsonify

app = Flask(__name__)

# Sample data store, replace with a database in production
expenses = []

# Endpoint to add an expense
@app.route('/add_expense', methods=['POST'])
def add_expense():
    data = request.get_json()
    expense = {
        'id': len(expenses) + 1,
        'description': data['description'],
        'amount': data['amount'],
        'date': data['date']
    }
    expenses.append(expense)
    return jsonify(expense), 201

# Endpoint to get all expenses
@app.route('/expenses', methods=['GET'])
def get_expenses():
    return jsonify(expenses), 200

if __name__ == '__main__':
    app.run(debug=True)