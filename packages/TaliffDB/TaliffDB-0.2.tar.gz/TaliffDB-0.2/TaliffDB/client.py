import urllib.request

url = ""

def setUrl(e):
    global url
    url = e

def gotoURL(url):
    with urllib.request.urlopen(url) as response:
        html = response.read()
        return html


def decrypt(arg):
    return ''.join([chr(int(i)) for i in arg.split('Q')])


def encrypt(arg):
    retvar = []
    for i in str(arg):
        retvar.append(str(ord(i)))
    retvar = 'Q'.join(retvar)
    return retvar


def querydb(password, db, query):
    global url
    print(url.rstrip("/") + "/db/" + "/".join([password, db, encrypt(query)]))
    q = gotoURL(url.rstrip("/") + "/db/" + "/".join([password, db, encrypt(query)]))
    if q == "200":
        return "Executed Successfully"
    else:
        try:

            return decrypt((str(q)[2:-1]))
        except:
            return str(q)

#    return