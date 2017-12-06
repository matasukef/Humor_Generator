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
        if(counter < num_exp){
            img.src = img_list[counter];
            render();

            counter += 1;
        }else{
            console.log("finish");
        }
    });
    
    img.addEventListener('load', render, false);
    window.addEventListener('resize', render, false);
}

var show_caption = function(captions, target){
    first_cap = captions[0];
    $(target).text(first_cap);

    var cap_counter = 0;
    $('#submit').on('click', function(){
        if(cap_counter < num_exp){
            cap_counter += 1;
            cap = captions[cap_counter];
            $(target).text(cap);
            
        }
    });
}

var show_progress = function(num){
    first_ratio = 100 / num;
    $('.progress-bar').css('width', first_ratio + '%');
    $('.progress-bar').text('1/' + num);

    var progress_counter = 1;
    $('#submit').on('click', function(){
        if(progress_counter < num){
            progress_counter += 1;
            ratio = (progress_counter / num) * 100;
            $('.progress-bar').css('width', ratio + '%');
            $('.progress-bar').text(progress_counter + '/' + num);
        }
    });
}

var check_state = function(target_name){
    //var state = $('input[name=' + target_name + ']').val();
    var state = $("[name=" + target_name + "]").prop("checked");
    return state;
}

var clear_checked = function(target_name){
    $('input[name=' + target_name + ']').prop('checked', false);
    $('.btn').removeClass('active');
}

var get_result = function(target_name){
    if(check_state(target_name)){
        var res = $('input[name=' + target_name + ']:checked').val();
        clear_checked(target_name);
        return res;
    }else{
        console.log('not selected');
        return 'false';
    }

}

var get_all_result = function(){
    $('#submit').on('click', function(){
        res1 = get_result('exp1_q1');
        res2 = get_result('exp1_q2');
        console.log(res1);
        console.log(res2);
    });
}


show_image(img_list);
show_caption(cap_list, '.caption1');
show_caption(humor_cap_list, '.caption2');
show_progress(num_exp);
get_all_result();
