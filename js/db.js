// 1. Dexie Database Setup
    const db = new Dexie('DangmokdamgeulDB');
    db.version(3).stores({
      personas: '++id, name, style, tone, preferredWritingStyle',
      primers: '++id, personaId, content, timestamp, weather, emotion, sensorContext, type',
      relays: '++id, primerId, personaId, content, audioBlob, timestamp, emotion'
    });

    // Populate initial default personas and actual happy letters from m-letter.or.kr
    db.on('populate', () => {
      db.personas.bulkAdd([
        { name: '하루 (위로)', style: '예쁜 일본어 구어체', tone: '따스하고 다정한 목소리', preferredWritingStyle: '소박하고 따스한 말투' },
        { name: '사쿠라 (설렘)', style: '귀엽고 낭만적인 구어체', tone: '맑고 생기 넘치는 목소리', preferredWritingStyle: '발랄하고 감성 가득한 말투' },
        { name: '렌 (평온)', style: '차분하고 정갈한 구어체', tone: '나직하고 깊은 목소리', preferredWritingStyle: '담담하면서 평화로운 말투' }
      ]);

      // Populate actual m-letter happy content (마중물 편지)
      db.primers.bulkAdd([
        { type: "오늘의 편지", emotion: "위로", content: "“삶이 어디로 향하고 있는지 방향을 잃은 것 같다고 느끼는 분들께 이런 말을 해주고 싶어요. '나는 이런 사람이야' 하면서 자신을 가두거나, '나는 안 맞아' 하면서 미리 포기하지 마세요.” — 김창완 <이제야 보이네> 중에서", translation: { ja: "「人生がどこに向かっているのか、方向を見失ったと感じている方々に、こんな言葉を贈りたいです。『私はこういう人間だから』と自分を閉じ込めたり、『自分には合わない』と最初から諦めたりしないでください」 — キム・チャンワン『やっと見えるね』より", en: "“To those who feel they have lost their direction in life, I want to say this. Don't trap yourself by saying 'I'm this kind of person,' or give up in advance saying 'It doesn't suit me.'” — From Kim Chang-wan <Only Now I See>" } },
        { type: "오늘의 편지", emotion: "위로", content: "“부디 자기 인생을 다른 사람과 비교하며 비참해지지 않았으면 좋겠습니다. 허탈함 속의 나를 발견하는 것도 나쁘지 않아요. 괜한 불안을 느끼는 일도 일상의 아름다움 아닐까요?” — 김창완 <이제야 보이네> 중에서", translation: { ja: "「どうか自分の人生を他の人と比較して惨めにならないでほしいです。虚しさの中の自分を発見することも悪くありません。無駄な不安を感じることも、日常の美しさではないでしょうか？」 — キム・チャンワン『やっと見えるね』より", en: "“I hope you don't make yourself miserable by comparing your life to others. Discovering yourself in emptiness isn't bad either. Isn't feeling unnecessary anxiety also a beauty of daily life?” — From Kim Chang-wan <Only Now I See>" } },
        { type: "오늘의 편지", emotion: "위로", content: "“자신을, 우리 삶을 재단하지 말아요. 어마어마한 기적을 가두지 말자고요.” — 김창완 <이제야 보이네> 중에서", translation: { ja: "「自分を、私たちの人生を裁かないでください。とてつもない奇跡を閉じ込めないでいましょう」 — キム・チャンワン『やっと見えるね』より", en: "“Let's not judge ourselves, or our lives. Let's not confine this immense miracle.” — From Kim Chang-wan <Only Now I See>" } },
        { type: "오늘의 편지", emotion: "위로", content: "“우리는 매일 밤 서로의 목소리에 기대어 보이지 않는 선을 잇는다. 그것은 하루를 견뎌낸 이들에게 주는 소박한 위안이다.”", translation: { ja: "「私たちは毎晩、お互いの声に寄り添い、見えない線をつなぐ。それは一日を耐え抜いた人々への、ささやかな慰めだ」", en: "“Every night, we lean on each other's voices to connect invisible lines. It is a simple comfort to those who have endured the day.”" } },
        { type: "오늘의 편지", emotion: "위로", content: "“그늘이 깊다는 것은 그만큼 빛이 가깝다는 뜻입니다. 당신의 지친 하루에 조용히 손을 얹습니다.”", translation: { ja: "「陰が深いということは, それだけ光が近いという意味です。あなたの疲れた一日に、静かに手を添えます」", en: "“A deep shadow means that the light is just that close. I quietly lay my hand on your tiring day.”" } },
        { type: "오늘의 편지", emotion: "설렘", content: "“아이들이 놀아달라고 하는 것은 부모와 눈을 맞추고 따뜻한 교감을 하고 싶다는 신호입니다. 그것이 우리 안에 숨겨진 가장 맑고 설레는 만남의 시작입니다.”", translation: { ja: "「子供たちが遊んでほしいと言うのは、親と目を合わせ、温かい交感をしたいというシグナルです。それが私たちの中に隠された、最も澄んだときめく出会いの始まりです」", en: "“Children asking to play is a signal that they want to make eye contact and have a warm connection with their parents. It is the beginning of the clearest and most exciting meeting hidden within us.”" } },
        { type: "오늘의 편지", emotion: "설렘", content: "“가족과 함께 보내는 여가 시간은 서로를 더 깊이 이해하고 신뢰를 쌓아가는 신비한 울타리이자, 일상 속 작은 소풍과 같습니다.”", translation: { ja: "「家族と過ごす余暇時間は、お互いをより深く理解し、信頼を築いていく神秘的な垣根であり、日常の中의小さな遠足のようです」", en: "“Leisure time spent with family is a mysterious fence where we understand each other deeper and build trust, like a small picnic in daily life.”" } },
        { type: "오늘의 편지", emotion: "설렘", content: "“어쩌면 오늘, 바람결에 실려 온 맑은 목소리가 당신의 마음을 가만히 두드릴지도 모릅니다. 설레는 맘으로 기다려 보세요.”", translation: { ja: "「もしかしたら今日、風に乗って届いた澄んだ声が、あなたの心をそっと叩くかもしれません。ワクワクする気持ちで待ってみてください」", en: "“Perhaps today, a clear voice carried on the wind might gently knock on your heart. Please wait for it with an excited heart.”" } },
        { type: "오늘의 편지", emotion: "설렘", content: "“새로운 방향을 찾아 한 걸음 내딛는 일, 비록 불안할지라도 그것은 우리 삶이 꽃피기 시작하는 가장 설레는 기적입니다.”", translation: { ja: "「新しい方向を模索して一歩を踏み出すこと、たとえ不安であっても、それは私たちの人生が花開き始める最もときめく奇跡です」", en: "“Taking a step toward a new direction, even if anxious, is the most exciting miracle where our lives begin to blossom.”" } },
        { type: "오늘의 편지", emotion: "평온", content: "“어른이 되어가는 과정에서 겪는 아픔이나 결핍을 다독이고, 스스로를 따뜻한 시선으로 바라보며 '지금' 행복해지는 마음의 자세를 배워갑니다.”", translation: { ja: "「大人になる過程で経験する痛みや欠乏をなだめ、自分自身を温かい視선で見つめながら『今』幸せになる心の姿勢を学んでいきます」", en: "“We soothe the pain or deprivation experienced in the process of becoming an adult, and learn the mental attitude to be happy 'now' by looking at ourselves with warm eyes.”" } },
        { type: "오늘의 편지", emotion: "평온", content: "“모두에게 무리하여 좋은 사람이 되려 하기보다, 내 마음의 온기를 먼저 돌볼 때 비로소 진정한 평화가 깃듭니다.”", translation: { ja: "「すべての人に無理して良い人になろうとするより、自分の心の中の温もりをまずケアする時、初めて真の平和が宿ります」", en: "“Rather than trying hard to be a good person to everyone, true peace resides only when we care for the warmth in our own hearts first.”" } },
        { type: "오늘의 편지", emotion: "평온", content: "“'나는 이런 사람이야'라며 억지로 규정하지 않을 때, 마음속에는 비로소 고요하고 넓은 평온함이 찾아옵니다.”", translation: { ja: "「『私はこういう人間だ』と無理に規定しない時、心の中には初めて穏やかで広い平穏が訪れます」", en: "“When we do not force ourselves to be defined as 'I am this kind of person,' a calm and wide serenity finally visits our hearts.”" } },
        { type: "오늘의 편지", emotion: "평온", content: "“불안마저 일상의 자연스러운 부분으로 받아들이고 흘려보낼 때, 우리의 일상은 가장 정갈하고 평화로워집니다.”", translation: { ja: "「不安さえも日常の自然な一部として受け入れ、流し出す時、私たちの日常は最も端正で平和になります」", en: "“When we accept and let go of even anxiety as a natural part of daily life, our daily life becomes the most neat and peaceful.”" } },
        { type: "오늘의 편지", emotion: "평온", content: "“아무 일도 일어나지 않는 오후, 가볍게 스쳐 가는 새소리와 바람 소리 속에 우리의 평화가 조용히 깃들어 있다.”", translation: { ja: "「何事も起こらない午後、軽くかすめていく鳥のさえずりと風の音の中に、私たちの平和が静かに宿っています」", en: "“On an afternoon when nothing happens, our peace quietly dwells in the sound of birds and the wind lightly brushing by.”" } }
      ]);
    });

    // Open DB
    db.open().then(async () => {
      const primerCount = await db.primers.count();
      if (primerCount === 0) {
        await db.personas.bulkAdd([
          { name: '하루 (위로)', style: '예쁜 일본어 구어체', tone: '따스하고 다정한 목소리', preferredWritingStyle: '소박하고 따스한 말투' },
          { name: '사쿠라 (설렘)', style: '귀엽고 낭만적인 구어체', tone: '맑고 생기 넘치는 목소리', preferredWritingStyle: '발랄하고 감성 가득한 말투' },
          { name: '렌 (평온)', style: '차분하고 정갈한 구어체', tone: '나직하고 깊은 목소리', preferredWritingStyle: '담담하면서 평화로운 말투' }
        ]);
        await db.primers.bulkAdd([
          { type: "오늘의 편지", emotion: "위로", content: "“삶이 어디로 향하고 있는지 방향을 잃은 것 같다고 느끼는 분들께 이런 말을 해주고 싶어요. '나는 이런 사람이야' 하면서 자신을 가두거나, '나는 안 맞아' 하면서 미리 포기하지 마세요.” — 김창완 <이제야 보이네> 중에서", translation: { ja: "「人生がどこに向かっているのか、方向を見失ったと感じている方々に、こんな言葉を贈りたいです。『私はこういう人間だから』と自分を閉じ込めたり、『自分には合わない』と最初から諦めたりしないでください」 — キム・チャンワン『やっと見えるね』より", en: "“To those who feel they have lost their direction in life, I want to say this. Don't trap yourself by saying 'I'm this kind of person,' or give up in advance saying 'It doesn't suit me.'” — From Kim Chang-wan <Only Now I See>" } },
          { type: "오늘의 편지", emotion: "위로", content: "“부디 자기 인생을 다른 사람과 비교하며 비참해지지 않았으면 좋겠습니다. 허탈함 속의 나를 발견하는 것도 나쁘지 않아요. 괜한 불안을 느끼는 일도 일상의 아름다움 아닐까요?” — 김창완 <이제야 보이네> 중에서", translation: { ja: "「혹시 자신의 인생을 다른 사람과 비교하며 비참해지지 않았으면 좋겠습니다. 허탈함 속의 나를 발견하는 것도 나쁘지 않아요. 괜한 불안을 느끼는 일도 일상의 아름다움 아닐까요？」 — キム・チャンワン『やっと見えるね』より", en: "“I hope you don't make yourself miserable by comparing your life to others. Discovering yourself in emptiness isn't bad either. Isn't feeling unnecessary anxiety also a beauty of daily life?” — From Kim Chang-wan <Only Now I See>" } },
          { type: "오늘의 편지", emotion: "위로", content: "“자신을, 우리 삶을 재단하지 말아요. 어마어마한 기적을 가두지 말자고요.” — 김창완 <이제야 보이네> 중에서", translation: { ja: "「自分を、私たちの人生を裁かないでください. とてつもない奇跡を閉じ込めないでいましょう」 — キム・チャンワン『やっと見えるね』より", en: "“Let's not judge ourselves, or our lives. Let's not confine this immense miracle.” — From Kim Chang-wan <Only Now I See>" } },
          { type: "오늘의 편지", emotion: "위로", content: "“우리는 매일 밤 서로의 목소리에 기대어 보이지 않는 선을 잇는다. 그것은 하루를 견뎌낸 이들에게 주는 소박한 위안이다.”", translation: { ja: "「私たちは毎晩、お互いの声に寄り添い、見えない線をつなぐ。それは一日を耐え抜いた人々への、ささやかな慰めだ」", en: "“Every night, we lean on each other's voices to connect invisible lines. It is a simple comfort to those who have endured the day.”" } },
          { type: "오늘의 편지", emotion: "위로", content: "“그늘이 깊다는 것은 그만큼 빛이 가깝다는 뜻입니다. 당신의 지친 하루에 조용히 손을 얹습니다.”", translation: { ja: "「陰が深いということは, それだけ光が近いという意味です。あなたの疲れた一日に、静かに手を添えます」", en: "“A deep shadow means that the light is just that close. I quietly lay my hand on your tiring day.”" } },
          { type: "오늘의 편지", emotion: "설렘", content: "“아이들이 놀아달라고 하는 것은 부모와 눈을 맞추고 따뜻한 교감을 하고 싶다는 신호입니다. 그것이 우리 안에 숨겨진 가장 맑고 설레는 만남의 시작입니다.”", translation: { ja: "「子供たちが遊んでほしいと言うのは、親と目を合わせ、温かい交感をしたいというシグナルです。それが私たちの中に隠された、最も澄んだときめく出会いの始まりです」", en: "“Children asking to play is a signal that they want to make eye contact and have a warm connection with their parents. It is the beginning of the clearest and most exciting meeting hidden within us.”" } },
          { type: "오늘의 편지", emotion: "설렘", content: "“가족과 함께 보내는 여가 시간은 서로를 더 깊이 이해하고 신뢰를 쌓아가는 신비한 울타리이자, 일상 속 작은 소풍과 같습니다.”", translation: { ja: "「家族と過ごす余暇時間は、お互いをより深く理解し、信頼を築いていく神秘的な垣根であり、日常の中の小さな遠足のようです」", en: "“Leisure time spent with family is a mysterious fence where we understand each other deeper and build trust, like a small picnic in daily life.”" } },
          { type: "오늘의 편지", emotion: "설렘", content: "“어쩌면 오늘, 바람결에 실려 온 맑은 목소리가 당신의 마음을 가만히 두드릴지도 모릅니다. 설레는 맘으로 기다려 보세요.”", translation: { ja: "「もしかしたら今日、風に乗って届いた澄んだ声が、あなたの心をそっと叩くかもしれません。ワクワクする気持ちで待ってみてください」", en: "“Perhaps today, a clear voice carried on the wind might gently knock on your heart. Please wait for it with an excited heart.”" } },
          { type: "오늘의 편지", emotion: "설렘", content: "“새로운 방향을 찾아 한 걸음 내딛는 일, 비록 불안할지라도 그것은 우리 삶이 꽃피기 시작하는 가장 설레는 기적입니다.”", translation: { ja: "「新しい方向を模索し、一歩を踏み出すこと。たとえ不安であっても、それは私たちの人生が花開き始める、最もワクワクする奇跡です」", en: "“Stepping out to find a new direction, even if anxious, is the most exciting miracle where our lives begin to bloom.”" } },
          { type: "오늘의 편지", emotion: "평온", content: "“어른이 되어가는 과정에서 겪는 아픔이나 결핍을 다독이고, 스스로를 따뜻한 시선으로 바라보며 '지금' 행복해지는 마음의 자세를 배워갑니다.”", translation: { ja: "「大人になっていく過程で経験する痛みや欠乏をなぐさめ、自分自身を温かい目で見つめながら『今』幸せになる心の姿勢を学んでいきます」", en: "“We learn the attitude of mind to heal the pain or deficiency experienced in the process of becoming an adult, look at ourselves with a warm gaze, and become happy 'now.'”" } },
          { type: "오늘의 편지", emotion: "평온", content: "“모두에게 무리하여 좋은 사람이 되려 하기보다, 내 마음의 온기를 먼저 돌볼 때 비로소 진정한 평화가 깃듭니다.”", translation: { ja: "「すべての人に無理して良い人になろうとするより、自分の心の温もりをまずケアする時、初めて本当の平和が宿ります」", en: "“Instead of trying to be a good person to everyone by overworking, true peace dwells only when we first take care of the warmth of our own heart.”" } },
          { type: "오늘의 편지", emotion: "평온", content: "“'나는 이런 사람이야'라며 억지로 규정하지 않을 때, 마음속에는 비로소 고요하고 넓은 평온함이 찾아옵니다.”", translation: { ja: "「自分を『こういう人間だ』と無理に規定しない時、心の中には初めて静かで広い平穏が訪れます」", en: "“When we do not force ourselves to be defined as 'I am this kind of person,' a calm and wide serenity finally visits our hearts.”" } },
          { type: "오늘의 편지", emotion: "평온", content: "“불안마저 일상의 자연스러운 부분으로 받아들이고 흘려보낼 때, 우리의 일상은 가장 정갈하고 평화로워집니다.”", translation: { ja: "「不安さえも日常の自然な一部として受け入れ、流し出す時、私たちの日常は最も端正で平和になります」", en: "“When we accept and let go of even anxiety as a natural part of daily life, our daily life becomes the most neat and peaceful.”" } },
          { type: "오늘의 편지", emotion: "평온", content: "“아무 일도 일어나지 않는 오후, 가볍게 스쳐 가는 새소리와 바람 소리 속에 우리의 평화가 조용히 깃들어 있다.”", translation: { ja: "「何事も起こらない午後、軽くかすめていく鳥のさえずりと風の音の中に、私たちの平和が静かに宿っています」", en: "“On an afternoon when nothing happens, our peace quietly dwells in the sound of birds and the wind lightly brushing by.”" } }
        ]);
        
        await loadPrimersFromDB();
        updatePrimerUI();
      }
    }).catch((err) => {
      console.error("DB 오픈 실패:", err);
    });