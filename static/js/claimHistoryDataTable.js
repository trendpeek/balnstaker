  $(document).ready(function() {
             $.fn.DataTable.ext.pager.numbers_length = 5;
             $('#claimHistory').DataTable({
               columnDefs: [
                  { orderable: false, targets: 0 },
                  { orderable: false, targets: 2 },
                  { orderable: false, targets: 3 }
               ],
               "language": {
               "emptyTable": "No data available"
               },
               "order": [[ 1, "asc" ]],
               "info": false,
               "lengthChange": false,
               "searching": false
             });
         } );