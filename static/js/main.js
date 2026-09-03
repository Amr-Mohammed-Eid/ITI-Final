// Warraq Digital Archives - Theme & Interactive Scripts
document.addEventListener('DOMContentLoaded', () => {
    let darkMode = localStorage.getItem('dark_mode');
    const themeSwitch = document.getElementById('theme_switch');

    const enableDarkMode = () => {
        document.body.classList.add('dark_mode');
        localStorage.setItem('dark_mode', 'active');
    };

    const disableDarkMode = () => {
        document.body.classList.remove('dark_mode');
        localStorage.setItem('dark_mode', null);
    };

    if (darkMode === 'active') {
        enableDarkMode();
    }

    if (themeSwitch) {
        themeSwitch.addEventListener('click', () => {
            darkMode = localStorage.getItem('dark_mode');
            if (darkMode !== 'active') {
                enableDarkMode();
            } else {
                disableDarkMode();
            }
        });
    }
});
