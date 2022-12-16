from django.core.exceptions import ValidationError
from rest_framework import serializers
from users.models import History
from django.contrib.auth.models import User


class HistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = History
        exclude = ["user"]

    def create(self, validated_data):
        validated_data["user"] = self.context["request"].user
        return super().create(validated_data)


class RegistrationSerializer(serializers.ModelSerializer):
    confirmed_password = serializers.CharField()

    class Meta:
        model = User
        fields = ["username", "password", "confirmed_password"]

    def validate(self, attrs):
        if(attrs["password"] != attrs["confirmed_password"]):
            raise ValidationError("Confirmation mismatched")
        if(User.objects.filter(username=attrs["username"]).count() != 0):
            raise ValidationError("User with this email already exists");
        return super().validate(attrs)

    def create(self, validated_data):
        validated_data.pop("confirmed_password")
        return User.objects.create_user(**validated_data)

