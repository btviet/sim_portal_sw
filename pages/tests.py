from django.test import TestCase, SimpleTestCase
from django.urls import reverse


class HomepageTests(SimpleTestCase):
    def test_url_exists_at_correct_location(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
    def test_url_available_by_name(self): # new
        response = self.client.get(reverse("home"))
        self.assertEqual(response.status_code, 200)


class SESCpageTests(SimpleTestCase):
    def test_url_exists_at_correct_location(self):
        response = self.client.get("/sesc/")
        self.assertEqual(response.status_code, 200)
    def test_url_available_by_name(self): # new
        response = self.client.get(reverse("sesc"))
        self.assertEqual(response.status_code, 200)

class HESCpageTests(SimpleTestCase):
    def test_url_exists_at_correct_location(self):
        response = self.client.get("/hesc/")
        self.assertEqual(response.status_code, 200)
    def test_url_available_by_name(self): # new
        response = self.client.get(reverse("hesc"))
        self.assertEqual(response.status_code, 200)

class RESCpageTests(SimpleTestCase):
    def test_url_exists_at_correct_location(self):
        response = self.client.get("/resc/")
        self.assertEqual(response.status_code, 200)
    def test_url_available_by_name(self): # new
        response = self.client.get(reverse("resc"))
        self.assertEqual(response.status_code, 200)
class IESCpageTests(SimpleTestCase):
    def test_url_exists_at_correct_location(self):
        response = self.client.get("/iesc/")
        self.assertEqual(response.status_code, 200)
    def test_url_available_by_name(self): # new
        response = self.client.get(reverse("iesc"))
        self.assertEqual(response.status_code, 200)
class GESCpageTests(SimpleTestCase):
    def test_url_exists_at_correct_location(self):
        response = self.client.get("/gesc/")
        self.assertEqual(response.status_code, 200)
    def test_url_available_by_name(self): # new
        response = self.client.get(reverse("gesc"))
        self.assertEqual(response.status_code, 200)