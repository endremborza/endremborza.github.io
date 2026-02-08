<script lang="ts">
	import FractalGrid from '$lib/components/FractalGrid.svelte';
	import treeData from '$lib/data/tree-data.json';
	import type { TileContents } from '$lib/util';
	let tileContents: TileContents = Object.fromEntries(treeData.map((e) => [e.id, e]));
</script>

<svelte:head>
	<title>endremborza</title>
</svelte:head>

<div>
	<FractalGrid {tileContents} rootId={'home'} />
</div>

<style>
	div {
		width: 100%;
		height: 100svh;
		margin: 0px;
	}
</style>
