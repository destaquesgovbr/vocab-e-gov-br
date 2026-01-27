# Configuração DNS para vocab.e.gov.br

## Resumo

Configurar o subdomínio `vocab.e.gov.br` para apontar para o GitHub Pages da organização `destaquesgovbr`.

---

## Configuração Necessária

### Registro CNAME

| Campo | Valor |
|-------|-------|
| **Tipo** | CNAME |
| **Nome/Host** | `vocab` |
| **Valor/Target** | `destaquesgovbr.github.io` |
| **TTL** | 3600 (ou padrão) |

### Formato alternativo (alguns provedores DNS)

```
vocab.e.gov.br.  IN  CNAME  destaquesgovbr.github.io.
```

---

## Verificação

Após a configuração, verificar com o comando:

```bash
dig vocab.e.gov.br +nostats +nocomments +nocmd
```

**Resposta esperada:**

```
vocab.e.gov.br.     3600    IN    CNAME    destaquesgovbr.github.io.
destaquesgovbr.github.io.  3600  IN  A      185.199.108.153
destaquesgovbr.github.io.  3600  IN  A      185.199.109.153
destaquesgovbr.github.io.  3600  IN  A      185.199.110.153
destaquesgovbr.github.io.  3600  IN  A      185.199.111.153
```

---

## Informações Adicionais

- **Repositório:** https://github.com/destaquesgovbr/vocab-e-gov-br
- **GitHub Pages atual:** https://destaquesgovbr.github.io/vocab-e-gov-br/
- **Domínio final:** https://vocab.e.gov.br/

### Sobre HTTPS

O GitHub Pages fornece certificado SSL/TLS gratuito automaticamente após a configuração do DNS. O processo de emissão do certificado pode levar até 24 horas após a propagação do DNS.

---

## Contato

Em caso de dúvidas, entrar em contato com a equipe responsável pelo repositório.

---

## Referências

- [GitHub Docs - Managing a custom domain](https://docs.github.com/en/pages/configuring-a-custom-domain-for-your-github-pages-site/managing-a-custom-domain-for-your-github-pages-site)
- [GitHub Docs - Verifying your custom domain](https://docs.github.com/en/pages/configuring-a-custom-domain-for-your-github-pages-site/verifying-your-custom-domain-for-github-pages)
