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
    if todoDatabase[listID] != None:
      #If there is, just add it to the list
      todoDatabase[listID].append(requestData)
    else:
      #Otherwise, create a new list and add data to list
      todoDatabase[listID] = []
      todoDatabase[listID].append(requestData)
    print(todoDatabase[listID])
    return "Successfully POSTed data"

  elif request.method == "GET":
    pass
    return "Get Success"

if __name__ == "__main__":
  app.run(debug=True, host="0.0.0.0")