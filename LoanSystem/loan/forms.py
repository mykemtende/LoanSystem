from datetime import date

from django import forms
from django.contrib.auth.models import User
from django.contrib.auth import authenticate

from .models import Account, Profile, Organization,Detail, Message
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field, Div, HTML, Fieldset
from crispy_forms.bootstrap import PrependedText

def validate_username_available(username):
    """
    This is a validator that throws an error if the given username already exists.
    """

    if User.objects.filter(username__icontains=username).count():
        raise forms.ValidationError("That email is already registered")


def validate_username_exists(username):
    """
    This is a validator that throws an error if the given username doesn't exist.
    """
    if not User.objects.filter(username=username).count():
        raise forms.ValidationError("That email does not exist")


def validate_not_admitted(account):
    """
    This is a validator that throws an error if the student is already admitted.
    """
    queryset = Admission.objects.filter(account=account);
    if queryset.count():
        for admission in queryset:
            if admission.active:
                raise forms.ValidationError("student already admitted")


def validate_birthday(birthday):
    """
    This is a validator that checks if the date is realistic.
    """
    if birthday.year < (date.today().year - 200):
        raise forms.ValidationError("Please choose a later date")
    elif birthday > date.today():
        raise forms.ValidationError("Please choose an earlier date")


def setup_field(field, placeholder=None):
    """
    This configures the given field to play nice with the bootstrap theme. Additionally, you can add
    an additional argument to set a placeholder text on the field.
    """
    field.widget.attrs['class'] = 'form-control'
    if placeholder is not None:
        field.widget.attrs['placeholder'] = placeholder


class BasicForm(forms.Form):
    def disable_field(self, field):
        """
        Marks the field as disabled.
        :param field: The name of the field
        """
        self.fields[field].widget.attrs['disabled'] = ""

    def mark_error(self, field, description):
        """
        Marks the given field as errous. The given description is displayed when the form it generated
        :param field: The name of the field
        :param description: The error description
        """
        self._errors[field] = self.error_class([description])
        del self.cleaned_data[field]

    def clear_errors(self):
        self._errors = {}


class LoginForm(BasicForm):
    email = forms.EmailField(max_length=50, validators=[validate_username_exists])
    setup_field(email, 'Enter email here')
    password = forms.CharField(max_length=50, widget=forms.PasswordInput())
    setup_field(password, "Enter password here")

    def clean(self):
        """
        This is to make sure the password is valid for the given email. We don't have to worry about
        the email being invalid because the field specific validators run before this clean function.
        """
        cleaned_data = super(LoginForm, self).clean()
        username = cleaned_data.get('email')
        password = cleaned_data.get('password')
        if username and password:
            user = authenticate(username=username, password=password)
            if user is None:
                self.mark_error('password', 'Incorrect password')
        return cleaned_data


class AccountRegisterForm(BasicForm):
    firstname = forms.CharField(label='First Name', max_length=50)
    setup_field(firstname, 'Enter first name here')
    lastname = forms.CharField(label='Last Name', max_length=50)
    setup_field(lastname, 'Enter a last name here')
    email = forms.EmailField(max_length=50, validators=[validate_username_available])
    setup_field(email, 'Enter email here')
    password_first = forms.CharField(label='Password', min_length=1, max_length=50, widget=forms.PasswordInput())
    setup_field(password_first, "Enter password here")
    password_second = forms.CharField(label='', min_length=1, max_length=50, widget=forms.PasswordInput())
    setup_field(password_second, "Enter password again")

    def clean(self):
        """
        This is to make sure both passwords fields have the same values in them. If they don't mark
        them as erroneous.
        """
        cleaned_data = super(AccountRegisterForm, self).clean()
        password_first = cleaned_data.get('password_first')
        password_second = cleaned_data.get('password_second')
        if password_first and password_second and password_first != password_second:
            self.mark_error('password_second', 'Passwords do not match')
        return cleaned_data


class CustomerRegisterForm(AccountRegisterForm):
    IDNO = forms.CharField(max_length=50)
    setup_field(IDNO, 'Enter your National ID Number:')


class PasswordForm(BasicForm):
    password_current = forms.CharField(label='Current', max_length=50, widget=forms.PasswordInput())
    setup_field(password_current, 'Enter your current password here')
    password_first = forms.CharField(label='New', max_length=50, widget=forms.PasswordInput())
    setup_field(password_first, "Enter new password here")
    password_second = forms.CharField(label='', max_length=50, widget=forms.PasswordInput())
    setup_field(password_second, "Enter new password again")

    def clean(self):
        """
        This is to make sure both passwords fields have the same values in them. If they don't, mark
        them as erroneous. Also check if the current and new passwords are they same. If they are, then
        mark them as erroneous (we want different passwords).
        """
        cleaned_data = super(PasswordForm, self).clean()
        password_current = cleaned_data.get('password_current')
        password_first = cleaned_data.get('password_first')
        password_second = cleaned_data.get('password_second')
        if password_first and password_second:
            if password_first != password_second:
                self.mark_error('password_second', 'Passwords do not match')
            if password_current and password_current == password_first:
                self.mark_error('password_current', 'Your current and new passwords must be different')
        return cleaned_data


class ProfileForm(BasicForm):
    firstname = forms.CharField(label='First Name', max_length=50)
    setup_field(firstname, 'Enter first name here')
    lastname = forms.CharField(label='Last Name', max_length=50)
    setup_field(lastname, 'Enter a last name here')
    IDNO = forms.CharField(max_length=50)
    setup_field(IDNO, "Enter your National ID Number")
    sex = forms.ChoiceField(required=False, choices=Profile.GENDER)
    setup_field(sex)
    birthday = forms.DateField(required=False, validators=[validate_birthday])
    setup_field(birthday, 'Enter birthday as YYYY-MM-DD')
    phone = forms.CharField(required=False, max_length=20)
    setup_field(phone, 'Enter phone number here')
    address = forms.CharField(required=False, max_length=250)
    setup_field(address, 'Enter your address here')
    company = forms.ModelChoiceField(label="Organization", required=False, queryset=Organization.objects.all())
    setup_field(company)
    #primaryCompany = forms.ModelChoiceField(label="Primary Company", required=False, queryset=Account.objects.filter(role=Account.ACCOUNT_LOANOFFICER))
    #setup_field(primaryCompany)

    def assign(self, profile):
        profile.firstname = self.cleaned_data['firstname']
        profile.lastname = self.cleaned_data['lastname']
        profile.sex = self.cleaned_data['sex']
        if self.cleaned_data['birthday'] is not None:
            profile.birthday = self.cleaned_data['birthday']
        profile.phone = self.cleaned_data['phone']
        profile.address = self.cleaned_data['address']
        profile.IDNO = self.cleaned_data['IDNO']
        profile.company = self.cleaned_data['company']
        #profile.primaryCompany = self.cleaned_data['primaryCompany']


class EmployeeProfileForm(ProfileForm):
    IDNO =    forms.CharField(required=False, max_length=50)
    setup_field(IDNO ,   "Enter your id Number")




class EmployeeRegisterForm(BasicForm):
    firstname = forms.CharField(label='First Name', max_length=50)
    setup_field(firstname, 'Enter first name here')
    lastname = forms.CharField(label='Last Name', max_length=50)
    setup_field(lastname, 'Enter a last name here')
    email = forms.EmailField(max_length=50, validators=[validate_username_available])
    setup_field(email, 'Enter email here')
    password_first = forms.CharField(label='Password', min_length=1, max_length=50, widget=forms.PasswordInput())
    setup_field(password_first, "Enter password here")
    password_second = forms.CharField(label='', min_length=1, max_length=50, widget=forms.PasswordInput())
    setup_field(password_second, "Enter password again")
    employee = forms.ChoiceField(required=False, choices=Account.EMPLOYEE_TYPES)
    setup_field(employee)

    def clean(self):
        """
        This is to make sure both passwords fields have the same values in them. If they don't mark
        them as errous.
        """
        cleaned_data = super(EmployeeRegisterForm, self).clean()
        password_first = cleaned_data.get('password_first')
        password_second = cleaned_data.get('password_second')
        if password_first and password_second and password_first != password_second:
            self.mark_error('password_second', 'Passwords do not match')
        return cleaned_data






class OrganizationForm(BasicForm):
    place = forms.CharField(max_length=50)
    setup_field(place, "Enter the Organization's place")
    postalcode = forms.CharField(max_length=50)
    setup_field(postalcode, "Enter the Organization's postal code")
    address = forms.CharField(max_length=50)
    setup_field(address, "Enter the Organization's address")
    county= forms.CharField(max_length=50)
    setup_field(county, "Enter the Organization's county")
    name = forms.CharField(max_length=50)
    setup_field(name, "Enter the Organization's name")
    phone = forms.CharField(max_length=50)
    setup_field(phone, "Enter the Organization's primary phone number")



class DetailForm(BasicForm):
    account = forms.ModelChoiceField(label="Customer Name", queryset=Account.objects.filter(role=Account.ACCOUNT_CUSTOMER))
    setup_field(account)
    level = forms.ChoiceField(label='Loan level', choices=Detail.LEVEL, required=False)
    setup_field(level)
    address = forms.CharField(max_length=100, required=False)
    setup_field(address, "Enter address here")
    description = forms.CharField(max_length=500, required=False)
    setup_field(description, "Enter your detail information here")

    def assign(self, detail):
        detail.account = self.cleaned_data['account']
        detail.level = self.cleaned_data['level']
        detail.address = self.cleaned_data['address']
        detail.description = self.cleaned_data['description']
    
class MessageForm(BasicForm):
    target = forms.ModelChoiceField(queryset=Account.objects.all(), label="To")
    setup_field(target)
    header = forms.CharField(max_length=300)
    setup_field(header, "Message header")
    body = forms.CharField(max_length=1000)
    setup_field(body, "Message body")

    def generate(self, sender):
        return Message(
            target=self.cleaned_data['target'],
            sender=sender,
            header=self.cleaned_data['header'],
            body=self.cleaned_data['body'],
        )



COMPOUND_PERIOD = (
    (1, u"Annually"),
    (2, u"Semi Annually"),
    (4, u"Quarterly"),
    (12, u"Monthly"),
)


class LoanForm(forms.Form):
    amount_borrowed = forms.DecimalField(label='Amount to borrow',
                                   decimal_places=2,
                                   help_text=u"Amount to be borrowed ")
    amountpay = forms.DecimalField(label='Cash to paid periodically',
                                decimal_places=2,
                                help_text=u"The  amount client supposed to pay monthly")
    company_borrowing_rate = forms.DecimalField(label='company borrowing rate',
                                             decimal_places=2,
                                             help_text=u"The interest rate the company is offering for a loan.")


    months_borrowed = forms.ChoiceField(choices=((x, x) for x in range(1, 85)))

    def __init__(self, *args, **kwargs):
        self.helper = FormHelper()
        self.helper.disable_csrf = False
        self.helper.form_tag = True
        self.helper.layout = Layout(
            Div(
                Fieldset(
                    'Company loan Rate',
                    Div(
                        Div(PrependedText('amount_borrowed', 'Ksh:', placeholder='Amount Borrowed'), css_class="col-lg-12"),
                        Div(PrependedText('amountpay', 'Ksh: ', placeholder='Cash Payment Monthly '), css_class="col-lg-12"),
                        Div(PrependedText('company_borrowing_rate', '%', placeholder='Company borrowing rate'), css_class="col-lg-12"),
                        Div(Field('months_borrowed'), css_class="col-lg-12"),
                        css_class="row"
                    ),
                ),
            ),
            Div(
                Div(
                    HTML('<input title="Calculate" type="submit" name="submit" value="Calculate" class="btn btn-primary btn-lg"/>'),
                    css_class="col-lg-12",
                ),
                css_class="row",
            ),
        )
        super(LoanForm, self).__init__(*args, **kwargs)
