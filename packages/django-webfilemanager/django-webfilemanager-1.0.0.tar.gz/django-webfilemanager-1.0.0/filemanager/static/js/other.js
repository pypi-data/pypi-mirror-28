/**
 * Created by VectoR on 26-01-2018.
 */
jQuery(document).ready(function($) {

    $(".clickable-row").click(function() {
        window.location = $(this).closest('tr').data("href");
    });
     $('.file-info-button').click(function(event) {

        var path = $(this).attr('data-href');



        $('#file-info .modal-filename').text('Loading...');
        $('#file-info .modal-filesize').text('Loading...');
        $('#file-info .modal-filedate').text('Loading...');
        $('#file-info .modal-url').text('Loading...');
        $('#file-info .modal-filepath').text('Loading...');

        $.ajax({
            url:      path + '&format=json',
            type:    'get',
            success: function(data) {

                // Parse the JSON data
                var obj = jQuery.parseJSON(data);

                // Set modal pop-up hash values
                $('#file-info-modal .modal-title').text(obj.filename);
                $('#file-info .modal-filename').text(obj.filename);
                $('#file-info .modal-filesize').text(obj.filesize);
                $('#file-info .modal-filedate').text(obj.filedate);
                $('#file-info .modal-url').text(obj.fileurl);
                $('#file-info .modal-filepath').text(obj.filepath);

            }
        });

        // Show the modal
        $('#file-info-modal').modal('show');

        // Prevent default link action
        event.preventDefault();

    });

         $('#create-directory-modal').click(function () {
         var path = $(this).attr('href');
         $.ajax({
            url:   path ,
            type:    'get',

        });
          $('#create-directory .modal-title').html('Path : <b> /'+path.split('=')[1] +'</b>');
          $('#create-directory').modal('show');

        // Prevent default link action
        event.preventDefault();
     });

      $('#upload-modal-click').click(function () {
         var path = $(this).attr('href');
         $.ajax({
            url:   path ,
            type:  'get',

        });
          $('#upload-modal .modal-title').html('Path : <b> /'+path.split('=')[1] +'</b>');
          $('#upload-modal').modal('show');

        // Prevent default link action
        event.preventDefault();
     });

    $('#fileupload').fileupload({
      dataType: 'json',
        start: function (e) {
       var strProgress = 0 + "%";
      $(".progress-bar").css({"width": strProgress});
      $(".progress-bar").text(strProgress);
    },

      done: function(e, data) {
        $.each(data.result.files, function (index, file) {
            $("#show-files").append('<tr><td>'+file.name+'</tr></td>')
      });
        $('#upload-btn').click(function () {
        location.reload();
    });

    },
      progressall: function (e, data) {
      var progress = parseInt(data.loaded / data.total * 100, 10);
      var strProgress = progress + "%";
      $(".progress-bar").css({"width": strProgress});
      $(".progress-bar").text(strProgress);
    },

  });

    $('#upload-modal').on('hidden.bs.modal', function () {
        location.reload();
    });

          var urlParams = new URLSearchParams(window.location.search);
          var q = urlParams.get('path');
          if(q!=null){
              var hiddenVar='<input type="hidden" name="path" value='+q+'>';
              $('#searchform').append(hiddenVar);
          }
});