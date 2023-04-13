import json

from django.urls import reverse
from rest_framework.test import APITestCase

from users.models import User
from users.serializers import UserSerializer, UserDetailSerializer
from users.authentication import JWTAuthentication
from users.services import count_user_subscribers, count_user_subscriptions


class UserApiTestCase(APITestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(
            username='user1', password='User1234', phone='+79999999999', email='ab@c.ru', first_name='User1',
            last_name='User')
        self.user2 = User.objects.create_user(
            username='user2', password='User1234', phone='+79999999991', email='ab@d.ru', first_name='User2',
            last_name='User')
        self.staff = User.objects.create_user(username='staff', password='User1234',
                                              phone='+79999999992', email='admin@staff.com')
        self.staff.is_staff = True

    def test_get_users(self):
        """Проверка получения списка пользователей"""
        response = self.client.get(reverse('users-list'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 3)

    def test_create_user(self):
        """Проверка создания пользователя"""
        response = self.client.post(reverse('users-list'), data={
            'username': 'user',
            'password': 'User1234',
            'phone': '+79991119992',
            'email': 'qwe@rty.ru'
        })
        self.assertEqual(response.status_code, 201)
        new_user = User.objects.values('username', 'phone', 'email').get(username='user')
        self.assertEqual(response.data, new_user)

    def test_get_user_detail(self):
        """Проверка получения детальной информации о пользователе"""
        response = self.client.get(reverse('users-detail', args=[self.user1.id]))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, UserDetailSerializer(self.user1).data)

    def test_get_user_detail_not_found(self):
        """Проверка несуществующего пользователя"""
        response = self.client.get(reverse('users-detail', args=[999]))
        self.assertEqual(response.status_code, 404)

    def test_user_update_and_delete(self):
        """Проверка обновления и удаления пользователя"""
        self.client.force_authenticate(user=self.user1)

        path_data = {
            'username': 'user',
        }
        json_path_data = json.dumps(path_data)
        put_data = {
            "username": "User3",
            "phone": "+79991112233",
            "email": "user@e1111xample.com"
        }
        json_put_data = json.dumps(put_data)
        response = self.client.patch(reverse('users-detail', args=[self.user2.pk]), json_path_data,
                                     content_type='application/json')
        self.assertEqual(response.status_code, 403)
        response = self.client.put(reverse('users-detail', args=[self.user2.pk]), json_put_data,
                                   content_type='application/json')
        self.assertEqual(response.status_code, 403)
        response = self.client.delete(reverse('users-detail', args=[self.user2.pk]))
        self.assertEqual(response.status_code, 403)

        self.client.force_authenticate(user=self.staff)
        response = self.client.patch(reverse('users-detail', args=[self.user2.pk]), json_path_data,
                                     content_type='application/json')
        self.assertEqual(response.status_code, 200)
        response = self.client.put(reverse('users-detail', args=[self.user2.pk]), json_put_data,
                                   content_type='application/json')
        self.assertEqual(response.status_code, 200)
        response = self.client.delete(reverse('users-detail', args=[self.user2.pk]))
        self.assertEqual(response.status_code, 204)

    def test_user_login(self):
        """Проверка авторизации пользователя"""
        response = self.client.post(reverse('users-login'), data={
            'username': 'user1',
            'password': 'User1234'
        })
        self.assertEqual(response.status_code, 200)
        token = response.data['token']
        self.assertTrue(JWTAuthentication().authenticate_credentials(token))

    def test_user_me(self):
        """Проверка получения пользователем своей детальной информации"""
        self.client.force_authenticate(user=self.user1)
        response = self.client.get(reverse('users-me'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, UserDetailSerializer(self.user1).data)

    def test_update_user_me(self):
        """Проверка обновления пользователем своей детальной информации"""
        self.client.force_authenticate(user=self.user1)
        data = {
            "username": "User3",
            "phone": "+79991112233",
            "email": "user@e1111xample.com"
        }
        json_data = json.dumps(data)
        response = self.client.put(reverse('users-me'), json_data, content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.user1.refresh_from_db()
        self.assertEqual('User3', User.objects.get(pk=self.user1.pk).username)
        self.assertEqual('+79991112233', User.objects.get(pk=self.user1.pk).phone)
        self.assertEqual('user@e1111xample.com', User.objects.get(pk=self.user1.pk).email)

    def test_partial_update_user_me(self):
        """Проверка частичного обновления пользователем своей детальной информации"""
        self.client.force_authenticate(user=self.user1)
        data = {
            'username': 'user',
        }
        json_data = json.dumps(data)
        response = self.client.patch(reverse('users-me'), json_data, content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.user1.refresh_from_db()
        self.assertEqual('user', User.objects.get(pk=self.user1.pk).username)

    def test_delete_user_me(self):
        """Проверка удаления пользователем своего аккаунта"""
        self.client.force_authenticate(user=self.user1)
        response = self.client.delete(reverse('users-me'))
        self.assertEqual(response.status_code, 204)
        self.assertEqual(User.objects.count(), 2)

    def test_user_search(self):
        """Проверка поиска пользователей"""
        response = self.client.get(reverse('users-list'), data={'search': 'User'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, UserSerializer([self.user1, self.user2], many=True).data)

    def test_user_ordering(self):
        """Проверка сортировки пользователей"""
        response = self.client.get(reverse('users-list'), data={'ordering': 'username'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, UserSerializer([self.staff, self.user1, self.user2], many=True).data)

    def test_subscribe(self):
        """Проверка подписки"""
        self.client.force_authenticate(user=self.user1)

        # Проверка подписки
        response = self.client.post(reverse('users-subscribers', args=[self.user2.pk]))
        self.assertEqual(response.status_code, 201)
        self.assertEqual(count_user_subscribers(self.user2), 1)

        # Проверка отписки
        response = self.client.post(reverse('users-subscribers', args=[self.user2.pk]))
        self.assertEqual(response.status_code, 204)
        self.assertEqual(count_user_subscribers(self.user2), 0)

        # Проверка подписки на себя
        response = self.client.post(reverse('users-subscribers', args=[self.user1.pk]))
        self.assertEqual(response.status_code, 400)
        self.assertEqual(count_user_subscribers(self.user1), 0)

        # Проверка подписки на несуществующего пользователя
        response = self.client.post(reverse('users-subscribers', args=[100]))
        self.assertEqual(response.status_code, 404)
        self.assertEqual(count_user_subscriptions(self.user1), 0)
