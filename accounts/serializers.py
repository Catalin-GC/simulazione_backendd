from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers

User = get_user_model()


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True,
        required=True,
        style={"input_type": "password"},
        validators=[validate_password],
    )
    conferma_password = serializers.CharField(
        write_only=True,
        required=True,
        style={"input_type": "password"},
    )

    class Meta:
        model = User
        fields = ["id", "nome", "cognome", "email", "ruolo", "password", "conferma_password"]

    def validate_nome(self, value):
        if not value.strip():
            raise serializers.ValidationError("Il nome è obbligatorio.")
        return value.strip()

    def validate_cognome(self, value):
        if not value.strip():
            raise serializers.ValidationError("Il cognome è obbligatorio.")
        return value.strip()

    def validate_email(self, value):
        if User.objects.filter(email__iexact=value).exists():
            raise serializers.ValidationError("Email già registrata.")
        return value

    def validate(self, attrs):
        if attrs["password"] != attrs.pop("conferma_password"):
            raise serializers.ValidationError(
                {"conferma_password": "Le password non coincidono."}
            )
        return attrs

    def create(self, validated_data):
        return User.objects.create_user(
            email=validated_data["email"],
            password=validated_data["password"],
            nome=validated_data["nome"],
            cognome=validated_data["cognome"],
            ruolo=validated_data.get("ruolo", User.Ruolo.DIPENDENTE),
        )


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "nome", "cognome", "email", "ruolo", "date_joined"]
