from django.contrib.auth.models import User, Group
from models import Book, Appliances
from rest_framework import serializers


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('url', 'username', 'email', 'groups', 'password')


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ('url', 'name')


class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ('bookid', 'bookname', 'bookprice', 'booksalescount')


class AppliancesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Appliances
        fields = ('name', 'ip', 'location', 'netbios_name', 'os_type')
