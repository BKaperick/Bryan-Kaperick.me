const root = document.documentElement;
const toggle = document.getElementById("toggle");
const darkMode = localStorage.getItem("dark-mode") || (window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches);
if (darkMode) {
  root.classList.add("dark-theme");
}
toggle.addEventListener("click", () => {
  root.classList.toggle("dark-theme");
  if (root.classList.contains("dark-theme")) {
    localStorage.setItem("dark-mode", true);
  } else {
    localStorage.removeItem("dark-mode");
  }
});
