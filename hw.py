import hashlib
import socket
import requests
import urllib3


def knock(host, port):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(0.2)
    try:
        s.connect((host, port))
    except socket.error:
        print("knocking...", port, "port")


def calculate(piece):
    piece = piece[1:]
    result = int(piece[0])
    for x in range(1, len(piece) - 1):
        if piece[x].isdigit():
            continue
        elif piece[x] == '-':
            result -= int(piece[x + 1])
        elif piece[x] == '+':
            result += int(piece[x + 1])
        elif piece[x] == '=':
            break
    print(result)
    return result


def slicer(txt):
    slice = txt[0].split(" ")
    number = int(slice[4])
    return number


def brute(result):
    i = 0
    while (True):
        pc = ''
        pc = str(i)
        hashr = hashlib.sha1(str.encode(result + str(pc))).hexdigest()
        if hashr[:4] == "0000":
            return result + str(pc)
        else:
            i += 1


def login():
    idpw = {'neptun': 'jqwghk', 'password': 'crysys'}
    session = requests.session()
    r = session.post('http://152.66.249.144', data=idpw)
    certificate = session.get('http://152.66.249.144/getcert.php')
    key = session.get('http://152.66.249.144/getkey.php')

    with open('getcert.pem', 'wb') as c:
        c.write(certificate.content)
    with open('getkey.pem', 'wb') as c:
        c.write(key.content)

    headers = {'User-Agent': 'CrySys'}
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    a = requests.get('https://152.66.249.144', cert=('getcert.pem', 'getkey.pem'), verify=False, headers=headers)
    print(a.text)


def main():
    host = '152.66.249.144'
    port = [1337, 2674, 4011]
    destination = 8888
    for x in range(0, 3):
        knock(host, port[x])
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((host, destination))
    data = s.recv(1024)
    print(data.decode('utf-8'))
    s.sendall(b'JQWGHK')
    neptuncode = s.recv(1024)
    print(neptuncode.decode('utf-8'))
    equations = s.recv(1024)
    print(equations.decode('utf-8'))  # I will send...
    equations = equations.decode('utf-8').split("\n")
    numofeq = slicer(equations)

    for i in range(0, numofeq):
        if i == 0:
            result = calculate(equations[2].split(" "))
            s.sendall(str.encode(str(result)))
        else:
            eq = s.recv(1024).decode('utf-8')
            print(eq)
            result = calculate(eq.split(" "))
            s.sendall(str.encode(str(result)))

    print(s.recv(1024).decode('utf-8'))
    print(s.recv(1024).decode('utf-8'))

    neptun = "JQWGHK"
    sha_1 = hashlib.sha1(str.encode((neptun) + str(result))).hexdigest()
    print(sha_1)
    s.sendall(str.encode(sha_1))
    print()

    print(s.recv(1024).decode('utf-8'))
    print(s.recv(1024).decode('utf-8'))

    print(str.encode(brute(neptun + str(result))))
    s.sendall(str.encode(brute(neptun + str(result))))

    print(s.recv(1024).decode('utf-8'))
    print(s.recv(1024).decode('utf-8'))
    print(s.recv(1024).decode('utf-8'))
   
    login()

main()
