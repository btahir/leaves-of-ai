var el = x => document.getElementById(x);
var textData = "";

function showPicker(inputId) { el('file-input').click(); }

function showPicked(input) {
    el('upload-label').innerHTML = input.files[0].name;
    var reader = new FileReader();
    reader.onload = function (e) {
        el('image-picked').src = e.target.result;
        el('image-picked').className = '';
    }
    reader.readAsDataURL(input.files[0]);
}

function showText(input) {
    textData = String(input.value);
    var reader = new FileReader();
    reader.onload = function (e) {
        el('text-input').src = e.target.result;
        el('text-input').className = '';
    }    
}

function analyze() {
    // console.log(textData);
    // var uploadFiles = el('file-input').files;
    // if (uploadFiles.length != 1) alert('Please select 1 file to analyze!');

    el('analyze-button').innerHTML = 'Generating...';
    el('result-label').innerHTML = 'Please refresh and try again if nothing shows up after a few minutes.'
    var xhr = new XMLHttpRequest();
    var loc = window.location
    xhr.open('POST', `${loc.protocol}//${loc.hostname}:${loc.port}/analyze`, true);
    xhr.onerror = function() {alert (xhr.responseText);}
    xhr.onload = function(e) {
        if (this.readyState === 4) {
            var response = JSON.parse(e.target.responseText);
            el('result-label').innerHTML = `${response['result']}`;
        }
        el('analyze-button').innerHTML = 'Generate Poem';
    }

    var fileData = new FormData();
    fileData.append('file', textData);
    xhr.send(fileData);
}
