from notion_client import Client
from notion_client.errors import APIResponseError, RequestTimeoutError

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
        block_type = block.get("type", "")

        # Tipos de bloque que usan rich_text estándar
        standard_types = {
            "paragraph", "heading_1", "heading_2", "heading_3",
            "bulleted_list_item", "numbered_list_item", "to_do",
            "toggle", "quote", "callout"
        }

        try:
            if block_type in standard_types:
                rich_text = block.get(block_type, {}).get("rich_text", [])
                return self._get_rich_text(rich_text)
            elif block_type == "code":
                code_data = block.get("code", {}).get("rich_text", [])
                return code_data[0].get("plain_text", "") if code_data else ""
        except (KeyError, IndexError, TypeError):
            pass

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

        except (APIResponseError, RequestTimeoutError, KeyError, AttributeError, TypeError) as e:
            print(f"Error obteniendo bloques: {e}")

        return all_blocks

    def _extract_text_from_blocks(self, blocks):
        """
        Extract plain text from a list of blocks.
        """
        plain_texts = []
        for block in blocks:
            plain_text = self._extract_plain_text_from_block(block)
            if plain_text.strip():
                plain_texts.append(plain_text.strip())
        return plain_texts

    def get_all_plain_text_list(self):
        """
        Get all plain text as a list of strings (one per block).
        """
        try:
            all_blocks = self._get_blocks_recursively(self.block_id)
            return self._extract_text_from_blocks(all_blocks)
        except (APIResponseError, RequestTimeoutError, KeyError, AttributeError, TypeError) as e:
            print(f"Error procesando bloques: {e}")
            return []

def get_notion_instance():
    """
    Get Notion instance.
    """
    return NotionService()