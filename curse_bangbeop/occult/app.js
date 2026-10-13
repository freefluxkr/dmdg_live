if('serviceWorker' in navigator) {
    navigator.serviceWorker.register('sw.js');
}

// Initialize Dexie DB
const db = new Dexie('OccultCurseDB');
db.version(1).stores({
    curses: '++id, name, story, photo, x, y, timestamp'
});

const inputPanel = document.getElementById('input-panel');
const treeContainer = document.getElementById('tree-container');
const photoUpload = document.getElementById('photo-upload');
const previewImg = document.getElementById('preview-img');
const startBtn = document.getElementById('start-btn');
const photoIcon = document.getElementById('photo-icon');

// Sounds
const soundBell = new Audio('https://actions.google.com/sounds/v1/alarms/digital_watch_alarm_long.ogg'); 
const soundWind = new Audio('https://actions.google.com/sounds/v1/horror/creepy_wind.ogg');
soundWind.loop = true;
soundWind.volume = 0.4;

document.body.addEventListener('click', () => {
    if(soundWind.paused) soundWind.play().catch(e=>console.log(e));
}, {once:true});

function createTalisman(curse, isNew = false) {
    const el = document.createElement('div');
    el.className = 'talisman';
    if(isNew) el.classList.add('neon-glow');
    
    el.style.left = curse.x + '%';
    el.style.top = curse.y + '%';
    el.style.backgroundImage = `url('${curse.photo}')`;
    
    const nameEl = document.createElement('div');
    nameEl.className = 'talisman-name';
    nameEl.innerText = curse.name.substring(0, 3);
    
    el.appendChild(nameEl);
    
    el.addEventListener('click', () => {
        alert(`[${curse.name}]\n사연: ${curse.story}\n\n"이미 신목에 묶인 원한입니다. 평온을 찾으십시오."`);
    });
    
    treeContainer.appendChild(el);
    
    // Remove neon glow after some time for new curses so they blend in
    if(isNew) {
        setTimeout(() => {
            el.classList.remove('neon-glow');
            el.style.border = '1px solid #7f1d1d';
        }, 5000);
    }
}

async function loadCurses() {
    const curses = await db.curses.toArray();
    curses.forEach(c => createTalisman(c));
}
loadCurses();

let photoBase64 = null;
photoUpload.addEventListener('change', function(e) {
    if(this.files && this.files[0]) {
        const reader = new FileReader();
        reader.onload = function(e) {
            photoBase64 = e.target.result;
            previewImg.src = photoBase64;
            previewImg.classList.remove('hidden');
            photoIcon.classList.add('hidden');
        }
        reader.readAsDataURL(this.files[0]);
    }
});

startBtn.addEventListener('click', async () => {
    const name = document.getElementById('target-name').value;
    const story = document.getElementById('target-story').value;
    
    if(!name || !photoBase64) {
        alert("이름과 사진이 없으면 매달 수 없습니다."); return;
    }
    
    // Generate random position on the upper branches (y: 10% to 55%, x: 10% to 90%)
    const x = 10 + Math.random() * 80;
    const y = 10 + Math.random() * 45;
    
    const newCurse = {
        name, story, photo: photoBase64, x, y, timestamp: Date.now()
    };
    
    await db.curses.add(newCurse);
    
    inputPanel.style.transform = 'translateY(100%)';
    soundBell.play();
    
    createTalisman(newCurse, true);
    
    setTimeout(() => {
        inputPanel.style.transform = 'translateY(0)';
        document.getElementById('target-name').value = '';
        document.getElementById('target-story').value = '';
        previewImg.classList.add('hidden');
        photoIcon.classList.remove('hidden');
        photoBase64 = null;
    }, 4000); 
});
