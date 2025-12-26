# Justificativa para Restauração e Manutenção do vocab.e.gov.br

## Sumário Executivo

O domínio **vocab.e.gov.br** hospedava o Repositório de Vocabulários e Ontologias do Governo Eletrônico (e-VoG), uma infraestrutura crítica para a Web Semântica governamental brasileira. O servidor foi desligado há anos, causando quebra de referências em sistemas que dependem de URIs persistentes.

**Este documento justifica a necessidade de restaurar e manter o domínio vocab.e.gov.br como infraestrutura permanente do Governo Federal.**

---

## 1. O Problema: URIs Persistentes e Linked Data

### 1.1 Por que URIs precisam ser persistentes?

Segundo as [Melhores Práticas do W3C para Publicação de Linked Data](https://www.w3.org/TR/ld-bp/):

> "Vocabulários DEVEM ter URLs persistentes - o acesso persistente ao servidor que hospeda o vocabulário é necessário para facilitar a reutilização."

Quando um sistema referencia uma ontologia ou vocabulário, ele usa a URI como identificador único e permanente. Se a URI deixa de funcionar:

- **Sistemas que validam metadados falham**
- **Documentos RDF/SKOS ficam com referências quebradas**
- **Portais de dados perdem capacidade de classificação semântica**
- **Motores de busca semântica não conseguem indexar corretamente**

### 1.2 O padrão Cool URIs

O documento [Cool URIs for the Semantic Web](https://www.w3.org/TR/cooluris/) do W3C estabelece:

> "Para ser 'persistente', uma URI deve ter um significado estável e bem documentado, e ser plausivelmente destinada a identificar um recurso em perpetuidade."

O vocab.e.gov.br seguia este padrão, com URIs como:
- `http://vocab.e.gov.br/2011/03/vcge#agricultura-extrativismo-pesca`
- `http://vocab.e.gov.br/id/governo#administracao`

---

## 2. O VCGE e sua Importância

### 2.1 O que é o VCGE?

O **Vocabulário Controlado do Governo Eletrônico (VCGE)** é o padrão oficial para classificação temática de conteúdos governamentais, definido pela [e-PING (Padrões de Interoperabilidade de Governo Eletrônico)](https://eping.governoeletronico.gov.br/).

Segundo a [documentação oficial](https://www.gov.br/governodigital/pt-br/governanca-de-dados/vocabulario-controlado-do-governo-eletronico):

> "O VCGE é um vocabulário controlado para indexar informações (documentos, bases de dados, sites etc) no governo federal, projetado como interface de comunicação com o cidadão e ferramenta de gestão."

### 2.2 Características técnicas

- **1623 termos** (versão 2011) organizados hierarquicamente
- **116 termos** (versão 2.0.3) em estrutura simplificada
- **Formato SKOS** (Simple Knowledge Organization System) - padrão W3C
- **Poli-hierarquia** - um termo pode ter múltiplos termos gerais

### 2.3 Evolução histórica

| Ano | Nome | Versão |
|-----|------|--------|
| 2004 | Lista de Categorias de Governo (LCG) | - |
| 2011 | Vocabulário Controlado do Governo Eletrônico | 1.0 |
| 2013 | VCGE | 2.0.2 |
| 2014 | VCGE | 2.0.3 |
| 2016 | VCGE | 2.1.0 |

---

## 3. Sistemas que Utilizam o VCGE

### 3.1 Portais Plone do Governo Federal

O pacote [brasil.gov.vcge](https://github.com/plonegovbr/brasil.gov.vcge) implementa o VCGE para portais Plone:

> "Este produto utiliza um arquivo SKOS, padrão W3C para representar vocabulários controlados. Os conteúdos classificados com este produto, e publicados na web, se juntam a outras iniciativas semelhantes e constituem um enorme repositório enriquecido com metadados."

O código gera tags RDFa que **referenciam diretamente as URIs do vocab.e.gov.br**:

```html
<link rel="http://purl.org/dc/terms/subject"
      href="http://vocab.e.gov.br/2011/03/vcge#agricultura-extrativismo-pesca" />
```

### 3.2 Portal Brasileiro de Dados Abertos (dados.gov.br)

O [Portal de Dados Abertos](https://dados.gov.br) utiliza CKAN com extensões específicas para o Brasil:

- [ckanext-dadosgovbr](https://github.com/dadosgovbr/ckanext-dadosgovbr) - Plugin do portal
- [ckanext-dadosgovbrschema](https://github.com/dadosgovbr/ckanext-dadosgovbrschema) - Schema de metadados

O VCGE é usado como vocabulário para classificação temática dos datasets.

### 3.3 Portais CKAN Estaduais e Municipais

Diversos portais de dados abertos utilizam CKAN e podem usar o VCGE:

| Portal | URL | Plataforma |
|--------|-----|------------|
| Tesouro Transparente | https://www.tesourotransparente.gov.br/ckan/ | CKAN |
| Dados Abertos RJ | https://dadosabertos.rj.gov.br/ | CKAN |
| Dados Abertos GO | https://dadosabertos.go.gov.br/ | CKAN |
| Dados Abertos MG | https://dados.mg.gov.br/ | CKAN |
| Dados SP (Município) | https://dados.prefeitura.sp.gov.br/ | CKAN |
| Dados PBH | https://ckan.pbh.gov.br/ | CKAN |
| Banco Central | https://dadosabertos.bcb.gov.br/ | CKAN |

### 3.4 Padrão de Metadados e-PMG

O VCGE é elemento obrigatório do [e-PMG (Padrão de Metadados do Governo Eletrônico)](https://www.gov.br/governodigital/pt-br/governanca-de-dados):

> "O VCGE é um esquema para ser utilizado no elemento `assunto.categoria` (subject.category) do Padrão de Metadados do Governo Eletrônico."

---

## 4. Impacto do Desligamento

### 4.1 Referências quebradas

Todos os documentos que contêm referências RDFa, RDF/XML ou JSON-LD para URIs do vocab.e.gov.br estão com links quebrados:

```turtle
# Exemplo de documento com referência quebrada
@prefix dcterms: <http://purl.org/dc/terms/> .
@prefix vcge: <http://vocab.e.gov.br/2011/03/vcge#> .  # ❌ INACESSÍVEL

<http://dados.gov.br/dataset/exemplo>
    dcterms:subject vcge:agricultura-extrativismo-pesca .  # ❌ Não resolve
```

### 4.2 Validação de metadados falha

Sistemas que validam metadados SKOS não conseguem resolver as URIs do vocabulário, gerando erros ou avisos.

### 4.3 Perda de interoperabilidade

A premissa fundamental de Linked Data - que dados de diferentes fontes podem ser interligados através de URIs comuns - é quebrada quando o vocabulário de referência não está disponível.

---

## 5. Proposta de Restauração

### 5.1 O que foi recuperado

O conteúdo foi recuperado do [Internet Archive (Wayback Machine)](https://web.archive.org/web/20191222064047/http://vocab.e.gov.br/) e está disponível temporariamente em:

**https://destaquesgovbr.github.io/vocab-e-gov-br/**

### 5.2 Arquivos preservados

| Arquivo | Formato | Descrição |
|---------|---------|-----------|
| vcge-2011-tree.json | JSON | Hierarquia VCGE 2011 (1623 termos) |
| vcge-203-tree.json | JSON | Hierarquia VCGE 2.0.3 (116 termos) |
| vcge-2011.json | JSON | Dados completos VCGE 2011 |
| vcge-2011.n3 | RDF/N3 | VCGE em SKOS/Notation3 |
| vcge-2011.rdf | RDF/XML | VCGE em SKOS/RDF-XML |
| loa.owl | OWL/XML | Ontologia do Orçamento Federal |

### 5.3 Configuração necessária

Para restaurar o domínio original, é necessário:

1. **Configurar DNS** de `vocab.e.gov.br` apontando para GitHub Pages
2. **Manter o repositório** github.com/destaquesgovbr/vocab-e-gov-br
3. **Garantir persistência** do conteúdo a longo prazo

---

## 6. Benefícios da Restauração

### 6.1 Imediatos

- Restauração de todas as referências RDFa em sites governamentais
- Validação de metadados volta a funcionar
- Portais de dados recuperam classificação temática

### 6.2 Estratégicos

- **Conformidade com e-PING**: Atende aos padrões de interoperabilidade
- **Web Semântica**: Habilita uso do VCGE em aplicações de IA e LLMs
- **Linked Data**: Permite interligação de dados governamentais
- **Transparência**: Metadados padronizados facilitam acesso à informação

### 6.3 Para IA e LLMs

Vocabulários controlados são fundamentais para:

- **RAG (Retrieval-Augmented Generation)**: Melhora recuperação de documentos
- **Fine-tuning**: Fornece dados de treinamento estruturados
- **Knowledge Graphs**: URIs padronizadas permitem construção de grafos
- **Classificação automática**: Reduz ambiguidade em modelos

---

## 7. Referências

### Documentos W3C

- [Best Practices for Publishing Linked Data](https://www.w3.org/TR/ld-bp/)
- [Cool URIs for the Semantic Web](https://www.w3.org/TR/cooluris/)
- [SKOS Simple Knowledge Organization System](https://www.w3.org/TR/skos-reference/)

### Governo Federal

- [Vocabulário Controlado do Governo Eletrônico - Gov.br](https://www.gov.br/governodigital/pt-br/governanca-de-dados/vocabulario-controlado-do-governo-eletronico)
- [e-PING - Padrões de Interoperabilidade](https://eping.governoeletronico.gov.br/)
- [Portal de Dados Abertos](https://dados.gov.br/)

### Implementações

- [brasil.gov.vcge - GitHub](https://github.com/plonegovbr/brasil.gov.vcge)
- [ckanext-dadosgovbr - GitHub](https://github.com/dadosgovbr/ckanext-dadosgovbr)

### Artigos Acadêmicos

- [O vocabulário controlado do Governo Eletrônico: contribuições e limites na implementação da LAI](https://seer.ufrgs.br/EmQuestao/article/view/70989)

---

## 8. Conclusão

A restauração do vocab.e.gov.br não é apenas uma questão de preservação histórica, mas uma **necessidade técnica** para:

1. Manter a integridade de sistemas que dependem de URIs persistentes
2. Cumprir os padrões de interoperabilidade (e-PING)
3. Habilitar aplicações modernas de IA e Web Semântica

**Recomendação**: Configurar o domínio vocab.e.gov.br como redirecionamento permanente para a infraestrutura GitHub Pages, garantindo persistência e baixo custo operacional.

---

*Documento elaborado em dezembro de 2024*
