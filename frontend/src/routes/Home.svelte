<script>
  import wordSearchPuzzle from "../assets/word-search-puzzle.png";
</script>

<main>
  <div id="top">
    <div id="puz-img">
      <img src={wordSearchPuzzle} alt="word-search-puzzle" />
      <p>Thousands ready to play online</p>
    </div>
    <div id="desc">
      <h1>Word Search</h1>
      <p>
        We have the best collection of word search puzzles online, with new ones
        being added regularly.
      </p>
      <p>
        They are fun to play, but also educational, in fact, many teachers make
        use of them.
      </p>
      <p>
        Puzzles are 100% free to play and work on desktop pc, mac, mobile and
        tablet. Or you can go old school and print them to enjoy offline later.
      </p>
      <p>
        Plus, if you're feeling a little more adventurous, why not create your
        very own with our simple to use Word Search Maker, and then share them
        with your friends.
      </p>
      <p>
        To get started playing, just select a game from below. Best of luck.
      </p>
    </div>
  </div>
  <div id="content">
    <h1>PUZZLES</h1>
    <ul>
      <li>word search 1</li>
      <li>word search 2</li>
      <li>word search 3</li>
      <li>word search 4</li>
    </ul>
  </div>
</main>

<style>
  #top {
    display: flex;
    margin-top: 18px;
    margin-left: 60px;
    margin-right: 60px;
  }
  #puz-img {
    text-align: center;
    color: var(--white-text-color);
    background: teal;
    margin: 0;
    padding: 6px;
  }
  #puz-img p {
    padding: 18px 0 18px 0;
  }

  #desc {
    width: 100%;
    height: auto;
    padding: 26px;
    color: var(--footer-background);
    background-color: var(--desc-background);
    border: 1px solid var(--desc-border-color);
  }
  #desc h1 {
    font-weight: bold;
    font-size: 30px;
    margin-top: 10px;
    margin-bottom: 20px;
  }
  #desc p {
    font-size: 18px;
    margin-bottom: 10px;
  }
  #desc p:nth-of-type(1) {
    font-weight: bold;
  }

  #content {
    background-color: var(--desc-background);
    border: 1px solid var(--desc-border-color);
    color: var(--footer-background);
    margin-top: 18px;
    margin-left: 60px;
    margin-right: 60px;
  }
  #content h1 {
    color: red;
    font-weight: bold;
    font-size: 30px;
    margin-top: 10px;
    margin-left: 3px;
    margin-bottom: 10px;
  }
  #content ul {
    padding-left: 30px;
    list-style: disc;
  }
  #content li {
    padding: 10px;
  }
</style>
