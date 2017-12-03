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
                    console.log(colloquial);
                    formData.append('img_sim', img_sim);
                    formData.append('word_sim', word_sim);
                    formData.append('colloquial', colloquial);
                    
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
                        

                        var head = '<tr><th class="col-md-2">No</th><th class="col-md-8">Captions</th></tr>';
                        $('#captions').append(head);
                        
                        var normal_cap = data[0]['caption']['sentence'];
                        element = '<tr><td>Normal cap</td><td>' + normal_cap + '</td></tr>';
                        $('#captions').append(element);

                        var num_captions = Object.keys(data[0]['humor_captions']).length;
                        for(i = 0; i < num_captions; i++){
                            var cap = data[0]['humor_captions'][i];
                            var no = i + 1
                            element = '<tr><td>' + no + '</td><td>' + cap + '</td></tr>';

                            $('#captions').append(element);
                        }

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
    
    var table_id = '#' + table_id
    $(table_id).empty();
    
    var head = '<thread>' +
                    '<tr>' +
                        '<th>keys</th>' +
                        '<th>values</th>' +
                    '</tr>' +
                '/thread';

    $(table_id).append(head);
                        
                        var normal_cap = data[0]['caption']['sentence'];
                        element = '<tr><td>Normal cap</td><td>' + normal_cap + '</td></tr>';
                        $('#captions').append(element);

                        var num_captions = Object.keys(data[0]['humor_captions']).length;
                        for(i = 0; i < num_captions; i++){
                            var cap = data[0]['humor_captions'][i];
                            var no = i + 1
                            element = '<tr><td>' + no + '</td><td>' + cap + '</td></tr>';

                            $('#captions').append(element);
                        }

}

