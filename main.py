from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

inventory = []


@app.route('/')
def index():
    return render_template('index.html', inventory=inventory)


@app.route('/add_inventory', methods=['POST'])
def add_inventory():
    item_name = request.form['item_name']
    quantity = int(request.form['quantity'])
    date_added = request.form['date_added']

    # Check if the item already exists
    for item in inventory:
        if item['item_name'] == item_name:
            item['quantity'] += quantity
            return jsonify({'message': 'Item already exists. Quantity updated.', 'status': 'success'})

    # If item doesn't exist, add it to inventory
    inventory.append({'item_name': item_name, 'quantity': quantity, 'date_added': date_added})
    return jsonify({'message': 'Item added successfully.', 'status': 'success'})


@app.route('/update_inventory', methods=['POST'])
def update_inventory():
    item_name = request.form['item_name']
    action = request.form['action']
    for item in inventory:
        if item['item_name'] == item_name:
            if action == 'reduce' and item['quantity'] > 0:
                item['quantity'] -= 1
                return jsonify({'message': 'Item quantity reduced successfully.', 'status': 'success'})
            elif action == 'add':
                item['quantity'] += 1
                return jsonify({'message': 'Item quantity increased successfully.', 'status': 'success'})
            elif action == 'restock' or item['quantity'] == 0:
                item['quantity'] += 1
                return jsonify({'message': 'Item restocked successfully.', 'status': 'success'})
    return jsonify({'message': 'Item not found or already in stock.', 'status': 'error'})


if __name__ == '__main__':
    app.run(debug=True)
