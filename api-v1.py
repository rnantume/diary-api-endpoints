""" Restful api with python and flask
"""
from flask import Flask, jsonify, abort, make_response, request, url_for
# from flask_httpauth import HTTPBasicAuth

# auth = HTTPBasicAuth()
app = Flask(__name__)


# @auth.get_password
# def get_password(username):
#     if username == 'robin':
#         return 'robin'
    # return None

# @auth.error_handler
# def unauthorized():
#     return make_response(jsonify({'error': 'Unauthorized access'}), 401)

# @auth.error_handler
# def unauthorized():
#     return make_response(jsonify({'error': 'Forbidden error'}), 403)
# this will be invoked in order to distract web browsers is to return an error code other than 401
# which shows an ugly login dialog box when a request comes back with a 401 error code.

@app.errorhandler(400)
def bad_request(error):
    return make_response(jsonify({'error': 'Bad request'}), 400)


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)

entries = [
    {
        'entry_id': 1,
        'title': u'Upcoming interview at GTD.org',
        'entryContent': u'I would have to carry some business cards to give to GTD.org employees',
        'date': ''
    },
    {
        'entry_id': 2,
        'title': u'Call Emma in the evening',
        'entryContent': u'I need to inform him about the new stock',
        'date': ''
    }
]

def make_public_entry(entry):
    new_entry = {}
    for field in entry:
        if field == 'entry_id':
            new_entry['uri'] = url_for('get_entry', entry_id=entry['entry_id'],_external=True)
        else:
            new_entry[field] = entry[field]
    return new_entry

@app.route('/api/v1/entries', methods=['GET'])
# @auth.login_required
def get_entries():
    return jsonify({'entries': [make_public_entry(entry) for entry in entries]})

@app.route('/api/v1/entries/<int:entry_id>', methods=['GET'])
# @auth.login_required
def get_entry(entry_id):
    entry = [entry for entry in entries if entry['entry_id'] == entry_id]
    if len(entry) == 0:
        abort(404)
    return jsonify({'entry': make_public_entry(entry[0])})

@app.route('/api/v1/entries', methods=['POST'])
# @auth.login_required
def create_entry():
    if not request.json or not 'title' in request.json:
        abort(400)
    entry = {
        'entry_id': entries[-1]['id'] + 1,
        'title': request.json['title'],
        'entryContent': request.json.get('entryContent', ""),
        'done': False
    }
    entries.append(entry)
    return jsonify({'entry': make_public_entry(entry)}), 201

@app.route('/api/v1/entries/<int:entry_id>', methods=['PUT'])
# @auth.login_required
def update_entry(entry_id):
    entry = [entry for entry in entries if entry['entry_id'] == entry_id]
    if len(entry) == 0:
        abort(404)
    if not request.json:
        abort(400)
    if 'title' in request.json and type(request.json['title']) != unicode:
        abort(400)
    if 'entryContent' in request.json and type(request.json['entryContent']) is not unicode:
        abort(400)
    if 'done' in request.json and type(request.json['done']) is not bool:
        abort(400)
    entry[0]['title'] = request.json.get('title', entry[0]['title'])
    entry[0]['entryContent'] = request.json.get('entryContent', entry[0]['entryContent'])
    entry[0]['done'] = request.json.get('done', entry[0]['done'])
    return jsonify({'entry': make_public_entry(entry[0])})

@app.route('/api/v1/entries/<int:entry_id>', methods=['DELETE'])
# @auth.login_required
def delete_entry(entry_id):
    entry = [entry for entry in entries if entry['entry_id'] == entry_id]
    if len(entry) == 0:
        abort(404)
    entries.remove(entry[0])
    return jsonify({'result': True})


if __name__ == '__main__':
    app.run(debug=True)