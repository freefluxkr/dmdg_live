if('serviceWorker' in navigator) {
    navigator.serviceWorker.register('sw.js');
}

// Initialize Dexie DB
const db = new Dexie('CasualWishDB');
db.version(1).stores({
    wishes: '++id, name, story, photo, x, y, rot, timestamp'
});

const inputPanel = document.getElementById('input-panel');
const treeContainer = document.getElementById('tree-container');
const photoUpload = document.getElementById('photo-upload');
const previewImg = document.getElementById('preview-img');
const startBtn = document.getElementById('start-btn');
const photoIcon = document.getElementById('photo-icon');

const soundPop = new Audio('https://actions.google.com/sounds/v1/cartoon/cartoon_boing.ogg'); 

const noteColors = ['#fff9c4', '#ffcdd2', '#c8e6c9', '#bbdefb', '#e1bee7'];

function createStickyNote(wish, isNew = false) {
    const el = document.createElement('div');
    el.className = 'sticky-note';
    
    const color = noteColors[(wish.id || Math.floor(Math.random()*10)) % noteColors.length];
    el.style.backgroundColor = color;
    
    el.style.setProperty('--rot', wish.rot + 'deg');
    
    if(isNew) {
        el.classList.add('neon-glow');
    } else {
        el.style.transform = `rotate(${wish.rot}deg)`;
    }
    
    el.style.left = wish.x + '%';
    el.style.top = wish.y + '%';
    
    const photoEl = document.createElement('div');
    photoEl.className = 'note-photo';
    photoEl.style.backgroundImage = `url('${wish.photo}')`;
    
    const nameEl = document.createElement('div');
    nameEl.className = 'note-name';
    nameEl.innerText = wish.name;
    
    el.appendChild(photoEl);
    el.appendChild(nameEl);
    
    el.addEventListener('click', () => {
        alert(`[${wish.name}]\n사연: ${wish.story}\n\n"소원 나무가 당신의 마음을 위로합니다. 🌸"`);
    });
    
    treeContainer.appendChild(el);
    
    if(isNew) {
        setTimeout(() => {
            el.classList.remove('neon-glow');
            el.style.transform = `rotate(${wish.rot}deg)`;
        }, 3000);
    }
}

async function loadWishes() {
    const wishes = await db.wishes.toArray();
    wishes.forEach(w => createStickyNote(w));
}
loadWishes();

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
        alert("이름과 사진을 꼭 넣어주세요!"); return;
    }
    
    // Random position within the leafy area of the tree
    const x = 15 + Math.random() * 70;
    const y = 15 + Math.random() * 50;
    const rot = -20 + Math.random() * 40; 
    
    const newWish = {
        name, story, photo: photoBase64, x, y, rot, timestamp: Date.now()
    };
    
    // Generate id locally immediately for color consistency
    const id = await db.wishes.add(newWish);
    newWish.id = id;
    
    inputPanel.style.transform = 'translateY(100%)';
    soundPop.play();
    
    createStickyNote(newWish, true);
    
    setTimeout(() => {
        inputPanel.style.transform = 'translateY(0)';
        document.getElementById('target-name').value = '';
        document.getElementById('target-story').value = '';
        previewImg.classList.add('hidden');
        photoIcon.classList.remove('hidden');
        photoBase64 = null;
    }, 3000); 
});
