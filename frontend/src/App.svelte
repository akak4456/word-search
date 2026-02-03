<script>
  import Header from "./components/Header.svelte";
  import Router from "svelte-spa-router";
  import Home from "./routes/Home.svelte";
  import Admin from "./routes/Admin.svelte";
  import Footer from "./components/Footer.svelte";
  import Puzzle from "./routes/Puzzle.svelte";
  const routes = {
    "/": Home,
    "/admin": Admin,
    "/puzzle/:id": Puzzle,
  };
</script>

<Header />
<Router {routes} />
<Footer />

<style>
</style>
