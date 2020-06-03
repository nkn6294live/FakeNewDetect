from json import dumps
from bottle import route, run, response, static_file, get, post, request
from GraphSearch import GraphSearch

@get("/FD")
def get_index():
    return static_file("index.html", root="static")

@get("/FD/view")
def get_view():
    return static_file("index.html", root="static")

@route('/FD/api/fakenew/check', method='POST')
def do_login():
    inputText = request.forms.get('inputText')
    response.content_type = 'application/json'

    data = graphSearch.process_text(inputText)
    return dumps(data)

@route('/api/fakenew/<inputText>')
def index(inputText):
    response.content_type = 'application/json'
    data = graphSearch.process_text(inputText)
    return dumps(data)

if __name__ == '__main__':
    graphSearch = GraphSearch()
    run(host='localhost', port=18080)
