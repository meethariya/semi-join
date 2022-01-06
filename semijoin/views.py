from django.shortcuts import render
from . import store

# Create your views here.
def home(request):
    if request.method == 'POST':
        table = request.POST.get('table')
        if table == 'seller':
            db = "ads4_2"
        else:
            db = "ads4_3"
            # dictionary = store.typejoin()
        dictionary = store.joins(table,db)
        print(dictionary)
        return render(request, 'semijoin/process.html', dictionary)
    info = store.get_info()
    return render(request,'semijoin/home.html',{'info':info})