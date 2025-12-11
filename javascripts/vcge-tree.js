/**
 * Componente Alpine.js para navegação em árvore do VCGE
 * Substitui o antigo jstree por uma implementação moderna e leve
 */

document.addEventListener('alpine:init', () => {
  Alpine.data('vcgeTree', () => ({
    // Estado
    treeData: null,
    filteredData: null,
    search: '',
    selectedNode: null,
    matchCount: 0,
    loading: true,
    error: null,
    expandedNodes: new Set(),

    // Inicialização
    async init() {
      await this.loadData();

      // Verificar hash na URL para selecionar nó inicial
      if (window.location.hash) {
        const nodeId = window.location.hash.substring(1);
        this.$nextTick(() => this.selectNodeById(nodeId));
      }

      // Escutar mudanças no hash
      window.addEventListener('hashchange', () => {
        const nodeId = window.location.hash.substring(1);
        if (nodeId) this.selectNodeById(nodeId);
      });
    },

    // Carregar dados JSON
    async loadData() {
      try {
        this.loading = true;
        const basePath = document.querySelector('meta[name="base-url"]')?.content || '';
        const dataFile = document.querySelector('meta[name="vcge-data"]')?.content || 'vcge-2011-tree.json';
        const response = await fetch(`${basePath}data/${dataFile}`);
        if (!response.ok) throw new Error('Falha ao carregar dados');
        this.treeData = await response.json();
        this.filteredData = this.treeData;
        this.loading = false;
      } catch (e) {
        this.error = e.message;
        this.loading = false;
        console.error('Erro ao carregar VCGE:', e);
      }
    },

    // Filtrar árvore
    filterTree() {
      if (!this.search || this.search.length < 2) {
        this.filteredData = this.treeData;
        this.matchCount = 0;
        this.expandedNodes.clear();
        return;
      }

      const term = this.search.toLowerCase().normalize('NFD').replace(/[\u0300-\u036f]/g, '');
      this.matchCount = 0;
      this.expandedNodes.clear();

      const filterNode = (node, parentPath = []) => {
        const normalizedLabel = (node.label || '').toLowerCase().normalize('NFD').replace(/[\u0300-\u036f]/g, '');
        const matches = normalizedLabel.includes(term);

        let filteredChildren = [];
        if (node.children) {
          filteredChildren = node.children
            .map(child => filterNode(child, [...parentPath, node.id]))
            .filter(Boolean);
        }

        if (matches || filteredChildren.length > 0) {
          if (matches) this.matchCount++;

          // Expandir todos os ancestrais se houver match
          if (matches || filteredChildren.length > 0) {
            parentPath.forEach(id => this.expandedNodes.add(id));
            if (filteredChildren.length > 0) {
              this.expandedNodes.add(node.id);
            }
          }

          return {
            ...node,
            matches,
            children: filteredChildren.length > 0 ? filteredChildren : node.children
          };
        }
        return null;
      };

      const result = filterNode(this.treeData);
      this.filteredData = result || this.treeData;
    },

    // Selecionar nó
    selectNode(node) {
      this.selectedNode = node;
      if (node.id) {
        history.pushState(null, '', `#${node.id}`);
      }
    },

    // Selecionar nó por ID
    selectNodeById(nodeId) {
      const findNode = (node, path = []) => {
        if (node.id === nodeId) {
          // Expandir caminho até o nó
          path.forEach(id => this.expandedNodes.add(id));
          return node;
        }
        if (node.children) {
          for (const child of node.children) {
            const found = findNode(child, [...path, node.id]);
            if (found) return found;
          }
        }
        return null;
      };

      const node = findNode(this.treeData);
      if (node) {
        this.selectedNode = node;
      }
    },

    // Toggle expansão de nó
    toggleNode(nodeId) {
      if (this.expandedNodes.has(nodeId)) {
        this.expandedNodes.delete(nodeId);
      } else {
        this.expandedNodes.add(nodeId);
      }
      // Forçar reatividade
      this.expandedNodes = new Set(this.expandedNodes);
    },

    // Verificar se nó está expandido
    isExpanded(nodeId) {
      return this.expandedNodes.has(nodeId);
    },

    // Encontrar nó pai
    findParent(targetId, node = this.treeData, parent = null) {
      if (node.id === targetId) return parent;
      if (node.children) {
        for (const child of node.children) {
          const found = this.findParent(targetId, child, node);
          if (found) return found;
        }
      }
      return null;
    },

    // Expandir todos
    expandAll() {
      const addAllIds = (node) => {
        if (node.children && node.children.length > 0) {
          this.expandedNodes.add(node.id);
          node.children.forEach(addAllIds);
        }
      };
      addAllIds(this.treeData);
      this.expandedNodes = new Set(this.expandedNodes);
    },

    // Colapsar todos
    collapseAll() {
      this.expandedNodes.clear();
      this.expandedNodes = new Set();
    },

    // Limpar busca
    clearSearch() {
      this.search = '';
      this.filterTree();
    }
  }));
});
