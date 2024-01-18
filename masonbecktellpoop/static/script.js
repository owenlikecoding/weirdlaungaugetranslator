var sentenceInput = document.getElementById('sentenceInput');
var translateButton = document.getElementById('translateButton');
var translationResult = document.getElementById('translationResult');

translateButton.addEventListener('click', translate);

function translate() {
    var sentence = document.getElementById('sentenceInput').value;
    fetch('/translate', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ sentence: sentence }),
    })
        .then(response => response.json())
        .then(data => {
            document.getElementById('translationResult').innerText = data.translated;
        })
        .catch(error => console.error('Error:', error));
}