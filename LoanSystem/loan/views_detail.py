from django.shortcuts import render
from django.http import HttpResponseRedirect

from .forms import DetailForm
from .models import Action, Account, Detail
from . import logger
from . import views


def list_view(request):
    # Authentication check.
    authentication_result = views.authentication_check(
        request,
        [ Account.ACCOUNT_LOANOFFICER]
    )
    if authentication_result is not None: return authentication_result
    # Get the template data from the session
    template_data = views.parse_session(request)
    # Proceed with the rest of the view
    template_data['query'] = Detail.objects.filter(account__role=Account.ACCOUNT_CUSTOMER)
    return render(request, 'loan/detail/list.html', template_data)


def apply_view(request):
    # Authentication check.
    authentication_result = views.authentication_check(
        request,
        [Account.ACCOUNT_CUSTOMER, Account.ACCOUNT_LOANOFFICER]
    )
    if authentication_result is not None: return authentication_result
    # 
    if 'pk' in request.GET:
        if request.user.account.role != Account.ACCOUNT_LOANOFFICER :
            request.session['alert_danger'] = "You don't have permission to view that page."
            return HttpResponseRedirect('/error/denied/')
        pk = request.GET['pk']
        try:
            detail = Detail.objects.get(pk=pk)
        except Exception:
            request.session['alert_danger'] = "The requested loan does not exist."
            return HttpResponseRedirect('/error/denied/')
    else:
        detail = Detail.objects.get(account=request.user.account)
    # Get the template data from the session
    template_data = views.parse_session(
        request, {
            'form_button': "Apply",
        })
    if 'pk' in request.GET:
        template_data['form_action'] = "?pk=" + pk
    # Proceed with the rest of the view
    request.POST._mutable = True
    request.POST['account'] = detail.account.pk
    if request.method == 'POST':
        form = DetailForm(request.POST)
        if form.is_valid():
            form.assign(detail)
            detail.save()
            logger.log(Action.ACTION_DETAIL, 'loan applied successfully', request.user.account)
            template_data['alert_success'] = "The loan application has been made successfully"
    else:
        form = DetailForm(detail.get_populated_fields())
    template_data['form'] = form
    form.disable_field('account')
    return render(request, 'loan/detail/apply.html', template_data)