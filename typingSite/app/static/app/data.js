// form inputs fields 
let form = document.getElementsByClassName('formdata')


function avg( v1 , v2 ){
    v1 = parseInt(v1);
    v2 = parseInt(v2);
    return parseInt( (v1 + v2) / 2);    
}

function prepereData(data){
    if(data['accuracy'] >= 1000)
        data['accuracy'] = accuracy;
    data['accuracy'] = avg(accuracy , data['accuracy']);
    if(data['wpm'] >= 1000) 
        data['wpm'] = wpmm;
    data['wpm'] = avg(wpmm , data['wpm']);
    var curr_char = 'A';
    var atr = "accuracy";
    for(var i = 0; i < 26; i++){
        curr_charL = curr_char.toLowerCase();   
        curr_accuracy = charCnt[curr_charL] / (charCnt[curr_charL] + charMiss[curr_charL]) * 100;
        if(curr_accuracy < 0 || curr_accuracy === Infinity || curr_accuracy == 0 || isNaN(curr_accuracy))
        curr_accuracy = 0;
        // integer data of data[atr + curr_char]
        if(parseInt(data[atr + curr_char]) > 100)
            data[atr + curr_char] = curr_accuracy;
        data[atr + curr_char] = avg(curr_accuracy , parseInt(data[atr + curr_char]));
        curr_char = String.fromCharCode(curr_char.charCodeAt(0) + 1);
    }
    return data;
}


form[0].addEventListener("submit", function(e){
    e.preventDefault();
    const formData = new FormData(this);
    var csrfToken = document.querySelector('.formdata input[name="csrfmiddlewaretoken"]').value
    let data = {};
    formData.forEach((value, key) => {
        data[key] = value;
    })

    data = prepereData(data);
    data['last_accuracy'] = accuracy;
    data['last_wpm'] = wpmm;
    data['last_mistakes'] = mistakecount;

    fetch('/app/typing/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrfToken
        },
        body: JSON.stringify(data)
    })
    .then(Response => {
        console.log(Response);
        window.location.href = Response.url;
    })
})