from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from .models import Prediction, Bet
from core.models import CustomUser

class PredictionModelTestCase(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(
            username='test_user', email='test@example.com', password='test_password'
        )
        self.prediction = Prediction.objects.create(
            user=self.user,
            prediction_type='Super Bowl',
            prediction_text='My prediction for the Super Bowl winner.'
        )

    def test_prediction_model_str(self):
        self.assertEqual(
            str(self.prediction),
            f'Prediction: {self.prediction.prediction_text} {self.prediction.prediction_type} - {self.prediction.user}'
        )

class BetModelTestCase(TestCase):
    def setUp(self):
        self.user1 = CustomUser.objects.create_user(
            username='user1', email='user1@example.com', password='user1_password'
        )
        self.user2 = CustomUser.objects.create_user(
            username='user2', email='user2@example.com', password='user2_password'
        )
        self.prediction = Prediction.objects.create(
            user=self.user1,
            prediction_type='Super Bowl',
            prediction_text='My prediction for the Super Bowl winner.'
        )
        self.bet = Bet.objects.create(
            prediction=self.prediction,
            stake=100
        )
        self.bet.users.set([self.user1, self.user2])

    def test_bet_model_str(self):
        self.assertEqual(
            str(self.bet),
            f'Bet: {self.prediction}: {self.bet.stake}'
        )

class PredictionAPITestCase(APITestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(
            username='test_user', email='test@example.com', password='test_password'
        )
        self.client.force_authenticate(user=self.user)

    def test_create_prediction(self):
        url = reverse('prediction-list-create')
        data = {
            'user': self.user.id,
            'prediction_type': 'Super Bowl',
            'prediction_text': 'My prediction for the Super Bowl winner.'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Prediction.objects.count(), 1)
        self.assertEqual(Prediction.objects.get().user, self.user)

    def test_retrieve_prediction(self):
        prediction = Prediction.objects.create(
            user=self.user,
            prediction_type='Super Bowl',
            prediction_text='My prediction for the Super Bowl winner.'
        )
        url = reverse('prediction-retrieve-update-destroy', kwargs={'pk': prediction.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['prediction_text'], 'My prediction for the Super Bowl winner.')

class BetAPITestCase(APITestCase):
    def setUp(self):
        self.user1 = CustomUser.objects.create_user(
            username='user1', email='user1@example.com', password='user1_password'
        )
        self.user2 = CustomUser.objects.create_user(
            username='user2', email='user2@example.com', password='user2_password'
        )
        self.client1 = self.client_class()
        self.client1.force_authenticate(user=self.user1)

    def test_create_bet(self):
        prediction = Prediction.objects.create(
            user=self.user1,
            prediction_type='Super Bowl',
            prediction_text='My prediction for the Super Bowl winner.'
        )
        url = reverse('bet-list-create')
        data = {
            'users': [self.user1.id, self.user2.id],
            'prediction': prediction.id,
            'stake': 100
        }
        response = self.client1.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Bet.objects.count(), 1)
        self.assertEqual(Bet.objects.get().prediction, prediction)

    def test_retrieve_bet(self):
        prediction = Prediction.objects.create(
            user=self.user1,
            prediction_type='Super Bowl',
            prediction_text='My prediction for the Super Bowl winner.'
        )
        bet = Bet.objects.create(
            prediction=prediction,
            stake=100
        )
        bet.users.set([self.user1, self.user2])
        url = reverse('bet-retrieve-update-destroy', kwargs={'pk': bet.pk})
        response = self.client1.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['stake'], '100.00')

# Add more test cases for updating and deleting predictions and bets if needed

