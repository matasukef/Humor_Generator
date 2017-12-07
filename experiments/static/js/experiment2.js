var parent = document.getElementById('canvas-container');
var canvas = document.getElementById('canvas');
var ctx = canvas.getContext('2d');
var img = new Image();
var isInit = false;

var list_q1 = [];
var list_q2 = [];

var render = function(){
    if(isInit){
        ctx.clearRect(0, 0, canvas.width, canvas.height);
    }else{
        isInit = true;
    }

    canvas.width = parent.clientWidth;
    canvas.height = parent.clientHeight;

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


var show_image = function(img_list){
    img.src = img_list[0];
    render();

    var counter = 1;
    $('#submit').on('click', function(){
        if(check_state('exp1_q1') && check_state('exp1_q2')){
            if(counter < num_exp){
                img.src = img_list[counter];
                render();

                counter += 1;
            }
        }
    });
    
    img.addEventListener('load', render, false);
    window.addEventListener('resize', render, false);
}

var randamize_captions = function(cap1, cap2){
    var randamized_caps1 = [];
    var randamized_caps2 = [];

    for(var i = 0; i < cap1.length; i++){
        var select = Math.random() >= 0.5;
        if(select == 0){
            randamized_caps1.push(cap1[i]);
            randamized_caps2.push(cap2[i]);
        }else{
            randamized_caps1.push(cap2[i]);
            randamized_caps2.push(cap1[i]);
        }
    }
    
    var randamized_captions = { 'caps1': randamized_caps1, 'caps2': randamized_caps2 };
    
    return randamized_captions;
}

var show_caption = function(captions, target){
    first_cap = captions[0];
    $(target).text(first_cap);

    var cap_counter = 1;
    $('#submit').on('click', function(){
        if(check_state('exp1_q1') && check_state('exp1_q2')){
            if(cap_counter < num_exp){
                cap_counter += 1;
                cap = captions[cap_counter];
                $(target).text(cap);
            }    
        }
    });
}

var show_progress = function(num){
    first_ratio = 100 / num;
    $('.progress-bar').css('width', first_ratio + '%');
    $('.progress-bar').text('1/' + num);

    var progress_counter = 1;
    $('#submit').on('click', function(){
        if(check_state('exp1_q1') && check_state('exp1_q2')){
            if(progress_counter < num){
                progress_counter += 1;
                ratio = (progress_counter / num) * 100;
                $('.progress-bar').css('width', ratio + '%');
                $('.progress-bar').text(progress_counter + '/' + num);
            }
        }
    });
}

var check_state = function(target_name){
    //var state = $('input[name=' + target_name + ']').val();
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

var get_all_result = function(){
    var result_counter = 0;
    $('#submit').on('click', function(){
        if(check_state('exp1_q1') && check_state('exp1_q2')){
            $('#warning').empty();
            res1 = get_result('exp1_q1', '.caption1');
            res2 = get_result('exp1_q2', '.caption2');
            
            if(cap_list.indexOf(res1['cap']) >= 0){
                list_q1.push(res1['val']);
                list_q2.push(res2['val']);
            }else{
                list_q1.push(res2['val']);
                list_q2.push(res1['val']);
            }
            result_counter += 1;
            if(result_counter >= num_exp){
                var form = $('<form/>', {action: "finish_experiment", method: "post"});
                for(i = 0; i < num_exp; i++){
                    j = i + 1;
                    form.append($('<input/>', {type: 'hidden', name: 'exp1_q' + j + '_1', value: list_q1[i] }));
                    form.append($('<input/>', {type: 'hidden', name: 'exp1_q' + j + '_2', value: list_q2[i] }));
                }
                form.appendTo(document.body).submit();
            }

        }else{
            $('#warning').text('記入されていないフォームがあります。');
        }
    });
}

randamized_captions = randamize_captions(cap_list, humor_cap_list);

show_image(data_list['images']);
show_caption(randamized_captions['caps1'], '.caption1');
show_caption(randamized_captions['caps2'], '.caption2');
show_progress(num_exp);
get_all_result();
