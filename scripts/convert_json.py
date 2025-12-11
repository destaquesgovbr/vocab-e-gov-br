#!/usr/bin/env python3
"""
Converte JSON do formato jstree para formato simplificado para Alpine.js.
"""

import json
import sys
from pathlib import Path


def convert_node(node: dict, base_uri: str) -> dict:
    """Converte um nó do formato jstree para o formato simplificado."""
    # Extrair label do nó
    data = node.get('data', '')
    if isinstance(data, dict):
        label = data.get('title') or data.get('name', '')
    else:
        label = str(data)

    # Extrair ID
    attr = node.get('attr', {})
    node_id = attr.get('id', '')

    # Construir resultado
    result = {
        'id': node_id,
        'label': label.strip() if label else node_id,
        'uri': f"{base_uri}#{node_id}" if node_id else base_uri
    }

    # Processar filhos recursivamente
    children = node.get('children', [])
    if children:
        result['children'] = [
            convert_node(child, base_uri)
            for child in children
        ]

    return result


def convert_vcge_json(input_path: Path, output_path: Path, base_uri: str):
    """Converte arquivo VCGE de jstree para formato Alpine.js."""
    with open(input_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    converted = convert_node(data, base_uri)

    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(converted, f, ensure_ascii=False, indent=2)

    print(f"Converted {input_path} -> {output_path}")

    # Contar nós
    def count_nodes(node):
        count = 1
        for child in node.get('children', []):
            count += count_nodes(child)
        return count

    total = count_nodes(converted)
    print(f"Total nodes: {total}")


def main():
    base_dir = Path(__file__).parent.parent

    # VCGE 2011/03
    convert_vcge_json(
        base_dir / 'raw_content/2011/03/vcge-treeview.json',
        base_dir / 'docs/data/vcge-2011-tree.json',
        'http://vocab.e.gov.br/2011/03/vcge'
    )


if __name__ == '__main__':
    main()
