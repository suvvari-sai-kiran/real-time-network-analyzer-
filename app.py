from flask import Flask, render_template, jsonify
import mysql.connector

app = Flask(__name__)

def get_traffic_data():
    conn = mysql.connector.connect(
        host="127.0.0.1",
        port=3306,
        user="root",
        password="SAIKIRAN",
        database="network_logs"
    )
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT timestamp, src_ip, src_hostname, dst_ip, protocol, length
        FROM traffic_logs
        ORDER BY id DESC
        LIMIT 100
    """)
    data = cursor.fetchall()
    conn.close()
    return data

@app.route('/')
def index():
    data = get_traffic_data()
    return render_template("index.html", traffic=data)

@app.route('/refresh')
def refresh():
    data = get_traffic_data()
    return jsonify(data)

if __name__ == '__main__':
    app.run(debug=True)
