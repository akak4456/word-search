<script>
  import wordSearchTitle from "../assets/word-search-title.png";
  import home from "../assets/home.svg";
</script>

<header>
  <button class="logo-btn" on:click={(window.location.hash = "/")}>
    <img src={wordSearchTitle} alt="word-search-title" />
  </button>
  <nav>
    <button class="home-btn" on:click={(window.location.hash = "/")}>
      <div class="home-btn__img">
        <img src={home} alt="home" />
      </div>
      <div class="home-btn__desc">More Puzzles</div>
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
  .home-btn {
    display: flex;
    justify-content: center;
    align-items: center;
    padding: 8px;
    cursor: pointer;
  }
  .home-btn:hover {
    background-color: #444;
  }
  .home-btn__img img {
    width: 30px;
  }
  .home-btn__desc {
    color: #444;
    margin-left: 8px;
    font-size: 18px;
  }
  .home-btn:hover .home-btn__desc {
    color: white;
  }
</style>
