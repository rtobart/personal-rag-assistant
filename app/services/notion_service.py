import json
from notion_client import Client

# Tu token de integración
notion = Client(auth="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")

# ID de la página
page_id = "1ee284434f80806c8783e5d956d3223d"

# Obtener bloques hijos de la página
blocks = notion.blocks.children.list(block_id=page_id)

# Mostrar el contenido con indentación legible
print(json.dumps(blocks, indent=2))
