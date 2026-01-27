<script lang="ts">
	import { getColorByRate, getFibs, getLayout, type Layout, type TileContent } from '$lib/util';
	import { flip } from 'svelte/animate';
	import { quintOut } from 'svelte/easing';
	import { crossfade } from 'svelte/transition';

	type Tile = { top: number; left: number; height: number; width: number };
	type Direction = 'left' | 'right' | 'up' | 'down';

	export let tilesContent: TileContent[];
	export let n = 5;
	export let gap = 10;

	const RATIO = (Math.sqrt(5) + 1) / 2;
	//1.61803398875

	let fibs = getFibs(n);

	function handleClick(tc: TileContent) {
		let targetTile = 0;
		let sourceI, targetI;
		for (let i = 0; i < tilesContent.length; i++) {
			if (tilesContent[i].id == tc.id) {
				sourceI = i;
			}
			if (tilesContent[i].assignedTile == targetTile) {
				targetI = i;
			}
		}
		if (sourceI != undefined && targetI != undefined) {
			[tilesContent[sourceI].assignedTile, tilesContent[targetI].assignedTile] = [
				tilesContent[sourceI].assignedTile,
				tilesContent[sourceI].assignedTile
			];
		}
		tc.assignedTile = 0;
		console.log(tc);
	}
	//top padding tile and left padding tile limited in size
	//padding is at least l-4, at most l-2
	//if parent is extra tall / wide ??? - at first just leave space at the end, at some point maybe repetition of component
	//make it reactive with scrolling, granular interaction only on tile 1, and possibly padding tile

	function tilesFromLayout(
		layout: Layout,
		extWidth: number,
		extHeight: number,
		fibs: number[]
	): Tile[] {
		const out: Tile[] = [];
		if (extWidth == undefined) return out;
		let top = gap / 2;
		let left = gap / 2;
		let width = extWidth;
		let height = extHeight;
		function addTile(sizeW: number, sizeH: number, d: Direction) {
			let size = { width: sizeW, height: sizeH };
			if (d == 'right') {
				out.push({ top, left, ...size });
				left += sizeW;
				width -= sizeW;
				top += sizeH;
			} else if (d == 'down') {
				left -= sizeW;
				out.push({ top, left, ...size });
				top += sizeH;
				height -= sizeH;
			} else if (d == 'left') {
				top -= sizeH;
				left -= sizeW;
				out.push({ top, left, ...size });
				width -= sizeW;
			} else if (d == 'up') {
				top -= sizeH;
				out.push({ top, left, ...size });
				height -= sizeH;
				left += sizeW;
			}
		}
		let ps = layout.pSize;
		if (layout.padLoc == 'left') {
			out.push({ top, left, width: ps, height });
			left += ps;
			width -= ps;
		}
		if (layout.padLoc == 'top') {
			out.push({ top, left, width, height: ps });
			top += ps;
			height -= ps;
		}
		const DIRS: Direction[] = ['right', 'down', 'left', 'up'];
		let dirInd = 0;
		for (let i = 0; i < fibs.length; i++) {
			let fibU = fibs[fibs.length - 1 - i] * layout.unit;
			if (i == 0) {
				let size = { height: fibU, width: fibU };
				out.push({ top, left, ...size });
				left += fibU;
				if (layout.isLandscape) {
					width -= fibU;
				} else {
					top += fibU;
					height -= fibU;
				}
			} else {
				addTile(fibU, fibU, DIRS[dirInd]);
			}
			if (!layout.isLandscape || i > 0) {
				dirInd = (dirInd + 1) % DIRS.length;
			}
		}
		return out;
	}
	function getColor(i: number, layout: Layout, fibs: number[]) {
		let sumN = fibs.length - 1 + (layout.padLoc != 'none' ? 1 : 0);
		let rate = i / sumN;
		return getColorByRate(rate);
	}
	function styleFromTile(tile: Tile) {
		return `top: ${tile.top}px; left: ${tile.left}px; width: ${tile.width}px; height: ${tile.height}px;`;
	}
	export const [send, receive] = crossfade({
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

	// the 'almost fitters' are a problem
	// maybe stretch one way a little
	let pWidth: number;
	let pHeight: number;
	$: innerWidth = pWidth - gap;
	$: innerHeight = pHeight - gap;
	$: layout = getLayout(innerWidth, innerHeight, fibs);
	$: tiles = tilesFromLayout(layout, innerWidth, innerHeight, fibs);
</script>

<div class="container" bind:clientWidth={pWidth} bind:clientHeight={pHeight} style="--gap: {gap}px">
	{#if pHeight != undefined && pWidth != undefined}
		{#each tilesContent as tc (tc.id)}
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
				<div class="tile" style="--col:{getColor(tc.assignedTile, layout, fibs)}">
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
	p {
		margin: 1rem;
		font-size: 10px;
		overflow: hidden;
	}

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
