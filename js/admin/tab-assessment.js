/**
 * ==============================================================================
 * DMDG 관리자 콘솔 - 탭 4: 자가진단 분석 (Assessment 20문항) 모듈
 * 파일명: js/admin/tab-assessment.js
 * ==============================================================================
 */

export class TabAssessment {
  constructor() {
    this.candidates = [
      {
        id: 'ASS-20261029-01',
        name: '정*훈',
        email: 'jungh**@gmail.com',
        phone: '010-****-4821',
        score: 85,
        level: '고급 (Level 3)',
        passed: true,
        date: '2026-10-29 15:30',
        career: '현업 백엔드 4년차 (Python/FastAPI)',
        interest: '자율형 멀티에이전트 & pgvector'
      },
      {
        id: 'ASS-20261028-05',
        name: '강*우',
        email: 'kang**@kakao.com',
        phone: '010-****-9132',
        score: 90,
        level: '최고급 (Level 4)',
        passed: true,
        date: '2026-10-28 11:20',
        career: 'ML 엔지니어 5년차 (PyTorch)',
        interest: '지식그래프 Graph RAG & Neo4j'
      },
      {
        id: 'ASS-20261027-02',
        name: '임*서',
        email: 'lim**@naver.com',
        phone: '010-****-1984',
        score: 65,
        level: '중급 (Level 2)',
        passed: false,
        date: '2026-10-27 19:45',
        career: '웹 프론트엔드 2년차 (React)',
        interest: '클린룸 TDD & 리버스엔지니어링'
      },
      {
        id: 'ASS-20261026-08',
        name: '오*택',
        email: 'oh**@enterprise.com',
        phone: '010-****-7741',
        score: 75,
        level: '고급 (Level 3)',
        passed: true,
        date: '2026-10-26 14:10',
        career: '데이터 사이언티스트 3년차',
        interest: '시맨틱 청킹 & Docling'
      },
      {
        id: 'ASS-20261025-03',
        name: '윤*진',
        email: 'yoon**@hanmail.net',
        phone: '010-****-6215',
        score: 95,
        level: '마스터 (Level 5)',
        passed: true,
        date: '2026-10-25 18:00',
        career: '소프트웨어 아키텍트 8년차',
        interest: '12대 페르소나 StateGraph 무인 팩토리'
      }
    ];
  }

  init() {
    this.renderStats();
    this.renderTable();
    this.bindEvents();
  }

  bindEvents() {
    const btnCsv = document.getElementById('btn-export-assessment-csv');
    if (btnCsv) {
      btnCsv.addEventListener('click', () => this.exportCsv());
    }
  }

  renderStats() {
    const total = this.candidates.length;
    const passed = this.candidates.filter(c => c.passed).length;
    const avgScore = Math.round(this.candidates.reduce((a, b) => a + b.score, 0) / total);
    const passRate = Math.round((passed / total) * 100);

    const elTotal = document.getElementById('ass-stat-total-count');
    const elAvg = document.getElementById('ass-stat-avg-score');
    const elRate = document.getElementById('ass-stat-pass-rate');

    if (elTotal) elTotal.textContent = `${total}명`;
    if (elAvg) elAvg.textContent = `${avgScore}점`;
    if (elRate) elRate.textContent = `${passRate}%`;
  }

  renderTable() {
    const tbody = document.getElementById('assessment-candidates-tbody');
    if (!tbody) return;

    tbody.innerHTML = '';

    this.candidates.forEach(c => {
      const tr = document.createElement('tr');
      const passBadge = c.passed
        ? '<span class="badge-status badge-success">합격 (70점 이상)</span>'
        : '<span class="badge-status badge-danger">미달</span>';

      tr.innerHTML = `
        <td class="font-mono text-xs text-slate-400">${c.id}</td>
        <td>
          <div class="font-bold text-white text-xs">${c.name}</div>
          <div class="text-[11px] text-slate-400 font-mono">${c.email} | ${c.phone}</div>
        </td>
        <td class="text-xs text-slate-300">${c.career}</td>
        <td>
          <div class="flex items-center gap-2">
            <span class="font-bold text-sm text-purple-400">${c.score}점</span>
            <span class="text-[11px] text-slate-400">(${c.level})</span>
          </div>
        </td>
        <td>${passBadge}</td>
        <td class="text-xs text-slate-300 font-medium">${c.interest}</td>
        <td class="text-[11px] text-slate-400 font-mono">${c.date}</td>
      `;

      tbody.appendChild(tr);
    });
  }

  exportCsv() {
    let csv = 'ID,이름,이메일,연락처,점수,등급,합격여부,경력,관심분야,응시일시\n';
    this.candidates.forEach(c => {
      csv += `"${c.id}","${c.name}","${c.email}","${c.phone}",${c.score},"${c.level}","${c.passed ? '합격' : '미달'}","${c.career}","${c.interest}","${c.date}"\n`;
    });

    const blob = new Blob(['\uFEFF' + csv], { type: 'text/csv;charset=utf-8;' });
    const url = URL.createObjectURL(blob);
    const link = document.createElement('a');
    link.href = url;
    link.download = `DMDG_20문항_역량평가_응시자리스트_${new Date().toISOString().split('T')[0]}.csv`;
    link.click();
    URL.revokeObjectURL(url);
  }
}
