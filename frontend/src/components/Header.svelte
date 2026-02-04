<script>
  import wordSearchTitle from "../assets/word-search-title.png";
  import home from "../assets/home.svg";
  import my from "../assets/my.svg";
</script>

<header>
  <button class="logo-btn" on:click={(window.location.hash = "/")}>
    <img src={wordSearchTitle} alt="word-search-title" />
  </button>
  <nav>
    <button class="btn" on:click={(window.location.hash = "/my")}>
      <div class="btn__img">
        <img src={my} alt="my" />
      </div>
      <div class="btn__desc">My Page</div>
    </button>
    <button class="btn" on:click={(window.location.hash = "/")}>
      <div class="btn__img">
        <img src={home} alt="home" />
      </div>
      <div class="btn__desc">More Puzzles</div>
    </button>
  </nav>
</header>

<style>
  header {
    border-bottom: 4px solid teal;
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding-bottom: 18px;
    margin: 10px 60px 0 60px;
  }

  .logo-btn {
    cursor: pointer;
  }
  nav {
    display: flex;
    gap: 10px;
  }
  .btn {
    display: flex;
    justify-content: center;
    align-items: center;
    padding: 8px;
    cursor: pointer;
  }
  .btn:hover {
    background-color: var(--normal-text-color);
  }
  .btn__img img {
    width: 30px;
  }
  .btn__desc {
    color: var(--normal-text-color);
    margin-left: 8px;
    font-size: 18px;
  }
  .btn:hover .btn__desc {
    color: white;
  }
</style>
