from flask import Flask, request, render_template, redirect, url_for
from datetime import datetime as dt
import datetime

app= Flask(__name__, template_folder="templates")

# todos1 = [ {"ToDo ": "Sample ToDo", "done": False}]
todos1 = []
todos2 = []
todos3 = []

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/location1')
def location1():
    return render_template("location1.html", todos=todos1)


@app.route('/location1/add', methods = ["POST"])
def add():
    todo = request.form['todo']
    deadline = dt.strptime(request.form['deadline'], '%Y-%m-%dT%H:%M')
    current_time = dt.now()

    if deadline < current_time:
        # deadline has already passed
        return redirect(url_for("location1"))

    todos1.append({"task": todo, "deadline": deadline, "done": False})
    return redirect(url_for("location1"))

@app.route('/edit/<location>/<int:index>', methods=['GET', 'POST'])
def edit(location, index):
    todo = None
    if location == 'location1':
        todo = todos1[index]
    elif location == 'location2':
        todo = todos2[index]
    elif location == 'location3':
        todo = todos3[index]

    if todo:
        if request.method == 'POST':
            todo['task'] = request.form['todo']
            if location == 'location1':
                deadline = request.form['deadline']
                if deadline:
                    try:
                        deadline = dt.strptime(deadline, '%Y-%m-%dT%H:%M')
                        current_time = dt.now()

                        if deadline < current_time:
                            # deadline has already passed
                            return "Error: Invalid deadline. Deadline should be a future date."

                        todo['deadline'] = deadline
                    except ValueError:
                        # invalid deadline format
                        pass
                return redirect(url_for('location1'))
            elif location == 'location2':
                todo['deadline'] = request.form['deadline']
                deadline = datetime.datetime.strptime(todo['deadline'], '%Y-%m-%d').date()
                current_date = datetime.date.today()
                if deadline < current_date:
                    return "Error: Invalid deadline. Deadline should be a future date."
                return redirect(url_for('location2'))
            elif location == 'location3':
                return  redirect(url_for('location3'))
        else:
            return render_template('edit.html', todo=todo, location=location, index=index)


@app.route('/location1/check/<int:index>')
def check(index):
    todos1[index]['done']= not todos1[index]['done']
    return redirect(url_for("location1"))

@app.route('/location1/delete/<int:index>')
def delete(index):
    del todos1[index]
    return redirect(url_for("location1"))

@app.route('/location2')
def location2():
    return  render_template("location2.html", todos=todos2)

@app.route('/location2/add2', methods=["POST"])
def add2():
    todo = request.form['todo']
    deadline = request.form['deadline']
    todos2.append({"task": todo, "done": False, "deadline": deadline})
    return redirect(url_for("location2"))


@app.route('/location2/check2/<int:index>')
def check2(index):
    todos2[index]['done'] = not todos2[index]['done']
    return redirect(url_for("location2"))

@app.route('/location2/delete2/<int:index>')
def delete2(index):
    del todos2[index]
    return redirect(url_for("location2"))

@app.route('/location3')
def location3():
    return render_template("location3.html", todos=todos3)

@app.route('/location3/add3', methods=["POST"])
def add3():
    todo = request.form['todo']
    todos3.append({"task": todo, "done": False})
    return redirect(url_for("location3"))

@app.route('/location3/check3/<int:index>')
def check3(index):
    todos3[index]['done'] = not todos3[index]['done']
    return redirect(url_for("location3"))

@app.route('/location3/delete3/<int:index>')
def delete3(index):
    del todos3[index]
    return redirect(url_for("location3"))

if __name__ == "__main__":
    app.run(debug=True)



