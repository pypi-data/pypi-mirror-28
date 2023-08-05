
# A very simple Flask Hello World app for you to get started with...

from flask import Flask
import sqlite3 as sql

app = Flask(__name__)

passEs = ['cheb']


def setpass(d):
    if d == "[CLEAR]":
        global passEs
        passEs = []
    else:
        passEs.append(str(d))


def decrypt(arg):
    return ''.join([chr(int(i)) for i in arg.split('Q')])


def encrypt(arg):
    retvar = []
    for i in str(arg):
        retvar.append(str(ord(i)))
    retvar = 'Q'.join(retvar)
    return retvar


@app.route('/')
def hello_world():
    return '''
Welcome to Michael Ilie's server API for sqlite, or TaliffDB for short
this is a home page
the package requirements are sqlite3 and flask
It runs on any version of python that can support these
  _    _     __      ________   ______ _    _ _   _
 | |  | |   /\ \    / /  ____| |  ____| |  | | \ | |
 | |__| |  /  \ \  / /| |__    | |__  | |  | |  \| |
 |  __  | / /\ \ \/ / |  __|   |  __| | |  | | . ` |
 | |  | |/ ____ \  /  | |____  | |    | |__| | |\  |
 |_|  |_/_/    \_\/   |______| |_|     \____/|_| \_|'''


@app.route('/db/<password>/<dbName>/<query>')
def query(password, dbName, query):
    if password not in passEs:
        return "Wrong Key Error"
    conn = sql.connect(dbName)
    c = conn.cursor()
    try:
        c.execute(decrypt(query))
        try:
            assert "select" in decrypt(query).lower() or "pragma" in decrypt(query).lower()
            w = c.fetchall()
            conn.commit()
            conn.close()
            return encrypt(str(w))
        except:
            conn.commit()
            conn.close()
            return "200"
    except Exception as e:
        return "Your query returned an error :) " + str(e)




