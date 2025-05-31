// Wait for the DOM to be fully loaded
document.addEventListener('DOMContentLoaded', () => {
  $('#filmTable').DataTable({
    ajax: {
      url: '../php/proiezioni/fetch.php',
      dataSrc: ''
    },
    columns: [
      { data: 'numProiezione',
        render: {
          display: (data) => `#${data}`,
          sort: (data) => data
        }
      },
      { data: 'sala' },
      { data: 'film' },
      { data: 'biglietti' },
      {
        data: 'data',
        render: (data) => {
          const [year, month, day] = data.split('-');
          return `${day}/${month}/${year}`;
        }
      },
      { data: 'ora' }
    ],
    language: {
      url: '//cdn.datatables.net/plug-ins/1.13.6/i18n/it-IT.json'
    },
    pageLength: 10
  });
});
