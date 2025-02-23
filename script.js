const questions = [
    "나는 업무에서 완벽을 추구하는 편이다.",
    "나는 동료들과 적극적으로 소통하는 것을 좋아한다.",
    "나는 새로운 업무를 배우는 것에 열정적이다.",
    "나는 계획대로 일을 진행하는 것을 선호한다.",
    "나는 창의적인 해결방안을 제시하는 것을 좋아한다.",
    "나는 팀 프로젝트에서 리더역할을 선호한다.",
    "나는 혼자 일하는 것을 더 편하게 느낀다.",
    "나는 마감시간을 철저히 지키는 편이다.",
    "나는 업무 스트레스를 잘 관리하는 편이다.",
    "나는 변화하는 환경에 잘 적응하는 편이다.",
    "나는 동료의 일도 기꺼이 도와주는 편이다.",
    "나는 업무에서 실수하는 것을 극도로 두려워한다.",
    "나는 회사의 규칙과 절차를 잘 따르는 편이다.",
    "나는 업무 관련 결정을 빠르게 내리는 편이다.",
    "나는 비판이나 피드백을 잘 수용하는 편이다.",
    "나는 어려운 상황에서도 긍정적인 태도를 유지한다.",
    "나는 업무시간 외 개인시간을 잘 지키는 편이다.",
    "나는 새로운 아이디어를 자주 제안하는 편이다.",
    "나는 갈등 상황을 잘 중재하는 편이다.",
    "나는 업무에서 세세한 부분까지 신경 쓰는 편이다."
];

let currentQuestion = 0;
let answers = [];

const personalityTypes = {
    "완벽주의형": "세세한 것까지 꼼꼼하게 챙기며 높은 기준을 가지고 있습니다.",
    "리더형": "결단력이 있고 팀을 이끄는데 탁월한 능력을 보입니다.",
    "협력형": "타인과의 협업을 즐기며 원만한 인간관계를 유지합니다.",
    "창의형": "새로운 아이디어를 내고 혁신적인 해결책을 제시합니다.",
    "분석형": "논리적이고 체계적으로 문제를 해결합니다."
};

function startTest() {
    document.getElementById('start-page').style.display = 'none';
    document.getElementById('question-page').style.display = 'block';
    showQuestion();
}

function showQuestion() {
    document.getElementById('question-text').textContent = 
        `Q${currentQuestion + 1}. ${questions[currentQuestion]}`;
    document.getElementById('progress').style.width = 
        `${((currentQuestion + 1) / questions.length) * 100}%`;
}

function selectAnswer(value) {
    answers.push(value);
    
    if (currentQuestion < questions.length - 1) {
        currentQuestion++;
        showQuestion();
    } else {
        showResult();
    }
}

function showResult() {
    document.getElementById('question-page').style.display = 'none';
    document.getElementById('result-page').style.display = 'block';
    
    const type = calculatePersonalityType();
    document.getElementById('result-type').textContent = type;
    document.getElementById('result-description').textContent = personalityTypes[type];
}

function calculatePersonalityType() {
    const sum = answers.reduce((a, b) => a + b, 0);
    
    if (sum < 40) return "완벽주의형";
    else if (sum < 60) return "리더형";
    else if (sum < 80) return "협력형";
    else if (sum < 100) return "창의형";
    else return "분석형";
}

function restartTest() {
    currentQuestion = 0;
    answers = [];
    document.getElementById('result-page').style.display = 'none';
    document.getElementById('start-page').style.display = 'block';
}

