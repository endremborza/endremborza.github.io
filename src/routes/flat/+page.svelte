<script lang="ts">
  import data from '$lib/data/tree-data.json';

  const nodeMap = new Map(data.map(node => [node.id, node]));
  const root = data[0];

  type FlatNode = {
    node: typeof data[0];
    depth: number;
  }

  const flatNodes: FlatNode[] = [];
  const visited = new Set<string>();

  function traverse(nodeId: string, depth: number) {
    if (visited.has(nodeId)) {
      return;
    }
    visited.add(nodeId);

    const node = nodeMap.get(nodeId);
    if (!node) {
      return;
    }

    flatNodes.push({ node, depth });

    if (node.children) {
      for (const childId of node.children) {
        traverse(childId, depth + 1);
      }
    }
  }

  if (root) {
    traverse(root.id, 0);
  }

</script>

<svelte:head>
  <title>endremborza.github.io - Flat</title>
  <meta name="description" content="A flat, scrollable presentation of my work and interests." />
</svelte:head>

<div class="container">
  <h1>Flat View</h1>

  {#each flatNodes as { node, depth }}
    <div class="node" style="margin-left: {depth * 1.5}rem;">
      <h2>{node.title}</h2>
      <div>{@html node.body}</div>
    </div>
  {/each}
</div>

<style>
  .container {
    padding: 2rem;
    max-width: 800px;
    margin: 0 auto;
    font-family: sans-serif;
  }
  .node {
    margin-bottom: 2rem;
    border-left: 2px solid #eee;
    padding-left: 1.5rem;
  }
  h1, h2 {
      font-family: "Linux Libertine", "Georgia", "Times", "Source Serif Pro", serif;
  }
  h1 {
    border-bottom: 2px solid #eee;
    padding-bottom: 1rem;
    margin-bottom: 2rem;
  }
</style>
