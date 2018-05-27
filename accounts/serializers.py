from rest_framework import serializers

from . import models as accounts_models


class UserEditSerializer(serializers.ModelSerializer):
    password = serializers.CharField(max_length=16, min_length=6, write_only=True, required=True)

    class Meta:
        model = accounts_models.User
        fields = ('id', 'first_name', 'last_name', 'email', 'password', 'phone', 'about_me', 'date_of_birth',
                  'gender', 'profile_picture')

    def create(self, validated_data):
        user = accounts_models.User.objects.create_user(
            email=validated_data.get('email'),
            password=validated_data.get('password'),
            first_name=validated_data.get('first_name'),
            last_name=validated_data.get('last_name', ''),
            phone=validated_data.get('phone', ''),
            about_me=validated_data.get('about_me', ''),
            date_of_birth=validated_data.get('date_of_birth', None),
            gender=validated_data.get('gender', None),
            profile_picture=validated_data.get('profile_picture', None),
        )
        return user

    def update(self, instance, validated_data):
        """Prevents setting profile picture to null if no file is submitted and handles password hashing"""

        profile_picture = validated_data.get('profile_picture', None)
        password = validated_data.get('password', None)

        if 'profile_picture' in validated_data:
            del validated_data['profile_picture']

        if 'password' in validated_data:
            del validated_data['password']

        user = super().update(instance, validated_data)

        if profile_picture:
            user.profile_picture = profile_picture
            user.save()

        if password:
            user.set_password(password)
            user.save()

        return user


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = accounts_models.User
        fields = ('id', 'first_name', 'last_name', 'email', 'phone', 'about_me', 'date_of_birth', 'gender',
                  'profile_picture')
