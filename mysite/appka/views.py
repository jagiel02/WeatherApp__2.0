from django.contrib import messages
from django.contrib.auth import login, authenticate
from django.shortcuts import render, get_object_or_404, redirect
import requests
from .models import City
from .forms import CityForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from rest_framework import viewsets
from .serializers import CitySerializer


def weather(request):
    url = 'http://api.openweathermap.org/data/2.5/weather?q={}&units=metric&appid=9abc3912b3b74cbc4b807c9353041aac'

    msg = ''
    if request.method == "POST":
        form = CityForm(request.POST or None)

        if form.is_valid():
            new_city = form.cleaned_data['name']
            existing_city = City.objects.filter(name=new_city).count()  # import cities models and filter it as list
            if existing_city == 0:
                r = requests.get(url.format(new_city)).json()
                if r['cod'] == 200:
                    form.save()
                    msg = f'Corectly added {new_city}'
                    messages.success(request, msg)
                    return redirect("weather")
                else:
                    msg = f"{new_city} doesn't exist"
                    messages.error(request, msg)
                    return redirect("weather")
            else:
                msg = f'City {new_city} is arleady exist'
                messages.error(request, msg)
                return redirect("weather")

    form = CityForm()
    cities = City.objects.all()
    weather_data = []

    for city in cities:
        r = requests.get(url.format(city)).json()
        city_weather = {
            'city': city.name,
            "temperature": r['main']['temp'],
            'description': r['weather'][0]['description'],
            'icon': r['weather'][0]['icon'],
            'city_id': city.city_id
        }

        weather_data.append(city_weather)

    context = {'weather_data': weather_data,
               'form': form,
               'cities': cities,
               'msg': msg}
    return render(request, 'weather.html', context)

@login_required

def delete(request, id):
    city = get_object_or_404(City, pk=id)
    form = CityForm(request.POST or None, request.FILES, instance=city)

    if request.method == 'POST':
        city.delete()
        return redirect(weather)

    return render(request, 'confirm.html', {'form': form})
@login_required
def edit(request, id):
    url = 'http://api.openweathermap.org/data/2.5/weather?q={}&units=metric&appid=9abc3912b3b74cbc4b807c9353041aac'
    city = get_object_or_404(City, pk=id)
    form = CityForm(request.POST or None, request.FILES or None, instance=city)

    if form.is_valid():
        edit_city = form.cleaned_data['name']
        existing_city = City.objects.filter(name=city).count()
        if existing_city == 0:
            r = requests.get(url.format(edit_city)).json()
            if r['cod'] == 200:
                form.save()
                msg = f'Corectly added {city}'
                messages.success(request, msg)
                return redirect(weather)
            else:
                msg = f'City {city} does not exit'
                messages.error(request, msg)
                return redirect(weather)
        else:
            msg = f'City: {city} is arleady exit'
            messages.error(request, msg)
            return redirect(weather)

    return render(request, 'edit.html', {'form': form, 'city': city})

def register(request):
    form = UserCreationForm(request.POST)
    if request.method == "POST":
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('weather')

        else:
            form = UserCreationForm()

    return render(request, 'registration/register.html', {'form': form})
class CityView(viewsets.ModelViewSet):
    queryset = City.objects.all()
    serializer_class = CitySerializer
