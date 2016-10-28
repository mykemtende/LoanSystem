from csv import QUOTE_MINIMAL, writer
import re

from django.shortcuts import render

from django.http import HttpResponseRedirect, HttpResponse
from django.db.utils import IntegrityError

from .forms import EmployeeRegisterForm, OrganizationForm

from .models import Account, Action, Organization, Location
from . import logger
from . import views


def users_view(request):
    # Authentication check.
    authentication_result = views.authentication_check(request, [Account.ACCOUNT_ADMIN])
    if authentication_result is not None: return authentication_result
    # Get the template data from the session
    template_data = views.parse_session(request)
    # Proceed with the rest of the view
    if request.method == 'POST':
        pk = request.POST['pk']
        role = request.POST['role']
        approved = request.POST['approved']
        account = Account.objects.get(pk=pk)
        if account is not None:
            account.role = role
            account.approved = approved
            account.save()
            logger.log(Action.ACTION_ADMIN, 'Admin modified ' + account.user.username + "'s role and approval status", request.user.account)
            template_data['alert_success'] = "Successfully Updated " + account.user.username + "'s role and approval status!"
    # Parse search sorting
    template_data['query'] = Account.objects.all().order_by('-role')
    return render(request, 'loan/admin/users.html', template_data)




def add_organization_view(request):
    # Authentication check.
    authentication_result = views.authentication_check(
        request,
        [Account.ACCOUNT_ADMIN]
    )
    if authentication_result is not None: return authentication_result
    # Get the template data from the session
    template_data = views.parse_session(
        request,
        {'form_button': "Add Organization"}
    )
    # Proceed with the rest of the view
    if request.method == 'POST':
        form = OrganizationForm(request.POST)
        if form.is_valid():
            location = Location(
                place=form.cleaned_data['place'],
                postalcode=form.cleaned_data['postalcode'],
                address=form.cleaned_data['address'],
                county=form.cleaned_data['county']
            )
            location.save()
            organization = Organization(
                name=form.cleaned_data['name'],
                phone=form.cleaned_data['phone'],
                location=location,
            )
            organization.save()
            form = OrganizationForm()  # Clean the form when the page is redisplayed
            template_data['alert_success'] = "Successfully added the Organization!"
    else:
        form = OrganizationForm()
    template_data['form'] = form
    return render(request, 'loan/admin/add_organization.html', template_data)


def createemployee_view(request):
    # Authentication check.
    authentication_result = views.authentication_check(request, [Account.ACCOUNT_ADMIN])
    if authentication_result is not None: return authentication_result
    # Get the template data from the session
    template_data = views.parse_session(
        request,
        {'form_button': "Register"}
    )
    # Proceed with the rest of the view
    if request.method == 'POST':
        form = EmployeeRegisterForm(request.POST)
        if form.is_valid():
            user = views.register_user(
                form.cleaned_data['email'],
                form.cleaned_data['password_first'],
                form.cleaned_data['firstname'],
                form.cleaned_data['lastname'],
                form.cleaned_data['employee']
            )
            logger.log(Action.ACTION_ADMIN, 'Admin registered ' + user.username, request.user.account)
            request.session['alert_success'] = "Successfully added new staff account."
            return HttpResponseRedirect('/admin/users/')
    else:
        form = EmployeeRegisterForm()
    template_data['form'] = form
    return render(request, 'loan/admin/createemployee.html', template_data)

