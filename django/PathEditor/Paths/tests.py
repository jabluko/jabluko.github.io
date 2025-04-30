from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile

from .models import Background, Path, Path, UserProfile

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
            name="Test Path",
            user=self.user,
            background=self.background
        )
        self.assertEqual(str(paths), f"'Test Path' na tle 'Test Background' (użytkownik: {self.user.username})")
        self.assertEqual(paths.user, self.user)
        self.assertEqual(paths.background, self.background)

    def test_paths_point_creation(self):
        paths = Path.objects.create(title="Path For Points", user=self.user, background=self.background)
        point = Path.objects.create(
            paths=paths,
            x_coord=10,
            y_coord=20,
            order=1
        )
        self.assertEqual(str(point), f"Punkt 1 (10, 20) dla trasy 'Path For Points'")
        self.assertEqual(point.paths, paths)
        self.assertEqual(point.order, 1)

class CoreWebViewTests(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.user1 = User.objects.create_user(username='webuser1', password='password1')
        cls.user2 = User.objects.create_user(username='webuser2', password='password2')
        dummy_image = SimpleUploadedFile("web_bg.jpg", b"content", content_type="image/jpeg")
        cls.background = Background.objects.create(title="Web Background", image=dummy_image)
        cls.paths1 = Path.objects.create(title="User1 Path", user=cls.user1, background=cls.background)
        cls.point1 = Path.objects.create(paths=cls.paths1, x_coord=5, y_coord=5, order=1)

    def setUp(self):
        # self.client jest dostępny w TestCase, nie trzeba go tworzyć
        pass

    def test_paths_list_login_required(self):
        response = self.client.get(reverse('paths_list'))
        # Sprawdź przekierowanie do strony logowania
        self.assertRedirects(response, f"{reverse('login')}?next={reverse('paths_list')}")

    def test_paths_detail_login_required(self):
        response = self.client.get(reverse('paths_detail', args=[self.paths1.id]))
        self.assertRedirects(response, f"{reverse('login')}?next={reverse('paths_detail', args=[self.paths1.id])}")

    def test_paths_list_authenticated(self):
        self.client.login(username='webuser1', password='password1')
        response = self.client.get(reverse('paths_list'))
        self.assertEqual(response.status_code, 200)
        # Sprawdź, czy strona zawiera nazwę trasy użytkownika
        #self.assertContains(response, self.paths1.name)
        # Sprawdź, czy profil użytkownika ma ustawione tło (powinien móc je wybrać)
        self.user1.profile.selected_background = self.background
        self.user1.profile.save()
        response = self.client.get(reverse('paths_list'))
        self.assertContains(response, self.background.name)


    def test_paths_detail_authenticated_user(self):
        self.client.login(username='webuser1', password='password1')
        response = self.client.get(reverse('paths_detail', args=[self.paths1.id]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.paths1.name)
        # Sprawdź, czy zawiera współrzędną punktu
        self.assertContains(response, str(self.point1.x_coord))

    def test_paths_detail_forbidden_other_user(self):
        # Użytkownik webuser2 próbuje zobaczyć trasę webuser1
        self.client.login(username='webuser2', password='password2')
        response = self.client.get(reverse('paths_detail', args=[self.paths1.id]))
        # Widok używa get_object_or_404, więc powinien zwrócić 404 dla innego użytkownika
        self.assertEqual(response.status_code, 404)

    def test_create_paths_view(self):
        self.client.login(username='webuser1', password='password1')
        # Najpierw ustaw wybrane tło dla profilu
        self.user1.profile.selected_background = self.background
        self.user1.profile.save()

        paths_count_before = Path.objects.filter(user=self.user1).count()
        response = self.client.post(reverse('paths_list'), { # POST na ten sam URL co lista
            'name': 'Nowa trasa z testu',
            'description': 'Opis testowy'
            # background jest brany z profilu, nie z formularza
        })
        paths_count_after = Path.objects.filter(user=self.user1).count()

        self.assertEqual(paths_count_after, paths_count_before + 1)
        new_paths = Path.objects.get(title='Nowa trasa z testu')
        # Sprawdź przekierowanie do szczegółów nowej trasy
        self.assertRedirects(response, reverse('paths_detail', args=[new_paths.id]))

    def test_delete_paths_view(self):
        self.client.login(username='webuser1', password='password1')
        paths_to_delete_id = self.paths1.id
        paths_count_before = Path.objects.filter(user=self.user1).count()

        response = self.client.post(reverse('delete_paths', args=[paths_to_delete_id])) # POST do usunięcia
        paths_count_after = Path.objects.filter(user=self.user1).count()

        self.assertEqual(paths_count_after, paths_count_before - 1)
        self.assertFalse(Path.objects.filter(id=paths_to_delete_id).exists())
        # Sprawdź przekierowanie z powrotem do listy tras
        self.assertRedirects(response, reverse('paths_list'))

    def test_add_point_view(self):
        self.client.login(username='webuser1', password='password1')
        point_count_before = Path.objects.filter(paths=self.paths1).count()

        response = self.client.post(reverse('paths_detail', args=[self.paths1.id]), {
            'x_coord': 100,
            'y_coord': 200
        })
        point_count_after = Path.objects.filter(paths=self.paths1).count()

        self.assertEqual(point_count_after, point_count_before + 1)
        new_point = Path.objects.get(paths=self.paths1, x_coord=100, y_coord=200)
        self.assertTrue(new_point.order > 0) # Sprawdź, czy nadano kolejność
        # Sprawdź przekierowanie do tej samej strony szczegółów
        self.assertRedirects(response, reverse('paths_detail', args=[self.paths1.id]))


# --- Testy API REST ---

class CoreAPITests(APITestCase): # Używamy APITestCase z DRF

    @classmethod
    def setUpTestData(cls):
        cls.user1 = User.objects.create_user(username='apiuser1', password='apipassword1', email='api1@test.com')
        cls.user2 = User.objects.create_user(username='apiuser2', password='apipassword2', email='api2@test.com')
        # Utwórz tokeny dla użytkowników
        cls.token1 = Token.objects.create(user=cls.user1)
        cls.token2 = Token.objects.create(user=cls.user2)

        dummy_image = SimpleUploadedFile("api_bg.jpg", b"api_content", content_type="image/jpeg")
        cls.background = Background.objects.create(title="API Background", image=dummy_image)
        cls.paths1 = Path.objects.create(title="API User1 Path", user=cls.user1, background=cls.background)
        cls.point1 = Path.objects.create(paths=cls.paths1, x_coord=10, y_coord=10, order=1)

    def authenticate(self, user_token):
        """Pomocnicza metoda do ustawiania nagłówka autoryzacji."""
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {user_token.key}')

    def test_api_list_pathss_unauthenticated(self):
        response = self.client.get(reverse('trasa-list')) # Używamy nazw z pathsra DRF (basename='trasa')
        # Oczekujemy błędu 401 lub 403 w zależności od konfiguracji IsAuthenticated
        self.assertIn(response.status_code, [status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN])

    def test_api_list_pathss_authenticated(self):
        self.authenticate(self.token1)
        response = self.client.get(reverse('trasa-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Sprawdź, czy odpowiedź zawiera ID trasy użytkownika 1
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['id'], self.paths1.id)
        self.assertEqual(response.data[0]['user'], self.user1.username)

    def test_api_create_paths(self):
        self.authenticate(self.token1)
        data = {
            'name': 'API Created Path',
            'description': 'Created via API test',
            'background': self.background.id
        }
        response = self.client.post(reverse('trasa-list'), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['name'], 'API Created Path')
        self.assertEqual(response.data['user'], self.user1.username)
        # Sprawdź, czy trasa faktycznie istnieje w bazie
        self.assertTrue(Path.objects.filter(title='API Created Path', user=self.user1).exists())

    def test_api_retrieve_own_paths(self):
        self.authenticate(self.token1)
        response = self.client.get(reverse('trasa-detail', args=[self.paths1.id]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['id'], self.paths1.id)
        # Sprawdź, czy zawiera zagnieżdżone punkty
        self.assertTrue('points' in response.data)
        self.assertEqual(len(response.data['points']), 1)
        self.assertEqual(response.data['points'][0]['id'], self.point1.id)


    def test_api_retrieve_other_user_paths_forbidden(self):
        self.authenticate(self.token2) # Logujemy się jako user2
        response = self.client.get(reverse('trasa-detail', args=[self.paths1.id])) # Próba dostępu do trasy user1
        # Ponieważ get_queryset filtruje, a IsOwner sprawdza, oczekujemy 404 lub 403
        self.assertIn(response.status_code, [status.HTTP_404_NOT_FOUND, status.HTTP_403_FORBIDDEN])

    def test_api_add_point_to_own_paths(self):
        self.authenticate(self.token1)
        url = reverse('trasa-punkty-list', args=[self.paths1.id]) # Używamy nazwy z pathsra zagnieżdżonego
        data = {'x_coord': 55, 'y_coord': 66}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['x_coord'], 55)
        self.assertEqual(response.data['y_coord'], 66)
        # Sprawdź, czy nadano kolejność (powinna być 2, bo punkt 1 już istnieje)
        self.assertEqual(response.data['order'], 2)
        self.assertEqual(response.data['paths'], self.paths1.id)

    def test_api_add_point_to_other_user_paths_forbidden(self):
        self.authenticate(self.token2) # Logujemy się jako user2
        url = reverse('trasa-punkty-list', args=[self.paths1.id]) # Próba dodania do trasy user1
        data = {'x_coord': 1, 'y_coord': 1}
        response = self.client.post(url, data, format='json')
        # Widok powinien zwrócić 404 (bo get_object_or_404 na trasie się nie powiedzie) lub 403
        self.assertIn(response.status_code, [status.HTTP_404_NOT_FOUND, status.HTTP_403_FORBIDDEN])

    def test_api_delete_own_point(self):
        self.authenticate(self.token1)
        # Używamy nazwy z pathsra zagnieżdżonego dla detali punktu
        url = reverse('trasa-punkty-detail', args=[self.paths1.id, self.point1.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Path.objects.filter(id=self.point1.id).exists())

    def test_api_delete_own_paths(self):
        self.authenticate(self.token1)
        url = reverse('trasa-detail', args=[self.paths1.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Path.objects.filter(id=self.paths1.id).exists())

    def test_api_create_paths_invalid_background_id(self):
        self.authenticate(self.token1)
        data = {
            'name': 'Invalid BG Path',
            'background': 99999 # Nieistniejące ID
        }
        response = self.client.post(reverse('trasa-list'), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        # Sprawdź, czy błąd dotyczy pola background
        self.assertIn('background', response.data)