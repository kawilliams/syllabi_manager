from flask import Flask, render_template, redirect, url_for, request 
from flask_sqlalchemy import SQLAlchemy
from make_database import Course
from make_database import db

import logging


app = Flask(__name__)
app.debug=True
#app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////new.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
#db = SQLAlchemy(app)


@app.route("/", methods=["GET", "POST"])
def manage_form():
    courses = Course.query.all()
    logging.warning(len(courses))
    
    coursesSet = set()
    
    
    #form_dict = {}
    depsSet = set()
    profsSet = set()
    classesSet = set() 
    miss_syl = set() #or int??
    miss_prof = set()
    for c in courses:
	dep = str(c.dep.strip())
	prof = str(c.instructor.strip())
	title = str(c.title.strip())
	depsSet.add(dep)
	profsSet.add(prof)
	classesSet.add(title)
	coursesSet.add(c.CRN)
	#checking syllabi
	if c.syllabus_link == "":
	    miss_syl.add(c.title)
	    miss_prof.add(c.instructor)
    logging.warning(len(miss_syl))
    depsList = []
    for d in depsSet:
	depsList.append(d)
    depsList.sort()	
    
    profList = []
    courseList = []
   
    if request.method == 'POST':
	
	sub = request.form['submit']
	logging.warning(sub)
	#logging.warning(request.form.get(sub+".submit"))
	
	miss_syl = set()
	miss_prof = set()
	miss_syl_int = 0
	
	if sub in depsList:    
	    #here
	    dep_courses = Course.query.filter_by(dep=sub).all()
	    profSet = set()
	    
	    for dc in dep_courses:
		profSet.add(dc.instructor.strip())
		if dc.syllabus_link == "":
		    miss_syl.add(dc.title)
		    miss_prof.add(dc.instructor)
		    miss_syl_int += 1
	    for ps in profSet:
		profList.append(ps)
	    profList.sort()  
	    logging.warning((len(miss_syl)/miss_syl_int))
	    return render_template("syllabi_manager.html", deps=depsList, 
		                   profs=profList, courses=courseList, 
	                           selected_dep=sub, selected_prof="", 
	                           profs_courses="", miss_syl=len(miss_syl), 
	                           miss_prof=len(miss_prof))	

	if sub in profsSet:
	    logging.warning("we've clicked a person!")
	    logging.warning(request.form)
	    logging.warning(dep)
	    dep = request.form['selected_dep']
	    logging.warning(dep)
	    
	    
	    
	    dep_courses = Course.query.filter_by(dep=request.form['selected_dep']).all()
	    profSet = set()
	    for dc in dep_courses:
		profSet.add(dc.instructor.strip())
		if dc.syllabus_link == "":
		    miss_syl.add(dc.title)
		    miss_prof.add(dc.instructor)
		    miss_syl_int += 1
	    for ps in profSet:
		profList.append(ps)
	    profList.sort() 
	    
	    #profs_courses = Course.query.filter_by(dep=request.form['selected_dep']).filter_by(instructor=sub).all()
	    
	    profs_courses = Course.query.filter_by(dep=request.form['selected_dep']).filter_by(instructor=sub).order_by(Course.course_num)
	    
	    logging.warning((len(miss_syl)/miss_syl_int))
	    return render_template("syllabi_manager.html", deps=depsList, 
			               profs=profList, courses=courseList, 
	                               selected_dep=dep, selected_prof=sub, 
	                               profs_courses=profs_courses, 
	                               miss_syl=len(miss_syl), miss_prof=len(miss_prof))		
	
    logging.warning((len(coursesSet)))
    return render_template("syllabi_manager.html", deps=depsList, 
                           profs=[], courses=[], selected_dep="", 
                           selected_prof="", profs_courses="", 
                           miss_syl=len(miss_syl), miss_prof=len(miss_prof))
    

		
if __name__ =="__main__":
    db.create_all()	
    app.run(debug=True)
	
