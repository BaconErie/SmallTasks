import sqlite3
import secrets

def check_list_permission(function):
    def action(user_id, list_id, *other_args):
        connection = sqlite3.connect('SmallTasks_Data.db')
        cursor = connection.cursor()

        cursor.execute('SELECT * FROM list WHERE user_id=? AND list_id=?', (user_id, list_id))
        connection.commit()

        if len(cursor.fetchone()) == 0:
            connection.close()
            return 'No Perms'
        else:
            connection.close()
            return function(user_id, list_id, *other_args)
    
    return action

@check_list_permission
def add_item(user_id, list_id, task_body):
    connection = sqlite3.connect('SmallTasks_Data.db')
    cursor = connection.cursor()

    cursor.execute('INSERT INTO task (task_body, list_id) VALUES (?, ?)', (task_body, list_id))
    connection.commit()

    connection.close()

@check_list_permission
def remove_item(user_id, list_id, item_num):
    connection = sqlite3.connect('SmallTasks_Data.db')
    cursor = connection.cursor()
    
    #Get current list contents to be added later
    contents = get_list(user_id, list_id)
    contents.pop(item_num - 1)
    
    #Delete all tasks part of list
    cursor.execute('DELETE FROM task WHERE list_id=?', (list_id)
    connection.commit()
    
    #Add tasks back in table except for deleted task
    for task in contents:
        add_item(user_id, list_id, task)

    connection.close()  

def create_list(user_id):
    new_list_id = 0
    not_generated = True
    connection = sqlite3.connect('SmallTasks_Data.db')
    cursor = connection.cursor()

    #Recursively generate id until unique one is found
    while not_generated:
        new_list_id = secrets.token_urlsafe(8)

        cursor.execute('SELECT * FROM list WHERE list_id=?', (new_list_id))
        connection.commit()

        if len(cursor.fetchall()) == 0:
            #Unique id
            not_generated = False

    cursor.execute('INSERT INTO list (list_id, user_id) VALUES (?, ?)', (new_list_id, user_id))
    connection.commit()

    connection.close()

@check_list_permission
def get_list(user_id, list_id):
    task_list = []
    connection = sqlite3.connect('SmallTasks_Data.db')
    cursor = connection.cursor()

    cursor.execute('SELECT task_body FROM task WHERE list_id=? ORDER BY task_num', (list_id))
    connection.commit()

    output = cursor.fetchall()

    for line in output:
        task_list.append(line[0])
    
    return task_list

@check_list_permission
def delete_list(user_id, list_id):
    connection = sqlite3.connect('SmallTasks_Data.db')
    cursor = connection.cursor()

    #Clear tasks
    cursor.execute('DELETE FROM task WHERE list_id=?', (list_id))

    #Clear list from list table
    cursor.execute('DELETE FROM task WHERE user_id=? AND list_id=?', (user_id, list_id))
