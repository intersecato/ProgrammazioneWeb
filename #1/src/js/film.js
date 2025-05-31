// Wait for the DOM to be fully loaded
document.addEventListener('DOMContentLoaded', () => {
  const tableElement = $('#filmTable');
  const dataTable = tableElement.DataTable({
    ajax: {
      url: '../php/film/fetch.php',
      dataSrc: ''
    },
    columns: [
      { data: 'titolo' },
      { data: 'anno' },
      {
        data: 'durata',
        render: (data) => {
          // Convert duration from minutes to "Xh Ymin"
          const hours = Math.floor(data / 60);
          const minutes = data % 60;
          return `${hours}h ${minutes}min`;
        }
      },
      { data: 'lingua' },
      { data: 'proiezioni',
        render: {
          display: (data) => `${data} volte`,
          sort: (data) => data
        }
       },
      { data: 'vendite',
        render: {
          display: (data) => `${data} biglietti`,
          sort: (data) => data
        }
       },
      {
        data: 'codice',
        render: (data) => `
          <button class="edit" data-id="${data}">✏️</button>
          <button class="delete" data-id="${data}">🗑️</button>
        `
      }
    ],
    language: {
      url: '//cdn.datatables.net/plug-ins/1.13.6/i18n/it-IT.json'
    },
    pageLength: 10
  });

  const addFilmBtn = document.getElementById('addFilmBtn');
  const filmModal = document.getElementById('filmModal');
  const filmForm = document.getElementById('filmForm');
  const modalTitle = document.getElementById('modalTitle');
  const closeModalBtn = document.querySelector('.modal .close');

  // Handle toast message display
  const showToast = (message, type = 'success') => {
    const toast = document.getElementById('toast');
    toast.textContent = message;
    toast.className = `toast toast-show ${type === 'success' ? 'toast-success' : 'toast-error'}`;
    toast.style.display = 'block';

    setTimeout(() => {
      toast.classList.replace('toast-show', 'toast-hide');
      toast.addEventListener('animationend', () => {
        toast.style.display = 'none';
        toast.classList.remove('toast-hide');
      }, { once: true });
    }, 3000);
  };

  const openModal = (title = 'Inserisci nuovo film') => {
    modalTitle.textContent = title;
    filmModal.classList.remove('hidden');
  };

  const closeModal = () => {
    filmModal.classList.add('hidden');
  };

  const populateForm = (data) => {
    for (const key in data) {
      if (filmForm.elements[key]) {
        filmForm.elements[key].value = data[key];
      }
    }
  };

  // Open modal when clicking "Aggiungi film" button
  addFilmBtn.addEventListener('click', () => {
    filmForm.reset();
    filmForm.elements['codice'].value = '';
    openModal('Inserisci nuovo film');
  });

  // Close modal when clicking the close button
  closeModalBtn.addEventListener('click', closeModal);

  // Handle form submission (Insert or Update)
  filmForm.addEventListener('submit', async (e) => {
    e.preventDefault();

    const formData = new FormData(filmForm);
    const data = Object.fromEntries(formData.entries());
    const isEdit = !!data.codice;
    const url = isEdit ? '../php/film/update.php' : '../php/film/insert.php';

    try {
      const response = await fetch(url, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(data)
      });

      const result = await response.json();
      if (response.ok && result.success) {
        showToast(isEdit ? 'Film aggiornato con successo!' : 'Film inserito con successo!');
        closeModal();
        dataTable.ajax.reload();
      } else {
        showToast('Errore durante il salvataggio', 'error');
      }
    } catch {
      showToast('Errore di rete', 'error');
    }
  });

  // Fill and open modal for editing a film
  tableElement.on('click', 'button.edit', function () {
    const rowData = dataTable.row($(this).closest('tr')).data();
    populateForm(rowData);
    openModal('Modifica film');
  });

  // Handle deletion of a film entry
  tableElement.on('click', 'button.delete', async function () {
    const id = this.dataset.id;
    if (!confirm('Sei sicuro di voler eliminare questo film?')) return;

    try {
      const response = await fetch(`../php/film/delete.php?id=${id}`, { method: 'DELETE' });
      const result = await response.json();

      if (response.ok && result.success) {
        showToast('Film eliminato correttamente!');
        dataTable.ajax.reload();
      } else {
        showToast('Errore durante la cancellazione', 'error');
      }
    } catch {
      showToast('Errore di rete', 'error');
    }
  });
});
