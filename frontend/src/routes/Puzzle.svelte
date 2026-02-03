<script>
  import { onMount } from "svelte";
  export let params;

  let puzzle = null;
  let loading = true;

  onMount(async () => {
    const res = await fetch(`http://127.0.0.1:8000/puzzles/${params.id}`);
    puzzle = await res.json();
    loading = false;
  });
</script>

{#if loading}
  <p>Loading...</p>
{:else if puzzle.error}
  <p>{puzzle.error}</p>
{:else}
  <h1>{puzzle.title}</h1>
  <p>{puzzle.description}</p>

  <ul>
    {#each puzzle.words as word}
      <li>{word}</li>
    {/each}
  </ul>
{/if}
