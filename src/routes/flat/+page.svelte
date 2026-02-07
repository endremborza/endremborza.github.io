<script lang="ts">
	import data from '$lib/data/tree-data.json';

	const nodeMap = new Map(data.map((node) => [node.id, node]));
	const root = data[0];

	type FlatNode = {
		node: (typeof data)[0];
		depth: number;
	};

	const minDepths = new Map<string, number>();

	function calculateMinDepths(nodeId: string, depth: number) {
		const currentMinDepth = minDepths.get(nodeId);
		if (currentMinDepth !== undefined && depth >= currentMinDepth) {
			return;
		}
		minDepths.set(nodeId, depth);

		const node = nodeMap.get(nodeId);
		if (node && node.children) {
			for (const childId of node.children) {
				calculateMinDepths(childId, depth + 1);
			}
		}
	}

	const flatNodes: FlatNode[] = [];
	const visited = new Set<string>();

	function buildFlatNodes(nodeId: string) {
		if (visited.has(nodeId)) {
			return;
		}
		visited.add(nodeId);

		const node = nodeMap.get(nodeId);
		if (!node) {
			return;
		}

		const depth = minDepths.get(nodeId) ?? 0;
		flatNodes.push({ node, depth });

		if (node.children) {
			for (const childId of node.children) {
				buildFlatNodes(childId);
			}
		}
	}

	if (root) {
		calculateMinDepths(root.id, 0);
		buildFlatNodes(root.id);
	}
</script>

<svelte:head>
	<title>Flat View</title>
</svelte:head>

<div class="container">
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
		max-width: 900px;
		margin: 0 auto;
		font-family: sans-serif;
	}
	.node {
		margin-bottom: 2rem;
		border-left: 1px solid var(--palette-1);
		padding-left: 1.5rem;
	}
</style>
