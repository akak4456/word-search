<script>
  let id = "";
  let password = "";
  async function handleSubmit() {
    const res = await fetch("http://localhost:8000/login", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        id,
        password,
      }),
    });

    if (res.status === 200) {
      const data = await res.json();

      localStorage.setItem("token", data.access_token);
      window.location.hash = "/";
    } else {
      alert("로그인에 실패했습니다.");
    }
  }
</script>

<main>
  <h1>Login</h1>
  <form on:submit|preventDefault={handleSubmit}>
    <div id="id">
      <label for="id">ID</label>
      <input type="text" id="id" bind:value={id} />
      <div class="fErr"><b>↪</b> ID is required</div>
    </div>
    <div id="password">
      <label for="password">Password</label>
      <input type="password" id="password" bind:value={password} />
      <div class="fErr"><b>↪</b> Password is required</div>
    </div>
    <button id="submit">Login</button>
    <button
      id="signup"
      on:click|preventDefault={(window.location.hash = "/signup")}
      >Sign Up</button
    >
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

  #submit,
  #signup {
    color: var(--input-text-color);
    background-color: var(--submit-background);
    margin: 30px 0;
    width: 100%;
    padding: 18px;
    font-size: 1.4em;
    font-weight: 700;
  }
  #signup {
    margin-top: 0;
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
