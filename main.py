from flask import Flask, render_template, request

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
      #First get the data
      requestData = requestTable["data"]
      #Then put into database

      #Check if there is already a list
      if listID in todoDatabase.keys():
        #If there is, just add it to the list
        todoDatabase[listID].append(requestData)
      else:
        #Otherwise, create a new list and add data to list
        todoDatabase[listID] = []
        todoDatabase[listID].append(requestData)

    if requestTable["type"] == "remove":
      #Remove Task

      #Check if list exists
      if listID in todoDatabase.keys():
        #Check if item exists
        if int(requestTable["item"]) <= len(todoDatabase[listID]) and int(requestTable["item"]) > 0:
          #If all condtions are true, remove data from table
          todoDatabase[listID].pop(int(requestTable["item"]) - 1)
        else:
          return "Item not in list"
      else:
        return "List does not exist"

  elif request.method == "GET":
    #Check if there is data for the to do list
    if listID in todoDatabase.keys():
      #If there is data send data
      responseDict = {"data": todoDatabase[listID]}
      return responseDict
    else:
      #If there isn't return nothing
      return {"data": "nothing"}
  
  return "Success"

if __name__ == "__main__":
  app.run(debug=True, host="0.0.0.0")