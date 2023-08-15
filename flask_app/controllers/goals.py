from flask_app import app
from flask import render_template,redirect,request,session,flash
from flask_app.models import goal,user
from flask_bcrypt import Bcrypt
bcrypt=Bcrypt(app)


@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect('/logout')
    data={
        'id': session['user_id']
    }
    goals_list = goal.Goal.get_goals_by_id(data) 
    return render_template('dashboard.html',goals_list=goals_list)

@app.route('/dashboard/dropdown', methods=['GET'])
def dropdown():
    return render_template('dashboard.html')

# @app.route('/dashboard/<string:category>')
# def dashboard_detail():
#     return render_template('category.html')

@app.route('/category/<category>')
def view_goals(category):
    if "user_id" not in session:
        return redirect('/logout')
    data ={
        'user_id':session['user_id'],
        'category':category
    }
    goals_list=goal.Goal.get_goals_by_category(data)
    return render_template("category.html",category=category,goals_list=goals_list)

@app.route('/create')
def create_recipe():
    if "user_id" not in session:
        return redirect('/logout')
    return render_template('create.html')

@app.route('/create_process', methods=['POST'])
def create_process():
    if 'user_id' not in session:
        return redirect('/logout')
    if not goal.Goal.validate_goal(request.form):
        return redirect("/create")
    data = {
        'user_id': session['user_id'],
        'title': request.form['title'],
        'plan': request.form['plan'],
        'category': request.form['category']
    }
    goal.Goal.save_goal(data)
    return redirect('/dashboard')

@app.route("/edit/<int:id>")
def edit(id):
    if "user_id" not in session:
        return redirect('/logout')
    return render_template("edit.html",goal_id=id)

@app.route("/edit_process/<int:id>",methods=['POST'])
def edit_process(id):
    if 'user_id' not in session:
        return redirect('/logout')
    if not goal.Goal.validate_goal(request.form):
        return redirect(f"/edit/{id}")
    data = {
        'id':id,
        'title':request.form['title'],
        'plan':request.form['plan'],
        'category':request.form['category'],
        'achieved':bool(request.form['achieved'])
    }
    print('----------------------')
    print(data)
    goal.Goal.edit_goal(data)
    return redirect('/dashboard')

@app.route("/delete/<int:id>")
def delete(id):
    if "user_id" not in session:
        return redirect('/logout')
    data = {
        "id":id
    }
    goal.Goal.delete(data)
    return redirect('/dashboard')
