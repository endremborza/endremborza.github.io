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
	<title>endremborza</title>
</svelte:head>

<div class="container" style="--fancy-disp: none">
	{#each flatNodes as { node, depth }}
		<div class="node" style="margin-left: min({depth * 1.5}em, {depth * 3.2}vmin);">
			<h2>{node.title}</h2>
			<div>{@html node.body}</div>
		</div>
	{/each}
</div>

<style>
	.container {
		padding: 1.5em;
		max-width: 900px;
		margin: 0 auto;
		font-size: min(4vmin, 18px);
	}
	.node {
		margin-bottom: 2em;
		border-left: 1px solid var(--palette-1);
		padding-left: min(1.5em, 3vmin);
	}
</style>
