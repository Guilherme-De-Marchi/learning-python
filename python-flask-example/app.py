import psycopg2
import flask

db_conn = psycopg2.connect(
    database='for_generic_tests',
    user='postgres',
    password='',
    host='localhost',
    port='5432',
)

app = flask.Flask(__name__)

@app.get('/static/<path:path>')
def send_static(path):
    return flask.send_from_directory('static', path)

@app.get('/client/<id>')
def get_client(id):
    cur = db_conn.cursor()
    cur.execute(
        """
            SELECT *
            FROM clients
            WHERE id=%s
            ;
        """,
        (id,)
    )
    client = cur.fetchone()
    db_conn.commit()
    cur.close()
    
    return flask.jsonify(client)

@app.post('/client')
def post_client():
    body = flask.request.json

    cur = db_conn.cursor()
    cur.execute(
        """
            INSERT INTO clients(
                first_name,
                last_name,
                age,
                email,
                password
            ) 
            VALUES (%s, %s, %s, %s, %s)
            RETURNING id
            ;
        """,
        (
            body['first_name'],
            body['last_name'],
            body['age'],
            body['email'],
            body['password'],
        )
    )
    id = cur.fetchone()[0]
    db_conn.commit()
    cur.close()

    return flask.jsonify({'id': id})