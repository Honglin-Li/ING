import sys

from . import calculation
from flask import render_template, redirect, request, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from app.models.User import User
from app.extensions import db
from datetime import datetime
import app
from app.forms.calculation import FinanceForm
from app.models.Calculation import CalculationService


@calculation.route('/my_finance', methods=['GET', 'POST'])
@login_required
def my_finance():
    form = FinanceForm()

    if request.method == 'GET':
        # fill in the form
        form.salary.data = current_user.salary
        form.external_income.data = current_user.external_income
        form.rent.data = current_user.rent
        form.load.data = current_user.load
        form.travel.data = current_user.travel
        form.insurance.data = current_user.insurance
        form.education.data = current_user.education
        form.personal_care.data = current_user.personal_care
        form.household.data = current_user.household
        form.childcare.data = current_user.childcare
        form.household_hours.data = current_user.household_hours
        form.childcare_hours.data = current_user.childcare_hours

        return render_template('fill_finance_state.html', form=form)

    elif form.validate():
        # POST: update db
        current_user.salary = form.salary.data
        current_user.external_income = form.external_income.data
        current_user.rent = form.rent.data
        current_user.load = form.load.data
        current_user.travel = form.travel.data
        current_user.insurance = form.insurance.data
        current_user.education = form.education.data
        current_user.personal_care = form.personal_care.data
        current_user.household = form.household.data
        current_user.childcare = form.childcare.data
        current_user.household_hours = form.household_hours.data
        current_user.childcare_hours = form.childcare_hours.data

        db.session.add(current_user)
        db.session.commit()

        flash('Your finance data is succussfully edited！')

        return redirect(url_for('calculation.partner_finance'))

    else:
        flash('Please check your input and re-submit.')
        return redirect(url_for('calculation.my_finance'))


@calculation.route('/partner_finance', methods=['GET', 'POST'])
@login_required
def partner_finance():
    form = FinanceForm()

    if request.method == 'POST' and form.validate():
        # POST: update db
        # create memory User object to memory partner tmp
        partner = User()
        partner.salary = form.salary.data
        partner.external_income = form.external_income.data
        partner.rent = form.rent.data
        partner.load = form.load.data
        partner.travel = form.travel.data
        partner.insurance = form.insurance.data
        partner.education = form.education.data
        partner.personal_care = form.personal_care.data
        partner.household = form.household.data
        partner.childcare = form.childcare.data
        partner.household_hours = form.household_hours.data
        partner.childcare_hours = form.childcare_hours.data

        # calculate
        results = CalculationService().calculate_individually(current_user, partner)

        return render_template('calculation_results.html', results=results)

    return render_template('handle_partner_finance_state.html', form=form)

