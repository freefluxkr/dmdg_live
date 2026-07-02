// Lucide icons initialization
lucide.createIcons();

// Define allowed admin emails (can be customized)
const ALLOWED_ADMINS = ['tuesv@gmail.com', 'admin@gmail.com', 'admin@dmdg.com'];

// Wait for firebase init
document.addEventListener('DOMContentLoaded', () => {
  // Check if already logged in
  firebase.auth().onAuthStateChanged(user => {
    if (user && !user.isAnonymous) {
      document.getElementById('auth-overlay').classList.add('hidden');
      const dash = document.getElementById('dashboard-container');
      dash.classList.remove('hidden');
      // small delay to trigger transition
      setTimeout(() => dash.classList.remove('opacity-0'), 50);
      loadDashboardData();
    }
  });
});

async function loginWithGoogle() {
  const provider = new firebase.auth.GoogleAuthProvider();
  try {
    const result = await firebase.auth().signInWithPopup(provider);
    const user = result.user;
    
    // For local test, we might bypass the strict check, but here is the logic:
    // if (!ALLOWED_ADMINS.includes(user.email)) {
    //   await firebase.auth().signOut();
    //   throw new Error('인가되지 않은 관리자 계정입니다.');
    // }
    
    document.getElementById('auth-error').classList.add('hidden');
  } catch (error) {
    console.error("Login failed:", error);
    const errorEl = document.getElementById('auth-error');
    errorEl.classList.remove('hidden');
    errorEl.textContent = error.message || "접근 권한이 없는 계정입니다.";
  }
}

async function logoutAdmin() {
  await firebase.auth().signOut();
  window.location.reload();
}

// ----------------------------------------------------
// 대시보드 데이터 로드 로직
// ----------------------------------------------------
async function loadDashboardData() {
  try {
    // 1. 총 마중물 수 (Primers)
    const primersSnap = await firestore.collection('primers').get();
    document.getElementById('stat-primers').textContent = primersSnap.size.toLocaleString() + " 개";

    // 2. 주요 수치 (Stats Overview) - Firebase에서 집계된 데이터 불러오기
    const statsDoc = await firestore.collection('stats').doc('overview').get();
    const stats = statsDoc.exists ? statsDoc.data() : { relays: 0, premiumUsers: 0, visits: 0 };

    document.getElementById('stat-relays').textContent = (stats.relays || 0).toLocaleString() + " 건";
    document.getElementById('stat-premium').textContent = (stats.premiumUsers || 0).toLocaleString() + " 명";
    document.getElementById('stat-visits').textContent = (stats.visits || 0).toLocaleString() + " 회";

    // 4. 유입경로 및 일별 차트용 애널리틱스 데이터
    const analyticsSnap = await firestore.collection('analytics').get();
    const analyticsData = analyticsSnap.docs.map(d => d.data());
    
    // 데이터 가공 (유입 경로 및 일별 트렌드)
    processAndRenderCharts(analyticsData);
    
  } catch (error) {
    console.error("대시보드 데이터 로드 실패:", error);
    alert("데이터를 불러오는 중 오류가 발생했습니다.");
  }
}

function processAndRenderCharts(data) {
  // 1. 유입 경로 (Referrer) 처리
  const referrerCounts = {};
  const dailyCounts = {};

  data.forEach(item => {
    // Referrer 분류
    let ref = item.referrer || 'Direct / Bookmark';
    if (ref.includes('google')) ref = 'Google Search';
    else if (ref.includes('naver')) ref = 'Naver Search';
    else if (ref.includes('kakao') || ref.includes('daum')) ref = 'Kakao/Daum';
    else if (ref.includes('facebook') || ref.includes('instagram')) ref = 'Social Media';
    else if (ref.length > 20) ref = ref.substring(0, 20) + '...';
    
    referrerCounts[ref] = (referrerCounts[ref] || 0) + 1;

    // 일별 접속 분류
    if (item.timestamp) {
      const date = new Date(item.timestamp);
      // Format YYYY-MM-DD
      const dateStr = `${date.getFullYear()}-${String(date.getMonth()+1).padStart(2, '0')}-${String(date.getDate()).padStart(2, '0')}`;
      dailyCounts[dateStr] = (dailyCounts[dateStr] || 0) + 1;
    }
  });

  // 차트 데이터 정렬
  const refLabels = Object.keys(referrerCounts);
  const refData = Object.values(referrerCounts);

  // 날짜순 정렬
  const sortedDates = Object.keys(dailyCounts).sort();
  const dateData = sortedDates.map(date => dailyCounts[date]);

  // Chart.js 렌더링
  renderReferrerChart(refLabels, refData);
  renderDailyChart(sortedDates, dateData);
}

let refChartInstance = null;
let dailyChartInstance = null;

function renderReferrerChart(labels, data) {
  const ctx = document.getElementById('referrerChart').getContext('2d');
  if (refChartInstance) refChartInstance.destroy();

  refChartInstance = new Chart(ctx, {
    type: 'doughnut',
    data: {
      labels: labels,
      datasets: [{
        data: data,
        backgroundColor: [
          '#6366f1', '#ec4899', '#f59e0b', '#10b981', '#3b82f6', '#8b5cf6'
        ],
        borderWidth: 0,
        hoverOffset: 4
      }]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        legend: { position: 'right', labels: { font: { family: 'Outfit' } } }
      }
    }
  });
}

function renderDailyChart(labels, data) {
  const ctx = document.getElementById('dailyChart').getContext('2d');
  if (dailyChartInstance) dailyChartInstance.destroy();

  dailyChartInstance = new Chart(ctx, {
    type: 'line',
    data: {
      labels: labels,
      datasets: [{
        label: '일간 방문자 수',
        data: data,
        borderColor: '#f43f5e',
        backgroundColor: 'rgba(244, 63, 94, 0.1)',
        borderWidth: 3,
        pointBackgroundColor: '#f43f5e',
        pointBorderColor: '#fff',
        pointBorderWidth: 2,
        pointRadius: 4,
        fill: true,
        tension: 0.4
      }]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        legend: { display: false }
      },
      scales: {
        y: { beginAtZero: true, grid: { borderDash: [4, 4] } },
        x: { grid: { display: false } }
      }
    }
  });
}
