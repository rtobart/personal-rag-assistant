import json
from notion_client import Client

from app.config.config import VARS
from app.config.config_instance import ConfigInstance

class NotionService:
    """
    Notion service to interact with Notion API.
    """
    def __init__(self):
        self.token = ConfigInstance.get(VARS.NOTION_API_KEY)
        self.notion = Client(auth=self.token)
        self.block_id = ConfigInstance.get(VARS.NOTION_PAGE_ID)

    def _extract_plain_text_from_block(self, block):
        """
        Extract plain text from a single block based on its type.
        """
        block_type = block.get("type")
        
        # Mapeo de tipos de bloque y sus estructuras de texto
        text_extractors = {
            "paragraph": lambda b: self._get_rich_text(b["paragraph"]["rich_text"]),
            "heading_1": lambda b: self._get_rich_text(b["heading_1"]["rich_text"]),
            "heading_2": lambda b: self._get_rich_text(b["heading_2"]["rich_text"]),
            "heading_3": lambda b: self._get_rich_text(b["heading_3"]["rich_text"]),
            "bulleted_list_item": lambda b: self._get_rich_text(b["bulleted_list_item"]["rich_text"]),
            "numbered_list_item": lambda b: self._get_rich_text(b["numbered_list_item"]["rich_text"]),
            "to_do": lambda b: self._get_rich_text(b["to_do"]["rich_text"]),
            "toggle": lambda b: self._get_rich_text(b["toggle"]["rich_text"]),
            "quote": lambda b: self._get_rich_text(b["quote"]["rich_text"]),
            "callout": lambda b: self._get_rich_text(b["callout"]["rich_text"]),
            "code": lambda b: b["code"]["rich_text"][0]["plain_text"] if b["code"]["rich_text"] else "",
        }
        
        if block_type in text_extractors:
            try:
                return text_extractors[block_type](block)
            except (KeyError, IndexError, TypeError):
                return ""
        
        return ""

    def _get_rich_text(self, rich_text_array):
        """
        Extract plain text from rich_text array.
        """
        if not rich_text_array:
            return ""
        
        return "".join([text_obj.get("plain_text", "") for text_obj in rich_text_array])

    def _get_blocks_recursively(self, block_id):
        """
        Get all blocks recursively, including children blocks.
        """
        all_blocks = []
        
        try:
            response = self.notion.blocks.children.list(block_id=block_id)
            blocks = response.get("results", [])
            
            for block in blocks:
                all_blocks.append(block)
                
                # Si el bloque tiene hijos, obtenerlos recursivamente
                if block.get("has_children"):
                    child_blocks = self._get_blocks_recursively(block["id"])
                    all_blocks.extend(child_blocks)
                    
        except Exception as e:
            print(f"Error obteniendo bloques: {e}")
            
        return all_blocks

    async def get_blocks_children(self):
        """
        Get children blocks of a page and extract all plain text as a list.
        """
        try:
            # Obtener todos los bloques (incluyendo hijos)
            all_blocks = self._get_blocks_recursively(self.block_id)
            
            # Extraer texto plano de cada bloque
            plain_texts = []
            for block in all_blocks:
                plain_text = self._extract_plain_text_from_block(block)
                if plain_text.strip():  # Solo agregar si no está vacío
                    plain_texts.append(plain_text.strip())
            
            return plain_texts
            
        except Exception as e:
            print(f"Error procesando bloques: {e}")
            return []

    def get_all_plain_text_list(self):
        """
        Get all plain text as a list of strings (one per block).
        """
        try:
            all_blocks = self._get_blocks_recursively(self.block_id)
            
            plain_texts = []
            for block in all_blocks:
                plain_text = self._extract_plain_text_from_block(block)
                if plain_text.strip():
                    plain_texts.append(plain_text.strip())
            
            return plain_texts
            
        except Exception as e:
            print(f"Error procesando bloques: {e}")
            return []

def get_notion_instance():
    """
    Get Notion instance.
    """
    return NotionService()