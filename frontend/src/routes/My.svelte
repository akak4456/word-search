<script>
  import { onMount } from "svelte";
  let userId = "";

  onMount(() => {
    userId = localStorage.getItem("id") || "";
    console.log("userId", userId);
  });
  async function handleSubmit() {
    localStorage.setItem("id", "");
    localStorage.setItem("token", "");
    window.location.hash = "/";
  }
</script>

<main>
  {#if userId}
    <h1>{userId}</h1>
  {/if}
  <form on:submit|preventDefault={handleSubmit}>
    <button id="submit">Logout</button>
  </form>
</main>

<style>
  main {
    margin: 36px 60px 18px 60px;
    padding-bottom: 300px;
  }
  main h1 {
    color: var(--footer-background);
    font-size: 25px;
    font-weight: bold;
    margin-bottom: 18px;
  }

  #submit {
    color: var(--input-text-color);
    background-color: var(--submit-background);
    margin: 30px 0;
    width: 100%;
    padding: 18px;
    font-size: 1.4em;
    font-weight: 700;
  }
</style>
