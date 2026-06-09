from rest_framework import serializers
from .models import CategoriaSpesa, RichiestaRimborso


class CategoriaSpesaSerializer(serializers.ModelSerializer):
    class Meta:
        model = CategoriaSpesa
        fields = ["id", "descrizione"]


class RichiestaRimborsoSerializer(serializers.ModelSerializer):
    dipendente_nome = serializers.CharField( source="dipendente.__str__", read_only=True)
    categoria_descrizione = serializers.CharField( source="categoria.descrizione", read_only=True)
    stato_display = serializers.CharField( source="get_stato_display", read_only=True)

    class Meta:
        model = RichiestaRimborso
        fields = [
            "id", "dipendente", "dipendente_nome",
            "categoria", "categoria_descrizione",
            "data_inserimento", "data_spesa", "importo", "descrizione",
            "riferimento_giustificativo", "stato", "stato_display",
            "responsabile_valutazione", "data_valutazione",
            "motivazione_rifiuto", "data_liquidazione",
        ]
        read_only_fields = [
            "stato", "dipendente", "data_inserimento",
            "responsabile_valutazione", "data_valutazione",
            "motivazione_rifiuto", "data_liquidazione",
        ]

    def validate_importo(self, value):
        if value <= 0:
            raise serializers.ValidationError("L'importo deve essere maggiore di zero.")
        return value

    def validate_descrizione(self, value):
        if not value.strip():
            raise serializers.ValidationError("La descrizione è obbligatoria.")
        return value

    def validate_riferimento_giustificativo(self, value):
        if value and not value.strip():
            raise serializers.ValidationError(
                "Il riferimento giustificativo non può essere solo spazi."
            )
        return value