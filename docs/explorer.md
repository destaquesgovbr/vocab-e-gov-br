# Explorador VCGE

<meta name="base-url" content="">

Navegue pela árvore hierárquica do **Vocabulário Controlado de Governo Eletrônico (VCGE)** com busca e filtro em tempo real.

<div x-data="vcgeTree()" x-init="init()" class="vcge-explorer">

  <!-- Painel da Árvore -->
  <div class="vcge-tree-panel">
    <div class="vcge-tree-header">
      <div class="vcge-search-box">
        <input
          type="text"
          x-model="search"
          @input.debounce.300ms="filterTree()"
          placeholder="Buscar termo..."
          class="vcge-search-input"
        >
        <button @click="clearSearch()" class="vcge-search-clear" x-show="search">✕</button>
      </div>
      <div class="vcge-toolbar">
        <button @click="expandAll()">Expandir todos</button>
        <button @click="collapseAll()">Colapsar todos</button>
        <span class="vcge-match-count" x-show="matchCount > 0" x-text="matchCount + ' resultados'"></span>
      </div>
    </div>

    <div class="vcge-tree-container">
      <!-- Loading -->
      <div x-show="loading" class="vcge-loading">
        Carregando vocabulário...
      </div>

      <!-- Erro -->
      <div x-show="error" class="vcge-error" x-text="error"></div>

      <!-- Árvore -->
      <template x-if="!loading && !error && filteredData">
        <div class="vcge-tree">
          <template x-for="node in (filteredData.children || [])" :key="node.id">
            <div class="vcge-tree-node" x-data="{ localExpanded: false }">
              <!-- Nó -->
              <div
                class="vcge-node-row"
                :class="{ 'selected': selectedNode?.id === node.id }"
                @click="selectNode(node)"
              >
                <span
                  class="vcge-node-toggle"
                  :class="{ 'has-children': node.children?.length }"
                  @click.stop="toggleNode(node.id)"
                  x-text="node.children?.length ? (isExpanded(node.id) ? '▼' : '▶') : '•'"
                ></span>
                <span
                  class="vcge-node-label"
                  :class="{ 'match': node.matches }"
                  x-text="node.label"
                ></span>
              </div>

              <!-- Filhos (primeiro nível) -->
              <template x-if="node.children?.length && isExpanded(node.id)">
                <div class="vcge-node-children">
                  <template x-for="child in node.children" :key="child.id">
                    <div class="vcge-tree-node">
                      <div
                        class="vcge-node-row"
                        :class="{ 'selected': selectedNode?.id === child.id }"
                        @click="selectNode(child)"
                      >
                        <span
                          class="vcge-node-toggle"
                          :class="{ 'has-children': child.children?.length }"
                          @click.stop="toggleNode(child.id)"
                          x-text="child.children?.length ? (isExpanded(child.id) ? '▼' : '▶') : '•'"
                        ></span>
                        <span
                          class="vcge-node-label"
                          :class="{ 'match': child.matches }"
                          x-text="child.label"
                        ></span>
                      </div>

                      <!-- Filhos (segundo nível) -->
                      <template x-if="child.children?.length && isExpanded(child.id)">
                        <div class="vcge-node-children">
                          <template x-for="grandchild in child.children" :key="grandchild.id">
                            <div class="vcge-tree-node">
                              <div
                                class="vcge-node-row"
                                :class="{ 'selected': selectedNode?.id === grandchild.id }"
                                @click="selectNode(grandchild)"
                              >
                                <span
                                  class="vcge-node-toggle"
                                  :class="{ 'has-children': grandchild.children?.length }"
                                  @click.stop="toggleNode(grandchild.id)"
                                  x-text="grandchild.children?.length ? (isExpanded(grandchild.id) ? '▼' : '▶') : '•'"
                                ></span>
                                <span
                                  class="vcge-node-label"
                                  :class="{ 'match': grandchild.matches }"
                                  x-text="grandchild.label"
                                ></span>
                              </div>

                              <!-- Filhos (terceiro nível) -->
                              <template x-if="grandchild.children?.length && isExpanded(grandchild.id)">
                                <div class="vcge-node-children">
                                  <template x-for="ggchild in grandchild.children" :key="ggchild.id">
                                    <div class="vcge-tree-node">
                                      <div
                                        class="vcge-node-row"
                                        :class="{ 'selected': selectedNode?.id === ggchild.id }"
                                        @click="selectNode(ggchild)"
                                      >
                                        <span
                                          class="vcge-node-toggle"
                                          :class="{ 'has-children': ggchild.children?.length }"
                                          @click.stop="toggleNode(ggchild.id)"
                                          x-text="ggchild.children?.length ? (isExpanded(ggchild.id) ? '▼' : '▶') : '•'"
                                        ></span>
                                        <span
                                          class="vcge-node-label"
                                          :class="{ 'match': ggchild.matches }"
                                          x-text="ggchild.label"
                                        ></span>
                                      </div>

                                      <!-- Filhos (quarto nível) -->
                                      <template x-if="ggchild.children?.length && isExpanded(ggchild.id)">
                                        <div class="vcge-node-children">
                                          <template x-for="gggchild in ggchild.children" :key="gggchild.id">
                                            <div class="vcge-tree-node">
                                              <div
                                                class="vcge-node-row"
                                                :class="{ 'selected': selectedNode?.id === gggchild.id }"
                                                @click="selectNode(gggchild)"
                                              >
                                                <span class="vcge-node-toggle" x-text="'•'"></span>
                                                <span
                                                  class="vcge-node-label"
                                                  :class="{ 'match': gggchild.matches }"
                                                  x-text="gggchild.label"
                                                ></span>
                                              </div>
                                            </div>
                                          </template>
                                        </div>
                                      </template>
                                    </div>
                                  </template>
                                </div>
                              </template>
                            </div>
                          </template>
                        </div>
                      </template>
                    </div>
                  </template>
                </div>
              </template>
            </div>
          </template>
        </div>
      </template>
    </div>
  </div>

  <!-- Painel de Detalhes -->
  <div class="vcge-details-panel">
    <div class="vcge-details-header">
      <h3 x-text="selectedNode ? selectedNode.label : 'Selecione um termo'"></h3>
    </div>
    <div class="vcge-details-content">
      <template x-if="selectedNode">
        <dl>
          <dt>URI</dt>
          <dd>
            <input
              type="text"
              class="vcge-uri-input"
              :value="selectedNode.uri"
              readonly
              @click="$el.select()"
            >
          </dd>

          <dt>Termo Geral (TG)</dt>
          <dd>
            <template x-if="findParent(selectedNode.id)">
              <span
                class="vcge-related-link"
                @click="selectNode(findParent(selectedNode.id))"
                x-text="findParent(selectedNode.id).label"
              ></span>
            </template>
            <template x-if="!findParent(selectedNode.id)">
              <span style="color: var(--md-default-fg-color--light)">Raiz</span>
            </template>
          </dd>

          <template x-if="selectedNode.children?.length">
            <div>
              <dt>Termos Específicos (TE)</dt>
              <dd>
                <ul class="vcge-related-list">
                  <template x-for="child in selectedNode.children" :key="child.id">
                    <li>
                      <span
                        class="vcge-related-link"
                        @click="selectNode(child); toggleNode(selectedNode.id)"
                        x-text="child.label"
                      ></span>
                    </li>
                  </template>
                </ul>
              </dd>
            </div>
          </template>
        </dl>
      </template>

      <template x-if="!selectedNode">
        <div class="vcge-placeholder">
          Clique em um termo na árvore para ver seus detalhes
        </div>
      </template>
    </div>
  </div>

</div>

---

## Sobre o VCGE

O **VCGE** (Vocabulário Controlado do Governo Eletrônico) é um esquema para ser utilizado no elemento `assunto.categoria` (subject.category) do Padrão de Metadados do Governo Eletrônico (e-PMG).

Termos retirados do VCGE tornam mais direta, para os gerentes de sítios e portais governamentais, a apresentação dos serviços disponibilizados em uma estrutura de diretório baseada nos indexadores do VCGE.

O VCGE ajuda os cidadãos a encontrar informações mesmo sem o conhecimento de qual órgão o assunto é responsabilidade.

### Formatos disponíveis

| Formato | Descrição | Download |
|---------|-----------|----------|
| JSON | JavaScript Object Notation | [vcge-2011.json](data/vcge-2011-tree.json) |
| RDF/N3 | Notation 3 | [vcge.n3](data/vcge-2011.n3) |
| RDF/XML | XML serialization | [vcge.rdf](data/vcge-2011.rdf) |
