from rest_framework import mixins, viewsets, permissions
from .models import Prediction, Bet
from .serializers import PredictionSerializer, BetSerializer


class PredictionViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.DestroyModelMixin,
    mixins.UpdateModelMixin,
    viewsets.GenericViewSet,
):
    queryset = Prediction.objects.all()
    permission_classes = (permissions.IsAuthenticated)
    serializer_class = PredictionSerializer


class BetViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.DestroyModelMixin,
    mixins.UpdateModelMixin,
    viewsets.GenericViewSet,
):
    queryset = Bet.objects.all()
    permission_classes = (permissions.IsAuthenticated)
    serializer_class = BetSerializer
