import sys

from . import calculation
from flask import render_template, redirect, request, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from app.models.User import User
from app.extensions import db
from datetime import datetime
import app
from app.forms.calculation import FinanceForm, PartnerFinanceForm
from app.models.Calculation import CalculationService


@calculation.route('/my_finance', methods=['GET', 'POST'])
@login_required
def my_finance():
    form = FinanceForm()

    if request.method == 'GET':
        # fill in the form
        form.goal.data = str(int(current_user.goal))
        form.salary.data = current_user.salary
        form.salary_per_hour.data = current_user.salary_per_hour
        form.expenses_contribution.data = current_user.expenses_contribution
        form.house_care_hours_per_day.data = current_user.house_care_hours_per_day
        #form.working_hours_a_day.data = current_user.working_hours_a_day
        #form.care_hours_a_day.data = current_user.care_hours_a_day
        #form.life_hours_a_day.data = current_user.life_hours_a_day

        return render_template('fill_finance_state.html', form=form)

    else: #form.validate():
        # POST: update db
        current_user.goal = bool(int(form.goal.data))
        current_user.salary = form.salary.data
        current_user.salary_per_hour = form.salary_per_hour.data
        current_user.expenses_contribution = form.expenses_contribution.data
        current_user.house_care_hours_per_day = form.house_care_hours_per_day.data
        #current_user.working_hours_a_day = form.working_hours_a_day.data
        #current_user.care_hours_a_day = form.care_hours_a_day.data
        #current_user.life_hours_a_day = form.life_hours_a_day.data

        db.session.add(current_user)

        flash('Your finance data is succussfully edited！')

        return redirect(url_for('calculation.partner_finance'))

    #else:
        #flash('Please check your input and re-submit.')
        #return redirect(url_for('calculation.my_finance'))


@calculation.route('/partner_finance', methods=['GET', 'POST'])
@login_required
def partner_finance():
    form = PartnerFinanceForm()

    if request.method == 'POST' and form.validate():
        # POST: update db
        # create memory User object to memory partner tmp
        partner = User()
        partner.salary = form.salary.data
        partner.salary_per_hour = form.salary_per_hour.data
        partner.expenses_contribution = form.expenses_contribution.data
        partner.house_care_hours_per_day = form.house_care_hours_per_day.data
        #partner.working_hours_a_day = form.working_hours_a_day.data
        #partner.care_hours_a_day = form.care_hours_a_day.data
        #partner.life_hours_a_day = form.life_hours_a_day.data

        # calculate
        user_unfair, partner_unfair = CalculationService().calculate_unfair(current_user, partner)
        user_fair, partner_fair = CalculationService().calculate_fair(current_user, partner)

        results={}
        results['user_unfair'] = user_unfair
        results['partner_unfair'] = partner_unfair
        results['user_fair'] = user_fair
        results['partner_fair'] = partner_fair

        return render_template('result_visualisation.html', results=results)

    return render_template('handle_partner_finance_state.html', form=form)

