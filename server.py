import socket
from threading import Thread
import random 

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

ip_address = '127.0.0.1'
port = 8000

server.bind((ip_address,port))
server.listen()
list_of_clients = []

print("Welcome to the Quize Hub!")

question=[
    "What country has the highest life expectancy? \n a.Australia\n b.Hong Kong\n c.India\n d.China",
    "How many minutes are in a full week? \n a.10040\n b.12052\n c.10080\n d.70036"
]

answers=['b','c']

def broadcast(message,conn):
    for clients in list_of_clients:
        if clients != conn:
            try:
                clients.send(message.encode('utf-8'))
            except:
                remove(clients)

def remove(conn):
    if conn in list_of_clients:
        list_of_clients.remove(conn)

def remove_question(index):
    question.pop(index)
    answers.pop(index)

def get_random_question_answer(conn):
    random_index = random.randint(0,len(question)-1)
    random_question = question[random_index]
    random_answer = answers[random_index]
    conn.send(random_question.encode('utf-8'))
    return random_index, random_question, random_answer

def clientthread(conn):
    score = 0
    conn.send("You will recieve a question. the answer to that question should be one of a,b,c,d\n".encode('utf-8'))
    conn.send("Good Luck!\n\n".encode('utf-8'))
    index, question, answers = get_random_question_answer(conn)
    while True:
        try:
            message = conn.recv(2048).decode('utf-8')
            if message:
                if message.lower() == answers:
                    score +=1
                    conn.send("Bravo! Your score is {score}\n\n".encode('utf-8'))
                else:
                    conn.send("Incorrect answer! Better Luck next time.\n\n".encode('utf-8'))
                remove_question(index)
                index, question, answers = get_random_question_answer(conn)
            else:
                remove(conn)
        except:
            continue