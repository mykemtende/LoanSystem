from django.shortcuts import render

from django.http import HttpResponseRedirect
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist

from .models import Account, Profile, Action, Detail
from . import logger
from .forms import LoanForm
from decimal import *

def authentication_check(request, required_roles=None, required_GET=None):
    """
    :param request: The page request
    :param required_roles: The role values of the users allowed to view the page
    :param required_GET: The GET values that the page needs to function properly
    :return: A redirect request if there's a problem, None otherwise
    """
    # Authentication check. Users not logged in cannot view this page.
    if not request.user.is_authenticated():
        request.session['alert_danger'] = "You must be logged into Loan  System to view that page."
        return HttpResponseRedirect('/')
    # Sanity check. Users without accounts cannot interact with  sys
    try:
        request.user.account
    except ObjectDoesNotExist:
        request.session['alert_danger'] = "Your account was not properly created, please try a different account."
        return HttpResponseRedirect('/logout/')
    # Permission Check.
    if required_roles and request.user.account.role not in required_roles:
        request.session['alert_danger'] = "You don't have permission to view that page."
        return HttpResponseRedirect('/error/denied/')
    # Validation Check. Make sure this page has any required GET keys.
    if required_GET:
        for key in required_GET:
            if key not in request.GET:
                request.session['alert_danger'] = "Looks like you tried to use a malformed URL."
                return HttpResponseRedirect('/error/denied/')


def parse_session(request, template_data=None):
    """
    Checks the session for any alert data. If there is alert data, it added to the given template data.
    :param request: The request to check session data for
    :param template_data: The dictionary to update
    :return: The updated dictionary
    """
    if template_data is None:
        template_data = {}
    if request.session.has_key('alert_success'):
        template_data['alert_success'] = request.session.get('alert_success')
        del request.session['alert_success']
    if request.session.has_key('alert_danger'):
        template_data['alert_danger'] = request.session.get('alert_danger')
        del request.session['alert_danger']
    return template_data


def register_user(email, password, firstname, lastname, role, IDNO=""):
    user = User.objects.create_user(
        email.lower(),
        email.lower(),
        password
    )
    profile = Profile(
        firstname=firstname,
        lastname=lastname,
        IDNO=IDNO,
    )
    profile.save()
    account = Account(
        role=role,
        profile=profile,
        user=user
    )
    account.save()
    detail = Detail(
        account=account
    )
    detail.save()
    logger.log(Action.ACTION_ACCOUNT, "Account registered", account)
    return user

def sanitize_js(string):
    return string.replace("\\", "\\\\").replace("'", "\\'")


#loan

def rootfinding_amortization(i, P, n, A):
    return P*(i + (i/((1+i)**n - 1))) - A


def payment(principal, apr, number_of_periods):
    if apr == 0:
        periodic_payment = principal/number_of_periods
    else:
        monthly_interest_rate = apr/12
        periodic_payment = principal*(monthly_interest_rate + (monthly_interest_rate/((1+monthly_interest_rate)**number_of_periods - 1)))
    return periodic_payment


def loan(request):
    if request.method == 'POST':
        form = LoanForm(request.POST)
        if form.is_valid():
            # Gather and sanitize inputs
            amount_borrowed = form.cleaned_data['amount_borrowed']
            amountpay = form.cleaned_data['amountpay']
            company_apr = form.cleaned_data['company_borrowing_rate'] / Decimal(100)
            loan_periods = int(form.cleaned_data['months_borrowed'])

            # Calculated Values
            company_principle = amount_borrowed + amountpay #-


            # Monthly Payment Calculations
            company_monthly_payment = payment(company_principle, company_apr, loan_periods)
            #


            # Total Calculations
            company_total_amount = company_monthly_payment * loan_periods
            #

            # Interest  Calculations
            # 
            company_total_interest_Ksh = round(Decimal(company_total_amount) - company_principle, 2) #
            #

            #  Calculation
            company_apr = round(company_apr * 100, 4)

        

            # Return values to HTML page
            # Ksh amounts are formatted to exactly two decimal places
            return render(request, 'loan.html', {'form': form,
                                                 'company_total_amount': Decimal('%.2f' % company_total_amount),
                                                 'company_total_interest_Ksh': Decimal('%.2f' % company_total_interest_Ksh),
                                                 'company_monthly_payment': Decimal('%.2f' % company_monthly_payment),
                                                 'real_company_interest_rate': company_apr})
    else:
        form = LoanForm()
    return render(request, 'loan.html', {'form': form})