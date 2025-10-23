from django.db import models

class Atlet(models.Model):
    # key unik untuk matching dengan file medali
    short_name = models.CharField(max_length=100, unique=True, db_index=True, blank=True, null=True)
    
    # data untuk Guest
    name = models.CharField(max_length=255)
    country = models.CharField(max_length=100)
    discipline = models.CharField(max_length=100)
    
    # data detail (untuk Member & Admin, sesuai CSV
    gender = models.CharField(max_length=10, blank=True, null=True)
    birth_date = models.DateField(blank=True, null=True)
    birth_place = models.CharField(max_length=100, blank=True, null=True)
    birth_country = models.CharField(max_length=100, blank=True, null=True)
    
    # nanti akan dianggap sama dengan country. jadi assume nationality=country
    nationality = models.CharField(max_length=100, blank=True, null=True) 
    
    # fitur Admin 
    is_visible = models.BooleanField(default=True) 

    def __str__(self):
        return self.name

class Medali(models.Model):
    # relasi ke atlet (parentnya)
    atlet = models.ForeignKey(Atlet, on_delete=models.CASCADE, related_name='medali')
    
    # detail medali 
    medal_type = models.CharField(max_length=50) # cth: Gold Medal
    event = models.CharField(max_length=255) # cth: Men's 100m Backstroke - S2
    medal_date = models.CharField(max_length=50) # cth: 2021-08-25

    def __str__(self):
        return f"{self.atlet.name} - {self.event} ({self.medal_type})"