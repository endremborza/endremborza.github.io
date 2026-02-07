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
	export let rootId: string;
	export let n = 5;
	export let gap = 8;

	// const RATIO = (Math.sqrt(5) + 1) / 2;
	//1.61803398875

	let fibs = getFibs(n);
	function handleClick(sc: ShownContent) {
		let tc = tileContents[sc.id];
		if (tc == undefined) return;
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

	function getColor(i: number, layout: Layout) {
		let palI = i % 3;
		return `var(--palette-${palI})`;
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
			let has = false;
			for (const o of out) {
				if (o.id == k) {
					has = true;
					break;
				}
			}
			if (!has) fillWithTc(out, tc, k);
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
		let hasRoot = false;
		for (const sc of scArr) {
			if (sc.id == rootId) {
				hasRoot = true;
				break;
			}
		}
		while (scArr.length <= n) {
			let i = scArr.length;
			if (!hasRoot && i == n) {
				scArr.push({ title: tileContents[rootId].title, body: '', id: rootId });
			} else {
				scArr.push({ title: '', body: '', id: `_empty${i}` });
			}
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

	function doesTitleFit(tile: Tile, tc: ShownContent) {
		if (tile.width < 100) return false;
		if (tile.height < 30) return false;
		let inSq = (tile.width - 48) * (tile.height - 48);
		return inSq / Math.pow(32, 2) > tc.title.length;
	}

	function getFontSize(tile: Tile, layout: Layout) {
		let sideMean = (tile.height * 4 + tile.width) / 5;
		let minFontSize = 7;
		let maxFontSize = 20;
		let fontSize = Math.min(Math.floor(Math.max(sideMean * 0.04, minFontSize)), maxFontSize);
		return { minFontSize, maxFontSize, fontSize };
	}

	function getTileStyleVars(i: number, layout: Layout, tiles: Tile[], fibs: number[]) {
		let tile = tiles[i];
		let { fontSize } = getFontSize(tile, layout);
		let clamp = i == 0 ? 100 : Math.min(Math.floor((tile.height - 50) / fontSize), 10);
		let vars = [`--col:${getColor(i, layout)}`, `--clamp: ${clamp}`, `font-size: ${fontSize}px`];

		return vars.join('; ');
	}

	function getTileClasses(i: number, tc: ShownContent, tiles: Tile[]) {
		if (tc.id.startsWith('_')) {
			return 'noheader nocontent';
		}
		let tile = tiles[i];
		let { fontSize, minFontSize } = getFontSize(tile, layout);
		if (!doesTitleFit(tile, tc)) return 'noheader nocontent';
		if (fontSize == minFontSize) {
			return 'headed nocontent';
		}
		return 'headed contented';
	}

	// the 'almost fitters' are a problem
	// maybe stretch one way a little or pad
	let transMs = 500;
	let pWidth: number;
	let pHeight: number;
	$: innerWidth = pWidth - gap;
	$: innerHeight = pHeight - gap;
	$: layout = getLayout(innerWidth, innerHeight, fibs);
	$: tiles = tilesFromLayout(layout, innerWidth, innerHeight, fibs, gap);
	$: shownContent = getShownContent(tileContents, n);
</script>

<div
	class="container"
	bind:clientWidth={pWidth}
	bind:clientHeight={pHeight}
	style="--gap: {gap}px; --trans: {transMs}ms"
>
	{#if pHeight != undefined && pWidth != undefined}
		{#each shownContent.slice(0, tiles.length).entries() as [i, tc] (tc.id)}
			<!-- svelte-ignore a11y-click-events-have-key-events -->
			<!-- svelte-ignore a11y-no-static-element-interactions -->
			<div
				class="abs {getExtraClass(i, tc)}"
				style={styleFromTile(tiles[i])}
				on:click={() => handleClick(tc)}
				in:receive={{ key: tc.id }}
				out:send={{ key: tc.id }}
				animate:flip={{ duration: transMs }}
			>
				<div
					class="tile {getTileClasses(i, tc, tiles)}"
					style={getTileStyleVars(i, layout, tiles, fibs)}
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

		background-color: var(--tile-bg);
		border: solid var(--col) calc(var(--gap) / 2);
		/* border-radius: calc(var(--gap) * 4); */
		box-shadow: 0 6px 12px rgba(255, 255, 255, 0.1);
		transition:
			transform var(--trans) ease-in-out,
			box-shadow var(--trans) ease-in-out,
			background-color var(--trans) ease-in-out;
	}

	.tile > h2,
	span {
		transition: var(--trans) all;
	}

	.noheader > h2 {
		display: none;
	}

	.nocontent > span {
		display: none;
	}

	.contented > h2 {
		margin: 0 0 0.75em 0;
		border-bottom: 0.08em solid var(--col);
		padding-bottom: 0.5em;
	}

	.headed {
		padding: min(2em, 1.5rem);
	}

	.clickable:hover .tile {
		transform: translateY(calc(var(--gap) / -2));
		box-shadow: 0 12px 24px rgba(255, 255, 255, 0.2);
	}

	.tile h2 {
		width: 100%;
		font-size: 1.8em;
		text-align: center;
	}

	.tile span {
		width: 100%;
		overflow: hidden;
		display: -webkit-box;
		line-clamp: var(--clamp);
		-webkit-box-orient: vertical;
		-webkit-line-clamp: var(--clamp);
	}
</style>
