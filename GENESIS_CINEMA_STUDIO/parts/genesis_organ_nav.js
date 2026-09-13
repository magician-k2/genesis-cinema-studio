/**
 * 🧬 GENESIS Organ Navigator | 共通生体器官ナビゲーション・コンポーネント
 * 各器官（Cinema, Music, Character, Storyboard）の上部に自動マウントされ、
 * 一元的な器官切り替えと生体パルス（Q-NO / MaleCNS）ステータスを表示する。
 */
(function() {
  const ORGANS = [
    { id: 'mobile', name: 'Antigravity Mobile', label: '大脳/制御', icon: 'fa-brain', url: '/mobile_antigravity.html', color: '#38bdf8' },
    { id: 'cinema', name: 'Cinema Studio', label: '視覚野', icon: 'fa-film', url: '/cinema_lite.html', color: '#06b6d4' },
    { id: 'music', name: 'Music & Sampling', label: '聴覚野', icon: 'fa-music', url: '/music_studio.html', color: '#8b5cf6' },
    { id: 'character', name: 'Character Studio', label: '身体野', icon: 'fa-user-astronaut', url: '/character_studio.html', color: '#ec4899' },
    { id: 'storyboard', name: 'Storyboard Studio', label: '記憶野', icon: 'fa-book-open', url: '/storyboard_studio.html', color: '#f59e0b' }
  ];

  function detectActiveOrgan() {
    const path = window.location.pathname.toLowerCase();
    if (path.includes('mobile_antigravity')) return 'mobile';
    const path = window.location.pathname.toLowerCase();
    if (path.includes('music')) return 'music';
    if (path.includes('character')) return 'character';
    if (path.includes('storyboard')) return 'storyboard';
    return 'cinema';
  }

  function initOrganNav() {
    let container = document.getElementById('genesis-organ-nav');
    if (!container) {
      container = document.createElement('div');
      container.id = 'genesis-organ-nav';
      document.body.prepend(container);
    }

    const activeId = detectActiveOrgan();

    const linksHtml = ORGANS.map(organ => {
      const isActive = organ.id === activeId;
      return `
        <a href="${organ.url}" class="gon-link ${isActive ? 'active' : ''}" style="--active-border: ${organ.color};">
          <i class="fa-solid ${organ.icon}" style="color: ${organ.color};"></i>
          <span>${organ.name}</span>
          <span class="gon-sub">[${organ.label}]</span>
        </a>
      `;
    }).join('');

    container.innerHTML = `
      <style>
        #genesis-organ-nav-bar {
          background: rgba(7, 9, 14, 0.94);
          backdrop-filter: blur(20px);
          -webkit-backdrop-filter: blur(20px);
          border-bottom: 1px solid rgba(255, 255, 255, 0.08);
          padding: 8px 20px;
          display: flex;
          align-items: center;
          justify-content: space-between;
          position: sticky;
          top: 0;
          z-index: 99999;
          font-family: 'Outfit', 'Noto Sans JP', sans-serif;
          font-size: 0.85rem;
          color: #f8fafc;
        }
        .gon-brand {
          display: flex;
          align-items: center;
          gap: 10px;
          text-decoration: none;
          color: inherit;
        }
        .gon-logo {
          width: 26px;
          height: 26px;
          border-radius: 6px;
          background: linear-gradient(135deg, #06b6d4, #8b5cf6);
          display: flex;
          align-items: center;
          justify-content: center;
          color: white;
          font-weight: 900;
          font-size: 0.8rem;
          box-shadow: 0 0 12px rgba(139, 92, 246, 0.5);
        }
        .gon-links {
          display: flex;
          align-items: center;
          gap: 6px;
        }
        .gon-link {
          display: inline-flex;
          align-items: center;
          gap: 6px;
          padding: 6px 12px;
          border-radius: 8px;
          text-decoration: none;
          color: #94a3b8;
          font-weight: 500;
          border: 1px solid transparent;
          transition: all 0.2s ease;
        }
        .gon-link:hover {
          color: #f8fafc;
          background: rgba(255, 255, 255, 0.05);
          border-color: rgba(255, 255, 255, 0.1);
        }
        .gon-link.active {
          color: #ffffff;
          background: rgba(255, 255, 255, 0.08);
          border-color: var(--active-border, #8b5cf6);
          box-shadow: 0 0 10px rgba(139, 92, 246, 0.25);
        }
        .gon-sub {
          font-size: 0.7rem;
          opacity: 0.7;
          font-family: 'JetBrains Mono', monospace;
        }
        .gon-telemetry {
          display: flex;
          align-items: center;
          gap: 12px;
          font-family: 'JetBrains Mono', monospace;
          font-size: 0.72rem;
          color: #94a3b8;
        }
        .gon-dot {
          width: 7px;
          height: 7px;
          border-radius: 50%;
          background: #10b981;
          display: inline-block;
          box-shadow: 0 0 8px #10b981;
          animation: gonPulse 2s infinite ease-in-out;
        }
        @keyframes gonPulse {
          0%, 100% { opacity: 1; transform: scale(1); }
          50% { opacity: 0.4; transform: scale(0.85); }
        }
      </style>
      <div id="genesis-organ-nav-bar">
        <a href="/cinema_lite.html" class="gon-brand">
          <div class="gon-logo">G</div>
          <div>
            <div style="font-weight: 700; letter-spacing: 0.5px;">GENESIS <span style="font-size: 0.7rem; opacity: 0.6;">SYNTHETIC BRAIN</span></div>
          </div>
        </a>

        <div class="gon-links">
          ${linksHtml}
        </div>

        <div class="gon-telemetry">
          <span style="display: flex; align-items: center; gap: 6px;">
            <span class="gon-dot"></span>
            <span>MaleCNS 166k SNN</span>
          </span>
          <span style="color: #64748b;">|</span>
          <span style="color: #a855f7;"><i class="fa-solid fa-atom"></i> Q-NO</span>
        </div>
      </div>
    `;
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initOrganNav);
  } else {
    initOrganNav();
  }
})();
