document.addEventListener('DOMContentLoaded', () => {
  $('#filmTable').DataTable({
    ajax: {
      url: '/api/sale/',
      dataSrc: ''
    },
    columns: [
      {
        data: 'numero',
        render: {
          display: (data) => `#${data}`,
          sort: (data) => data
        }
      },
      {
        data: 'dim',
        render: {
          display: (data) => `${data} posti`,
          sort: (data) => data
        }
      },
      { data: 'tipo' },
      {
        data: 'num_proiezioni',
        render: {
          display: (data) => `${data} film`,
          sort: (data) => data
        }
      }
    ],
    language: {
      url: '//cdn.datatables.net/plug-ins/1.13.6/i18n/it-IT.json'
    },
    pageLength: 10
  });
});
