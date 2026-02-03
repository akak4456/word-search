<script>
  import { onMount } from "svelte";
  export let params;

  let puzzle = null;
  let loading = true;
  let board = [];
  let mappedWord = [];
  let highlighted = null;

  const generateBoard = (words) => {
    const ROWS = 12;
    const COLS = 14;

    let board = Array.from({ length: ROWS }, () => Array(COLS).fill(""));

    const directions = [
      { dr: 0, dc: 1 }, // →
      { dr: 0, dc: -1 }, // ←
      { dr: 1, dc: 0 }, // ↓
      { dr: -1, dc: 0 }, // ↑
      { dr: 1, dc: 1 }, // ↘
      { dr: 1, dc: -1 }, // ↙
      { dr: -1, dc: 1 }, // ↗
      { dr: -1, dc: -1 }, // ↖
    ];

    for (let word of words) {
      word = word.toUpperCase();

      let placed = false;
      let attempts = 0;

      while (!placed && attempts < 100) {
        attempts++;

        const dir = directions[Math.floor(Math.random() * directions.length)];
        const row = Math.floor(Math.random() * ROWS);
        const col = Math.floor(Math.random() * COLS);

        let canPlace = true;

        for (let i = 0; i < word.length; i++) {
          const newRow = row + dir.dr * i;
          const newCol = col + dir.dc * i;

          // 1️⃣ 범위 체크
          if (newRow < 0 || newRow >= ROWS || newCol < 0 || newCol >= COLS) {
            canPlace = false;
            break;
          }

          // 2️⃣ 겹침 체크
          if (
            board[newRow][newCol] !== "" &&
            board[newRow][newCol] !== word[i]
          ) {
            canPlace = false;
            break;
          }
        }

        if (canPlace) {
          for (let i = 0; i < word.length; i++) {
            const newRow = row + dir.dr * i;
            const newCol = col + dir.dc * i;
            board[newRow][newCol] = word[i];
          }
          mappedWord.push({
            startRow: row,
            startCol: col,
            word: word,
            isSolved: false,
          });
          placed = true;
        }
      }

      if (!placed) {
        console.warn(`단어 배치 실패: ${word}`);
      }
    }

    // 빈칸 채우기
    const letters = "ABCDEFGHIJKLMNOPQRSTUVWXYZ";

    for (let r = 0; r < ROWS; r++) {
      for (let c = 0; c < COLS; c++) {
        if (board[r][c] === "") {
          board[r][c] = letters[Math.floor(Math.random() * letters.length)];
        }
      }
    }

    return board;
  };

  const gameSetup = () => {
    board = generateBoard(puzzle.words);
  };

  onMount(async () => {
    const res = await fetch(`http://127.0.0.1:8000/puzzles/${params.id}`);
    puzzle = await res.json();
    gameSetup();
    loading = false;
  });
</script>

{#if loading}
  <p>Loading...</p>
{:else if puzzle.error}
  <p>{puzzle.error}</p>
{:else}
  <div id="puzzle">
    <div id="pTitle">
      <h1>{puzzle.title}</h1>
    </div>
    <div id="pGame">
      <div id="pLeft">
        <div class="grid">
          {#each board as row, r}
            <div class="row">
              {#each row as cell, c}
                <div
                  class="cell"
                  class:highlight={highlighted &&
                    highlighted.row === r &&
                    highlighted.col === c}
                >
                  {cell}
                </div>
              {/each}
            </div>
          {/each}
        </div>
        <ul>
          {#each mappedWord as mw}
            <li
              on:click={() =>
                (highlighted = { row: mw.startRow, col: mw.startCol })}
            >
              {mw.word}
            </li>
          {/each}
        </ul>
      </div>
    </div>
  </div>

  <p>{puzzle.description}</p>
{/if}

<style>
  #puzzle {
    margin-top: 30px;
    margin-left: 60px;
    margin-right: 60px;
  }
  #pTitle h1 {
    color: var(--footer-background);
    font-size: 25px;
    font-weight: bold;
  }

  #pGame {
    margin-top: 18px;
  }

  #pLeft {
    display: flex;
  }

  #pLeft ul {
    margin-left: 8px;
    margin-top: 16px;
  }

  #pLeft li {
    margin-bottom: 8px;
    color: var(--footer-background);
    font-weight: bold;
  }

  .row {
    display: flex;
  }

  .cell {
    width: 50px;
    height: 50px;
    background-color: white;
    border: 1px solid var(--gray-color);
    font-size: 20px;
    display: flex;
    color: var(--footer-background);
    font-weight: bold;
    justify-content: center;
    align-items: center;
    font-weight: bold;
  }

  .highlight {
    background-color: var(--highlight-color);
    border: 4px solid var(--highlight-border);
  }
</style>
