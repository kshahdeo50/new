import os
import django
import numpy as np
 
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'cloud.settings')
django.setup()
from app.models import project, rds,iam,bill,final



rdso = rds.objects.all().last()
proj = project.objects.all().last()
iamo = iam.objects.all().last()
budo = bill.objects.all().last()








proj_name = proj.Project_Name
proj_env  = proj.Environment_Name
proj_vpc  = proj.vpc_cidr
bill      = budo.budget
proj_email = budo.email
iam_user   = iamo.username
iam_group  = iamo.groupname
rds_type  = rdso.rds_type
rds_username = rdso.rds_username
rds_password = rdso.rds_password
region = proj.region


f = final(Project_Name = proj_name,Environment_Name = proj_env,Region=region  ,
VPC_CIDR =proj_vpc ,RDS_Username =rds_username ,RDS_Password=rds_password,RDS_Type=rds_type,IAM_Username=iam_user,
IAM_Groupname=iam_group,Email=proj_email,Budget=bill)
f.save()




f = open('vars.tf','w')
f.write((' variable "project_name"  { default = ' +repr(proj_name) + '}').replace("'","") + '\n')
f.write((' variable "environment_name" { default = '+repr(proj_env) + '}').replace("'","")+ '\n')
f.write((' variable "cidr_block"  { default = ' +repr(proj_vpc) + '}').replace("'","") + '\n')
f.write((' variable "email_adderss"{ default = '+repr(proj_email) + '}').replace("'","")+'\n')
f.write((' variable "billing_limit" { default =' +repr(bill) + '}').replace("'","")+'\n')
f.write((' variable "iam_user"{ default ='+   repr(iam_user) + '}').replace("'","")+'\n')
f.write((' variable "group_name"{ default = ' +repr(iam_group) + '}').replace("'","")+'\n')
f.write((' variable "db_instance_username"{ default ='+repr(rds_username) +'\n' +'sensitive = true }').replace("'","")+'\n')
f.write((' variable "db_instance_password" { default = ' +repr(rds_password) +'\n' +'sensitive = true }').replace("'","")+'\n')
f.write((' variable "db_security_port" { default = 5432 }').replace("'","")+'\n')
    
f.close()

f = open('variables.tfvars','w')

f.write(('region = "'+repr(region)+'"').replace("'","")+'\n')
f.write(('project_name = "'+repr(proj_name)+'"').replace("'","")+'\n')
f.write(('cidr_block = "'+repr(proj_vpc)+'"').replace("'","")+'\n')
f.write(('environment_name = "'+repr(proj_env) + '"').replace("'","")+ '\n')

f.write(('email_address = ["'+repr(proj_email) + '"]').replace("'","")+'\n')

f.write(('billing_limit = "' +repr(bill) + '"').replace("'","")+'\n')
f.write(('iam_user = "'+   repr(iam_user) + '"').replace("'","")+'\n')
f.write(('group_name = "' +repr(iam_group) + '"').replace("'","")+'\n')
f.write(('db_instance_username = "'+repr(rds_username) + '"').replace("'","")+'\n')
f.write(('db_instance_password = "' +repr(rds_password) + '"').replace("'","")+'\n')
if rds_type == 'RDS MySql' or rds_type == 'AURORA MYSQL':
    f.write(('db_security_port  = 3306  ').replace("'","")+'\n')
else :
    f.write(('db_security_port  = 5432').replace("'","")+'\n')
f.close()
print(proj_name)
print(proj_env)
print(proj_vpc)
print(proj_email)




