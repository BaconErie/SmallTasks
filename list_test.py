'''
TEST FOR LIST.PY

This should be moved from the "tests" folder to the same directory
as list.py 

'''

import sqlite3
import list

print('Hello world! Starting up...')

print('Setting up SQL tables list and task...')

connection = sqlite3.connect('SmallTasks_Data.db')
cursor = connection.cursor()

cursor.execute('CREATE TABLE list (list_id text, user_id text)')
connection.commit()

cursor.execute('CREATE TABLE task (task_body text, list_id text, task_num int)')
connection.commit()

print('Finished setting up SQL tables')


print('Testing create_list')
list_id = list.create_list('bob')
print('Got list_id, it is {}'.format(list_id))

print('Testing add_item')
output = list.add_item('bob', list_id, 'Bob\'s first task')
print(output)

print('Testing add_item no perms')
output = list.add_item('eve', list_id, 'Eve tries to add to Bob\'s list')
print(output)

print('Testing remove_item')
output = list.remove_item('bob', list_id, 1)
print(output)

print('Testing no perms remove_item')
output = list.remove_item('eve', list_id, 1)
print(output)

print('Testing get_list')
output = list.get_list('bob', list_id)
print(output)

print('Testing no perms get_list')
output = list.get_list('eve', list_id)
print(output)

print('Testing delete_list')
output = list.delete_list('bob', list_id)
print(output)

print('Testing no perms delete_list')
output = list.delete_list('eve', list_id)
print(output)

print('Good day world! Ending script...')
