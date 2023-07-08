from datetime import datetime
from app.extensions import db


class CalculationService():
    def __init__(self):
        # unpaid hour salary
        self.hour_salary_for_household = 20
        self.hour_salary_for_child_care = 20

    def calculate_expense(self, user):
        # calculate expense of a person
        user_expense = user.rent + user.load + user.travel + user.insurance +\
                       user.household + user.childcare + user.education + user.personal_care

        user_unpaid = user.household_hours * self.hour_salary_for_household +\
                      user.childcare_hours * self.hour_salary_for_child_care

        user_total = user_expense + user_unpaid

        return user_total, user_expense, user_unpaid

    def calculate_current_state(self, owner, partner):
        # calculate for estimated partner spending
        owner_total, owner_expense, owner_unpaid = self.calculate_expense(owner)

        partner_total, partner_expense, partner_unpaid = self.calculate_expense(partner)

        results = {
            'owner_total': owner_total,
            'owner_expense': owner_expense,
            'owner_unpaid': owner_unpaid,
            'partner_total': partner_total,
            'partner_expense': partner_expense,
            'partner_unpaid': partner_unpaid,
            'diff_total': partner_total - owner_total,
            'diff_expense': partner_expense - owner_expense,
            'diff_unpaid': partner_unpaid - owner_unpaid
        }

        return results






