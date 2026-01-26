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

	let n = 6;
	let fibs = getFibs(n);

	function handleClick(child: any) {
		console.log(child);
	}
	//top padding tile and left padding tile limited in size
	//padding is at least l-4, at most l-2
	//if parent is extra tall / wide ??? - at first just leave space at the end, at some point maybe repetition of component
	//make it reactive with scrolling, granular interaction only on tile 1, and possibly padding tile

	let pWidth: number;
	let pHeight: number;

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
			return { unit: width / smallD, isLandscape, padLoc: 'top', pSize };
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
		let top = 0;
		let left = 0;
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
		const nArr = getColorArr(i / (fibs.length - 1));
		return `rgb(${nArr.join(', ')})`;
	}

	export function getColorArr(rate: number) {
		const uRate = Math.abs(rate - 0.5) * 2;
		return [rate * 250, uRate * 220, 255 - rate * 250];
	}

	// the 'almost fitters' are a problem
	// stretch one way a little
	$: layout = getLayout(pWidth, pHeight, fibs);
	$: tiles = tilesFromLayout(layout, pWidth, pHeight, fibs);
</script>

<div class="container" bind:clientWidth={pWidth} bind:clientHeight={pHeight}>
	{#if pHeight != undefined && pWidth != undefined}
		{#each tiles as tile, i}
			<div
				class="abs"
				style="top: {tile.top}px;left: {tile.left}px;width: {tile.width}px; height:{tile.height}px;background-color:{getColor(
					i,
					layout,
					fibs
				)}"
			>
				<p>
					{i}
					{layout.isLandscape ? 'land' : 'port'}
					{layout.padLoc}
					{(layout.pSize / layout.unit).toFixed(1)}
					{(pWidth / layout.unit).toFixed(1)}
					{(pHeight / layout.unit).toFixed(1)}
				</p>
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

	.container {
		height: 100%;
		width: 100%;
		margin: 0px;
	}

	.abs {
		position: absolute;
	}
</style>
