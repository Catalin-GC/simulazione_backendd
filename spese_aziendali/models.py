from django.conf import settings
from django.db import models


class CategoriaSpesa(models.Model):
    descrizione = models.CharField(max_length=100, unique=True)

    class Meta:
        verbose_name = "Categoria di spesa"
        verbose_name_plural = "Categorie di spesa"

    def __str__(self):
        return self.descrizione


class RichiestaRimborso(models.Model):
    class Stato(models.TextChoices):
        IN_ATTESA = "IN_ATTESA", "In attesa"
        APPROVATA = "APPROVATA", "Approvata"
        RIFIUTATA = "RIFIUTATA", "Rifiutata"
        LIQUIDATA = "LIQUIDATA", "Liquidata"

    dipendente = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="richieste",
    )
    categoria = models.ForeignKey(
        CategoriaSpesa,
        on_delete=models.PROTECT,
        related_name="richieste",
    )
    data_inserimento = models.DateTimeField(auto_now_add=True)
    data_spesa = models.DateField()
    importo = models.DecimalField(max_digits=10, decimal_places=2)
    descrizione = models.TextField()
    riferimento_giustificativo = models.CharField(
        max_length=100, blank=True, default=""
    )
    stato = models.CharField(
        max_length=20, choices=Stato.choices, default=Stato.IN_ATTESA
    )

    # Campi di valutazione / liquidazione
    responsabile_valutazione = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True, blank=True,
        related_name="valutazioni",
    )
    data_valutazione = models.DateTimeField(null=True, blank=True)
    motivazione_rifiuto = models.TextField(blank=True, default="")
    data_liquidazione = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ["-data_inserimento"]
        verbose_name = "Richiesta di rimborso"
        verbose_name_plural = "Richieste di rimborso"

    def __str__(self):
        return f"#{self.pk} - {self.dipendente} - {self.importo}€ ({self.get_stato_display()})"