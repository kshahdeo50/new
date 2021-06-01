from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator,MinValueValidator

GROUP_CHOICE = (
    ('billing','Billing'),
    ('admin', 'Admin'),
    ('readonly', 'ReadOnly'),
)

DATABASE_TYPE = (
    ('RDS MySql','RDS MYSQL'),
    ('RDS PostGreSQl','RDS PostgreSQL'),
    ('AURORA MYSQL','Aurora Mysql'),
    ('AURORA PostGreSQL','Aurora PostGreSQl'),
)
REGIONS = (
    ('us-east-1','us-east-1'),
    ('us-east-2','us-east-2'),
    ('us-west-1','us-west-2'),
)


# Create your models here.

class project(models.Model):
    user = models.ForeignKey(User, on_delete= models.CASCADE)
    Project_Name = models.CharField(max_length=100)
    Environment_Name = models.CharField(max_length = 100)
    region = models.CharField(choices = REGIONS, max_length = 100)
    vpc_cidr = models.CharField(max_length = 100)
    email   = models.CharField(max_length = 100)

class rds(models.Model):
    user = models.ForeignKey(User,on_delete = models.CASCADE)
    rds_username = models.CharField(max_length = 100)
    rds_password = models.CharField(max_length = 100)
    rds_type = models.CharField(choices = DATABASE_TYPE, max_length = 100)
    date = models.DateTimeField(auto_now_add = True)

class iam(models.Model):
    user = models.ForeignKey(User, on_delete = models.CASCADE)
    username = models.CharField(max_length = 100)
    groupname = models.CharField(choices = GROUP_CHOICE, max_length = 100)


class bill(models.Model):
    user = models.ForeignKey(User,on_delete = models.CASCADE)
    email = models.CharField(max_length = 100)
    budget = models.CharField(max_length = 100)


class final(models.Model):
    Project_Name = models.CharField(max_length=100)
    Environment_Name = models.CharField(max_length=100)
    Region= models.CharField(max_length=100)
    VPC_CIDR= models.CharField(max_length=100)
    RDS_Username = models.CharField(max_length=100)
    RDS_Password= models.CharField(max_length=100)
    RDS_Type = models.CharField(max_length=100)
    IAM_Username = models.CharField(max_length=100)
    IAM_Groupname = models.CharField(max_length=100)
    Email = models.CharField(max_length=100)
    Budget = models.CharField(max_length=100)
    date = models.DateTimeField(auto_now_add = True)





