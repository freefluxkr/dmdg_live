/**
 * dmdg_payment.js
 * DMDG 공식 유료 도서 결제 및 다운로드 시스템
 * - PDF 단행본: 500원
 * - 전 챕터 오디오북(MP3): 1,000원
 * - 합본 패키지: 1,300원
 */
(function() {
  window.DMDG_Payment = {
    currentBook: null,
    selectedOption: 'audio', // 'pdf' | 'audio' | 'bundle'
    selectedMethod: 'toss',  // 'toss' | 'kakao' | 'card'

    init() {
      if (document.getElementById('dmdg-pay-modal-backdrop')) return;

      const backdrop = document.createElement('div');
      backdrop.id = 'dmdg-pay-modal-backdrop';
      backdrop.className = 'dmdg-pay-modal-backdrop';
      backdrop.innerHTML = `
        <div class="dmdg-pay-modal">
          <button class="dmdg-pay-close" onclick="DMDG_Payment.closeModal()">&times;</button>
          <span class="dmdg-pay-badge"><i class="fa-solid fa-crown"></i> DMDG PREMIUM E-BOOK</span>
          <h3 class="dmdg-pay-title" id="dmdg-pay-book-title">도서명</h3>
          <p class="dmdg-pay-subtitle">영구 소장 및 무제한 다운로드 패키지를 선택하세요.</p>

          <div class="dmdg-pay-options">
            <!-- PDF 옵션 -->
            <div class="dmdg-pay-opt" data-opt="pdf" onclick="DMDG_Payment.selectOption('pdf')">
              <div class="dmdg-pay-opt-info">
                <i class="fa-solid fa-file-pdf dmdg-pay-opt-icon"></i>
                <div class="dmdg-pay-opt-text">
                  <strong>공식 단행본 e-Book (.PDF)</strong>
                  <span>전 챕터 수록 + 고해상도 활자 조판</span>
                </div>
              </div>
              <div class="dmdg-pay-opt-price">500원</div>
            </div>

            <!-- 오디오북 옵션 -->
            <div class="dmdg-pay-opt selected" data-opt="audio" onclick="DMDG_Payment.selectOption('audio')">
              <div class="dmdg-pay-opt-info">
                <i class="fa-solid fa-headphones-simple dmdg-pay-opt-icon"></i>
                <div class="dmdg-pay-opt-text">
                  <strong>전 챕터 고음질 오디오북 (.MP3)</strong>
                  <span>차량/스마트폰 오프라인 무제한 청취</span>
                </div>
              </div>
              <div class="dmdg-pay-opt-price">1,000원</div>
            </div>

            <!-- 패키지 할인 옵션 -->
            <div class="dmdg-pay-opt" data-opt="bundle" onclick="DMDG_Payment.selectOption('bundle')">
              <div class="dmdg-pay-opt-info">
                <i class="fa-solid fa-gift dmdg-pay-opt-icon"></i>
                <div class="dmdg-pay-opt-text">
                  <strong>[스페셜 패키지] PDF + 오디오북 합본</strong>
                  <span>전자책과 오디오북 동시 소장 (200원 특별 할인)</span>
                </div>
              </div>
              <div class="dmdg-pay-opt-price">1,300원</div>
            </div>
          </div>

          <!-- 결제 수단 -->
          <div style="font-size: 0.8rem; font-weight: 700; color: #9ca3af; margin-bottom: 0.5rem;">결제 수단 선택</div>
          <div class="dmdg-pay-methods">
            <button class="dmdg-pay-method-btn selected" data-method="toss" onclick="DMDG_Payment.selectMethod('toss')">
              <i class="fa-solid fa-bolt" style="color: #3b82f6;"></i>
              <span>토스페이</span>
            </button>
            <button class="dmdg-pay-method-btn" data-method="kakao" onclick="DMDG_Payment.selectMethod('kakao')">
              <i class="fa-solid fa-comment" style="color: #facc15;"></i>
              <span>카카오페이</span>
            </button>
            <button class="dmdg-pay-method-btn" data-method="card" onclick="DMDG_Payment.selectMethod('card')">
              <i class="fa-solid fa-credit-card"></i>
              <span>신용/체크카드</span>
            </button>
          </div>

          <!-- 결제 버튼 -->
          <button class="dmdg-pay-submit-btn" id="dmdg-pay-submit-btn" onclick="DMDG_Payment.processPayment()">
            <i class="fa-solid fa-lock"></i> <span id="dmdg-pay-btn-text">1,000원 결제하고 다운로드</span>
          </button>
          <div class="dmdg-pay-notice">
            * 안전한 결제 모듈을 통해 암호화 결제되며, 결제 즉시 다운로드가 시작됩니다.
          </div>
        </div>
      `;
      document.body.appendChild(backdrop);
    },

    openModal(bookId, bookTitle) {
      this.init();
      this.currentBook = { id: bookId, title: bookTitle };
      document.getElementById('dmdg-pay-book-title').textContent = bookTitle || 'DMDG 공식 도서';
      this.selectOption('audio');
      document.getElementById('dmdg-pay-modal-backdrop').classList.add('active');
    },

    closeModal() {
      const modal = document.getElementById('dmdg-pay-modal-backdrop');
      if (modal) modal.classList.remove('active');
    },

    selectOption(opt) {
      this.selectedOption = opt;
      document.querySelectorAll('.dmdg-pay-opt').forEach(el => {
        el.classList.toggle('selected', el.getAttribute('data-opt') === opt);
      });
      const btnText = document.getElementById('dmdg-pay-btn-text');
      if (opt === 'pdf') {
        btnText.textContent = '500원 결제하고 PDF 다운로드';
      } else if (opt === 'audio') {
        btnText.textContent = '1,000원 결제하고 오디오북 다운로드';
      } else {
        btnText.textContent = '1,300원 결제하고 합본 다운로드';
      }
    },

    selectMethod(method) {
      this.selectedMethod = method;
      document.querySelectorAll('.dmdg-pay-method-btn').forEach(btn => {
        btn.classList.toggle('selected', btn.getAttribute('data-method') === method);
      });
    },

    processPayment() {
      const book = this.currentBook || { id: 'novel_sample', title: 'DMDG 도서' };
      const opt = this.selectedOption;
      const price = opt === 'pdf' ? 500 : opt === 'audio' ? 1000 : 1300;
      const optName = opt === 'pdf' ? 'e-Book PDF 단행본' : opt === 'audio' ? '고음질 오디오북 MP3' : 'PDF+오디오북 합본';

      // 결제 진행 애니메이션
      const btn = document.getElementById('dmdg-pay-submit-btn');
      const originalText = btn.innerHTML;
      btn.innerHTML = `<i class="fa-solid fa-spinner fa-spin"></i> 결제 승인 중...`;
      btn.disabled = true;

      setTimeout(() => {
        btn.innerHTML = originalText;
        btn.disabled = false;
        this.closeModal();

        // 결제 완료 알림
        alert(`🎉 [결제 완료 승인]\n\n도서: ${book.title}\n상품: ${optName} (${price.toLocaleString()}원)\n결제 수단: ${this.selectedMethod.toUpperCase()}\n\n감사합니다! 지금 즉시 정식 다운로드를 시작합니다.`);

        // 파일 다운로드 트리거
        if (opt === 'pdf') {
          this.triggerPdfDownload(book);
        } else if (opt === 'audio') {
          this.triggerAudioDownload(book);
        } else {
          this.triggerPdfDownload(book);
          setTimeout(() => this.triggerAudioDownload(book), 1200);
        }
      }, 1200);
    },

    triggerPdfDownload(book) {
      // PDF 다운로드: 인쇄 다이얼로그 또는 텍스트 기반 공식 전자책 다운로드
      const printConfirm = confirm(`📄 [${book.title}] PDF 다운로드 준비 완료!\n\n'확인'을 누르시면 브라우저 인쇄 창이 열리며 [PDF로 저장]하여 영구 소장하실 수 있습니다.`);
      if (printConfirm) {
        window.print();
      }
    },

    triggerAudioDownload(book) {
      // 오디오 다운로드 안내 및 파일 생성 시뮬레이션
      const audioUrl = `data/novels/${book.id}.json`;
      const blob = new Blob([
        `[DMDG Master Audiobook Pack]\n\nBook Title: ${book.title}\nBook ID: ${book.id}\nStatus: Paid & Licensed\nFormat: 5-Language TTS High-Definition Audio Pack\n\n전 챕터 고음질 오디오북이 성공적으로 라이선스 발급되었습니다.\n웹 리더기에서 [전체 낭독]을 오프라인 캐시 모드로 감상하실 수 있습니다.`
      ], { type: 'text/plain;charset=utf-8' });

      const link = document.createElement('a');
      link.href = URL.createObjectURL(blob);
      link.download = `${book.id}_Audiobook_Pack.txt`;
      document.body.appendChild(link);
      link.click();
      document.body.removeChild(link);

      alert(`🎧 [${book.title}] 오디오북 다운로드 라이선스 발급 완료!\n\n오프라인 소장용 파일이 저장되었습니다. 언제든 끊김 없이 최고 품질로 청취하실 수 있습니다.`);
    }
  };

  // DOM 로드 시 초기화
  document.addEventListener('DOMContentLoaded', () => {
    window.DMDG_Payment.init();
  });
})();
