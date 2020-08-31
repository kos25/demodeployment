from flask import Flask ,request , jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://bzjhedrrusadyw:c564f989468c53fd818d5ac36b9d6d9a7015cd04baf05d06839de28effa479b6@ec2-54-234-28-165.compute-1.amazonaws.com:5432/da1hn9t83vuk83'
db = SQLAlchemy(app)
CORS(app)

class Tasklists(db.Model):
   __tablename__ = "tasklists"
   id = db.Column(db.Integer, primary_key = True)
   name = db.Column(db.String)    
   
#constructor function of  tasklits 
   def __init__(self, name):
    self.name = name

#to create tasks tabel in database 
class Tasks(db.Model):
   __tablename__ = "tasks"
   id = db.Column(db.Integer, primary_key = True)
   text = db.Column(db.String)
   Completed = db.Column(db.Boolean)
   list_id = db.Column(db.Integer)
 
   
#constructor function of  tasklits 
   def __init__(self, text ,list_id):
    self.text = text
    self.list_id = list_id
    self.Completed = False



#to get the value of  tasklist 
@app.route('/tasklists')      
def get_taskList():  
      task_lists = Tasklists.query.all()
      task_lists_list =[] 
      for task_list in task_lists:
        t={}
        t["id"] = task_list.id
        t["name"] = task_list.name    
        task_lists_list.append(t)
 
      return jsonify(tasklist=task_lists_list) 
 

# post thet tasklist
@app.route('/tasklists' ,  methods = ['POST']) 
def create_task_lists():
   data = request.get_json()
   name = data["name"]
   ts = Tasklists(name)   
   db.session.add(ts)
   db.session.commit()
   return jsonify(message = " task list is created") ,201


# post a new task    
@app.route('/tasks', methods = ['POST'])  
def create_task():
   data = request.get_json()
   text = data["text"]
   list_id = data["list_id"]   
   tl =  Tasks(text,list_id) 
   db.session.add(tl)
   db.session.commit()
   return jsonify(message ="task  created") , 201    


@app.route('/tasks')
def get_tasks():
   task_lists_id  = request.args.get('task_list')
   tasks = Tasks.query.filter_by(list_id = task_lists_id)
   task_list = []
   for task in tasks:
    t={}
    t["id"] = task.id 
    t["text"] = task.text
    t["Completed"]  = task.Completed
    t["list_id"] = task.list_id
    task_list.append(t)
   return jsonify(task = task_list) 


# put the  task or update the task 
@app.route('/tasks/<id>', methods = ['PUT'])
def update_task(id):   
   task = Tasks.query.filter_by (id = id).first()
   task.Completed = not(task.Completed)
   db.session.add(task)
   db.session.commit()   
   return jsonify(message = "task updated" , task_id = task.id, task_Completed = task.Completed)


# delete  the task 
@app.route("/tasks/<id>" , methods = ['DELETE'])
def delete(id):
   task =  Tasks.query.filter_by (id = id).first() 
   db.session.delete(task)
   db.session.commit()
   return jsonify(message = "delete task ")   
    





    

@app.route('/')
def Hello_Alean():
    return 'Hello Do to app!'


if __name__ == "__main__":
    db.create_all()
    app.run(debug=True)
