from flask import Flask, render_template
from flask_mysqldb import MySQL
import paho.mqtt.client as mqtt
import time

DEVICE_NAME = 'fipygroup7'

TTN_BROKER = 'eu.thethings.network'
TTN_USERNAME = ''
TTN_PASSWORD = ''
TTN_TOPIC = '+/devices/{}/up'.format(DEVICE_NAME)

app = Flask(__name__)

app.config['MYSQL_HOST'] = 'sql2.freemysqlhosting.net'
app.config['MYSQL_USER'] = 'sql2291958'
app.config['MYSQL_PASSWORD'] = 'tP1!yV7%'
app.config['MYSQL_DB'] = 'sql2291958'

mysql = MySQL(app)


@app.route('/')
def home():
    return render_template('Project_3_IoT_Home.html')


@app.route('/Search_for_Cycle/')
def search_for_cycle():
    MQTT_Connection()

    cur = mysql.connection.cursor()
    cur.execute('''SELECT cord1, cord2 FROM cordinates''')
    rv = cur.fetchall()
    cordinate1 = rv
    finalCordinate1 = ''.join(map(str, cordinate1))
    finalCordinate1 = finalCordinate1[1: -2]
    cutFinalCordinate = (finalCordinate1.translate(
        {ord(i): None for i in '"abcdefgashdtu:anwoi#$@faogjagpaw}])jgoawgpowaojgpagspgks;gma;ldsmaldaw;d'}))
    xAsis, yAsis = cutFinalCordinate.split(",")
    str(xAsis)
    str(yAsis)

    return render_template('Project_3_IoT_Map_Site.html', xAsis=xAsis, yAsis=yAsis)


@app.route('/Prices/')
def prices():
    return render_template('Project_3_IoT_Prices.html')


@app.route('/Contacts/')
def contacts():
    return render_template('Project_3_IoT_Contacts.html')


@app.route('/Registration/')
def registration():
    return render_template('Project_3_IoT_Registration.html')


def MQTT_Connection():
    def on_connect(client, userdata, flags, rc):
        print("Connected with result code", str(rc))
        client.subscribe(TTN_TOPIC)

    def on_message(client, userdata, msg):
        cut1 = msg.payload[460:496]
        cut2 = str(cut1)
        cut3 = cut2.replace("b", "")
        cut4 = (cut3.translate(
            {ord(i): None for i in '"abcdefgashdtu:anwoi#$@faogjagpaw}])jgoawgpowaojgpagspgks;gma;ldsmaldaw;d'}))
        cut5 = cut4.replace("'", "")
        x, y = cut5.split(",")
        float(x)
        float(y)
        cur = mysql.connection.cursor()
        cur.execute("UPDATE cordinates SET cord1 = %s, cord2 = %s", (x, y))
        mysql.connection.commit()

    client = mqtt.Client()
    client.username_pw_set(TTN_USERNAME, password=TTN_PASSWORD)
    client.on_connect = on_connect
    client.on_message = on_message
    client.connect(TTN_BROKER, 1883, 60)
    i = 10
    while i > 1:
        client.loop()
        i = i - 1


if __name__ == '__main__':
    app.run(debug=True)
