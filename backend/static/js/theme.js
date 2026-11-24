// 라이트/다크 전환: <html data-theme>을 바꾸고 브라우저(localStorage)에 기억합니다.
// 바꾼 뒤 "themechange" 이벤트를 보내면 차트(analyses.js, dashboard.js)가 새 색으로 다시 그립니다.
(function () {
  const root = document.documentElement;
  const btn = document.getElementById("theme-toggle");
  if (!btn) return;

  function label() {
    const next = root.dataset.theme === "light" ? "다크" : "라이트";
    btn.setAttribute("aria-label", `${next} 모드로 전환`);
    btn.title = `${next} 모드로 전환`;
  }

  btn.addEventListener("click", () => {
    const theme = root.dataset.theme === "light" ? "dark" : "light";
    root.classList.add("theme-anim");
    root.dataset.theme = theme;
    try { localStorage.setItem("theme", theme); } catch (e) { /* 저장이 막힌 브라우저에서는 이번 화면에만 적용 */ }
    label();
    document.dispatchEvent(new CustomEvent("themechange", { detail: { theme } }));
    setTimeout(() => root.classList.remove("theme-anim"), 250);
  });
  label();
})();
