import os
def mysql():
    type="db.t2.micro"
    insclass=str(input("Enter instance class you want to use [Default Value: db.t2.micro]: "))
    if insclass=='':
        insclass=type
    fin = open("terraform.tfvars", "rt")
    data = fin.read()
    data = data.replace('db.t2.micro', insclass)
    data = data.replace('5432','3306')
    fin.close()
    fin = open("terraform.tfvars", "wt")
    fin.write(data)
    fin.close()
    os.system('terraform init')
    os.system('terraform validate')
    os.system('terraform plan -target=module.vpc -target=module.mysql')
    os.system('terraform apply -target=module.vpc -target=module.mysql')
def postgresql():
    type="db.m5.large"
    insclass=str(input("Enter instance class you want to use [Default Value: db.m5.large]: "))
    if insclass=='':
        insclass=type
    fin = open("terraform.tfvars", "rt")
    data = fin.read()
    data = data.replace('db.m5.large', insclass)
    data = data.replace('3306','5432' )
    fin.close()
    fin = open("terraform.tfvars", "wt")
    fin.write(data)
    fin.close()
    os.system('terraform init')
    os.system('terraform validate')
    os.system('terraform plan -target=module.vpc -target=module.postgresql')
    os.system('terraform apply -target=module.vpc -target=module.postgresql')
def auroramysql():
    type="db.r5.large"
    insclass=str(input("Enter instance class you want to use [Default Value: db.r5.large]: "))
    if insclass=='':
        insclass=type
    fin = open("terraform.tfvars", "rt")
    data = fin.read()
    data = data.replace('db.r5.large', insclass)
    data = data.replace('5432','3306' )
    fin.close()
    fin = open("terraform.tfvars", "wt")
    fin.write(data)
    fin.close()
    os.system('terraform init')
    os.system('terraform validate')
    os.system('terraform plan -target=module.vpc -target=module.auroramysql')
    os.system('terraform apply -target=module.vpc -target=module.auroramysql')
def aurorapostgresql():
    vpc()
    type="db.r5.large"
    insclass=str(input("Enter instance class you want to use [Default Value: db.r5.large]: "))
    if insclass=='':
        insclass=type
    fin = open("terraform.tfvars", "rt")
    data = fin.read()
    data = data.replace('db.r5.large', insclass)
    data = data.replace('3306','5432' )
    fin.close()
    fin = open("terraform.tfvars", "wt")
    fin.write(data)
    fin.close()
    file = open("vpc.tf", "rt")
    data = file.read()
    data = data.replace('3306','5432' )
    file.close()
    os.system('terraform init')
    os.system('terraform validate')
    os.system('terraform plan -target=module.vpc -target=module.aurorapostgresql')
    os.system('terraform apply -target=module.vpc -target=module.aurorapostgresql')    
i=1
while i=='1':
    print(" ")
    print("Choose which type instance you wnat to create")
    print("To create RDS instance with MYSQL Engine, ENTER 1")
    print("To create RDS instance with POSTGRESQL Engine, ENTER 2")
    print("To create AURORA instance with MYSQL Engine, ENTER 3")
    print("To create AURORA instance with POSTGRESQL Engine, ENTER 4")    
    print("To exit, ENTER 0")
    s=input("Enter your choice: ")
    if s=='1':
        mysql()
    elif s=='2':
        postgresql()
    elif s=='3':
        auroramysql()
    elif s=='4':
        aurorapostgresql()
    else:
        print("Invalid choice, Enter Valid option")
    
    
