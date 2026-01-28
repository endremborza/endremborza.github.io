<script lang="ts">
	import FractalGrid from '$lib/components/FractalGrid.svelte';
	import fractalData from '$lib/data/fractal-data.json';
	import githubRepos from '$lib/data/github-repos.json';
	import type { TileContent, TileContents } from '$lib/util';

	let initTiles = [
		{ title: 'T1', body: '<span>Tile one</span>', id: 't0' },
		{ title: 'T2', body: '<span>Tile two with longer text</span>', id: 't1' },
		{ title: 'T3', body: '<span>Tile three</span>', id: 't2' },
		{ title: 'T4', body: '<span>Tile four</span>', id: 't3', children: ['t4', 't0'] },
		{ title: 'T5', body: '<span>Tile five</span>', id: 't4', children: ['t2', 't1', 't3'] }
	];

	let tileContents: TileContents = Object.fromEntries(initTiles.map((e) => [e.id, e]));
</script>

<svelte:head>
	<title>Endre Mark Borza</title>
</svelte:head>

<div>
	<FractalGrid {tileContents} />
</div>

<style>
	div {
		width: 100%;
		height: 100svh;
		margin: 0px;
	}
</style>
