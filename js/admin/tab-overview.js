/**
 * ==============================================================================
 * DMDG 관리자 콘솔 - 탭 1: 개요 (Overview) 트래픽 및 KPI 모듈
 * 파일명: js/admin/tab-overview.js
 * ==============================================================================
 */

export class TabOverview {
  constructor() {
    this.chart = null;
    this.currentPeriod = 7;
  }

  init() {
    this.initChart();
    this.renderRealtimeWidget();
    this.bindEvents();
  }

  bindEvents() {
    const p7 = document.getElementById('period-btn-7');
    const p28 = document.getElementById('period-btn-28');
    const p90 = document.getElementById('period-btn-90');

    if (p7) p7.addEventListener('click', () => this.changePeriod(7));
    if (p28) p28.addEventListener('click', () => this.changePeriod(28));
    if (p90) p90.addEventListener('click', () => this.changePeriod(90));
  }

  changePeriod(days) {
    this.currentPeriod = days;

    // 버튼 활성 스타일 전환
    [7, 28, 90].forEach(d => {
      const btn = document.getElementById(`period-btn-${d}`);
      if (btn) {
        if (d === days) {
          btn.className = 'period-btn px-3 py-1.5 rounded-lg font-bold bg-amber-500 text-slate-950 transition-all shadow-sm';
        } else {
          btn.className = 'period-btn px-3 py-1.5 rounded-lg font-medium text-slate-400 hover:text-white transition-all';
        }
      }
    });

    this.updateChartData(days);
  }

  generateDataForPeriod(days) {
    const labels = [];
    const pvData = [];
    const uvData = [];
    const today = new Date();

    for (let i = days - 1; i >= 0; i--) {
      const d = new Date(today);
      d.setDate(d.getDate() - i);
      const dateStr = `${d.getMonth() + 1}/${d.getDate()}`;
      labels.push(dateStr);

      // 리얼한 트래픽 시뮬레이션
      const basePv = Math.floor(12 + Math.sin(i * 0.5) * 6 + Math.random() * 8);
      const baseUv = Math.max(3, Math.floor(basePv * 0.35 + Math.random() * 2));
      pvData.push(basePv);
      uvData.push(baseUv);
    }

    const totalPv = pvData.reduce((a, b) => a + b, 0);
    const totalUv = uvData.reduce((a, b) => a + b, 0);

    return { labels, pvData, uvData, totalPv, totalUv };
  }

  initChart() {
    const canvas = document.getElementById('trafficTimeSeriesChart');
    if (!canvas) return;

    const data = this.generateDataForPeriod(7);

    // KPI 수치 업데이트
    const statPv = document.getElementById('chart-stat-total-pv');
    const statUv = document.getElementById('chart-stat-total-uv');
    if (statPv) statPv.textContent = data.totalPv;
    if (statUv) statUv.textContent = data.totalUv;

    const ctx = canvas.getContext('2d');
    
    // 그라디언트 채우기
    const pvGrad = ctx.createLinearGradient(0, 0, 0, 260);
    pvGrad.addColorStop(0, 'rgba(245, 158, 11, 0.35)');
    pvGrad.addColorStop(1, 'rgba(245, 158, 11, 0.0)');

    const uvGrad = ctx.createLinearGradient(0, 0, 0, 260);
    uvGrad.addColorStop(0, 'rgba(6, 182, 212, 0.25)');
    uvGrad.addColorStop(1, 'rgba(6, 182, 212, 0.0)');

    this.chart = new Chart(ctx, {
      type: 'line',
      data: {
        labels: data.labels,
        datasets: [
          {
            label: '페이지 조회수 (PV)',
            data: data.pvData,
            borderColor: '#f59e0b',
            backgroundColor: pvGrad,
            borderWidth: 2.5,
            fill: true,
            tension: 0.35,
            pointRadius: 3,
            pointBackgroundColor: '#f59e0b',
            pointHoverRadius: 6
          },
          {
            label: '순 방문자수 (UV)',
            data: data.uvData,
            borderColor: '#06b6d4',
            backgroundColor: uvGrad,
            borderWidth: 2,
            borderDash: [4, 4],
            fill: true,
            tension: 0.35,
            pointRadius: 2,
            pointBackgroundColor: '#06b6d4',
            pointHoverRadius: 5
          }
        ]
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          legend: {
            display: true,
            position: 'top',
            labels: {
              color: '#94a3b8',
              font: { size: 11, family: 'Pretendard' },
              boxWidth: 12,
              boxHeight: 12,
              usePointStyle: true
            }
          },
          tooltip: {
            backgroundColor: '#0f172a',
            borderColor: 'rgba(245, 158, 11, 0.3)',
            borderWidth: 1,
            titleColor: '#ffffff',
            bodyColor: '#e2e8f0',
            padding: 10,
            cornerRadius: 8
          }
        },
        scales: {
          x: {
            grid: { color: 'rgba(255, 255, 255, 0.04)' },
            ticks: { color: '#64748b', font: { size: 10 } }
          },
          y: {
            grid: { color: 'rgba(255, 255, 255, 0.04)' },
            ticks: { color: '#64748b', font: { size: 10 } },
            beginAtZero: true
          }
        }
      }
    });
  }

  updateChartData(days) {
    if (!this.chart) return;
    const data = this.generateDataForPeriod(days);

    this.chart.data.labels = data.labels;
    this.chart.data.datasets[0].data = data.pvData;
    this.chart.data.datasets[1].data = data.uvData;
    this.chart.update();

    const statPv = document.getElementById('chart-stat-total-pv');
    const statUv = document.getElementById('chart-stat-total-uv');
    if (statPv) statPv.textContent = data.totalPv;
    if (statUv) statUv.textContent = data.totalUv;
  }

  renderRealtimeWidget() {
    const barsContainer = document.getElementById('realtime-bars-container');
    if (!barsContainer) return;

    barsContainer.innerHTML = '';
    // 48시간 시간대별 미니 바 차트
    for (let i = 0; i < 24; i++) {
      const height = Math.floor(10 + Math.random() * 85);
      const bar = document.createElement('div');
      bar.className = 'w-full bg-slate-800 hover:bg-amber-500 rounded-t transition-all cursor-pointer relative group';
      bar.style.height = `${height}%`;
      
      const tooltip = document.createElement('div');
      tooltip.className = 'hidden group-hover:block absolute bottom-full left-1/2 -translate-x-1/2 mb-1 px-1.5 py-0.5 bg-slate-950 text-[10px] text-amber-300 font-bold rounded whitespace-nowrap z-10 border border-amber-500/30';
      tooltip.textContent = `${Math.floor(height / 4)}명`;
      
      bar.appendChild(tooltip);
      barsContainer.appendChild(bar);
    }
  }
}
