/**
 * ==============================================================================
 * DMDG 관리자 콘솔 - 탭 2: 결제 및 거래 (Revenue) 모듈
 * 파일명: js/admin/tab-revenue.js
 * ==============================================================================
 */

export class TabRevenue {
  constructor() {
    this.transactions = [
      {
        id: 'PAY-20261029-001',
        name: '김*현',
        email: 'k**@naver.com',
        product: '말쌈 신조어 사전 영구 소장권',
        amount: 29000,
        currency: 'KRW',
        method: '카카오페이 (PortOne)',
        status: 'PAID',
        date: '2026-10-29 18:42:15'
      },
      {
        id: 'PAY-20261028-004',
        name: '이*수',
        email: 'lee**@kakao.com',
        product: '사전 역량평가 20문항 + 1:1 진단서',
        amount: 49000,
        currency: 'KRW',
        method: '토스페이 (PortOne)',
        status: 'PAID',
        date: '2026-10-28 14:15:30'
      },
      {
        id: 'PAY-20261027-009',
        name: 'Michael Chang',
        email: 'm***@gmail.com',
        product: 'DMDG Studio Global eBook All-Pass',
        amount: 39,
        currency: 'USD',
        method: 'PayPal Express',
        status: 'PAID',
        date: '2026-10-27 09:20:11'
      },
      {
        id: 'PAY-20261026-003',
        name: '박*진',
        email: 'park**@daum.net',
        product: '말쌈 신조어 사전 영구 소장권',
        amount: 29000,
        currency: 'KRW',
        method: 'KG이니시스 카드',
        status: 'REFUNDED',
        date: '2026-10-26 11:05:44'
      },
      {
        id: 'PAY-20261025-007',
        name: '최*민',
        email: 'choi**@company.co.kr',
        product: '기업 HR 세대소통 워크숍 키트 (PDF+PPT)',
        amount: 199000,
        currency: 'KRW',
        method: '토스페이 (PortOne)',
        status: 'PAID',
        date: '2026-10-25 16:50:22'
      }
    ];

    this.currentFilter = 'all';
  }

  init() {
    this.renderStats();
    this.renderTable();
    this.bindEvents();
  }

  bindEvents() {
    const filterSelect = document.getElementById('revenue-method-filter');
    if (filterSelect) {
      filterSelect.addEventListener('change', (e) => {
        this.currentFilter = e.target.value;
        this.renderTable();
      });
    }

    const refreshBtn = document.getElementById('btn-refresh-revenue');
    if (refreshBtn) {
      refreshBtn.addEventListener('click', () => {
        this.renderStats();
        this.renderTable();
      });
    }
  }

  renderStats() {
    let totalKrw = 0;
    let paidCount = 0;

    this.transactions.forEach(t => {
      if (t.status === 'PAID') {
        paidCount++;
        totalKrw += t.currency === 'KRW' ? t.amount : t.amount * 1350;
      }
    });

    const elTotal = document.getElementById('rev-stat-total-amount');
    const elCount = document.getElementById('rev-stat-paid-count');
    const elRate = document.getElementById('rev-stat-success-rate');

    if (elTotal) elTotal.textContent = `₩${totalKrw.toLocaleString()}`;
    if (elCount) elCount.textContent = `${paidCount}건`;
    if (elRate) elRate.textContent = `${Math.round((paidCount / this.transactions.length) * 100)}%`;
  }

  renderTable() {
    const tbody = document.getElementById('revenue-transactions-tbody');
    if (!tbody) return;

    tbody.innerHTML = '';

    const filtered = this.transactions.filter(t => {
      if (this.currentFilter === 'all') return true;
      if (this.currentFilter === 'portone') return t.method.includes('PortOne') || t.method.includes('이니시스');
      if (this.currentFilter === 'paypal') return t.method.includes('PayPal');
      if (this.currentFilter === 'paid') return t.status === 'PAID';
      if (this.currentFilter === 'refund') return t.status === 'REFUNDED';
      return true;
    });

    filtered.forEach(t => {
      const tr = document.createElement('tr');
      
      const statusBadge = t.status === 'PAID'
        ? '<span class="badge-status badge-success">✓ 결제완료</span>'
        : '<span class="badge-status badge-danger">↩ 환불완료</span>';

      const formattedAmount = t.currency === 'KRW'
        ? `₩${t.amount.toLocaleString()}`
        : `$${t.amount.toFixed(2)}`;

      tr.innerHTML = `
        <td class="font-mono text-xs text-slate-400">${t.id}</td>
        <td>
          <div class="font-bold text-white text-xs">${t.name}</div>
          <div class="text-[11px] text-slate-400 font-mono">${t.email}</div>
        </td>
        <td class="text-xs font-medium text-slate-200">${t.product}</td>
        <td class="font-bold text-amber-400 text-xs">${formattedAmount}</td>
        <td class="text-xs text-slate-300">${t.method}</td>
        <td>${statusBadge}</td>
        <td class="text-[11px] text-slate-400 font-mono">${t.date}</td>
      `;

      tbody.appendChild(tr);
    });
  }
}
