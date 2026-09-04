// Warraq Digital Archives - Client-Side Catalog Search & Filtering (FR-2, FR-5)
document.addEventListener('DOMContentLoaded', () => {
    const searchInput = document.getElementById('catalog-search-input') || document.querySelector('.search-input-wrapper input');
    if (!searchInput) return;

    const searchBtn = document.getElementById('catalog-search-btn') || document.querySelector('.search-input-wrapper button');
    const bookCards = document.querySelectorAll('.books-grid .book-card');
    const booksGrid = document.querySelector('.books-grid');
    const popularTags = document.querySelectorAll('.popular-tags a');

    function filterBooks() {
        const query = searchInput.value.trim().toLowerCase();
        let visibleCount = 0;

        bookCards.forEach((card) => {
            const titleEl = card.querySelector('.book-title');
            const authorEl = card.querySelector('.book-author');
            const title = titleEl ? titleEl.textContent.toLowerCase() : '';
            const author = authorEl ? authorEl.textContent.toLowerCase() : '';

            // Match query in either title or author
            if (!query || title.includes(query) || author.includes(query)) {
                card.style.display = '';
                visibleCount++;
            } else {
                card.style.display = 'none';
            }
        });

        // Toggle 'no search results' feedback
        let noResultsMsg = document.getElementById('js-no-search-results');
        if (visibleCount === 0 && bookCards.length > 0) {
            if (!noResultsMsg) {
                noResultsMsg = document.createElement('div');
                noResultsMsg.id = 'js-no-search-results';
                noResultsMsg.className = 'empty-state';
                noResultsMsg.innerHTML = '<h3>No matching books found</h3><p>Try searching for a different title or author.</p>';
                if (booksGrid) {
                    booksGrid.appendChild(noResultsMsg);
                }
            }
            noResultsMsg.style.display = '';
        } else if (noResultsMsg) {
            noResultsMsg.style.display = 'none';
        }
    }

    // Filter in real-time as user types (client-side only, no server round-trip)
    searchInput.addEventListener('input', filterBooks);

    if (searchBtn) {
        searchBtn.addEventListener('click', (e) => {
            e.preventDefault();
            filterBooks();
        });
    }

    searchInput.addEventListener('keydown', (e) => {
        if (e.key === 'Enter') {
            e.preventDefault();
            filterBooks();
        }
    });

    // Quick-filter via popular tags
    popularTags.forEach((tag) => {
        tag.addEventListener('click', (e) => {
            e.preventDefault();
            searchInput.value = tag.textContent.trim();
            filterBooks();
            searchInput.focus();
        });
    });
});
