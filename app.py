from flask import Flask, jsonify, request, abort

app = Flask(__name__)

# Хранилище элементов в памяти
items = {}
next_id = 1

@app.route('/items', methods=['GET'])
def get_items():
    return jsonify(list(items.values()))

@app.route('/items', methods=['POST'])
def create_item():
    global next_id
    data = request.get_json()
    if not data or 'name' not in data:
        abort(400, description="Отсутствует обязательное поле 'name'")
    item = {'id': next_id, 'name': data['name']}
    items[next_id] = item
    next_id += 1
    return jsonify(item), 201

@app.route('/items/<int:item_id>', methods=['GET'])
def get_item(item_id):
    item = items.get(item_id)
    if item is None:
        abort(404, description="Элемент не найден")
    return jsonify(item)

@app.route('/items/<int:item_id>', methods=['PUT'])
def update_item(item_id):
    if item_id not in items:
        abort(404, description="Элемент не найден")
    data = request.get_json()
    if not data or 'name' not in data:
        abort(400, description="Отсутствует обязательное поле 'name'")
    items[item_id]['name'] = data['name']
    return jsonify(items[item_id])

@app.route('/items/<int:item_id>', methods=['DELETE'])
def delete_item(item_id):
    if item_id not in items:
        abort(404, description="Элемент не найден")
    del items[item_id]
    return '', 204

# Тестовый эндпоинт для сброса состояния API
@app.route('/reset', methods=['POST'])
def reset():
    global items, next_id
    items = {}
    next_id = 1
    return '', 204

if __name__ == '__main__':
    app.run(debug=True)
