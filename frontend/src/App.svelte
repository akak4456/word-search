<script>
  import Router from "svelte-spa-router";
  import Home from "./routes/Home.svelte";
  import Admin from "./routes/Admin.svelte";
  const routes = {
    "/": Home,
    "/admin": Admin,
  };
</script>

<Router {routes} />

<style>
</style>
