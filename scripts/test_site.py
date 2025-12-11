#!/usr/bin/env python3
"""
Teste do site vocab-e-gov-br com Playwright
"""

from playwright.sync_api import sync_playwright
import sys

BASE_URL = "http://127.0.0.1:8765/vocab-e-gov-br/"

def test_homepage(page):
    """Testa a homepage"""
    print("\n=== Testando Homepage ===")
    page.goto(BASE_URL)
    page.wait_for_load_state("networkidle")

    # Screenshot
    page.screenshot(path="/tmp/vocab-homepage.png", full_page=True)
    print("Screenshot salvo: /tmp/vocab-homepage.png")

    # Verificar título
    title = page.title()
    print(f"Título: {title}")

    # Verificar se os cards estão renderizados
    cards = page.locator(".grid.cards").count()
    print(f"Número de grid cards encontrados: {cards}")

    # Verificar se os ícones estão renderizando (não devem aparecer como texto)
    icon_text = page.locator("text=':material-check-circle:'").count()
    if icon_text > 0:
        print(f"❌ ERRO: {icon_text} ícones não renderizados (aparecem como texto)")
    else:
        print("✓ Ícones renderizados corretamente")

    # Verificar conteúdo da página
    content = page.content()
    if ":material-" in content:
        print("❌ ERRO: Sintaxe de ícones Material não processada")
        # Encontrar onde
        lines = [l for l in content.split('\n') if ':material-' in l]
        for line in lines[:3]:
            print(f"  Linha: {line[:100]}...")
    else:
        print("✓ Sintaxe de ícones processada")

    return cards > 0 and icon_text == 0


def test_explorer(page):
    """Testa o explorador VCGE"""
    print("\n=== Testando Explorador VCGE ===")
    page.goto(BASE_URL + "explorer/")
    page.wait_for_load_state("networkidle")

    # Esperar Alpine.js carregar
    page.wait_for_timeout(2000)

    # Screenshot
    page.screenshot(path="/tmp/vocab-explorer.png", full_page=True)
    print("Screenshot salvo: /tmp/vocab-explorer.png")

    # Verificar se a árvore carregou
    tree_panel = page.locator(".vcge-tree-panel").count()
    print(f"Painel da árvore encontrado: {tree_panel > 0}")

    # Verificar se há mensagem de loading
    loading = page.locator(".vcge-loading").is_visible()
    print(f"Loading visível: {loading}")

    # Verificar se há erro
    error = page.locator(".vcge-error").is_visible()
    if error:
        error_text = page.locator(".vcge-error").text_content()
        print(f"❌ ERRO encontrado: {error_text}")

    # Verificar se há nós na árvore
    tree_nodes = page.locator(".vcge-tree-node").count()
    print(f"Nós da árvore encontrados: {tree_nodes}")

    # Verificar se o JSON foi carregado (verificar console)
    console_messages = []
    page.on("console", lambda msg: console_messages.append(f"{msg.type}: {msg.text}"))

    # Recarregar para capturar mensagens do console
    page.reload()
    page.wait_for_timeout(3000)

    print(f"\nMensagens do console:")
    for msg in console_messages:
        print(f"  {msg}")

    # Tentar buscar
    search_input = page.locator(".vcge-search-input")
    if search_input.count() > 0:
        search_input.fill("agricultura")
        page.wait_for_timeout(500)

        match_count = page.locator(".vcge-match-count").text_content()
        print(f"Resultado da busca por 'agricultura': {match_count}")

    return tree_nodes > 0


def main():
    print("Iniciando testes do site vocab-e-gov-br")
    print("=" * 50)

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        # Capturar erros de rede
        page.on("requestfailed", lambda request: print(f"Request failed: {request.url}"))

        results = []

        try:
            results.append(("Homepage", test_homepage(page)))
        except Exception as e:
            print(f"❌ Erro no teste da homepage: {e}")
            results.append(("Homepage", False))

        try:
            results.append(("Explorer", test_explorer(page)))
        except Exception as e:
            print(f"❌ Erro no teste do explorer: {e}")
            results.append(("Explorer", False))

        browser.close()

    print("\n" + "=" * 50)
    print("RESUMO DOS TESTES:")
    for name, passed in results:
        status = "✓ PASSOU" if passed else "❌ FALHOU"
        print(f"  {name}: {status}")

    return all(r[1] for r in results)


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
