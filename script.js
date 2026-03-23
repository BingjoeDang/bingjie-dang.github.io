// 粒子特效配置
/* 粒子特效配置保持不变 */
particlesJS('particles-js', {
    "particles": {
        "number": { "value": 80 },
        "number": { "value": 60 },
        "color": { "value": "#d2b4a0" },
        "shape": { "type": "circle" },
        "opacity": { "value": 0.5 },
        "size": { "value": 3 },
        "line_linked": { "enable": true, "distance": 150, "color": "#d2b4a0", "opacity": 0.4, "width": 1 },
        "move": { "enable": true, "speed": 2 }
        "opacity": { "value": 0.3 },
        "size": { "value": 2 },
        "line_linked": { "enable": true, "distance": 150, "color": "#d2b4a0", "opacity": 0.2, "width": 1 },
        "move": { "enable": true, "speed": 1.5 }
    },
    "interactivity": {
        "events": { "onhover": { "enable": true, "mode": "repulse" } }
    }
});

async function updatePublicationCitations() {
            const publicationItems = [...document.querySelectorAll('.pub-list li')]
                .filter(li => li.querySelector('em'));

            publicationItems.forEach(li => {
                if (!li.querySelector('.citation-badge')) {
                    li.appendChild(document.createElement('br'));
                    li.appendChild(createCitationBadge());
                }
            });

            try {
                // 直接读取 GitHub Actions 每天为你生成的 json 文件
                const response = await fetch(`citations.json?v=${Date.now()}`);
                if (!response.ok) throw new Error('citations.json not found');
                const data = await response.json();
                
                const citationMap = new Map((Array.isArray(data) ? data : []).map(item => [
                    buildPublicationKey(item.title || ''), 
                    Number(item.citations || 0)
                ]));

                publicationItems.forEach(li => {
                    const badge = li.querySelector('.citation-badge');
                    const key = li.dataset.citeKey || buildPublicationKey(li.innerText);
                    const count = citationMap.has(key) ? citationMap.get(key) : 0;
                    
                    badge.classList.remove('error', 'loading');
                    badge.innerHTML = `<span class="en">Citations: ${count}</span><span class="zh">引用：${count}</span>`;
                });
            } catch (err) {
                console.error('Failed to load citations.json:', err);
                publicationItems.forEach(li => {
                    const badge = li.querySelector('.citation-badge');
                    if (badge) {
                        badge.classList.remove('loading');
                        badge.innerHTML = '<span class="en">Citations: 0</span><span class="zh">引用：0</span>';
                    }
                });
            }
        }
