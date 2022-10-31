from pyexpat.errors import messages
from django.contrib.auth.models import User 
from django.db import connection
from django.shortcuts import render, redirect
from .models import Customers, Employees, Inventory, SaleOrders
# Create your views here.
import psycopg2
from django.views.generic import (
    ListView,
    CreateView)

from django.db import connection
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .forms import QueryForm
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.admin.views.decorators import staff_member_required



class StaffRequiredMixin(LoginRequiredMixin, UserPassesTestMixin):

    def test_func(self):
        return self.request.user.is_staff


def home(request):
    context = {
        'inventory': Inventory.objects.all(),
        
    }
    return render(request,'frontstore/home.html',context)









@staff_member_required
def staff(request):
    return render(request,'frontstore/staff.html',{'title':'title'})

@staff_member_required
def orders(request):
    context = {
        'saleorders':SaleOrders.objects.all(),
    }
    return render(request,'frontstore/orders.html',context)

class OrderListView(StaffRequiredMixin,ListView):
    #we need to reference our model that will be used to create the view in this case it will be post
    model = SaleOrders
    # app/model_viewtype.html in our case it would be blog/post_list.html
    template_name = 'frontstore/orders.html'
    #we also need to name our variable that our html will loop through
    context_object_name = 'saleorders'
    paginate_by = 10
    
    
@staff_member_required  
def querycustomer(request):
    if request.method == 'POST':
        form = QueryForm(request.POST)
        if form.is_valid():
            request.session['customer_id'] = form.cleaned_data.get('customer_id')
            request.session.modified = True
            return redirect('customerorders')
    else:
        form= QueryForm()
    #the variable form below will be used in html page
    return render(request,'frontstore/customerorderquery.html',{'form':form})

@staff_member_required
def orders_date(request):
 
    customer_id = request.session['customer_id']
    #connect to the db
    con = psycopg2.connect(
        host = "pg",
        database= "dwstore",
        user = "postgres"
    )
    cur = con.cursor()

    cur.execute("SELECT c.customer_id, c.first_name, c.last_name, fs.order_number_id from frontstore_customers c JOIN frontstore_saleinvoices fs ON c.customer_id = fs.customer_id WHERE c.customer_id = %s",(customer_id,))

    rows = cur.fetchall()

    cur.close()
    #close the connection
    con.close()
    mylist = []
    for items in rows:
        mydict = {}
        mydict['customer_id']=items[0]
        mydict['first_name']=items[1]
        mydict['last_name']=items[2]
        mydict['order_number']=items[3]
        mylist.append(mydict)
        
    page = request.GET.get('page', 1)
    paginator = Paginator(mylist,10)
    try:
        mylist = paginator.page(page)
    except PageNotAnInteger:
        mylist = paginator.page(1)
    except EmptyPage:
        mylist = paginator.page(paginator.num_pages)
        
    
    context = {'customerorders':mylist}
    return render(request,'frontstore/customerorders.html',context)
    
    
class CustomerCreateView(StaffRequiredMixin,LoginRequiredMixin,SuccessMessageMixin,CreateView):
    #we need to reference our model that will be used to create the view in this case it will be Customers
    model = Customers
    fields = ['first_name','last_name','email','phone','city']
    template_name = 'frontstore/create_customer.html'


    success_message = 'Customer Added'
    
    def form_valid(self,form):
        form.instance.author=self.request.user
        response = super().form_valid(form)
        return response


#Adding products aka inventory

class InventoryListView(StaffRequiredMixin,ListView):
    #we need to reference our model that will be used to create the view in this case it will be post
    model = Inventory
    # app/model_viewtype.html in our case it would be blog/post_list.html
    template_name = 'frontstore/inventory.html'
    #we also need to name our variable that our html will loop through
    context_object_name = 'inventory'
    paginate_by = 10

#Adding Employee List view

class EmployeeListView(ListView):
    #we need to reference our model that will be used to create the view in this case it will be post
    model = Employees
    # app/model_viewtype.html in our case it would be blog/post_list.html
    template_name = 'frontstore/placeorder.html'
    #we also need to name our variable that our html will loop through
    context_object_name = 'employees'
    paginate_by = 10

@staff_member_required
def about(request):
    return render(request,'frontstore/staffhome.html',{'title':'title'})





@staff_member_required
def stock_level(request):
 

    #connect to the db
    con = psycopg2.connect(
        host = "pg",
        database= "dwstore",
        user = "postgres"
    )
    cur = con.cursor()

    cur.execute("SELECT i.item_id, i.product_name, i.stock_level, i.price, s.supplier_id,s.supplier_address,s.company_name,p.po_id FROM frontstore_inventory i JOIN frontstore_purchaseorders p ON i.item_id = p.item_id JOIN frontstore_purchaseinvoices pi ON p.po_id = pi.po_id JOIN frontstore_suppliers s ON pi.supplier_id = s.supplier_id Order BY i.stock_level ")

    rows = cur.fetchall()

    cur.close()
    #close the connection
    con.close()
    mylist = []
    for items in rows:
        mydict = {}
        mydict['item_id']=items[0]
        mydict['product_name']=items[1]
        mydict['stock_level']=items[2]
        mydict['price']=items[3]
        mydict['supplier_id']=items[4]
        mydict['supplier_address']=items[5]
        mydict['company_name']=items[6]
        mylist.append(mydict)
        
    page = request.GET.get('page', 1)
    paginator = Paginator(mylist,10)
    try:
        mylist = paginator.page(page)
    except PageNotAnInteger:
        mylist = paginator.page(1)
    except EmptyPage:
        mylist = paginator.page(paginator.num_pages)
        
    
    context = {'inventorylist':mylist}
    return render(request,'frontstore/stocklevel.html',context)