<script>
  let title = "";
  let description = "";

  // 기본 30개 생성
  let words = Array(30).fill("");

  async function handleSubmit() {
    let isPossible = true;
    if (title === "") {
      const titleErr = document.querySelector("#title .fErr");
      titleErr.style.display = "block";
      isPossible = false;
    } else {
      const titleErr = document.querySelector("#title .fErr");
      titleErr.style.display = "none";
    }
    if (description === "") {
      const descErr = document.querySelector("#description .fErr");
      descErr.style.display = "block";
      isPossible = false;
    } else {
      const descErr = document.querySelector("#description .fErr");
      descErr.style.display = "none";
    }
    const filteredWords = words.map((w) => w.trim()).filter((w) => w !== "");
    if (filteredWords.length < 10) {
      const wordlistErr = document.querySelector("#wordlist .fErr");
      wordlistErr.style.display = "block";
      isPossible = false;
    } else {
      const wordlistErr = document.querySelector("#wordlist .fErr");
      wordlistErr.style.display = "none";
    }
    if (!isPossible) return;

    const response = await fetch("http://127.0.0.1:8000/puzzles", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        title,
        description,
        words: filteredWords,
      }),
    });

    const result = await response.json();
    console.log(result);
  }
</script>

<main>
  <p>
    Make your own word search game on any topic you like, simply by providing
    between 10 and 30 words. Once submitted, your puzzle will be instantly
    playable on-line as well as easily printed, so you can share it with
    friends. Instructions are available at the bottom of this page
  </p>
  <form on:submit|preventDefault={handleSubmit}>
    <div id="title">
      <label for="title">Title</label>
      <input type="text" id="title" bind:value={title} />
      <div class="fErr"><b>↪</b> Title is required</div>
    </div>
    <div id="description">
      <label for="description">Description</label>
      <textarea id="description" bind:value={description}></textarea>
      <div class="fErr"><b>↪</b> Description is required</div>
    </div>
    <div id="wordlist">
      <label for="word">Word List</label>
      <p class="word-list-p">
        Between 10 and 30 words. Puzzles are randomly generated using a
        selection of your words at play time.
      </p>
      <div id="wordlist-input">
        {#each words as word, index}
          <div class="word">
            <input type="text" bind:value={words[index]} />
          </div>
        {/each}
      </div>
      <div class="fErr"><b>↪</b> At least 10 words are required</div>
    </div>
    <button id="submit">Submit</button>
  </form>
</main>

<style>
  main {
    margin: 36px 60px 18px 60px;
  }
  p {
    color: var(--footer-background);
    text-align: center;
    padding-top: 12px;
    padding-bottom: 30px;
  }
  .word-list-p {
    text-align: left;
    padding-bottom: 5px;
  }
  main label {
    margin: 18px 0 4px;
    font-size: 1.2em;
    font-weight: 700;
    color: var(--footer-background);
  }
  main input,
  main textarea {
    box-sizing: border-box;
    color: var(--input-text-color);
    background: var(--white-text-color);
    border: 1px solid var(--gray-color);
    width: 100%;
    padding: 6px 8px;
    font-family: inherit;
    font-size: 1.2em;
    font-weight: 700;
    display: block;
    margin-top: 8px;
  }
  #description {
    margin-top: 18px;
  }
  #wordlist {
    margin-top: 18px;
  }
  #wordlist-input {
    display: flex;
    flex-wrap: wrap;
  }
  #wordlist .word {
    margin: 0;
  }
  #wordlist .word input {
    margin: 0;
  }
  @media (min-width: 520px) {
    #wordlist .word {
      width: 50%;
    }
  }
  @media (min-width: 800px) {
    #wordlist .word {
      width: 33.33%;
    }
  }
  @media (min-width: 1000px) {
    #wordlist .word {
      width: 25%;
    }
  }
  @media (min-width: 1250px) {
    #wordlist .word {
      width: 20%;
    }
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

  .fErr {
    color: var(--err-text-color);
    background: var(--err-background);
    padding: 0 4px;
    font-size: 0.8em;
    line-height: 2.4em;
    display: none;
  }
  .fErr b {
    color: var(--submit-background);
    padding: 0 6px;
  }
</style>
