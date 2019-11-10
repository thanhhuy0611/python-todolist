import os
import sqlite3
from termcolor import colored
from tabulate import tabulate 
from datetime import datetime


DEFAULT_PATH = os.path.join(os.path.dirname(__file__), 'database.sqlite3')

conn = sqlite3.connect(DEFAULT_PATH)
cur = conn.cursor()

# Setup DB ------------------
def set_up_database():
    sql = """
        CREATE TABLE IF NOT EXISTS todos(
            id INTEGER PRIMARY KEY,
            body TEXT NOT NULL,
            status TEXT NOT NULL,
            project_id INTEGER NOT NULL,
            user_id INTEGER NOT NULL,
            due_date DATETIME
        )
    """
    cur.execute(sql)
    conn.commit()

def set_up_user():
    sql = """
        CREATE TABLE IF NOT EXISTS users(
            id INTEGER PRIMARY KEY,
            email TEXT NOT NULL,
            name TEXT NOT NULL
        )
    """
    cur.execute(sql)
    conn.commit()

set_up_database()   
set_up_user()


def show_help_menu():
#   os.system('cls' if os.name == 'nt' else 'clear')
  print(colored('Todo List Options:', 'blue'))
  print(colored('*' * 50, 'blue'))
  print(colored('1. List all todos:', 'blue'),colored('\t\t list', 'yellow'))
  print(colored('2. Add a new todo:', 'blue'),colored('\t\t add', 'yellow'))
  print(colored('3. Delete a todo:', 'blue'),colored('\t\t delete', 'yellow'))
  print(colored('4. Mark a todo complete:', 'blue'),colored('\t\t complete', 'yellow'))
  print(colored('5. Mark a todo uncomplete:', 'blue'),colored('\t incomplete', 'yellow'))
  print(colored('6. Show help menu:', 'blue'),colored('\t\t help', 'yellow'))
  print(colored('-' * 100, 'blue'))

def list(user_id):
    id = user_id
    sql = """
        SELECT * FROM todos
        WHERE user_id = ?
        ORDER BY due_date DESC
    """
    cur.execute(sql,(id,))
    result = cur.fetchall()
    print(tabulate (result, 
        headers=[
            colored("id","green"), 
            colored("body","green"), 
            colored("status","green"), 
            colored("project_id","green"), 
            colored("user_id","green"),
            colored("due_date","green"), 
        ], 
        tablefmt="fancy_grid"))

def add(id):

    print("what do you want to add?")
    body = input()
    print("What project ID?")
    project_id = input()    
    user_id = id
    due_date = datetime.now()

    sql = """
        INSERT INTO todos
            (body,status,project_id,user_id,due_date)
         VALUES (?,?,?,?,?)
    """
    cur.execute(sql,(body, "INCOMPLETE", project_id, user_id, due_date,))
    conn.commit()
    print(colored("ADD SUCCESS!","yellow"))
    list(user_id)

def delete():
    list()
    print("Which is ID you want to delete?")
    id = input()
    sql = """
        DELETE FROM todos WHERE id = (?)
    """
    cur.execute(sql,(id,))
    conn.commit()
    list()
    print(colored("DELETE SUCCESS!","yellow"))

def complete():
    print("Which is ID you want to mark complete?")
    id = input()
    sql = """
        UPDATE todos  SET status = "COMPLETE" WHERE id = (?)
    """
    cur.execute(sql,(id,))
    conn.commit()
    list(user_id)

def incomplete():
    print("Which is ID you want to mark incomplete?")
    id = input()
    sql = """
        UPDATE todos  SET status = "INCOMPLETE" WHERE id = (?)
    """
    cur.execute(sql,(id,))
    conn.commit()
    list(user_id)

def check_account():    
    sql="""
        SELECT email FROM users
        WHERE email = (?) 
    """
    cur.execute(sql,(email,))
    email_list = cur.fetchall()
    # print(email_list)
    if len(email_list) == 0:
        create_new_user()
    else: print(colored('Welcome back',"green"),colored(email,'green'))

def create_new_user():
    print("Created account with email",colored(email,"green"))
    print("what's your name?")
    name=input()
    sql ="""
        INSERT INTO users 
        (email,name)
        VALUES (?,?)
    """
    cur.execute(sql,(email,name,))
    conn.commit()  


# Define R.E.P.L.
if __name__ == '__main__':
    # try:
        print('What your email?')
        email = input()
        check_account()
        sql = """
            SELECT * FROM users
            WHERE email = (?)
        """
        cur.execute(sql,(email,))
        user_info = cur.fetchall()
        user_id = user_info[0][0]
        user_name = user_info[0][2]
        # print(user_info)
        show_help_menu()
        while True:
            print("Please type your order,"+ colored(user_name,"green") +"?")
            choice = input()
            if choice == "list":
                list(user_id)
            elif choice == "add":
                add(user_id)  
            elif choice == "delete":
                delete()
            elif choice == "complete":
                complete()
            elif choice == "incomplete":
                incomplete()
            elif choice == "help":
                show_help_menu()
            
            else: 
                show_help_menu()
                print(colored("[!]WRONG SYNTAX","red"))
     
    # except:
    #     print('[!]ERROR')
