<script>
  import { onMount } from "svelte";
  export let params;

  let puzzle = null;
  let loading = true;
  let board = [];
  let mappedWord = [];
  let highlighted = null;

  let selecting = false;
  let startPoint = null;
  let currentPoint = null;

  let solvedRects = [];

  const cellSize = 50; // 현재 cell 크기

  $: if (startPoint && currentPoint) {
    const dx = currentPoint.x - startPoint.x;
    const dy = currentPoint.y - startPoint.y;

    const distance = Math.sqrt(dx * dx + dy * dy);
    const angle = Math.atan2(dy, dx) * (180 / Math.PI);

    selectionRect = {
      left: startPoint.x,
      top: startPoint.y,
      width: distance,
      height: 30, // 🔴 고정 높이 (원하는 값)
      angle,
    };
  }

  let selectionRect = null;

  let startCell = null;
  let currentCell = null;
  let selectedCells = [];

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

    while (true) {
      let allPlaced = true;
      board = Array.from({ length: ROWS }, () => Array(COLS).fill(""));
      mappedWord = [];
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
          allPlaced = false;
        }
      }
      if (allPlaced) {
        break;
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

  function startSelection(e) {
    selecting = true;

    const rect = e.currentTarget.getBoundingClientRect();

    startPoint = {
      x: rect.left + rect.width / 2,
      y: rect.top + rect.height / 2,
    };

    currentPoint = { ...startPoint };
  }

  function handleMouseMove(e) {
    if (!selecting) return;

    currentPoint = {
      x: e.clientX,
      y: e.clientY,
    };

    const gridRect = e.currentTarget.getBoundingClientRect();

    const x = e.clientX - gridRect.left;
    const y = e.clientY - gridRect.top;

    const col = Math.floor(x / cellSize);
    const row = Math.floor(y / cellSize);

    if (row >= 0 && row < 12 && col >= 0 && col < 14) {
      if (startCell == null) {
        startCell = { row, col };
      }
      currentCell = { row, col };
      calculateSelection();
    }
  }

  function calculateSelection() {
    if (!startCell || !currentCell) return;

    const dr = currentCell.row - startCell.row;
    const dc = currentCell.col - startCell.col;

    const absDr = Math.abs(dr);
    const absDc = Math.abs(dc);

    // 🔥 8방향 조건
    const isStraight = dr === 0 || dc === 0 || absDr === absDc;

    if (!isStraight) {
      selectedCells = [];
      return;
    }

    const stepR = dr === 0 ? 0 : dr / absDr;
    const stepC = dc === 0 ? 0 : dc / absDc;

    const length = Math.max(absDr, absDc);

    let temp = [];

    for (let i = 0; i <= length; i++) {
      temp.push({
        row: startCell.row + stepR * i,
        col: startCell.col + stepC * i,
      });
    }

    selectedCells = temp;
    const selectedWord = selectedCells
      .map((cell) => board[cell.row][cell.col])
      .join("");
    if (checkWord(selectedWord)) {
      addSolvedRect();
      resetSelect();
    }
  }

  function resetSelect() {
    highlighted = null;
    startCell = null;
    currentCell = null;
    selecting = false;
  }

  function checkWord(word) {
    const reversed = word.split("").reverse().join("");

    const index = mappedWord.findIndex(
      (mw) => !mw.isSolved && (mw.word === word || mw.word === reversed),
    );

    if (index !== -1) {
      // 1️⃣ isSolved true
      mappedWord[index].isSolved = true;

      // 2️⃣ 맨 뒤로 이동
      const solvedItem = mappedWord.splice(index, 1)[0];
      mappedWord = [...mappedWord, solvedItem];

      // 🔥 Svelte 반응성 강제 업데이트
      mappedWord = [...mappedWord];
      return true;
    }
    return false;
  }

  function addSolvedRect() {
    if (!startCell || !currentCell) return;

    const grid = document.querySelector(".grid");
    const gridRect = grid.getBoundingClientRect();

    // 🔥 셀 중심 좌표 계산
    const startCenter = {
      x: gridRect.left + startCell.col * cellSize + cellSize / 2,
      y: gridRect.top + startCell.row * cellSize + cellSize / 2,
    };

    const endCenter = {
      x: gridRect.left + currentCell.col * cellSize + cellSize / 2,
      y: gridRect.top + currentCell.row * cellSize + cellSize / 2,
    };

    const dx = endCenter.x - startCenter.x;
    const dy = endCenter.y - startCenter.y;

    const distance = Math.sqrt(dx * dx + dy * dy);
    const angle = Math.atan2(dy, dx) * (180 / Math.PI);

    const rect = {
      left: startCenter.x,
      top: startCenter.y,
      width: distance,
      height: 30,
      angle,
    };

    solvedRects = [...solvedRects, rect];
  }

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
        <div
          class="grid-wrapper"
          on:mousemove={handleMouseMove}
          on:mouseup={() => {
            resetSelect();
          }}
        >
          <!-- 🔴 selection box -->
          {#if selecting && selectionRect}
            <div
              class="selection-box"
              style="
      left: {selectionRect.left}px;
      top: {selectionRect.top - selectionRect.height / 2}px;
      width: {selectionRect.width}px;
      height: {selectionRect.height}px;
      transform: rotate({selectionRect.angle}deg);
    "
            ></div>
          {/if}

          {#each solvedRects as rect}
            <div
              class="selection-box solved-box"
              style="
      left: {rect.left}px;
      top: {rect.top - rect.height / 2}px;
      width: {rect.width}px;
      height: {rect.height}px;
      transform: rotate({rect.angle}deg);
    "
            ></div>
          {/each}

          <!-- 🔵 실제 grid -->
          <div class="grid">
            {#each board as row, r}
              <div class="row">
                {#each row as cell, c}
                  <div
                    class="cell"
                    class:highlight={highlighted &&
                      highlighted.row === r &&
                      highlighted.col === c}
                    on:mousedown={(e) => startSelection(e)}
                  >
                    {cell}
                  </div>
                {/each}
              </div>
            {/each}
          </div>
        </div>
        <ul>
          {#each mappedWord as mw}
            <li
              class:solved={mw.isSolved}
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
    user-select: none;
  }

  .highlight {
    background-color: var(--highlight-color);
    border: 4px solid var(--highlight-border);
  }

  .grid-wrapper {
    position: relative;
  }

  .selection-box {
    position: fixed;
    transform-origin: 0 50%; /* 🔥 왼쪽 중앙 기준 회전 */
    border: 3px solid red;
    background-color: rgba(255, 0, 0, 0.2);
    pointer-events: none;
    z-index: 1000;
    border-radius: 20px;
  }

  .solved {
    text-decoration: line-through;
    opacity: 0.5;
  }

  .solved-box {
    border: 3px solid green;
    background-color: rgba(0, 200, 0, 0.25);
  }
</style>
