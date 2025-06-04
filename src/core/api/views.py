from rest_framework.mixins import ListModelMixin
from rest_framework.viewsets import GenericViewSet


class MultiSerializerMixin:
    serializer_action_classes = {}

    def get_serializer_class(self):
        return self.serializer_action_classes.get(self.action, super().get_serializer_class())


class AppGenericViewSet(MultiSerializerMixin, GenericViewSet):
    pass


class AppListModelMixin(ListModelMixin):
    pass
