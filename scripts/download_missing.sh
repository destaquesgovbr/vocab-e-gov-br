#!/bin/bash
# Script para baixar arquivos faltantes do Wayback Machine
# Execute: bash download_missing.sh

OUTPUT_DIR="../raw_content"
WAYBACK_PREFIX="https://web.archive.org/web/20191222064047id_/http://vocab.e.gov.br"

mkdir -p "$OUTPUT_DIR"/{css,js,img/bg,2011/03/_lib,2011/03/themes/apple,2011/09,2013/09/jowl/{scripts,css/jq/custom-theme/images,img/treeView/dotted},2013/11,2013/12,id/themes/apple,id/_lib}

# Lista de arquivos faltantes
declare -a FILES=(
    # Dados importantes
    "2011/03/vcge.nt"
    "id/vcge-treeview.json"
    "2013/12/cosp.owl"
    "2011/02/siorg.ttl"
    "siafi.ttl"
    "sicaf.ttl"
    "2013/11/VCGE_2_0_EXP_sql.sql"
    "2013/11/VCGE_2_0_1_EXP_sql.sql"

    # JavaScript essencial
    "js/modernizr-2.0.6.min.js"
    "2011/03/_lib/jquery.js"
    "2011/03/_lib/jquery.jstree.js"
    "2011/03/_lib/jquery-ui-1.8.16.custom.min.js"
    "2011/03/_lib/jquery.history.js"
    "2011/03/_lib/jquery.snippet.js"
    "2011/03/_lib/jquery.snippet.css"
    "2011/03/vcge-nav.js"
    "id/vcge-nav.js"

    # jOWL
    "2013/09/jowl/scripts/jOWL.js"
    "2013/09/jowl/scripts/jOWL_UI.js"
    "2013/09/jowl/scripts/jOWLBrowser.js"
    "2013/09/jowl/scripts/jquery.tooltip.js"
    "2013/09/jowl/css/jOWL.css"
    "2013/09/jowl/css/jq/custom-theme/jquery-ui-1.7.custom.css"

    # Temas jstree
    "2011/03/themes/apple/style.css"
    "2011/03/themes/apple/bg.jpg"
    "2011/03/themes/apple/d.png"
    "2011/03/themes/apple/throbber.gif"
    "id/themes/apple/style.css"
    "id/themes/apple/bg.jpg"
    "id/themes/apple/d.png"
    "id/themes/apple/throbber.gif"

    # Imagens
    "img/bg/govbr_2011_e-PING.png"
    "img/bg/bg_body.jpg"
    "2013/09/exemplo-ntriples.png"
    "2013/09/exemplo-tripla-rdf.png"
    "2013/09/exemplo-turtle.png"
    "2013/09/ferramentas-manipulacao.png"
    "2013/09/mapeamento-rdf-owl.png"
    "2011/09/organizacoes-siorg-completo.png"
    "2011/09/organizacoes-siorg-externos.png"
    "2011/09/organizacoes-siorg-nucleo.png"

    # jOWL images
    "2013/09/jowl/img/treeView/dotted/tvi.gif"
    "2013/09/jowl/img/treeView/dotted/tvic.gif"
    "2013/09/jowl/img/treeView/dotted/tvie.gif"
    "2013/09/jowl/img/treeView/dotted/tvil.gif"
    "2013/09/jowl/img/treeView/dotted/tvilc.gif"
    "2013/09/jowl/img/treeView/dotted/tvile.gif"
    "2013/09/jowl/img/treeView/dotted/tviload.gif"

    # PDF
    "2011/09/org.pdf"
)

echo "Downloading ${#FILES[@]} files..."
echo "========================================"

for file in "${FILES[@]}"; do
    echo "Downloading: $file"
    curl -sL "${WAYBACK_PREFIX}/${file}" -o "${OUTPUT_DIR}/${file}"
    if [ $? -eq 0 ]; then
        echo "  ✓ OK"
    else
        echo "  ✗ FAILED"
    fi
    sleep 1  # Rate limiting
done

echo "========================================"
echo "Done!"
