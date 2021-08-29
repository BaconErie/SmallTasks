'''
TEST FOR auth.PY

This should be moved from the "tests" folder to the same directory
as auth.py 

'''
import auth
import sqlite3

print('Hello world! Starting up...')

print('Setting up SQL table user...')

connection = sqlite3.connect('SmallTasks_Data.db')
cursor = connection.cursor()

cursor.execute('CREATE TABLE user (user_id text, username text, password text)')
connection.commit()

connection.close()

print('Finished setting up SQL tables')

print('Testing create_account')
user_id = auth.create_account('Bob123', 'CorrectHorseBatteryStaple')
print(user_id)

print('Testing generate_token')
token = auth.generate_token(user_id)
print(token)

print('Testing decode_token')
decoded = auth.decode_token(token)
print(decoded)

print('Testing invalid decode_token')
decoded_invalid = auth.decode_token('totally_real_token')
print(decoded_invalid)

print('Testing verify_password (should output user id)')
output = auth.verify_password('Bob123', 'CorrectHorseBatteryStaple')
print(output)

print('Testing bad password verify_password')
output = auth.verify_password('Bob123', 'def real password')
print(output)

print('Testing not found verify_password')
output = auth.verify_password('Alice456', 'xkcd.com/936')
print(output)

print('Testing bad password delete_account')
output = auth.delete_account('Bob123', 'trob4dor thingidk')
print(output)

print('Testing not found delete_account')
output = auth.delete_account('Alice456', 'Was it trombone')
print(output)

print('Testing delete_account')
output = auth.delete_account('Bob123', 'CorrectHorseBatteryStaple')
print(output)

print('Making sure account was deleted')
output = auth.verify_password('Bob123', 'CorrectHorseBatteryStaple')
print(output)
print('If the above says \'Not Found\' then auth.delete_account() is a success')

print('Good day world! Stopping script...')