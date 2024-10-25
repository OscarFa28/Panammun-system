from rest_framework import serializers
from .models import Panammun_edition, Committee, Country, CustomUser
from django.contrib.auth.hashers import make_password

class PanammunEditionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Panammun_edition
        fields = ['id', 'name', 'start_registration_date', 'start_choose_date', 'start_mun_date', 'notes']


class CommitteeSerializer(serializers.ModelSerializer):
    # Incluye la edición de Panammun relacionada 
    panammun_edition = PanammunEditionSerializer(read_only=True)
    
    class Meta:
        model = Committee
        fields = ['id', 'name', 'language', 'panammun_edition', 'notes']


class CountrySerializer(serializers.ModelSerializer):
    # Incluye el comité relacionado 
    committee = CommitteeSerializer(read_only=True)
    
    class Meta:
        model = Country
        fields = ['id', 'name', 'committee', 'notes']


class CustomUserSerializer(serializers.ModelSerializer):
    # Relaciona la edición de Panammun, comité, y país del usuario
    
    committee_staff = CommitteeSerializer(read_only=True, required=False)
    country = CountrySerializer(read_only=True, required=False)
    password = serializers.CharField(write_only=True, required=True, min_length=8)
    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'first_name', 'last_name', 'email', 'phone_number', 'phone_number_2', 'account_type', 
                  'school', 'notes', 'panammun_edition', 'committee_staff', 'country', 'voucher', 'password']

    def create(self, validated_data):
        panammun_edition = validated_data.pop('panammun_edition', None)

        password = validated_data.pop('password')
        user = CustomUser(**validated_data)
        user.set_password(password) 
        user.save()
        if panammun_edition:
            user.panammun_edition = panammun_edition
            user.save()

        return user