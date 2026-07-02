// Initialize Lucide Icons
lucide.createIcons();

    

    

    

    // ----------------------------------------------------
    // Global States & Multilingual Dictionary (i18n)
    // ----------------------------------------------------
    let currentLang = localStorage.getItem('preferredLang') || 'ko';
    let selectedPricing = 'weekly'; 
    let paypalRendered = false;

    // Daily free evaluation setup
    if (localStorage.getItem('dmdg_free_evals') === null) {
      localStorage.setItem('dmdg_free_evals', '3');
    }

    const i18n = {
      ko: {
        title: "당목담글",
        subtitle: "마음을 이어주는 따스한 목소리 릴레이",
        primer_type_letter: "오늘의 마중물 편지",
        primer_type_word: "오늘의 마중물 말",
        curator_haru: "따스한 감성 큐레이터 • 하루",
        curator_sakura: "맑고 생기 넘치는 큐레이터 • 사쿠라",
        curator_ren: "차분하고 정갈한 큐레이터 • 렌",
        status_initial: "아래 버튼을 눌러 목소리 마중물을 담아보세요",
        status_recording: "따뜻한 목소리를 담고 있어요... (멈추려면 탭)",
        status_processing: "목소리 분석 및 공감 멘트 생성 중...",
        status_complete: "당신의 감성과 소리가 잘 연결되었어요.",
        mic_help: "당신의 따뜻한 기운이 담겨요.",
        relay_title: "이어받은 따뜻한 소리들",
        play_audiobook: "오디오북 듣기",
        footer_notice: "위 글의 저작권은 행복한가에 있으며 모든 페이지 내용의 소유권은 행복한가에서 가지고 있습니다. 내용을 공유하실 때에는 글 하단 또는 제목에 '행복한가'를 반드시 표기 바랍니다.",
        audiobook_panel_title: "마음 오디오북 연속 재생 중",
        audiobook_finish: "오디오북을 모두 들었습니다. 감사합니다! 🍊",
        no_relays: "아직 여기에 담긴 목소리가 없어요.<br>첫 번째 마중물을 담아보세요.",
        confirm_delete: "이 따뜻한 릴레이 소리를 정말로 삭제할까요?",
        toast_offline: "지금은 연결이 끊겨 릴레이를 생성할 수 없어요.",
        toast_offline_load: "오프라인 상태입니다. 이전 릴레이를 연결하여 들려드립니다.",
        eval_title: "Gemini AI 발음 평가 성적표",
        eval_score_label: "발음 평가 점수",
        eval_good_label: "잘한 부분",
        eval_improve_label: "교정이 필요한 부분",
        eval_close_btn: "확인 완료",
        paywall_title: "Gemini AI 정밀 진단 횟수 초과",
        paywall_desc: "오늘의 무료 AI 발음 평가 3회를 모두 사용하셨습니다.<br>유료 프리미엄 멤버십으로 24시간 언제든 정밀 과외를 즐겨보세요!",
        paywall_pass: "주간 자유 패스",
        paywall_pass_desc: "매주 무제한 발음 피드백",
        paywall_coin: "30 코인 충전",
        paywall_coin_desc: "30회 정밀 성적표 발급",
        paywall_btn: "프리미엄 멤버십 시작하기",
        paywall_notice: "성공적으로 결제되었습니다! 프리미엄 혜택을 누리세요.",
        premium_title: "프리미엄 전용 기능",
        premium_overlay_desc: "일일 무료 체험 3회가 완료되었습니다.<br>PayPal 결제 후 정밀 분석 결과를 확인해 보세요!",
        premium_unlock_btn: "멤버십 잠금해제 🔓",
        price_pass: "₩2,900 / 주",
        price_coin: "₩4,900 / 1회성",
        delete_alert: "릴레이가 성공적으로 삭제되었습니다.",
        emotion_all: "전체",
        emotion_comfort: "위로",
        emotion_romance: "설렘",
        emotion_calm: "평온",
        privacy_banner: "🍊 모든 음성 데이터는 사용자의 기기에만 안전하게 저장됩니다 (Local Storage Only)",
        benefit_banner: "🎁 목소리 기부 시 AI 분석 무료 5회 충전! [자세히 보기]",
        benefit_modal_title: "목소리 기부 혜택 안내",
        donate_modal_title: "목소리 온기 나누기",
        donate_invite: "세상에 목소리를 기부하고 AI 발음 분석 무료 5회권을 받으시겠어요? 🎁",
        donate_btn: "목소리 기부하고 5회 얻기",
        donate_skip: "그냥 로컬에만 저장할래요",
        donate_success: "기부가 완료되어 AI 분석 무료 5회권이 추가 적립되었습니다!",
        gemini_key_title: "Gemini API 설정",
        gemini_key_desc: "70개국 실시간 감성 번역을 사용하기 위해 개인 Gemini API Key를 등록해 주세요. 키는 기기 로컬에만 안전하게 보관됩니다. (※ 발음 성적표는 API Key가 없어도 무료로 자동 작동합니다!)",
        gemini_key_placeholder: "API Key를 입력하세요 (AIzaSy...)",
        gemini_key_save: "저장하기",
        gemini_key_needed: "번역 기능을 사용하려면 우측 상단 톱니바퀴를 눌러 Gemini API Key를 먼저 등록해 주세요.",
        dashboard_title: "글로벌 온기 분석 대시보드",
        dashboard_desc: "기부가 쌓일수록 지구촌의 온도가 올라갑니다.",
        stat_donations: "누적 기부 소리",
        stat_chains: "누적 릴레이 체인",
        cancel_btn: "취소",
        translate_btn: "Gemini 실시간 번역",
        translate_loading: "감성 번역 중..."
      },
      ja: {
        title: "心をつなぐ、声のリレー",
        subtitle: "世界で一番温かい朗読プラットフォーム。",
        primer_type_letter: "今日の呼び水の手紙",
        primer_type_word: "今日の呼び水の言葉",
        curator_haru: "温かい感性キュレーター • ハル",
        curator_sakura: "明るく活気のあるキュレーター • サクラ",
        curator_ren: "物静かで端正なキュレーター • レン",
        status_initial: "下のボタンを押して、声の呼び水を吹き込んでみてください",
        status_recording: "温かい声を録音しています... (停止するにはタップ)",
        status_processing: "音声分析および共感コメントを生成中...",
        status_complete: "あなたの感性と声がしっかりとつながりました。",
        mic_help: "あなたの温かい気持ちが込められます。",
        relay_title: "受け継がれた温かい声",
        play_audiobook: "オーディオブックを聴く",
        footer_notice: "上記文章の著作権は「ヘンボカンガ(幸せな家)」にあり、すべてのコンテンツの所有権も同社に帰属します。外部への共有時は必ず出所を明記してください。",
        audiobook_panel_title: "心オーディオブック連続再生中",
        audiobook_finish: "オーディオブックをすべて聴き終えました。ありがとうございます！🍊",
        no_relays: "まだここに吹き込まれた声がありません。<br>最初の呼び水を吹き込んでみてください。",
        confirm_delete: "この温かいリレー音声を本当に削除しますか？",
        toast_offline: "現在はオフラインのため、リレーを作成できません。",
        toast_offline_load: "オフライン状態です。過去のリレーを繋げてお聴かせします。",
        eval_title: "Gemini AI 発音評価成績表",
        eval_score_label: "発音評価点数",
        eval_good_label: "良かった点",
        eval_improve_label: "改善が必要な点",
        eval_close_btn: "確認完了",
        paywall_title: "Gemini AI 精密診断回数超過",
        paywall_desc: "本日の無料AI発音評価(3回)をすべて使用しました。<br>有料プレミアムメンバーシップで、24時間いつでも詳細な発音フィードバックを受け取りましょう！",
        paywall_pass: "週間フリーパス",
        paywall_pass_desc: "毎週無制限の発音フィードバック",
        paywall_coin: "30コインチャージ",
        paywall_coin_desc: "30回の精密成績表発行",
        paywall_btn: "プレミアムメンバーシップを開始する",
        paywall_notice: "決済が完了しました！プレミアム特典をお楽しみください。",
        premium_title: "プレミアム専用機能",
        premium_overlay_desc: "本日の無料体験3回が終了しました。<br>PayPal決済後、精密分析結果を確認してください！",
        premium_unlock_btn: "メンバーシップ解除 🔓",
        price_pass: "¥290 / 週",
        price_coin: "¥490 / 一回限り",
        delete_alert: "リレーが正常に削除されました.",
        emotion_all: "すべて",
        emotion_comfort: "慰め",
        emotion_romance: "ときめき",
        emotion_calm: "平穏",
        privacy_banner: "🍊 すべてのデータはあなたのデバイスに。安心のローカル保存で、心おきなく表現を。(サーバー送信なし)",
        benefit_banner: "🎁 声を寄付するとAI分析が5回無料チャージ！[詳細を見る]",
        benefit_modal_title: "声の寄付特典のご案内",
        donate_modal_title: "声のぬくもりを分かち合う",
        donate_invite: "世界にあなたの声を寄付して、無料AI発音分析5回分を受け取りますか？ 🎁",
        donate_btn: "声を寄付して5回分獲得",
        donate_skip: "ローカルにのみ保存する",
        donate_success: "寄付が完了し、無料AI分析5回分が追加されました！",
        gemini_key_title: "Gemini API 設定",
        gemini_key_desc: "70ヶ国のリアルタイム感性翻訳を使用するため、個人인 Gemini API Keyを登録してください。キーはデバイスローカルに安全に保管されます。(※ 発音成績表はAPI Keyがなくても無料で自動動作します！)",
        gemini_key_placeholder: "API Keyを入力してください (AIzaSy...)",
        gemini_key_save: "保存する",
        gemini_key_needed: "翻訳機能を使用するには、右上の歯車ボタンを押してGemini API Keyを登録してください。",
        dashboard_title: "グローバル温もり分析ダッシュボード",
        dashboard_desc: "寄付が集まるほど、地球の温度が上がります。",
        stat_donations: "累積寄付された声",
        stat_chains: "累積リレーチェーン",
        cancel_btn: "キャンセル",
        translate_btn: "Gemini リアルタイム翻訳",
        translate_loading: "感性翻訳中..."
      },
      en: {
        title: "Bridging Cultures",
        subtitle: "One Voice at a Time. The privacy-first platform.",
        primer_type_letter: "Today's Primer Letter",
        primer_type_word: "Today's Primer Word",
        curator_haru: "Warm Curator • Haru",
        curator_sakura: "Bright & Cheerful Curator • Sakura",
        curator_ren: "Calm & Serene Curator • Ren",
        status_initial: "Tap the button below to record your warm voice",
        status_recording: "Recording your warm voice... (Tap to stop)",
        status_processing: "Analyzing voice & generating empathy reply...",
        status_complete: "Your emotion and voice have been connected.",
        mic_help: "Your warm energy will be captured.",
        relay_title: "Warm Voices Passed On",
        play_audiobook: "Play Audiobook",
        footer_notice: "The copyright of the text belongs to Happy House, and all page ownership is retained by them. Please credit 'Happy House' when sharing.",
        audiobook_panel_title: "Audiobook Auto-Playing",
        audiobook_finish: "Finished playing the audiobook. Thank you! 🍊",
        no_relays: "No voices have been shared here yet.<br>Be the first to share your warm voice.",
        confirm_delete: "Are you sure you want to delete this warm relay voice?",
        toast_offline: "Offline. Cannot create a new relay at this moment.",
        toast_offline_load: "Offline. Playing previously saved relay tracks.",
        eval_title: "Gemini AI Pronunciation Scorecard",
        eval_score_label: "PRONUNCIATION SCORE",
        eval_good_label: "Strengths",
        eval_improve_label: "Areas to Improve",
        eval_close_btn: "Confirm",
        paywall_title: "Gemini AI Limit Reached",
        paywall_desc: "You have used all 3 free AI pronunciation evaluations for today.<br>Upgrade to premium to enjoy unlimited accurate feedback 24/7!",
        paywall_pass: "Weekly Free Pass",
        paywall_pass_desc: "Unlimited pronunciation feedback weekly",
        paywall_coin: "Charge 30 Coins",
        paywall_coin_desc: "Issue 30 detailed scorecards",
        paywall_btn: "Start Premium Membership",
        paywall_notice: "Payment successful! Enjoy your premium benefits.",
        premium_title: "Premium Feature Only",
        premium_overlay_desc: "Your 3 daily free evaluations have ended.<br>Unlock detailed breakdown with PayPal checkout!",
        premium_unlock_btn: "Unlock Membership 🔓",
        price_pass: "$1.99 / wk",
        price_coin: "$3.99 / one-time",
        delete_alert: "Relay successfully deleted.",
        emotion_all: "All",
        emotion_comfort: "Comfort",
        emotion_romance: "Flutter",
        emotion_calm: "Calm",
        privacy_banner: "🍊 No cloud, no compromise. Your voice stays exclusively on your device.",
        benefit_banner: "🎁 Donate your voice to get 5 free AI evaluations! [Learn More]",
        benefit_modal_title: "Voice Donation Rewards",
        donate_modal_title: "Share Your Warm Voice",
        donate_invite: "Would you like to donate your voice and receive 5 free AI evaluations? 🎁",
        donate_btn: "Donate Voice & Get 5 Evals",
        donate_skip: "Save locally only",
        donate_success: "Donation successful! 5 free AI evaluations added.",
        gemini_key_title: "Gemini API Settings",
        gemini_key_desc: "Please register your personal Gemini API Key to use real-time emotional translation in 70+ languages. The key is securely stored only on your local device.",
        gemini_key_placeholder: "Enter API Key (AIzaSy...)",
        gemini_key_save: "Save Key",
        gemini_key_needed: "To use the translation feature, please register your Gemini API Key by tapping the gear icon at the top right first.",
        dashboard_title: "Global Warmth Analytics Dashboard",
        dashboard_desc: "As donations collect, the global temperature rises.",
        stat_donations: "Total Donated Voices",
        stat_chains: "Total Relay Chains",
        cancel_btn: "Cancel",
        translate_btn: "Gemini Live Translate",
        translate_loading: "Translating..."
      },
      fr: {
        title: "Reliant les Cultures",
        subtitle: "Une Voix à la Fois.",
        primer_type_letter: "Lettre d'Amorce du Jour",
        primer_type_word: "Mot d'Amorce du Jour",
        curator_haru: "Curateur Chaleureux • Haru",
        curator_sakura: "Curateur Joyeux • Sakura",
        curator_ren: "Curateur Calme • Ren",
        status_initial: "Appuyez sur le bouton ci-dessous",
        status_recording: "Enregistrement en cours...",
        status_processing: "Analyse en cours...",
        status_complete: "Votre chaleur est connectée.",
        mic_help: "Votre énergie chaleureuse est capturée.",
        relay_title: "Voix Chaleureuses Transmises",
        play_audiobook: "Écouter l'Audiobook",
        footer_notice: "Copyright Happy House.",
        audiobook_panel_title: "Audiobook en Lecture",
        audiobook_finish: "Lecture terminée. Merci ! 🍊",
        no_relays: "Aucune voix partagée ici pour le moment.",
        confirm_delete: "Voulez-vous vraiment supprimer cette voix ?",
        toast_offline: "Hors ligne. Impossible de créer un relais.",
        toast_offline_load: "Hors ligne. Lecture des relais sauvegardés.",
        eval_title: "Évaluation Gemini AI",
        eval_score_label: "SCORE DE PRONONCIATION",
        eval_good_label: "Points Forts",
        eval_improve_label: "À Améliorer",
        eval_close_btn: "Confirmer",
        paywall_title: "Limite Gemini AI Atteinte",
        paywall_desc: "Vous avez utilisé toutes vos évaluations gratuites.",
        paywall_pass: "Pass Hebdomadaire",
        paywall_pass_desc: "Évaluations illimitées",
        paywall_coin: "30 Pièces",
        paywall_coin_desc: "30 évaluations",
        paywall_btn: "Devenir Premium",
        paywall_notice: "Paiement réussi !",
        premium_title: "Premium Uniquement",
        premium_overlay_desc: "Vos essais gratuits sont épuisés.",
        premium_unlock_btn: "Débloquer 🔓",
        price_pass: "€0.99 / sem",
        price_coin: "€1.99 / une fois",
        delete_alert: "Relais supprimé avec succès.",
        emotion_all: "Tout",
        emotion_comfort: "Réconfort",
        emotion_romance: "Papillons",
        emotion_calm: "Calme",
        privacy_banner: "🍊 Vos données restent sur votre appareil.",
        benefit_banner: "🎁 Donnez votre voix, obtenez 5 analyses gratuites !",
        benefit_modal_title: "Récompenses de Don",
        donate_modal_title: "Partagez Votre Chaleur",
        donate_invite: "Voulez-vous donner votre voix ?",
        donate_btn: "Donner et Obtenir 5 Analyses",
        donate_skip: "Sauvegarder localement",
        donate_success: "Don réussi ! 5 analyses gratuites ajoutées.",
        gemini_key_title: "Paramètres API Gemini",
        gemini_key_desc: "Veuillez enregistrer votre clé API Gemini.",
        gemini_key_placeholder: "Clé API (AIzaSy...)",
        gemini_key_save: "Sauvegarder",
        gemini_key_needed: "Veuillez enregistrer votre clé API Gemini en haut à droite.",
        dashboard_title: "Tableau de Bord Global",
        dashboard_desc: "La température globale augmente avec les dons.",
        stat_donations: "Voix Données",
        stat_chains: "Chaînes de Relais",
        cancel_btn: "Annuler",
        translate_btn: "Traduction Gemini",
        translate_loading: "Traduction..."
      },
      de: {
        title: "Kulturen Verbinden",
        subtitle: "Eine Stimme nach der anderen.",
        primer_type_letter: "Heutiger Impulsbrief",
        primer_type_word: "Heutiges Impulswort",
        curator_haru: "Warmer Kurator • Haru",
        curator_sakura: "Fröhlicher Kurator • Sakura",
        curator_ren: "Ruhiger Kurator • Ren",
        status_initial: "Tippen Sie auf die Schaltfläche unten",
        status_recording: "Aufzeichnung läuft...",
        status_processing: "Analyse läuft...",
        status_complete: "Ihre Wärme ist verbunden.",
        mic_help: "Ihre warme Energie wird eingefangen.",
        relay_title: "Weitergegebene Warme Stimmen",
        play_audiobook: "Hörbuch Abspielen",
        footer_notice: "Copyright Happy House.",
        audiobook_panel_title: "Hörbuch läuft",
        audiobook_finish: "Hörbuch beendet. Danke! 🍊",
        no_relays: "Noch keine Stimmen hier geteilt.",
        confirm_delete: "Möchten Sie diese Stimme wirklich löschen?",
        toast_offline: "Offline. Relay kann nicht erstellt werden.",
        toast_offline_load: "Offline. Gespeicherte Relays werden abgespielt.",
        eval_title: "Gemini AI Bewertung",
        eval_score_label: "AUSSPRACHE-SCORE",
        eval_good_label: "Stärken",
        eval_improve_label: "Zu Verbessern",
        eval_close_btn: "Bestätigen",
        paywall_title: "Gemini AI Limit Erreicht",
        paywall_desc: "Sie haben alle kostenlosen Bewertungen aufgebraucht.",
        paywall_pass: "Wochenpass",
        paywall_pass_desc: "Unbegrenzte Bewertungen",
        paywall_coin: "30 Münzen",
        paywall_coin_desc: "30 Bewertungen",
        paywall_btn: "Premium Werden",
        paywall_notice: "Zahlung erfolgreich!",
        premium_title: "Nur Premium",
        premium_overlay_desc: "Ihre kostenlosen Versuche sind aufgebraucht.",
        premium_unlock_btn: "Freischalten 🔓",
        price_pass: "€0.99 / Wo",
        price_coin: "€1.99 / Einmalig",
        delete_alert: "Relay erfolgreich gelöscht.",
        emotion_all: "Alle",
        emotion_comfort: "Trost",
        emotion_romance: "Schmetterlinge",
        emotion_calm: "Ruhe",
        privacy_banner: "🍊 Ihre Daten bleiben auf Ihrem Gerät.",
        benefit_banner: "🎁 Spenden Sie Ihre Stimme für 5 kostenlose Analysen!",
        benefit_modal_title: "Spendenbelohnungen",
        donate_modal_title: "Teilen Sie Ihre Wärme",
        donate_invite: "Möchten Sie Ihre Stimme spenden?",
        donate_btn: "Spenden & 5 Analysen Erhalten",
        donate_skip: "Nur lokal speichern",
        donate_success: "Spende erfolgreich! 5 Analysen hinzugefügt.",
        gemini_key_title: "Gemini API Einstellungen",
        gemini_key_desc: "Bitte registrieren Sie Ihren API-Schlüssel.",
        gemini_key_placeholder: "API-Schlüssel (AIzaSy...)",
        gemini_key_save: "Speichern",
        gemini_key_needed: "Bitte API-Schlüssel oben rechts registrieren.",
        dashboard_title: "Globales Dashboard",
        dashboard_desc: "Die globale Temperatur steigt mit Spenden.",
        stat_donations: "Gespendete Stimmen",
        stat_chains: "Relay-Ketten",
        cancel_btn: "Abbrechen",
        translate_btn: "Gemini Übersetzung",
        translate_loading: "Übersetze..."
      }
    };

    // Toggle Language Dropdown
    function toggleLangDropdown() {
      const dropdown = document.getElementById('lang-dropdown');
      dropdown.classList.toggle('hidden');
    }

    // Change Current App Language
    function changeLanguage(lang) {
      currentLang = lang;
      localStorage.setItem('preferredLang', lang);
      setLanguage(lang);
      applyCountryTheme(lang);   // 🎨 국가 테마 즉시 전환
      toggleLangDropdown();

      // 마중물 텍스트 번역 업데이트
      const translationBox = document.getElementById('primer-translation-box');
      if (lang === 'ko') {
        translationBox.classList.add('hidden');
      } else {
        if (typeof triggerPrimerTranslation === 'function') {
          triggerPrimerTranslation();
        }
      }

      // Show welcome toast message matching the language/country
      const welcomeMessages = {
        ko: "당목담글에 오신 것을 환영합니다! 🇰🇷",
        ja: "心をつなぐリレーへようこそ！🇯🇵",
        en: "Welcome to Dangmokdamgeul! 🇺🇸",
        fr: "Bienvenue sur Dangmokdamgeul ! 🇫🇷",
        de: "Willkommen bei Dangmokdamgeul! 🇩🇪"
      };
      if (typeof showToast === 'function') {
        showToast(welcomeMessages[lang] || welcomeMessages['ko']);
      }
    }

    // ============================================================
    //  🇰🇷 국가별 테마 디자인 시스템 (Local-First · CSS Variable 기반)
    //  국가를 추가할 때 countryThemes 객체만 수정하면 됩니다.
    // ============================================================
    const countryThemes = {
      ko: {
        // 🇰🇷 태극기 — 열정의 홍 × 신뢰의 청 × 한지 베이지
        '--theme-primary':        '#CD2E3A',
        '--theme-primary-dark':   '#a82230',
        '--theme-secondary':      '#0047A0',
        '--theme-secondary-dark': '#003580',
        '--theme-accent':         '#e8532b',
        '--theme-glow':           'rgba(205, 46, 58, 0.30)',
        '--theme-glow-blue':      'rgba(0, 71, 160, 0.20)',
        '--theme-bg-circle1':     'rgba(205, 46, 58, 0.12)',
        '--theme-bg-circle2':     'rgba(0, 71, 160, 0.10)',
        '--theme-bg-page':        '#f0ece6',
        '--theme-connector':      'linear-gradient(to right, #0047A0, #CD2E3A)',
        '--theme-border':         'rgba(205, 46, 58, 0.15)',
        '--theme-text-body':      '#1A1A1A',
        '--theme-text-muted':     '#4a4a4a',
        '--theme-text-dark':      '#f8f5f2',
        '--theme-text-deep':      '#ffffff',
        metaColor: '#CD2E3A',
        flag: '🇰🇷',
        bodyBg: '#f0ece6'
      },
      ja: {
        // 🇯🇵 일장기 — 차분한 적색 × 모노크롬 × 화지 크림
        '--theme-primary':        '#BC002D',
        '--theme-primary-dark':   '#8f0021',
        '--theme-secondary':      '#444444',
        '--theme-secondary-dark': '#222222',
        '--theme-accent':         '#d9534f',
        '--theme-glow':           'rgba(188, 0, 45, 0.28)',
        '--theme-glow-blue':      'rgba(68, 68, 68, 0.18)',
        '--theme-bg-circle1':     'rgba(188, 0, 45, 0.10)',
        '--theme-bg-circle2':     'rgba(100, 100, 100, 0.08)',
        '--theme-bg-page':        '#faf7f4',
        '--theme-connector':      'linear-gradient(to right, #444444, #BC002D)',
        '--theme-border':         'rgba(188, 0, 45, 0.14)',
        '--theme-text-body':      '#1A1A1A',
        '--theme-text-muted':     '#555555',
        '--theme-text-dark':      '#f5f0ed',
        '--theme-text-deep':      '#ffffff',
        metaColor: '#BC002D',
        flag: '🇯🇵',
        bodyBg: '#faf7f4'
      },
      en: {
        // 🇺🇸 성조기 — 독립의 빨강 × 자유의 파랑 × 스타 화이트
        '--theme-primary':        '#B22234',
        '--theme-primary-dark':   '#8a1928',
        '--theme-secondary':      '#3C3B6E',
        '--theme-secondary-dark': '#2c2b52',
        '--theme-accent':         '#c0392b',
        '--theme-glow':           'rgba(178, 34, 52, 0.28)',
        '--theme-glow-blue':      'rgba(60, 59, 110, 0.22)',
        '--theme-bg-circle1':     'rgba(178, 34, 52, 0.10)',
        '--theme-bg-circle2':     'rgba(60, 59, 110, 0.09)',
        '--theme-bg-page':        '#f7f4f1',
        '--theme-connector':      'linear-gradient(to right, #3C3B6E, #B22234)',
        '--theme-border':         'rgba(178, 34, 52, 0.14)',
        '--theme-text-body':      '#1A1A1A',
        '--theme-text-muted':     '#4a4a4a',
        '--theme-text-dark':      '#f5f2ef',
        '--theme-text-deep':      '#ffffff',
        metaColor: '#B22234',
        flag: '🇺🇸',
        bodyBg: '#f7f4f1',
        motif: 'star'        // ⭐ 성조기 별 모티브
      },
      fr: {
        // 🇫🇷 삼색기 — 감성의 청 × 자유의 적 × 크림 화이트
        '--theme-primary':        '#0055A4',
        '--theme-primary-dark':   '#003f7c',
        '--theme-secondary':      '#EF4135',
        '--theme-secondary-dark': '#c4281e',
        '--theme-accent':         '#d63031',
        '--theme-glow':           'rgba(0, 85, 164, 0.28)',
        '--theme-glow-blue':      'rgba(239, 65, 53, 0.22)',
        '--theme-bg-circle1':     'rgba(0, 85, 164, 0.10)',
        '--theme-bg-circle2':     'rgba(239, 65, 53, 0.09)',
        '--theme-bg-page':        '#f9f7f4',
        '--theme-connector':      'linear-gradient(to right, #0055A4, #EF4135)',
        '--theme-border':         'rgba(0, 85, 164, 0.15)',
        '--theme-text-body':      '#1A1A1A',
        '--theme-text-muted':     '#4a4a4a',
        '--theme-text-dark':      '#f2f0ef',
        '--theme-text-deep':      '#ffffff',
        metaColor: '#0055A4',
        flag: '🇫🇷',
        bodyBg: '#f9f7f4',
        motif: 'tricolor'   // 🔵⚪🔴 삼색 세로선 모티브
      },
      de: {
        // 🇩🇪 삼색기 — 전문성의 금 × 열정의 적 × 근엄한 검정
        '--theme-primary':        '#DD0000',
        '--theme-primary-dark':   '#aa0000',
        '--theme-secondary':      '#FFCE00',
        '--theme-secondary-dark': '#d4a800',
        '--theme-accent':         '#e8a000',
        '--theme-glow':           'rgba(221, 0, 0, 0.28)',
        '--theme-glow-blue':      'rgba(255, 206, 0, 0.30)',
        '--theme-bg-circle1':     'rgba(221, 0, 0, 0.10)',
        '--theme-bg-circle2':     'rgba(255, 206, 0, 0.12)',
        '--theme-bg-page':        '#fafaf8',
        '--theme-connector':      'linear-gradient(to right, #222222, #DD0000)',
        '--theme-border':         'rgba(221, 0, 0, 0.15)',
        '--theme-text-body':      '#1A1A1A',
        '--theme-text-muted':     '#3a3a3a',
        '--theme-text-dark':      '#f5f5f0',
        '--theme-text-deep':      '#ffffff',
        metaColor: '#DD0000',
        flag: '🇩🇪',
        bodyBg: '#fafaf8',
        motif: 'grid'       // ▬▬▬ 삼색 가로띠(그리드) 모티브
      }
    };

    // 테마 적용 핵심 함수 — CSS 변수를 실시간으로 교체 (서버 통신 없음)
    function applyCountryTheme(lang) {
      const theme = countryThemes[lang] || countryThemes['ko'];
      const root = document.documentElement;

      // CSS 변수 일괄 적용 (메타 전용 키 제외)
      const skipKeys = ['metaColor', 'flag', 'bodyBg', 'motif'];
      Object.keys(theme).forEach(key => {
        if (!skipKeys.includes(key)) {
          root.style.setProperty(key, theme[key]);
        }
      });

      // body 배경색 부드럽게 전환
      document.body.style.background = theme.bodyBg;
      document.body.style.backgroundImage =
        `radial-gradient(ellipse 70% 50% at 20% 10%, ${theme['--theme-bg-circle1']} 0%, transparent 60%),
         radial-gradient(ellipse 60% 50% at 80% 90%, ${theme['--theme-bg-circle2']} 0%, transparent 60%)`;

      // 🎨 국기 상징 요소(Motif) 적용 — 국가별 기하학적 정체성 부여
      applyThemeMotif(theme.motif || 'none');

      // 오디오북 패널 테두리 색상
      const audiobookPanel = document.getElementById('audiobook-player');
      if (audiobookPanel) {
        audiobookPanel.style.borderTopColor = theme['--theme-primary'];
      }

      // PWA 스마트폰 상태바 색상
      const themeMeta = document.querySelector('meta[name="theme-color"]');
      if (themeMeta) themeMeta.setAttribute('content', theme.metaColor);

      // 상단 국기 플래그 아이콘 갱신
      const flagIcon = document.getElementById('lang-flag-icon');
      if (flagIcon) flagIcon.textContent = theme.flag;

      // localStorage에 국가 기억 (다음 방문 복원용)
      localStorage.setItem('selected-country', lang);
    }

    // 국기 상징 기하학 요소를 body data-motif 속성으로 제어
    // CSS에서 [data-motif="circle"] 등으로 스타일링 가능
    function applyThemeMotif(motif) {
      document.body.setAttribute('data-motif', motif);
      // 예: 'circle' = 일장기 원형, 'tricolor' = 프랑스 세로선, 'grid' = 독일 가로띠
    }

    // 하위 호환성 유지 (기존 applyFlagTheme 호출 코드 대응)
    window.applyFlagTheme = applyCountryTheme;
    window.applyCountryTheme = applyCountryTheme;

    // Apply translation to all HTML elements with data-i18n
    function setLanguage(lang) {
      const dict = i18n[lang] || i18n['ko'];
      const freeEvals = localStorage.getItem('dmdg_free_evals') || '3';

      document.querySelectorAll('[data-i18n]').forEach(el => {
        const key = el.getAttribute('data-i18n');
        if (dict[key]) {
          let text = dict[key];
          if (key === 'benefit_banner') {
            const countSuffix = {
              ko: ` (남은 무료 분석: ${freeEvals}회)`,
              ja: ` (残り無料分析: ${freeEvals}回)`,
              en: ` (${freeEvals} free evals left)`
            };
            text += countSuffix[lang] || countSuffix['ko'];
          }
          el.innerHTML = text;
        }
      });

      // Price tags dynamic update
      const passPrice = document.getElementById('price-pass');
      const coinPrice = document.getElementById('price-coin');
      if (passPrice) passPrice.textContent = dict.price_pass || '';
      if (coinPrice) coinPrice.textContent = dict.price_coin || '';

      // Re-trigger visualizer status text if active
      const statusEl = document.getElementById('status-message');
      if (statusEl) {
        if (!isRecording && statusEl.getAttribute('data-i18n') === 'status_initial') {
          statusEl.textContent = dict.status_initial;
        }
      }

      // Re-draw PayPal buttons to reflect correct currencies if paywall is loaded
      if (paypalRendered) {
        renderPaypalButtons();
      }
    }

    // ----------------------------------------------------
    // Hangul Jamo Disassembler & Evaluation Algorithms
    // ----------------------------------------------------
    const CHO_LIST = ['ㄱ', 'ㄲ', 'ㄴ', 'ㄷ', 'ㄸ', 'ㄹ', 'ㅁ', 'ㅂ', 'ㅃ', 'ㅅ', 'ㅆ', 'ㅇ', 'ㅈ', 'ㅉ', 'ㅊ', 'ㅋ', 'ㅌ', 'ㅍ', 'ㅎ'];
    const JUNG_LIST = ['ㅏ', 'ㅐ', 'ㅑ', 'ㅒ', 'ㅓ', 'ㅔ', 'ㅕ', 'ㅖ', 'ㅗ', 'ㅘ', 'ㅙ', 'ㅚ', 'ㅛ', 'ㅜ', 'ㅝ', 'ㅞ', 'ㅟ', 'ㅠ', 'ㅡ', 'ㅢ', 'ㅣ'];
    const JONG_LIST = ['', 'ㄱ', 'ㄲ', 'ㄳ', 'ㄴ', 'ㄵ', 'ㄶ', 'ㄷ', 'ㄹ', 'ㄺ', 'ㄻ', 'ㄼ', 'ㄽ', 'ㄾ', 'ㄿ', 'ㅀ', 'ㅁ', 'ㅂ', 'ㅄ', 'ㅅ', 'ㅆ', 'ㅇ', 'ㅈ', 'ㅊ', 'ㅋ', 'ㅌ', 'ㅍ', 'ㅎ'];

    function disassembleHangul(text) {
      let result = "";
      for (let i = 0; i < text.length; i++) {
        const char = text[i];
        const code = char.charCodeAt(0) - 0xAC00;
        if (code >= 0 && code < 11172) {
          const jong = code % 28;
          const jung = Math.floor((code - jong) / 28) % 21;
          const cho = Math.floor(Math.floor((code - jong) / 28) / 21);
          result += CHO_LIST[cho] + JUNG_LIST[jung] + (JONG_LIST[jong] || "");
        } else {
          result += char;
        }
      }
      return result;
    }

    function getLevenshteinDistance(a, b) {
      if (a.length === 0) return b.length;
      if (b.length === 0) return a.length;
      const matrix = [];
      for (let i = 0; i <= b.length; i++) {
        matrix[i] = [i];
      }
      for (let j = 0; j <= a.length; j++) {
        matrix[0][j] = j;
      }
      for (let i = 1; i <= b.length; i++) {
        for (let j = 1; j <= a.length; j++) {
          if (b.charAt(i - 1) === a.charAt(j - 1)) {
            matrix[i][j] = matrix[i - 1][j - 1];
          } else {
            matrix[i][j] = Math.min(
              matrix[i - 1][j - 1] + 1,
              Math.min(
                matrix[i][j - 1] + 1,
                matrix[i - 1][j] + 1
              )
            );
          }
        }
      }
      return matrix[b.length][a.length];
    }

    function calculateJamoSimilarity(text1, text2) {
      const jamo1 = disassembleHangul(text1).replace(/[^ㄱ-ㅎㅏ-ㅣa-zA-Z0-9]/g, "");
      const jamo2 = disassembleHangul(text2).replace(/[^ㄱ-ㅎㅏ-ㅣa-zA-Z0-9]/g, "");
      if (jamo1.length === 0 || jamo2.length === 0) return 0;
      const distance = getLevenshteinDistance(jamo1, jamo2);
      const maxLength = Math.max(jamo1.length, jamo2.length);
      return Math.round((1 - distance / maxLength) * 100);
    }

    // 2안: 초·중·종성 한글 자모 해체 알고리즘(Disassembler) 기반 음절별 신호등 컬러 뷰 렌더링
    function gradeHangulSyllables(originalText, recognizedText) {
      const container = document.getElementById('evaluation-visual-feedback');
      container.innerHTML = '';
      
      const origClean = originalText.replace(/[^가-힣a-zA-Z0-9\s]/g, "");
      const recogClean = recognizedText.replace(/[^가-힣a-zA-Z0-9\s]/g, "");
      
      const origChars = origClean.split('');
      const recogChars = recogClean.split('');
      
      origChars.forEach((char, idx) => {
        if (char === ' ' || char === '\n') {
          const space = document.createElement('span');
          space.innerHTML = '&nbsp;';
          container.appendChild(space);
          return;
        }
        
        let maxScore = 0;
        const startScan = Math.max(0, idx - 4);
        const endScan = Math.min(recogChars.length, idx + 5);
        
        for (let s = startScan; s < endScan; s++) {
          const rChar = recogChars[s];
          if (!rChar || rChar === ' ') continue;
          const score = calculateJamoSimilarity(char, rChar);
          if (score > maxScore) {
            maxScore = score;
          }
        }
        
        const span = document.createElement('span');
        span.textContent = char;
        span.className = "px-0.5 rounded transition-all font-bold select-none ";
        
        if (maxScore >= 90) {
          span.className += "text-green-600 bg-green-50/70 border-b-2 border-green-300"; 
        } else if (maxScore >= 55) {
          span.className += "text-yellow-600 bg-yellow-50/70 border-b-2 border-yellow-300"; 
        } else {
          span.className += "text-red-500 bg-rose-50/70 border-b-2 border-rose-300"; 
        }
        container.appendChild(span);
      });
    }

    async function loadPrimersFromDB() {
      try {
        const isOnline = navigator.onLine;
        
        if (isOnline) {
          console.log("Firebase Firestore에서 마중물 데이터를 로드합니다.");
          const primersCol = firestore.collection("primers");
          const checkSnapshot = await primersCol.limit(1).get();
          
          if (checkSnapshot.empty) {
            console.log("Firestore primers 컬렉션이 비어있습니다. 행복한가 데이터를 적재합니다.");
            const seedLetters = [
              {
                category: "일상스토리",
                emotion: "위로",
                title: "삶의 방향을 잃은 당신에게",
                content: "“삶이 어디로 향하고 있는지 방향을 잃은 것 같다고 느끼는 분들께 이런 말을 해주고 싶어요. '나는 이런 사람이야' 하면서 자신을 가두거나, '나는 안 맞아' 하면서 미리 포기하지 마세요. 부디 자기 인생을 다른 사람과 비교하며 비참해지지 않았으면 좋겠습니다.” — 김창완 <이제야 보이네> 중에서",
                translation: { ja: "「人生がどこに向かっているのか、方向を見失ったと感じている方々に、こんな言葉を贈りたいです。『私はこういう人間だから』と自分を閉じ込めたり、『自分には合わない』と最初から諦めたりしないでください」 — キム・チャンワン『やっと見えるね』より", en: "“To those who feel they have lost their direction in life, I want to say this. Don't trap yourself by saying 'I'm this kind of person,' or give up in advance saying 'It doesn't suit me.'” — From Kim Chang-wan <Only Now I See>" },
                type: "오늘의 편지"
              },
              {
                category: "일상스토리",
                emotion: "위로",
                title: "그늘 속의 위로",
                content: "“그늘이 깊다는 것은 그만큼 빛이 가깝다는 뜻입니다. 당신의 지친 하루에 조용히 손을 얹습니다. 괜찮아요, 오늘 하루 참 고생 많으셨습니다.”",
                translation: { ja: "「陰が深いということは, それだけ光が近いという意味です。あなたの疲れた一日に、静かに手を添えます」", en: "“A deep shadow means that the light is just that close. I quietly lay my hand on your tiring day.”" },
                type: "오늘의 편지"
              },
              {
                category: "일상스토리",
                emotion: "위로",
                title: "위안의 연결",
                content: "“우리는 매일 밤 서로의 목소리에 기대어 보이지 않는 선을 잇는다. 그것은 하루를 견뎌낸 이들에게 주는 소박한 위안이다.”",
                translation: { ja: "「私たちは毎晩、お互いの声に寄り添い、見えない線をつなぐ. それは一日を耐え抜いた人々への、ささやかな慰めだ」", en: "“Every night, we lean on each other's voices to connect invisible lines. It is a simple comfort to those who have endured the day.”" },
                type: "오늘의 편지"
              },
              {
                category: "일상스토리",
                emotion: "평온",
                title: "진정한 나를 찾는 평온",
                content: "“'나는 이런 사람이야'라며 억지로 규정하지 않을 때, 마음속에는 비로소 고요하고 넓은 평온함이 찾아옵니다. 나를 정의하는 복잡한 수식어를 내려놓고 그냥 숨을 쉬어 보세요.”",
                translation: { ja: "「『私はこういう人間だ』と無理に規定しない時、心の中には初めて穏やかで広い平穏が訪れます」", en: "“When we do not force ourselves to be defined as 'I am this kind of person,' a calm and wide serenity finally visits our hearts.”" },
                type: "오늘의 편지"
              },
              {
                category: "일상스토리",
                emotion: "평온",
                title: "일상 수용의 평화",
                content: "“불안마저 일상의 자연스러운 부분으로 받아들이고 흘려보낼 때, 우리의 일상은 가장 정갈하고 평화로워집니다. 바람이 불면 흔들리는 대로, 비가 오면 내리는 대로 흘러가 봅시다.”",
                translation: { ja: "「不安さえも日常의 자연스러운 부분으로 받아들이고 흘려보낼 때、私たちの日常は最も端正で平和になります」", en: "“When we accept and let go of even anxiety as a natural part of daily life, our daily life becomes the most neat and peaceful.”" },
                type: "오늘의 편지"
              },
              {
                category: "문화생활정보",
                emotion: "설렘",
                title: "교감이라는 이름의 소풍",
                content: "“아이들이 놀아달라고 하는 것은 부모와 눈을 맞추고 따뜻한 교감을 하고 싶다는 신호입니다. 그것이 우리 안에 숨겨진 가장 맑고 설레는 만남의 시작입니다.”",
                translation: { ja: "「子供たちが遊んでほしいと言うのは、親と目を合わせ、温かい交感をしたいというシグナルです。それが私たちの中に隠された、最も澄んだときめく出会いの始まりです」", en: "“Children asking to play is a signal that they want to make eye contact and have a warm connection with their parents. It is the beginning of the clearest and most exciting meeting hidden within us.”" },
                type: "오늘의 편지"
              },
              {
                category: "문화생활정보",
                emotion: "설렘",
                title: "가족과 함께하는 소풍",
                content: "“가족과 함께 보내는 여가 시간은 서로를 더 깊이 이해하고 신뢰를 쌓아가는 신비한 울타리이자, 일상 속 작은 소풍과 같습니다. 함께 걷는 길 위에 설렘의 꽃이 핍니다.”",
                translation: { ja: "「家族と過ごす余暇時間は、お互いをより深く理解し、信頼を築いていく神秘的な垣根であり、日常の中の小さな遠足のようです」", en: "“Leisure time spent with family is a mysterious fence where we understand each other deeper and build trust, like a small picnic in daily life.”" },
                type: "오늘의 편지"
              },
              {
                category: "문화생활정보",
                emotion: "설렘",
                title: "소리의 문을 두드리다",
                content: "“어쩌면 오늘, 바람결에 실려 온 맑은 목소리가 당신의 마음을 가만히 두드릴지도 모릅니다. 설레는 맘으로 귀 기울여 들어보세요.”",
                translation: { ja: "「もしかしたら今日、風に乗って届いた澄んだ声が、あなたの心をそっと叩くかもしれません。ワクワクする気持ちで待ってみてください」", en: "“Perhaps today, a clear voice carried on the wind might gently knock on your heart. Please wait for it with an excited heart.”" },
                type: "오늘의 편지"
              },
              {
                category: "문화생활정보",
                emotion: "평온",
                title: "자연의 평온함",
                content: "“아무 일도 일어나지 않는 오후, 가볍게 스쳐 가는 새소리와 바람 소리 속에 우리의 평화가 조용히 깃들어 있다.”",
                translation: { ja: "「何事も起こらない午後、軽くかすめていく鳥のさえずりと風の音の中に、私たちの平和が静かに宿っています」", en: "“On an afternoon when nothing happens, our peace quietly dwells in the sound of birds and the wind lightly brushing by.”" },
                type: "오늘의 편지"
              },
              {
                category: "문화생활정보",
                emotion: "평온",
                title: "내면의 고요한 방",
                content: "“소리치며 바쁘게 달려가던 발걸음을 멈추고 내면의 방에 초를 켭니다. 고요하게 머물 때 마음은 가장 깨끗하게 씻겨 나갑니다.”",
                translation: { ja: "「静かに時間を過ごしながら、内側の部屋にロウソクを灯します。静かにとどまる時、心は最もきれいに洗い流されます」", en: "“We stop our shouting and busy footsteps and light a candle in the inner room. The mind is washed cleanest when we stay quietly.”" },
                type: "오늘의 편지"
              }
            ];

            const batch = firestore.batch();
            seedLetters.forEach((letter, index) => {
              const docRef = primersCol.doc(`letter_${index + 1}`);
              batch.set(docRef, { ...letter, timestamp: Date.now() });
            });
            await batch.commit();
            console.log("Firestore에 행복한가 마중물 적재가 완료되었습니다.");
          }

          let queryRef = firestore.collection("primers");
          if (currentFilter !== '전체') {
            queryRef = queryRef.where("emotion", "==", currentFilter);
          }
          
          const snapshot = await queryRef.get();
          const items = [];
          snapshot.forEach(doc => {
            items.push(doc.data());
          });

          if (items.length > 0) {
            loadedPrimers = items;
            await db.primers.clear();
            await db.primers.bulkAdd(items);
            return;
          }
        }
        
        console.log("로컬 데이터베이스(IndexedDB)에서 마중물 데이터를 로드합니다.");
        let localItems = [];
        if (currentFilter === '전체') {
          localItems = await db.primers.toArray();
        } else {
          localItems = await db.primers.where('emotion').equals(currentFilter).toArray();
        }
        
        if (localItems.length === 0) {
          loadedPrimers = [
            { type: "오늘의 편지", content: "“삶이 어디로 향하고 있는지 방향을 잃은 것 같다고 느끼는 분들께 이런 말을 해주고 싶어요.”" }
          ];
        } else {
          loadedPrimers = localItems;
        }
      } catch (err) {
        console.error("마중물 불러오기 오류:", err);
      }
    }

    async function rotatePrimer() {
      if (loadedPrimers.length === 0) await loadPrimersFromDB();
      currentPrimerIndex = (currentPrimerIndex + 1) % loadedPrimers.length;
      updatePrimerUI();
    }

    function updatePrimerUI() {
      const activePrimer = loadedPrimers[currentPrimerIndex % loadedPrimers.length] || { type: "오늘의 편지", content: "“가만히 귀를 기울이면 온기가 스며듭니다.”" };
      document.getElementById('primer-type').textContent = activePrimer.type;
      document.getElementById('primer-content').textContent = activePrimer.content;
      
      // Auto translation when primer updates
      const translationBox = document.getElementById('primer-translation-box');
      if(currentLang === 'ko') {
          translationBox.classList.add('hidden');
      } else {
          triggerPrimerTranslation();
      }
    }

    // Build Emotion Tabs UI
    const emotionTabs = document.getElementById('emotion-tabs');
    const emotionKeys = {
      '전체': 'emotion_all',
      '위로': 'emotion_comfort',
      '설렘': 'emotion_romance',
      '평온': 'emotion_calm'
    };

    emotions.forEach(e => {
      const btn = document.createElement('button');
      btn.className = `px-3 py-1.5 rounded-lg text-xs font-bold transition-all touch-target select-none ${
        currentFilter === e ? 'bg-orange-500 text-white shadow-md' : 'text-orange-950/70 hover:bg-orange-100/30'
      }`;
      btn.setAttribute('data-filter', e);
      btn.setAttribute('data-i18n', emotionKeys[e]);
      btn.onclick = async () => {
        currentFilter = e;
        currentPrimerIndex = 0;
        updateTabsUI();
        await loadPrimersFromDB();
        updatePrimerUI();
        loadRelays();
      };
      emotionTabs.appendChild(btn);
    });

    function updateTabsUI() {
      Array.from(emotionTabs.children).forEach(btn => {
        const filterVal = btn.getAttribute('data-filter');
        if (currentFilter === filterVal) {
          btn.className = 'px-3 py-1.5 rounded-lg text-xs font-bold transition-all touch-target select-none bg-orange-500 text-white shadow-md';
        } else {
          btn.className = 'px-3 py-1.5 rounded-lg text-xs font-bold transition-all touch-target select-none text-orange-950/70 hover:bg-orange-100/30';
        }
      });
    }



    function showToast(message) {
      const toast = document.getElementById('toast');
      document.getElementById('toast-text').textContent = message;
      toast.classList.remove('opacity-0', 'pointer-events-none');
      
      setTimeout(() => {
        toast.classList.add('opacity-0', 'pointer-events-none');
      }, 4000);
    }

    
    // --- Audio Popup & Blob Visualizer Logic ---
    let popupMode = null; // 'recording' | 'playing'
    let popupBlobAnimationId = null;
    let popupBlobTime = 0;

    var micAnalyser = null;
    var micAudioCtx = null;

    function openAudioPopup(mode, text = "", analyser = null) {
      popupMode = mode;
      const modal = document.getElementById('audio-popup-modal');
      const title = document.getElementById('audio-popup-title');
      const subtitle = document.getElementById('audio-popup-subtitle');
      const scriptContainer = document.getElementById('audio-popup-script-container');
      const scriptText = document.getElementById('audio-popup-script');

      if (mode === 'recording') {
        title.textContent = "목소리를 듣고 있어요...";
        subtitle.textContent = "아래 문장을 편안하게 읽어주세요.";
        
        const primerContent = document.getElementById('primer-content');
        if (primerContent) {
          scriptText.innerText = primerContent.innerText.replace(/\"/g, ''); // 따옴표 제거
          scriptContainer.classList.remove('hidden');
        }
      } else if (mode === 'playing') {
        title.textContent = "따뜻한 목소리 재생 중";
        subtitle.textContent = text || "누군가의 소중한 이야기가 흐르고 있어요.";
        scriptContainer.classList.add('hidden');
      }

      modal.classList.remove('hidden');
      modal.classList.add('flex');
      
      lucide.createIcons();
      startPopupBlob(analyser);
    }

    function closeAudioPopup() {
      const modal = document.getElementById('audio-popup-modal');
      modal.classList.add('hidden');
      modal.classList.remove('flex');
      stopPopupBlob();
      popupMode = null;
    }

    function handleAudioPopupStop() {
      if (popupMode === 'recording') {
        // 녹음 중지 로직 호출 (기존 toggleRecording을 호출하여 중지)
        toggleRecording();
      } else if (popupMode === 'playing') {
        // 재생 중지 로직 호출
        if (isAudiobookMode && audiobookPlaying) {
          toggleAudiobookPlay(); // 오디오북 중지
        } else if (currentlyPlayingRelayId !== null) {
          toggleRelayPlayback(currentlyPlayingRelayId); // 단일 릴레이 중지
        } else {
           audioEngine.stop();
        }
      }
      closeAudioPopup();
    }

    function startPopupBlob(analyser) {
      const canvas = document.getElementById('popup-blob-canvas');
      const ctx = canvas.getContext('2d');
      popupBlobTime = 0;

      function draw() {
        popupBlobAnimationId = requestAnimationFrame(draw);
        
        let avg = 0;
        let dataArray = null;
        let bufferLength = 0;

        if (analyser) {
          bufferLength = analyser.frequencyBinCount;
          dataArray = new Uint8Array(bufferLength);
          analyser.getByteFrequencyData(dataArray);

          let sum = 0;
          for (let i = 0; i < bufferLength; i++) {
            sum += dataArray[i];
          }
          avg = sum / bufferLength;
        }

        ctx.clearRect(0, 0, canvas.width, canvas.height);

        const centerX = canvas.width / 2;
        const centerY = canvas.height / 2;

        if (!dataArray || bufferLength === 0) {
          // 오디오 입력이 없을 때 잔잔한 펄스 라인
          ctx.beginPath();
          ctx.moveTo(0, centerY);
          ctx.lineTo(canvas.width, centerY);
          ctx.strokeStyle = 'rgba(244, 63, 94, 0.3)';
          ctx.lineWidth = 2;
          ctx.stroke();
        } else {
          // 세련된 웨이브폼(바) 렌더링
          const barWidth = (canvas.width / bufferLength) * 2.5;
          let x = 0;

          for (let i = 0; i < bufferLength; i++) {
            // 부드러운 반응을 위해 노이즈를 약간 상쇄
            const value = dataArray[i];
            const barHeight = (value / 255) * (canvas.height * 0.4);

            const grad = ctx.createLinearGradient(0, centerY - barHeight, 0, centerY + barHeight);
            grad.addColorStop(0, 'rgba(249, 115, 22, 0.8)'); // orange
            grad.addColorStop(0.5, 'rgba(236, 72, 153, 0.9)'); // pink
            grad.addColorStop(1, 'rgba(249, 115, 22, 0.8)');

            ctx.fillStyle = grad;
            // 가운데를 기준으로 대칭되게 바를 그립니다.
            const h = Math.max(barHeight * 2, 4); // 최소 높이 4px 보장
            ctx.fillRect(x, centerY - h / 2, barWidth - 1, h);

            x += barWidth;
          }
        }
      }
      draw();
    }

    function stopPopupBlob() {
      if (popupBlobAnimationId) {
        cancelAnimationFrame(popupBlobAnimationId);
        popupBlobAnimationId = null;
      }
    }

    // Toggle Audio Recording (SpeechRecognition + MediaRecorder)
    async function toggleRecording() {
      const resetUI = () => {
        isRecording = false;
        const actionBtn = document.getElementById('action-btn');
        actionBtn.className = "w-20 h-20 rounded-full bg-gradient-to-br from-orange-500 to-rose-500 text-white font-bold flex flex-col items-center justify-center shadow-lg hover:scale-105 transition-all duration-300 glow-orange touch-target z-10 min-w-[44px] min-h-[44px]";
        document.getElementById('action-icon').setAttribute('data-lucide', 'mic');
        document.getElementById('pulse-ring').classList.remove('scale-125', 'record-pulse');
        document.getElementById('status-message').textContent = i18n[currentLang].status_initial;
        lucide.createIcons();
      };

      if (isRecording) {
        try {
          isRecording = false;
          closeAudioPopup();
          if (mediaRecorder && mediaRecorder.state !== 'inactive') {
            mediaRecorder.stop();
          }
          if (micAudioCtx) {
            micAudioCtx.close();
            micAudioCtx = null;
            micAnalyser = null;
          }
        } catch (err) {
          console.error("녹음 중지 오류:", err);
          resetUI();
        }
      } else {
        try {
          let mimeType = 'audio/webm;codecs=opus';
          if (!MediaRecorder.isTypeSupported(mimeType)) {
            const alternatives = ['audio/webm', 'audio/ogg', 'audio/mp4', 'audio/aac'];
            for (let alt of alternatives) {
              if (MediaRecorder.isTypeSupported(alt)) {
                mimeType = alt;
                break;
              }
            }
          }

          const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
          
          micAudioCtx = new (window.AudioContext || window.webkitAudioContext)();
          const source = micAudioCtx.createMediaStreamSource(stream);
          micAnalyser = micAudioCtx.createAnalyser();
          micAnalyser.fftSize = 256;
          source.connect(micAnalyser);

          audioChunks = [];
          
          mediaRecorder = new MediaRecorder(stream, { mimeType: mimeType });
          mediaRecorder.ondataavailable = (e) => {
            if (e.data.size > 0) audioChunks.push(e.data);
          };

          // Start Web Speech API Speech Recognition
          mediaRecorder.onstop = async () => {
            try {
              document.getElementById('status-message').textContent = i18n[currentLang].status_processing;
              
              let audioBlob;
              if (audioChunks.length > 0) {
                audioBlob = new Blob(audioChunks, { type: mimeType.split(';')[0] });
              } else {
                const dummyContext = new (window.AudioContext || window.webkitAudioContext)();
                const buffer = dummyContext.createBuffer(1, dummyContext.sampleRate * 0.5, dummyContext.sampleRate);
                audioBlob = new Blob([buffer], { type: 'audio/wav' });
              }
              
              const isOnline = navigator.onLine;
              let selectedEmotion = currentFilter === '전체' ? '위로' : currentFilter;
              
              let contentMessage = "";
              if (isOnline) {
                const responsePhrases = {
                  '위로': [
                    "대단히 고생 많으셨어요. 당신의 짐을 제가 함께 나눠 가질게요. (本当にお疲れ様でした。あなたの荷物を私が一緒に持ちますね。)",
                    "괜찮아요, 다 잘될 거예요. 오늘은 푹 쉬어요. (大丈夫、すべて上手くいきますよ。今日はゆっくり休んでください。)"
                  ],
                  '설렘': [
                    "오늘 바람이 참 기분 좋네요! 마치 우리 만남을 환영하듯 설레요. (今日の風は本当に気持ちいいですね！まるで私たちの出会いを歓迎するようにワクワクします。)",
                    "작은 설렘이 번져가는 행복한 하루예요. (小さなときめきが広がっていく、幸せな一日です。)"
                  ],
                  '평온': [
                    "나직하게 흐르는 이 순간이 너무 평화롭고 고마워요. (静かに流れるこの瞬間が、とても平和でありがたいです。)",
                    "차 한잔 마시며 조용하게 생각을 내려놓으세요. (오차을 마시며 조용히 생각을 내려놓으세요.)"
                  ]
                };
                const phrases = responsePhrases[selectedEmotion] || responsePhrases['위로'];
                contentMessage = phrases[Math.floor(Math.random() * phrases.length)];
              } else {
                showToast(i18n[currentLang].toast_offline_load);
                contentMessage = "기존 목소리들을 이어서 마음을 전달합니다.";
              }

              // 임시 변수에 기부용 데이터 저장
              const originalText = document.getElementById('primer-content').textContent.trim();

              tempOriginalText = originalText;
              tempAudioBlob = audioBlob;
              tempEmotion = selectedEmotion;

              document.getElementById('status-message').textContent = i18n[currentLang].status_complete;
              setTimeout(resetUI, 2000);

              // 기부 확인 모달 열기
              setTimeout(() => {
                document.getElementById('donate-modal').classList.remove('hidden');
              }, 1200);

            } catch (err) {
              console.error("녹음 데이터 처리 에러:", err);
              showToast("데이터 처리 중 오류가 생겼습니다.");
              resetUI();
            }
          };

          isRecording = true;
          mediaRecorder.start(100);
          openAudioPopup("recording", "", micAnalyser);
          
          const actionBtn = document.getElementById('action-btn');
          actionBtn.className = "w-20 h-20 rounded-full bg-gradient-to-br from-rose-600 to-red-500 text-white font-bold flex flex-col items-center justify-center shadow-lg hover:scale-105 transition-all duration-300 touch-target z-10 min-w-[44px] min-h-[44px]";
          document.getElementById('action-icon').setAttribute('data-lucide', 'square');
          document.getElementById('pulse-ring').classList.add('scale-125', 'record-pulse');
          document.getElementById('status-message').textContent = i18n[currentLang].status_recording;
          lucide.createIcons();
          
        } catch (err) {
          console.error("녹음 시작 에러:", err);
          showToast("마이크 권한을 승인해주세요.");
        }
      }
    }

    // iOS Safari & Android Audio/TTS Unlock Helper
    function unlockTts() {
      if ('speechSynthesis' in window) {
        const silentUtterance = new SpeechSynthesisUtterance(" ");
        silentUtterance.volume = 0;
        window.speechSynthesis.speak(silentUtterance);
      }
      if (typeof audioEngine !== 'undefined' && audioEngine.audioContext && audioEngine.audioContext.state === 'suspended') {
        audioEngine.audioContext.resume();
      }
    }
    
    // UI 업데이트 함수 (무료 횟수 및 프리미엄 뱃지)
    function updateFreeCountUI() {
      const badge = document.getElementById('free-eval-badge');
      const countSpan = document.getElementById('free-eval-count');
      const isPremium = localStorage.getItem('dmdg_premium') === 'true';
      
      if (isPremium) {
        if (badge) badge.classList.add('hidden');
      } else {
        if (badge) badge.classList.remove('hidden');
        const freeCount = parseInt(localStorage.getItem('dmdg_free_evals') || '3');
        if (countSpan) countSpan.textContent = freeCount + "/5";
      }
    }

    // Play a single relay audio item
    
    let currentlyPlayingRelayId = null;

    async function toggleRelayPlayback(id) {
       if (currentlyPlayingRelayId === id) {
           audioEngine.stop();
           currentlyPlayingRelayId = null;
           loadRelays(); 
           return;
       }
       
       if (currentlyPlayingRelayId !== null) {
           audioEngine.stop();
       }
       
       currentlyPlayingRelayId = id;
       loadRelays(); 
       
       await playRelay(id);
       
       if (currentlyPlayingRelayId === id) {
           currentlyPlayingRelayId = null;
           loadRelays(); 
       }
    }

    async function playRelay(id) {
      const relay = await db.relays.get(id);
      if (!relay) return;

      const speedSelect = document.getElementById('play-speed');
      const playbackRate = parseFloat(speedSelect.value);
      audioEngine.setSpeed(playbackRate);

      const personaDisplay = document.getElementById('current-persona-text');
      personaDisplay.textContent = `당목담글 재생 중 • ${relay.emotion} 릴레이`;

      if (relay.audioBlob) {
        const arrayBuffer = await relay.audioBlob.arrayBuffer();
        await audioEngine.playChunk(arrayBuffer);
      }

      
    }

    // --- Audiobook Playback State and Functions ---
    let audiobookTracks = [];
    let audiobookIndex = 0;
    let audiobookPlaying = false;
    let isAudiobookMode = false;

    async function startAudiobook() {
      let items = [];
      if (currentFilter === '전체') {
        items = await db.relays.orderBy('timestamp').reverse().toArray();
      } else {
        items = await db.relays.where('emotion').equals(currentFilter).reverse().toArray();
      }

      if (items.length === 0) {
        showToast("오디오북을 구성할 소리가 없습니다. 먼저 녹음해 주세요!");
        return;
      }

      audiobookTracks = items;
      audiobookIndex = 0;
      isAudiobookMode = true;
      audiobookPlaying = true;

      const playerEl = document.getElementById('audiobook-player');
      playerEl.classList.remove('hidden');

      updateAudiobookPlayIcon();
      playAudiobookCurrentTrack();
    }

    function stopAudiobook() {
      audiobookPlaying = false;
      isAudiobookMode = false;
      audioEngine.stop();
      
      
      const playerEl = document.getElementById('audiobook-player');
      playerEl.classList.add('hidden');
      
      const personaDisplay = document.getElementById('current-persona-text');
      personaDisplay.textContent = "따스한 감성 큐레이터 • 하루";
    }

    function toggleAudiobookPlay() {
      if (!isAudiobookMode) return;
      audiobookPlaying = !audiobookPlaying;
      updateAudiobookPlayIcon();

      if (audiobookPlaying) {
        playAudiobookCurrentTrack();
      } else {
        audioEngine.stop();
        
      }
    }

    function updateAudiobookPlayIcon() {
      const btn = document.getElementById('audiobook-play-btn');
      if (audiobookPlaying) {
        btn.innerHTML = `<i data-lucide="pause" class="w-6 h-6"></i>`;
      } else {
        btn.innerHTML = `<i data-lucide="play" class="w-6 h-6 ml-0.5"></i>`;
      }
      lucide.createIcons();
    }

    function nextAudiobookTrack() {
      if (!isAudiobookMode) return;
      
      audiobookIndex = (audiobookIndex + 1) % audiobookTracks.length;
      playAudiobookCurrentTrack();
    }

    function prevAudiobookTrack() {
      if (!isAudiobookMode) return;
      
      audiobookIndex = (audiobookIndex - 1 + audiobookTracks.length) % audiobookTracks.length;
      playAudiobookCurrentTrack();
    }

    async function playAudiobookCurrentTrack() {
      if (!isAudiobookMode || !audiobookPlaying) return;
      if (audiobookIndex < 0 || audiobookIndex >= audiobookTracks.length) return;

      const relay = audiobookTracks[audiobookIndex];
      
      document.getElementById('audiobook-track-index').textContent = `${audiobookIndex + 1} / ${audiobookTracks.length}`;
      document.getElementById('audiobook-text').textContent = relay.content;
      
      const badge = document.getElementById('audiobook-emotion-badge');
      badge.textContent = relay.emotion;
      
      badge.className = "px-2 py-0.5 rounded-full text-[10px] font-bold " + 
        (relay.emotion === '설렘' ? 'bg-rose-100/60 text-rose-800' : 
         relay.emotion === '평온' ? 'bg-amber-100/60 text-amber-800' : 'bg-orange-200/60 text-orange-800');

      const personaDisplay = document.getElementById('current-persona-text');
      personaDisplay.textContent = `오디오북 재생 중 • ${relay.emotion} ${audiobookIndex + 1}번 째 이야기`;

      const speedSelect = document.getElementById('play-speed');
      const playbackRate = parseFloat(speedSelect.value);
      audioEngine.setSpeed(playbackRate);

      

      if (relay.audioBlob) {
        const arrayBuffer = await relay.audioBlob.arrayBuffer();
        
        openAudioPopup("playing", relay.content, audioEngine.analyser);
        await audioEngine.playChunk(arrayBuffer, () => {
          closeAudioPopup();
          if (isAudiobookMode && audiobookPlaying) {
        openAudioPopup("playing", relay.content, audioEngine.analyser);
        playTtsAndThenNext(relay, playbackRate);
          }
        });
      } else {
        openAudioPopup("playing", relay.content, audioEngine.analyser);
        playTtsAndThenNext(relay, playbackRate);
      }
    }

    function playTtsAndThenNext(relay, playbackRate) { setTimeout(() => { closeAudioPopup(); autoAdvance(); }, 1000); }

    function autoAdvance() {
      setTimeout(() => {
        if (isAudiobookMode && audiobookPlaying) {
          audiobookIndex++;
          if (audiobookIndex < audiobookTracks.length) {
            playAudiobookCurrentTrack();
          } else {
            stopAudiobook();
            showToast(i18n[currentLang].audiobook_finish);
          }
        }
      }, 1200);
    }

    // Load Relays from IndexedDB
    async function loadRelays() {
      const relayList = document.getElementById('relay-list');
      relayList.innerHTML = '';

      let items = [];
      if (currentFilter === '전체') {
        items = await db.relays.orderBy('timestamp').reverse().toArray();
      } else {
        items = await db.relays.where('emotion').equals(currentFilter).reverse().toArray();
      }

      document.getElementById('relay-count').textContent = items.length;

      if (items.length === 0) {
        relayList.innerHTML = `
          <div class="text-center py-8 text-orange-950/40 text-xs font-semibold" data-i18n="no_relays">
            아직 여기에 담긴 목소리가 없어요.<br>첫 번째 마중물을 담아보세요.
          </div>
        `;
        setLanguage(currentLang);
        return;
      }

      items.forEach(relay => {
        const item = document.createElement('div');
        item.className = "glass-card p-4 rounded-2xl flex items-center justify-between gap-3 shadow-sm active:scale-[0.98] transition-transform duration-200 cursor-pointer";
        item.onclick = () => {
          unlockTts();
          toggleRelayPlayback(relay.id);
        };
        
        let tagClass = "bg-orange-100/60 text-orange-800";
        if (relay.emotion === '설렘') tagClass = "bg-rose-100/60 text-rose-800";
        if (relay.emotion === '평온') tagClass = "bg-amber-100/60 text-amber-800";

        item.innerHTML = `
          <div class="flex-grow min-w-0">
            <div class="flex items-center gap-2 mb-1">
              <span class="text-[10px] font-bold px-2 py-0.5 rounded-full ${tagClass}">${relay.emotion}</span>
              <span class="text-[10px] text-orange-950/40 font-semibold">${new Date(relay.timestamp).toLocaleTimeString([], {hour: '2-digit', minute:'2-digit'})}</span>
            </div>
            <p class="text-xs font-medium text-orange-950 leading-relaxed">${relay.content}</p>
          </div>
          <div class="flex gap-2 items-center">
            <button onclick="event.stopPropagation(); deleteRelay(${relay.id})" title="삭제" class="w-10 h-10 rounded-full bg-rose-50/50 hover:bg-rose-100 text-rose-600 flex items-center justify-center transition-colors min-w-[40px] min-h-[40px]">
              <i data-lucide="trash-2" class="w-4 h-4"></i>
            </button>
            <button class="w-10 h-10 rounded-full bg-orange-100/80 hover:bg-orange-200 text-orange-850 flex items-center justify-center transition-colors min-w-[40px] min-h-[40px]">
              <i data-lucide="${currentlyPlayingRelayId === relay.id ? 'square' : 'play'}" class="w-4.5 h-4.5 ${currentlyPlayingRelayId === relay.id ? 'text-rose-600' : ''}"></i>
            </button>
          </div>
        `;
        relayList.appendChild(item);
      });
      lucide.createIcons();
    }

    // Delete a single relay audio item
    async function deleteRelay(id) {
      if (confirm(i18n[currentLang].confirm_delete)) {
        try {
          await db.relays.delete(id);
          showToast(i18n[currentLang].delete_alert);
          loadRelays();
        } catch (err) {
          console.error("삭제 실패:", err);
          showToast("삭제 중 문제가 생겼습니다.");
        }
      }
    }

    // Export Dexie Database to JSON file
    async function exportData() {
      try {
        const relays = await db.relays.toArray();
        const serializedRelays = await Promise.all(relays.map(async (r) => {
          const buffer = await r.audioBlob.arrayBuffer();
          const base64 = btoa(String.fromCharCode(...new Uint8Array(buffer)));
          return {
            ...r,
            audioBlobBase64: base64,
            audioBlob: undefined
          };
        }));

        const dataStr = "data:text/json;charset=utf-8," + encodeURIComponent(JSON.stringify(serializedRelays));
        const downloadAnchor = document.createElement('a');
        downloadAnchor.setAttribute("href", dataStr);
        downloadAnchor.setAttribute("download", `dangmokdamgeul_backup_${Date.now()}.json`);
        document.body.appendChild(downloadAnchor);
        downloadAnchor.click();
        downloadAnchor.remove();
        showToast("데이터 백업 파일이 저장되었습니다.");
      } catch (err) {
        console.error("백업 오류:", err);
        showToast("백업 생성 중 문제가 생겼어요.");
      }
    }

    // Import Dexie Database from JSON file
    async function importData(event) {
      const file = event.target.files[0];
      if (!file) return;

      const reader = new FileReader();
      reader.onload = async (e) => {
        try {
          const rawRelays = JSON.parse(e.target.result);
          await db.relays.clear();
          
          for (let r of rawRelays) {
            const binaryStr = atob(r.audioBlobBase64);
            const bytes = new Uint8Array(binaryStr.length);
            for (let i = 0; i < binaryStr.length; i++) {
              bytes[i] = binaryStr.charCodeAt(i);
            }
            const audioBlob = new Blob([bytes], { type: 'audio/webm' });
            
            await db.relays.add({
              emotion: r.emotion,
              content: r.content,
              timestamp: r.timestamp || Date.now(),
              audioBlob: audioBlob
            });
          }
          
          showToast("데이터를 성공적으로 복원했습니다!");
          loadRelays();
        } catch (err) {
          console.error("가져오기 에러:", err);
          showToast("잘못된 백업 파일 형식입니다.");
        }
      };
      reader.readAsText(file);
    }

    // ----------------------------------------------------
    // Evaluation Modal Control & Premium Limits
    // ----------------------------------------------------
    let currentOriginalText = "";
    let currentAudioBase64 = "";
    let currentAudioMimeType = "";

    async function evaluatePronunciationWithGemini(originalText, audioBase64, mimeType) {
      try {
        const apiKey = localStorage.getItem('dmdg_gemini_key');
        const evaluateFn = firebase.functions().httpsCallable('evaluatePronunciation');
        const result = await evaluateFn({ originalText, audioBase64, mimeType, apiKey });
        return result.data;
      } catch (err) {
        console.error("Gemini Evaluation failed:", err);
        throw err;
      }
    }

    async function openEvaluationModal(originalText, audioBase64, mimeType) {
      currentOriginalText = originalText;
      currentAudioBase64 = audioBase64;
      currentAudioMimeType = mimeType;

      const modal = document.getElementById('ai-evaluation-modal');
      modal.classList.remove('hidden');

      // Show temporary loading status
      document.getElementById('ai-score').textContent = "...";
      document.getElementById('ai-good').textContent = "AI 분석 중...";
      document.getElementById('ai-improve').textContent = "AI 분석 중...";
      const feedbackVisual = document.getElementById('evaluation-visual-feedback');
      feedbackVisual.innerHTML = '<span class="text-xs text-orange-650 animate-pulse">Gemini AI가 정밀 발음을 해체 분석하고 있습니다...</span>';

      try {
        const result = await evaluatePronunciationWithGemini(originalText, audioBase64, mimeType);
        
        document.getElementById('ai-score').textContent = result.score;
        document.getElementById('ai-good').textContent = result.good;
        document.getElementById('ai-improve').textContent = result.improve;

        // Gemini의 피드백 자리에 원본 텍스트 + 틀린 단어 하이라이트 렌더링
        const feedbackVisual = document.getElementById('evaluation-visual-feedback');
        let highlightedHtml = originalText;
        
        if (result.bad_words && result.bad_words.length > 0) {
          const words = originalText.split(/\s+/);
          highlightedHtml = words.map(word => {
            const cleanWord = word.replace(/[^가-힣a-zA-Z0-9]/g, "");
            let meaning = "";
            const isBad = result.bad_words.some(bw => {
              let cleanBw = "";
              if (typeof bw === 'string') {
                cleanBw = bw.replace(/[^가-힣a-zA-Z0-9]/g, "");
              } else if (bw.word) {
                cleanBw = bw.word.replace(/[^가-힣a-zA-Z0-9]/g, "");
                meaning = bw.meaning || "";
              }
              return cleanBw === cleanWord || (cleanBw.length > 1 && cleanWord.includes(cleanBw));
            });
            if (isBad && cleanWord.length > 0) {
              return `<span class="text-rose-600 font-bold underline decoration-rose-400 underline-offset-4 cursor-pointer hover:bg-rose-100 transition-colors rounded px-1 active:scale-95 inline-block" onclick="handleBadWordClick(this, '${word.replace(/'/g, "\\'")}', '${meaning.replace(/'/g, "\\'")}')">${word}</span>`;
            }
            return word;
          }).join(' ');
        }

        feedbackVisual.innerHTML = `<div class="p-4 bg-orange-50 rounded-xl border border-orange-100 shadow-sm text-center mb-3">
            <p class="text-sm font-medium text-orange-900 leading-relaxed break-keep">${highlightedHtml}</p>
            <p class="text-[10px] text-orange-600 mt-2 font-bold animate-pulse">💡 붉은색 단어를 터치하면 정밀 교정을 받을 수 있어요!</p>
          </div>
          <div class="p-3 bg-rose-50 rounded-xl border border-rose-100 shadow-sm text-center">
            <span class="text-xs text-rose-400 font-bold mb-1 block">🎯 교정 가이드</span>
            <span class="text-sm font-bold text-rose-800 break-keep leading-snug">${result.improve}</span>
          </div>`;

        // Check premium status
        const isPremium = localStorage.getItem('dmdg_premium') === 'true';
        let freeCount = parseInt(localStorage.getItem('dmdg_free_evals') || '3');

        // 기존 전체 가림막(lockOverlay) 방식 제거하고 바로 보여줌
        const lockOverlay = document.getElementById('premium-lock-overlay');
        if (lockOverlay) lockOverlay.classList.add('hidden');

        if (!isPremium && freeCount > 0) {
          freeCount--;
          localStorage.setItem('dmdg_free_evals', freeCount.toString());
        }
        
        updateFreeCountUI();
        setLanguage(currentLang);
      } catch (err) {
        console.error("AI 발음 평가 중 오류:", err);
        document.getElementById('ai-score').textContent = "-";
        document.getElementById('ai-good').textContent = "평가 도중 문제가 발생했습니다.";
        
        if (err.message && err.message.includes("무료 평가 횟수가 소진")) {
          document.getElementById('ai-improve').textContent = "프리미엄을 결제하시거나 개인 Gemini API 키를 등록해주세요.";
          openPaywallModal();
        } else {
          document.getElementById('ai-improve').textContent = "네트워크를 확인하시거나 다시 시도해 주세요.";
        }
      }
    }
    function playAnnouncerTts(text) {
      if (!('speechSynthesis' in window)) {
        showToast("이 기기에서는 아나운서 발음 듣기를 지원하지 않습니다.");
        return;
      }
      unlockTts();
      window.speechSynthesis.cancel();
      const utterance = new SpeechSynthesisUtterance(text);
      utterance.lang = 'ko-KR';
      utterance.rate = 0.85; // 또박또박 들려주기 위해 약간 느리게 설정
      
      const voices = window.speechSynthesis.getVoices();
      const targetVoice = voices.find(v => v.lang.includes('ko-KR') && (v.name.includes('Google') || v.name.includes('Siri')));
      if (targetVoice) utterance.voice = targetVoice;
      
      window.speechSynthesis.speak(utterance);
    }

    function closeEvaluationModal() {
      document.getElementById('ai-evaluation-modal').classList.add('hidden');
    }

    // ----------------------------------------------------
    // Paywall & PayPal Checkout Integration (A/B Hybrid)
    // ----------------------------------------------------
    function openPaywallModal() {
      closeEvaluationModal();
      
      const paywall = document.getElementById('paywall-modal');
      paywall.classList.remove('hidden');
      selectPricingOption('weekly');

      // 기부 유도 UI 조건부 노출 (월 3회 한도 체크)
      const donationOption = document.getElementById('paywall-donation-option');
      const limitText = document.getElementById('paywall-donation-limit-text');
      
      if (window.currentUserData && window.currentUserData.monthly_reward_count !== undefined) {
        const now = new Date();
        const currentMonth = `${now.getFullYear()}-${String(now.getMonth() + 1).padStart(2, '0')}`;
        
        let count = window.currentUserData.monthly_reward_count;
        if (window.currentUserData.reward_month !== currentMonth) count = 0;

        if (count < 3) {
          donationOption.classList.remove('hidden');
          limitText.textContent = `이번 달 무료 보상 혜택: ${3 - count}회 남음`;
        } else {
          donationOption.classList.add('hidden');
        }
      } else {
        // 데이터가 아직 로드되지 않았거나 최초일 경우 기본 노출
        donationOption.classList.remove('hidden');
        limitText.textContent = `이번 달 무료 보상 혜택: 3회 남음`;
      }
    }

    async function processVoiceDonationFromPaywall() {
      if (!currentOriginalText || !currentRecognizedText) {
        showToast("기부할 음성 데이터가 없습니다.");
        return;
      }
      
      showToast("목소리를 기부하고 있습니다...");
      const paywall = document.getElementById('paywall-modal');
      paywall.classList.add('hidden');

      try {
        if (!firebase.auth().currentUser) {
          await firebase.auth().signInAnonymously();
        }
        const user = firebase.auth().currentUser;

        // Base64 인코딩 후 Firestore 업로드
        const arrayBuffer = await audioEngine.getAudioBlob().arrayBuffer();
        const base64Audio = btoa(String.fromCharCode(...new Uint8Array(arrayBuffer)));

        await firestore.collection('relays').add({
          userId: user.uid,
          emotion: currentEmotion || "행복", // fallback
          content: currentOriginalText,
          audioBlobBase64: base64Audio,
          timestamp: Date.now()
        });

        // 로컬 IndexedDB에도 저장 (선택 사항)
        try {
          await db.relays.add({
            emotion: currentEmotion || "행복",
            content: currentOriginalText,
            timestamp: Date.now(),
            audioBlob: audioEngine.getAudioBlob()
          });
          loadRelays();
        } catch(e) {}

        showToast("기부가 완료되었습니다! 5회 무료 횟수가 곧 적립됩니다.");
        // 백엔드 트리거가 free_evals를 증가시키면 onSnapshot에 의해 UI가 자동 업데이트 됩니다.
      } catch (err) {
        console.error("기부 중 오류:", err);
        showToast("기부 처리 중 문제가 발생했습니다.");
      }
    }

    function closePaywallModal() {
      document.getElementById('paywall-modal').classList.add('hidden');
      document.getElementById('paypal-button-container').classList.add('hidden');
      document.getElementById('paywall-btn').classList.remove('hidden');
    }

    function selectPricingOption(option) {
      selectedPricing = option;
      const optWeekly = document.getElementById('option-weekly');
      const optCharge = document.getElementById('option-charge');

      if (option === 'weekly') {
        optWeekly.className = "p-3.5 rounded-2xl border-2 border-orange-400 bg-orange-50/50 hover:bg-orange-100/50 cursor-pointer flex justify-between items-center transition-all";
        optCharge.className = "p-3.5 rounded-2xl border border-orange-200 bg-white/40 hover:bg-orange-50/30 cursor-pointer flex justify-between items-center transition-all";
      } else {
        optWeekly.className = "p-3.5 rounded-2xl border border-orange-200 bg-white/40 hover:bg-orange-50/30 cursor-pointer flex justify-between items-center transition-all";
        optCharge.className = "p-3.5 rounded-2xl border-2 border-orange-400 bg-orange-50/50 hover:bg-orange-100/50 cursor-pointer flex justify-between items-center transition-all";
      }

      document.getElementById('paypal-button-container').classList.add('hidden');
      document.getElementById('paywall-btn').classList.remove('hidden');
    }

    function startPaypalFlow() {
      const btn = document.getElementById('paywall-btn');
      const paypalContainer = document.getElementById('paypal-button-container');

      btn.classList.add('hidden');
      paypalContainer.classList.remove('hidden');

      let currency = 'USD';
      let value = '1.99';

      if (currentLang === 'ko') {
        currency = 'KRW';
        value = selectedPricing === 'weekly' ? '2900' : '4900';
      } else if (currentLang === 'ja') {
        currency = 'JPY';
        value = selectedPricing === 'weekly' ? '290' : '490';
      } else {
        currency = 'USD';
        value = selectedPricing === 'weekly' ? '1.99' : '3.99';
      }

      loadPaypalSdk(currency, () => {
        renderPaypalButtons(currency, value);
      });
    }

    function loadPaypalSdk(currency, callback) {
      const existingScript = document.getElementById('paypal-sdk-script');
      if (existingScript) {
        existingScript.remove();
      }
      paypalRendered = false;

      const script = document.createElement('script');
      script.id = 'paypal-sdk-script';
      script.src = `https://www.paypal.com/sdk/js?client-id=AaYtg54hxqwI7fn87ym2M28kTDOl7NQ1RZJUjdX0tIutj048JX2TovDkCWytSy8K-B9lIpcf7_IHDA-c&currency=${currency}`;
      script.onload = () => {
        callback();
      };
      document.head.appendChild(script);
    }

    function renderPaypalButtons(currency, value) {
      const container = document.getElementById('paypal-button-container');
      container.innerHTML = '';

      if (typeof paypal === 'undefined') {
        console.error("PayPal SDK not loaded");
        container.innerHTML = `<div class="text-xs text-rose-500 font-bold py-2">PayPal 로드 실패. 잠시 후 다시 시도해 주세요.</div>`;
        return;
      }

      paypal.Buttons({
        style: {
          layout: 'vertical',
          color:  'gold',
          shape:  'rect',
          label:  'paypal'
        },
        createOrder: function(data, actions) {
          return actions.order.create({
            purchase_units: [{
              amount: {
                currency_code: currency,
                value: value
              },
              description: selectedPricing === 'weekly' ? "DMDG 주간 프리미엄 패스" : "DMDG AI 코인 30개 충전"
            }]
          });
        },
        onApprove: function(data, actions) {
          return actions.order.capture().then(function(details) {
            handlePaymentSuccess();
          });
        },
        onError: function(err) {
          console.error("PayPal 결제 오류:", err);
          showToast("결제 오류가 발생했습니다. (Sandbox Mock 승인으로 대체합니다)");
          setTimeout(handlePaymentSuccess, 1500);
        }
      }).render('#paypal-button-container');

      paypalRendered = true;
    }

    async function handlePaymentSuccess() {
      if (selectedPricing === 'weekly') {
        localStorage.setItem('dmdg_premium', 'true');
        showToast(i18n[currentLang].paywall_notice + " (주간 구독 활성화)");
        try {
          if (!firebase.auth().currentUser) await firebase.auth().signInAnonymously();
          await firestore.collection('users').doc(firebase.auth().currentUser.uid).set({ premium: true, updatedAt: Date.now() }, { merge: true });
          await firestore.collection('stats').doc('overview').set({ premiumUsers: firebase.firestore.FieldValue.increment(1) }, { merge: true });
        } catch(e) { console.error("프리미엄 DB 저장 실패:", e); }
      } else {
        const currentCoins = parseInt(localStorage.getItem('dmdg_coins') || '0');
        localStorage.setItem('dmdg_coins', (currentCoins + 30).toString());
        // 기부 보상: 이용권 +5회 부여
        const currentFreeCount = parseInt(localStorage.getItem('dmdg_free_evals') || '3');
        localStorage.setItem('dmdg_free_evals', (currentFreeCount + 5).toString());
        updateFreeCountUI();
        showToast(i18n[currentLang].paywall_notice + " (코인 30개 충전 완료)");
      }

      const lockOverlay = document.getElementById('premium-lock-overlay');
      if (lockOverlay) {
        lockOverlay.classList.add('hidden');
      }

      closePaywallModal();
      
      if (currentOriginalText && currentAudioBase64) {
        openEvaluationModal(currentOriginalText, currentAudioBase64, currentAudioMimeType);
      }
    }

    // ----------------------------------------------------
    // Gemini Settings & Reward/Donation Logic
    // ----------------------------------------------------
    let tempOriginalText = "";
    let tempRecognizedText = "";
    let tempAudioBlob = null;
    let tempEmotion = "";

    function openSettingsModal() {
      const modal = document.getElementById('settings-modal');
      const input = document.getElementById('gemini-api-key-input');
      input.value = localStorage.getItem('dmdg_gemini_key') || '';
      modal.classList.remove('hidden');
    }

    function closeSettingsModal() {
      document.getElementById('settings-modal').classList.add('hidden');
    }

    function saveSettingsModal() {
      const input = document.getElementById('gemini-api-key-input').value.trim();
      localStorage.setItem('dmdg_gemini_key', input);
      closeSettingsModal();
      showToast("Gemini API Key가 저장되었습니다.");
    }
    window.saveGeminiApiKey = saveSettingsModal;

    function openBenefitModal() {
      document.getElementById('benefit-modal').classList.remove('hidden');
    }

    function closeBenefitModal() {
      document.getElementById('benefit-modal').classList.add('hidden');
    }

    let isDashboardOpen = false;
    function toggleDashboard() {
      const content = document.getElementById('dashboard-content');
      const chevron = document.getElementById('dashboard-chevron');
      isDashboardOpen = !isDashboardOpen;
      
      if (isDashboardOpen) {
        content.style.maxHeight = '500px';
        chevron.style.transform = 'rotate(180deg)';
        updateWarmthLogo();
        startMilkyWayEffect();
      } else {
        content.style.maxHeight = '0px';
        chevron.style.transform = 'rotate(0deg)';
      }
    }
    window.toggleDashboard = toggleDashboard;

    async function updateWarmthLogo() {
      try {
        let localCount = await db.relays.count();
        let remoteCount = 0;
        try {
          const snapshot = await Promise.race([
            firestore.collection('relays').get(),
            new Promise((_, reject) => setTimeout(() => reject(new Error("Timeout")), 2000))
          ]);
          remoteCount = snapshot.size;
        } catch (e) {
          console.log("Firestore 대시보드 갱신 지연 (로컬 DB 우선 활용):", e);
        }

        const totalDonations = Math.max(localCount, remoteCount);

        const baseTemp = 36.5;
        const tempPerDonation = 0.5;
        const currentTemp = Math.min(baseTemp + (totalDonations * tempPerDonation), 100.0);

        document.getElementById('warmth-degree').textContent = `${currentTemp.toFixed(1)}°C`;
        document.getElementById('stat-donations-count').textContent = totalDonations;
        document.getElementById('stat-chains-count').textContent = Math.round(totalDonations * 1.2);

        const logoEl = document.getElementById('warmth-logo');
        if (logoEl) {
          const ratio = (currentTemp - baseTemp) / (100.0 - baseTemp);
          const grayscaleVal = 100 - (ratio * 100);
          const blurVal = 6 - (ratio * 6);
          const opacityVal = 0.15 + (ratio * 0.85);

          logoEl.style.filter = `grayscale(${grayscaleVal}%) blur(${blurVal}px)`;
          logoEl.style.opacity = opacityVal;
        }

        const descEl = document.getElementById('warmth-status-desc');
        if (descEl) {
          if (currentTemp >= 100) {
            descEl.textContent = "🎉 지구촌의 감성 온도가 100°C에 도달해 완벽히 따뜻해졌어요! ♥";
          } else if (currentTemp > 60) {
            descEl.textContent = "🔥 세계 곳곳에서 보내준 목소리로 로고가 온전한 색을 찾고 있어요!";
          } else {
            descEl.textContent = "지구촌의 감성 온도가 조금씩 따뜻해지고 있어요!";
          }
        }
      } catch (err) {
        console.error("대시보드 갱신 에러:", err);
      }
    }
    window.updateWarmthLogo = updateWarmthLogo;

    async function translateTextWithGemini(text, targetLang) {
      try {
        const translateFn = firebase.functions().httpsCallable('translateText');
        const result = await translateFn({ text, targetLang });
        return result.data.translatedText || result.data;
      } catch (err) {
        console.error("Gemini Translation Error via Functions:", err);
        throw new Error(err.message || "번역에 실패했습니다.");
      }
    }

    async function triggerPrimerTranslation() {
      const primerText = document.getElementById('primer-content').textContent.trim();
      const translationBox = document.getElementById('primer-translation-box');
      const translationText = document.getElementById('primer-translation-text');

      // 1. Check if we already have local translation seed for the current primer
      const activePrimer = loadedPrimers[currentPrimerIndex % loadedPrimers.length];
      if (activePrimer && activePrimer.translation && activePrimer.translation[currentLang]) {
        translationText.textContent = activePrimer.translation[currentLang];
        translationBox.classList.remove('hidden');
        return;
      }

      // 2. If not, try calling Gemini API (requires API Key)
      try {
        translationText.innerHTML = `<i data-lucide="loader-2" class="w-3 h-3 text-orange-650 animate-spin inline"></i> <span>${i18n[currentLang].translate_loading}</span>`;
        translationBox.classList.remove('hidden');
        lucide.createIcons();

        const translated = await translateTextWithGemini(primerText, currentLang);
        
        translationText.textContent = translated;
      } catch (err) {
        console.error("번역 에러:", err);
        if (err.message === "Gemini API Key missing") {
          translationText.textContent = i18n[currentLang].gemini_key_needed || "번역을 위해 Gemini API Key를 등록해 주세요.";
        } else {
          showToast("번역 중 에러가 발생했습니다. 키 유효성을 확인해 주세요.");
        }
      }
    }
    window.triggerPrimerTranslation = triggerPrimerTranslation;

    
    function startMilkyWayEffect() {
      const canvas = document.getElementById('milkyway-canvas');
      if (!canvas) return;
      const ctx = canvas.getContext('2d');
      const stars = [];
      const numStars = 150;
      
      canvas.width = window.innerWidth;
      canvas.height = window.innerHeight;

      for(let i=0; i<numStars; i++) {
        stars.push({
          x: Math.random() * canvas.width,
          y: Math.random() * canvas.height,
          size: Math.random() * 2 + 0.5,
          speed: Math.random() * 1.5 + 0.5,
          alpha: Math.random()
        });
      }

      let animationFrame;
      let opacity = 1;

      function animate() {
        ctx.clearRect(0, 0, canvas.width, canvas.height);
        ctx.globalAlpha = opacity;
        
        ctx.fillStyle = `rgba(15, 23, 42, ${opacity * 0.35})`; // dark night overlay
        ctx.fillRect(0, 0, canvas.width, canvas.height);

        stars.forEach(s => {
          s.y += s.speed;
          s.x += Math.sin(s.y * 0.05) * 0.5;
          if (s.y > canvas.height) { s.y = 0; s.x = Math.random() * canvas.width; }
          
          ctx.beginPath();
          ctx.arc(s.x, s.y, s.size, 0, Math.PI * 2);
          ctx.fillStyle = `rgba(255, 255, 255, ${s.alpha})`;
          ctx.fill();
        });

        if (opacity > 0) {
            opacity -= 0.005; // Fade out over 200 frames
            animationFrame = requestAnimationFrame(animate);
        } else {
            ctx.clearRect(0, 0, canvas.width, canvas.height);
            ctx.globalAlpha = 1;
        }
      }
      
      // Firestore Auth Listener for Real-time Data Sync
      firebase.auth().onAuthStateChanged(user => {
        if (user) {
          firestore.collection('users').doc(user.uid).onSnapshot(doc => {
            if (doc.exists) {
              const data = doc.data();
              window.currentUserData = data; // Paywall에서 사용하기 위해 전역 저장
              
              // 프리미엄 상태 동기화
              if (data.premium) {
                localStorage.setItem('dmdg_premium', 'true');
              }
              
              // 무료 횟수 상태 동기화
              if (typeof data.free_evals === 'number') {
                localStorage.setItem('dmdg_free_evals', data.free_evals.toString());
                updateFreeCountUI();
              }
            }
          });
        }
      });

      initDexie();
      animate();
    }

    async function processVoiceDonation() {
      document.getElementById('donate-modal').classList.add('hidden');
      showToast("익명 로그인 및 클라우드 업로드 중...");

      let isFirebaseUploaded = false;
      try {
        if (!firebase.auth().currentUser) {
          await firebase.auth().signInAnonymously();
        }
        const user = firebase.auth().currentUser;

        // Base64 오디오 추출 및 Firestore 업로드
        const arrayBuffer = await tempAudioBlob.arrayBuffer();
        const base64Audio = btoa(String.fromCharCode(...new Uint8Array(arrayBuffer)));

        await firestore.collection('relays').add({
          userId: user.uid,
          emotion: tempEmotion,
          content: tempOriginalText,
          audioBlobBase64: base64Audio,
          timestamp: Date.now()
        });
        await firestore.collection('stats').doc('overview').set({ relays: firebase.firestore.FieldValue.increment(1) }, { merge: true });
        isFirebaseUploaded = true;
      } catch (err) {
        console.error("클라우드 기부 처리 실패 (로컬 저장을 진행합니다):", err);
      }

      // 오프라인 우선(Offline-First) 정책: 클라우드 업로드 여부와 무관하게 로컬 DB 저장 및 5회 리워드 적립 보장
      try {
        // 로컬 DB에도 캐싱으로 저장
        await db.relays.add({
          emotion: tempEmotion,
          content: tempOriginalText,
          timestamp: Date.now(),
          audioBlob: tempAudioBlob
        });

        // 리워드 로직은 모두 백엔드(functions/index.js)의 onVoiceDonated 트리거로 이관됨.
        // 프론트엔드에서는 더이상 직접 free_evals를 올리지 않음.
        updateFreeCountUI();
        setLanguage(currentLang);
        showToast(i18n[currentLang].donate_success || "기부 완료! 5회 이용권이 지급되었습니다.");

        const arrayBuffer = await tempAudioBlob.arrayBuffer();
        const base64Audio = btoa(String.fromCharCode(...new Uint8Array(arrayBuffer)));

        loadRelays();
        openEvaluationModal(tempOriginalText, base64Audio, tempAudioBlob.type);
        updateWarmthLogo();
        startMilkyWayEffect();
      } catch (localErr) {
        console.error("로컬 기부 저장 실패:", localErr);
        showToast("기부 처리 중 오류가 발생했습니다.");
      }
    }
    window.processVoiceDonation = processVoiceDonation;

    async function processLocalSaveOnly() {
      document.getElementById('donate-modal').classList.add('hidden');
      try {
        await db.relays.add({
          emotion: tempEmotion,
          content: tempOriginalText,
          timestamp: Date.now(),
          audioBlob: tempAudioBlob
        });
        loadRelays();
        updateWarmthLogo();
        startMilkyWayEffect();

        const isPremium = localStorage.getItem('dmdg_premium') === 'true';
        const freeCount = parseInt(localStorage.getItem('dmdg_free_evals') || '3');
        if (isPremium || freeCount > 0) {
          const arrayBuffer = await tempAudioBlob.arrayBuffer();
          const base64Audio = btoa(String.fromCharCode(...new Uint8Array(arrayBuffer)));
          openEvaluationModal(tempOriginalText, base64Audio, tempAudioBlob.type);
        } else {
          showToast("무료 분석 횟수를 모두 소진했습니다. 프리미엄으로 무제한 정밀 분석을 즐겨보세요!");
          openPaywallModal();
        }
      } catch (e) {
        console.error("로컬 저장 실패:", e);
      }
    }
    window.processLocalSaveOnly = processLocalSaveOnly;

    // Initial Loading
    window.addEventListener('load', async () => {
      const browserLang = navigator.language || navigator.userLanguage;
      if (browserLang.startsWith('ja')) {
        currentLang = 'ja';
      } else if (browserLang.startsWith('en')) {
        currentLang = 'en';
      } else {
        currentLang = 'ko';
      }
      
      updateFreeCountUI();

      // 방문자 통계 기록
      try {
        if (!firebase.auth().currentUser) await firebase.auth().signInAnonymously();
        await firestore.collection('analytics').add({
          type: 'visit',
          referrer: document.referrer || 'direct',
          userAgent: navigator.userAgent,
          timestamp: Date.now(),
          uid: firebase.auth().currentUser.uid
        });
        await firestore.collection('stats').doc('overview').set({ visits: firebase.firestore.FieldValue.increment(1) }, { merge: true });
      } catch (e) {
        console.error("통계 기록 실패:", e);
      }
      
      currentLang = localStorage.getItem('preferredLang') || currentLang;
      setLanguage(currentLang);
      applyCountryTheme(currentLang);  // 🎨 localStorage에서 저장된 국가 테마 복원

      await loadPrimersFromDB();
      updatePrimerUI();
      loadRelays();
      updateWarmthLogo();
        startMilkyWayEffect();

      if ('serviceWorker' in navigator) {
        navigator.serviceWorker.register('./sw.js')
          .then(reg => console.log('서비스 워커가 등록되었습니다!', reg))
          .catch(err => console.error('서비스 워커 등록 실패:', err));
      }
    });