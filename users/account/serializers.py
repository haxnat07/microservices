from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        attrs = super().validate(attrs)
        return {
            "username": self.user.username,
            "email": self.user.email,
            "permissions": self.user.user_permissions.values_list("codename", flat=True),
            "groups": self.user.groups.values_list("name", flat=True),
            **attrs,
        }


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer