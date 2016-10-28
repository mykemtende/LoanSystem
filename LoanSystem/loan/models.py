from __future__ import unicode_literals

from datetime import date

from django.db import models
from django.contrib.auth.models import User


class Location(models.Model):
    place = models.CharField(max_length=50)
    postalcode = models.CharField(max_length=50)
    address = models.CharField(max_length=50)
    county = models.CharField(max_length=50)
    country = models.CharField(max_length=50, default="KENYA")

    def __str__(self):
        return self.address

    class Admin:
        list_display = ('place', 'country')


class Organization(models.Model):
    name = models.CharField(max_length=50)
    phone = models.CharField(max_length=20)
    location = models.OneToOneField(Location)

    def __str__(self):
        return self.name

    class Admin:
        list_display = (
            'name',
            'phone',
            'location'
        )


class Profile(models.Model):
    GENDER = (
        ('M', "Male"),
        ('F', "Female"),
    )

    @staticmethod
    def to_gender(key):
        for item in Profile.GENDER:
            if item[0] == key:
                return item[1]
        return "None"

    firstname = models.CharField(blank=True, max_length=50)
    lastname = models.CharField(blank=True, max_length=50)
    IDNO = models.CharField(blank=True, max_length=50)
    sex = models.CharField(blank=True, max_length=1, choices=GENDER)
    birthday = models.DateField(default=date(1900, 1, 1))
    phone = models.CharField(blank=True, max_length=20)
    address = models.CharField(blank=True, max_length=250)
    created = models.DateTimeField(auto_now_add=True)
    company = models.ForeignKey(Organization, null=True, related_name="profiles_company")
    primaryCompany = models.ForeignKey('Account', null=True, related_name="profiles_primarycompany")

    def get_populated_fields(self):
        """
        This is used by the form to collect the data.
        """
        fields = {}
        if self.firstname is not None:
            fields['firstname'] = self.firstname
        if self.lastname is not None:
            fields['lastname'] = self.lastname
        if self.sex is not None:
            fields['sex'] = self.sex
        if not self.birthday.year == 1000:
            fields['birthday'] = self.birthday
        if self.phone is not None:
            fields['phone'] = self.phone
        if self.address is not None:
            fields['course'] = self.address 
        if self.IDNO is not None:
            fields['IDNO'] = self.IDNO 
        if self.company is not None:
            fields['company'] = self.company
        if self.primaryCompany is not None:
            fields['primaryCompany'] = self.primaryCompany
        return fields

    def __str__(self):
        return self.firstname + " " + self.lastname


class Account(models.Model):
    ACCOUNT_UNKNOWN = 0
    ACCOUNT_CUSTOMER = 10
    ACCOUNT_LOANOFFICER = 30
    ACCOUNT_ADMIN = 40
    ACCOUNT_TYPES = (
        (ACCOUNT_UNKNOWN, "Unknown"),
        (ACCOUNT_CUSTOMER, "Customer"),
        (ACCOUNT_LOANOFFICER, "Loan Officer"),
        (ACCOUNT_ADMIN, "Admin"),
    )
    EMPLOYEE_TYPES = (
        (ACCOUNT_LOANOFFICER, "Loan Officer"),
        (ACCOUNT_ADMIN, "Admin"),
    )

    @staticmethod
    def to_name(key):
        """
        Parses an integer value to a string representing an account role.
        :param key: The account role as a int
        :return: The string representation of the name for the account role
        """
        for item in Account.ACCOUNT_TYPES:
            if item[0] == key:
                return item[1]
        return "None"

    @staticmethod
    def to_value(key):
        """
        Parses an string to a integer representing an account role.
        :param key: The account role as a string
        :return: The integer representation of the account role
        """
        key = key.lower()
        for item in Account.ACCOUNT_TYPES:
            if item[1].lower() == key:
                return item[0]
        return 0

    role = models.IntegerField(default=0, choices=ACCOUNT_TYPES)
    profile = models.OneToOneField(Profile)
    user = models.OneToOneField(User)
    approved = models.IntegerField(default=0, null=False) #new field for approval

    def __str__(self):
        if self.role == 30:
            return "Loan Officer. " + self.profile.__str__()
        elif self.role == 10:
            return "Customer. " + self.profile.__str__()
        elif self.role == 40:
            return "Administrator. " + self.profile.__str__()
        else:
            return self.profile.__str__()

    class Admin:
        list_display = (
            'role',
            'profile',
            'user'
        )


class Action(models.Model):
    ACTION_NONE = 0
    ACTION_ACCOUNT = 1
    ACTION_CUSTOMER = 2
    ACTION_ADMIN = 3
    ACTION_LOANOFFICER = 4
    ACTION_DETAIL = 8
    ACTION_MESSAGE = 9
    ACTION_TYPES = (
        (ACTION_NONE, "None"),
        (ACTION_ACCOUNT, "Account"),
        (ACTION_CUSTOMER, "Customer"),
        (ACTION_ADMIN, "Admin"),
        (ACTION_LOANOFFICER, "Loanofficer"),
        (ACTION_DETAIL, "Customer Details"),
        (ACTION_MESSAGE, "Message"),
    )

    @staticmethod
    def to_name(key):
        """
        Parses an integer value to a string representing an action.
        :param key: The action number
        :return: The string representation of the name for action
        """
        for item in Action.ACTION_TYPES:
            if item[0] == key:
                return item[1]
        return "None"

    @staticmethod
    def to_value(key):
        """
        Parses an string to a integer representing an account role.
        :param key: The account role as a string
        :return: The integer representation of the account role
        """
        key = key.lower()
        for item in Action.ACTION_TYPES:
            if item[1].lower() == key:
                return item[0]
        return 0

    type = models.IntegerField(default=0, choices=ACTION_TYPES)
    timePerformed = models.DateTimeField(auto_now_add=True)
    description = models.CharField(max_length=100)
    account = models.ForeignKey(Account, related_name="actions_account")
    """
    Might have to add this field to specify:
    - where action was committed
    - exclude actions that are done at a company for which a specific
      admin is not in control of ?
    company = models.ForeignKey(Company)
    """




class Message(models.Model):
    target = models.ForeignKey(Account, related_name="messages_target")
    sender = models.ForeignKey(Account, related_name="messages_sender")
    header = models.CharField(max_length=300)
    body = models.CharField(max_length=1000)
    sender_deleted = models.BooleanField(default=False)
    target_deleted = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)


class Notification(models.Model):
    account = models.ForeignKey(Account, related_name="notifications_account")
    message = models.CharField(max_length=200)
    read = models.BooleanField(default=False)
    sent_timestamp = models.DateTimeField(auto_now_add=True)
    read_timestamp = models.DateTimeField(blank=True, null=True)




    
class Detail(models.Model):
    LEVEL = (
        ('Ksh: 1,000,000','Ksh: 1,000,000'),
        ('Ksh: 500,000','Ksh: 500,000'),
        ('Ksh: 100,000','Ksh: 100,000'),
        ('Ksh: 50,000','Ksh: 50,000'),
        ('Ksh: 20,000','Ksh: 20,000'),
        ('Ksh: 10,000','Ksh: 10,000'),
        ('Ksh: 5,000','Ksh: 5,000'),
        ('Other','Other'),
      
    )

    @staticmethod
    def to_blood(key):
        for item in Detail.LEVEL:
            if item[0] == key:
                return item[1]
        return "None"

    account = models.ForeignKey(Account, related_name="detail_account")
    level = models.CharField(max_length=15, choices=LEVEL)
    address = models.CharField(max_length=100)
    description = models.CharField(max_length=700)

    def get_populated_fields(self):
        fields = {
            'account': self.account.pk,
            'level': self.level,
            'address': self.address,
            'description': self.description,
        }
        return fields
