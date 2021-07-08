#SmallTasks Version 1.0.0 Development Version
#Created by BaconErie

from flask import Flask, render_template, request
import sqlite3

######################### Data Saving

#Tasks Table Creation
def createTable():
  connection = sqlite3.connect("tasksData.db")
  cursor = connection.cursor()

  #Check if table exists
  cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='Tasks';")
  connection.commit()
  output = cursor.fetchone()
  
  if not output:
    #If the table doesn't exist, create table
    cursor.execute("CREATE TABLE Tasks (listID int, taskNum int, task text)")

    connection.commit()
  
  connection.close()

#Get Todo List data from Tasks table
def getList(listID):
  connection = sqlite3.connect("tasksData.db")
  cursor = connection.cursor()
  print(listID)
  cursor.execute("SELECT * FROM Tasks WHERE listID=? ORDER BY taskNum", [listID])
  connection.commit()
  output = cursor.fetchone()

  connection.close()

  return output

def setList(listID, todoList):
  connection = sqlite3.connect("tasksData.db")
  cursor = connection.cursor()

  #First delete all current entries that belong to the todoList
  cursor.execute("DELETE FROM Tasks WHERE listID=?", [listID])
  connection.commit()

  #Then loop through the given todo list and enter all the new entries into the table
  for x in range(len(todoList)):
    cursor.execute("INSERT INTO Tasks (listID, taskNum, task) VALUES (?, ?, ?)", (listID, x + 1, todoList[x]))
    connection.commit()
  
  connection.close()

#Run the createTable function on startup
createTable()

########################### End Data Saving Code

app = Flask(__name__)
todoDatabase = {}

@app.route("/")
def index():
  return render_template("index.html")

@app.route("/<listID>")
def todo(listID):
  return render_template("todo.html", listID=listID)

@app.route("/<listID>/api", methods = ["GET", "POST"])
def api(listID):

  if request.method == "POST":
    #Get the JSON
    requestTable = request.get_json()
    #Check what the client wants to do
    if requestTable["type"] == "add":
      #Add task

      global todoDatabase
      #Get the data that is to be added to the todo list
      requestData = requestTable["data"]

      #Edit list and then put list into the database

      currentList = getList(listID)

      #Check if there is already a list
      if currentList:
        #If there is, just add to the list and push to database
        currentList.append(requestData)
        setList(listID, currentList)
        return "Added data success"

      else:
        #Otherwise, create a new list and add data to list
        currentList = []
        currentList.append(requestData)
        #Push data to database
        setList(listID, currentList)
        return "Created list and added data success"

    if requestTable["type"] == "remove":
      #Remove Task

      currentList = getList(listID)

      #Check if list exists
      if currentList:
        #Check if item exists
        if int(requestTable["item"]) <= len(currentList) and int(requestTable["item"]) > 0:
          #If all condtions are true, remove data from table
          currentList.pop(int(requestTable["item"]) - 1)
          #Push data to database
          setList(listID, currentList)
        else:
          return "Item not in list"
      else:
        return "List does not exist"

  elif request.method == "GET":
    #Check if there is data for the to do list
    
    currentList = getList(listID)
    
    if currentList:
      #If there is data send data
      responseDict = {"data": currentList}
      return responseDict
    else:
      #If there isn't return nothing
      return {"data": "nothing"}
  
  return "Success"
  


if __name__ == "__main__":
  app.run(debug=True, host="0.0.0.0")