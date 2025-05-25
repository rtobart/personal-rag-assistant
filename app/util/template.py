import json
import threading


class TemplateManager:
    """Clase para manejar la configuración desde un archivo JSON."""

    CONFIG_FILE = "./app/template/template-conversation.json"
    _lock = threading.Lock()  # Lock para sincronización en concurrencia

    def __init__(self):
        self._config = {}
        self.load_config()

    def load_config(self):
        """Carga la configuración desde el archivo JSON una sola vez."""
        with TemplateManager._lock:
            try:
                with open(TemplateManager.CONFIG_FILE, "r", encoding="utf-8") as f:
                    self._config = json.load(f)
            except FileNotFoundError:
                return None
            except json.JSONDecodeError:
                self._config = {
                    "instruction": "Responde en un formato estructurado.",
                    "conversation": [],
                    "retrieved_context": [],
                    "user_query": "",
                    "fixed_parameter": "valor_fijo",
                }

    def get_config(self):
        """Devuelve una copia de la configuración en memoria."""
        with TemplateManager._lock:
            return self._config.copy()
