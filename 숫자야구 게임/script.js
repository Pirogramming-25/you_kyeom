let answer = [];       // 컴퓨터가 생성한 정답 숫자 3개
let maxAttempts = 9 ;  // 총 기회
let attempts = maxAttempts; // 남은 기회
let isGameOver = false;

const attemptsDisplay = document.getElementById("attempts");
const resultsContainer = document.getElementById("results");
const resultImg = document.getElementById("game-result-img");
const inputs = [
    document.getElementById("number1"),
    document.getElementById("number2"),
    document.getElementById("number3")
];

// 기능: 게임 초기화 및 시작
function initGame() {
    attempts = maxAttempts; 
    isGameOver = false;
    
    // html의 결과창 내용 및 이미지 비우기
    attemptsDisplay.textContent = attempts;
    resultsContainer.innerHTML = "";
    resultImg.src = "";
    resultImg.style.display = "none";
    
    inputs.forEach(input => {
        input.value = "";
        input.disabled = false;
    });

    const submitBtn = document.querySelector(".submit-button");
    if (submitBtn) {
        submitBtn.disabled = false;
        submitBtn.style.backgroundColor = ""; 
        submitBtn.style.cursor = "pointer";
    }

    attemptsDisplay.parentElement.style.display = "block";

    inputs[0].focus(); 

    // 중복되지 않는 3개의 랜덤한 숫자 설정 (0 ~ 9)
    answer = [];
    while (answer.length < 3) {
        let randomNum = Math.floor(Math.random() * 10);
        if (!answer.includes(randomNum)) {
            answer.push(randomNum);
        }

    }
    
    // 테스트용 콘솔 출력 
    //console.log("새로운 정답:", answer);
}
window.onload = initGame;

inputs.forEach((input, index) => {
    input.addEventListener("input", () => {
        if (input.value.length === 1 && index < 2) {
            inputs[index + 1].focus();
        }
    });
});

function check_numbers() {
    if (isGameOver) return;

    let userInputs = inputs.map(input => input.value.trim());

    // 입력되지 않은 input이 있다면 숫자를 확인하지 않고 input 창만 비우기
    if (userInputs.some(val => val === "")) {
        alert("숫자 3개를 모두 입력해주세요!"); 
        inputs.forEach(input => input.value = ""); 
        inputs[0].focus(); 
        return; 
    }
    let userNumbers = userInputs.map(Number);

    //스트라이크, 볼 판정 계산 로직 
    let strikes = 0;
    let balls = 0;

    for (let i = 0; i < 3; i++) {
        if (userNumbers[i] === answer[i]) {
            strikes++; 
        } else if (answer.includes(userNumbers[i])) {
            balls++;   
        }
    }
    attempts--;
    attemptsDisplay.textContent = attempts;

    //결과창 띄우기(구조를 안바꾸고 영상처럼 컨테이너 양 옆에 넣는 법 모르겠습니다...)
    let resultHTML = "";

    if (strikes === 0 && balls === 0) {
        resultHTML = `
            <span></span>
            <span class="num-result out">O</span>
        `;
    } else {
        resultHTML = `
            <span>${strikes}</span><span class="num-result strike">S</span>
            <span>${balls}</span><span class="num-result ball">B</span>
        `;
    }

    resultsContainer.innerHTML += `
        <div class="check-result">
            <div class="left">${userNumbers.join(" ")}</div>
            <span>:</span>
            <div class="right">
                ${resultHTML}
            </div>
        </div>
    `;
    inputs.forEach(input => input.value = "");
    inputs[0].focus();

    if (strikes === 3) {
        endGame(true);
    } else if (attempts === 0) {
        endGame(false);
    }
}

function endGame(isWin) {
    isGameOver = true;
    
    attemptsDisplay.parentElement.style.display = "none";

    inputs.forEach(input => input.disabled = true);
    
    const submitBtn = document.querySelector(".submit-button");
    if (submitBtn) {
        submitBtn.disabled = true;
        submitBtn.style.backgroundColor = "#ccc";
        submitBtn.style.cursor = "not-allowed";
    }

    // 이미지 출력 처리
    resultImg.style.display = "block";
    
    if (isWin) {
        resultImg.src = "./success.png"; 
    } else {
        resultImg.src = "./fail.png";    
    }
}

