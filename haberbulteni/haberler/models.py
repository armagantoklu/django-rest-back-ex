from django.db import models


class Gazeteci(models.Model):
    isim = models.CharField(max_length=50)
    soyisim = models.CharField(max_length=50)
    biyografi = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.isim


class Makale(models.Model):
    yazar = models.ForeignKey(Gazeteci, on_delete=models.CASCADE, related_name='makaleler')
    # one to many, gazeteci silinince makaleleri de silinsin
    baslik = models.CharField(max_length=50)
    aciklama = models.CharField(max_length=50)
    metin = models.TextField(max_length=50)
    sehir = models.CharField(max_length=50)
    aktif = models.BooleanField(default=True)
    yayimlanma_tarihi = models.DateField()
    yaratilme_tarihi = models.DateTimeField(auto_now_add=True)  # olustur otomatik olarak ve bir daha degisme
    guncellenme_tarihi = models.DateTimeField(auto_now=True)  # otomatik olarak o zamani al

    def __str__(self):
        # return (f"{self.yazar} {self.baslik} {self.aciklama} {self.metin} {self.sehir} {self.aktif}")
        return self.baslik

