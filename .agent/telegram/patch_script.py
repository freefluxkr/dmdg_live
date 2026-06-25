"""script.js 530줄 이후를 Second Brain 버전으로 교체"""
import re

src = open(r'c:\Users\user\Downloads\connect_dmdg\global_service\script.js',
           'r', encoding='utf-8-sig')
lines = src.readlines()
src.close()

# 530번째 줄(0-indexed: 529)까지만 유지
keep = lines[:530]

# 새 Second Brain 코드
new_code = r"""
// --- 6. 여행 완료 및 스토리북 렌더링 ---
document.getElementById('btn-finish-trip').onclick = () => {
    switchScreen('map-screen', 'result-screen');
    renderStorybookPreview();
};

// 지식 클러스터 자동 분류 엔진
function autoClusterWords(stamps) {
    const clusterMap = {
        '음식 질감': ['바삭','쫄깃','살살','뜨끈','두툼','보글','노릇','고소','새콤','담백','푸짐','진하'],
        '풍경·분위기': ['야경','고즈넉','장엄','운치','아름'],
        '감정·포만감': ['든든','달콤','시원'],
        '문화·전통': ['한복','전통','돗자리','불쇼','해돋이','동백'],
    };
    const result = {};
    stamps.forEach(stamp => {
        if (!stamp.word) return;
        for (const [cluster, keywords] of Object.entries(clusterMap)) {
            if (keywords.some(k => stamp.word.includes(k))) {
                if (!result[cluster]) result[cluster] = [];
                result[cluster].push(stamp);
            }
        }
    });
    return result;
}

// Second Brain 마크다운 생성 (Obsidian 완전 호환)
function generateMarkdownContent() {
    const now    = new Date().toISOString().slice(0, 10);
    const cities = [...new Set(session.selectedStamps.map(s => s.city).filter(Boolean))];
    const clusters = autoClusterWords(session.selectedStamps);

    let md = '';
    // YAML Frontmatter
    md += '---\n';
    md += `title: "${session.storybookName}"\n`;
    md += `date: ${now}\n`;
    md += `traveler: "${session.name} (${session.nationality})"\n`;
    md += `gender: "${session.gender}" | age: "${session.age}"\n`;
    md += `purpose: [${session.purpose.map(p => `"${p}"`).join(', ')}]\n`;
    md += `cities: [${cities.map(c => `"${c}"`).join(', ')}]\n`;
    md += `word_count: ${session.selectedStamps.length}\n`;
    md += `tags: [KVJ, 한국여행, 한국어학습, SecondBrain, ${cities.join(', ')}]\n`;
    md += 'type: travel-second-brain\n';
    md += '---\n\n';

    // 타이틀
    md += `# 🌏 ${session.storybookName}\n\n`;
    md += `> **여행자**: ${session.name} | **출신**: ${session.nationality} | **날짜**: ${now}\n\n`;

    // 요약 카드
    md += '## 📊 나의 한국 지식 맵 요약\n\n';
    md += '| 항목 | 내용 |\n|------|------|\n';
    md += `| 🗺️ 방문 도시 | ${cities.join(' · ')} (${cities.length}개) |\n`;
    md += `| 🧠 학습 노드 | ${session.selectedStamps.length}개 체험 |\n`;
    md += `| 🔗 지식 클러스터 | ${Object.keys(clusters).length}개 자동 생성 |\n`;
    md += `| 🎯 여행 목적 | ${session.purpose.join(', ')} |\n\n`;
    md += '---\n\n';

    // 지식 노드
    md += '## 🗂️ 지식 노드 — 체험 아카이브\n\n';
    session.selectedStamps.forEach((stamp, idx) => {
        const cat = stamp.type === 'food' ? '🍜 음식체험' : '🏯 문화체험';
        md += `### ${idx + 1}. [[${stamp.name}]]\n\n`;
        md += `> *📍 ${(stamp.city || '').toUpperCase()} | ${cat}*\n\n`;
        md += '| 핵심 표현 | 핵심 단어 | 번역 |\n|----------|----------|------|\n';
        md += `| "${stamp.phrase}" | \`[[${stamp.word}]]\` | ${stamp.translation || '-'} |\n\n`;
        md += `**연관 태그**: \`#${stamp.word}\` \`#${stamp.city || ''}\` \`#${stamp.type === 'food' ? '음식체험' : '문화체험'}\`\n\n`;
        md += '---\n\n';
    });

    // 단어장
    md += '## 📚 나만의 의성어·의태어 단어장\n\n';
    md += '| # | 단어 | 배운 곳 | 영문 의미 |\n|---|------|--------|----------|\n';
    session.selectedStamps.forEach((stamp, idx) => {
        if (stamp.word) {
            const meaning = stamp.translation ? stamp.translation.slice(0, 40) + '...' : '-';
            md += `| ${idx + 1} | [[${stamp.word}]] | [[${stamp.name}]] | ${meaning} |\n`;
        }
    });
    md += '\n';

    // 자동 지식 클러스터
    if (Object.keys(clusters).length > 0) {
        md += '## 🔗 자동 생성 지식 클러스터\n\n';
        md += '> *KVJ Second Brain 엔진이 학습 패턴을 분석해 자동으로 연결했습니다*\n\n';
        for (const [name, cStamps] of Object.entries(clusters)) {
            md += `### 📌 ${name}\n`;
            cStamps.forEach(s => {
                md += `- [[${s.word}]] — [[${s.name}]] *(${(s.city || '').toUpperCase()})*\n`;
            });
            md += '\n';
        }
    }

    // 스크랩북
    if (session.scraps && session.scraps.length > 0) {
        md += '## 📸 스크랩북\n\n';
        session.scraps.forEach(s => { md += `- [[${s}]] ✅\n`; });
        md += '\n';
    }

    // 타임라인
    md += '## 🧭 나의 여행 타임라인\n\n';
    session.selectedStamps.forEach((stamp, idx) => {
        md += `- **Step ${idx + 1}**: ${stamp.city || ''} → [[${stamp.name}]] → \`${stamp.word}\` 습득\n`;
    });

    md += '\n---\n\n';
    md += '> *🧠 이 스토리북은 K-Virtual Journey Second Brain 엔진이 자동 생성했습니다.*\n';
    md += '> *Obsidian Vault로 가져오거나 Notion에 붙여넣기하여 나만의 한국 지식 베이스를 구축하세요!*\n';
    md += `> *생성일: ${now} | 이메일: ${session.email}*\n`;
    return md;
}

// 스토리북 HTML 미리보기
function renderStorybookPreview() {
    const stamps   = session.selectedStamps;
    const cities   = [...new Set(stamps.map(s => s.city).filter(Boolean))];
    const clusters = autoClusterWords(stamps);

    let html = `
        <div style="text-align:center;margin-bottom:20px;">
            <div style="font-size:40px;margin-bottom:8px;">🧠</div>
            <h3 style="margin:0;font-size:20px;">${session.storybookName}</h3>
            <p style="color:#94A3B8;font-size:13px;margin-top:6px;">${session.name} · ${session.nationality} · ${new Date().toLocaleDateString('ko-KR')}</p>
        </div>
        <div style="display:grid;grid-template-columns:repeat(3,1fr);gap:10px;margin-bottom:20px;">
            <div style="background:rgba(255,71,133,0.1);border:1px solid rgba(255,71,133,0.3);border-radius:10px;padding:14px;text-align:center;">
                <div style="font-size:26px;font-weight:900;color:#FF4785;">${cities.length}</div>
                <div style="font-size:11px;color:#94A3B8;margin-top:4px;">방문 도시</div>
            </div>
            <div style="background:rgba(121,40,202,0.1);border:1px solid rgba(121,40,202,0.3);border-radius:10px;padding:14px;text-align:center;">
                <div style="font-size:26px;font-weight:900;color:#A78BFA;">${stamps.length}</div>
                <div style="font-size:11px;color:#94A3B8;margin-top:4px;">지식 노드</div>
            </div>
            <div style="background:rgba(16,185,129,0.1);border:1px solid rgba(16,185,129,0.3);border-radius:10px;padding:14px;text-align:center;">
                <div style="font-size:26px;font-weight:900;color:#34D399;">${Object.keys(clusters).length || stamps.length}</div>
                <div style="font-size:11px;color:#94A3B8;margin-top:4px;">클러스터</div>
            </div>
        </div>
        <hr style="border:0.5px solid rgba(255,255,255,0.08);margin:15px 0;">
        <h4 style="font-size:11px;color:#64748B;margin-bottom:10px;letter-spacing:1px;">🗂️ 지식 노드 아카이브</h4>`;

    stamps.forEach((stamp, idx) => {
        html += `
        <div style="background:rgba(255,255,255,0.03);border:1px solid rgba(255,255,255,0.07);border-radius:10px;padding:12px;margin-bottom:8px;display:flex;justify-content:space-between;align-items:center;">
            <div style="flex:1;">
                <span style="font-size:10px;color:#FF4785;font-weight:bold;">${idx + 1}. ${(stamp.city || '').toUpperCase()}</span>
                <div style="font-weight:bold;font-size:14px;margin:3px 0;">${stamp.name}</div>
                <div style="font-size:11px;color:#64748B;font-style:italic;">"${stamp.phrase}"</div>
            </div>
            <span style="background:rgba(255,71,133,0.15);border:1px solid rgba(255,71,133,0.3);border-radius:20px;padding:4px 12px;font-size:12px;color:#FF4785;margin-left:12px;white-space:nowrap;">[[${stamp.word}]]</span>
        </div>`;
    });

    if (Object.keys(clusters).length > 0) {
        html += `<hr style="border:0.5px solid rgba(255,255,255,0.08);margin:15px 0;">
        <h4 style="font-size:11px;color:#64748B;margin-bottom:10px;letter-spacing:1px;">🔗 자동 생성 지식 클러스터</h4>`;
        for (const [name, cStamps] of Object.entries(clusters)) {
            html += `<div style="background:rgba(121,40,202,0.07);border:1px solid rgba(121,40,202,0.2);border-radius:8px;padding:10px;margin-bottom:8px;">
                <span style="font-size:12px;font-weight:bold;color:#A78BFA;">📌 ${name}</span>
                <span style="font-size:11px;color:#64748B;margin-left:8px;">${cStamps.map(s => `[[${s.word}]]`).join(' · ')}</span>
            </div>`;
        }
    }

    html += `<hr style="border:0.5px solid rgba(255,255,255,0.08);margin:15px 0;">
        <p style="font-size:11px;color:#475569;text-align:center;line-height:1.6;">
            🧠 <strong>Obsidian 호환 마크다운</strong>으로 저장하여<br>나만의 한국 Second Brain을 완성하세요!
        </p>`;

    document.getElementById('result-markdown-preview').innerHTML = html;
}

// 이메일 발송
document.getElementById('btn-send-email').onclick = () => {
    alert(`📧 [${session.email}] 주소로\n'${session.storybookName}' Second Brain 스토리북이 발송되었습니다!\n\n🧠 Obsidian/Notion에 붙여넣기하여 나만의 한국 지식 베이스를 구축하세요!`);
};

// Obsidian 호환 마크다운 저장
document.getElementById('btn-download-raw').onclick = () => {
    const md   = generateMarkdownContent();
    const blob = new Blob([md], { type: 'text/markdown;charset=utf-8;' });
    const link = document.createElement('a');
    link.href  = URL.createObjectURL(blob);
    link.setAttribute('download', `${session.storybookName}_SecondBrain.md`);
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
};
"""

result = keep + [new_code]
out = open(r'c:\Users\user\Downloads\connect_dmdg\global_service\script.js',
           'w', encoding='utf-8', newline='\n')
out.writelines(result)
out.close()

# 검증
verify = open(r'c:\Users\user\Downloads\connect_dmdg\global_service\script.js',
              'r', encoding='utf-8')
content = verify.read()
verify.close()
ok = 'autoClusterWords' in content and 'SecondBrain' in content and 'generateMarkdownContent' in content
print(f"SUCCESS={ok} | 총 {content.count(chr(10))}줄 | autoCluster:{content.count('autoClusterWords')}회 | 중복함수:{content.count('function generateMarkdownContent')}회")
