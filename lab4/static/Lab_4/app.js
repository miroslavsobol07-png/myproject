const button = document.querySelector('#load');
const filter = document.querySelector('#available');
const books = document.querySelector('#books');
const status = document.querySelector('#status');

// textContent wyświetla tekst z bazy bez wykonywania kodu HTML.
function addText(parent, tag, text, className = '') {
    const element = document.createElement(tag);
    element.textContent = text;
    element.className = className;
    parent.appendChild(element);
}

button.addEventListener('click', async () => {
    button.disabled = true;
    filter.disabled = true;
    books.setAttribute('aria-busy', 'true');
    books.replaceChildren();
    status.className = '';
    status.textContent = 'Ładowanie książek…';

    try {
        // Wartość filtra trafia do Django jako parametr adresu URL.
        const params = new URLSearchParams({available: filter.value});
        const response = await fetch(`${button.dataset.url}?${params}`);
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
            addText(card, 'span', book.available ? 'Dostępna' : 'Wypożyczona',
                book.available ? 'badge' : 'badge unavailable');
            addText(card, 'h3', book.title);
            addText(card, 'p', book.author);
            addText(card, 'p', `${book.genre} · ${book.year}`, 'meta');
            addText(card, 'p', book.description);
            books.appendChild(card);
        }
        status.textContent = data.items.length
            ? `Liczba książek: ${data.items.length}. Wyniki dla: ${filter.selectedOptions[0].textContent.toLowerCase()}.`
            : 'Brak książek spełniających wybrany filtr.';
    } catch (error) {
        books.replaceChildren();
        status.className = 'error';
        status.textContent = 'Nie udało się pobrać książek. Sprawdź połączenie i spróbuj ponownie.';
    } finally {
        // Przywracamy obsługę przycisku także po błędzie.
        button.disabled = false;
        filter.disabled = false;
        books.setAttribute('aria-busy', 'false');
    }
});
