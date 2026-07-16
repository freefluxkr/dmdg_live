const admin = require("firebase-admin");
const serviceAccount = require("./serviceAccountKey.json");

admin.initializeApp({
  credential: admin.credential.cert(serviceAccount)
});

const db = admin.firestore();

const letters = [
    {
        "category": "일상스토리",
        "emotion": "위로",
        "title": "서두르지 않아도 괜찮아",
        "content": "“남들의 속도에 맞춰 억지로 뛸 필요는 없습니다. 걷는 것도, 잠시 멈춰 서서 하늘을 보는 것도 우리 삶의 소중한 한 걸음입니다. 당신은 지금 아주 잘하고 있습니다.”",
        "type": "오늘의 편지"
    },
    {
        "category": "일상스토리",
        "emotion": "위로",
        "title": "눈물을 참지 말아요",
        "content": "“때로는 눈물이 지친 마음을 깨끗이 씻어내 줍니다. 억지로 강한 척 참을 필요 없어요. 울고 싶은 날에는 마음껏 소리 내어 울어도 괜찮습니다.”",
        "type": "오늘의 편지"
    },
    {
        "category": "일상스토리",
        "emotion": "위로",
        "title": "실수투성이 하루 끝에",
        "content": "“오늘 하루 수많은 실수를 저질렀다 해도 자책하지 마세요. 그 실수는 더 단단하고 아름다운 내일을 빚어내는 소중한 흙이 되어줄 것입니다.”",
        "type": "오늘의 편지"
    },
    {
        "category": "일상스토리",
        "emotion": "위로",
        "title": "가장 따스한 집",
        "content": "“바깥 세상이 아무리 차갑고 냉혹해도, 내 마음속의 작은 방만큼은 항상 스스로를 따뜻하게 안아줄 수 있는 온기가 머무는 곳이어야 합니다.”",
        "type": "오늘의 편지"
    },
    {
        "category": "일상스토리",
        "emotion": "위로",
        "title": "상처를 다독이는 목소리",
        "content": "“귀를 가만히 기울여 보세요. 보이지 않는 곳에서 당신의 하루를 응원하며 조용히 위안의 기운을 불어넣어 주는 다정한 속삭임이 들릴 것입니다.”",
        "type": "오늘의 편지"
    },
    {
        "category": "일상스토리",
        "emotion": "설렘",
        "title": "아침 햇살의 속삭임",
        "content": "“매일 아침 눈을 뜰 때 마주하는 얇은 커튼 사이의 햇살은, 오늘 하루 우리에게 찾아올 수많은 기분 좋은 우연과 만남을 설레게 예고해 줍니다.”",
        "type": "오늘의 편지"
    },
    {
        "category": "일상스토리",
        "emotion": "설렘",
        "title": "기분 좋은 엇박자",
        "content": "“예상치 못한 버스의 정차, 우연히 마주친 옛 친구. 우리의 계획된 일상이 조금 어긋나는 순간이야말로 설렘이 싹트는 가장 아름다운 찰나입니다.”",
        "type": "오늘의 편지"
    },
    {
        "category": "일상스토리",
        "emotion": "설렘",
        "title": "작은 미소의 전염",
        "content": "“지나가는 낯선 이가 건넨 아주 소박한 미소 한 조각이, 차갑게 굳어 있던 가슴속에 묘한 설렘과 행복을 퍼뜨리는 마법이 됩니다.”",
        "type": "오늘의 편지"
    },
    {
        "category": "일상스토리",
        "emotion": "설렘",
        "title": "다시 시작하는 설렘",
        "content": "“오랫동안 덮어두었던 낡은 책을 펼치듯, 내 가슴속 깊이 묻어 두었던 꿈틀거리는 열정에 불을 지피는 순간은 언제나 가슴 벅차게 설렙니다.”",
        "type": "오늘의 편지"
    },
    {
        "category": "일상스토리",
        "emotion": "평온",
        "title": "오후 3시의 고요",
        "content": "“시계 초침이 흘러가는 소리 외엔 아무런 소음도 들리지 않는 평일의 고요한 오후. 차 한잔의 따스함 속에 나의 복잡한 사념들을 조용히 흘려보냅니다.”",
        "type": "오늘의 편지"
    },
    {
        "category": "일상스토리",
        "emotion": "평온",
        "title": "바람을 껴안다",
        "content": "“내 볼을 스치고 지나가는 청량한 바람에 가만히 눈을 감아 봅니다. 바람이 가져다주는 대자연의 고요가 머릿속을 맑게 씻어내어 줍니다.”",
        "type": "오늘의 편지"
    },
    {
        "category": "일상스토리",
        "emotion": "평온",
        "title": "내려놓는 평화",
        "content": "“무언가를 끊임없이 움켜쥐고 애쓰려는 조바심을 조용히 내려놓을 때, 비로소 내 마음의 넓은 호수 위에는 고요하고 투명한 평온함이 자리합니다.”",
        "type": "오늘의 편지"
    },
    {
        "category": "일상스토리",
        "emotion": "평온",
        "title": "비 내리는 밤의 창가",
        "content": "“톡톡 창문을 두드리는 빗소리를 배경음악 삼아 조용히 스탠드 불빛 아래 앉아 있을 때, 온 세상의 모든 조급함이 빗물과 함께 씻겨 내려갑니다.”",
        "type": "오늘의 편지"
    },
    {
        "category": "문화생활정보",
        "emotion": "위로",
        "title": "작은 미술관의 위로",
        "content": "“오래된 유화 그림 한 점 앞에 우두커니 서 있는 동안, 화가가 붓 끝에 꾹꾹 눌러 담은 위안의 질감이 지친 영혼에 따뜻한 감동을 선사합니다.”",
        "type": "오늘의 편지"
    },
    {
        "category": "문화생활정보",
        "emotion": "위로",
        "title": "클래식 선율이 건네는 품",
        "content": "“조용히 눈을 감고 듣는 클래식 첼로의 묵직하고 낮은 선율은, 소리 없는 눈물을 닦아주고 차분하게 내 안의 상처를 안아주는 넓은 품이 됩니다.”",
        "type": "오늘의 편지"
    },
    {
        "category": "문화생활정보",
        "emotion": "위로",
        "title": "그림책을 읽는 시간",
        "content": "“알록달록한 그림책 속 단순하지만 깊은 이야기는, 때론 복잡한 어른들의 지친 마음에 그 어떤 논리적인 조언보다 깊은 위로가 되어 줍니다.”",
        "type": "오늘의 편지"
    },
    {
        "category": "문화생활정보",
        "emotion": "설렘",
        "title": "연극 무대의 조명이 켜질 때",
        "content": "“어두운 극장 안, 심장 소리가 울릴 정도로 팽팽한 고요함 속에 핀 조명이 무대를 비추는 바로 그 순간은 말로 다 할 수 없는 설렘으로 가득 찹니다.”",
        "type": "오늘의 편지"
    },
    {
        "category": "문화생활정보",
        "emotion": "설렘",
        "title": "낯선 여행지의 냄새",
        "content": "“비행기나 기차에서 내려 처음 들이마시는 그 나라, 그 동네 특유의 낯선 흙내음과 공기는 우리 여행의 가장 설레는 첫 페이지를 엽니다.”",
        "type": "오늘의 편지"
    },
    {
        "category": "문화생활정보",
        "emotion": "설렘",
        "title": "공원의 거리 악사",
        "content": "“해가 지는 공원 잔디밭 위에서 들려오는 청량한 통기타 버스킹 소리. 그 즉흥적인 멜로디 속에 우리의 오늘 하루는 특별한 소풍이 됩니다.”",
        "type": "오늘의 편지"
    },
    {
        "category": "문화생활정보",
        "emotion": "평온",
        "title": "숲속 도서관의 하루",
        "content": "“초록빛 나뭇잎들이 그늘을 만들어 주는 숲속 작은 도서관에서, 사락사락 책장을 넘기며 맑은 피톤치드를 들이마실 때 내 마음은 가장 평화롭습니다.”",
        "type": "오늘의 편지"
    },
    {
        "category": "문화생활정보",
        "emotion": "평온",
        "title": "도자기 흙을 만지며",
        "content": "“시끄러운 소리를 모두 차단하고 물레 위의 젖은 흙 감촉에 온 신경을 집중하는 시간. 손끝에 흐르는 정갈한 평화가 마음의 번뇌를 씻겨 줍니다.”",
        "type": "오늘의 편지"
    },
    {
        "category": "문화생활정보",
        "emotion": "평온",
        "title": "차 앙상블",
        "content": "“따뜻한 물을 부었을 때 다관 속에서 천천히 기지개를 켜며 피어나는 말린 찻잎들의 무용을 조용히 관찰하는 일은 가장 고요한 평온의 예술입니다.”",
        "type": "오늘의 편지"
    }
];

async function seed() {
  console.log("DMDG-LIVE Firestore 데이터베이스 다량 적재를 시작합니다...");
  const primersCol = db.collection("primers");

  const snapshot = await primersCol.get();
  const deletePromises = [];
  snapshot.forEach(doc => {
    deletePromises.push(doc.ref.delete());
  });
  await Promise.all(deletePromises);
  console.log("기존의 임시 데이터를 깨끗하게 삭제했습니다.");

  const batch = db.batch();
  letters.forEach((letter, index) => {
    const docRef = primersCol.doc(`letter_${index + 1}`);
    batch.set(docRef, {
      ...letter,
      timestamp: admin.firestore.FieldValue.serverTimestamp()
    });
    console.log(`   ↳ [적재대상등록] [${letter.category}] (${letter.emotion}) - ${letter.title}`);
  });

  await batch.commit();
  console.log(`🎉 성공적으로 총 ${letters.length}개의 행복한가 감성 글귀 데이터를 강제 적재 완료했습니다!`);
}

seed().catch(err => {
  console.error("적재 중 에러 발생:", err);
});
