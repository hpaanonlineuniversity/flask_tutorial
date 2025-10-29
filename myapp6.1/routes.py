from flask import render_template, request, jsonify, redirect, url_for
from models import Person
from bson import ObjectId

def register_routes(app, mongo):
    
    @app.route('/', methods=['GET', 'POST'])
    def index():
        if request.method == 'GET':
            people = Person.get_all()
            # Convert ObjectId to string for template
            for person in people:
                person['_id'] = str(person['_id'])
            return render_template('index.html', people=people)
        
        elif request.method == 'POST':
            name = request.form.get('name')
            age = int(request.form.get('age'))
            job = request.form.get('job')
            
            person = Person(name=name, age=age, job=job)
            person.save()
            
            return redirect(url_for('index'))
    
    @app.route('/delete/<pid>', methods=['POST'])
    def delete(pid):
        Person.delete_by_id(pid)
        return redirect(url_for('index'))
    
    @app.route('/details/<pid>')
    def details(pid):
        person = Person.get_by_id(pid)
        if person:
            person['_id'] = str(person['_id'])
        return render_template('detail.html', person=person)