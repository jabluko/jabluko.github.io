from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile

from .models import Background, Path, Point, UserProfile

from rest_framework.test import APITestCase
from rest_framework import status
from rest_framework.authtoken.models import Token

User = get_user_model()

class CoreModelTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        dummy_image = SimpleUploadedFile("test_bg.jpg", b"file_content", content_type="image/jpeg")
        cls.user = User.objects.create_user(username='testuser', password='testpassword')
        cls.background = Background.objects.create(title="Test Background", image=dummy_image)

    def test_background_creation(self):
        self.assertEqual(str(self.background), "Test Background")
        self.assertTrue(self.background.image.name.startswith('backgrounds/test_bg'))

    def test_user_profile_auto_creation(self):
        self.assertTrue(hasattr(self.user, 'profile'))
        self.assertIsInstance(self.user.profile, UserProfile)
        self.assertEqual(str(self.user.profile), self.user.username)

    def test_paths_creation(self):
        paths = Path.objects.create(
            title="Test Path",
            user=self.user,
            background=self.background
        )
        self.assertEqual(str(paths), "Test Path")
        self.assertEqual(paths.user, self.user)
        self.assertEqual(paths.background, self.background)

class APIEndpointTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.token = Token.objects.create(user=self.user)
        self.background = Background.objects.create(title="Test Background")
        self.path = Path.objects.create(title="Test Path", user=self.user, background=self.background)
        self.point = Point.objects.create(path=self.path, x=10, y=20, order=1)

    def test_get_paths(self):
        url = reverse('path-list')
        response = self.client.get(url, HTTP_AUTHORIZATION=f'Token {self.token.key}')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['title'], "Test Path")

    def test_create_path(self):
        url = reverse('path-list')
        data = {
            'title': 'New Path',
            'background': self.background.id
        }
        response = self.client.post(url, data, HTTP_AUTHORIZATION=f'Token {self.token.key}')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['title'], 'New Path')

    def test_update_path(self):
        url = reverse('path-detail', kwargs={'pk': self.path.id})
        data = {
            'title': 'Updated Path',
            'background': self.background.id
        }
        response = self.client.put(url, data, HTTP_AUTHORIZATION=f'Token {self.token.key}')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'Updated Path')

    def test_delete_path(self):
        url = reverse('path-detail', kwargs={'pk': self.path.id})
        response = self.client.delete(url, HTTP_AUTHORIZATION=f'Token {self.token.key}')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Path.objects.filter(id=self.path.id).exists())

    def test_create_point(self):
        url = reverse('points-list', kwargs={'path_pk': self.path.id})
        data = {
            'x': 30,
            'y': 40,
            'order': 2,
        }
        response = self.client.post(url, data, HTTP_AUTHORIZATION=f'Token {self.token.key}')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['x'], 30)
        self.assertEqual(response.data['y'], 40)
        self.assertEqual(response.data['order'], 2)

    def test_get_path_points(self):
        url = reverse('points-list', kwargs={'path_pk': self.path.id})
        response = self.client.get(url, HTTP_AUTHORIZATION=f'Token {self.token.key}')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['x'], 10)
        self.assertEqual(response.data[0]['y'], 20)
        self.assertEqual(response.data[0]['order'], 1)
        self.assertEqual(response.data[0]['path'], self.path.id)


class APIEndpointSecurityTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.secretuser2=User.objects.create_user(username='secretuser', password='secretpassword')
        self.token = Token.objects.create(user=self.user)
        self.background = Background.objects.create(title="Test Background")
        self.path = Path.objects.create(title="Test Path", user=self.user, background=self.background)
        self.point = Point.objects.create(path=self.path, x=10, y=20, order=1)

    def test_get_paths(self):
        url = reverse('path-list')
        response = self.client.get(url)
        
        self.assertTrue(response.status_code == status.HTTP_400_BAD_REQUEST or
                        response.status_code == status.HTTP_401_UNAUTHORIZED)

    def test_create_path(self):
        url = reverse('path-list')
        data = {
            'title': 'New Path',
            'background': self.background.id
        }
        response = self.client.post(url, data)
        self.assertTrue(response.status_code == status.HTTP_400_BAD_REQUEST or
                        response.status_code == status.HTTP_401_UNAUTHORIZED)

    def test_update_path(self):
        url = reverse('path-detail', kwargs={'pk': self.path.id})
        data = {
            'title': 'Updated Path',
            'background': self.background.id
        }
        response = self.client.put(url, data)
        self.assertTrue(response.status_code == status.HTTP_400_BAD_REQUEST or
                        response.status_code == status.HTTP_401_UNAUTHORIZED)

    def test_delete_path(self):
        url = reverse('path-detail', kwargs={'pk': self.path.id})
        response = self.client.delete(url)
        self.assertTrue(response.status_code == status.HTTP_400_BAD_REQUEST or
                        response.status_code == status.HTTP_401_UNAUTHORIZED)

    def test_create_point(self):
        url = reverse('points-list', kwargs={'path_pk': self.path.id})
        data = {
            'x': 30,
            'y': 40,
            'order': 2,
        }
        response = self.client.post(url, data)
        self.assertTrue(response.status_code == status.HTTP_400_BAD_REQUEST or
                        response.status_code == status.HTTP_401_UNAUTHORIZED)

    def test_get_path_points(self):
        url = reverse('points-list', kwargs={'path_pk': self.path.id})
        response = self.client.get(url)
        self.assertTrue(response.status_code == status.HTTP_400_BAD_REQUEST or
                        response.status_code == status.HTTP_401_UNAUTHORIZED)
