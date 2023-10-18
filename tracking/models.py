from django.db import models
import requests

class UserVisit(models.Model):
    user_identifier = models.CharField(max_length=255)  # اضافه کردن فیلد user_identifier
    ip_address = models.GenericIPAddressField()
    http_method = models.CharField(max_length=10)
    request_url = models.URLField()
    user_agent = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    referred_from = models.URLField(blank=True, null=True)
    country = models.CharField(max_length=100, blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    latitude = models.FloatField(blank=True, null=True)
    longitude = models.FloatField(blank=True, null=True)

    def __str__(self):
        return f"{self.request_url} - {self.created_at}"

    def save(self, *args, **kwargs):
        if not UserVisit.objects.filter(ip_address=self.ip_address, user_agent=self.user_agent).exists():
            super().save(*args, **kwargs)

    def get_user_location(self):
        url = f"https://api.ipgeolocation.io/ipgeo?apiKey=YOUR_API_KEY&ip={self.ip_address}"  # کلید API خود را وارد کنید

        try:
            response = requests.get(url)
            data = response.json()
            print(data)
            if 'country_name' in data and 'city' in data:
                self.country = data['country_name']
                self.city = data['city']
                self.latitude = data['latitude']
                self.longitude = data['longitude']
                self.save()
                location = {
                    'country': self.country,
                    'city': self.city,
                    'latitude': self.latitude,
                    'longitude': self.longitude
                }
            else:
                location = None
        except requests.exceptions.RequestException:
            location = None

        return location