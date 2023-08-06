# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
#
# Also note: You'll have to insert the output of 'django-admin sqlcustom [app_label]'
# into your database.
from __future__ import unicode_literals

from django.db import models

class Ca(models.Model):
    name = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'ca'


class Census(models.Model):
    title = models.CharField(max_length=100)
    postalcode = models.IntegerField(db_column='postalCode', blank=True, null=True)  # Field name made lowercase.
    estado = models.CharField(max_length=7)
    ca = models.ForeignKey(Ca)

    class Meta:
        managed = False
        db_table = 'census'


class Cookie(models.Model):
    number_id = models.CharField(primary_key=True, max_length=40)
    user_account = models.ForeignKey('UserAccount')

    class Meta:
        managed = False
        db_table = 'cookie'

class OptionPerVote(models.Model):
    vote = models.ForeignKey('Vote')
    question_option = models.ForeignKey('QuestionOption')

    class Meta:
        managed = False
        db_table = 'option_per_vote'


class Poll(models.Model):
    title = models.CharField(max_length=50)
    description = models.CharField(max_length=150, blank=True, null=True)
    startdate = models.DateField(db_column='startDate')  # Field name made lowercase.
    enddate = models.DateField(db_column='endDate')  # Field name made lowercase.
    census = models.ForeignKey(Census)
    participantes_admitidos = models.IntegerField()
    votos_actuales = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'poll'


class Question(models.Model):
    title = models.CharField(max_length=50)
    description = models.CharField(max_length=150, blank=True, null=True)
    optional = models.IntegerField()
    multiple = models.IntegerField()
    poll = models.ForeignKey(Poll)

    class Meta:
        managed = False
        db_table = 'question'


class QuestionOption(models.Model):
    description = models.CharField(max_length=150, blank=True, null=True)
    question = models.ForeignKey(Question)

    class Meta:
        managed = False
        db_table = 'question_option'

class Role(models.Model):
    name = models.CharField(max_length=10)

    class Meta:
        managed = False
        db_table = 'role'

class User(models.Model):
    name = models.CharField(max_length=100)
    surname = models.CharField(max_length=200)
    genre = models.CharField(max_length=1)
    fechanac = models.DateField()
    dni = models.CharField(max_length=9)
    ca = models.ForeignKey(Ca)
    user_account = models.ForeignKey('UserAccount')

    class Meta:
        managed = False
        db_table = 'user'

class UserAccount(models.Model):
    username = models.CharField(unique=True, max_length=50)
    password = models.CharField(max_length=50)
    email = models.CharField(max_length=100)
    role = models.ForeignKey(Role)

    class Meta:
        managed = False
        db_table = 'user_account'

class UserAccountPerCensus(models.Model):
    census = models.ForeignKey(Census)
    user_account = models.ForeignKey(UserAccount)

    class Meta:
        managed = False
        db_table = 'user_account_per_census'

class Vote(models.Model):
    token = models.CharField(max_length=150)
    vote_type = models.ForeignKey('VoteType')
    vote_date = models.DateField()

    class Meta:
        managed = False
        db_table = 'vote'

class VoteType(models.Model):
    name = models.CharField(max_length=10)

    class Meta:
        managed = False
        db_table = 'vote_type'
