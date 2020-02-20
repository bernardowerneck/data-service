
from json import dumps
from flask import Flask, Response, request
from neo4jrestclient.client import GraphDatabase, Node
import logging
from flask_cors import CORS, cross_origin

app = Flask(__name__, static_url_path='/static/')
gdb = GraphDatabase("http://localhost:7474", username="neo4j", password="secret")
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

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

@app.route("/problem", methods=["POST"])
@cross_origin()
def persist_problem():
    app.logger.info("problem")
    problem = request.json
    app.logger.info(problem)
    print(problem, flush=True)

    newProblemNode = gdb.nodes.create()
    newProblemNode['subject'] = problem['subject']
    newProblemNode.labels.add("Problem")
    
    for content in problem['contents']:
        contentNode = gdb.nodes.create()
        contentNode.labels.add('Content')
        contentNode.properties = content
        contentNode.relationships.create('BelongsTo', newProblemNode)

    query = ("MATCH (user:User {name: 'testUser'}) return user")
    results = gdb.query(query, returns = Node)
    userNode = results[0][0]

    userNode.relationships.create("Wrote", newProblemNode)

    return "oioioi"



if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    app.run(port=8080, debug=True)