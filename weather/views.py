from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_GET
from django.http import JsonResponse
from .models import City, SearchHistory
from .forms import UserRegisterForm
from django.contrib.auth import login
from django.contrib.postgres.search import SearchVector
from .utils import get_weather_data, get_cities_autocomplete
from django.db import models
from django.db.models import Count
from django.db.models.functions import TruncDate
from datetime import datetime, timedelta
from django.utils import timezone
from collections import defaultdict




def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Вы успешно зарегистрировались!')
            return redirect('index')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f'{field}: {error}')
    else:
        form = UserRegisterForm()
    
    return render(request, 'register.html', {'form': form})







@require_GET
def autocomplete(request):
    query = request.GET.get('query', '')
    if not query or len(query) < 2:
        return JsonResponse([], safe=False)
    
    local_results = City.objects.annotate(
        search=SearchVector('name', 'country')
    ).filter(search=query)[:5]
    
    if local_results.exists():
        cities = [{
            'name': f"{city.name}, {city.country}",
            'latitude': str(city.latitude),
            'longitude': str(city.longitude)
        } for city in local_results]
        return JsonResponse(cities, safe=False)
    
    cities = get_cities_autocomplete(query)
    return JsonResponse(cities, safe=False)




from django.shortcuts import render
from .models import SearchHistory

def index(request):
    if not request.session.session_key:
        request.session.create()
    
    recent_searches = []
    if request.user.is_authenticated:
        recent_searches = SearchHistory.objects.filter(user=request.user).order_by('-search_date')[:5]
    else:
        recent_searches = SearchHistory.objects.filter(
            session_key=request.session.session_key
        ).order_by('-search_date')[:5]
    
    return render(request, 'index.html', {'recent_searches': recent_searches})






def weather(request):
    if request.method == 'POST':
        city_name = request.POST.get('city')
        latitude = request.POST.get('latitude')
        longitude = request.POST.get('longitude')
        
        if not all([city_name, latitude, longitude]):
            messages.error(request, "Please select a city from the suggestions")
            return redirect('index')
        
        try:
            city, created = City.objects.get_or_create(
                name=city_name.split(',')[0].strip(),
                defaults={
                    'country': city_name.split(',')[-1].strip(),
                    'latitude': latitude,
                    'longitude': longitude
                }
            )
            
            if not request.session.session_key:
                request.session.create()
            
            SearchHistory.objects.create(
                user=request.user if request.user.is_authenticated else None,
                session_key=request.session.session_key,
                city=city
            )
            
            weather_data = get_weather_data(latitude, longitude)
            if not weather_data:
                messages.error(request, "Could not fetch weather data. Please try again.")
                return redirect('index')
            
            print("Weather data:", weather_data)
            print("Hourly time:", weather_data.get('hourly', {}).get('time', []))
            
            utc_offset_seconds = weather_data.get('utc_offset_seconds', 0)
            offset = timedelta(seconds=utc_offset_seconds)
            
            current_time = timezone.now() + offset 
            current_date = current_time.date()
            
            end_of_day = current_time.replace(hour=23, minute=59, second=59, microsecond=999999)
            
            next_day_midnight = datetime.combine(current_date + timedelta(days=1), datetime.min.time()) + offset
            next_day_midnight = timezone.make_aware(next_day_midnight, timezone.get_current_timezone())
            
            hourly_times = weather_data.get('hourly', {}).get('time', [])[:48]
            temperatures = weather_data.get('hourly', {}).get('temperature_2m', [])[:48]
            humidities = weather_data.get('hourly', {}).get('relativehumidity_2m', [])[:48]
            winds = weather_data.get('hourly', {}).get('windspeed_10m', [])[:48]
            
            filtered_times = []
            filtered_temperatures = []
            filtered_humidities = []
            filtered_winds = []
            
            for i, time_str in enumerate(hourly_times):
                try:
                    time_obj = datetime.fromisoformat(time_str)
                    time_obj = timezone.make_aware(time_obj + offset, timezone.get_current_timezone())
                    if time_obj >= current_time and time_obj <= end_of_day:
                        filtered_times.append(time_obj)
                        filtered_temperatures.append(temperatures[i])
                        filtered_humidities.append(humidities[i])
                        filtered_winds.append(winds[i])
                except (ValueError, IndexError):
                    continue
            
            if len(filtered_times) < 24:
                for i, time_str in enumerate(hourly_times):
                    try:
                        time_obj = datetime.fromisoformat(time_str)
                        time_obj = timezone.make_aware(time_obj + offset, timezone.get_current_timezone())
                        if time_obj > end_of_day and time_obj <= next_day_midnight:
                            filtered_times.append(time_obj)
                            filtered_temperatures.append(temperatures[i])
                            filtered_humidities.append(humidities[i])
                            filtered_winds.append(winds[i])
                            if len(filtered_times) >= 24:
                                break
                    except (ValueError, IndexError):
                        continue
            
            filtered_times = filtered_times[:24]
            filtered_temperatures = filtered_temperatures[:24]
            filtered_humidities = filtered_humidities[:24]
            filtered_winds = filtered_winds[:24]
            
            if filtered_times:
                start_date = filtered_times[0].date()
                end_date = filtered_times[-1].date()
                if start_date == end_date:
                    forecast_date = start_date.strftime("%B %d, %Y")  
                else:
                    forecast_date = f"{start_date.strftime('%B %d')} - {end_date.strftime('%B %d, %Y')}"
            else:
                forecast_date = current_date.strftime("%B %d, %Y") 
            
            daily_times = weather_data.get('daily', {}).get('time', [])
            daily_times = [
                timezone.make_aware(datetime.fromisoformat(time) + offset, timezone.get_current_timezone())
                if time else None 
                for time in daily_times
            ]
            
            context = {
                'city': city,
                'weather': weather_data,
                'current': weather_data.get('current_weather', {}),
                'hourly': zip(
                    filtered_times,
                    filtered_temperatures,
                    filtered_humidities,
                    filtered_winds,
                ),
                'daily': zip(
                    daily_times,
                    weather_data.get('daily', {}).get('temperature_2m_max', []),
                    weather_data.get('daily', {}).get('temperature_2m_min', []),
                    weather_data.get('daily', {}).get('precipitation_sum', []),
                ),
                'forecast_date': forecast_date 
            }
            
            return render(request, 'weather.html', context)
            
        except Exception as e:
            messages.error(request, f"An error occurred: {str(e)}")
            return redirect('index')
    
    return redirect('index')





@require_GET
def search_stats(request):
    stats = SearchHistory.objects.values('city__name').annotate(
        count=models.Count('id')
    ).order_by('-count')[:10]
    return JsonResponse(list(stats), safe=False)




@require_GET
def user_search_stats(request):
    if not request.session.session_key:
        request.session.create()
    
    stats = SearchHistory.objects.filter(
        session_key=request.session.session_key
    ).values('city__name').annotate(
        count=models.Count('id')
    ).order_by('-count')
    
    return JsonResponse(list(stats), safe=False)




def search_history(request):
    if request.user.is_authenticated:
        history = SearchHistory.objects.filter(user=request.user)
    elif request.session.session_key:
        history = SearchHistory.objects.filter(session_key=request.session.session_key)
    else:
        history = SearchHistory.objects.none()

    total_searches = history.count()
    top_queries = history.values('city__name').annotate(count=Count('city')).order_by('-count')[:5]
    searches_by_day = (
        history.annotate(day=TruncDate('search_date'))
        .values('day')
        .annotate(count=Count('id'))
        .order_by('day')
    )[:7]
    labels = [entry['day'].strftime('%Y-%m-%d') for entry in searches_by_day]
    data = [entry['count'] for entry in searches_by_day]

    history = history.order_by('search_date')
    city_count = defaultdict(int)
    history_with_counts = []
    for entry in history:
        city_count[entry.city_id] += 1
        entry.query_number = city_count[entry.city_id]
        history_with_counts.append(entry)

    history_with_counts.reverse()

    context = {
        'history': history_with_counts,
        'search_stats': {
            'total_searches': total_searches,
            'top_queries': top_queries,
            'chart_labels': labels,
            'chart_data': data,
        }
    }
    return render(request, 'search_history.html', context)
