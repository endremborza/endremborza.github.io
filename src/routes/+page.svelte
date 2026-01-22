<script lang="ts">
	import { onMount } from 'svelte';
	import convert from 'xml-js';
	import githubRepos from '$lib/data/github-repos.json'; // Import the generated JSON

	const RATIO = (Math.sqrt(5) + 1) / 2;

	let blocks: any[] = [];

	onMount(async () => {
		const response = await fetch('/data/index.xml');
		const xml = await response.text();
		const result = convert.xml2js(xml, { compact: true });
		blocks = result.root.blocks.block;
	});

	// Function to get GitHub repo details
	function getRepoDetails(repoName: string) {
		return githubRepos.find((repo) => repo.name.toLowerCase() === repoName.toLowerCase());
	}
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
							{@const repoDetails = getRepoDetails(elem.title._text.toLowerCase())}
							{#if repoDetails}
								<a href={repoDetails.html_url} target="_blank" rel="noopener noreferrer">
									{repoDetails.name} - {repoDetails.description} (⭐ {repoDetails.stargazers_count})
								</a>
							{:else}
								<a
									href="https://github.com/endremborza/{elem.title._text
										.toLowerCase()
										.replace(/ /g, '-')}"
									target="_blank"
									rel="noopener noreferrer"
								>
									{elem.title._text} (Repo details not found)
								</a>
							{/if}
						{:else}
							{elem.title._text}
						{/if}
					</li>
				{/each}
			</ul>
		</section>
	{/each}
</main>
