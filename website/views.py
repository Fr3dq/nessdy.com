from flask import Blueprint, render_template, request, flash, jsonify
from flask_login import current_user
from .models import Note, Links, Image
from . import db
import json
from .security import CheckForSpecialSigns, DivideLinks, DetectHarmfulLinks
import os
from werkzeug.utils import secure_filename
from datetime import datetime

# Uploading images
UPLOAD_FOLDER = r'static\uploads'
UPLOAD_FOLDER_2 = r'C:\Users\Fryderyk\Nessdy.com\website\static\uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

views = Blueprint('views', __name__)

@views.route('/')
def home():
    return render_template("home.html", user = current_user)

@views.route('/cloud')
def shop():
    all_notes = Note.query.all()
    return render_template("shop.html", user = current_user, notes=all_notes)

@views.route('/create', methods=['GET', 'POST'])
def facts():
    if request.method == 'POST':
        title = request.form.get('title')
        note = request.form.get('note')
        spec = request.form.get('spec')
        link = request.form.get('social')
        link = DivideLinks(link)
        files = request.files.getlist('images')

        if len(note) >= 30000:
            flash('Description is too long', category ='error')
        elif len(note) < 1:
            flash('Description is too short', category = 'error')
        elif len(title) < 1:
            flash('Title is too short', category ='error')
        elif len(title) > 50:
            flash('Title is too long', category ='error')
        elif CheckForSpecialSigns(title) == 1:
            flash('Do not use special characters', category ='error')
        elif len(spec) > 500:
            flash('Specyfication is too long', category = 'error')
        elif DetectHarmfulLinks(link) == 1:
            flash('Your links are unacceptable', category = 'error')    
        elif len(files) > 8:
                flash("You can upload up to 8 images", category='error')
        else:
            new_note = Note(title=title, data=note, spec=spec, user_id=current_user.id, username=current_user.first_name)
            db.session.add(new_note)
            db.session.commit()

            for x in link:
                new_link = Links(link=x, note_id=new_note.id)
                db.session.add(new_link)
            
            #Uploading images
            for file in files:
                if file and allowed_file(file.filename):
                    filename = secure_filename(file.filename) #Find out what is secure_filename
                    #filepath = "static/uploads/" + filename
                    filepath = os.path.join(UPLOAD_FOLDER_2, filename) 
                    if os.path.exists(UPLOAD_FOLDER_2):
                        file.save(filepath)
                    else:
                        print('doesnt exist ' + filepath)
                        
                    new_image = Image(path=filename, note_id=new_note.id) #I only add filename because path is always the same
                    db.session.add(new_image)

            db.session.commit()
            flash('Project created!', category = 'error')

    return render_template("facts.html", user = current_user)

@views.route('/delete-note', methods=['POST'])
def delete_note():
    note = json.loads(request.data)
    noteId = note['noteId']
    note = Note.query.get(noteId)

    if note:
        
        images = Image.query.filter_by(note_id=noteId).all()
        for image in images:
            try:
                os.remove(os.path.join(UPLOAD_FOLDER_2, image.path))
            except FileNotFoundError:
                pass
            db.session.delete(image)

        db.session.delete(note)
        db.session.commit()
            
    return jsonify({})

@views.route('/settings' , methods =['GET','POST'])
def settings():
    if request.method == 'POST':
        return render_template("facts.html", user = current_user)
    return render_template("settings.html", user = current_user, now=datetime.now())