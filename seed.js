import { db } from "./src/firebase.js";
import { collection, writeBatch, doc } from "firebase/firestore";

// 일상스토리 / 문화생활정보 카테고리 글 데이터
const letters = [
  {
    category: "일상스토리",
    emotion: "위로",
    title: "삶의 방향을 잃은 당신에게",
    content: "“삶이 어디로 향하고 있는지 방향을 잃은 것 같다고 느끼는 분들께 이런 말을 해주고 싶어요. '나는 이런 사람이야' 하면서 자신을 가두거나, '나는 안 맞아' 하면서 미리 포기하지 마세요. 부디 자기 인생을 다른 사람과 비교하며 비참해지지 않았으면 좋겠습니다. 허탈함 속의 나를 발견하는 것도 나쁘지 않아요. 괜한 불안을 느끼는 일도 일상의 아름다움 아닐까요? 자신을, 우리 삶을 재단하지 말아요. 어마어마한 기적을 가두지 말자고요.” — 김창완 <이제야 보이네> 중에서"
  },
  {
    category: "일상스토리",
    emotion: "위로",
    title: "그늘 속의 위로",
    content: "“그늘이 깊다는 것은 그만큼 빛이 가깝다는 뜻입니다. 당신의 지친 하루에 조용히 손을 얹습니다. 괜찮아요, 오늘 하루 참 고생 많으셨습니다.”"
  },
  {
    category: "일상스토리",
    emotion: "위로",
    title: "위안의 연결",
    content: "“우리는 매일 밤 서로의 목소리에 기대어 보이지 않는 선을 잇는다. 그것은 하루를 견뎌낸 이들에게 주는 소박한 위안이다.”"
  },
  {
    category: "일상스토리",
    emotion: "평온",
    title: "진정한 나를 찾는 평온",
    content: "“'나는 이런 사람이야'라며 억지로 규정하지 않을 때, 마음속에는 비로소 고요하고 넓은 평온함이 찾아옵니다. 나를 정의하는 복잡한 수식어를 내려놓고 그냥 숨을 쉬어 보세요.”"
  },
  {
    category: "일상스토리",
    emotion: "평온",
    title: "일상 수용의 평화",
    content: "“불안마저 일상의 자연스러운 부분으로 받아들이고 흘려보낼 때, 우리의 일상은 가장 정갈하고 평화로워집니다. 바람이 불면 흔들리는 대로, 비가 오면 내리는 대로 흘러가 봅시다.”"
  },
  {
    category: "문화생활정보",
    emotion: "설렘",
    title: "교감이라는 이름의 소풍",
    content: "“아이들이 놀아달라고 하는 것은 부모와 눈을 맞추고 따뜻한 교감을 하고 싶다는 신호입니다. 그것이 우리 안에 숨겨진 가장 맑고 설레는 만남의 시작입니다.”"
  },
  {
    category: "문화생활정보",
    emotion: "설렘",
    title: "가족과 함께하는 소풍",
    content: "“가족과 함께 보내는 여가 시간은 서로를 더 깊이 이해하고 신뢰를 쌓아가는 신비한 울타리이자, 일상 속 작은 소풍과 같습니다. 함께 걷는 길 위에 설렘의 꽃이 핍니다.”"
  },
  {
    category: "문화생활정보",
    emotion: "설렘",
    title: "소리의 문을 두드리다",
    content: "“어쩌면 오늘, 바람결에 실려 온 맑은 목소리가 당신의 마음을 가만히 두드릴지도 모릅니다. 설레는 맘으로 귀 기울여 들어보세요.”"
  },
  {
    category: "문화생활정보",
    emotion: "평온",
    title: "자연의 평온함",
    content: "“아무 일도 일어나지 않는 오후, 가볍게 스쳐 가는 새소리와 바람 소리 속에 우리의 평화가 조용히 깃들어 있다.”"
  },
  {
    category: "문화생활정보",
    emotion: "평온",
    title: "내면의 고요한 방",
    content: "“소리치며 바쁘게 달려가던 발걸음을 멈추고 내면의 방에 초를 켭니다. 고요하게 머물 때 마음은 가장 깨끗하게 씻겨 나갑니다.”"
  }
];

async function seedFirestore() {
  console.log("Firestore 데이터 적재 시작...");
  const batch = writeBatch(db);
  const primersCol = collection(db, "primers");

  letters.forEach((letter, index) => {
    const docRef = doc(primersCol, `letter_${index + 1}`);
    batch.set(docRef, {
      ...letter,
      timestamp: Date.now(),
      type: "오늘의 편지"
    });
  });

  await batch.commit();
  console.log("Firestore 데이터 적재 성공!");
}

seedFirestore().catch(console.error);
