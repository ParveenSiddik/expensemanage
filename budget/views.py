from django.shortcuts import render,redirect

from django.views.generic import View

from django.contrib import messages

from budget.forms import ExpenseForm,RegistrationForm,SignInForm

from budget.models import Expense

from django.contrib.auth.models import User

from django.contrib.auth import login,logout,authenticate

class ExpenseCreateView(View):

    def get(self,request,*args,**kwargs):

        form_instance=ExpenseForm()

        return render(request,"expense_create.html",{"form":form_instance})

    def post(self,request,*args,**kwargs):

        form_instance=ExpenseForm(request.POST)

        if form_instance.is_valid():

            form_instance.instance.user=request.user

            form_instance.save()

            messages.success(request,"Expense Added Successfully")

            return redirect("expense_list")
        else:

            messages.errror(request,"Addition Failed") 

            return render(request,"expense_create.html",{"form":form_instance})   

class ExpenseListView(View):

    def get(self,request,*args,**kwargs):

        qs=Expense.objects.all()      

        return render(request,"expense_list.html",{"expenses":qs})   

class ExpenseDetailView(View):

    def get(self,request,*args,**kwargs):

        id=kwargs.get("pk")

        qs=Expense.objects.get(id=id)

        return render(request,"expense_detail.html",{"task":qs})   

class ExpenseUpdateView(View):

    def get(self,request,*args,**kwargs):

         # extract pk from kwargs
        id=kwargs.get("pk")   

         # fetch task object
        
        expense_obj=Expense.objects.get(id=id)

        form_instance=ExpenseForm(instance=expense_obj)  

        return render(request,"expense_edit.html",{"form":form_instance})     

    def post(self,request,*args,**kwargs):

        # Extract id from Keyword args
        id=kwargs.get("pk")

        # Initialise from with request.POST
        form_instance=ExpenseForm(request.POST)

        # check form is valid
        if form_instance.is_valid():

            # fetch validated data
            data=form_instance.cleaned_data


            # Expense Update
            Expense.objects.filter(id=id).update(**data)
            
            # redirect to Task List
            return redirect("expense_list")

        else:    

            return render(request,"expense_edit.html",{"form":form_instance})        

class ExpenseDeleteView(View):

    def get(self,request,*args,**kwargs):    

        id=kwargs.get("pk")        

        Expense.objects.filter(id=id).delete()

        return redirect("expense_list")

class SignUpView(View):

    template_name="register.html"

    def get(self,request,*args,**kwargs):

        form_instance=RegistrationForm()

        return render(request,self.template_name,{"form":form_instance})

    def post(self,request,*args,**kwargs):

        form_instance=RegistrationForm(request.POST)

        if form_instance.is_valid():

            data=form_instance.cleaned_data

            User.objects.create_user(**data)

            return redirect("signin")
        else:

            return render(request,self.template_name,{"form":form_instance})


class SignInView(View):

    template_name="login.html"

    def get(self,request,*args,**kwargs):

        form_instance=SignInForm()

        return render(request,self.template_name,{"form":form_instance})

    def post(self,request,*args,**kwargs):

        form_instance=SignInForm(request.POST)

        if form_instance.is_valid():

            uname=form_instance.cleaned_data.get("username") 

            pwd=form_instance.cleaned_data.get("password")

            user_object=authenticate(request,username=uname,password=pwd)

            if user_object:

               login(request,user_object)

               return redirect("expense_list")

        return render(request,self.template_name,{"form":form_instance})

class SignOutView(View):

    def get(self,request,*args,**kwargs):

        logout(request)

        return redirect('signin')        








