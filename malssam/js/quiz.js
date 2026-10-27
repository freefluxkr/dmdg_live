// ============================================================
// ⚔️ [듀얼 세대 공감 배틀 퀴즈 엔진]
// ============================================================
let currentQuizMode = 'parent'; // 'parent' (MZ밈 맞히기) or 'retro' (라떼 맞히기)
let dynamicQuizList = [];
let currentQuizIndex = 0;
let quizScore = 0;

function startQuiz(mode) {
  currentQuizMode = mode || 'parent';
  const badge = document.getElementById('quizModeBadge');
  if (currentQuizMode === 'parent') {
    if (badge) {
      badge.innerText = "👔 부모·팀장님 모드 (2026 최신 밈)";
      badge.style.background = "rgba(236, 72, 153, 0.2)";
      badge.style.color = "#f472b6";
    }
  } else {
    if (badge) {
      badge.innerText = "🎧 자녀·신입사원 모드 (라떼 역주행)";
      badge.style.background = "rgba(56, 189, 248, 0.2)";
      badge.style.color = "#38bdf8";
    }
  }

  dynamicQuizList = generateBattleQuiz(currentQuizMode);
  currentQuizIndex = 0;
  quizScore = 0;

  const qModal = document.getElementById('quizModal');
  if (qModal) qModal.classList.add('active');
  const qPlay = document.getElementById('quizPlayView');
  if (qPlay) qPlay.style.display = 'block';
  const qRes = document.getElementById('quizResultView');
  if (qRes) qRes.style.display = 'none';
  renderQuizStep();
}

function restartCurrentQuiz() {
  startQuiz(currentQuizMode);
}

function closeQuizModal() {
  const qModal = document.getElementById('quizModal');
  if (qModal) qModal.classList.remove('active');
}

function generateBattleQuiz(mode) {
  let pool = [];
  if (!window.words) return [];
  if (mode === 'parent') {
    pool = window.words.filter(w => w.era === 'shorts');
  } else {
    pool = window.words.filter(w => w.era === 'latte' || w.era === 'smartphone');
  }

  const shuffled = [...pool].sort(() => 0.5 - Math.random()).slice(0, 5);

  return shuffled.map(w => {
    let wrongOptions = window.words
      .filter(item => item.id !== w.id)
      .sort(() => 0.5 - Math.random())
      .slice(0, 3)
      .map(item => item.short_def);

    while (wrongOptions.length < 3) {
      wrongOptions.push("전혀 상관없는 엉뚱한 뜻입니다.");
    }

    let allOpts = [w.short_def, ...wrongOptions].sort(() => 0.5 - Math.random());
    let correctIdx = allOpts.indexOf(w.short_def);

    return {
      word: w.word,
      eraName: w.era_name || (w.era === 'latte' ? '1990s 라떼' : '2026 밈'),
      correctDef: w.short_def,
      example: (w.examples && w.examples[0]) ? w.examples[0].replace(/\n/g, ' / ') : "실전 용례 없음",
      standard: w.standard_korean_mapping || "대응 표준어 없음",
      options: allOpts,
      answer: correctIdx
    };
  });
}

function renderQuizStep() {
  if (currentQuizIndex >= dynamicQuizList.length) {
    showQuizResult();
    return;
  }

  const q = dynamicQuizList[currentQuizIndex];
  const stepText = document.getElementById('quizStepText');
  if (stepText) stepText.innerText = `Q${currentQuizIndex + 1} / 5문항`;
  const progFill = document.getElementById('quizProgressFill');
  if (progFill) progFill.style.width = `${((currentQuizIndex + 1) / 5) * 100}%`;
  const qWord = document.getElementById('quizWord');
  if (qWord) qWord.innerText = `'${q.word}'`;
  const qEx = document.getElementById('quizExample');
  if (qEx) qEx.innerText = `[맥락 힌트] ${q.example}`;

  const container = document.getElementById('quizOptionsContainer');
  if (!container) return;
  container.innerHTML = "";

  q.options.forEach((opt, idx) => {
    const btn = document.createElement('button');
    btn.className = 'quiz-opt-btn';
    btn.innerText = `${idx + 1}. ${opt}`;
    btn.onclick = () => selectQuizAnswer(idx);
    container.appendChild(btn);
  });
}

function selectQuizAnswer(selectedIdx) {
  const q = dynamicQuizList[currentQuizIndex];
  const btns = document.querySelectorAll('.quiz-opt-btn');

  btns.forEach((b, idx) => {
    b.disabled = true;
    if (idx === q.answer) {
      b.classList.add('correct');
    }
    if (idx === selectedIdx && selectedIdx !== q.answer) {
      b.classList.add('wrong');
    }
  });

  if (selectedIdx === q.answer) {
    quizScore += 20;
    showToast("🎉 정답입니다! +20점");
  } else {
    showToast("😅 아쉽게 오답입니다!");
  }

  setTimeout(() => {
    currentQuizIndex++;
    renderQuizStep();
  }, 1100);
}

function showQuizResult() {
  const playV = document.getElementById('quizPlayView');
  if (playV) playV.style.display = 'none';
  const resV = document.getElementById('quizResultView');
  if (resV) resV.style.display = 'block';

  const scoreText = document.getElementById('quizScoreText');
  if (scoreText) scoreText.innerText = `${quizScore}점`;
  const gradeText = document.getElementById('quizGradeText');
  const descText = document.getElementById('quizResultDesc');

  if (quizScore === 100) {
    if (gradeText) gradeText.innerText = "👑 LV.99 세대 소통 마스터";
    if (descText) descText.innerText = "완벽합니다! 당신은 Z세대와 라떼 세대를 완벽히 잇는 소통의 신입니다.";
  } else if (quizScore >= 80) {
    if (gradeText) gradeText.innerText = "🥇 LV.80 센스만점 트렌드 리더";
    if (descText) descText.innerText = "대부분의 맥락을 이해하고 계시네요! 조직 내 소통에 전혀 문제없습니다.";
  } else if (quizScore >= 60) {
    if (gradeText) gradeText.innerText = "🥈 LV.60 소통 성장기";
    if (descText) descText.innerText = "조금만 더 관심을 기울이면 완벽한 세대 통합이 가능합니다!";
  } else {
    if (gradeText) gradeText.innerText = "🥉 LV.40 단절 경보 발령";
    if (descText) descText.innerText = "상대방의 언어를 조금 더 배워볼 필요가 있습니다! 말쌈 사전으로 특훈해 보세요.";
  }
}

// 티어 선택 모달
let selectedTier = 1; // 1: 개인용 1,000원, 2: 기업 B2B 9,900원

function openTierModal() {
  const tm = document.getElementById('tierModal');
  if (tm) tm.classList.add('active');
}

function selectTier(tierNum) {
  selectedTier = tierNum;
  document.getElementById('tierCard1').classList.toggle('active', tierNum === 1);
  document.getElementById('tierCard2').classList.toggle('active', tierNum === 2);
}

function closeTierModal() {
  const tm = document.getElementById('tierModal');
  if (tm) tm.classList.remove('active');
}

function getTierInfo() {
  if (selectedTier === 2) {
    return {
      name: "B2B 사내 세대 갈등 진단 패키지 & 지출결의서",
      amount: 9900,
      amountText: "9,900원",
      usd: "7.99",
      usdText: "$7.99 USD",
      docs: "인쇄용 공식 고화질 PDF + 세대소통 10계명 + B2B 지출결의서"
    };
  } else {
    return {
      name: "말쌈 정식 세대소통 리포트 & 수료증",
      amount: 1000,
      amountText: "1,000원",
      usd: "0.99",
      usdText: "$0.99 USD",
      docs: "정식 인증 리포트 (인쇄/PDF 출력 지원)"
    };
  }
}
