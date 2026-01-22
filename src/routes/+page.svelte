<script lang="ts">
	import { onMount } from 'svelte';
	import convert from 'xml-js';

	let blocks: any[] = [];

	onMount(async () => {
		const response = await fetch('/data/index.xml');
		const xml = await response.text();
		const result = convert.xml2js(xml, { compact: true });
		blocks = result.root.blocks.block;
	});
</script>

<svelte:head>
	<title>Endre Borza</title>
</svelte:head>

<main>
	{#each blocks as block}
		<section>
			<h2>{block.title._text}</h2>
			<ul>
				{#each block.elem as elem}
					<li>
						{#if elem._attributes.type === 'emb-gh'}
							<a href="https://github.com/endremborza/{elem.title._text.toLowerCase().replace(/ /g, '-')}">
								{elem.title._text}
							</a>
						{:else}
							{elem.title._text}
						{/if}
					</li>
				{/each}
			</ul>
		</section>
	{/each}
</main>