<script lang="ts">
	import {
		getColorByRate,
		getFibs,
		getLayout,
		styleFromTile,
		tilesFromLayout,
		type Layout,
		type ShownContent,
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
		shownContent = newShow;
	}
	//top padding tile and left padding tile limited in size
	//padding is at least l-4, at most l-2
	//if parent is extra tall / wide ??? - at first just leave space at the end, at some point maybe repetition of component
	//make it reactive with scrolling, granular interaction only on tile 1, and possibly padding tile

	function getColor(i: number, layout: Layout, fibs: number[]) {
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
		scArr.push({ title: tc.title, body: tc.body, assignedTile: scArr.length, id });
		for (const childId of tc.children || []) {
			if (scArr.length > n - 2) break;
			let tcc = tileContents[childId];
			if (tcc == undefined) {
				console.error('tc', id, 'children', tc.children, 'child', childId);
			}
			scArr.push({ title: tcc.title, body: tcc.body, assignedTile: scArr.length, id: childId });
		}
	}
	function fillRestShown(scArr: ShownContent[], n: number) {
		while (scArr.length <= n) {
			let i = scArr.length;
			scArr.push({ title: '', body: '', assignedTile: i, id: `_empty${i}` });
		}
	}

	function getExtraClass(tc: ShownContent) {
		if (tc.id.startsWith('_') || tc.assignedTile == 0) return '';
		return 'clickable';
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
		{#each shownContent as tc (tc.id)}
			<!-- svelte-ignore a11y-click-events-have-key-events -->
			<!-- svelte-ignore a11y-no-static-element-interactions -->
			<div
				class="abs"
				style={styleFromTile(tiles[tc.assignedTile])}
				on:click={() => handleClick(tc)}
				in:receive={{ key: tc.id }}
				out:send={{ key: tc.id }}
				animate:flip={{ duration: 200 }}
			>
				<div
					class="tile {getExtraClass(tc)}"
					style="--col:{getColor(tc.assignedTile, layout, fibs)}"
				>
					<h2>{tc.title}</h2>
					<span>
						{@html tc.body}
					</span>
				</div>
			</div>
		{/each}
	{/if}
</div>

<style>
	span {
		overflow: hidden;
	}

	.container {
		height: 100%;
		width: 100%;
		margin: 0px;
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
		justify-content: center;
		align-items: center;
		flex-direction: column;
		border-radius: calc(var(--gap) / 0.7);
		border: solid var(--col) calc(var(--gap) / 2);
		box-sizing: border-box;
	}
</style>
