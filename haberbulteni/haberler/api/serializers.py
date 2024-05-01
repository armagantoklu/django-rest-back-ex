from datetime import datetime, date

from django.utils.timesince import timesince
from rest_framework import serializers
from haberler.models import Makale, Gazeteci


class MakaleSerializer(serializers.ModelSerializer):
    time_since_pub = serializers.SerializerMethodField()

    # yazar = serializers.StringRelatedField()
    # yazar = GazeteciSerializer()

    class Meta:
        model = Makale
        fields = '__all__'  # hepsi
        # fields = ('yazar', 'baslik') #sadece yazar ve baslik
        # exclude = ('yazar', 'baslik') #yazar ve baslik haric hepsi
        # read_only_fields = ['yayimlanma_tarihi', 'guncellenme_tarihi']

    def get_time_since_pub(self, obj):
        now = datetime.now()
        pub_date = obj.yayimlanma_tarihi
        time_delta = timesince(pub_date, now)
        return time_delta

    def validate_yayimlanma_tarihi(self, value):
        today = date.today()
        if value > today:
            raise serializers.ValidationError("ileri tarih olamaz")
        return value


class GazeteciSerializer(serializers.ModelSerializer):
    # makaleler = MakaleSerializer(read_only=True, many=True) #readonly sebebi, yazar olsutururken makale de olusturmamak
    makaleler = serializers.HyperlinkedRelatedField(
        many=True,
        read_only=True,
        view_name="makale_detay",

    )
    class Meta:
        model = Gazeteci
        fields = '__all__'


# makale default serializer
class MakaleDefaultSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    yazar = serializers.CharField(required=False)
    baslik = serializers.CharField(required=False)
    aciklama = serializers.CharField(required=False)
    metin = serializers.CharField(required=False)
    sehir = serializers.CharField(required=False)
    aktif = serializers.BooleanField(required=False)
    yayimlanma_tarihi = serializers.DateField(required=False)
    yaratilme_tarihi = serializers.DateTimeField(read_only=True)
    guncellenme_tarihi = serializers.DateTimeField(read_only=True)

    def create(self, validated_data):
        return Makale.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.yazar = validated_data.get('yazar', instance.yazar)
        instance.baslik = validated_data.get('baslik', instance.baslik)
        instance.aciklama = validated_data.get('aciklama', instance.aciklama)
        instance.metin = validated_data.get('metin', instance.metin)
        instance.sehir = validated_data.get('sehir', instance.sehir)
        instance.aktif = validated_data.get('aktif', instance.aktif)
        instance.yayimlanma_tarihi = validated_data.get('yayimlanma_tarihi', instance.yayimlanma_tarihi)
        instance.save()
        return instance

    def validate(self, data):
        if data['baslik'] == data['aciklama']:
            raise serializers.ValidationError('baslik ve aciklama ayni olamaz')
        return data

    def validate_baslik(self, value):
        if len(value) < 20:
            raise serializers.ValidationError('baslik 20 karakterden kucuk olamaz')
        return value
