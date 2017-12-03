$(function(){
    
    $("#choose").change(function(){

        if(this.files.length){

            if($('#results').length){
                $('#results').empty();
            }

            var file = this.files[0];
            var canvas = document.getElementById('main');
            var ctx = canvas.getContext('2d');

            var image = new Image();

            var fr = new FileReader();

            fr.onload = function(evt){

                image.onload = function(){


                    //get the size of canvas;
                    var ch = canvas.height;
                    var cw = canvas.width;
                    
                    //get the size of image;
                    var image_height = image.naturalHeight;
                    var image_width = image.naturalWidth;

                    if(image_height >= image_width){
                        var mag = ch/image_height;
                    }else{
                        var mag = cw/image_width;
                    }

                    //resized image size;
                    var resized_height = image_height * mag;
                    var resized_width = image_width * mag;
                    ctx.fillStyle = "black";
                    ctx.fillRect(0, 0, cw, ch);
                    if(resized_height > resized_width){
                        var center = cw/2 - resized_width/2;
                        ctx.drawImage(image, center, 0, resized_width, resized_height);
                    }else{
                        var center = ch/2 - resized_height/2;
                        ctx.drawImage(image, 0, center, resized_width, resized_height);
                    }
                    

                    var formData = new FormData();
                    var targetFile = $('input[name=img]');
                    formData.append('file', $(targetFile).prop("files")[0]);

                    //get similarity config
                    var img_sim = $('#img_sim').val();
                    var word_sim = $('#word_sim').val();
                    var colloquial = $('#colloquial').is(':checked');
                    var num_caption = $('#num_caption').val();
                    var offset = $('#offset').val();
                    formData.append('img_sim', img_sim);
                    formData.append('word_sim', word_sim);
                    formData.append('colloquial', colloquial);
                    formData.append('num_caption', num_caption);
                    formData.append('offset', offset);
                    
                    $.ajax({
                        url: '/api',
                        type: 'POST',
                        //contentType: 'image/jpeg',
                        //contentType: 'multipart/form-data'
                        dataType: 'json',
                        data: formData,
                        contentType: false,
                        processData: false,
                    })
                    .success(function(data, statusText, jqXHR){
                        
                        $('#captions').empty();
                        $('#detail').empty();
                        
                        var head = '<tr><th class="col-md-1">No</th><th class="col-md-9">Captions</th></tr>';
                        $('#captions').append(head);
                        
                        //var normal_cap = data[0]['caption']['sentence'];
                        //element = '<tr><td>Normal cap</td><td>' + normal_cap + '</td></tr>';
                        //$('#captions').append(element);

                        var num_captions = Object.keys(data[0]['humor_captions']).length;
                        for(i = 0; i < num_captions; i++){
                            var cap = data[0]['humor_captions'][i];
                            var no = i + 1
                            element = '<tr><td>' + no + '</td><td>' + cap + '</td></tr>';

                            $('#captions').append(element);
                        }

                        createDetail(data, '#detail');          

                    })
                    .fail(function(jqXHR, statusText, errorThrown){
                        console.log(errorThrown);
                        console.log(statusText);
                        console.log(jqXHR);
                    });
                }
            image.src = evt.target.result;
            }
        fr.readAsDataURL(file);
        }
    });
});


drawImage = function(tag, img){
    
    var canvas = document.getElementById(tag);
    var ctx = canvas.getContext('2d');

    var image = new Image();

    image.onload = function(){

        //get the size of canvas;
        var ch = canvas.height;
        var cw = canvas.width;

        //get the size of image;
        var image_height = image.naturalHeight;
        var image_width = image.naturalWidth;

        if(image_height >= image_width){
            var mag = ch/image_height;
        }else{
            var mag = cw/image_width;
        }

        //resized image size;
        var resized_height = image_height * mag;
        var resized_width = image_width * mag;
        ctx.fillStyle = "black";
        ctx.fillRect(0, 0, cw, ch);
        if(resized_height > resized_width){
            var center = cw/2 - resized_width/2;
            ctx.drawImage(image, center, 0, resized_width, resized_height);
        }else{
            var center = ch/2 - resized_height/2;
            ctx.drawImage(image, 0, center, resized_width, resized_height);
        }
    }
    image.src = "data:image/jpg;base64," + img;
}

createDetail = function(result, table_id){
    
    $(table_id).empty();
    
    var head = '<tr>' +
                    '<th class="col-md-2">keys</th>' +
                    '<th class="col-md-8">values</th>' +
                '</tr>';

    $(table_id).append(head);

    var normal_cap = result[0]['caption']['sentence'];
    var caption_table = '<tr>' +
                            '<td>Caption</td>' +
                            '<td>' + normal_cap + '</td>' +
                        '</tr>';
    $(table_id).append(caption_table);

    var subject = result[0]['subject'];
    var subject_table = '<tr>' +
                            '<td>Subject</td>' +
                            '<td>' + subject + '</td>' +
                        '<tr>';
    $(table_id).append(subject_table);
    
    //image word sim words
    var iws_words = result[0]['img_word_sim_words'];
    var img_word_sim_words_table = '<tr>' +
                                        '<td>Image Word Sim Norms</td>' +
                                        '<td>' +
                                            '<table id="iws_words" class="table border-collapse:collapse">' +
                                                '<tr>' +
                                                    '<th class="col-md-2">Scores</th>' +
                                                    '<th class="col-md-6">Norms</th>' +
                                                '</tr>' +
                                            '</table>' +
                                        '</td>' +
                                    '</td>';
    $(table_id).append(img_word_sim_words_table);
    
    var num_iws_words = Object.keys(iws_words).length;
    for(i = 0; i < num_iws_words; i++){
        var iws_word = iws_words[i]['norm'];
        var iws_sim = iws_words[i]['score'];
        var img_word_sim_words_detail = '<tr>' +
                                            '<td>' + iws_sim + '</td>' +
                                            '<td>' + iws_word + '</td>' +
                                        '</tr>';
        $('#iws_words').append(img_word_sim_words_detail);
    }

    //image sim words
    var is_words = result[0]['img_sim_words'];
    var img_sim_words_table = '<tr>' +
                                    '<td>Image Sim Norms</td>' +
                                    '<td>' +
                                        '<table id="is_words" class="table border-collapse:collapse">' +
                                            '<tr>' +
                                                '<th class="col-md-2">Sims</th>' +
                                                '<th class="col-md-6">Norms</th>' +
                                            '</tr>' +
                                        '</table>' +
                                    '</td>' +
                                '</tr>';
    $(table_id).append(img_sim_words_table);
    var num_is_words = Object.keys(is_words).length;
    for(i = 0; i < num_is_words; i++){
        var is_word = is_words[i]['norm'];
        var is_sim = is_words[i]['sim'];
        var img_sim_words_detail =  '<tr>' +
                                        '<td>' + is_sim + '</td>' +
                                        '<td>' + is_word + '</td>' +
                                    '</tr>';
        $('#is_words').append(img_sim_words_detail);
    }

    //word sim words
        var ws_words = result[0]['word_sim_words'];
        var word_sim_words_table = '<tr>' +
                                        '<td>Word Sim Norms</td>' +
                                        '<td>' +
                                            '<table id="ws_words" class="table border-collapse:collapse">' +
                                                '<tr>' +
                                                    '<th class="col-md-2">Sims</th>' +
                                                    '<th class="col-md-6">Norms</th>' +
                                                '</tr>' +
                                            '</table>' +
                                        '</td>' +
                                    '</tr>';
        $(table_id).append(word_sim_words_table);
        var num_ws_words = Object.keys(ws_words).length;
        for(i = 0; i < num_ws_words; i++){
            var ws_word = ws_words[i]['norm'];
            var ws_sim = ws_words[i]['sim'];
            var word_sim_words_detail =  '<tr>' +
                                            '<td>' + ws_sim + '</td>' +
                                            '<td>' + ws_word + '</td>' +
                                        '</tr>';
            $('#ws_words').append(word_sim_words_detail);
        }
}

