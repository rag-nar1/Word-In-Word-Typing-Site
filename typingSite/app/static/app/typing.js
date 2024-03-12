const typingText = document.querySelector('.typing-text p');
const mistake = document.querySelector('.mistakes span b');
const timeTag = document.querySelector('.time span b');
const WPMTag = document.querySelector('.wpm span b');
const tryAgain = document.querySelector('.try');
const AccTag = document.querySelector('.Accuracy span b');
const inputField = document.querySelector('.input');
const submitButton = document.querySelector('.formdata button');
let mistakecount = 0;
let mistakes = 0;
let charIdx = 0;
let maxTime = parseInt(timeTag.innerHTML);
let currTime = maxTime; 
let timer ;
let isTyping = false;
let accuracy = 0;
let wpmm = 0;
// hash for characters from a to z 
let charCnt = { 'a': 0 , 'b': 0 , 'c': 0 , 'd': 0 , 'e': 0 , 'f': 0 , 'g': 0 , 'h': 0 , 'i': 0 , 'j': 0 , 'k': 0 , 'l': 0 , 'm': 0 , 'n': 0 , 'o': 0 , 'p': 0 , 'q': 0 , 'r': 0 , 's': 0 , 't': 0 , 'u': 0 , 'v': 0 , 'w': 0 , 'x': 0 , 'y': 0 , 'z': 0 };
let charMiss = { 'a': 0 , 'b': 0 , 'c': 0 , 'd': 0 , 'e': 0 , 'f': 0 , 'g': 0 , 'h': 0 , 'i': 0 , 'j': 0 , 'k': 0 , 'l': 0 , 'm': 0 , 'n': 0 , 'o': 0 , 'p': 0 , 'q': 0 , 'r': 0 , 's': 0 , 't': 0 , 'u': 0 , 'v': 0 , 'w': 0 , 'x': 0 , 'y': 0 , 'z': 0 };
inputField.focus();
let specialchar = []
let last_space = [-1];
// console.log(AccTag.innerHTML);
// get random paragraph
function randomParagraph(){
    let text = typingText.innerHTML;
    typingText.innerHTML = '';
    text = text.split(' ');
    // console.log(text);
    let charcount = 0;
    for(let i = 0; i < text.length; i++){
        if(charcount + text[i].length > 52){
            typingText.innerHTML += '<br>';
            charcount = 0;
        }
        for(let j = 0; j < text[i].length; j++){
            typingText.innerHTML += `<span>${text[i][j]}</span>`;
        }
        if(i < text.length - 2){
            typingText.innerHTML += '<span> </span>';
        }
        charcount += text[i].length + 1;
    }
    typingText.innerHTML += '<span>.</span>';
    
    
    // alabama amazing advisor aware angel bizrate bench bobby 
    document.addEventListener('keydown', () => {inputField.focus()})
    typingText.addEventListener('click', () => {inputField.focus()})
}


function submitData(){
    submitButton.click();
}

// calculate WPM
function calcWPM(characterscnt , currTime , mistakes){
    let wpm = (characterscnt - mistakes) / 5;
    wpm = wpm / (maxTime - currTime) * 60;
    if(wpm < 0 || wpm === Infinity || wpm == 0)
    wpm = 0;
    wpmm = Math.floor(wpm);
    WPMTag.innerHTML = Math.floor(wpm);
}

// calculate accuracy
function calcAccuracy(characterscnt , mistakes){
    let acc = ((characterscnt - mistakes) / characterscnt) * 100;
    if(acc < 0 || acc === Infinity || acc == 0)
    acc = 0;
    accuracy = Math.floor(acc);
    AccTag.innerHTML = Math.floor(acc);
}


// typing function
function initTyping(){
    if(inputField.getAttribute('disabled') === 'disabled'){
        return;
    }
    const characters = typingText.querySelectorAll('span');
    let typedChar = inputField.value.split('')[0];
    if(!isTyping){
        timer = setInterval(countdown, 1000);
        isTyping = true;
    }
    if(specialchar.length > 0){
        if(specialchar.length == 1 && specialchar[0] === 'Control') return;
        if(specialchar.length == 1 && specialchar[0] === 'Backspace'){
            if(charIdx === 0) return;
            if(characters[charIdx].classList.contains('wrong')){
                characters[charIdx].classList.remove('wrong' , 'wasWrong', 'alt');
                characters[charIdx].classList.add('wasWrong');
                mistakecount--;
                specialchar = [];
                return;
            }
            characters[charIdx].classList.remove('currChar');
            charIdx--;
            characters[charIdx].classList.remove('wrong' , 'correct' , 'alt');
            characters[charIdx].classList.add('currChar');
            mistake.innerHTML = mistakecount;
        }
        else if(specialchar.length == 2 && specialchar[0] === 'Control' && specialchar[1] === 'Backspace'){
            let lastS = last_space[last_space.length - 1];
            for(let i = charIdx; i > lastS ; i--){
                if(characters[i].classList.contains('wrong' , 'wasWrong' , 'alt')){
                    mistakecount--;
                    mistakes--;
                }
                characters[i].classList.remove('currChar' , 'wrong' , 'correct' , 'alt');
            }
            charIdx = lastS + 1;
            characters[charIdx].classList.add('currChar');
            mistake.innerHTML = mistakecount;
        }
        specialchar = [];
        return;
    }
    let correct = false;
    console.log(typedChar);
    console.log(characters[charIdx].innerText);
    console.log('\n')
    if(typedChar === characters[charIdx].innerText){
        if(typedChar === ' '){
            last_space.push(charIdx);
        }
        if(characters[charIdx].classList.contains('wasWrong')){
            characters[charIdx].classList.add('alt');
        }
        else 
            characters[charIdx].classList.add('correct');
        if(typedChar in charCnt){
            charCnt[typedChar]++;
        }
        correct = true;
        if(characters[charIdx].classList.contains('wrong')){
            characters[charIdx].classList.remove('wrong');
        }
        if(characters[charIdx].classList.contains('wasWrong')){
            characters[charIdx].classList.remove('wasWrong');
        }
    }else{
        if(characters[charIdx].innerHTML in charMiss){
            charMiss[characters[charIdx].innerHTML]++;
        }
        if(characters[charIdx].classList.contains('wrong')){
            mistakecount--;
            mistakes--;
        }
        mistakecount++;
        mistakes++;
        characters[charIdx].classList.add('wrong' , 'wasWrong');
        if(characters[charIdx].innerHTML in charMiss){
            charMiss[characters[charIdx].innerHTML]++;
        }
    }
    mistake.innerHTML = mistakecount;
    if(correct){
        characters[charIdx].classList.remove('currChar');
        charIdx++;
    }
    if(charIdx === characters.length){
        inputField.setAttribute('disabled', 'disabled');
        clearInterval(timer);
        submitData();
        return;
    }
    characters[charIdx].classList.add('currChar');
    inputField.value = '';
}

// countdown timer
function countdown(){
    if(currTime > 0){
        currTime--;
        timeTag.innerHTML = currTime;
    }else{
        inputField.setAttribute('disabled', 'disabled');
        clearInterval(timer);
        submitData();
    }
    calcWPM(charIdx + 1 , currTime , mistakecount);
    calcAccuracy(charIdx + 1 , mistakes);
    // console.log(mistakes);
}


// try again button
tryAgain.addEventListener('click', () => {
    window.location.reload()
});


// get random paragraph
randomParagraph();
// input event listener
inputField.addEventListener('keydown', function(e){
    if(e.key === 'Control' || e.key === 'Backspace'){
        specialchar.push(e.key);
        initTyping();
    }
});
inputField.addEventListener('input', initTyping);