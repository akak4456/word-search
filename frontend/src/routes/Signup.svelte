<script>
  let id = "";
  let password = "";
  let passwordCheck = "";

  let idError = false;
  let passwordError = false;
  let passwordCheckError = false;
  let passwordMatchError = false;
  async function handleSubmit() {
    // 🔄 매번 초기화
    idError = false;
    passwordError = false;
    passwordCheckError = false;
    passwordMatchError = false;

    let hasError = false;

    if (!id.trim()) {
      idError = true;
      hasError = true;
    }

    if (!password) {
      passwordError = true;
      hasError = true;
    }

    if (!passwordCheck) {
      passwordCheckError = true;
      hasError = true;
    }

    if (password && passwordCheck && password !== passwordCheck) {
      passwordMatchError = true;
      hasError = true;
    }

    if (hasError) return;

    // 3️⃣ 서버에 회원가입 요청
    try {
      const res = await fetch("http://localhost:8000/signup", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          id: id,
          password: password,
        }),
      });

      const data = await res.json();

      if (!res.ok) {
        alert(data.message);
        return;
      }

      alert("회원가입 성공!");
      window.location.hash = "#/login";
    } catch (err) {
      console.error(err);
      alert("서버 오류가 발생했습니다.");
    }
  }

  async function checkId() {
    const res = await fetch(`http://localhost:8000/users/check-id/${id}`);
    const data = await res.json();

    if (data.available) {
      alert("사용 가능한 아이디입니다.");
    } else {
      alert("이미 사용 중인 아이디입니다.");
    }
  }
</script>

<main>
  <h1>Sign Up</h1>
  <form on:submit|preventDefault={handleSubmit}>
    <div id="id">
      <label for="id">ID</label>
      <input type="text" id="id" bind:value={id} />
      <button id="id-check" on:click|preventDefault={checkId}>ID Check</button>
      {#if idError}
        <div class="fErr"><b>↪</b> ID is required</div>
      {/if}
    </div>
    <div id="password">
      <label for="password">Password</label>
      <input type="password" id="password" bind:value={password} />
      {#if passwordError}
        <div class="fErr"><b>↪</b> Password is required</div>
      {/if}
    </div>
    <div id="password-check">
      <label for="password-check">Password Check</label>
      <input type="password" id="password-check" bind:value={passwordCheck} />
      {#if passwordCheckError}
        <div class="fErr"><b>↪</b> Password Check is required</div>
      {/if}
      {#if passwordMatchError}
        <div class="fErr"><b>↪</b> Passwords do not match</div>
      {/if}
    </div>
    <button id="submit">Sign Up</button>
  </form>
</main>

<style>
  main {
    margin: 36px 60px 18px 60px;
    padding-bottom: 300px;
  }
  main h1 {
    color: var(--footer-background);
    font-size: 25px;
    font-weight: bold;
    margin-bottom: 18px;
  }
  main label {
    margin: 18px 0 4px;
    font-size: 1.2em;
    font-weight: 700;
    color: var(--footer-background);
  }
  main input {
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
  #password {
    margin-top: 18px;
  }

  #password-check {
    margin-top: 18px;
  }

  #submit,
  #id-check {
    color: var(--input-text-color);
    background-color: var(--submit-background);
    margin: 30px 0;
    width: 100%;
    padding: 18px;
    font-size: 1.4em;
    font-weight: 700;
  }
  #id-check {
    margin: 0;
  }

  .fErr {
    color: var(--err-text-color);
    background: var(--err-background);
    padding: 0 4px;
    font-size: 0.8em;
    line-height: 2.4em;
  }
  .fErr b {
    color: var(--submit-background);
    padding: 0 6px;
  }
</style>
