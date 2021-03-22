const __facingMode = webcam._facingMode
const __webcamElement = webcam._webcamElement
const __canvasElement = document.getElementById('canvas');
const __mImage = document.getElementById('detected_img');
var intervl = 0;
var tempData = 0
var __labels = { 0:'Apple', 1:"Banana", 2:"Orange" }
const minScore = 0.5
var pause = 1


placeholder_img = 'data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAOEAAADhCAMAAAAJbSJIAAAAA1BMVEUBAQHIpFY6AAAASElEQVR4nO3BgQAAAADDoPlTX+AIVQEAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAADwDcaiAAFXD1ujAAAAAElFTkSuQmCC'


function startMirror(){ 

    if(__canvasElement!=null){ 

            __canvasElement.height = __webcamElement.scrollHeight;
            __canvasElement.width = __webcamElement.scrollWidth;
            let context = __canvasElement.getContext('2d');
            if(__facingMode == 'user'){
                context.translate(__canvasElement.width, 0);
                context.scale(-1, 1);
            }
            context.clearRect(0, 0, __canvasElement.width, __canvasElement.height);
            context.drawImage(__webcamElement, 0, 0, __canvasElement.width, __canvasElement.height);
            let data = __canvasElement.toDataURL('image/jpg',0.1);
            
            return data;
        }
        else{
            throw "canvas element is missing";
        }
}


function startMirroring(){
    
    $(__mImage).removeClass('d-none');

    img = startMirror();

    if(!pause){
        ajx(img);
    }    
    // resizeBase64Img(img, 400, 400).then((newImg)=>{
    //     ajx(newImg);
    //     $(__mImage).attr("src",newImg);
    // });
        
}


function ajx( imgd ){
    
    var arr = { img : imgd };

    $.ajax({
            url: 'https://api.aspiringcvengineer.xyz:5000/predict',
            method: 'POST',
            data: JSON.stringify(arr),
            crossDomain: true,
            contentType: 'application/json; charset=utf-8',
            dataType: 'json',
            success: function(data) {
                tempData = data
                if (data && data.code == 200 ){

                    draeRectangle(imgd , JSON.parse(data.data))

                    if(!pause){
                        startMirroring()        
                    }    

                }
            }
    
        });
}


function draeRectangle(imgd, data){

    // h = __webcamElement.scrollHeight;
    // w = __webcamElement.scrollWidth;

    var p_canvas = document.createElement("canvas");
    let ctx = p_canvas.getContext('2d');

    var image = new Image();
    image.onload = function() {

        h = this.height;
        w = this.width;
        
        p_canvas.width = w;
        p_canvas.height = h;

        // ctx.translate(w, 0);
        // ctx.scale(-1, 1);
        ctx.drawImage(image, 0, 0);
        ctx.beginPath();
        ctx.fillStyle = "red";
        ctx.font = "16px Arial";
        for(var i=0; i<data.detection_scores[0].length;i++){
            if(data.detection_scores[0][i]>minScore){
                r = data.detection_boxes[0][i]
                ctx.fillText(__labels[data.detection_classes[0][i]], r[0]*w-7, r[1]*h-7);
                ctx.rect(r[0]*w, r[1]*h, r[2]*w, r[3]*h);
            }
            
        }

        ctx.lineWidth = 3;
        ctx.strokeStyle = 'green';
        ctx.stroke();
        __mImage.src = p_canvas.toDataURL('image/jpg',1);
        $(__mImage).height(h).width(w)
        
    };
    image.src = imgd;
    
}


function startDetection(){
    pause = 0;
    $(__mImage).attr('src',placeholder_img);
    // intervl = setInterval(startMirroring, 10000);
    setTimeout(startMirroring, 1000);

}


function stopDetection(){
    pause = 1;
    $(__mImage).addClass('d-none');
    if (intervl){
        clearInterval(intervl)
    }    
}


function resizeBase64Img(base64, newWidth, newHeight) {
    return new Promise((resolve, reject)=>{
        var canvas = document.createElement("canvas");
        canvas.style.width = newWidth.toString()+"px";
        canvas.style.height = newHeight.toString()+"px";
        let context = canvas.getContext("2d");
        let img = document.createElement("img");
        img.src = base64;
        img.onload = function () {
            context.scale(newWidth/img.width,  newHeight/img.height);
            context.drawImage(img, 0, 0); 
            resolve(canvas.toDataURL('image/jpg'));               
        }
    });
}