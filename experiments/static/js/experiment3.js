var parent = document.getElementById('canvas-container');
var canvas = document.getElementById('canvas');
var ctx = canvas.getContext('2d');
var img = new Image();
var isInit = false;

var render = function(){
    if(isInit){
        ctx.clearRect(0, 0, canvas.width, canvas.height);
    }else{
        isInit = true;
    }

    //canvas.width = parent.clientWidth;
    //canvas.height = parent.clientHeight;

    var canvas_height = canvas.height;
    var canvas_width = canvas.width;

    var img_height = img.naturalHeight;
    var img_width = img.naturalWidth;

    if(img_height > img_width){
        var mag = canvas_height / img_height;
    }else{
        var mag = canvas_width / img_width;
    }

    var resized_height = img_height * mag;
    var resized_width = img_width * mag;

    ctx.fillStyle = "black";
    ctx.fillRect(0, 0, canvas_width, canvas_height);

    if(resized_height > resized_width){
        var center = canvas_width / 2 - resized_width / 2;
        ctx.drawImage(img, center, 0, resized_width, resized_height);
    }else{
        var center = canvas_height / 2 - resized_height / 2;
        ctx.drawImage(img, 0, center, resized_width, resized_height);
    }
}

var check_state = function(target_name){
    var state = $("[name=" + target_name + "]:checked").val();
    return state;
}

var clear_checked = function(target_name){
    $('input[name=' + target_name + ']').prop('checked', false);
    $('.btn').removeClass('active');
}

var get_result = function(target_name, cap_class){
    var res = [];
    
    var val = $('input[name=' + target_name + ']:checked').val();
    var cap = $(cap_class).text();
    clear_checked(target_name);

    res = {'val': val, 'cap': cap}

    return res;
}


var init = function(num, data){
    
    /*progress bar*/
    ratio = 100 / num;
    $('.progress-bar').css('width', ratio + '%');
    $('.progress-bar').text('1/' + num);
    
    /*show image*/
    img.src = data['images'][0];
    render();
    img.addEventListener('load', render, false);
    window.addEventListener('resize', render, false);

    $('.caption1').text(data_list['captions'][0]);
}

var get_all_result = function(){
    
    var result_counter = 1;
    var result = [];

    $('#submit').on('click', function(){
        if(check_state('exp3_q1')){
            $('#warning').empty();
            res = get_result('exp3_q1', '.caption1');
            result.push(res['val']);
            
            /* show new image */
            img.src = data_list['images'][result_counter];
            render();
    
            /* show new caption */
            $('.caption1').text(data_list['captions'][result_counter]);
        
            /* progress counter */
            ratio = ((result_counter+1) / num_exp) * 100;
            $('.progress-bar').css('width', ratio + '%');
            $('.progress-bar').text((result_counter + 1) + '/' + num_exp);
        
            result_counter += 1;

            if(result_counter > num_exp){
                
                /* push result_table to result_list */
                var form = $('<form/>', {action: "finish", method: "post"});
                for(let i = 0; i < num_exp; i++){
                    let number = i + 1;
                    form.append($('<input/>', {type: 'hidden', name: 'exp3_q' + number, value: result[i] }));
                }

                for(let i = 0; i < num_exp; i++){
                    let number = i + 1;
                    let img_path = data_list['images'][i].split('/');
                        form.append($('<input/>', {type: 'hidden', name: 'exp3_q' + number + '_image', value: img_path[img_path.length - 1] }));

                }

                form.appendTo(document.body).submit();
            }

        }else{
            $('#warning').text('記入されていないフォームがあります。');
        }
    });
}


init(num_exp, data_list);
get_all_result();
