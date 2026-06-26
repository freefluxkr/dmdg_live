// Firebase Configuration
    const firebaseConfig = {
      apiKey: "AIzaSyBcS8aS5yHk2KFNYPImXslsFkSyoBwYrKI",
      authDomain: "dmdg-live.firebaseapp.com",
      projectId: "dmdg-live",
      storageBucket: "dmdg-live.firebasestorage.app",
      messagingSenderId: "357433220336",
      appId: "1:357433220336:web:1a8914811da09123a0f635",
      measurementId: "G-RRYE7JKKWX"
    };
    firebase.initializeApp(firebaseConfig);
    const firestore = firebase.firestore();

    const audioEngine = new AudioPlayerEngine();
    let currentFilter = '전체';
    const emotions = ['전체', '위로', '설렘', '평온'];
    let isRecording = false;
    let mediaRecorder = null;
    let audioChunks = [];
    let canvasAnimationId = null;

    let loadedPrimers = [];
    let currentPrimerIndex = 0;