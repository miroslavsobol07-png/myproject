const button = document.querySelector('#load');
const filter = document.querySelector('#available');
const form = document.querySelector('#filters');
const genre = document.querySelector('#genre');
const minRating = document.querySelector('#min-rating');
const sort = document.querySelector('#sort');
const jsonLink = document.querySelector('#json-link');
const books = document.querySelector('#books');
const status = document.querySelector('#status');

// wstawiamy tekst bez interpretowania HTML
function addText(parent, tag, text, className = '') {
    const element = document.createElement(tag);
    element.textContent = text;
    element.className = className;
    parent.appendChild(element);
}

async function loadBooks() {
    const params = new URLSearchParams({
        available: filter.value, genre: genre.value,
        min_rating: minRating.value, sort: sort.value,
    });
    const url = `${button.dataset.url}?${params}`;
    for (const control of form.elements) control.disabled = true;
    books.setAttribute('aria-busy', 'true');
    books.replaceChildren();
    status.className = '';
    status.textContent = 'Ładowanie książek…';

    try {
        // pobieramy przefiltrowane książki
        const response = await fetch(url);
        if (!response.ok) {
            throw new Error('Błąd HTTP: ' + response.status);
        }
        const data = await response.json();
        if (!Array.isArray(data.items)) {
            throw new Error('Niepoprawna struktura JSON');
        }

        for (const book of data.items) {
            const card = document.createElement('article');
            card.className = 'book';
            addText(card, 'h3', book.title);
            addText(card, 'p', book.author);
            addText(card, 'p', `${book.genre}, ${book.year}`, 'meta');
            addText(card, 'p', book.available ? 'Dostępna' : 'Wypożyczona',
                book.available ? 'availability' : 'availability unavailable');
            addText(card, 'p', book.rating === null ? 'Jeszcze bez oceny' : `Ocena: ${book.rating} / 5`, 'rating');
            const date = book.added_on ? book.added_on.split('-').reverse().join('.') : 'nie podano';
            addText(card, 'p', `W bibliotece od: ${date}`, 'meta');
            addText(card, 'p', book.description);
            books.appendChild(card);
        }
        status.textContent = data.items.length
            ? `Liczba książek: ${data.items.length}.`
            : 'Brak książek spełniających wybrany filtr.';
        jsonLink.href = url;
    } catch (error) {
        books.replaceChildren();
        status.className = 'error';
        status.textContent = 'Nie udało się pobrać książek. Sprawdź połączenie i spróbuj ponownie.';
    } finally {
        // włączamy przycisk ponownie
        for (const control of form.elements) control.disabled = false;
        books.setAttribute('aria-busy', 'false');
    }
}

form.addEventListener('submit', (event) => {
    event.preventDefault();
    loadBooks();
});
loadBooks();
