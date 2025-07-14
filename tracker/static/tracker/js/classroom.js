document.addEventListener('DOMContentLoaded', function () {
    const classroomId = window.CLASSROOM_ID;
    const csrfToken = window.CSRF_TOKEN;
    const tableBody = document.querySelector('#treeview-table tbody');
    const showNotesCheckbox = document.getElementById('show_notes');
    const notesCountSelect = document.getElementById('notes_count');

    function toggleStarsColumn(show) {
        document.querySelectorAll('.col-stars-header').forEach(th => th.style.display = show ? '' : 'none');
        document.querySelectorAll('.col-stars-cell').forEach(td => td.style.display = show ? '' : 'none');
        document.querySelectorAll('.col-button-header').forEach(th => th.style.display = show ? '' : 'none');
        document.querySelectorAll('.add-star-btn, .remove-star-btn').forEach(btn => btn.style.display = show ? '' : 'none');
    }

    function toggleNotesColumn(show) {
        // Hide all note headers (Note 1, Note 2, ..., Final Note)
        document.querySelectorAll('.col-notes-header, .col-final-note-header').forEach(th => {
            th.style.display = show ? '' : 'none';
        });

        // Hide all note cells (per student)
        document.querySelectorAll('.col-notes-cell, .col-final-note-cell').forEach(td => {
            td.style.display = show ? '' : 'none';
        });
    }

    function generateNotesHeader(count) {
        document.querySelectorAll('.col-notes-header, .col-final-note-header').forEach(el => el.remove());
        const headerRow = document.getElementById('header-row');
        const starsHeader = document.querySelector('.col-stars-header');

        for (let i = 1; i <= count; i++) {
            const th = document.createElement('th');
            th.classList.add('col-notes-header');
            th.textContent = `Note ${i}`;
            headerRow.insertBefore(th, starsHeader);
        }

        const finalTh = document.createElement('th');
        finalTh.classList.add('col-final-note-header');
        finalTh.textContent = 'Final Note';
        headerRow.insertBefore(finalTh, starsHeader);
    }

    function attachStarButtonListeners() {
        document.querySelectorAll('.add-star-btn').forEach(button => {
            button.addEventListener('click', function () {
                const studentId = this.getAttribute('data-student-id');
                const starsCell = this.closest('tr').querySelector('.col-stars-cell');

                // Get or create the inner span
                let starsSpan = starsCell.querySelector('.stars-wrapper');
                if (!starsSpan) {
                    starsSpan = document.createElement('span');
                    starsSpan.classList.add('stars-wrapper');
                    starsCell.innerHTML = ''; // Clear anything else
                    starsCell.appendChild(starsSpan);
                }

                const current = starsSpan.textContent.length;

                fetch('/api/treeview-settings/increment-star/', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json', 'X-CSRFToken': csrfToken },
                    body: JSON.stringify({ student_id: studentId })
                })
                .then(res => res.json())
                .then(data => {
                    if (data.status === 'success') {
                        starsSpan.textContent = '⭐'.repeat(current + 1);
                    }
                });
            });
        });

        document.querySelectorAll('.remove-star-btn').forEach(button => {
            button.addEventListener('click', function () {
                const studentId = this.getAttribute('data-student-id');
                const starsCell = this.closest('tr').querySelector('.col-stars-cell');

                // Get or create the inner span
                let starsSpan = starsCell.querySelector('.stars-wrapper');
                if (!starsSpan) {
                    starsSpan = document.createElement('span');
                    starsSpan.classList.add('stars-wrapper');
                    starsCell.innerHTML = '';
                    starsCell.appendChild(starsSpan);
                }

                const current = starsSpan.textContent.length;

                fetch('/api/treeview-settings/remove-star/', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json', 'X-CSRFToken': csrfToken },
                    body: JSON.stringify({ student_id: studentId })
                })
                .then(res => res.json())
                .then(data => {
                    if (data.status === 'success') {
                        starsSpan.textContent = '⭐'.repeat(Math.max(current - 1, 0));
                    }
                });
            });
        });
    }


    function regenerateStudentTable(notesCount) {
        if (!tableBody) return;
        tableBody.innerHTML = '';

        fetch('/api/students/')
            .then(res => res.json())
            .then(data => {
                const students = data
                    .filter(s => s.classroom_id === classroomId)
                    .sort((a, b) => (b.stars_count || 0) - (a.stars_count || 0));

                students.forEach(student => {
                    const row = document.createElement('tr');

                    // Editable Name
                    const nameTd = document.createElement('td');
                    nameTd.textContent = student.name;
                    nameTd.style.cursor = 'pointer';
                    nameTd.addEventListener('click', () => {
                        const input = document.createElement('input');
                        input.type = 'text';
                        input.value = student.name;
                        input.classList.add('editable-input');
                        input.style.width = '100%';  // ensures no resizing of column
                        input.style.boxSizing = 'border-box';  // prevent overflow
                        nameTd.innerHTML = '';
                        nameTd.appendChild(input);
                        input.focus();

                        input.addEventListener('blur', () => {
                            const newName = input.value.trim();
                            if (!newName || newName === student.name) {
                                nameTd.textContent = student.name;
                                return;
                            }
                            fetch(`/api/students/${student.id}/`, {
                                method: 'PATCH',
                                headers: {
                                    'Content-Type': 'application/json',
                                    'X-CSRFToken': csrfToken
                                },
                                body: JSON.stringify({ name: newName })
                            })
                            .then(res => res.json())
                            .then(() => regenerateStudentTable(notesCount))
                            .catch(err => {
                                console.error('Name update failed:', err);
                                nameTd.textContent = student.name;
                            });
                        });

                        input.addEventListener('keydown', (e) => {
                            if (e.key === 'Enter') input.blur();
                        });
                    });
                    row.appendChild(nameTd);

                    // Editable Surname
                    const surnameTd = document.createElement('td');
                    surnameTd.textContent = student.surname || '-';
                    surnameTd.style.cursor = 'pointer';
                    surnameTd.addEventListener('click', () => {
                        const input = document.createElement('input');
                        input.type = 'text';
                        input.value = student.surname || '';
                        input.classList.add('editable-input');
                        input.style.width = '100%';  // ensures no resizing of column
                        input.style.boxSizing = 'border-box';  // prevent overflow
                        surnameTd.innerHTML = '';
                        surnameTd.appendChild(input);
                        input.focus();
                        input.addEventListener('blur', () => {
                            const newSurname = input.value.trim();
                            if (newSurname === student.surname) {
                                surnameTd.textContent = student.surname || '-';
                                return;
                            }
                            fetch(`/api/students/${student.id}/`, {
                                method: 'PATCH',
                                headers: {
                                    'Content-Type': 'application/json',
                                    'X-CSRFToken': csrfToken
                                },
                                body: JSON.stringify({ surname: newSurname })
                            })
                            .then(res => res.json())
                            .then(() => regenerateStudentTable(notesCount))
                            .catch(err => {
                                console.error('Surname update failed:', err);
                                surnameTd.textContent = student.surname || '-';
                            });
                        });

                        input.addEventListener('keydown', (e) => {
                            if (e.key === 'Enter') input.blur();
                        });
                    });
                    row.appendChild(surnameTd);

                    // Editable Notes
                    for (let i = 0; i < notesCount; i++) {
                        const note = Array.isArray(student.notes) ? (student.notes[i] ?? '-') : '-';
                        const td = document.createElement('td');
                        td.classList.add('col-notes-cell');
                        td.textContent = note;
                        td.style.cursor = 'pointer';

                        td.addEventListener('click', () => {
                            const currentValue = td.textContent.trim() === '-' ? '' : td.textContent.trim();
                            const input = document.createElement('input');
                            input.type = 'text';
                            input.value = currentValue;
                            input.classList.add('editable-input');
                            input.style.width = '100%';  // ensures no resizing of column
                            input.style.boxSizing = 'border-box';  // prevent overflow
                            td.innerHTML = '';
                            td.appendChild(input);
                            input.focus();

                            input.addEventListener('blur', () => {
                                const newValue = input.value.trim() === '' ? null : parseInt(input.value.trim());
                                const updatedNotes = [...(student.notes || [])];
                                updatedNotes[i] = newValue;

                                fetch(`/api/students/${student.id}/`, {
                                    method: 'PATCH',
                                    headers: {
                                        'Content-Type': 'application/json',
                                        'X-CSRFToken': csrfToken
                                    },
                                    body: JSON.stringify({ notes: updatedNotes })
                                })
                                .then(res => res.json())
                                .then(() => regenerateStudentTable(notesCount))
                                .catch(err => {
                                    console.error("Note update failed:", err);
                                    td.textContent = currentValue;
                                });
                            });

                            input.addEventListener('keydown', (e) => {
                                if (e.key === 'Enter') input.blur();
                            });
                        });

                        row.appendChild(td);
                    }

                    // Final Note
                    //const finalTd = document.createElement('td');
                    //finalTd.classList.add('col-final-note-cell');
                    //const validNotes = (student.notes || []).slice(0, notesCount).filter(n => n !== null && !isNaN(n));
                    //const average = validNotes.length > 0 ? Math.round(validNotes.reduce((a, b) => a + b, 0) / validNotes.length) : '-';
                    //finalTd.textContent = average;
                    //row.appendChild(finalTd);

                    const finalTd = document.createElement('td');
                    finalTd.classList.add('col-final-note-cell');
                    finalTd.textContent = student.note_overall !== null ? student.note_overall : '-';
                    row.appendChild(finalTd);

                    // Stars
                    const starsTd = document.createElement('td');
                    starsTd.classList.add('col-stars-cell');

                    const starsSpan = document.createElement('span');
                    starsSpan.classList.add('stars-wrapper');
                    starsSpan.textContent = '⭐'.repeat(student.stars_count || 0);

                    starsTd.appendChild(starsSpan);
                    row.appendChild(starsTd);

                    // Buttons
                    const btnTd = document.createElement('td');
                    btnTd.classList.add('col-button-header');
                    btnTd.innerHTML = `
                        <button class="btn btn-primary add-star-btn btn-sm" data-student-id="${student.id}">Add A Star</button>
                        <button class="btn btn-danger remove-star-btn btn-sm" data-student-id="${student.id}">Remove A Star</button>
                    `;

                    row.appendChild(btnTd);

                    tableBody.appendChild(row);
                });

                toggleNotesColumn(showNotesCheckbox.checked);
                attachStarButtonListeners();
            })
            .catch(error => console.error('Error loading students:', error));
    }

    function updateNotesHeaderAndTable() {
        const count = parseInt(notesCountSelect.value);
        generateNotesHeader(count);
        regenerateStudentTable(count);
    }

    // Initial setup
    const initialNotesCount = parseInt(notesCountSelect.value);
    generateNotesHeader(initialNotesCount);
    toggleStarsColumn(document.getElementById('show_stars')?.checked);
    regenerateStudentTable(initialNotesCount);
    toggleNotesColumn(showNotesCheckbox.checked);

    ['show_notes', 'show_stars', 'notes_count'].forEach(field => {
        const el = document.getElementById(field);
        if (!el) return;

        el.addEventListener('change', () => {
            let value = el.type === 'checkbox' ? el.checked : el.value;
            let url = '/api/treeview-settings/';
            let payload = { [field]: value };

            if (field === 'show_notes') {
                generateNotesHeader(parseInt(notesCountSelect.value));
                toggleNotesColumn(value);
            }

            if (field === 'show_stars') {
                toggleStarsColumn(value);
            }

            if (field === 'notes_count') {
                const count = parseInt(value);
                updateNotesHeaderAndTable();
                toggleNotesColumn(showNotesCheckbox.checked);
                url = '/api/classes/';
                payload = {
                    id: classroomId,
                    notes_count: count
                };
            }

            fetch(url, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': csrfToken,
                },
                body: JSON.stringify(payload)
            })
            .then(res => res.json())
            .then(data => console.log(`Updated ${field}:`, data))
            .catch(err => console.error(`Error updating ${field}:`, err));
        });
    });
});
