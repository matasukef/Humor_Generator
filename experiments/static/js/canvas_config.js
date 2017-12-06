var exp_img = $('#exp_img').children('a');
var list_href = []
for(var i = 0; i < exp_img.length; i++){
    list_href.push(exp_img[i]['href']);
}

var parent = document.getElementById('canvas-container');
var canvas = document.getElementById('canvas');
var ctx = canvas.getContext('2d');
var isInit = false;
var img = new Image();
img.src = exp_img[0];

var render = function(){
    var scale = 0;
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
        var mag = canvas_height/img_height;
    }else{
        var mag = canvas_width/img_width;
    }

    var resized_height = img_height * mag;
    var resized_width = img_width * mag;
    
    ctx.fillStyle = "black";
    ctx.fillRect(0, 0, canvas_width, canvas_height);
    
    if(resized_height > resized_width){
        var center = canvas_width/2 - resized_width/2;
        ctx.drawImage(img, center, 0, resized_width, resized_height);
    }else{
        var center = canvas_height/2 - resized_height/2;
        ctx.drawImage(img, 0, center, resized_width, resized_height);
    }
}


var main = function(){
    img.addEventListener('load', render, false);
    window.addEventListener('resize', render, false);
}

main();

