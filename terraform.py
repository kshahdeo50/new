import os
def vpc():
    terraformtfvars="""region = "us-east-1"
    environment_name = "dev"
    project_name = "abc"
    insclass = "db.t2.micr"
    """
    file = open("terraform.tfvars", "w")
    file.write(terraformtfvars)
    file.close()
    provider="""provider "aws" {
    region = var.region
    shared_credentials_file = "${var.project_name}.credentials"
    profile = var.environment_name
    }"""
    file = open("provider.tf", "w")
    file.write(provider) 
    file.close()
    project_credentials="""[dev]
    AWSAccessKeyId=AKIAJEPV7O4SJR5G6NKQ
    AWSSecretKey=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"""
    file = open("project.credentials", "w")
    file.write(project_credentials)
    file.close()
    variables="""variable "region" {}
    variable "environment_name" {}
    variable "project_name" {}
    var "insclass" {}
    """
    file = open("variables.tf", "w")
    file.write(variables)
    file.close()
    assignment="""resource "aws_vpc" "default" {
    cidr_block       = "10.0.0.0/16"
    instance_tenancy = "default"
    tags = {
    Name = "vpc_rds"
      }
    }
    output "vpc_id" {
    description = "The id of vpc"
    value       = aws_vpc.default.id
    }
    resource "aws_subnet" "pub" {
    vpc_id     = aws_vpc.default.id
    cidr_block = "10.0.5.0/24"
    map_public_ip_on_launch = "true"
    availability_zone = "ap-south-1a"
    tags = {
    Name = "public-sub"
       }
    }
    output "pub_id" {
    description = "id of public subnet"
    value       = aws_subnet.pub.id
    }
    resource "aws_internet_gateway" "igw" {
    vpc_id     = aws_vpc.default.id
    tags = {
    Name = "custom-igw"
       }
    }
    output "igw_id" {
    description = "Id of igw"
    value       = aws_internet_gateway.igw.id
    }
    resource "aws_route_table" "pub_route" {
    vpc_id = aws_vpc.default.id
      route {
          cidr_block = "0.0.0.0/0"
          gateway_id = aws_internet_gateway.igw.id
          }
       tags = {
           Name = "pub-route"
              }
    }
    output "pub_rid" {
      description = "Id of public route table"
      value       = aws_route_table.pub_route.id
    }
    resource "aws_route_table_association" "associate4" {
      subnet_id      = aws_subnet.pub.id
      route_table_id = aws_route_table.pub_route.id
    }
    resource "aws_subnet" "main" {
      vpc_id     = aws_vpc.default.id
      cidr_block = "10.0.1.0/24"
      availability_zone = "ap-south-1a"
      tags = {
        Name = "app-subnet-az-1"
        }
    }
    output "sub_id" {
      description = "id of public subnet"
      value       = aws_subnet.main.id
    }
    resource "aws_subnet" "pvt" {
      vpc_id     = aws_vpc.default.id
      cidr_block = "10.0.0.0/24"
      availability_zone = "ap-south-1b"
      tags = {
         Name = "app-subnet-az-2"
         }
    }
    output "pvt_id" {
      description = "Id of private subnet"
      value       = aws_subnet.pvt.id
      }
    resource "aws_subnet" "db" {
      vpc_id     = aws_vpc.default.id
      cidr_block = "10.0.3.0/24"
      availability_zone = "ap-south-1a"
      tags = {
         Name = "db-subnet-az-1"
         }
    }
    output "subrds_id" {
      description = "Id of rds private subnet"
      value       = aws_subnet.db.id
    }
    resource "aws_subnet" "rds" {
      vpc_id     = aws_vpc.default.id
      cidr_block = "10.0.2.0/24"
      availability_zone = "ap-south-1b"
      tags = {
         Name = "db-subnet-az-2"
         }
    }
    output "subrdss_id" {
      description = "Id of rds private subnet"
      value       = aws_subnet.rds.id
    }
    resource "aws_eip" "e-ip" {
      vpc              = true
      tags = {
         Name = "eip"
         }
    }
    resource "aws_nat_gateway" "gw" {
      allocation_id = aws_eip.e-ip.id
      subnet_id     = aws_subnet.pub.id
      tags = {
         Name = "gw NAT"
         }
    }
    resource "aws_route_table" "pvt_route" {
      vpc_id = aws_vpc.default.id
      route {
        cidr_block = "0.0.0.0/0"
        nat_gateway_id = aws_nat_gateway.gw.id
    }
    tags = {
       Name = "pvt-route"
       }
    }
    output "pvt_rid" {
      description = "Id of public route table"
      value       = aws_route_table.pvt_route.id
    }
    resource "aws_route_table_association" "associate" {
      subnet_id      = aws_subnet.main.id
      route_table_id = aws_route_table.pvt_route.id
    }
    resource "aws_route_table_association" "associate1" {
      subnet_id      = aws_subnet.db.id
      route_table_id = aws_route_table.pvt_route.id
    }
    resource "aws_route_table_association" "associate2" {
      subnet_id      = aws_subnet.pvt.id
      route_table_id = aws_route_table.pvt_route.id
    }
    resource "aws_route_table_association" "associate3" {
      subnet_id      = aws_subnet.rds.id
      route_table_id = aws_route_table.pvt_route.id
    }
    resource "aws_db_subnet_group" "subnet_group" {
      name        = "mysql_subnet_group"
      subnet_ids  = [aws_subnet.db.id,aws_subnet.rds.id]
      description = "subnet group for rds"
      tags = {
         Name = "subnetgroup"
         }
    }
    resource "aws_security_group" "app" {
      name = "app-sg"
      vpc_id = aws_vpc.default.id
      ingress {
          from_port   = 8080
          to_port     = 8080
          protocol    = "tcp"
          cidr_blocks = ["0.0.0.0/0"]
      }
      egress {
        from_port   = 0
        to_port     = 0
        protocol    = "-1"
        cidr_blocks = ["0.0.0.0/0"]
      }
      tags = {
        Name = "app-sg"
      }
    }
    resource "aws_security_group" "sqlapp" {
      name = "db-sg"
      vpc_id = aws_vpc.default.id
      ingress {
          from_port   = 3306
          to_port     = 3306
          protocol    = "tcp"
          security_groups = [aws_security_group.app.id]
      }
      egress {
        from_port   = 0
        to_port     = 0
        protocol    = "-1"
        cidr_blocks = ["0.0.0.0/0"]
      }
      tags = {
        Name = "db-sg"
      }
    }
    """
    file = open("vpc.tf", "w")
    file.write(assignment)
    file.close()
def mysql():
    vpc()
    type="db.t2.micro"
    insclass=str(input("Enter project name: "))
    if insclass=='':
        insclass=type
    fin = open("terraform.tfvars", "rt")
    data = fin.read()
    data = data.replace('db.t2.micr', insclass)
    fin.close()
    fin = open("terraform.tfvars", "wt")
    fin.write(data)
    fin.close()
    text="""resource "aws_db_instance" "defult" {
    allocated_storage = 20
    identifier = "rds-mysql"
    storage_type = "gp2"
    engine = "mysql"
    engine_version = "5.7"
    instance_class = var.insclass
    name = "teraform"
    username = "cloudtechner"
    password = "cloudtechner"
    parameter_group_name = "default.mysql5.7"
    db_subnet_group_name =aws_db_subnet_group.subnet_group.name
    vpc_security_group_ids =[aws_security_group.sqlapp.id]
    skip_final_snapshot = true
    }"""
    fin=open("vpc.tf","a+")
    fin.write(text)
    fin.close()
    os.system('terraform init')
    os.system('terraform validate')
    os.system('terraform plan')
    os.system('terraform apply')
def postgresql():
    vpc()
    type="db.m5.large"
    insclass=str(input("Enter project name: "))
    if insclass=='':
        insclass=type
    fin = open("terraform.tfvars", "rt")
    data = fin.read()
    data = data.replace('db.t2.micr', insclass)
    fin.close()
    fin = open("terraform.tfvars", "wt")
    fin.write(data)
    fin.close()
    file = open("vpc.tf", "rt")
    data = file.read()
    data = data.replace('3306','5432' )
    file.close()
    file = open("vpc.tf", "wt")
    file.write(data)
    file.close()
    text="""resource "aws_db_instance" "defult" {
    allocated_storage = 20
    identifier = "rds-postgresql"
    storage_type = "gp2"
    engine = "postgres"
    engine_version = "11.5"
    instance_class = "db.m5.large"
    name = "teraform"
    username = "cloudtechner"
    password = "cloudtechner"
    db_subnet_group_name =aws_db_subnet_group.subnet_group.name
    vpc_security_group_ids =[aws_security_group.posapp.id]
    skip_final_snapshot = true
    }"""
    fin=open("vpc.tf","a+")
    fin.write(text)
    fin.close()
    os.system('terraform init')
    os.system('terraform validate')
    os.system('terraform plan')
    os.system('terraform apply')
def auroramysql():
    vpc()
    type="db.r5.large"
    insclass=str(input("Enter project name: "))
    if insclass=='':
        insclass=type
    fin = open("terraform.tfvars", "rt")
    data = fin.read()
    data = data.replace('db.t2.micr', insclass)
    fin.close()
    fin = open("terraform.tfvars", "wt")
    fin.write(data)
    fin.close()
    text="""resource "aws_rds_cluster_instance" "cluster_instances" {
    identifier         = "aurora-cluster-sql"
    cluster_identifier = aws_rds_cluster.default.id
    instance_class     = "db.r5.large"
    engine             = aws_rds_cluster.default.engine
    engine_version     = aws_rds_cluster.default.engine_version
    }
    resource "aws_rds_cluster" "default" {
    cluster_identifier      = "aurora-mysql"
    engine                  = "aurora-mysql"
    engine_version          = "5.7.mysql_aurora.1.22.2"
    availability_zones      = ["ap-south-1a", "ap-south-1b"]
    database_name           = "mydb"
    master_username         = "cloudtechner"
    master_password         = "cloudtechner"
    db_subnet_group_name =aws_db_subnet_group.subnet_group.name
    vpc_security_group_ids =[aws_security_group.ausapp.id]
    skip_final_snapshot = true
    }"""
    fin=open("vpc.tf","a+")
    fin.write(text)
    fin.close()
    os.system('terraform init')
    os.system('terraform validate')
    os.system('terraform plan')
    os.system('terraform apply')
def aurorapostgresql():
    vpc()
    type="db.r5.large"
    insclass=str(input("Enter project name: "))
    if insclass=='':
        insclass=type
    fin = open("terraform.tfvars", "rt")
    data = fin.read()
    data = data.replace('db.t2.micr', insclass)
    fin.close()
    fin = open("terraform.tfvars", "wt")
    fin.write(data)
    fin.close()
    file = open("vpc.tf", "rt")
    data = file.read()
    data = data.replace('3306','5432' )
    file.close()
    file = open("vpc.tf", "wt")
    file.write(data)
    file.close()
    text="""resource "aws_rds_cluster_instance" "cluster_instances" {
    identifier         = "aurora-cluster-demo"
    cluster_identifier = aws_rds_cluster.default.id
    instance_class     = "db.r5.large"
    engine             = aws_rds_cluster.default.engine
    engine_version     = aws_rds_cluster.default.engine_version
    }
    resource "aws_rds_cluster" "default" {
    cluster_identifier      = "aurora-postgre"
    engine                  = "aurora-postgresql"
    engine_version          = "11.9"
    availability_zones      = ["ap-south-1a", "ap-south-1b"]
    database_name           = "mydb"
    master_username         = "cloudtechner"
    master_password         = "cloudtechner"
    db_subnet_group_name =aws_db_subnet_group.subnet_group.name
    vpc_security_group_ids =[aws_security_group.auposapp.id]
    skip_final_snapshot = true
    }"""
    fin=open("vpc.tf","a+")
    fin.write(text)
    fin.close()
    os.system('terraform init')
    os.system('terraform validate')
    os.system('terraform plan')
    os.system('terraform apply')    
i=1
while i=='1':
    print(" ")
    print("Choose which type instance you wnat to create")
    print("To create RDS instance, ENTER 1")
    print("To create AURORA instance, ENTER 2")
    print("To exit, ENTER 0")
    s=input("Enter your choice: ")
    if s=='1':
        z=1
        while z==1:
            print(" ")
            print("Choose which type ENGINE you want to use for RDS instance")
            print("To choose MYSQL Engine, ENTER 1")
            print("To choose POSTGRESQL Engine, ENTER 2")
            print("To exit, ENTER 0")
            print(" ")
            engine=input("Enter your choice: ")
            if engine=='1':
                mysql()
            elif engine=='2':
                postgresql()
            elif engine=='0':
                z=0
            else:
                print("Invalid choice, Enter Valid option")
    elif s=='2':
        x=1
        while x==1:
            print(" ")
            print("Choose which type ENGINE you wnat to use for AURORA instance")
            print("To choose MYSQL Engine, ENTER 1")
            print("To choose POSTGRESQL, ENTER 2")
            print("To exit, ENTER 0")
            print(" ")
            engine=input("Enter your choice: ")
            if engine=='1':
                auroramysql()
            elif engine=='2':
                aurorapostgresql()
            elif engine=='0':
                x=0
            else:
                print("Invalid choice, Enter Valid option")
    elif s=='0':
        i=0
    else:
        print("Invalid choice, Enter Valid option")
    
    
