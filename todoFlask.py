from flask import Flask, jsonify, request
import datetime
app = Flask(__name__)

todos = {

}


@app.route('/todo', methods=['GET', 'PUT'])
def get_todos():
    if request.method == 'GET':
        # returns the full list of todos
        return jsonify(todos)
    else:
        # adds a new todo to the list of todos
        if todos.keys():
            new_todo = max(todos.keys()) + 1
        else:
            new_todo = 1
        todos[new_todo] = {
            'title': request.json['title'],
            'due': request.json['due'],
            'completed': request.json['completed'],
            'completedOn': None,
            'updated': datetime.datetime.now(),
            'createdOn': datetime.datetime.now()
            }
        return jsonify(todos[new_todo])


@app.route('/todo/<todo_id>', methods=['GET', 'PATCH', 'DELETE'])
def todo_by_id(todo_id):
    global todos
    if request.method == "GET":
        # returns a specific todo by id number
        return jsonify(todos[todo_id])
    elif request.method == "PATCH":
        # changes a specific todo by id number
        for key in request.json.keys():
            if request.json[key] is not todos[todo_id][key]:
                todos[todo_id][key] = request.json[key]
        if todos[todo_id]['completed']:
            todos[todo_id]['completedOn'] = datetime.datetime.now()
        todos[todo_id]['updated'] = datetime.datetime.now()
        return jsonify(todos[todo_id])
    elif request.method == "DELETE":
        # removes a todo from the list of todos by id
        todos.pop(todo_id)
        return jsonify(todos)


if __name__ == '__main__':
    app.run()
