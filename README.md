# Vocabulários e Ontologias do Governo Eletrônico

[![Deploy MkDocs](https://github.com/destaquesgovbr/vocab-e-gov-br/actions/workflows/deploy.yml/badge.svg)](https://github.com/destaquesgovbr/vocab-e-gov-br/actions/workflows/deploy.yml)

**Espelho do antigo repositório vocab.e.gov.br**, recuperado do [Internet Archive (Wayback Machine)](https://web.archive.org/web/20191222064047/http://vocab.e.gov.br/).

## Acesse o site

**https://destaquesgovbr.github.io/vocab-e-gov-br/**

## Sobre

O **Repositório de Vocabulários e Ontologias do Governo Eletrônico** (e-VoG) foi uma iniciativa do Governo Federal brasileiro para padronização semântica de dados governamentais. O site original (vocab.e.gov.br) foi desativado há alguns anos.

Este projeto recupera e preserva o conteúdo histórico, modernizando a apresentação com MkDocs Material.

## Conteúdo Preservado

### Vocabulários

| Vocabulário | Descrição | Status |
|-------------|-----------|--------|
| **VCGE 2.0.3** | Vocabulário Controlado de Governo Eletrônico (versão estável) | Documentação |
| **VCGE 2011** | Versão de março de 2011 (1623 termos) | Completo + Explorador |
| **LOA** | Ontologia do Orçamento Federal | Documentação + OWL |
| **SIORG** | Estruturas Organizacionais | Documentação |
| **SIAFI** | Sistema Integrado de Administração Financeira | Documentação |
| **SICAF** | Sistema de Cadastramento de Fornecedores | Documentação |
| **OPS** | Ontologia de Participação Social | Documentação |
| **EDGV** | Especificação Técnica para Estruturação de Dados Geoespaciais | Documentação |

### Arquivos de Dados

- `vcge-2011-tree.json` - Estrutura hierárquica do VCGE para visualização
- `vcge-2011.json` - Dados completos do VCGE em JSON
- `vcge-2011.n3` - VCGE em RDF/Notation3 (SKOS)
- `vcge-2011.rdf` - VCGE em RDF/XML (SKOS)
- `loa.owl` - Ontologia LOA em OWL/XML

### Explorador Interativo

O site inclui um **explorador interativo do VCGE** com:

- Navegação em árvore hierárquica
- Busca e filtro em tempo real
- Visualização de URIs e relações (TG/TE)
- Interface moderna com Alpine.js

## Tecnologias

- [MkDocs](https://www.mkdocs.org/) com tema [Material](https://squidfunk.github.io/mkdocs-material/)
- [Alpine.js](https://alpinejs.dev/) para componentes interativos
- GitHub Actions para deploy automático
- GitHub Pages para hospedagem

## Desenvolvimento Local

```bash
# Instalar dependências
pip install -r requirements.txt

# Servir localmente
mkdocs serve

# Acessar em http://127.0.0.1:8000
```

## Estrutura do Projeto

```
vocab-e-gov-br/
├── docs/
│   ├── index.md                  # Homepage
│   ├── explorer.md               # Explorador VCGE principal
│   ├── downloads.md              # Página de downloads
│   ├── sobre.md                  # Sobre o projeto
│   ├── vocabularios/             # Documentação dos vocabulários
│   │   ├── vcge.md
│   │   ├── vcge-2.md
│   │   ├── vcge-explorer.md      # Explorador VCGE 2011
│   │   ├── loa.md
│   │   └── ...
│   ├── data/                     # Arquivos de dados
│   │   ├── vcge-2011-tree.json
│   │   ├── vcge-2011.json
│   │   ├── vcge-2011.n3
│   │   ├── vcge-2011.rdf
│   │   └── loa.owl
│   ├── javascripts/              # Scripts
│   │   └── vcge-tree.js          # Componente Alpine.js
│   └── stylesheets/              # Estilos
│       └── vcge-tree.css
├── scripts/                      # Scripts auxiliares
│   └── test_site.py              # Testes com Playwright
├── mkdocs.yml                    # Configuração MkDocs
├── requirements.txt              # Dependências Python
└── .github/workflows/            # GitHub Actions
    └── deploy.yml
```

## Licença

O conteúdo original do e-VoG foi produzido pelo Governo Federal e está em **domínio público**. As modernizações seguem a mesma política.

## Contribuições

Contribuições são bem-vindas! Abra uma [issue](https://github.com/destaquesgovbr/vocab-e-gov-br/issues) ou envie um pull request.

---

Mantido por [DestaquesGovBr](https://github.com/destaquesgovbr)
