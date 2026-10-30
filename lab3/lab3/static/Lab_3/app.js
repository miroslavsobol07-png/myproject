let tasks = [];
let currentFilter = 'all';
let busy = false;

const form = document.querySelector('#task-form');
const apiUrl = form.dataset.apiUrl;
const titleInput = document.querySelector('#task-title');
const taskList = document.querySelector('#task-list');
const emptyState = document.querySelector('#empty-state');
const message = document.querySelector('#message');
const filterButtons = document.querySelectorAll('[data-filter]');
const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;

function showMessage(text = '') {
    message.textContent = text;
    message.hidden = !text;
}

function setBusy(value) {
    busy = value;
    form.querySelector('button').disabled = value;
    titleInput.disabled = value;
    taskList.querySelectorAll('button').forEach(button => { button.disabled = value; });
    taskList.setAttribute('aria-busy', String(value));
}

async function apiRequest(url, method = 'GET', data = null) {
    const options = { method, credentials: 'same-origin', headers: {} };
    if (method !== 'GET') {
        options.headers['X-CSRFToken'] = csrfToken;
    }
    if (data !== null) {
        options.headers['Content-Type'] = 'application/json';
        options.body = JSON.stringify(data);
    }
    let response;
    try {
        response = await fetch(url, options);
    } catch {
        throw new Error('Nie można połączyć się z serwerem. Sprawdź połączenie i spróbuj ponownie.');
    }
    let result;
    try {
        result = await response.json();
    } catch {
        throw new Error(`Serwer zwrócił nieprawidłową odpowiedź (HTTP ${response.status}).`);
    }
    if (!response.ok) {
        throw new Error(result.error || `Nie udało się wykonać operacji (HTTP ${response.status}).`);
    }
    return result;
}

function renderTasks() {
    const visibleTasks = tasks.filter(task => {
        if (currentFilter === 'active') return !task.completed;
        if (currentFilter === 'completed') return task.completed;
        return true;
    });
    taskList.replaceChildren();
    visibleTasks.forEach(task => {
        const item = document.createElement('li');
        item.className = task.completed ? 'task completed' : 'task';
        const title = document.createElement('span');
        title.className = 'task-title';
        title.textContent = task.title;
        const actions = document.createElement('div');
        actions.className = 'task-actions';
        const toggle = document.createElement('button');
        toggle.type = 'button';
        toggle.textContent = task.completed ? 'Przywróć' : 'Ukończ';
        toggle.setAttribute('aria-label', `${toggle.textContent}: ${task.title}`);
        toggle.disabled = busy;
        toggle.addEventListener('click', () => toggleTask(task));
        const remove = document.createElement('button');
        remove.type = 'button';
        remove.className = 'delete';
        remove.textContent = 'Usuń';
        remove.setAttribute('aria-label', `Usuń: ${task.title}`);
        remove.disabled = busy;
        remove.addEventListener('click', () => deleteTask(task.id));
        actions.append(toggle, remove);
        item.append(title, actions);
        taskList.append(item);
    });
    document.querySelector('#total-count').textContent = tasks.length;
    document.querySelector('#completed-count').textContent = tasks.filter(task => task.completed).length;
    emptyState.hidden = visibleTasks.length > 0;
    emptyState.textContent = tasks.length === 0
        ? 'Brak zadań. Dodaj pierwsze zadanie powyżej.'
        : 'Brak zadań w tym filtrze.';
    filterButtons.forEach(button => {
        button.setAttribute('aria-pressed', String(button.dataset.filter === currentFilter));
    });
}

async function loadTasks() {
    setBusy(true);
    showMessage();
    try {
        tasks = await apiRequest(apiUrl);
        renderTasks();
    } catch (error) {
        emptyState.textContent = 'Nie udało się wczytać listy. Odśwież stronę, aby spróbować ponownie.';
        showMessage(error.message);
    } finally {
        setBusy(false);
    }
}

async function addTask(event) {
    event.preventDefault();
    if (busy) return;
    const title = titleInput.value.trim();
    if (!title) {
        showMessage('Wpisz treść zadania. Pole nie może być puste.');
        titleInput.focus();
        return;
    }
    if (title.length > 200) {
        showMessage('Zadanie może mieć najwyżej 200 znaków.');
        return;
    }
    setBusy(true);
    showMessage();
    try {
        const task = await apiRequest(apiUrl, 'POST', { title });
        tasks.unshift(task);
        titleInput.value = '';
        renderTasks();
    } catch (error) {
        showMessage(error.message);
    } finally {
        setBusy(false);
        titleInput.focus();
    }
}

async function toggleTask(task) {
    if (busy) return;
    setBusy(true);
    showMessage();
    try {
        const updated = await apiRequest(`${apiUrl}${task.id}/`, 'PATCH', { completed: !task.completed });
        tasks = tasks.map(item => item.id === updated.id ? updated : item);
        renderTasks();
    } catch (error) {
        showMessage(error.message);
    } finally {
        setBusy(false);
    }
}

async function deleteTask(id) {
    if (busy) return;
    setBusy(true);
    showMessage();
    try {
        await apiRequest(`${apiUrl}${id}/`, 'DELETE');
        tasks = tasks.filter(task => task.id !== id);
        renderTasks();
    } catch (error) {
        showMessage(error.message);
    } finally {
        setBusy(false);
    }
}

form.addEventListener('submit', addTask);
filterButtons.forEach(button => {
    button.addEventListener('click', () => {
        currentFilter = button.dataset.filter;
        renderTasks();
    });
});
loadTasks();
