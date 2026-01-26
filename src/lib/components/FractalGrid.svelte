<script lang="ts">
	type Node = {
		title: string;
		body: string;
		zoomedBody?: string;
		children?: Node[];
	};
	export let node: Node;

	function getFibs(n: number) {
		const out = [1, 1];
		while (out.length < n) {
			let l = out.length;
			out.push(out[l - 1] + out[l - 2]);
		}
		return out;
	}

	const RATIO = (Math.sqrt(5) + 1) / 2;
	//1.61803398875

	let n = 5;
	let fibs = getFibs(n);
	let gap = 6;

	function handleClick(child: any) {
		console.log(child);
	}
	//top padding tile and left padding tile limited in size
	//padding is at least l-4, at most l-2
	//if parent is extra tall / wide ??? - at first just leave space at the end, at some point maybe repetition of component
	//make it reactive with scrolling, granular interaction only on tile 1, and possibly padding tile

	type Layout = {
		isLandscape: boolean;
		padLoc: 'top' | 'left' | 'none';
		unit: number;
		pSize: number;
	};
	type Tile = { top: number; left: number; height: number; width: number };

	function getLayout(width: number, height: number, fibs: number[]): Layout {
		let n = fibs.length;
		let smallD = fibs[n - 1];
		let sumD = smallD + fibs[n - 2];
		let upperPadLim = fibs[n - 2];
		let lowerPadLim = fibs[Math.max(0, n - 4)];
		let isLandscape = true;
		if (height <= width * ((smallD + upperPadLim) / sumD)) {
			if (height >= width * ((smallD + lowerPadLim) / sumD)) {
				let pSize = height - width * (smallD / sumD);
				return { unit: width / sumD, isLandscape, padLoc: 'top', pSize };
			}
			if (width >= height * ((sumD + lowerPadLim) / smallD)) {
				let pSize = width - height * (sumD / smallD);
				return { unit: height / smallD, isLandscape, padLoc: 'left', pSize };
			}
			let heightScaler = height / width / (smallD / sumD);
		}
		isLandscape = false;
		if (width <= (height * (lowerPadLim + smallD)) / sumD) {
			let pSize = height - width * (sumD / smallD);
			if (pSize > 0) return { unit: width / smallD, isLandscape, padLoc: 'top', pSize };
		}
		let pSize = width - height * (smallD / sumD);
		return { unit: height / sumD, isLandscape, padLoc: 'left', pSize }; //possibly wont fill it out?
	}

	type Direction = 'left' | 'right' | 'up' | 'down';

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
	function getColorR(i: number, layout: Layout, fibs: number[]) {
		let sumN = fibs.length - 1 + (layout.padLoc != 'none' ? 1 : 0);
		const nArr = getColorArr(i / sumN);
		return `rgb(${nArr.join(', ')})`;
	}

	export function getColorArr(rate: number): [number, number, number] {
		return [120 + Math.sin(rate * 2 * Math.PI) * 100, 80 + Math.cos(rate * 2 * Math.PI) * 100, 200];
	}

	export function getColor(rate: number): string {
		const hue = rate * 30 + 10; // avoid full wrap for smoother ends
		return `hsl(${hue}, 50%, 75%)`;
	}

	export function getColorMuted(rate: number): string {
		//muted
		const hue = 200 + rate * 80;
		const light = 40 + Math.sin(rate * Math.PI) * 20;
		return `hsl(${hue}, 30%, ${light}%)`;
	}

	// the 'almost fitters' are a problem
	// stretch one way a little
	let pWidth: number;
	let pHeight: number;
	$: innerWidth = pWidth - gap;
	$: innerHeight = pHeight - gap;

	$: layout = getLayout(innerWidth, innerHeight, fibs);
	$: tiles = tilesFromLayout(layout, innerWidth, innerHeight, fibs);
</script>

<div class="container" bind:clientWidth={pWidth} bind:clientHeight={pHeight} style="--gap: {gap}px">
	{#if pHeight != undefined && pWidth != undefined}
		{#each tiles as tile, i}
			<div
				class="abs"
				style="top: {tile.top}px;left: {tile.left}px;width: {tile.width}px; height:{tile.height}px;}"
			>
				<div class="tile" style="background-color:{getColor(i, layout, fibs)}">
					<span>
						{i}
						{#if i == 0}
							{layout.isLandscape ? 'land' : 'port'}
							{layout.padLoc}
							{(layout.pSize / layout.unit).toFixed(1)}
							{(pWidth / layout.unit).toFixed(1)}
							{(pHeight / layout.unit).toFixed(1)}
						{/if}
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
	}
</style>
