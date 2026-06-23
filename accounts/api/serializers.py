from rest_framework import serializers
from accounts.models import User, StudentProfile, TeacherProfile


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id","username","name","email","role","phone","profile_image",]
        read_only_fields = ["id"]


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    password2 = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ["username","name","email","role","phone","password","password2",]

    def validate(self, attrs):
        if attrs["password"] != attrs["password2"]:
            raise serializers.ValidationError(
                {"password": "Passwords do not match."}
            )

        return attrs

    def create(self, validated_data):
        validated_data.pop("password2")

        password = validated_data.pop("password")

        user = User(**validated_data)
        user.set_password(password)
        user.save()

        if user.role == "student":
            StudentProfile.objects.create(user=user)

        elif user.role == "teacher":
            TeacherProfile.objects.create(user=user)

        return user


class StudentProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = StudentProfile
        fields = ["id","user","roll_number",]


class TeacherProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = TeacherProfile
        fields = ["id","user","bio","expertise",]