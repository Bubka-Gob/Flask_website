from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user
from .models import User,Note, data_base
from sqlalchemy.sql import func  #time

home = Blueprint('home', __name__)

@home.route('/')
def home_page():
    return render_template('home_page.html')

@login_required
@home.route('/profile', methods= ['POST', 'GET'])
def profile():
    if request.method == 'GET':
        sort_notes()
        return render_template('profile_page.html', user_name=current_user.name,
                           user_first_name=current_user.first_name,
                           user_last_name=current_user.last_name,
                           email=current_user.email)
    else:
        if 'change_name' in request.form:
            if len(request.form['change_name']) < 4 or len(request.form['change_name']) > 20:
                flash('Invalid name', 'error')
                return render_template('profile_page.html', user_name=current_user.name,
                                       user_first_name=current_user.first_name,
                                       user_last_name=current_user.last_name,
                                       email=current_user.email)
            current_user.name = request.form['change_name']
            data_base.session.commit()
            flash('User name changed', 'success')
        else:
            if len(request.form['change_first_name']) > 30 or len(request.form['change_last_name']) > 30:
                flash('Invalid name', 'error')
                return render_template('profile_page.html', user_name=current_user.name,
                               user_first_name=current_user.first_name,
                               user_last_name=current_user.last_name,
                               email=current_user.email)
            else:
                current_user.first_name = request.form['change_first_name']
                current_user.last_name = request.form['change_last_name']
                data_base.session.commit()
                flash('User name changed', 'success')
                return render_template('profile_page.html', user_name=current_user.name,
                                       user_first_name=current_user.first_name,
                                       user_last_name=current_user.last_name,
                                       email=current_user.email)

@login_required
@home.route('/notes', methods= ['POST', 'GET'])
def notes():
    if request.method == 'GET':
        years = sort_notes()
        return render_template('notes_page.html', years=years)
    else:
        try:
            phrase = request.form['phrase']
            years = sort_notes(phrase)
            return render_template('notes_page.html', years=years)
        except:
            if len(request.form['note_name'])<1 or len(request.form['new_note'])<1:
                flash('Note can not be empty', 'error')
                return redirect(url_for('notes_page.html'))
            new_note = Note(note_name=request.form['note_name'], text=request.form['new_note'], user_id=current_user.id)
            data_base.session.add(new_note)
            data_base.session.commit()
            flash('Note added successfully', 'success')
            return redirect(url_for('home.notes'))

def sort_notes(phrase=None):
    user_notes = Note.query.filter_by(user_id=current_user.id).all()
    if phrase:
        temp = []
        for note in user_notes:
            if phrase.lower() in note.text.lower() or phrase.lower() in note.note_name.lower():
                temp.append(note)
        user_notes = temp
    user_notes_ids = [note.id for note in reversed(user_notes)]

    dates = []
    for note in reversed(user_notes):
        dates.append(str(note.date).split(' ')[0].split('-'))
    years = {}
    for splitted_date in dates:
        years[splitted_date[0]] = {}
    for splitted_date in dates:
        for year in years.keys():
            if year == splitted_date[0]:
                years[year][splitted_date[1]] = {}
    for splitted_date in dates:
        for year in years.keys():
            for month in years[year].keys():
                if month == splitted_date[1]:
                    years[year][month][splitted_date[2]] = Note.query.filter(
                        func.DATE(Note.date) == f'{year}-{month}-{splitted_date[2]}').\
                        filter(Note.id.in_(user_notes_ids)).all()
    return years
