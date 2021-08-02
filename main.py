# SmallTasks Version 1.0.0 Development Version
# Created by BaconErie

from flask import Flask, render_template, request
import databaseAPI
import auth

#Run the createTable function on startup
databaseAPI.createTable()

app = Flask(__name__)
todoDatabase = {}

@app.route("/")
def index():
    return render_template("index.html")

@app.route('/signup', methods = ['GET', 'POST'])
def signup():
    if request.method == 'GET':
        return render_template('signup.html')
    if request.method == 'POST':
        json = request.get_json()
        print('New sign up request. Username is ' + json['username'] + ' and password is ' + json['password'])
        return "Success", 201

@app.route('/login')
def login():
    return render_template('login.html')

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

            currentList = databaseAPI.getList(listID)

            #Check if there is already a list
            if currentList:
                #If there is, just add to the list and push to database
                currentList.append(requestData)
                databaseAPI.setList(listID, currentList)
                return "Added data success"

            else:
                #Otherwise, create a new list and add data to list
                currentList = []
                currentList.append(requestData)
                #Push data to database
                databaseAPI.setList(listID, currentList)
                return "Created list and added data success"

        if requestTable["type"] == "remove":
            #Remove Task

            currentList = databaseAPI.getList(listID)

            #Check if list exists
            if currentList:
                #Check if item exists
                if int(requestTable["item"]) <= len(currentList) and int(requestTable["item"]) > 0:
                    #If all condtions are true, remove data from table
                    currentList.pop(int(requestTable["item"]) - 1)
                    #Push data to database
                    databaseAPI.setList(listID, currentList)
                else:
                    return "Item not in list"
            else:
                return "List does not exist"

    elif request.method == "GET":
        #Check if there is data for the to do list
        
        currentList = databaseAPI.getList(listID)
        
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