from flask import Flask, jsonify, abort, make_response, request, url_for
import uuid
  

app = Flask(__name__)

ENTRIES = [
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

class Entries:
    """
    class for entries
    """
    def __init__(self, entry_id, title, entryContent, date):
        self.entry_id = uuid.uuid4().hex
        self.title = title
        self.entryContent = entryContent
        self.date = date

    def get_entries(self):
        return jsonify({'entries': ENTRIES})

    def get_entry(self, entry_id):
        entry = [entry for entry in ENTRIES if entry['entry_id'] == entry_id]
        if len(entry) == 0:
            abort(404)
        return jsonify({'entry': entry[0]})

    def create_entry(self):
        if not request.json or not 'title' in request.json:
            abort(400)
        entry = {
            'entry_id': uuid.uuid4().hex,
            'title': request.json['title'],
            'entryContent': request.json.get('entryContent', ""),
            'done': False
        }
        ENTRIES.append(entry)
        return jsonify({'entry': entry}), 201

    def update_entry(self, entry_id):
        entry = [entry for entry in ENTRIES if entry['entry_id'] == entry_id]
        if len(entry) == 0:
            abort(404)
        if not request.json:
            abort(400)
        if 'title' in request.json and type(request.json['title']) != 'unicode':
            abort(400)
        if 'entryContent' in request.json and type(request.json['entryContent']) != 'unicode':
            abort(400)
        if 'done' in request.json and type(request.json['done']) is not bool:
            abort(400)
        entry[0]['title'] = request.json.get('title', entry[0]['title'])
        entry[0]['entryContent'] = request.json.get('entryContent', entry[0]['entryContent'])
        entry[0]['done'] = request.json.get('done', entry[0]['done'])
        return jsonify({'entry': entry[0]})

    def delete_entry(self, entry_id):
        entry = [entry for entry in ENTRIES if entry['entry_id'] == entry_id]
        if len(entry) == 0:
            abort(404)
        ENTRIES.remove(entry[0])
        return jsonify({'result': True})


@app.route('/api/v1/entries', methods=['GET', 'POST'])
def entry():
    if request.method == 'POST': 
        return Entries.create_entry()
    else:
        return Entries.get_entries()

@app.route('/api/v1/entries/<int:entry_id>', methods=['GET', 'PUT', 'DELETE'])
def entries():
    if request.method == 'PUT':
        return Entries.update_entry()
    elif request.method == 'DELETE':
        return Entries.delete_entry()
    else:
        return Entries.get_entry()



if __name__ == '__main__':
    app.run(debug=True)        