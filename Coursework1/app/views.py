from flask import render_template, redirect, url_for, flash, request
from app import app, db
from app.models import Assessment
from app.forms import AssessmentForm


# Route for our homepage displaying all the assessments
@app.route('/')
def index():
    # This function is to get all the assessments
    assessments = Assessment.query.all()
    return render_template(
        'index.html',
        title='All Assessments',
        assessments=assessments
    )


# Route to add a new assessment
@app.route('/add', methods=['GET', 'POST'])
def add_assessment():
    form = AssessmentForm()
    duplicate_title = False

    if form.validate_on_submit():
        # Check if an assessment with the same title already exists
        existing_assessment = Assessment.query.filter_by(
            title=form.title.data).first()
        if existing_assessment:
            duplicate_title = True
        else:
            # Add the new assessment to the database
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

    return render_template(
        'add_assessment.html',
        title='Add Assessment',
        form=form,
        duplicate_title=duplicate_title
    )


# Route to edit an existing assessment
@app.route('/edit/<int:assessment_id>', methods=['GET', 'POST'])
def edit_assessment(assessment_id):
    assessment = Assessment.query.get_or_404(assessment_id)
    form = AssessmentForm(obj=assessment)

    next_page = request.args.get('next', 'index')

    if form.validate_on_submit():
        assessment.title = form.title.data
        assessment.module_code = form.module_code.data
        assessment.deadline_date = form.deadline_date.data
        assessment.description = form.description.data
        assessment.is_complete = form.is_complete.data
        db.session.commit()
        flash('Assessment updated successfully!')
        return redirect(url_for(next_page))

    return render_template(
        'edit_assessment.html',
        title='Edit Assessment',
        form=form,
        assessment=assessment
    )


# Route to delete an assessment
@app.route('/delete/<int:assessment_id>', methods=['POST'])
def delete_assessment(assessment_id):
    assessment = Assessment.query.get_or_404(assessment_id)
    db.session.delete(assessment)
    db.session.commit()
    flash('Assessment deleted successfully!', 'success')
    return redirect(url_for('index'))


# Route to mark an assessment as complete
@app.route('/mark_complete/<int:assessment_id>', methods=['POST'])
def mark_complete(assessment_id):
    assessment = Assessment.query.get_or_404(assessment_id)
    if not assessment.is_complete:
        assessment.is_complete = True
        db.session.commit()
        flash(f'Assessment "{assessment.title}" marked as complete!')
    return redirect(request.referrer)


# Route to view all completed assessments
@app.route('/view_completed')
def view_completed():
    completed_assessments = Assessment.query.filter_by(is_complete=True).all()
    return render_template(
        'view_completed.html',
        title='Completed Assessments',
        assessments=completed_assessments
    )


# Route to view all uncompleted assessments
@app.route('/view_uncompleted')
def view_uncompleted():
    uncompleted_assessments = Assessment.query.filter_by(
        is_complete=False).all()
    return render_template(
        'view_uncompleted.html',
        title='Uncompleted Assessments',
        assessments=uncompleted_assessments
    )


# Route to mark an assessment as incomplete
@app.route('/mark_incomplete/<int:assessment_id>', methods=['POST'])
def mark_incomplete(assessment_id):
    assessment = Assessment.query.get_or_404(assessment_id)
    assessment.is_complete = False
    db.session.commit()

    next_page = request.args.get('next')
    if next_page:
        return redirect(url_for(next_page))
    return redirect(url_for('index'))
