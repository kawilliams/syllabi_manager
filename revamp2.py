#!/usr/bin/python
import os
import logging
from flask import (Flask, request, flash, url_for, 
                   redirect, render_template,
                   send_from_directory)
from werkzeug import secure_filename
from flask_sqlalchemy import SQLAlchemy
from make_database import Course
from make_database import db

""" 
Have muliple forms on one page and not lose your mind.
This is version 1. It's done, no problems (knock on wood), but the
database is going to change so a few tweaks need to be made
before productionizing.
"""

UPLOAD_FOLDER = 'all_syllabi/'

app = Flask(__name__, template_folder = 'templates')

#app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///CoursesHermon.sqlite3'
app.config['SECRET_KEY'] = 'secret'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True


#db = SQLAlchemy(app)

        
@app.route('/', methods=['GET','POST'])        
def index():
    courses = Course.query.all()
    return render_template('show_all_revamp.html', courses=courses)

        
@app.route('/my_courses', methods=['GET','POST']) #decorator
def get_courses():
    if request.method == 'POST':
        if request.form['submit'] == 'Find My Courses':
            first = request.form['firstname']
            last = request.form['lastname']
            
            if first == "":
                flash('Please enter your first name')
                return render_template('revamp2.html', firstname="", 
                                       lastname="", courses="")
            if last == "":
                flash('Please enter your last name')
                return render_template('revamp2.html', firstname="", 
                                       lastname="", courses="")
            
            first_name = first[0].upper() + first[1:].lower()
            last_name = last[0].upper() + last[1:].lower()
            email = request.form['email'].lower
            
            db_name = last_name + ' ' + first_name[0]
            found = Course.query.filter_by(instructor=db_name).all()

            return render_template('revamp2.html', firstname=first_name, 
                                   lastname=last_name,courses=found,first_load=False)
                            
        if request.form['submit'] == 'Submit Syllabi':
            logging.warning("SUBMITTING - trying")
            first = request.form['firstname']
            last = request.form['lastname']
            
            first_name = first[0].upper() + first[1:].lower()
            last_name = last[0].upper() + last[1:].lower()
            email = request.form['email'].lower
            
            db_name = last_name + ' ' + first_name[0]            
                       
            found = Course.query.filter_by(instructor=db_name).all()
            
            changed_syl_list = []
            changed_vis_list = []
            changed_prv_list = []
            logging.warning(found)
            for i in range(len(found)):
                
                course_name = (found[i].dep + ' ' + str(found[i].course_num) +
                               ': ' + found[i].title)
                
                #logging.warning(found_id)
                syl = "syllabus_link"+str(i)
                vis = "visitable"+str(i)
                prv = "privacy"+str(i)
                logging.warning("NEW")
                logging.warning(request.files)
                new_syllabus = request.files[syl]
                new_visitable = request.form[vis]
                new_privacy = request.form[prv]
                
                filename = secure_filename(new_syllabus.filename)
                
                syl_changed = False
                vis_changed = False
                prv_changed = False
                
                logging.warning(new_syllabus.filename)
                logging.warning(filename)
                logging.warning(found[i].syllabus_link)
                
                if len(filename) > 0 and new_syllabus.filename != found[i].syllabus_link:
                    syl_changed = True
                    changed_syl_list.append(course_name)
                if new_visitable != found[i].visitable:
                    vis_changed = True
                    changed_vis_list.append(course_name)
                if new_privacy != found[i].privacy:
                    prv_changed = True
                    changed_prv_list.append(course_name)
                    
                if new_syllabus.filename != '':
                    #w = 'No selected file for ' + course_name
                    #flash(w)
                    #return redirect(request.url)
                
                    new_syllabus.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                    logging.warning(found[i].syllabus_link)
                    setattr(found[i], 'syllabus_link', filename)
                    logging.warning(found[i].syllabus_link)
              
                setattr(found[i], 'privacy', new_privacy)
                setattr(found[i], 'visitable', new_visitable)
                
                
            db.session.commit()       
                
            return render_template('thankyou.html', syl_list=changed_syl_list, 
                                   vis_list=changed_vis_list, 
                                   prv_list=changed_prv_list, first_load=False)
    
   
    return render_template('revamp2.html')



@app.route('/syllabi/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@app.route('/syllabi/<path:filename>', methods=['GET', 'POST'])
def download(filename):
    if filename != "":        
        uploads = os.path.join(current_app.root_path, app.config['UPLOAD_FOLDER'])
        return send_from_directory(directory=app.config['UPLOAD_FOLDER'], filename=filename)
    else:
        return ""



if __name__ == "__main__":
    
    db.create_all()   
    app.run(debug=True)
    app.secret_key = 'secret'