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

	let n = 7;
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

	type Layout = { isLandscape: boolean; padIsTop: boolean; unit: number; pSize: number };

	function getLayout(height: number, width: number, fibs: number[]): Layout {
		let n = fibs.length;
		let smallD = fibs[n - 1];
		let sumD = smallD + fibs[n - 2];
		let upperPadLim = fibs[n - 2];
		let lowerPadLim = fibs[Math.max(0, n - 4)];
		let isLandscape = true;
		console.log(lowerPadLim, upperPadLim);
		if (height <= width * ((smallD + upperPadLim) / sumD)) {
			if (height >= width * ((smallD + lowerPadLim) / sumD)) {
				let pSize = height - width * (smallD / sumD);
				return { unit: width / sumD, isLandscape, padIsTop: true, pSize };
			}
			if (width >= height * ((sumD + lowerPadLim) / smallD)) {
				let pSize = width - height * (sumD / smallD);
				return { unit: height / smallD, isLandscape, padIsTop: false, pSize };
			}
		}
		isLandscape = false;
		if (width <= (height * (lowerPadLim + smallD)) / sumD) {
			let pSize = height - width * (sumD / smallD);
			return { unit: width / smallD, isLandscape, padIsTop: true, pSize };
		}
		let pSize = width - height * (smallD / sumD);
		return { unit: height / sumD, isLandscape, padIsTop: false, pSize }; //possibly wont fill it out?
	}
	$: layout = getLayout(pHeight, pWidth, fibs);
</script>

<div class="container" bind:clientWidth={pWidth} bind:clientHeight={pHeight}>
	{#if pHeight != undefined && pWidth != undefined}
		<div class="pad abs {layout.padIsTop ? 'tpad' : 'lpad'}" style="--psize:{layout.pSize}px">
			<p>
				{layout.isLandscape ? 'land' : 'port'}
				{layout.padIsTop ? 'top' : 'left'}
				{(layout.pSize / layout.unit).toFixed(1)}
				{(pWidth / layout.unit).toFixed(1)}
				{(pHeight / layout.unit).toFixed(1)}
			</p>
		</div>
	{/if}
</div>

<style>
	p {
		margin: 1rem;
		font-size: 30px;
		overflow: hidden;
	}

	.container {
		height: 100%;
		width: 100%;
		margin: 0px;
	}

	.abs {
		position: absolute;
		border: 4px solid purple;
		box-sizing: border-box;
	}

	.pad {
		left: 0px;
		top: 0px;
		background-color: green;
	}
	.lpad {
		height: 100%;
		width: var(--psize);
	}
	.tpad {
		height: var(--psize);
		width: 100%;
	}

	.grid {
		display: grid;
		width: 100%;
		aspect-ratio: 34 / 21;
		gap: 8px;
		grid-template-columns: minmax(0, 21fr) minmax(0, 5fr) minmax(0, 8fr);
		grid-template-rows: minmax(0, 13fr) minmax(0, 3fr) minmax(0, 5fr);
	}

	.grid-item {
		border: 1px solid #ccc;
		padding: 0px;
		min-width: 0;
		min-height: 0;
		overflow: hidden;
		transition: all 0.2s ease-in-out;
	}

	.item0 {
		grid-row: 1 / span 3;
	}

	.item1 {
		/* grid-row: 1 / span 2; */
		grid-column: 2 / span 2;
	}

	.item2 {
		grid-column: 2 / span 1;
	}

	.item3 {
		grid-row: 3 / span 1;
	}
	.item4 {
		grid-column: 3 / span 1;
		grid-row: 2 / span 2;
	}
</style>
