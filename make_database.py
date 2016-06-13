#!/usr/bin/python
"""
Creates the course/syllabi database from a csv.
"""

import os
import cgi
import cgitb
import csv
import logging
from flask import (Flask, request, url_for, 
                   redirect, render_template)
from werkzeug import secure_filename
from flask_sqlalchemy import SQLAlchemy

cgitb.enable()


# Table Header indices
YEAR = 0 #2016
TERM = 1 #201601
TERM_TEXT = 2 #Fall 2016
CRN = 3 #15780
SUB = 4 #ARF
NUM = 5 #101
SECT = 6 #0
SEQ = 7 #1 or 2 <--not sure
SECTION_TITLE = 8 #Intro to Africana Studies
CREDITS = 9 #1
DAYS = 10 # M  W  F #
TIMES = 11 #0815-0930am
BLDG = 12 #CHAM
ROOM = 13 #1006
PROF = 14 #Hucks T
NOTES = 15 #XLST
MAX_ENROLL = 16 #30
DIST = 17 #CULT LBRQ
INTERDISCIPLINARY_COURSE1 = 18 #ARC
INTERDISCIPLINARY_COURSE2 = 19 #ENV
INTERDISCIPLINARY_COURSE3 = 20 #MHU
INTERDISCIPLINARY_COURSE4 = 21 #LIT

##########################################################################

def read_csv(filename):
    
    """Reads in filename.csv, writes contents to nested list"""
    
    courses = []   
    
    with open(filename, 'rU') as f:
        
        fReader = csv.reader(f, quotechar = '"', delimiter = ',')
        header = True
        
        for line in fReader: 
            
            if header:
                header = False
                pass            
            else:                
                #Remove extra whitespace
                #line[MEET_DAYS] = line[MEET_DAYS].replace(' ', '')
                #line[CLASS_TIME] = line[CLASS_TIME].replace(' ', '')
                line[DIST] = line[DIST].replace(
                    '\r\n', '')   
                courses.append(line)
            
    return courses

##########################################################################

app = Flask(__name__, template_folder = 'templates')

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///16-17coursesTeam.db'
app.config['SECRET_KEY'] = 'secret'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

db = SQLAlchemy(app)

class Course(db.Model):
    __tablename__='courses'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    dep = db.Column(db.String(100))
    course_num = db.Column(db.String(100))
    class_time = db.Column(db.String(100))
    class_section = db.Column(db.String(100), default='0')
    class_place = db.Column(db.String(100))
    class_days = db.Column(db.String(100))
    instructor = db.Column(db.String(100))
    acad_period = db.Column(db.String(100))
    max_enroll = db.Column(db.String(100)) #new
    dist = db.Column(db.String(100)) #new
    CRN = db.Column(db.String(100))
    syllabus_link = db.Column(db.String(1000), default="")
    visitable= db.Column(db.String(100), default="yes" )
    privacy= db.Column(db.String(100), default="davidson")
    all_data = db.Column(db.String(1000))
    
    def __init__(self, title, dep, course_num, class_time, class_section, 
                 class_place, class_days, instructor, acad_period, max_enroll, 
                 dist, CRN, syllabus_link, visitable, privacy): 
	 
	self.title = title 
	self.dep = dep 
	self.course_num = course_num
	self.class_time = class_time
	self.class_section = class_section
	self.class_place = class_place
	self.class_days = class_days
	self.instructor = instructor
	self.acad_period = acad_period
	self.max_enroll = max_enroll
	self.dist = dist
	self.CRN = CRN
	self.syllabus_link = syllabus_link #syllabus
	self.visitable = visitable
	self.privacy = privacy	
	self.all_data = (title+dep+course_num+class_time+class_section+
                 class_place+class_days+instructor+acad_period+max_enroll+
                 dist+CRN+syllabus_link+visitable+privacy)
    
    
    #def __repr__(self):
	#return "%s %s %s %s %s %s %s %s %s %s %s %s %s %s %s" \
	       #%(self.title, self.dep, self.course_num, self.class_time, self.class_section, 
                 #self.class_place, self.class_days, self.instructor, self.acad_period, self.max_enroll, 
                 #self.dist, self.CRN, self.syllabus_link, self.visitable, self.privacy)
    
	
def build_db(courses):
    db.create_all()
    
    for c in courses:	
	course = Course(c[SECTION_TITLE], c[SUB], c[NUM], c[TIMES], 
	                c[SECT], c[BLDG]+" "+c[ROOM], c[DAYS].replace(" ",''), 
	                c[PROF], c[TERM], c[MAX_ENROLL], c[DIST], 
	                c[CRN], "", "Can visit", "All")
	db.session.add(course)
	
    db.session.commit()

    return


@app.route('/', methods=['GET','POST'])        
def index():
    courses = Course.query.all()
    return render_template('show_all.html', courses=courses)

def main():
    #filename = "static/16-17_schedule.csv"
    #courses = read_csv(filename)
    #build_db(courses)
    logging.warning("MAIN")
    app.run(debug=True)

if __name__ == "__main__":
    main()