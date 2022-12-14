from datetime import datetime
import json
from flask import Blueprint, render_template, request, flash, jsonify
from flask_login import login_required, current_user
from .models import Note

from app import db

views =  Blueprint('views', __name__)

@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
    now = datetime.now()
    date = now.strftime("%d/%m/%Y %H:%M:%S")
    if request.method == 'POST':
        note = request.form.get('note')
        due_date = request.form.get('due-date')

        new_note = Note(creation_date=date, note=note, user_id=current_user.id, status='Working', due_date=due_date)
        db.session.add(new_note)
        db.session.commit()


    return render_template('home.html', user=current_user)


@views.route('/delete-note', methods=['POST'])
@login_required
def delete_note():
    note = json.loads(request.data)
    noteId = note['noteId']
    note = Note.query.get(noteId)

    if note:
        db.session.delete(note)
        db.session.commit()
        return jsonify({})

@views.route('/complete-note', methods=['POST'])
@login_required
def complete_note():
    note = json.loads(request.data)
    noteId = note['noteId']
    note = Note.query.get(noteId)

    if note.completed == True:
        note.completed = False
        note.status = 'Working'
        db.session.commit()
    elif note.completed == False:
        note.completed = True
        note.status = 'Completed'
        db.session.commit()
        
    return jsonify({})