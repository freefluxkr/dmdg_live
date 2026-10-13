// Initialize Lucide Icons
lucide.createIcons();

// DOM Elements
const htmlEl = document.documentElement;
const secretTrigger = document.getElementById('secret-trigger');
const appContainer = document.getElementById('app-container');
const glitchOverlay = document.getElementById('glitch-overlay');

const appTitle = document.getElementById('app-title');
const appSubtitle = document.getElementById('app-subtitle');
const nameLabel = document.getElementById('name-label');
const targetName = document.getElementById('target-name');
const belongingLabel = document.getElementById('belonging-label');
const targetBelonging = document.getElementById('target-belonging');
const submitBtn = document.getElementById('submit-btn');
const photoLabel = document.getElementById('photo-label');

const photoUpload = document.getElementById('photo-upload');
const previewImg = document.getElementById('preview-img');
const photoIcon = document.getElementById('photo-icon');

// State
let isOccultMode = false;
let clickCount = 0;
let clickTimer;

// Secret Trigger Logic (3 clicks in top left corner)
secretTrigger.addEventListener('click', () => {
    clickCount++;
    clearTimeout(clickTimer);
    
    if (clickCount >= 3) {
        toggleMode();
        clickCount = 0;
    } else {
        clickTimer = setTimeout(() => { clickCount = 0; }, 1000);
    }
});

// Toggle between Casual and Occult Mode
function toggleMode() {
    isOccultMode = !isOccultMode;
    
    // Trigger Intense Glitch Effect
    appContainer.classList.add('is-glitching');
    glitchOverlay.classList.add('glitch-overlay-active');
    
    // Sound effect could go here (e.g. heartbeat or static noise)
    
    setTimeout(() => {
        appContainer.classList.remove('is-glitching');
        glitchOverlay.classList.remove('glitch-overlay-active');
        
        if (isOccultMode) {
            // Apply Occult Mode (Bangbeop)
            htmlEl.classList.remove('theme-casual');
            htmlEl.classList.add('theme-occult');
            document.title = "謗法 (방법)";
            
            appTitle.innerHTML = "謗法 (방법)";
            appSubtitle.innerText = "원한을 끊어내고 저주를 내리십시오.";
            
            nameLabel.innerText = "한자 이름 (漢字 姓名)";
            targetName.placeholder = "저주할 대상의 한자 이름";
            
            photoLabel.innerText = "대상의 사진 (사진 필수)";
            
            belongingLabel.innerText = "소지품 (所持品) 및 사연";
            targetBelonging.placeholder = "대상의 소지품이나 원한이 깃든 사연을 적으십시오...";
            
            submitBtn.innerText = "방법(謗法) 실행";
        } else {
            // Apply Casual Mode (Mindfulness)
            htmlEl.classList.remove('theme-occult');
            htmlEl.classList.add('theme-casual');
            document.title = "마음 다이어리";
            
            appTitle.innerText = "감정 쓰레기통";
            appSubtitle.innerText = "미운 마음을 털어놓고 홀가분해지세요.";
            
            nameLabel.innerText = "이름";
            targetName.placeholder = "누가 당신을 힘들게 했나요?";
            
            photoLabel.innerText = "대상의 사진 (선택)";
            
            belongingLabel.innerText = "속마음 이야기";
            targetBelonging.placeholder = "그 사람에게 하고 싶은 말을 적어보세요...";
            
            submitBtn.innerText = "비워내기";
        }
    }, 800); // 800ms glitch transition
}

// Photo Preview Logic
photoUpload.addEventListener('change', function(e) {
    if (this.files && this.files[0]) {
        const reader = new FileReader();
        reader.onload = function(e) {
            previewImg.src = e.target.result;
            previewImg.classList.remove('hidden');
            photoIcon.classList.add('hidden');
            
            // Add a subtle creepy effect if in occult mode
            if (isOccultMode) {
                previewImg.style.filter = "grayscale(100%) contrast(150%) sepia(50%) hue-rotate(320deg)";
            } else {
                previewImg.style.filter = "none";
            }
        }
        reader.readAsDataURL(this.files[0]);
    }
});

// Submit Button Logic
submitBtn.addEventListener('click', () => {
    const name = targetName.value.trim();
    const hasPhoto = !previewImg.classList.contains('hidden');
    
    if (!name) {
        alert(isOccultMode ? "이름(漢字)을 입력해야 방법이 시작됩니다." : "이름을 입력해주세요.");
        return;
    }

    if (isOccultMode && !hasPhoto) {
        alert("사진이 없으면 방법을 내릴 수 없습니다.");
        return;
    }

    if (isOccultMode) {
        // Occult Execution Animation
        appContainer.classList.add('is-glitching');
        htmlEl.classList.add('cursing-active');
        submitBtn.innerText = "저주하는 중...";
        submitBtn.disabled = true;
        
        setTimeout(() => {
            appContainer.classList.remove('is-glitching');
            htmlEl.classList.remove('cursing-active');
            
            // Show Result Screen
            appContainer.innerHTML = `
                <div class="p-10 text-center space-y-6 flex flex-col items-center justify-center min-h-[400px]">
                    <h2 class="text-5xl font-bold text-red-600 font-serif" style="text-shadow: 0 0 10px red;">謗法 完了</h2>
                    <p class="text-red-400 text-lg">방법이 성공적으로 이루어졌습니다.</p>
                    <div class="w-32 h-32 my-6 opacity-50 grayscale contrast-150" style="background-image: url('${previewImg.src}'); background-size: cover; border-radius: 50%; box-shadow: inset 0 0 20px black, 0 0 20px red;"></div>
                    <p class="text-sm text-red-700 tracking-widest mt-10">살(煞)이 날아갔습니다.</p>
                    <button onclick="location.reload()" class="mt-8 px-8 py-3 border border-red-800 text-red-500 rounded hover:bg-red-900 transition font-serif tracking-widest">돌아가기</button>
                </div>
            `;
        }, 3000); // 3 seconds of cursing
        
    } else {
        // Casual Execution Animation
        submitBtn.innerText = "날려보내는 중...";
        submitBtn.disabled = true;
        submitBtn.classList.add('opacity-50');
        
        setTimeout(() => {
            appContainer.innerHTML = `
                <div class="p-10 text-center space-y-6 flex flex-col items-center justify-center min-h-[400px]">
                    <i data-lucide="wind" class="w-20 h-20 text-blue-400 mx-auto opacity-70"></i>
                    <h2 class="text-2xl font-bold text-gray-700">홀가분해졌어요!</h2>
                    <p class="text-gray-500">당신의 미운 마음이 바람에 멀리 날아갔습니다.</p>
                    <button onclick="location.reload()" class="mt-8 px-6 py-3 bg-blue-100 text-blue-700 rounded-lg hover:bg-blue-200 transition font-bold shadow">다시 쓰기</button>
                </div>
            `;
            lucide.createIcons();
        }, 1500);
    }
});
