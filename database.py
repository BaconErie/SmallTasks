import sqlite3

#Tasks Table Creationn
def createTable():
  connection = sqlite3.connect("tasksData.db")
  cursor = connection.cursor()

  #Check if table exists
  cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='Tasks';")
  connection.commit()
  output = cursor.fetchone()
  
  if not output:
    #If the table doesn't exist, create table
    cursor.execute("CREATE TABLE Tasks (taskID int PRIMARY KEY, listID int, taskNum int, task text)")

    connection.commit()
  
  #Create List Table
  cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='Tasks';")
  connection.commit()
  output = cursor.fetchone()

  if not output:
    cursor.exectue('CREATE TABLE Lists (listID text PRIMARY KEY, user text)')
    connection.commit

  #Create Users Table
  cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='Users';")
  connection.commit()
  output = cursor.fetchone()

  if not output:
    cursor.execute('CREATE TABLE Users (userID text PRIMARY KEY, username text, password text)')
    connection.commit()
  
  connection.close()

#Get Todo List data from Tasks table
def getList(listID, userID):
  connection = sqlite3.connect("tasksData.db")
  cursor = connection.cursor()
  cursor.execute("SELECT task FROM Tasks WHERE listID=? ORDER BY taskNum", [listID])
  connection.commit()
  output = cursor.fetchall()

  connection.close()

  if output:
    #Loop through all the outputs, and turn all the tuples into a string in a list
    returnList = []
    for x in range(len(output)):
      #Turn the tuple into a list and then get the first element which is the string
      #After that, put into return list
      returnList.append(list(output[x])[0])
    
    return returnList
  else:
    return None

def setList(listID, todoList):
  connection = sqlite3.connect("tasksData.db")
  cursor = connection.cursor()

  #First delete all current entries that belong to the todoList
  cursor.execute("DELETE FROM Tasks WHERE listID=?", [listID])
  connection.commit()

  #Then loop through the given todo list and enter all the new entries into the table 
  for x in range(len(todoList)):
    cursor.execute("INSERT INTO Tasks (listID, taskNum, task) VALUES (?, ?, ?)", (listID, (x + 1), todoList[x]))
    connection.commit()
  
  connection.close()
        

    