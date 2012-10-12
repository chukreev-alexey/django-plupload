var uploaders = uploaders || {};
$(function(){
  for (var key in uploaders) {
    var uploader = uploaders[key];
    uploader.bind('QueueChanged', function(up) {
      up.start();
    });
    uploader.bind('FileUploaded', function(up, file, response) {
      result = JSON.parse(response.response)
      console.log(result);
    });
    uploader.bind('Error', function(up, error){
      alert(error.message);
    });
    uploader.init();
  }
});
