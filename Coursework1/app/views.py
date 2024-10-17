from app import app, db
from flask import render_template, redirect, url_for, flash
from app.forms import AssessmentForm
from app.models import Assessment

@app.route('/')
def index():
    assessments = Assessment.query.all()
    return render_template('index.html', title='All Assessments', assessments=assessments)

@app.route('/add', methods=['GET', 'POST'])
def add_assessment():
    form = AssessmentForm()
    if form.validate_on_submit():
        new_assessment = Assessment(
            title=form.title.data,
            module_code=form.module_code.data,
            deadline_date=form.deadline_date.data,
            description=form.description.data,
            is_complete=form.is_complete.data
        )
        db.session.add(new_assessment)
        db.session.commit()
        flash('Assessment added successfully!')
        return redirect(url_for('index'))
    return render_template('add_assessment.html', title='Add Assessment', form=form)

@app.route('/edit/<int:assessment_id>', methods=['GET', 'POST'])
def edit_assessment(assessment_id):
    assessment = Assessment.query.get_or_404(assessment_id)
    form = AssessmentForm(obj=assessment)
    if form.validate_on_submit():
        assessment.title = form.title.data
        assessment.module_code = form.module_code.data
        assessment.deadline_date = form.deadline_date.data
        assessment.description = form.description.data
        assessment.is_complete = form.is_complete.data
        db.session.commit()
        flash('Assessment updated successfully!')
        return redirect(url_for('index'))
    return render_template('edit_assessment.html', title='Edit Assessment', form=form, assessment=assessment)

@app.route('/delete/<int:assessment_id>', methods=['POST'])
def delete_assessment(assessment_id):
    assessment = Assessment.query.get_or_404(assessment_id)
    db.session.delete(assessment)
    db.session.commit()
    flash('Assessment deleted successfully!', 'success')
    return redirect(url_for('index'))

@app.route('/mark_complete/<int:assessment_id>', methods=['POST'])
def mark_complete(assessment_id):
    assessment = Assessment.query.get_or_404(assessment_id)
    if not assessment.is_complete:
        assessment.is_complete = True
        db.session.commit()
        flash(f'Assessment "{assessment.title}" marked as complete!')
    return redirect(url_for('index'))

@app.route('/view_completed')
def view_completed():
    completed_assessments = Assessment.query.filter_by(is_complete=True).all()
    return render_template('view_assessments.html', title='Completed Assessments', assessments=completed_assessments)

@app.route('/view_uncompleted')
def view_uncompleted():
    uncompleted_assessments = Assessment.query.filter_by(is_complete=False).all()
    return render_template('view_assessments.html', title='Uncompleted Assessments', assessments=uncompleted_assessments)
