
const vscode = acquireVsCodeApi();

function clickableOnclick(e){
    vscode.postMessage({
        title: e.target.title,
        id: e.target.id,
        value: e.target.innerHTML
    })
}

window.addEventListener(
    "load", 
    function(event) {
        var clickables =  document.getElementsByClassName("clickable");
        for(var i = 0; i < clickables.length; i++){
            clickables[i].onclick = clickableOnclick
        }
        
        clickables =  document.getElementsByClassName("btn");
        for(var i = 0; i < clickables.length; i++){
            clickables[i].onclick = clickableOnclick
        }
    }
);   

