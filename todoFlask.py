from flask import Flask, jsonify, request
import datetime
import logging
from logging.handlers import RotatingFileHandler

app = Flask(__name__)

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
file_handler = RotatingFileHandler(
    'todoFlask.log', mode='a', maxBytes=5*1024*1024, backupCount=2,
    encoding=None, delay=0)
formatter = logging.Formatter(
    "%(asctime)s:%(levelname)s:%(threadName)s:%(message)s")
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

todos = {

}


@app.route('/todo', methods=['GET', 'PUT'])
def get_todos():
    """Returns a list of todos (GET) or adds a todo(PUT)"""
    if request.method == 'GET':
        # returns the full list of todos
        if todos.keys():
            logger.info("Todos requested, returned: {}".format(jsonify(todos)))
            return jsonify(todos)
        else:
            return "No todos found!"
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
        logger.info("New Todo created: {}".format(jsonify(todos[new_todo])))
        return jsonify(todos[new_todo])


@app.route('/todo/<int:todo_id>', methods=['GET', 'PATCH', 'DELETE'])
def todo_by_id(todo_id):
    """Returns, modifies, or deletes a todo based on /todo/<id>"""
    global todos
    if request.method == "GET":
        # returns a specific todo by id number
        logger.info("Requested Todo number: {}".format(todo_id))
        return jsonify(todos[todo_id])
    elif request.method == "PATCH":
        # changes a specific todo by id number
        for key in request.json.keys():
            if request.json[key] is not todos[todo_id][key]:
                todos[todo_id][key] = request.json[key]
        if todos[todo_id]['completed']:
            todos[todo_id]['completedOn'] = datetime.datetime.now()
        todos[todo_id]['updated'] = datetime.datetime.now()
        logger.info("Updated todo number: {}".format(todo_id))
        return jsonify(todos[todo_id])
    elif request.method == "DELETE":
        # removes a todo from the list of todos by id
        todos.pop(todo_id)
        logger.info("Deleted Todo number: {}".format(todo_id))
        return jsonify(todos)


if __name__ == '__main__':
    app.run()
