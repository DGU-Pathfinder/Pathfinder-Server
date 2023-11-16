from rest_framework import serializers
from django.contrib.auth import get_user_model


User = get_user_model()

class SignUpSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    def create(self, validated_data):
        user = User.objects.create_user(
            username    = validated_data['username'],
            is_active   = False,
        )
        user.set_password(validated_data['password'])
        user.save()
        return user

    class Meta:
        model = User
        fields = ['pk', 'username', 'password']