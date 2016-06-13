from flask import Flask, render_template, redirect, url_for, request 
from flask_sqlalchemy import SQLAlchemy
from make_database import Course
import logging


app = Flask(__name__)
app.debug=True
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////new.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
db = SQLAlchemy(app)


@app.route("/", methods=["GET", "POST"])
def manage_form():
    courses = Course.query.all()
    
    
    #form_dict = {}
    depsSet = set()
    profsSet = set()
    classesSet = set() 
    for c in courses:
	dep = str(c.dep.strip())
	prof = str(c.instructor.strip())
	title = str(c.title.strip())
	depsSet.add(dep)
	profsSet.add(prof)
	classesSet.add(title)
	
    depsList = []
    for d in depsSet:
	depsList.append(d)
    depsList.sort()	
    
    profList = []
    courseList = []
    logging.warning("ALL MY BUTTONS")
    logging.warning(request.form)
    if request.method == 'POST':
	
	if 'submit' not in request.form:
	    logging.warning("NOPE")
	if 'submit' in request.form:
	    logging.warning("YUP")
	if '.submit' in request.form:
	    logging.warning("WHHHHH")
	
	sub = request.form['submit']
	logging.warning(sub)
	
	if sub in depsList:    
	    dep_courses = Course.query.filter_by(dep=sub).all()
	    profSet = set()
	    for dc in dep_courses:
		profSet.add(dc.instructor.strip())
	    for ps in profSet:
		profList.append(ps)
	    profList.sort()  
	    
	    return render_template("syllabi_manager.html", deps=depsList, 
		                   profs=profList, courses=courseList, selected_dep=sub, selected_prof="")	
	logging.warning("WEIRD FORM")
	logging.warning(request.form)
	
	if sub in profsSet:
	    logging.warning("we've clicked a person!")
	    #dep = request.form['selected_dep']
	    logging.warning(request.form)
	    logging.warning(dep)
	    return render_template("syllabi_manager.html", deps=depsList, 
			               profs=profList, courses=courseList, selected_dep=dep, selected_prof=sub)		
	
    
    return render_template("syllabi_manager.html", deps=depsList, 
                           profs=profList, courses=[], selected_dep="", selected_prof="")


@app.route("/dept")
def get_profs():
    logging.warning("get_profs")
    logging.warning(request.form['submit'])
    
    
    return render_template("syllabi_manager.html", deps="")
    

		
if __name__ =="__main__":
    db.create_all()	
    app.run(debug=True)
	
