var parent = document.getElementById('canvas-container');
var canvas = document.getElementById('canvas');
var ctx = canvas.getContext('2d');
var img = new Image();
var isInit = false;

var sim_list = ['origin','hl','hh'];
var num_trial = num_exp * sim_list.length;

var answer_list = {}
for(let i = 0; i < sim_list.length; i++){
    answer_list[sim_list[i]] = [];
}

var render = function(){
    if(isInit){
        ctx.clearRect(0, 0, canvas.width, canvas.height);
    }else{
        isInit = true;
    }

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


var shuffle_array = function(array){
    var tmp_array = $.extend(true, [], array);
    for(let i = tmp_array.length-1; i > 0; i--){
        let r = Math.floor(Math.random() * (i + 1));
        let tmp = tmp_array[i];
        tmp_array[i] = tmp_array[r];
        tmp_array[r] = tmp;
    }

    return tmp_array;
}

var randamize_captions = function(caption_list){
    
    var randamized_list = {};
    var sim_table = {};
    for(let i = 0; i < sim_list.length; i++){
        randamized_list['cap_' + i] = [];
        sim_table['cap_' + i] = [];
    }

    for(let i = 0; i < num_exp; i++){
        let random_array = shuffle_array(sim_list);
        for(let j = 0; j < sim_list.length; j++){
            randamized_list['cap_' + j].push(data_list['cap_' + random_array[j]][i]);
            sim_table['cap_' + j].push(random_array[j]);
        }
    }

    caption_with_table = {'randamized_captions': randamized_list,
                          'sim_table': sim_table
                         }
    
    return caption_with_table;
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

var init = function(data){
    
    /*progress bar*/
    ratio = 100 / num_trial;
    $('.progress-bar').css('width', ratio + '%');
    $('.progress-bar').text('1/' + num_trial);
    
    /*show image*/
    img.src = data['images'][0];
    render();
    img.addEventListener('load', render, false);
    window.addEventListener('resize', render, false);

    $('#caption').text(caption_with_table['randamized_captions']['cap_0'][0]);
}

var get_all_result = function(){
    let question_counter = 1;
    let result_counter = 0;
    
    var result_table = [];
    for(let i = 0; i < num_exp; i++){
        result_table.push([]);
    }

    $('#submit').on('click', function(){
        if(check_state('exp1_q1')){
            $('#warning').empty();
            
            result_table[result_counter].push(get_result('exp1_q1', '#caption'));
            
            if(question_counter >= 3){
                /*move to next image*/
                result_counter += 1;
                
                if(result_counter < num_exp){
                    /*move to next images*/
                    question_counter = 0;
                    
                    /* set new image caption to caption class to show */
                    let next_cap = 'cap_0';
                    $('#caption').text(caption_with_table['randamized_captions'][next_cap][result_counter]);
                   
                    /* show new image */
                    img.src = data_list['images'][result_counter];
                    render();

                }

            }

            if(question_counter < 3){
                
                let next_cap = 'cap_' + question_counter;
                $('#caption').text(caption_with_table['randamized_captions'][next_cap][result_counter]);
                
                /*show next three captions*/
                question_counter += 1;
            }

            
            /* progress counter */
            progress = question_counter + ((result_counter+1) - 1) * 3;
            ratio = ( progress / num_trial ) * 100;
            $('.progress-bar').css('width', ratio + '%');
            $('.progress-bar').text(progress + '/' + num_trial);
            
            /* if experiment finish */
            if(result_counter >= num_exp){
                /* push result to answer_list */
                for(let i = 0; i < num_exp; i++){
                    for(let j = 0; j < sim_list.length; j++){
                        var res_cap = result_table[i][j]['cap'];
                        var res_val = result_table[i][j]['val'];
                        for(k = 0; k < sim_list.length; k++){
                            if(res_cap == caption_with_table['randamized_captions']['cap_' + k][i]){
                                answer_list[caption_with_table['sim_table']['cap_' + k][i]].push(res_val);
                            }
                        }
                    }
                }
                console.log(result_table);
                console.log(answer_list);

                /* push result_table to result_list */
                var form = $('<form/>', {action: "finish", method: "post"});
                for(i = 0; i < num_exp; i++){
                    for(let j = 0; j < sim_list.length; j++){
                        let number = i + 1;
                        form.append($('<input/>', {type: 'hidden', name: 'exp1_q' + number + '_' + sim_list[j], value: answer_list[sim_list[j]][i] }));
                    }
                }
                for(let i = 0; i < num_exp; i++){
                    let number = i + 1;
                    let img_path = data_list['images'][i].split('/');
                        form.append($('<input/>', {type: 'hidden', name: 'exp1_q' + number + '_image', value: img_path[img_path.length - 1] }));
                }
                form.appendTo(document.body).submit();
            }

        }else{
            $('#warning').text('記入されていないフォームがあります。');
        }
    });
}


var caption_with_table = randamize_captions(data_list);
console.log(caption_with_table);

init(data_list);
get_all_result();



