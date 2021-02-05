from flask import Flask
from flask_restful import reqparse, abort, Api, Resource

app = Flask(__name__)
api = Api(app)

NOTES = {
    'note1': {'title': 'Commonly used HTTP methods', 'content' : ' GET, POST, PUT, DELETE' },
    'note2': {'title': 'Graph Data Structure', 'content': 'A Graph is a non-linear data structure consisting of nodes and edges. The nodes are sometimes also referred to as vertices and the edges are lines or arcs that connect any two nodes in the graph. More formally a Graph can be defined as,A Graph consists of a finite set of vertices(or nodes) and set of Edges which connect a pair of nodes.'},
    'note3': {'title': 'Javascript','content': 'Javascript is a scripting language . It support prototype based oops'},
}


def abort_if_todo_doesnt_exist(note_id):
    if note_id not in NOTES:
        abort(404, message="Note {} doesn't exist".format(note_id))

parser = reqparse.RequestParser()
parser.add_argument('title',location='form')
parser.add_argument('content', location='form')


# Todo
# shows a single note item and lets you delete a note item
class MyNote(Resource):
    def get(self, note_id):
        abort_if_todo_doesnt_exist(note_id)
        return NOTES[note_id]

    def delete(self, note_id):
        abort_if_todo_doesnt_exist(note_id)
        del NOTES[note_id]
        return '', 204

    def put(self, note_id):
        args = parser.parse_args()
        note = {'title': args['title'], 'content':args['content']}
        NOTES[note_id] = note
        return note, 201


# TodoList
# shows a list of all NOTES, and lets you POST to add 
class MyNotebook(Resource):
    def get(self):
        return NOTES

    def post(self):
        args = parser.parse_args()
        note_id = int(max(NOTES.keys()).lstrip('note')) + 1
        note_id = 'note%i' % note_id
        
        NOTES[note_id] = {'title': args['title'], 'content':args['content']}
        return NOTES[note_id], 201


##
api.add_resource(MyNotebook, '/mynotebook')
api.add_resource(MyNote, '/mynotebook/<note_id>')

if __name__ == '__main__':
    app.run(debug=True)
