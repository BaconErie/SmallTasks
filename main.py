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
    global todoDatabase
    #First get the data
    requestTable = request.get_json()
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
    print(todoDatabase[listID])
    return "Successfully POSTed data"

  elif request.method == "GET":
    #Check if there is data for the to do list
    if listID in todoDatabase.keys():
      #If there is data send data
      responseDict = {"data": todoDatabase[listID]}
      return responseDict
    else:
      #If there isn't return nothing
      return {"data": "nothing"}

if __name__ == "__main__":
  app.run(debug=True, host="0.0.0.0")