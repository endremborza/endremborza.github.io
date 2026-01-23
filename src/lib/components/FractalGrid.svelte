<script lang="ts">
	type Node = {
		title: string;
		body: string;
		zoomedBody?: string;
		children?: Node[];
	};
	export let node: Node;

	function getFibs(n) {
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
	let fibs = getFibs();

	function handleClick(child: any) {
		console.log(child);
	}
	//top padding tile and left padding tile limited in size
	//padding is at least l-4, at most l-2
	//if parent is extra tall / wide ??? - at first just leave space at the end, at some point maybe repetition of component
	//make it reactive with scrolling, granular interaction only on tile 1, and possibly padding tile

	let pWidth: number;
	let pHeight: number;
</script>

<div class="container" bind:clientWidth={pWidth} bind:clientHeight={pHeight}>
	<div class="grid">
		<div class="grid-item item0"><p>body {pWidth} x {pHeight}</p></div>
		{#if node.children && node.children?.length > 0}
			{#each node.children as child, i}
				<div class="grid-item item{i + 1} clickable" on:click={() => handleClick(child)}>
					<p>{child.title}</p>
				</div>
			{/each}
		{/if}
		{#if node.children && node.children?.length < 4}
			<div class="grid-item item4 clickable">
				<p>4 nothing</p>
			</div>
		{/if}
	</div>
</div>

<style>
	p {
		margin: 1rem;
		font-size: 10px;
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
