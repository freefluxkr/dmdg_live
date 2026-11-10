# -*- coding: utf-8 -*-
import json
import os
from exam_data_22015 import EXAM_META_22015, QUESTIONS_22015
from exam_data_22036 import EXAM_META_22036, QUESTIONS_22036
from exam_data_22037 import EXAM_META_22037, QUESTIONS_22037

OUT_DIR = r"C:\DMDG_Jobs\DMDG_PRJ\dmdg_live_dot_com"
DOCS_DIR = os.path.join(OUT_DIR, "exam_docs")
os.makedirs(DOCS_DIR, exist_ok=True)


HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="ko" class="dark">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>__TITLE__ | DMDG 공인 역량 평가 & 직무 추천</title>
  <script src="https://cdn.tailwindcss.com"></script>
  <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
  <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css" rel="stylesheet">
  <style>
    @import url('https://cdn.jsdelivr.net/gh/orioncactus/pretendard/dist/web/static/pretendard.css');
    @import url('https://fonts.googleapis.com/css2?family=Fira+Code:wght@400;500;600;700&display=swap');
    body {
      font-family: 'Pretendard', -apple-system, sans-serif;
      background-color: #070b14;
      color: #f8fafc;
    }
    .code-font { font-family: 'Fira Code', monospace; }
    .glass-card {
      background: rgba(15, 23, 42, 0.88);
      backdrop-filter: blur(14px);
      border: 1px solid rgba(56, 189, 248, 0.25);
    }
    .option-btn { transition: all 0.16s ease; }
    .option-btn:hover { border-color: __ACCENT__; background: rgba(30, 41, 59, 0.95); }
    .option-btn.selected {
      border-color: __ACCENT__;
      background: rgba(16, 185, 129, 0.16);
      box-shadow: 0 0 18px rgba(56, 189, 248, 0.22);
    }
  </style>
</head>
<body class="min-h-screen flex flex-col">

  <!-- Header -->
  <header class="bg-slate-900/95 backdrop-blur-md border-b border-slate-800 sticky top-0 z-50">
    <div class="max-w-6xl mx-auto px-4 py-3 flex flex-wrap justify-between items-center gap-3">
      <div class="flex items-center gap-3">
        <div class="w-10 h-10 rounded-xl flex items-center justify-center font-black text-slate-950 shadow-lg" style="background: linear-gradient(135deg, __ACCENT__, __ACCENT_SEC__);">
          30Q
        </div>
        <div>
          <h1 class="text-base sm:text-lg font-extrabold text-white">__TITLE__</h1>
          <p class="text-xs text-slate-400">__SUBTITLE__</p>
        </div>
      </div>

      <div class="flex items-center gap-2.5 flex-wrap">
        <div id="header-timer-badge" class="hidden items-center gap-2 bg-slate-950 border border-slate-700 px-3 py-1.5 rounded-xl">
          <i class="fa-solid fa-stopwatch text-cyan-400"></i>
          <span id="timer-display" class="code-font text-sm font-extrabold text-cyan-300">01:00</span>
        </div>
        <a href="__BOOK_URL__" target="_blank" class="px-3 py-1.5 rounded-lg bg-slate-800 hover:bg-slate-700 text-xs font-bold text-slate-200 border border-slate-700">
          📘 위키독스 교안
        </a>
        <a href="__SIM_URL__" target="_blank" class="px-3 py-1.5 rounded-lg bg-slate-800 hover:bg-slate-700 text-xs font-bold text-emerald-300 border border-emerald-500/40">
          🎛️ 시뮬레이터
        </a>
        <a href="career_aces.html" class="px-3 py-1.5 rounded-lg text-xs font-extrabold text-slate-950" style="background: linear-gradient(135deg, __ACCENT__, __ACCENT_SEC__);">
          🏆 A.C.E.S 종합 직무진단
        </a>
      </div>
    </div>
  </header>

  <main class="max-w-5xl w-full mx-auto px-4 py-7 flex-1">

    <!-- VIEW 1: START SCREEN -->
    <section id="view-start" class="glass-card rounded-2xl p-6 sm:p-8 space-y-6">
      <div class="flex flex-wrap justify-between items-start gap-4 border-b border-slate-800 pb-5">
        <div>
          <span class="inline-block px-2.5 py-1 rounded-full text-[11px] font-extrabold mb-2" style="background: rgba(56,189,248,0.16); color: __ACCENT__; border: 1px solid __ACCENT__;">
            DMDG OFFICIAL CERTIFICATION · 30 QUESTIONS + JOB MATCHING
          </span>
          <h2 class="text-2xl font-black text-white">실전 변별력 30문항 역량 평가 &amp; 직무 추천 평가지표</h2>
          <p class="text-sm text-slate-300 mt-1">
            5대 핵심 영역(각 6문항, 총 30문항)을 응시하면 <b>자동 채점 결과(PASS 80점 기준)</b>와 함께
            <b>DMDG A.C.E.S 6대 역량 레이더 차트 · 1~3순위 최적 추천 직무 · SHAP 강점/보완 분석</b>을 즉시 산출합니다.
          </p>
        </div>
      </div>

      <!-- Domain Overview Grid -->
      <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-3" id="category-cards"></div>

      <!-- User Info & Mode Settings -->
      <div class="bg-slate-950/80 border border-slate-800 rounded-xl p-5 space-y-4">
        <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div>
            <label class="block text-xs font-bold text-slate-300 mb-1.5">응시자 성명</label>
            <input type="text" id="input-student-name" placeholder="예: 홍길동 (미입력 시 '학습자')" class="w-full bg-slate-900 border border-slate-700 rounded-xl px-4 py-2.5 text-sm text-white focus:outline-none focus:border-cyan-400">
          </div>
          <div>
            <label class="block text-xs font-bold text-slate-300 mb-1.5">응시 모드 선택</label>
            <select id="select-exam-mode" class="w-full bg-slate-900 border border-slate-700 rounded-xl px-4 py-2.5 text-sm text-white focus:outline-none focus:border-cyan-400">
              <option value="timed">⏱️ 실전 공인 모드 (문항당 60초 제한 · 보기 셔플)</option>
              <option value="practice">📖 자유 학습 모드 (시간 제한 없음 · 보기 셔플)</option>
            </select>
          </div>
        </div>

        <div class="flex flex-wrap gap-3 pt-2">
          <button onclick="startExam('ALL')" class="flex-1 min-w-[220px] py-3.5 px-6 rounded-xl font-black text-slate-950 text-sm shadow-lg transition hover:brightness-110" style="background: linear-gradient(135deg, __ACCENT__, __ACCENT_SEC__);">
            🚀 전체 30문항 실전 시험 &amp; 직무 추천 시작하기
          </button>
          <button onclick="showSampleResult()" class="py-3.5 px-5 rounded-xl font-bold text-xs bg-slate-800 hover:bg-slate-700 text-cyan-300 border border-cyan-500/40 transition">
            📊 직무 추천 평가지표 결과 미리보기 (샘플)
          </button>
        </div>
      </div>
    </section>

    <!-- VIEW 2: EXAM IN PROGRESS -->
    <section id="view-exam" class="hidden glass-card rounded-2xl p-6 sm:p-8 space-y-5">
      <div class="flex justify-between items-center text-xs text-slate-400">
        <span id="exam-progress-text" class="code-font font-bold text-cyan-300">문항 1 / 30</span>
        <span id="exam-category-badge" class="px-2.5 py-1 rounded-md bg-slate-800 text-emerald-300 font-bold"></span>
      </div>
      <div class="w-full bg-slate-800 h-2 rounded-full overflow-hidden">
        <div id="exam-progress-bar" class="h-full transition-all duration-300" style="width: 3%; background: linear-gradient(90deg, __ACCENT__, __ACCENT_SEC__);"></div>
      </div>

      <div class="space-y-4">
        <div class="flex items-center gap-2">
          <span id="q-chapter-badge" class="px-2 py-0.5 rounded bg-indigo-500/20 text-indigo-300 text-xs font-bold border border-indigo-500/30"></span>
          <span id="q-diff-badge" class="px-2 py-0.5 rounded bg-amber-500/20 text-amber-300 text-xs font-bold border border-amber-500/30"></span>
        </div>
        <h2 id="q-title" class="text-lg sm:text-xl font-bold text-white leading-relaxed"></h2>
        <pre id="q-code" class="hidden bg-slate-950 border border-slate-800 rounded-xl p-4 text-xs text-cyan-200 code-font overflow-x-auto leading-relaxed"></pre>

        <div id="q-options" class="grid grid-cols-1 gap-3 pt-2"></div>
      </div>

      <div class="flex justify-between items-center pt-4 border-t border-slate-800">
        <span class="text-xs text-slate-400">정답 선택 후 [다음 문항]을 클릭하세요.</span>
        <button onclick="nextQuestion()" id="btn-next-q" class="px-6 py-2.5 rounded-xl font-extrabold text-sm text-slate-950 transition hover:brightness-110" style="background: linear-gradient(135deg, __ACCENT__, __ACCENT_SEC__);">
          다음 문항 ➔
        </button>
      </div>
    </section>

    <!-- VIEW 3: RESULT + JOB RECOMMENDATION BENCHMARK DASHBOARD -->
    <section id="view-result" class="hidden space-y-6">
      <!-- Score & Readiness Card -->
      <div class="glass-card rounded-2xl p-6 sm:p-8 space-y-6">
        <div class="flex flex-wrap justify-between items-center gap-4 border-b border-slate-800 pb-5">
          <div>
            <span class="text-xs font-bold text-cyan-300 code-font">OFFICIAL ASSESSMENT &amp; A.C.E.S CAREER REPORT</span>
            <h2 class="text-2xl font-black text-white mt-1"><span id="res-student-name">응시자</span>님의 역량 평가 및 직무 추천 리포트</h2>
          </div>
          <div class="flex items-center gap-4">
            <div class="text-right">
              <div class="text-xs text-slate-400">100점 환산 점수</div>
              <div class="text-3xl font-black code-font" style="color: __ACCENT__;"><span id="res-score-100">0</span>점</div>
              <div id="res-correct-count" class="text-xs text-slate-300"></div>
            </div>
            <span id="res-pass-badge" class="px-3.5 py-1.5 rounded-full text-xs font-extrabold"></span>
          </div>
        </div>

        <!-- Area Breakdown -->
        <div>
          <h3 class="text-sm font-bold text-slate-200 mb-3">📊 5대 핵심 영역별 정답률</h3>
          <div id="res-area-bars" class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-5 gap-3"></div>
        </div>

        <!-- DMDG A.C.E.S 6-Axis Radar + Top 3 Job Recommendation -->
        <div class="bg-slate-950/90 border border-slate-800 rounded-2xl p-5 sm:p-6 space-y-5">
          <div class="flex flex-wrap justify-between items-center gap-2">
            <div>
              <span class="px-2 py-0.5 rounded bg-cyan-500/20 text-cyan-300 text-[11px] font-extrabold">DMDG A.C.E.S 6대 직무 역량 평가지표</span>
              <h3 class="text-lg font-black text-white mt-1">🏆 직무 추천 평가지표 &amp; 6대 육각형 역량 레이더</h3>
            </div>
            <a id="btn-send-aces" href="career_aces.html" class="px-4 py-2 rounded-xl text-xs font-extrabold text-slate-950 shadow-lg transition hover:brightness-110" style="background: linear-gradient(135deg, #38bdf8, #10b981);">
              🚀 A.C.E.S 종합 직무진단에 이 성적 연동하기 ➔
            </a>
          </div>

          <div class="grid grid-cols-2 sm:grid-cols-6 gap-2.5 text-center" id="res-aces-6kpi"></div>

          <div class="grid grid-cols-1 lg:grid-cols-2 gap-6 items-center">
            <div class="bg-slate-900/80 border border-slate-800 rounded-xl p-4 h-[320px]">
              <canvas id="radarChart"></canvas>
            </div>
            <div class="space-y-3" id="res-job-cards"></div>
          </div>

          <!-- SHAP XAI Analysis -->
          <div class="grid grid-cols-1 md:grid-cols-2 gap-4 bg-slate-900/70 border border-slate-800 rounded-xl p-4 text-xs leading-relaxed">
            <div>
              <div class="font-extrabold text-emerald-400 mb-1.5">🌟 직무 추천을 견인한 핵심 강점 (SHAP +)</div>
              <div id="res-shap-plus" class="text-slate-300 space-y-1"></div>
            </div>
            <div>
              <div class="font-extrabold text-amber-400 mb-1.5">💡 커리어 확장을 위한 보완 권장 영역</div>
              <div id="res-shap-minus" class="text-slate-300 space-y-1"></div>
            </div>
          </div>
        </div>

        <div class="flex flex-wrap gap-3">
          <button onclick="retakeExam()" class="px-5 py-2.5 rounded-xl bg-slate-800 hover:bg-slate-700 text-xs font-bold text-white border border-slate-700">
            🔄 다시 응시하기
          </button>
          <button onclick="filterReview('all')" class="px-4 py-2.5 rounded-xl bg-indigo-600/30 hover:bg-indigo-600/50 text-xs font-bold text-indigo-200 border border-indigo-500/40">
            전체 30문항 해설 보기
          </button>
          <button onclick="filterReview('wrong')" class="px-4 py-2.5 rounded-xl bg-rose-600/25 hover:bg-rose-600/45 text-xs font-bold text-rose-200 border border-rose-500/40">
            오답 문항만 모아보기
          </button>
        </div>
      </div>

      <!-- Detailed Question-by-Question Review -->
      <div id="res-review-list" class="space-y-4"></div>
    </section>

  </main>

  <script>
    const EXAM_META = __META_JSON__;
    const RAW_QUESTIONS = __QUESTIONS_JSON__;

    // A.C.E.S 6대 IT/AI 직무 벤치마크 [수학, SW코딩, 데이터인프라, GenAI, 비즈니스기획, 아키텍처]
    const JOBS = [
      { name: "AI 데이터 엔지니어 (Lakehouse)", scores: [70, 80, 95, 60, 50, 72], desc: "대용량 분산 레이크하우스(Kafka, HDFS, Hive), 실시간 스트림 정제 및 파이프라인 총괄" },
      { name: "MLOps / LLMOps 엔지니어", scores: [65, 82, 90, 78, 55, 75], desc: "FastMCP 인프라, 컨테이너 오케스트레이션, LoRA 무중단 서빙 및 모니터링 최적화" },
      { name: "GenAI 풀스택 / 에이전트 개발자", scores: [60, 92, 65, 90, 68, 75], desc: "GraphRAG, Standalone MCP Client, 지속 메모리 기반 자율 AI 에이전트 개발" },
      { name: "AI 모델 연구원 (Core Research)", scores: [94, 85, 60, 72, 45, 70], desc: "Unsloth QLoRA/DPO 모델 정렬, 파괴적 망각(EWC) 극복 및 심층신경망(DNN) 연구" },
      { name: "AI 솔루션 아키텍트 / 테크 PM", scores: [55, 68, 70, 75, 92, 88], desc: "엔터프라이즈 컴플라이언스·보안 아키텍처 설계 및 AI ROI 전략 수립" },
      { name: "온디바이스 / 엣지 AI 엔지니어", scores: [85, 90, 72, 60, 48, 68], desc: "실시간 차량 센서 추론 엔진 및 4-bit 양자화 소형 모델(SLM) 경량 최적화" }
    ];

    let session = null;
    let selectedOptionOrigIdx = null;
    let timerId = null;
    let radarChart = null;
    let lastDetails = [];

    function shuffleArray(arr) {
      const a = arr.slice();
      for (let i = a.length - 1; i > 0; i--) {
        const j = Math.floor(Math.random() * (i + 1));
        [a[i], a[j]] = [a[j], a[i]];
      }
      return a;
    }

    function initStartView() {
      const wrap = document.getElementById("category-cards");
      wrap.innerHTML = EXAM_META.categories.map((cat, idx) => {
        const cnt = RAW_QUESTIONS.filter(q => q.category === cat).length;
        return `
          <div class="bg-slate-950/75 border border-slate-800 rounded-xl p-4 flex flex-col justify-between gap-2">
            <div>
              <div class="text-[11px] code-font font-bold text-cyan-400">PART ${idx + 1} · ${cnt}문항</div>
              <div class="text-sm font-bold text-white mt-0.5">${cat}</div>
            </div>
            <button onclick="startExam('${cat}')" class="text-left text-xs font-bold text-emerald-400 hover:underline">이 영역만 연습하기 ➔</button>
          </div>
        `;
      }).join("");
    }

    function startExam(catFilter) {
      const name = document.getElementById("input-student-name").value.trim() || "학습자";
      const mode = document.getElementById("select-exam-mode").value;
      const filtered = catFilter === "ALL" ? RAW_QUESTIONS : RAW_QUESTIONS.filter(q => q.category === catFilter);

      // Prepare questions with shuffled option indices
      const prepared = filtered.map(q => {
        const idxs = shuffleArray([0, 1, 2, 3]);
        return { ...q, shuffledOrder: idxs };
      });

      session = {
        studentName: name,
        mode: mode,
        questions: prepared,
        currentIdx: 0,
        details: []
      };

      document.getElementById("view-start").classList.add("hidden");
      document.getElementById("view-result").classList.add("hidden");
      document.getElementById("view-exam").classList.remove("hidden");
      if (mode === "timed") {
        document.getElementById("header-timer-badge").classList.remove("hidden");
        document.getElementById("header-timer-badge").classList.add("flex");
      } else {
        document.getElementById("header-timer-badge").classList.add("hidden");
      }
      renderQuestion();
    }

    function renderQuestion() {
      if (timerId) { clearInterval(timerId); timerId = null; }
      selectedOptionOrigIdx = null;
      const q = session.questions[session.currentIdx];
      const total = session.questions.length;
      const num = session.currentIdx + 1;

      document.getElementById("exam-progress-text").textContent = `문항 ${num} / ${total}`;
      document.getElementById("exam-category-badge").textContent = q.category;
      document.getElementById("exam-progress-bar").style.width = `${Math.round((num / total) * 100)}%`;
      document.getElementById("q-chapter-badge").textContent = q.chapter;
      document.getElementById("q-diff-badge").textContent = `난이도: ${q.difficulty}`;
      document.getElementById("q-title").textContent = `Q${num}. ${q.question}`;

      const codeEl = document.getElementById("q-code");
      if (q.code) {
        codeEl.textContent = q.code;
        codeEl.classList.remove("hidden");
      } else {
        codeEl.classList.add("hidden");
      }

      const optWrap = document.getElementById("q-options");
      optWrap.innerHTML = "";
      q.shuffledOrder.forEach((origIdx, dispIdx) => {
        const btn = document.createElement("button");
        btn.className = "option-btn w-full text-left p-4 rounded-xl bg-slate-900/90 border border-slate-700 text-sm text-slate-200 flex items-start gap-3";
        btn.innerHTML = `<span class="code-font font-black text-cyan-400 shrink-0">${dispIdx + 1})</span><span>${escapeHtml(q.options[origIdx])}</span>`;
        btn.onclick = () => {
          selectedOptionOrigIdx = origIdx;
          document.querySelectorAll("#q-options .option-btn").forEach(b => b.classList.remove("selected"));
          btn.classList.add("selected");
        };
        optWrap.appendChild(btn);
      });

      document.getElementById("btn-next-q").textContent = num === total ? "제출 및 직무추천 성적표 확인 ➔" : "다음 문항 ➔";

      if (session.mode === "timed") {
        let sec = 60;
        const tDisp = document.getElementById("timer-display");
        tDisp.textContent = "01:00";
        timerId = setInterval(() => {
          sec--;
          const mm = String(Math.floor(sec / 60)).padStart(2, "0");
          const ss = String(sec % 60).padStart(2, "0");
          tDisp.textContent = `${mm}:${ss}`;
          if (sec <= 0) {
            clearInterval(timerId);
            nextQuestion();
          }
        }, 1000);
      }
    }

    function nextQuestion() {
      if (timerId) { clearInterval(timerId); timerId = null; }
      const q = session.questions[session.currentIdx];
      const isCorrect = selectedOptionOrigIdx !== null && selectedOptionOrigIdx === q.answer;
      session.details.push({
        q: q,
        userOrigIdx: selectedOptionOrigIdx,
        isCorrect: isCorrect
      });

      if (session.currentIdx + 1 < session.questions.length) {
        session.currentIdx++;
        renderQuestion();
      } else {
        finishExam();
      }
    }

    function finishExam() {
      document.getElementById("view-exam").classList.add("hidden");
      document.getElementById("header-timer-badge").classList.add("hidden");
      document.getElementById("view-result").classList.remove("hidden");

      const details = session.details;
      lastDetails = details;
      const correctCnt = details.filter(d => d.isCorrect).length;
      const totalCnt = details.length;
      const score100 = Math.round((correctCnt / totalCnt) * 100);

      renderDashboard(session.studentName, score100, correctCnt, totalCnt, details);
    }

    function showSampleResult() {
      const sampleDetails = RAW_QUESTIONS.map((q, i) => ({
        q: q,
        userOrigIdx: (i % 7 === 0) ? ((q.answer + 1) % 4) : q.answer,
        isCorrect: (i % 7 !== 0)
      }));
      lastDetails = sampleDetails;
      const correctCnt = sampleDetails.filter(d => d.isCorrect).length;
      const score100 = Math.round((correctCnt / sampleDetails.length) * 100);
      document.getElementById("view-start").classList.add("hidden");
      document.getElementById("view-result").classList.remove("hidden");
      renderDashboard("샘플 응시자 (데모)", score100, correctCnt, sampleDetails.length, sampleDetails);
    }

    function renderDashboard(studentName, score100, correctCnt, totalCnt, details) {
      document.getElementById("res-student-name").textContent = studentName;
      document.getElementById("res-score-100").textContent = score100;
      document.getElementById("res-correct-count").textContent = `${correctCnt} / ${totalCnt}문항 정답`;

      const badge = document.getElementById("res-pass-badge");
      if (score100 >= 80) {
        badge.textContent = "PASS (공인 합격 · 80점 이상)";
        badge.className = "px-3.5 py-1.5 rounded-full text-xs font-extrabold bg-emerald-500/20 text-emerald-300 border border-emerald-500/40";
      } else {
        badge.textContent = "보완 권장 (80점 미만)";
        badge.className = "px-3.5 py-1.5 rounded-full text-xs font-extrabold bg-rose-500/20 text-rose-300 border border-rose-500/40";
      }

      // Compute per-category %
      const areaScores = {};
      const areaHtml = EXAM_META.categories.map(cat => {
        const sub = details.filter(d => d.q.category === cat);
        const pct = sub.length > 0 ? Math.round((sub.filter(d => d.isCorrect).length / sub.length) * 100) : score100;
        areaScores[cat] = pct;
        return `
          <div class="bg-slate-950/80 border border-slate-800 rounded-xl p-3.5">
            <div class="text-[11px] font-bold text-slate-300 truncate">${cat}</div>
            <div class="text-lg font-black code-font text-cyan-300 mt-1">${pct}%</div>
            <div class="w-full bg-slate-800 h-1.5 rounded-full mt-2 overflow-hidden">
              <div class="h-full rounded-full" style="width:${pct}%; background: linear-gradient(90deg, __ACCENT__, __ACCENT_SEC__);"></div>
            </div>
          </div>
        `;
      }).join("");
      document.getElementById("res-area-bars").innerHTML = areaHtml;

      // Map 5 area scores -> A.C.E.S 6-Axis [Math, Coding, Data, GenAI, Biz, Arch]
      const raw6 = [0, 0, 0, 0, 0, 0];
      const normSum = [0, 0, 0, 0, 0, 0];
      EXAM_META.categories.forEach(cat => {
        const w = EXAM_META.aces_weights[cat];
        const s = areaScores[cat];
        for (let i = 0; i < 6; i++) {
          raw6[i] += s * w[i];
          normSum[i] += w[i];
        }
      });
      const aces6 = raw6.map((v, i) => Math.min(100, Math.round(normSum[i] > 0 ? v / normSum[i] : score100)));

      const featNames = ["수학/알고리즘", "SW 코딩", "데이터/인프라", "GenAI/프롬프트", "비즈니스 기획", "시스템 아키텍처"];
      document.getElementById("res-aces-6kpi").innerHTML = featNames.map((fn, i) => `
        <div class="bg-slate-900 border border-slate-800 rounded-xl p-2.5">
          <div class="text-[11px] text-slate-400">${fn}</div>
          <div class="text-base font-black text-cyan-300 code-font">${aces6[i]}점</div>
        </div>
      `).join("");

      // Update A.C.E.S integration link
      document.getElementById("btn-send-aces").href = `career_aces.html?exam=${EXAM_META.id}&score=${score100}`;

      // Cosine + Adequacy Job Matching
      const uNorm = Math.sqrt(aces6.reduce((a, v) => a + v * v, 0));
      const uMean = aces6.reduce((a, v) => a + v, 0) / 6;
      const ranked = JOBS.map((job, idx) => {
        const b = job.scores;
        const bNorm = Math.sqrt(b.reduce((a, v) => a + v * v, 0));
        let dot = 0;
        for (let i = 0; i < 6; i++) dot += aces6[i] * b[i];
        const cosSim = uNorm > 0 ? Math.max(0, dot / (uNorm * bNorm)) : 0;
        return { job, idx, score: cosSim };
      });
      const expSum = ranked.reduce((a, r) => a + Math.exp(r.score * 6.0), 0);
      const scaleFactor = Math.min(1.0, Math.max(0.45, uMean / 65.0));
      ranked.forEach(r => { r.prob = Math.round((Math.exp(r.score * 6.0) / expSum) * 100 * scaleFactor * 10) / 10; });
      ranked.sort((a, b) => b.prob - a.prob);

      const medals = ["🥇 1순위 추천", "🥈 2순위 추천", "🥉 3순위 추천"];
      document.getElementById("res-job-cards").innerHTML = ranked.slice(0, 3).map((r, i) => `
        <div class="p-4 rounded-xl border ${i === 0 ? 'bg-cyan-950/30 border-cyan-500/50' : 'bg-slate-900/70 border-slate-800'}">
          <div class="flex justify-between items-center">
            <span class="text-xs font-extrabold ${i === 0 ? 'text-cyan-300' : 'text-slate-300'}">${medals[i]}</span>
            <span class="text-lg font-black code-font ${i === 0 ? 'text-emerald-400' : 'text-slate-300'}">${r.prob}%</span>
          </div>
          <div class="text-base font-extrabold text-white mt-0.5">${r.job.name}</div>
          <div class="text-xs text-slate-400 mt-1">${r.job.desc}</div>
        </div>
      `).join("");

      // SHAP XAI
      const top1 = ranked[0].job;
      const diffs = featNames.map((fn, i) => ({ name: fn, val: aces6[i], diff: aces6[i] - top1.scores[i] }))
        .sort((a, b) => b.diff - a.diff);
      document.getElementById("res-shap-plus").innerHTML = diffs.slice(0, 3).map(d =>
        `<div>• <b>${d.name}</b> (${d.val}점): 목표 기준선 대비 <span class="${d.diff >= 0 ? 'text-emerald-400' : 'text-cyan-300'} font-bold">${d.diff >= 0 ? '+' : ''}${d.diff}점</span></div>`
      ).join("");
      document.getElementById("res-shap-minus").innerHTML = diffs.slice(-2).map(d =>
        `<div>• <b>${d.name}</b> (${d.val}점): 기준(${d.val - d.diff}점) 대비 ${d.diff >= 0 ? '충분히 우수함' : `<span class="text-amber-300 font-bold">${d.diff}점 보완 시 경쟁력 극대화</span>`}</div>`
      ).join("");

      // Radar Chart
      const ctx = document.getElementById("radarChart").getContext("2d");
      if (radarChart) radarChart.destroy();
      radarChart = new Chart(ctx, {
        type: "radar",
        data: {
          labels: featNames.map((n, i) => `${n} (${aces6[i]})`),
          datasets: [
            {
              label: "내 역량 점수",
              data: aces6,
              backgroundColor: "rgba(56, 189, 248, 0.3)",
              borderColor: "#38bdf8",
              borderWidth: 2.5
            },
            {
              label: `1순위 직무 (${top1.name}) 기준선`,
              data: top1.scores,
              backgroundColor: "rgba(245, 158, 11, 0.1)",
              borderColor: "#f59e0b",
              borderDash: [4, 4],
              borderWidth: 2
            }
          ]
        },
        options: {
          responsive: true,
          maintainAspectRatio: false,
          scales: {
            r: {
              min: 0, max: 100,
              ticks: { display: false, stepSize: 20 },
              grid: { color: "#1e293b" },
              angleLines: { color: "#1e293b" },
              pointLabels: { color: "#cbd5e1", font: { size: 11, weight: "bold" } }
            }
          },
          plugins: { legend: { labels: { color: "#f8fafc", font: { size: 11 } }, position: "bottom" } }
        }
      });

      filterReview("all");
    }

    function filterReview(mode) {
      const list = document.getElementById("res-review-list");
      const items = mode === "wrong" ? lastDetails.filter(d => !d.isCorrect) : lastDetails;
      if (items.length === 0) {
        list.innerHTML = `<div class="glass-card rounded-2xl p-6 text-center text-emerald-400 font-bold">축하합니다! 틀린 문항이 없습니다.</div>`;
        return;
      }
      list.innerHTML = items.map((d, idx) => {
        const q = d.q;
        const badge = d.isCorrect
          ? `<span class="px-2 py-0.5 rounded bg-emerald-500/20 text-emerald-300 text-xs font-bold">정답</span>`
          : `<span class="px-2 py-0.5 rounded bg-rose-500/20 text-rose-300 text-xs font-bold">오답</span>`;
        return `
          <div class="glass-card rounded-2xl p-5 space-y-3 border ${d.isCorrect ? 'border-emerald-500/30' : 'border-rose-500/40'}">
            <div class="flex flex-wrap justify-between items-center gap-2 text-xs">
              <div class="flex items-center gap-2">
                <span class="code-font font-bold text-slate-400">Q${q.id}</span>
                <span class="px-2 py-0.5 rounded bg-slate-800 text-cyan-300 font-semibold">${q.category} · ${q.chapter}</span>
                ${badge}
              </div>
              <span class="text-emerald-400 font-bold">정답: ${q.answer + 1}번</span>
            </div>
            <div class="text-sm sm:text-base font-bold text-white">${escapeHtml(q.question)}</div>
            ${q.code ? `<pre class="bg-slate-950 p-3 rounded-lg text-xs text-cyan-200 code-font overflow-x-auto">${escapeHtml(q.code)}</pre>` : ''}
            <div class="grid grid-cols-1 gap-1.5 text-xs">
              ${q.options.map((opt, oi) => {
                const isC = oi === q.answer;
                const isU = oi === d.userOrigIdx;
                const cls = isC ? "bg-emerald-950/40 border-emerald-500/50 text-emerald-200 font-bold" : (isU ? "bg-rose-950/40 border-rose-500/50 text-rose-200" : "bg-slate-900/70 border-slate-800 text-slate-400");
                return `<div class="p-2.5 rounded-lg border ${cls}">${oi + 1}) ${escapeHtml(opt)} ${isC ? '<b>[정답]</b>' : ''} ${isU && !isC ? '<b>[내 선택]</b>' : ''}</div>`;
              }).join("")}
            </div>
            <div class="bg-indigo-950/35 border border-indigo-500/30 rounded-lg p-3 text-xs text-slate-200 leading-relaxed">
              <b class="text-amber-400">💡 핵심 해설:</b> ${escapeHtml(q.explanation)}
            </div>
          </div>
        `;
      }).join("");
    }

    function retakeExam() {
      document.getElementById("view-result").classList.add("hidden");
      document.getElementById("view-start").classList.remove("hidden");
    }

    function escapeHtml(str) {
      return String(str || "").replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;");
    }

    initStartView();
  </script>
</body>
</html>
"""


def build_exam(meta, questions, filename):
    html = HTML_TEMPLATE
    html = html.replace("__TITLE__", meta["title"])
    html = html.replace("__SUBTITLE__", meta["subtitle"])
    html = html.replace("__BOOK_URL__", meta["book_url"])
    html = html.replace("__SIM_URL__", meta["sim_url"])
    html = html.replace("__ACCENT__", meta["accent"])
    html = html.replace("__ACCENT_SEC__", meta["accent_secondary"])
    html = html.replace("__META_JSON__", json.dumps(meta, ensure_ascii=False))
    html = html.replace("__QUESTIONS_JSON__", json.dumps(questions, ensure_ascii=False))

    out_path = os.path.join(OUT_DIR, filename)
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"✅ 시험 웹앱 생성 완료: {filename} ({len(questions)}문항, {len(html):,} bytes)")

    # Markdown 문제은행 백업 저장
    md_lines = [f"# {meta['title']}\n", f"> 출처 도서: {meta['book_url']} | 총 {len(questions)}문항\n\n---\n"]
    for q in questions:
        md_lines.append(f"### Q{q['id']:02d}. [{q['category']} | {q['chapter']} | {q['difficulty']}] {q['question']}\n")
        if q.get("code"):
            md_lines.append(f"```python\n{q['code']}\n```\n")
        for idx, opt in enumerate(q["options"], 1):
            mark = "✅ **(정답)**" if (idx - 1) == q["answer"] else ""
            md_lines.append(f"{idx}. {opt} {mark}\n")
        md_lines.append(f"> **해설**: {q['explanation']}\n\n---\n")

    md_path = os.path.join(DOCS_DIR, f"EXAM_{meta['book_id']}_30_QUESTIONS.md")
    with open(md_path, "w", encoding="utf-8") as f:
        f.write("".join(md_lines))
    print(f"✅ 문제은행 Markdown 저장 완료: {md_path}")


def main():
    build_exam(EXAM_META_22015, QUESTIONS_22015, "exam_smartcar_lakehouse.html")
    build_exam(EXAM_META_22036, QUESTIONS_22036, "exam_graphrag_mcp.html")
    build_exam(EXAM_META_22037, QUESTIONS_22037, "exam_continual_memory.html")


if __name__ == "__main__":
    main()
