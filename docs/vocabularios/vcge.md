# VCGE - Vocabulário Controlado do Governo Eletrônico (2011)

!!! note "Versão"
    Esta é a versão de **março de 2011** do VCGE. Para a versão mais recente, veja [VCGE 2.0.3](vcge-2.md).

## Descrição

O **VCGE** (Vocabulário Controlado do Governo Eletrônico) é um esquema para ser utilizado no elemento `assunto.categoria` (subject.category) do Padrão de Metadados do Governo Eletrônico (e-PMG).

Termos retirados do VCGE tornam mais direta, para os gerentes de sítios e portais governamentais, a apresentação dos serviços disponibilizados em uma estrutura de diretório baseada nos indexadores do VCGE.

O VCGE ajuda os cidadãos a encontrar informações mesmo sem o conhecimento de qual órgão o assunto é responsabilidade.

## Características

- **Poli-hierarquia**: Um termo pode ter um ou mais Termos Gerais (TG)
- **1623 termos** organizados hierarquicamente
- Baseado no padrão [SKOS](https://www.w3.org/2004/02/skos/)

## Namespace URI

```
http://vocab.e.gov.br/2011/03/vcge
```

## Autores

- [ePING](http://www.eping.e.gov.br/) - Padrões de Interoperabilidade de Governo Eletrônico

## Formatos Disponíveis

| Formato | Descrição | Download |
|---------|-----------|----------|
| JSON | JavaScript Object Notation | [vcge.json](../data/vcge-2011.json) |
| JSON Tree | Formato para visualização em árvore | [vcge-tree.json](../data/vcge-2011-tree.json) |
| RDF/N3 | SKOS em Notation 3 | [vcge.n3](../data/vcge-2011.n3) |
| RDF/XML | SKOS em XML | [vcge.rdf](../data/vcge-2011.rdf) |

## Explorador Interativo

Use o [Explorador VCGE](../explorer.md) para navegar pela árvore hierárquica com busca e filtro.

## Exemplo de Uso

### HTML 5 + RDFa 1.1

```html
<!DOCTYPE html>
<html>
<head>
  <title>Página sobre Agricultura</title>
  <link rel="http://purl.org/dc/terms/subject"
        href="http://vocab.e.gov.br/2011/03/vcge#agricultura-extrativismo-pesca" />
</head>
<body>
  ...
</body>
</html>
```

### RDF/Turtle

```turtle
@prefix dcterms: <http://purl.org/dc/terms/> .
@prefix vcge: <http://vocab.e.gov.br/2011/03/vcge#> .

<http://exemplo.gov.br/pagina>
    dcterms:subject vcge:agricultura-extrativismo-pesca .
```
