from datetime import datetime
from app.extensions import db
import copy


class CalculationService():
    def __init__(self):
        # unpaid hour salary
        self.basic_salary_per_hour = 17

    def calculate_unpaid_house_care_work(self, user):
        # calculate unpaid care work
        # 2 diff hour salary for unpaid house work
        if user.house_care_hours == 0: # speed up
            return 0

        opportunity_hours_per_month = 4 * (40 - (user.job_composition * 40))
        marketing_hours_per_month = 0

        if user.house_care_hours > opportunity_hours_per_month:
            marketing_hours_per_month = user.house_care_hours - opportunity_hours_per_month
        else:
            opportunity_hours_per_month = user.house_care_hours

        house_care_cost = marketing_hours_per_month * self.basic_salary_per_hour
        house_care_cost += opportunity_hours_per_month * user.salary_per_hour

        return house_care_cost

    def calculate_unfair(self, user1, partner1):
        user = copy.copy(user1)
        partner = copy.copy(partner1)

        # calculate unpaid work
        user.house_care_cost = self.calculate_unpaid_house_care_work(user)
        partner.house_care_cost = self.calculate_unpaid_house_care_work(partner)

        # total contribution
        user.total_contribution = user.expenses_contribution + user.house_care_cost
        partner.total_contribution = partner.expenses_contribution + partner.house_care_cost

        # pct of salary
        user.contribution_pct = user.total_contribution / user.salary
        partner.contribution_pct = partner.total_contribution / partner.salary

        user.contribution_show = f'{round(user.contribution_pct,4) * 100}%'
        partner.contribution_show = f'{round(partner.contribution_pct,4) * 100}%'

        # remain
        user.remain = user.salary - user.total_contribution
        partner.remain = partner.salary - partner.total_contribution

        # for pie chart
        total = user.total_contribution + partner.total_contribution

        user.user_expense = user.expenses_contribution / total
        user.user_unpaid = user.house_care_cost / total
        user.partner_expense = partner.expenses_contribution / total
        user.partner_unpaid = partner.house_care_cost / total

        return user, partner

    def calculate_fair(self, user1, partner1):
        user = copy.copy(user1)
        partner = copy.copy(partner1)

        # calculate unpaid work
        user.house_care_cost = self.calculate_unpaid_house_care_work(user)
        partner.house_care_cost = self.calculate_unpaid_house_care_work(partner)

        # total contribution
        user.total_contribution = user.expenses_contribution + user.house_care_cost
        partner.total_contribution = partner.expenses_contribution + partner.house_care_cost

        # total for a family
        #total_income = user.salary + partner.salary
        user.total_expense = user.total_contribution + partner.total_contribution
        user.joint_salary = user.salary + partner.salary
        user.alpha = user.total_expense / user.joint_salary # fairness scale
        #fair_scale = user.salary / (partner.salary + user.salary)

        # fair contribution
        user.fair_contribution = user.salary * user.alpha
        partner.fair_contribution = partner.salary * user.alpha#total_expense - user.fair_contribution

        # difference
        user.contribution_diff = user.total_contribution - user.fair_contribution
        partner.contribution_diff = partner.total_contribution - partner.fair_contribution

        # pct of salary
        user.contribution_pct = user.fair_contribution / user.salary
        partner.contribution_pct = partner.fair_contribution / partner.salary

        # remain
        user.remain = user.salary - user.fair_contribution
        partner.remain = partner.salary - partner.fair_contribution

        user.contribution_show = f'{ round(user.contribution_pct* 100, 2) }%'
        partner.contribution_show = f'{ round(partner.contribution_pct* 100, 2) }%'

        user.user_expense = user.expenses_contribution / user.total_expense
        user.user_unpaid = user.house_care_cost / user.total_expense
        user.partner_expense = partner.expenses_contribution / user.total_expense
        user.partner_unpaid = partner.house_care_cost / user.total_expense

        return user, partner






