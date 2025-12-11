# Vocabulários e Ontologias do Governo Eletrônico

<div class="grid cards" markdown>

-   :material-brain:{ .lg .middle } **Para IA & LLMs**

    ---

    Vocabulários controlados em SKOS para enriquecer RAG, fine-tuning e knowledge graphs

-   :material-semantic-web:{ .lg .middle } **Linked Data**

    ---

    URIs persistentes e formatos RDF para interoperabilidade semântica

-   :material-download:{ .lg .middle } **Dados Abertos**

    ---

    JSON, RDF/N3, OWL - pronto para integração

-   :material-history:{ .lg .middle } **Preservação**

    ---

    Espelho do vocab.e.gov.br recuperado do Internet Archive

</div>

---

## Por que usar vocabulários controlados?

Na era dos **LLMs e sistemas de IA**, vocabulários controlados como o VCGE oferecem:

| Aplicação | Benefício |
|-----------|-----------|
| **RAG (Retrieval-Augmented Generation)** | Hierarquias semânticas melhoram a recuperação de documentos relacionados |
| **Fine-tuning** | Taxonomias estruturadas fornecem dados de treinamento de alta qualidade |
| **Knowledge Graphs** | URIs padronizadas permitem ligação entre bases de conhecimento |
| **Classificação automática** | Labels normalizados reduzem ambiguidade em modelos de classificação |
| **Busca semântica** | Relações TG/TE (Termo Geral/Específico) expandem queries automaticamente |

---

## Exploradores Interativos

<div class="grid cards" markdown>

-   :material-file-tree:{ .lg .middle } **VCGE 2.0.3**

    ---

    **116 termos** em 23 categorias

    Versão simplificada e atualizada

    [:octicons-search-24: Explorar VCGE 2.0.3](explorer.md)

-   :material-file-tree-outline:{ .lg .middle } **VCGE 2011**

    ---

    **1623 termos** hierárquicos

    Versão completa em SKOS

    [:octicons-search-24: Explorar VCGE 2011](vocabularios/vcge-explorer.md)

</div>

---

## Acesso Rápido aos Dados

### VCGE - Vocabulário Controlado de Governo Eletrônico

```python
# Python - Carregar VCGE para uso com LLMs
import requests

# VCGE 2.0.3 (116 termos, hierarquia simplificada)
vcge_203 = requests.get(
    "https://destaquesgovbr.github.io/vocab-e-gov-br/data/vcge-203-tree.json"
).json()

# VCGE 2011 (1623 termos, hierarquia completa)
vcge_2011 = requests.get(
    "https://destaquesgovbr.github.io/vocab-e-gov-br/data/vcge-2011-tree.json"
).json()

# Extrair labels para embeddings
def extract_labels(node, labels=[]):
    labels.append(node['label'])
    for child in node.get('children', []):
        extract_labels(child, labels)
    return labels

labels = extract_labels(vcge_2011)
print(f"Total de termos: {len(labels)}")
```

### Downloads Diretos

| Vocabulário | JSON | RDF/N3 | RDF/XML | OWL |
|-------------|------|--------|---------|-----|
| **VCGE 2.0.3** | [:material-download: vcge-203-tree.json](data/vcge-203-tree.json) | - | - | - |
| **VCGE 2011** | [:material-download: vcge-2011-tree.json](data/vcge-2011-tree.json) | [:material-download: vcge-2011.n3](data/vcge-2011.n3) | [:material-download: vcge-2011.rdf](data/vcge-2011.rdf) | - |
| **LOA** | - | - | - | [:material-download: loa.owl](data/loa.owl) |

---

## Vocabulários Disponíveis

### Vocabulários Estáveis

<div class="grid cards" markdown>

-   :material-check-circle:{ .lg .middle } **VCGE 2.0.3**

    ---

    Vocabulário Controlado de Governo Eletrônico - versão simplificada

    **116 termos** · **Namespace:** `http://vocab.e.gov.br/id/governo`

    [:octicons-arrow-right-24: Documentação](vocabularios/vcge-2.md) · [:octicons-search-24: Explorador](explorer.md)

-   :material-check-circle:{ .lg .middle } **VCGE 2011**

    ---

    Vocabulário Controlado de Governo Eletrônico - versão completa em SKOS

    **1623 termos** · **Namespace:** `http://vocab.e.gov.br/2011/03/vcge`

    [:octicons-arrow-right-24: Documentação](vocabularios/vcge.md) · [:octicons-search-24: Explorador](vocabularios/vcge-explorer.md)

-   :material-check-circle:{ .lg .middle } **LOA - Orçamento Federal**

    ---

    Ontologia da classificação da despesa do orçamento federal brasileiro

    **Formato:** OWL/XML

    [:octicons-arrow-right-24: Documentação](vocabularios/loa.md)

-   :material-check-circle:{ .lg .middle } **EDGV 2.1**

    ---

    Estruturação de Dados Geoespaciais Vetoriais

    **Autor:** CONCAR

    [:octicons-arrow-right-24: Documentação](vocabularios/edgv.md)

</div>

### Outros Vocabulários

| Vocabulário | Descrição | Status |
|-------------|-----------|--------|
| [SIORG](vocabularios/siorg.md) | Sistema de Órgãos - Estruturas Organizacionais | Documentação |
| [SIAFI](vocabularios/siafi.md) | Sistema Integrado de Administração Financeira | Documentação |
| [SICAF](vocabularios/sicaf.md) | Sistema de Cadastramento Unificado de Fornecedores | Documentação |
| [OPS](vocabularios/ops.md) | Ontologia de Participação Social | Documentação |

---

## Exemplo: Integração com LangChain

Este exemplo demonstra como usar o VCGE para criar um **índice vetorial de busca semântica** com LangChain e FAISS. O código:

1. Carrega a hierarquia completa do VCGE (1623 termos)
2. Transforma cada termo em um documento com metadados (URI, caminho hierárquico, nível)
3. Gera embeddings usando OpenAI e indexa no FAISS
4. Permite buscar termos semanticamente relacionados a uma query

Isso é útil para **expandir queries de usuários** com termos do vocabulário controlado, melhorando a precisão de sistemas RAG.

```python
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import FAISS
import requests

# Carregar VCGE
vcge = requests.get(
    "https://destaquesgovbr.github.io/vocab-e-gov-br/data/vcge-2011-tree.json"
).json()

# Criar documentos a partir da hierarquia
def create_docs(node, path=""):
    current_path = f"{path} > {node['label']}" if path else node['label']
    docs = [{
        "content": node['label'],
        "metadata": {
            "uri": node['uri'],
            "path": current_path,
            "level": len(current_path.split(" > "))
        }
    }]
    for child in node.get('children', []):
        docs.extend(create_docs(child, current_path))
    return docs

documents = create_docs(vcge)

# Criar índice vetorial para busca semântica
embeddings = OpenAIEmbeddings()
vectorstore = FAISS.from_texts(
    [d['content'] for d in documents],
    embeddings,
    metadatas=[d['metadata'] for d in documents]
)

# Buscar termos relacionados
results = vectorstore.similarity_search("agricultura sustentável", k=5)
for r in results:
    print(f"{r.page_content} - {r.metadata['uri']}")
```

---

## Sobre este Projeto

!!! info "Preservação Histórica"
    Este site é um espelho do antigo **vocab.e.gov.br**, recuperado do [Internet Archive](https://web.archive.org/web/20191222064047/http://vocab.e.gov.br/). O conteúdo foi modernizado com MkDocs Material e componentes Alpine.js, mas os dados originais foram preservados.

O **e-VoG** (Vocabulários e Ontologias do Governo Eletrônico) foi uma iniciativa do Governo Federal para padronização semântica de dados governamentais, visando:

- Intercâmbio de informações com acordo semântico
- Alinhamento conceitual entre áreas do governo
- Publicação de dados em formatos abertos e interoperáveis
- URIs persistentes para identificação de conceitos

[:octicons-mark-github-16: Código fonte](https://github.com/destaquesgovbr/vocab-e-gov-br) · [:octicons-info-16: Sobre o projeto](sobre.md)
