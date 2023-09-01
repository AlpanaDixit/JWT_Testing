from django.urls import reverse, resolve
from django.test import SimpleTestCase 
from api.views import CustomerView
from rest_framework.test import APITestCase, APIClient
from rest_framework.authtoken.models import Token
from rest_framework import status
from django.contrib.auth.models import User

class ApiUrlsTests(SimpleTestCase):
    
    def test_get_customers_is_resolved(self):
        url = reverse('customer')
        # print(url)
        self.assertEqual(resolve(url).func.view_class, CustomerView)
        
class CustomerAPIViewTests(APITestCase):
    
    customers_urls = reverse('customer')
    
    def setUp(self):
        self.user = User.objects.create_user(username='admin', password='some-strong-password')
        self.token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token' + self.token.key)
        
    def tearDown(self):
        pass
    
    def test_get_customers_authenticated(self):
        response = self.client.get(self.customers_urls)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
    def test_get_customers_un_authenticated(self):
        self.client.force_authenticate(user=None, token=None)
        response = self.client.get(self.customers_urls)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        
    def test_post_customer_authenticated(self):
        data = {
            'title':'mr',
            'name':'Peter',
            'last_name':'Parker',
            'gender':'M',
            'status':'published'
        }
        response = self.client.post(self.customers_urls, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['name'],'peter')
        
class CustomerDetailAPIViewTests(APITestCase):
    customers_url = reverse('customer')
    customer_url = reverse('customer-detail', args=[1])
    
    def setUP(self):
        self.user = User.objects.create_user(
            username='admin', password='some-strong-password'
        )
        self.token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token' + self.token.key)
        
        #Saving User
        data = {
            'title':'mr',
            'name':'Bruce',
            'last_name':'Barner',
            'gender':'M',
            'status':'published'
        }
        response = self.client.post(self.customers_urls, data, format='json')
        
        
    def test_get_customer_authenticated(self):
        response = self.client.get(self.customer_url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['name'],'Bruce')
        
    def test_get_customer_un_authenticated(self):
        self.client.force_authenticate(user=None, token=None)
        response = self.client.get(self.customer_url)
        self.assertEqual(response.status_code, 401)

    def test_delete_customer_authenticated(self):
        response = self.client.delete(self.customer_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)