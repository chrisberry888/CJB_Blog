(function () {
  const body = document.body;
  const root = document.documentElement;
  const drawer = document.querySelector("[data-drawer-open]") ? document.getElementById("site-drawer") : null;
  const overlay = document.querySelector("[data-drawer-overlay]");
  const openButton = document.querySelector("[data-drawer-open]");
  const closeButton = document.querySelector("[data-drawer-close]");
  const settingsToggle = document.querySelector("[data-settings-toggle]");
  const settingsPanel = document.querySelector("[data-settings-panel]");
  const backgroundInput = document.querySelector("[data-theme-background]");
  const textInput = document.querySelector("[data-theme-text]");
  const sizeInputs = Array.from(document.querySelectorAll("input[name='theme-size']"));
  const resetButton = document.querySelector("[data-theme-reset]");
  const storageKey = "cjb_blog_theme";

  const sizeToPixels = {
    small: "16px",
    medium: "18px",
    large: "20px",
  };

  function defaults() {
    return {
      background: body.dataset.defaultBackground || "#2B213A",
      text: body.dataset.defaultText || "#F6F0FF",
      size: body.dataset.defaultFontSize || "medium",
    };
  }

  function readStoredTheme() {
    try {
      return JSON.parse(localStorage.getItem(storageKey)) || {};
    } catch (_error) {
      return {};
    }
  }

  function saveTheme(theme) {
    localStorage.setItem(storageKey, JSON.stringify(theme));
  }

  function currentTheme() {
    return Object.assign(defaults(), readStoredTheme());
  }

  function applyTheme(theme) {
    const normalized = Object.assign(defaults(), theme);
    root.style.setProperty("--bg-color", normalized.background);
    root.style.setProperty("--text-color", normalized.text);
    root.style.setProperty("--font-size-base", sizeToPixels[normalized.size] || sizeToPixels.medium);

    if (backgroundInput) {
      backgroundInput.value = normalized.background;
    }
    if (textInput) {
      textInput.value = normalized.text;
    }
    sizeInputs.forEach((input) => {
      input.checked = input.value === normalized.size;
    });
  }

  function openDrawer() {
    if (!drawer || !overlay) {
      return;
    }
    overlay.hidden = false;
    drawer.setAttribute("aria-hidden", "false");
    body.classList.add("drawer-open");
    if (closeButton) {
      closeButton.focus();
    }
  }

  function closeDrawer() {
    if (!drawer || !overlay) {
      return;
    }
    body.classList.remove("drawer-open");
    drawer.setAttribute("aria-hidden", "true");
    overlay.hidden = true;
    if (openButton) {
      openButton.focus();
    }
  }

  applyTheme(currentTheme());

  if (openButton) {
    openButton.addEventListener("click", openDrawer);
  }
  if (closeButton) {
    closeButton.addEventListener("click", closeDrawer);
  }
  if (overlay) {
    overlay.addEventListener("click", closeDrawer);
  }

  document.addEventListener("keydown", (event) => {
    if (event.key === "Escape" && body.classList.contains("drawer-open")) {
      closeDrawer();
    }
  });

  if (settingsToggle && settingsPanel) {
    settingsToggle.addEventListener("click", () => {
      const isHidden = settingsPanel.hidden;
      settingsPanel.hidden = !isHidden;
      settingsToggle.setAttribute("aria-expanded", String(isHidden));
    });
  }

  if (backgroundInput) {
    backgroundInput.addEventListener("input", () => {
      const theme = currentTheme();
      theme.background = backgroundInput.value;
      saveTheme(theme);
      applyTheme(theme);
    });
  }

  if (textInput) {
    textInput.addEventListener("input", () => {
      const theme = currentTheme();
      theme.text = textInput.value;
      saveTheme(theme);
      applyTheme(theme);
    });
  }

  sizeInputs.forEach((input) => {
    input.addEventListener("change", () => {
      if (!input.checked) {
        return;
      }
      const theme = currentTheme();
      theme.size = input.value;
      saveTheme(theme);
      applyTheme(theme);
    });
  });

  if (resetButton) {
    resetButton.addEventListener("click", () => {
      localStorage.removeItem(storageKey);
      applyTheme(defaults());
    });
  }
})();

