
from json import dumps

from flask import Flask, Response, request

from neo4jrestclient.client import GraphDatabase, Node

app = Flask(__name__, static_url_path='/static/')
gdb = GraphDatabase("http://localhost:7474", username="neo4j", password="secret")

@app.route("/")
def get_index():
    return app.send_static_file('index.html')

@app.route("/search")
def get_search():
    query = ("MATCH (student:User) "
                "RETURN student")
    results = gdb.query(
        query,
        returns=Node,
    )
    return Response(dumps([{"student": row.properties}
                            for [row] in results]),
                    mimetype="application/json")


if __name__ == '__main__':
    app.run(port=8080)