from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from .models import City, SearchHistory

class WeatherAppTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.city = City.objects.create(
            name='Test City',
            country='Test Country',
            latitude=0.0,
            longitude=0.0
        )

    def test_index_view(self):
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'index.html')

    def test_autocomplete_view(self):
        response = self.client.get(reverse('autocomplete') + '?query=test')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'application/json')

    def test_weather_view_post(self):
        response = self.client.post(reverse('weather'), {
            'city': 'Test City, Test Country',
            'latitude': '0.0',
            'longitude': '0.0'
        })
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'weather.html')
        self.assertTrue(SearchHistory.objects.filter(
            session_key=self.client.session.session_key,
            city=self.city
        ).exists())

    def test_search_history_view_unauthenticated(self):
        self.client.post(reverse('weather'), {
            'city': 'Test City, Test Country',
            'latitude': '0.0',
            'longitude': '0.0'
        })
        response = self.client.get(reverse('search_history'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'search_history.html')

    def test_user_search_stats_view(self):
        self.client.post(reverse('weather'), {
            'city': 'Test City, Test Country',
            'latitude': '0.0',
            'longitude': '0.0'
        })
        response = self.client.get(reverse('user_search_stats'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'application/json')
        self.assertJSONEqual(response.content, [{'city__name': 'Test City, Test Country', 'count': 1}])


    def test_search_history_city_click(self):
      self.client.login(username='testuser', password='testpass123')
      self.client.post(reverse('weather'), {
          'city': 'Test City, Test Country',
          'latitude': '0.0',
          'longitude': '0.0'
      })
      response = self.client.post(reverse('weather'), {
          'city': 'Test City, Test Country',
          'latitude': '0.0',
          'longitude': '0.0'
      })
      self.assertEqual(response.status_code, 200)
      self.assertTemplateUsed(response, 'weather.html')
      self.assertTrue(SearchHistory.objects.filter(
          user=self.user,
          city__name='Test City'
      ).exists())

    



    def test_weather_view_hourly_forecast(self):
        response = self.client.post(reverse('weather'), {
            'city': 'Test City, Test Country',
            'latitude': '0.0',
            'longitude': '0.0'
        })
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'weather.html')
        self.assertContains(response, 'Hourly Forecast (Next 24 Hours)')
        self.assertContains(response, 'Humidity</span> 89 %')  