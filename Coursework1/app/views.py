from app import app, db
from flask import render_template, redirect, url_for, flash
from app.forms import AssessmentForm
from app.models import Assessment
from flask import request
from flask import flash, redirect, url_for

# Route for our homepage displaying all the assesments
@app.route('/')
def index():
    # This function is to get all the assessments
    assessments = Assessment.query.all()
    return render_template('index.html', title='All Assessments', assessments=assessments)

# Route to add a new assesment
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
        # this function is to add the new assesment to the 
        # database session
        db.session.add(new_assessment)
        
        # and this one is to commit the session to save the assesment
        db.session.commit()
        flash('Assessment added successfully!')
        # Once the assesment is added, we redirect to the homepage
        # to view all the updated assessments.
        return redirect(url_for('index'))
    return render_template('add_assessment.html', title='Add Assessment', form=form)

# Route to edit an existing assessment. 
@app.route('/edit/<int:assessment_id>', methods=['GET', 'POST'])
def edit_assessment(assessment_id):
    # Try to get the assesment by its ID
    # Return 404 if not found
    assessment = Assessment.query.get_or_404(assessment_id)
    # Then populate the form with current assesment data
    form = AssessmentForm(obj=assessment)

    # Get the 'next' parameter to redirect to the referring page after editing
    next_page = request.args.get('next', 'index')  # Defaults to 'index' if no 'next' is provided

    if form.validate_on_submit():
        # Update assessment with form data
        assessment.title = form.title.data
        assessment.module_code = form.module_code.data
        assessment.deadline_date = form.deadline_date.data
        assessment.description = form.description.data
        assessment.is_complete = form.is_complete.data
        # Then commit the changes
        db.session.commit()
        flash('Assessment updated successfully!')
        # Redirect to the previous view after updating the assessment
        return redirect(url_for(next_page))

    return render_template('edit_assessment.html', title='Edit Assessment', form=form, assessment=assessment)

# Route to delete an assessment. 
@app.route('/delete/<int:assessment_id>', methods=['POST'])
def delete_assessment(assessment_id):
    # Get the assesment by its ID
    assessment = Assessment.query.get_or_404(assessment_id)
    # Deletre the assesment
    db.session.delete(assessment)
    # Commit the changes
    db.session.commit()
    # To flash a success message
    flash('Assessment deleted successfully!', 'success')
    return redirect(url_for('index'))

# Route to mark an assessment as completee
@app.route('/mark_complete/<int:assessment_id>', methods=['POST'])
def mark_complete(assessment_id):
    assessment = Assessment.query.get_or_404(assessment_id)
    if not assessment.is_complete:
        assessment.is_complete = True
        db.session.commit()
        flash(f'Assessment "{assessment.title}" marked as complete!')
    return redirect(request.referrer)

# Route to view the completed assessments
@app.route('/view_completed')
def view_completed():
    completed_assessments = Assessment.query.filter_by(is_complete=True).all()
    return render_template('view_completed.html', title='Completed Assessments', assessments=completed_assessments)

# Route to view the uncompleted assessments
@app.route('/view_uncompleted')
def view_uncompleted():
    uncompleted_assessments = Assessment.query.filter_by(is_complete=False).all()
    return render_template('view_uncompleted.html', title='Uncompleted Assessments', assessments=uncompleted_assessments)

# Route to mark an assessment as incomplete
@app.route('/mark_incomplete/<int:assessment_id>', methods=['POST'])
def mark_incomplete(assessment_id):
    # Logic to mark the assessment as incomplete
    assessment = Assessment.query.get_or_404(assessment_id)
    assessment.is_complete = False
    db.session.commit()

    # Determine where to redirect after marking incomplete
    next_page = request.args.get('next')
    if next_page:
        return redirect(url_for(next_page))
    else:
        return redirect(url_for('index'))