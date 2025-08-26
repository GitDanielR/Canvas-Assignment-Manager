function removeLink(btn) {
    btn.parentElement.remove();
}

function normalizeLink(link) {
    if (!/^https?:\/\//i.test(link)) {
        return "http://" + link;
    }
    return link;
}

function cleanFilePath(path) {
    path = path.trim();
    if (!path) return "";

    path = path.replace(/['"]/g, '');
    path = path.replace(/\\/g, "/");
    path = path.replace(/([^:]\/)\/+/g, "$1");
    
    if (path.length > 1 && path.endsWith("/")) {
        path = path.slice(0, -1);
    }
    return path;
}

function addLink(event) {
    event.preventDefault();
    const input = document.getElementById('new-link');
    let url = input.value.trim();
    if (!url) return;
    url = normalizeLink(url);
    const ul = document.getElementById('links-list');
    const li = document.createElement('li');
    li.className = 'link-item';
    li.innerHTML = `<span class="link-text">${url}</span>
                    <button type="button" class="remove-link-btn" onclick="removeLink(this)">Remove</button>`;
    ul.appendChild(li);
    input.value = '';
}

function addFile(event) {
    event.preventDefault();
    const input = document.getElementById('new-file');
    const file = cleanFilePath(input.value);
    if (!file) return;
    const ul = document.getElementById('links-list');
    const li = document.createElement('li');
    li.className = 'link-item';
    li.innerHTML = `<span class="link-text">${file}</span>
                    <button type="button" class="remove-link-btn" onclick="removeLink(this)">Remove</button>`;
    ul.appendChild(li);
    input.value = '';
}

function saveLinks() {
    const related_links_files = Array.from(document.querySelectorAll('#links-list .link-text')).map(span => span.innerHTML);
    
    fetch(`/assignments/${assignmentId}/save_related_links_files`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ related_links_files })
    })
    .then(response => {
        if (response.ok) {
            showToast("Related links/files saved successfully!", 2000);
        }
    });
}