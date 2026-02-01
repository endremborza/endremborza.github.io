<script lang="ts">
	import {
		getColorByRate,
		getFibs,
		getLayout,
		styleFromTile,
		tilesFromLayout,
		type Layout,
		type ShownContent,
		type Tile,
		type TileContent,
		type TileContents
	} from '$lib/util';
	import { flip } from 'svelte/animate';
	import { quintOut } from 'svelte/easing';
	import { crossfade } from 'svelte/transition';

	export let tileContents: TileContents;
	export let n = 5;
	export let gap = 10;

	// const RATIO = (Math.sqrt(5) + 1) / 2;
	//1.61803398875

	let fibs = getFibs(n);
	function handleClick(sc: ShownContent) {
		let tc = tileContents[sc.id];
		const newShow: ShownContent[] = [];
		fillWithTc(newShow, tc, sc.id);
		fillWithOld(newShow, shownContent);
		fillRestShown(newShow, n);
		shownContent = newShow;
	}
	//top padding tile and left padding tile limited in size
	//padding is at least l-4, at most l-2
	//if parent is extra tall / wide ??? - at first just leave space at the end, at some point maybe repetition of component
	//make it reactive with scrolling, granular interaction only on tile 1, and possibly padding tile

	function getColor(i: number, layout: Layout, fibs: number[]) {
		return `var(--palette-${i})`;
		let sumN = fibs.length - 1 + (layout.padLoc != 'none' ? 1 : 0);
		let rate = i / sumN;
		return getColorByRate(rate);
	}
	const [send, receive] = crossfade({
		duration: (d) => Math.sqrt(d * 200),

		fallback(node, params) {
			const style = getComputedStyle(node);
			const transform = style.transform === 'none' ? '' : style.transform;

			return {
				duration: 600,
				easing: quintOut,
				css: (t) => `
				transform: ${transform} scale(${t});
				opacity: ${t}
			`
			};
		}
	});
	function getShownContent(tcs: TileContents, n: number): ShownContent[] {
		const out: ShownContent[] = [];
		for (const [k, tc] of Object.entries(tcs)) {
			if (out.length > n - 2) break;
			fillWithTc(out, tc, k);
		}
		fillRestShown(out, n);
		return out;
	}

	function fillWithTc(scArr: ShownContent[], tc: TileContent, id: string) {
		scArr.push({ title: tc.title, body: tc.body, id });
		for (const childId of tc.children || []) {
			if (scArr.length > n - 2) break;
			let tcc = tileContents[childId];
			if (tcc == undefined) {
				console.error('tc', id, 'children', tc.children, 'child', childId);
			}
			scArr.push({ title: tcc.title, body: tcc.body, id: childId });
		}
	}
	function fillRestShown(scArr: ShownContent[], n: number) {
		while (scArr.length <= n) {
			let i = scArr.length;
			scArr.push({ title: '', body: '', id: `_empty${i}` });
		}
	}
	function fillWithOld(scArr: ShownContent[], oldArr: ShownContent[]) {
		let haveIds = scArr.map((e) => e.id);
		for (const oldSc of oldArr) {
			if (!haveIds.includes(oldSc.id)) {
				scArr.push(oldSc);
			}
			if (scArr.length > n - 2) break;
		}
	}

	function getExtraClass(i: number, tc: ShownContent) {
		if (tc.id.startsWith('_') || i == 0) return '';
		return 'clickable';
	}
	function getClamp(tile: Tile) {
		return Math.min(Math.floor((tile.height - 50) / 50), 10);
	}

	// the 'almost fitters' are a problem
	// maybe stretch one way a little
	let pWidth: number;
	let pHeight: number;
	$: innerWidth = pWidth - gap;
	$: innerHeight = pHeight - gap;
	$: layout = getLayout(innerWidth, innerHeight, fibs);
	$: tiles = tilesFromLayout(layout, innerWidth, innerHeight, fibs, gap);
	$: shownContent = getShownContent(tileContents, n);
</script>

<div class="container" bind:clientWidth={pWidth} bind:clientHeight={pHeight} style="--gap: {gap}px">
	{#if pHeight != undefined && pWidth != undefined}
		{#each shownContent.entries() as [i, tc] (tc.id)}
			<!-- svelte-ignore a11y-click-events-have-key-events -->
			<!-- svelte-ignore a11y-no-static-element-interactions -->
			<div
				class="abs {getExtraClass(i, tc)}"
				style={styleFromTile(tiles[i])}
				on:click={() => handleClick(tc)}
				in:receive={{ key: tc.id }}
				out:send={{ key: tc.id }}
				animate:flip={{ duration: 200 }}
			>
				<div
					class="tile"
					class:square={tiles[i].width === tiles[i].height}
					style="--col:{getColor(i, layout, fibs)}"
				>
					{#if !tc.id.startsWith('_')}
						<h2>{tc.title}</h2>
						<span style="--clamp: {getClamp(tiles[i])}">
							{@html tc.body}
						</span>
					{/if}
				</div>
			</div>
		{/each}
	{/if}
</div>

<style>
	.container {
		height: 100%;
		width: 100%;
		margin: 0;
	}

	.abs {
		position: absolute;
		display: flex;
		justify-content: center;
		align-items: center;
	}

	.tile {
		width: calc(100% - var(--gap));
		height: calc(100% - var(--gap));
		display: flex;
		flex-direction: column;
		justify-content: center;
		align-items: center;
		box-sizing: border-box;
		padding: 1.5rem;

		background-color: var(--tile-bg);
		border-radius: calc(var(--gap) / 0.7);
		border: solid var(--col) calc(var(--gap) / 2);
		box-shadow: 0 6px 12px rgba(255, 255, 255, 0.1);
		transition:
			transform 0.2s ease-in-out,
			box-shadow 0.2s ease-in-out,
			background-color 0.2s ease-in-out;
	}

	.clickable:hover .tile {
		transform: translateY(calc(var(--gap) / -2));
		box-shadow: 0 12px 24px rgba(255, 255, 255, 0.2);
	}

	.tile h2 {
		width: 100%;
		margin: 0 0 0.75rem 0;
		font-size: 2.1rem;
		text-align: center;
		border-bottom: 1px solid var(--col);
		padding-bottom: 0.5rem;
	}

	.tile span {
		width: 100%;
		font-size: 1.4rem;
		text-align: left;
		text-align: center;
		overflow: hidden;
		display: -webkit-box;
		line-clamp: var(--clamp);
		-webkit-box-orient: vertical;
		-webkit-line-clamp: var(--clamp); /* Limit to 10 lines */
	}
</style>
