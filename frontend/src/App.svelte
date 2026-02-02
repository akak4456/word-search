<script>
  import Header from "./components/Header.svelte";
  import Router from "svelte-spa-router";
  import Home from "./routes/Home.svelte";
  import Admin from "./routes/Admin.svelte";
  import Footer from "./components/Footer.svelte";
  const routes = {
    "/": Home,
    "/admin": Admin,
  };
</script>

<Header />
<Router {routes} />
<Footer />

<style>
</style>
