document.addEventListener('DOMContentLoaded', () => {
  const tableElement = $('#filmTable');
  const dataTable = tableElement.DataTable({
    ajax: {
      url: '/api/film/',
      dataSrc: ''
    },
    columns: [
      { data: 'titolo' },
      { data: 'anno' },
      {
        data: 'durata',
        render: data => `${Math.floor(data / 60)}h ${data % 60}min`
      },
      { data: 'lingua' },
      {
        data: 'proiezioni',
        render: data => `${data} volte`
      },
      {
        data: 'vendite',
        render: data => `${data} biglietti`
      },
      {
        data: 'codice',
        render: codice => `
          <button class="edit" data-id="${codice}">✏️</button>
          <button class="delete" data-id="${codice}">🗑️</button>
        `
      }
    ],
    language: {
      url: '//cdn.datatables.net/plug-ins/1.13.6/i18n/it-IT.json'
    }
  });

  const filmModal = document.getElementById('filmModal');
  const filmForm = document.getElementById('filmForm');
  const modalTitle = document.getElementById('modalTitle');
  const toast = document.getElementById('toast');

  const showToast = (text, type = 'success') => {
    toast.textContent = text;
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

  const openModal = (title = 'Nuovo film') => {
    modalTitle.textContent = title;
    filmModal.classList.remove('hidden');
  };

  const closeModal = () => {
    filmModal.classList.add('hidden');
  };

  document.getElementById('addFilmBtn').addEventListener('click', () => {
    filmForm.reset();
    filmForm.elements['codice'].value = '';
    openModal('Inserisci nuovo film');
  });

  document.querySelector('.modal .close').addEventListener('click', closeModal);

  filmForm.addEventListener('submit', async (e) => {
    e.preventDefault();
    const formData = new FormData(filmForm);
    const data = Object.fromEntries(formData.entries());
    const isEdit = !!data.codice;
    const url = isEdit ? '/film/update/' : '/film/insert/';

    try {
      const response = await fetch(url, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(data)
      });
      const result = await response.json();
      if (response.ok && result.success) {
        showToast(isEdit ? 'Film aggiornato!' : 'Film inserito!');
        closeModal();
        dataTable.ajax.reload();
      } else {
        showToast(result.error || 'Errore!', 'error');
      }
    } catch {
      showToast('Errore di rete', 'error');
    }
  });

  tableElement.on('click', 'button.edit', function () {
    const rowData = dataTable.row($(this).closest('tr')).data();
    for (const key in rowData) {
      if (filmForm.elements[key]) {
        filmForm.elements[key].value = rowData[key];
      }
    }
    openModal('Modifica film');
  });

  tableElement.on('click', 'button.delete', async function () {
    const id = this.dataset.id;
    if (!confirm('Eliminare questo film?')) return;
    try {
      const response = await fetch(`/film/delete/${id}/`, { method: 'DELETE' });
      const result = await response.json();
      if (response.ok && result.success) {
        showToast('Film eliminato');
        dataTable.ajax.reload();
      } else {
        showToast(result.error || 'Errore!', 'error');
      }
    } catch {
      showToast('Errore di rete', 'error');
    }
  });
});
