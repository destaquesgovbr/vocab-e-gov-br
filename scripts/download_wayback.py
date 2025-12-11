#!/usr/bin/env python3
"""
Script para baixar arquivos do vocab.e.gov.br via Wayback Machine.

Uso:
    python download_wayback.py --output ../raw_content
"""

import os
import sys
import json
import time
import argparse
import urllib.request
import urllib.error
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed

# Lista de URLs arquivadas (obtida via CDX API)
ARCHIVED_URLS = [
    # Páginas HTML principais
    ("http://vocab.e.gov.br/", "index.html"),
    ("http://vocab.e.gov.br/2011/03/vcge.html", "2011/03/vcge.html"),
    ("http://vocab.e.gov.br/2011/09/org.html", "2011/09/org.html"),
    ("http://vocab.e.gov.br/2013/09/loa.html", "2013/09/loa.html"),
    ("http://vocab.e.gov.br/2013/09/jowl/index.html", "2013/09/jowl/index.html"),
    ("http://vocab.e.gov.br/2013/12/ops.html", "2013/12/ops.html"),
    ("http://vocab.e.gov.br/id/governo.html", "id/governo.html"),

    # Arquivos de dados - VCGE
    ("http://vocab.e.gov.br/2011/03/vcge.json", "2011/03/vcge.json"),
    ("http://vocab.e.gov.br/2011/03/vcge-treeview.json", "2011/03/vcge-treeview.json"),
    ("http://vocab.e.gov.br/2011/03/vcge.n3", "2011/03/vcge.n3"),
    ("http://vocab.e.gov.br/2011/03/vcge.rdf", "2011/03/vcge.rdf"),
    ("http://vocab.e.gov.br/2011/03/vcge.nt", "2011/03/vcge.nt"),
    ("http://vocab.e.gov.br/id/vcge-treeview.json", "id/vcge-treeview.json"),

    # Arquivos de dados - Ontologias
    ("http://vocab.e.gov.br/2013/09/loa.owl", "2013/09/loa.owl"),
    ("http://vocab.e.gov.br/2013/12/cosp.owl", "2013/12/cosp.owl"),
    ("http://vocab.e.gov.br/2011/02/siorg.ttl", "2011/02/siorg.ttl"),
    ("http://vocab.e.gov.br/siafi.ttl", "siafi.ttl"),
    ("http://vocab.e.gov.br/sicaf.ttl", "sicaf.ttl"),

    # SQL
    ("http://vocab.e.gov.br/2013/11/VCGE_2_0_EXP_sql.sql", "2013/11/VCGE_2_0_EXP_sql.sql"),
    ("http://vocab.e.gov.br/2013/11/VCGE_2_0_1_EXP_sql.sql", "2013/11/VCGE_2_0_1_EXP_sql.sql"),

    # CSS
    ("http://vocab.e.gov.br/css/style.css", "css/style.css"),
    ("http://vocab.e.gov.br/css/960_24_col.css", "css/960_24_col.css"),
    ("http://vocab.e.gov.br/css/doc-style.css", "css/doc-style.css"),
    ("http://vocab.e.gov.br/css/custom-theme/jquery-ui-1.8.16.custom.css", "css/custom-theme/jquery-ui-1.8.16.custom.css"),

    # JavaScript - libs
    ("http://vocab.e.gov.br/js/modernizr-2.0.6.min.js", "js/modernizr-2.0.6.min.js"),
    ("http://vocab.e.gov.br/2011/03/_lib/jquery.js", "2011/03/_lib/jquery.js"),
    ("http://vocab.e.gov.br/2011/03/_lib/jquery.jstree.js", "2011/03/_lib/jquery.jstree.js"),
    ("http://vocab.e.gov.br/2011/03/_lib/jquery-ui-1.8.16.custom.min.js", "2011/03/_lib/jquery-ui-1.8.16.custom.min.js"),
    ("http://vocab.e.gov.br/2011/03/_lib/jquery.history.js", "2011/03/_lib/jquery.history.js"),
    ("http://vocab.e.gov.br/2011/03/_lib/jquery.snippet.js", "2011/03/_lib/jquery.snippet.js"),
    ("http://vocab.e.gov.br/2011/03/_lib/jquery.snippet.css", "2011/03/_lib/jquery.snippet.css"),
    ("http://vocab.e.gov.br/2011/03/vcge-nav.js", "2011/03/vcge-nav.js"),
    ("http://vocab.e.gov.br/id/vcge-nav.js", "id/vcge-nav.js"),

    # jOWL
    ("http://vocab.e.gov.br/2013/09/jowl/scripts/jOWL.js", "2013/09/jowl/scripts/jOWL.js"),
    ("http://vocab.e.gov.br/2013/09/jowl/scripts/jOWL_UI.js", "2013/09/jowl/scripts/jOWL_UI.js"),
    ("http://vocab.e.gov.br/2013/09/jowl/scripts/jOWLBrowser.js", "2013/09/jowl/scripts/jOWLBrowser.js"),
    ("http://vocab.e.gov.br/2013/09/jowl/scripts/jquery.tooltip.js", "2013/09/jowl/scripts/jquery.tooltip.js"),
    ("http://vocab.e.gov.br/2013/09/jowl/css/jOWL.css", "2013/09/jowl/css/jOWL.css"),
    ("http://vocab.e.gov.br/2013/09/jowl/css/jq/custom-theme/jquery-ui-1.7.custom.css", "2013/09/jowl/css/jq/custom-theme/jquery-ui-1.7.custom.css"),

    # Temas jstree
    ("http://vocab.e.gov.br/2011/03/themes/apple/style.css", "2011/03/themes/apple/style.css"),
    ("http://vocab.e.gov.br/2011/03/themes/apple/bg.jpg", "2011/03/themes/apple/bg.jpg"),
    ("http://vocab.e.gov.br/2011/03/themes/apple/d.png", "2011/03/themes/apple/d.png"),
    ("http://vocab.e.gov.br/2011/03/themes/apple/throbber.gif", "2011/03/themes/apple/throbber.gif"),
    ("http://vocab.e.gov.br/id/themes/apple/style.css", "id/themes/apple/style.css"),
    ("http://vocab.e.gov.br/id/themes/apple/bg.jpg", "id/themes/apple/bg.jpg"),
    ("http://vocab.e.gov.br/id/themes/apple/d.png", "id/themes/apple/d.png"),
    ("http://vocab.e.gov.br/id/themes/apple/throbber.gif", "id/themes/apple/throbber.gif"),

    # Imagens
    ("http://vocab.e.gov.br/img/bg/govbr_2011_e-PING.png", "img/bg/govbr_2011_e-PING.png"),
    ("http://vocab.e.gov.br/img/bg/bg_body.jpg", "img/bg/bg_body.jpg"),
    ("http://vocab.e.gov.br/2013/09/ontologia-da-despesa.png", "2013/09/ontologia-da-despesa.png"),
    ("http://vocab.e.gov.br/2013/09/item-de-despesa.png", "2013/09/item-de-despesa.png"),
    ("http://vocab.e.gov.br/2013/09/exemplo-consulta-sparql.png", "2013/09/exemplo-consulta-sparql.png"),
    ("http://vocab.e.gov.br/2013/09/exemplo-grafo-rdf.png", "2013/09/exemplo-grafo-rdf.png"),
    ("http://vocab.e.gov.br/2013/09/exemplo-ntriples.png", "2013/09/exemplo-ntriples.png"),
    ("http://vocab.e.gov.br/2013/09/exemplo-rdf-xml.png", "2013/09/exemplo-rdf-xml.png"),
    ("http://vocab.e.gov.br/2013/09/exemplo-tripla-rdf.png", "2013/09/exemplo-tripla-rdf.png"),
    ("http://vocab.e.gov.br/2013/09/exemplo-turtle.png", "2013/09/exemplo-turtle.png"),
    ("http://vocab.e.gov.br/2013/09/ferramentas-manipulacao.png", "2013/09/ferramentas-manipulacao.png"),
    ("http://vocab.e.gov.br/2013/09/mapeamento-rdf-owl.png", "2013/09/mapeamento-rdf-owl.png"),
    ("http://vocab.e.gov.br/2011/09/organizacoes-siorg-completo.png", "2011/09/organizacoes-siorg-completo.png"),
    ("http://vocab.e.gov.br/2011/09/organizacoes-siorg-externos.png", "2011/09/organizacoes-siorg-externos.png"),
    ("http://vocab.e.gov.br/2011/09/organizacoes-siorg-nucleo.png", "2011/09/organizacoes-siorg-nucleo.png"),

    # jOWL images
    ("http://vocab.e.gov.br/2013/09/jowl/img/treeView/dotted/tvi.gif", "2013/09/jowl/img/treeView/dotted/tvi.gif"),
    ("http://vocab.e.gov.br/2013/09/jowl/img/treeView/dotted/tvic.gif", "2013/09/jowl/img/treeView/dotted/tvic.gif"),
    ("http://vocab.e.gov.br/2013/09/jowl/img/treeView/dotted/tvie.gif", "2013/09/jowl/img/treeView/dotted/tvie.gif"),
    ("http://vocab.e.gov.br/2013/09/jowl/img/treeView/dotted/tvil.gif", "2013/09/jowl/img/treeView/dotted/tvil.gif"),
    ("http://vocab.e.gov.br/2013/09/jowl/img/treeView/dotted/tvilc.gif", "2013/09/jowl/img/treeView/dotted/tvilc.gif"),
    ("http://vocab.e.gov.br/2013/09/jowl/img/treeView/dotted/tvile.gif", "2013/09/jowl/img/treeView/dotted/tvile.gif"),
    ("http://vocab.e.gov.br/2013/09/jowl/img/treeView/dotted/tviload.gif", "2013/09/jowl/img/treeView/dotted/tviload.gif"),

    # jQuery UI images
    ("http://vocab.e.gov.br/css/custom-theme/images/ui-bg_flat_10_000000_40x100.png", "css/custom-theme/images/ui-bg_flat_10_000000_40x100.png"),
    ("http://vocab.e.gov.br/css/custom-theme/images/ui-bg_glass_100_f6f6f6_1x400.png", "css/custom-theme/images/ui-bg_glass_100_f6f6f6_1x400.png"),
    ("http://vocab.e.gov.br/css/custom-theme/images/ui-bg_glass_65_ffffff_1x400.png", "css/custom-theme/images/ui-bg_glass_65_ffffff_1x400.png"),
    ("http://vocab.e.gov.br/css/custom-theme/images/ui-icons_222222_256x240.png", "css/custom-theme/images/ui-icons_222222_256x240.png"),

    # jOWL jQuery UI images
    ("http://vocab.e.gov.br/2013/09/jowl/css/jq/custom-theme/images/ui-bg_flat_0_aaaaaa_40x100.png", "2013/09/jowl/css/jq/custom-theme/images/ui-bg_flat_0_aaaaaa_40x100.png"),
    ("http://vocab.e.gov.br/2013/09/jowl/css/jq/custom-theme/images/ui-bg_glass_55_fbf9ee_1x400.png", "2013/09/jowl/css/jq/custom-theme/images/ui-bg_glass_55_fbf9ee_1x400.png"),
    ("http://vocab.e.gov.br/2013/09/jowl/css/jq/custom-theme/images/ui-icons_222222_256x240.png", "2013/09/jowl/css/jq/custom-theme/images/ui-icons_222222_256x240.png"),

    # PDF
    ("http://vocab.e.gov.br/2011/09/org.pdf", "2011/09/org.pdf"),
]


def get_wayback_url(original_url: str) -> str:
    """Constrói URL do Wayback Machine para download raw."""
    # Usar timestamp de dezembro 2019 (última snapshot conhecida)
    return f"https://web.archive.org/web/20191222064047id_/{original_url}"


def download_file(url: str, output_path: Path, retries: int = 3) -> tuple[str, bool, str]:
    """Baixa um arquivo do Wayback Machine."""
    wayback_url = get_wayback_url(url)

    for attempt in range(retries):
        try:
            # Criar diretório se não existir
            output_path.parent.mkdir(parents=True, exist_ok=True)

            # Headers para evitar bloqueio
            headers = {
                'User-Agent': 'Mozilla/5.0 (compatible; vocab-archiver/1.0)',
                'Accept': '*/*',
            }

            request = urllib.request.Request(wayback_url, headers=headers)

            with urllib.request.urlopen(request, timeout=30) as response:
                content = response.read()

                # Salvar arquivo
                with open(output_path, 'wb') as f:
                    f.write(content)

                return (str(output_path), True, f"OK ({len(content)} bytes)")

        except urllib.error.HTTPError as e:
            if e.code == 404:
                return (str(output_path), False, f"Not found (404)")
            if attempt < retries - 1:
                time.sleep(2 ** attempt)
                continue
            return (str(output_path), False, f"HTTP Error: {e.code}")

        except Exception as e:
            if attempt < retries - 1:
                time.sleep(2 ** attempt)
                continue
            return (str(output_path), False, f"Error: {str(e)}")

    return (str(output_path), False, "Max retries exceeded")


def main():
    parser = argparse.ArgumentParser(description='Download vocab.e.gov.br from Wayback Machine')
    parser.add_argument('--output', '-o', default='../raw_content',
                        help='Output directory (default: ../raw_content)')
    parser.add_argument('--workers', '-w', type=int, default=4,
                        help='Number of parallel workers (default: 4)')
    parser.add_argument('--dry-run', action='store_true',
                        help='Show what would be downloaded without downloading')
    args = parser.parse_args()

    output_dir = Path(args.output)

    if args.dry_run:
        print(f"Would download {len(ARCHIVED_URLS)} files to {output_dir}")
        for url, local_path in ARCHIVED_URLS:
            print(f"  {url} -> {local_path}")
        return

    print(f"Downloading {len(ARCHIVED_URLS)} files to {output_dir}")
    print(f"Using {args.workers} parallel workers")
    print("-" * 60)

    results = {"success": 0, "failed": 0, "errors": []}

    with ThreadPoolExecutor(max_workers=args.workers) as executor:
        futures = {
            executor.submit(download_file, url, output_dir / local_path): (url, local_path)
            for url, local_path in ARCHIVED_URLS
        }

        for future in as_completed(futures):
            url, local_path = futures[future]
            output_path, success, message = future.result()

            status = "✓" if success else "✗"
            print(f"  {status} {local_path}: {message}")

            if success:
                results["success"] += 1
            else:
                results["failed"] += 1
                results["errors"].append((local_path, message))

            # Rate limiting
            time.sleep(0.5)

    print("-" * 60)
    print(f"Downloaded: {results['success']}/{len(ARCHIVED_URLS)}")

    if results["errors"]:
        print(f"\nFailed downloads ({results['failed']}):")
        for path, error in results["errors"]:
            print(f"  - {path}: {error}")


if __name__ == "__main__":
    main()
