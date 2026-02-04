<script>
  import Header from "./components/Header.svelte";
  import Router from "svelte-spa-router";
  import Home from "./routes/Home.svelte";
  import Admin from "./routes/Admin.svelte";
  import Footer from "./components/Footer.svelte";
  import Puzzle from "./routes/Puzzle.svelte";
  import My from "./routes/My.svelte";
  import { protectedRoute } from "./lib/protected";
  import Login from "./routes/Login.svelte";
  const routes = {
    "/": Home,
    "/login": Login,
    "/admin": Admin,
    "/my": protectedRoute(My),
    "/puzzle/:id": Puzzle,
  };
</script>

<Header />
<Router {routes} />
<Footer />

<style>
</style>
