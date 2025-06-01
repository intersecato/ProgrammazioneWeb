from django.db import models
from django.db.models import CompositePrimaryKey


class Sala(models.Model):
    numero = models.IntegerField(primary_key=True, db_column='numero')
    numPosti = models.IntegerField(db_column='numPosti')
    dim = models.IntegerField(db_column='dim')
    numFile = models.IntegerField(db_column='numFile')
    numPostiPerFila = models.IntegerField(db_column='numPostiPerFila')

    TIPO_CHOICES = [
        ('3-D', '3-D'),
        ('tradizionale', 'Tradizionale'),
    ]
    tipo = models.CharField(max_length=20, choices=TIPO_CHOICES, db_column='tipo')

    class Meta:
        db_table = 'sala'
        managed = False

    def __str__(self):
        return f"Sala {self.numero}"


class Film(models.Model):
    codice = models.AutoField(primary_key=True, db_column='codice')
    titolo = models.CharField(max_length=100, db_column='titolo')
    anno = models.IntegerField(db_column='anno')
    durata = models.PositiveIntegerField(db_column='durata')
    lingua = models.CharField(max_length=30, db_column='lingua')

    class Meta:
        db_table = 'film'
        managed = False

    def __str__(self):
        return f"{self.titolo} ({self.anno})"


class Proiezione(models.Model):
    numProiezione = models.IntegerField(primary_key=True, db_column='numProiezione')
    sala = models.ForeignKey(Sala, on_delete=models.CASCADE, related_name="proiezioni", db_column='sala')
    filmProiettato = models.ForeignKey(Film, on_delete=models.CASCADE, db_column='filmProiettato')
    data = models.DateField(db_column='data')
    ora = models.TimeField(db_column='ora')

    class Meta:
        db_table = 'proiezione'
        managed = False

    def __str__(self):
        return f"Proiezione {self.numProiezione}"


class Biglietto(models.Model):
    pk = CompositePrimaryKey("numProiezione", "numFila", "numPosto")

    numProiezione = models.ForeignKey("Proiezione", on_delete=models.CASCADE, db_column="numProiezione")
    numFila = models.IntegerField(db_column="numFila")
    numPosto = models.IntegerField(db_column="numPosto")
    dataVendita = models.DateField(db_column="dataVendita")
    prezzo = models.DecimalField(max_digits=6, decimal_places=2, db_column="prezzo")

    class Meta:
        db_table = "biglietto"
        managed = False

    def __str__(self):
        return f"Biglietto P{self.numPosto} F{self.numFila} per Proiezione {self.numProiezione.numProiezione}"
