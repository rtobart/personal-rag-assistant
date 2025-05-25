import re
from app.config.config import VARS
from app.config.config_instance import ConfigInstance
import unicodedata


class TextTools:

    async def replace_patter_value(self, text: str, value: dict = {}) -> str:
        """
        Reemplaza patrones en un texto usando expresiones regulares.

        :param texto: El texto que contiene los patrones a reemplazar.
        :param reemplazos: Un diccionario con los patrones y sus valores de reemplazo.
                   Las claves son las expresiones regulares y los valores las cadenas de reemplazo.
        :return: El texto con los reemplazos aplicados.
        """
        # Iterar sobre los patrones y reemplazar en el texto
        texto = text
        for clave, valor in value.items():
            texto = re.sub(clave, valor, texto)
        return texto

    async def normalizar_texto(self, texto: str) -> str:
        """
        Normaliza el texto eliminando tildes, convirtiendo a minúsculas y
        quitando caracteres especiales como puntuaciones.

        Args:
            texto (str): El texto a normalizar.

        Returns:
            str: El texto normalizado.
        """
        # Convertir a minúsculas
        texto = texto.lower()

        # Eliminar tildes y acentos
        texto = "".join(
            char
            for char in unicodedata.normalize("NFKD", texto)
            if not unicodedata.combining(char)
        )

        # Eliminar puntuación y caracteres especiales, dejando solo letras y espacios
        texto = re.sub(r"[^a-z\s]", "", texto)

        # Quitar espacios adicionales
        texto = texto.strip()

        return texto
