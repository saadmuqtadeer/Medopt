from django.shortcuts import render, HttpResponse, redirect
from datetime import datetime
from home.models import Contact
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.contrib.auth import login, logout
import csv
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer
# Create your views here.

def index(request):
    return render(request, 'index.html')

def about(request):
    return render(request, 'about.html')

def services(request):
    return render(request, 'services.html')

def profile(request):
    return render(request, 'profile.html')

def logout_view(request):
    logout(request)
    return redirect('home')

def contact(request):
    if request.method == "POST":
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone') 
        desc = request.POST.get('desc')
        contact = Contact (name=name, email=email, phone=phone, desc=desc, date = datetime.today())
        contact.save()
        messages.success(request, 'Profile has been Updated!!')
    return render(request, 'contact.html')

def signup(request):
    if request.method== 'POST':
        uname=request.POST.get('username')
        email=request.POST.get('email')
        pass1=request.POST.get('password1')
        pass2=request.POST.get('password2')
        if pass1!=pass2: 
            return HttpResponse("Your password and confrom password are same!!")
        else:
            my_user=User.objects.create_user(uname, email, pass1)
            my_user.save()
            return redirect('login')
    return render(request, 'signup.html')

def log(request):
    if request.method== 'POST':
        username=request.POST.get('username')
        pass1=request.POST.get('pass')
        user=authenticate(request, username=username, password=pass1)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            error_message = "Invalid username or password"
            return render(request, 'login.html', {'error_message': error_message})
            # return HttpResponse ("Username or Password is incorrect!!!")
    return render(request, 'login.html')

def search_view(request):
    if request.method == 'GET':
        search_query = request.GET.get('search_input')
        search_results = []

        if search_query:
            csv_path = 'datasets/1mgadded.csv'  # Path to your CSV file
            items = []
            names = []
            with open(csv_path, 'r', encoding='utf-8') as csvfile:
                reader = csv.DictReader(csvfile)
                for row in reader:
                    items.append(row)
                    names.append(row['cleaned_combined_text'])
                    # if search_query.lower() in row['Drug_Name'].lower():
                    #     search_results.append(row)
            vectorizer = TfidfVectorizer()
            vectors = vectorizer.fit_transform(names + [search_query])
            query_vector = vectors[-1]  # Vector representation of the search query
            item_vectors = vectors[:-1]  # Vector representations of the items
            similarities = cosine_similarity(query_vector, item_vectors).flatten()

            # Sort items based on similarity
            sorted_indices = similarities.argsort()[::-1][:13]
            for index in sorted_indices:
                search_results.append(items[index])

        return render(request, 'search.html', {'search_results': search_results, 'search_query': search_query})
    return render(request, 'search.html')

def details(request):
    item_id = request.GET.get('item_id')
    name = request.GET.get('name')
    desc = request.GET.get('desc')
    manufacturer = request.GET.get('manufacturer')
    active_ingredient = request.GET.get('activeIngredient')
    alcoholWarning = request.GET.get('alcoholWarning')
    breastfeedingWarning = request.GET.get('breastfeedingWarning')
    pregnancyWarning = request.GET.get('pregnancyWarning')

    context = {
        'item_id': item_id,
        'name': name,
        'desc': desc,
        'manufacturer': manufacturer,
        'active_ingredient': active_ingredient,
        'alcoholWarning':alcoholWarning,
        'breastfeedingWarning':breastfeedingWarning,
        'pregnancyWarning':pregnancyWarning
    }

    return render(request, 'details.html', context)


