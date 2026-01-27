<script lang="ts">
	import FractalGrid from '$lib/components/FractalGrid.svelte';
	import fractalData from '$lib/data/fractal-data.json';
	import githubRepos from '$lib/data/github-repos.json';
	import type { TileContent } from '$lib/util';

	let initTiles: TileContent[] = [
		{ title: 'T1', assignedTile: 0, body: '<span>Tile one</span>', id: 't0' },
		{ title: 'T2', assignedTile: 1, body: '<span>Tile two with longer text</span>', id: 't1' },
		{ title: 'T3', assignedTile: 2, body: '<span>Tile three</span>', id: 't2' },
		{ title: 'T4', assignedTile: 3, body: '<span>Tile four</span>', id: 't3' },
		{ title: 'T5', assignedTile: 4, body: '<span>Tile five</span>', id: 't4' }
	];

	let tilesContent = initTiles.slice(0, 4);
	function goHome() {
		// node = fractalData;
	}
</script>

<svelte:head>
	<title>Endre Mark Borza</title>
</svelte:head>

<div class="clickablex" on:click={goHome}>
	<FractalGrid bind:tilesContent />
</div>

<style>
	div {
		width: 100%;
		height: 100svh;
		margin: 0px;
	}
</style>
