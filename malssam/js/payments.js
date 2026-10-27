// ============================================================
// 💳 [후원 및 결제, 정식 리포트 & PDF 발급 엔진]
// ============================================================

// 1) 🟡 카카오페이 실전 연동
async function requestKakaoPay() {
  closeTierModal();
  const info = getTierInfo();
  const paymentId = 'kakao_' + Date.now();

  if (window.PortOne) {
    try {
      const response = await window.PortOne.requestPayment({
        storeId: 'store-d0b81c4e-5882-4f36-96b6-d249d32fb1cf',
        channelKey: 'channel-key-kakaopay-live',
        paymentId: paymentId,
        orderName: info.name,
        totalAmount: info.amount,
        currency: 'KRW',
        payMethod: 'EASY_PAY',
        easyPay: { provider: 'KAKAOPAY' },
        customer: {
          fullName: '말쌈 후원자',
          email: 'support@malssam.com'
        }
      });

      if (response && response.code) {
        showToast(`❌ 카카오페이 취소/오류: ${response.message || response.code}`);
        return;
      }

      if (response && (response.paymentId || !response.code)) {
        executePaymentComplete('카카오페이', response.paymentId || paymentId, info.amountText);
        return;
      }
    } catch (e) {
      console.warn("PortOne v2 호출 fallback 진행:", e);
    }
  }

  // Fallback: IMP v1
  if (typeof IMP !== 'undefined') {
    IMP.init('imp00000000');
    IMP.request_pay({
      pg: 'kakaopay',
      pay_method: 'card',
      merchant_uid: paymentId,
      name: info.name,
      amount: info.amount,
      buyer_email: 'support@malssam.com',
      buyer_name: '말쌈 후원자'
    }, function (rsp) {
      if (rsp.success) {
        executePaymentComplete('카카오페이', rsp.imp_uid || paymentId, info.amountText);
      } else {
        showToast(`❌ 결제 취소 또는 오류: ${rsp.error_msg}`);
      }
    });
  } else {
    alert("결제 모듈을 로드 중입니다. 잠시 후 다시 시도해 주세요.");
  }
}

// 2) 🔵 토스페이 실전 연동
async function requestTossPay() {
  closeTierModal();
  const info = getTierInfo();
  const paymentId = 'toss_' + Date.now();

  if (window.PortOne) {
    try {
      const response = await window.PortOne.requestPayment({
        storeId: 'store-d0b81c4e-5882-4f36-96b6-d249d32fb1cf',
        channelKey: 'channel-key-tosspay-live',
        paymentId: paymentId,
        orderName: info.name,
        totalAmount: info.amount,
        currency: 'KRW',
        payMethod: 'EASY_PAY',
        easyPay: { provider: 'TOSSPAY' },
        customer: {
          fullName: '말쌈 후원자',
          email: 'support@malssam.com'
        }
      });

      if (response && response.code) {
        showToast(`❌ 토스페이 취소/오류: ${response.message || response.code}`);
        return;
      }

      if (response && (response.paymentId || !response.code)) {
        executePaymentComplete('토스페이', response.paymentId || paymentId, info.amountText);
        return;
      }
    } catch (e) {
      console.warn("PortOne v2 호출 fallback 진행:", e);
    }
  }

  // Fallback: IMP v1
  if (typeof IMP !== 'undefined') {
    IMP.init('imp00000000');
    IMP.request_pay({
      pg: 'tosspay',
      pay_method: 'card',
      merchant_uid: paymentId,
      name: info.name,
      amount: info.amount,
      buyer_email: 'support@malssam.com',
      buyer_name: '말쌈 후원자'
    }, function (rsp) {
      if (rsp.success) {
        executePaymentComplete('토스페이', rsp.imp_uid || paymentId, info.amountText);
      } else {
        showToast(`❌ 결제 취소 또는 오류: ${rsp.error_msg}`);
      }
    });
  } else {
    alert("결제 모듈을 로드 중입니다. 잠시 후 다시 시도해 주세요.");
  }
}

// 3) 🌐 PayPal 실전 연동
function requestPayPal() {
  const info = getTierInfo();
  document.getElementById('paypalModalDesc').innerHTML = `${info.name}<br><strong id="paypalAmountText" style="font-size:1.3rem; color:#facc15;">Amount: ${info.usdText}</strong>`;
  document.getElementById('paypalModal').classList.add('active');

  const container = document.getElementById('paypal-button-container');
  if (!container) return;
  container.innerHTML = '';

  if (window.paypal) {
    try {
      window.paypal.Buttons({
        createOrder: function(data, actions) {
          return actions.order.create({
            purchase_units: [{
              amount: { value: info.usd },
              description: info.name
            }]
          });
        },
        onApprove: function(data, actions) {
          return actions.order.capture().then(function(details) {
            closePayPalModal();
            executePaymentComplete('PayPal Global', details.id, info.usdText);
          });
        },
        onError: function(err) {
          console.error("PayPal Error:", err);
          showToast("PayPal 연결 중 오류가 발생했습니다.");
        }
      }).render('#paypal-button-container');
    } catch(e) {
      console.error(e);
    }
  }
}

function closePayPalModal() {
  const pm = document.getElementById('paypalModal');
  if (pm) pm.classList.remove('active');
}

// 4) ☕ 커피 후원
function openCoffeeSponsor() {
  selectedTier = 1;
  const confirmed = confirm("[☕ 커피 한 잔 후원]\n\n말쌈 사전 개발팀에게 따뜻한 커피 한 잔(1,000원)을 후원해 주시겠습니까?\n카카오페이 간편 결제창으로 이동합니다.");
  if (confirmed) {
    requestKakaoPay();
  }
}

// 결제 완료 승인 및 리포트 발급
function executePaymentComplete(provider, txId, amountText) {
  closeQuizModal();
  const info = getTierInfo();
  document.getElementById('receiptPackageName').innerText = info.name;
  document.getElementById('receiptProvider').innerText = provider;
  document.getElementById('receiptTxId').innerText = txId;
  document.getElementById('receiptAmount').innerText = amountText;
  document.getElementById('receiptDocs').innerText = info.docs;
  document.getElementById('reportModal').classList.add('active');
  showToast(`🎉 [${provider}] 결제 완료! 정식 리포트가 발급되었습니다!`);
}

function closeReportModal() {
  const rm = document.getElementById('reportModal');
  if (rm) rm.classList.remove('active');
}

// B2B 세대 소통 가이드북 & 사내 지출결의서 인쇄/PDF 엔진
function downloadRealReportPDF() {
  const info = getTierInfo();
  const provider = document.getElementById('receiptProvider').innerText || "카카오페이";
  const txId = document.getElementById('receiptTxId').innerText || "TX-2026-OK";
  const amount = document.getElementById('receiptAmount').innerText || info.amountText;
  const grade = document.getElementById('quizGradeText') ? document.getElementById('quizGradeText').innerText : "👑 LV.99 세대 소통 마스터";
  const score = document.getElementById('quizScoreText') ? document.getElementById('quizScoreText').innerText : "100점";
  const today = new Date().toLocaleDateString('ko-KR', { year: 'numeric', month: 'long', day: 'numeric' });

  let wordsTableRows = "";
  if (window.words) {
    window.words.forEach((w, i) => {
      let eraTag = "⚡ 요즘 밈";
      if (w.era === 'latte') eraTag = "📟 라떼";
      if (w.era === 'smartphone') eraTag = "📱 국민유행어";
      if (w.era === 'soul') eraTag = "💎 K-정서";

      wordsTableRows += `
        <tr style="border-bottom:1px solid #e2e8f0; font-size:12px;">
          <td style="padding:8px 6px; font-weight:700; color:#0f172a; text-align:center;">${i+1}</td>
          <td style="padding:8px 6px; font-weight:800; color:#2563eb;">${w.word}</td>
          <td style="padding:8px 6px; color:#64748b; text-align:center;">${eraTag}</td>
          <td style="padding:8px 6px; color:#334155;">${w.short_def}</td>
          <td style="padding:8px 6px; color:#059669; font-weight:600;">${w.standard_korean_mapping || '-'}</td>
        </tr>
      `;
    });
  }

  let expenseResolutionHtml = "";
  if (selectedTier === 2) {
    expenseResolutionHtml = `
      <div class="page-break"></div>
      <div style="border: 2px solid #0f172a; padding: 25px; border-radius: 8px; margin-top: 30px; background: #fff;">
        <div style="text-align:center; margin-bottom: 20px;">
          <h2 style="font-size:22px; font-weight:900; letter-spacing: 2px; text-decoration: underline; margin-bottom: 6px;">지 출 결 의 서 (사내 제출용)</h2>
          <p style="font-size:12px; color:#64748b;">(Expense Resolution & Tax Receipt)</p>
        </div>

        <table style="width:100%; border:1px solid #000; margin-bottom:15px; font-size:12px;">
          <tr>
            <td style="background:#f1f5f9; padding:8px; font-weight:700; width:120px; border:1px solid #cbd5e1;">발의 부서</td>
            <td style="padding:8px; border:1px solid #cbd5e1;">인사팀 / 경영지원팀 / HRD</td>
            <td style="background:#f1f5f9; padding:8px; font-weight:700; width:120px; border:1px solid #cbd5e1;">발의 일자</td>
            <td style="padding:8px; border:1px solid #cbd5e1;">${today}</td>
          </tr>
          <tr>
            <td style="background:#f1f5f9; padding:8px; font-weight:700; border:1px solid #cbd5e1;">지출 과목</td>
            <td style="padding:8px; border:1px solid #cbd5e1;">교육훈련비 / 도서인쇄비 / 복리후생비</td>
            <td style="background:#f1f5f9; padding:8px; font-weight:700; border:1px solid #cbd5e1;">결제 수단</td>
            <td style="padding:8px; border:1px solid #cbd5e1;">${provider} (승인번호: ${txId})</td>
          </tr>
          <tr>
            <td style="background:#f1f5f9; padding:8px; font-weight:700; border:1px solid #cbd5e1;">지출 금액</td>
            <td colspan="3" style="padding:8px; font-size:14px; font-weight:900; color:#0f172a; border:1px solid #cbd5e1;">
              일금 구천구백원정 (₩9,900 / 부가세 포함)
            </td>
          </tr>
          <tr>
            <td style="background:#f1f5f9; padding:8px; font-weight:700; border:1px solid #cbd5e1;">지출 목적</td>
            <td colspan="3" style="padding:8px; border:1px solid #cbd5e1;">
              신입사원-관리자 간 세대 갈등 해소 및 2026 사내 커뮤니케이션 가이드라인 교육 교재 구독료
            </td>
          </tr>
        </table>
        <p style="font-size:11px; color:#64748b; line-height:1.6;">
          위 금액을 사내 세대 소통 증진 및 조직 문화 개선비로 정히 영수 및 결의합니다.
        </p>
      </div>
    `;
  }

  const reportHtml = `<!DOCTYPE html>
<html lang="ko">
<head>
  <meta charset="UTF-8">
  <title>말쌈(MALSSAM) 공식 세대 소통 인증 리포트</title>
  <style>
    @page { size: A4; margin: 15mm; }
    body { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; color: #0f172a; background: #fff; line-height: 1.6; margin: 0; padding: 20px; }
    .page-break { page-break-before: always; }
    h1 { font-size: 24px; color: #0f172a; border-bottom: 2px solid #0f172a; padding-bottom: 8px; margin-bottom: 20px; }
    h2 { font-size: 16px; color: #1e293b; margin-top: 25px; margin-bottom: 10px; border-left: 4px solid #2563eb; padding-left: 8px; }
    table { width: 100%; border-collapse: collapse; margin-top: 10px; }
    th { background: #f8fafc; font-weight: 700; border: 1px solid #cbd5e1; padding: 8px 6px; }
    td { border: 1px solid #e2e8f0; }
  </style>
</head>
<body onload="window.print()">
  <div style="max-width: 800px; margin: 0 auto;">
    <div style="display:flex; justify-content:space-between; align-items:center; border-bottom: 3px solid #0f172a; padding-bottom: 15px; margin-bottom: 20px;">
      <div>
        <h1 style="border:none; margin:0; padding:0; font-size:26px;">말쌈 (MALSSAM) 세대 소통 공식 진단서</h1>
        <p style="color:#64748b; font-size:13px; margin:4px 0 0;">Generational Linguistics & Communication Diagnostic Certificate</p>
      </div>
      <div style="text-align:right;">
        <span style="display:inline-block; background:#0f172a; color:#fff; font-size:12px; font-weight:800; padding:4px 10px; border-radius:4px;">공식 인증</span>
        <div style="font-size:11px; color:#64748b; margin-top:4px;">발급일자: ${today}</div>
      </div>
    </div>

    <table style="margin-bottom: 25px;">
      <tr>
        <th style="width:120px;">진단 등급</th>
        <td style="font-weight:800; color:#2563eb; font-size:15px;">${grade}</td>
        <th style="width:120px;">진단 점수</th>
        <td style="font-weight:800; color:#f43f5e; font-size:15px;">${score}</td>
      </tr>
      <tr>
        <th>패키지명</th>
        <td>${info.name}</td>
        <th>승인 번호</th>
        <td style="font-family:monospace; font-size:12px;">${txId} (${provider})</td>
      </tr>
    </table>

    <h2>1. 신입사원과 팀장님을 위한 세대 소통 10계명</h2>
    <ol style="margin-left:20px; font-size:13px; color:#334155; line-height:1.8;">
      <li><strong>알잘딱깔센의 바른 활용</strong>: 지시를 모호하게 내린 후 요구하지 말고, 명확한 가이드라인 제공 후 신뢰의 의미로 사용하세요.</li>
      <li><strong>중꺾마의 동기부여</strong>: 무리한 야근 강요가 아닌 프로젝트 위기 극복을 위한 격려의 언어로 활용하세요.</li>
      <li><strong>럭키비키의 회복탄력성</strong>: 실수를 자책하기보다 '오히려 좋아!'라는 Z세대의 긍정적 전환 방식을 존중해 주세요.</li>
      <li><strong>핑프 방지 사내 지식 공유</strong>: 누구나 검색할 수 있는 사내 위키와 매뉴얼을 최신화하여 불필요한 질문을 줄이세요.</li>
      <li><strong>라떼 감성의 경청</strong>: 선배 세대의 경험과 노하우를 '꼰대'로 치부하지 않고 조직의 중요한 자산으로 수용하세요.</li>
    </ol>

    <h2>2. 3대 시대별 318종 신조어 전수 매핑 사전</h2>
    <table>
      <thead>
        <tr>
          <th style="width:35px; text-align:center;">No</th>
          <th style="width:100px;">신조어</th>
          <th style="width:85px; text-align:center;">시대 구분</th>
          <th>핵심 의미 및 뉘앙스</th>
          <th style="width:110px;">기성 표준어 매칭</th>
        </tr>
      </thead>
      <tbody>
        ${wordsTableRows}
      </tbody>
    </table>

    ${expenseResolutionHtml}

    <div style="margin-top:40px; text-align:center; border-top:1px solid #e2e8f0; padding-top:20px; font-size:12px; color:#94a3b8;">
      발행처: <strong>당목담글(DMDG) 스튜디오 연구 본부</strong> | 공식 도메인: https://malssam.com/
    </div>
  </div>
</body>
</html>`;

  const printWindow = window.open('', '_blank');
  if (printWindow) {
    printWindow.document.write(reportHtml);
    printWindow.document.close();
  }
  showToast("📥 정식 리포트 & 인쇄 화면이 새 창으로 열렸습니다!");
}
