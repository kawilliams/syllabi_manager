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
    #for dc in dep_courses:
	#profSet.add(dc.instructor.strip())
    #for ps in profsSet:
	#profList.append(ps)
    #profList.sort()     

    
    logging.warning("ALL MY BUTTONS")
    logging.warning(request.form)
    
   
    if request.method == 'POST':
	
	sub = request.form['submit']
	logging.warning(sub)
	logging.warning(request.form.get(sub+".submit"))
	
	if sub in depsList:    
	    #here
	    dep_courses = Course.query.filter_by(dep=sub).all()
	    profSet = set()
	    for dc in dep_courses:
		profSet.add(dc.instructor.strip())
	    for ps in profSet:
		profList.append(ps)
	    profList.sort()  		    
	    return render_template("syllabi_manager.html", deps=depsList, 
		                   profs=profList, courses=courseList, 
	                           selected_dep=sub, selected_prof="", 
	                           profs_courses="")	

	if sub in profsSet:
	    logging.warning("we've clicked a person!")
	    logging.warning(request.form)
	    logging.warning(dep)
	    
	    dep_courses = Course.query.filter_by(dep=request.form['selected_dep']).all()
	    profSet = set()
	    for dc in dep_courses:
		profSet.add(dc.instructor.strip())
	    for ps in profSet:
		profList.append(ps)
	    profList.sort() 
	    
	    profs_courses = Course.query.filter_by(dep=request.form['selected_dep']).filter_by(instructor=sub).all()
	    
	    return render_template("syllabi_manager.html", deps=depsList, 
			               profs=profList, courses=courseList, 
	                               selected_dep=dep, selected_prof=sub, 
	                               profs_courses=profs_courses)		
	
    
    return render_template("syllabi_manager.html", deps=depsList, 
                           profs=[], courses=[], selected_dep="", 
                           selected_prof="", profs_courses="")


@app.route("/dept")
def get_profs():
    logging.warning("get_profs")
    logging.warning(request.form['submit'])
    
    
    return render_template("syllabi_manager.html", deps="")
    

		
if __name__ =="__main__":
    db.create_all()	
    app.run(debug=True)
	
