// Dark Mode
// https://developer.mozilla.org/en-US/docs/Web/API/CustomEvent/CustomEvent
(() => {
    const switch_btn = document.querySelector(".dark-mode-switcher");
    const storedTheme = localStorage.getItem("theme");
    const getPreferredTheme = () => {
        if (storedTheme) {
            return storedTheme;
        }
        return window.matchMedia("(prefers-color-scheme: dark)").matches ? "dark" : "light";
    };
    const setTheme = (theme) => {
        if (theme === "auto" && window.matchMedia("(prefers-color-scheme: dark)").matches || theme == "dark") {
            document.documentElement.setAttribute("data-bs-theme", "dark");
            switch_btn.classList.add("active");
        } else {
            document.documentElement.setAttribute("data-bs-theme", "light");
            switch_btn.classList.remove("active");
        }
    };

    window.addEventListener("dark_mode", (e) => {
        if (e.detail.active == 1) {
            localStorage.setItem("theme", "dark");
            setTheme("dark");
        } else {
            localStorage.setItem("theme", "");
            setTheme("light");
        }
    });

    window.addEventListener("DOMContentLoaded", () => {
        document.querySelectorAll("[data-bs-theme-value]")
            .forEach(toggle => {
                toggle.addEventListener("click", (event) => {
                    event.stopPropagation();
                    const activate = (bs_theme == "light" || bs_theme == "" || bs_theme === null) ? 1 : 0;
                    window.dispatchEvent(new CustomEvent("dark_mode", {
                        detail: {
                            active: activate
                        }
                    }));
                });
            });
    });

    switch_btn.addEventListener("click", () => {
        const bs_theme = document.documentElement.getAttribute("data-bs-theme");
        const activate = (bs_theme == "light" || bs_theme == "" || bs_theme === null) ? 1 : 0;
        window.dispatchEvent(new CustomEvent("dark_mode", {
            detail: {
                active: activate
            }
        }));
    });

    setTheme(getPreferredTheme());

})();