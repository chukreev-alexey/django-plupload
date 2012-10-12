var uploaders = uploaders || {};
$(function(){
  var button_id = '{{ button_id }}',
    settings = {{ upload_settings|safe }};
  settings['headers']['X-CSRFToken'] = CSRF_TOKEN;
  settings['headers']['X-PluploadKey'] = button_id;
  uploaders[button_id] = new plupload.Uploader(settings);
});
