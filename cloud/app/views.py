from django.shortcuts import render
from django.views import View
from .models import project, rds ,iam,bill,final
from .forms import ProjectForm ,IamForm,RdsForm,BillForm
import os
from subprocess import call
from django.http  import HttpResponse,HttpResponseRedirect

def home(request):
 return render(request, 'app/home.html')

#def product_detail(request):
# return render(request, 'app/productdetail.html')

#class add_to_cart(View):
   # def add_to_cart(self, request, pk):
       # project = project.objects.get()
        #return render(request, 'app/addtocart.html',{'project':project})'
def add_to_cart(request):

    proj = project.objects.all().last()
    rdso = rds.objects.all().last()
    iamo = iam.objects.all().last()
    budo = bill.objects.all().last()
    print('My Output',proj)
    return render(request, 'app/addtocart.html',{'proj':proj ,'rdso':rdso,'iamo':iamo,'budo':budo})

def buy_now(request):
 return render(request, 'app/buynow.html')

def profile(request):
 return render(request, 'app/profile.html')

def address(request):
    finalo = final.objects.all()

    return render(request, 'app/address.html',{'finalo':finalo})

#def orders(request):
# return render(request, 'app/orders.html')

def change_password(request):
 return render(request, 'app/changepassword.html')

#def mobile(request):
 #return render(request, 'app/mobile.html')

def login(request):
 return render(request, 'app/login.html')

#def customerregistration(request):
 #return render(request, 'app/customerregistration.html')

def checkout(request):
 return render(request, 'app/checkout.html')

class ProjectView(View):
    def get(self, request):
        form = ProjectForm
        form2 = BillForm
        form3 = IamForm
        form4 = RdsForm
        return render(request,'app/mobile.html',{'form':form,'form2':form2,'form3':form3,'form4':form4})

    def post(self, request):
        submitbutton= request.POST.get("submit")
        form = ProjectForm(request.POST)
        form2 = BillForm(request.POST)
        form3 = IamForm
        form4 = RdsForm

        if form.is_valid() or form2.is_valid():
            usr = request.user
            #new_tnx = form.save(commit = False)
            #nex_tnx.ceated_by = request.user
            #new_tnx.save()
            iamo = iam.objects.all().last()
            Project_Name    = form.cleaned_data['Project_Name']
            Environment_Name  = form.cleaned_data['Environment_Name']
            region    = form.cleaned_data['region']
            vpc_cidr  = form.cleaned_data['vpc_cidr']
            budget   = form2.cleaned_data['budget']
            email    = form2.cleaned_data['email']
            iam_group = form3.cleaned_data['groupname']
            username  = form3.cleaned_data['username']
            rds_username = form4.cleaned_data['rds_username']
            rds_password = form4.cleaned_data['rds_password']
            rds_type     = form4.cleaned_data['rds_type']
            reg = final(Project_Name = Project_Name, Environment_Name = Environment_Name,Region = region,VPC_CIDR = vpc_cidr,
            RDS_Username = rds_username,RDS_Password = rds_password,RDS_Type = rds_type,
            IAM_Username = username,IAM_Groupname = iam_group,Email = email,Budjet = budjet)
            reg.save()
        return render(request,'app/mobile.html',{'form':form,'form2':form2,'form3':form3,'form4':form4})

class IamView(View):
    def get(self,request):
        form = IamForm
        return render(request,'app/orders.html',{'form':form})
    
    def post(self,request):
        form = IamForm(request.POST)
        submitbutton= request.POST.get("submit")
        iamo = iam.objects.all().last()
        if form.is_valid():
            usr = request.user
            username = form.cleaned_data['username']
            groupname = form.cleaned_data['groupname']
            
            reg = iam(user = usr,username = username,groupname = groupname)
            reg.save()
            if request.POST.get('save_add'):
                return HttpResponseRedirect('buy')
        context= {'form': form, 'username':username ,'groupname':groupname,'submitbutton':submitbutton}
        return render(request,'app/orders.html',context)  


class RdsView(View):
    def get(self,request):
        form = RdsForm
        submitbutton= request.POST.get("submit")
        return render(request,'app/productdetail.html',{'form':form})
    
    def post(self,request):
        form = RdsForm(request.POST)
        submitbutton= request.POST.get("submit")
        if form.is_valid():
            usr = request.user
            rds_username = form.cleaned_data['rds_username']
            rds_password = form.cleaned_data['rds_password']
            rds_type     = form.cleaned_data['rds_type']
            
            reg = rds(user = usr,rds_type =rds_type,rds_username = rds_username,rds_password = rds_password)
            reg.save()
            if request.POST.get('save_add'):
                return HttpResponseRedirect('cart')
        context= {'form': form, 'rds_username':rds_username ,'rds_password':rds_password,'rds_type':rds_type,'submitbutton':submitbutton}
        return render(request,'app/productdetail.html',context) 

class BillView(View):
    def get(self,request):
        form = BillForm   
        submitbutton = request.POST.get("submit")
        return render(request,'app/customerregistration.html',{'form':form})
    def post(self,request):
        form = BillForm(request.POST)
        submitbutton = request.POST.get("submit")
        if form.is_valid():
            usr = request.user
            budget = form.cleaned_data['budget']
            email  = form.cleaned_data['email']

            reg = bill(user = usr,email = email,budget=budget)
            reg.save()
            if request.POST.get('save_add'):
                return HttpResponseRedirect('order')
        context= {'form':form,'budget':budget,'email':email,'submitbutton':submitbutton}
        return render(request,'app/customerregistration.html',context)




def function(request):
    path = '\djangoproject\cloud\cloud\run.py'
    call(["python", 'C:/djangoproject/cloud/cloud/run.py'])
    return HttpResponse("""<html><script>window.location.replace('/');</script></html>""")