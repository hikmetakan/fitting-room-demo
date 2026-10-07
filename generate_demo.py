import base64

def get_b64(path, mime='image/jpeg'):
    with open(path, 'rb') as f:
        return f'data:{mime};base64,' + base64.b64encode(f.read()).decode('utf-8')

b_man = get_b64('/Users/hikmetakan/.gemini/antigravity/scratch/fitting-room-demo/public/images/base-mannequin.jpg', 'image/jpeg')
# Transparent PNG cutouts without background!
b_brn = get_b64('/Users/hikmetakan/.gemini/antigravity/scratch/fitting-room-demo/public/images/brown-vest.png', 'image/png')
b_blk = get_b64('/Users/hikmetakan/.gemini/antigravity/scratch/fitting-room-demo/public/images/black-vest.png', 'image/png')
m_brn = get_b64('/Users/hikmetakan/.gemini/antigravity/scratch/fitting-room-demo/public/images/model-brown-vest.jpg', 'image/jpeg')
m_blk = get_b64('/Users/hikmetakan/.gemini/antigravity/scratch/fitting-room-demo/public/images/model-black-vest.jpg', 'image/jpeg')

html_content = f'''<!DOCTYPE html>
<html lang="tr" class="dark">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Sanal Kabin Canlı Demo - Şeffaf PNG Dekupe Animasyonu</title>
  <script src="https://www.gstatic.com/antigravity/web/dev/tailwindcss.min.js"></script>
  <style>
    .model-transition {{
      transition: opacity 450ms cubic-bezier(0.22, 1, 0.36, 1), transform 450ms cubic-bezier(0.22, 1, 0.36, 1), filter 450ms cubic-bezier(0.22, 1, 0.36, 1);
    }}
    .flying-card {{
      position: fixed;
      z-index: 9999;
      pointer-events: none;
      background: transparent !important;
      border: none !important;
      box-shadow: none !important;
      filter: drop-shadow(0 25px 35px rgba(224, 133, 68, 0.6)) drop-shadow(0 10px 15px rgba(0, 0, 0, 0.7));
    }}
    ::-webkit-scrollbar {{
      height: 6px;
      width: 6px;
    }}
    ::-webkit-scrollbar-track {{
      background: #0f1117;
    }}
    ::-webkit-scrollbar-thumb {{
      background: #27272a;
      border-radius: 9999px;
    }}
  </style>
</head>
<body class="bg-[#0E0F12] text-zinc-100 antialiased min-h-screen p-4 sm:p-6 lg:p-8 selection:bg-amber-500/30 selection:text-amber-200">

  <!-- Üst Bilgi Çubuğu -->
  <div class="max-w-7xl mx-auto mb-6">
    <div class="rounded-2xl border border-zinc-800 bg-[#16171D]/80 backdrop-blur-xl p-4 shadow-xl flex flex-wrap items-center justify-between gap-4">
      <div class="flex items-center gap-3">
        <div class="h-10 w-10 rounded-xl bg-gradient-to-tr from-amber-500 to-amber-300 flex items-center justify-center text-black font-black text-base shadow-md shadow-amber-500/20">
          V
        </div>
        <div>
          <div class="flex items-center gap-2">
            <h1 class="text-sm font-bold tracking-wider uppercase text-zinc-100">Atelier Studio</h1>
            <span class="text-xs px-2 py-0.5 rounded-full bg-emerald-500/10 text-emerald-400 border border-emerald-500/20 font-mono">ŞEFFAF PNG DEKUPE AKTİF</span>
          </div>
          <p class="text-xs text-zinc-400">Arka plansız saf kıyafet süzülüşü &amp; Canlı model eşlemesi</p>
        </div>
      </div>

      <div class="flex flex-wrap items-center gap-3 text-xs">
        <div class="px-3 py-1.5 rounded-xl bg-zinc-950/80 border border-zinc-800 flex items-center gap-2">
          <span class="h-2 w-2 rounded-full bg-emerald-400 animate-pulse"></span>
          <span class="text-zinc-400">Model Eşleme Hızı:</span>
          <span class="font-bold text-emerald-400 font-mono" id="latency-metric">&lt; 14 ms</span>
        </div>
        <button id="btn-reset-mannequin" class="px-3 py-1.5 rounded-xl bg-zinc-800 hover:bg-zinc-700 text-zinc-300 hover:text-white transition-all text-xs font-medium border border-zinc-700">
          Baz Mankene Sıfırla
        </button>
      </div>
    </div>
  </div>

  <!-- Ana Düzen: Sol Panel (Manken) + Sağ Panel (Kartlar) -->
  <div class="max-w-7xl mx-auto grid grid-cols-1 lg:grid-cols-12 gap-8 items-start">

    <!-- ==============================================================
         SOL PANEL: SANAL KABİN (ÖNİZLEME & GÖNDERİLEN MODEL)
         ============================================================== -->
    <aside class="lg:col-span-5 lg:sticky lg:top-6 space-y-4">
      <div id="fitting-room-container" class="rounded-3xl border border-zinc-800/90 bg-[#16171D]/90 backdrop-blur-2xl p-5 shadow-2xl relative overflow-hidden">
        
        <!-- Başlık Alanı -->
        <div class="flex items-center justify-between pb-3.5 border-b border-zinc-800/70">
          <div class="flex items-center gap-2.5">
            <div class="h-7 w-7 rounded-lg bg-amber-500/10 border border-amber-500/20 flex items-center justify-center">
              <svg class="w-4 h-4 text-amber-400" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                <path d="M12 3a3 3 0 0 0-3 3c0 1.25.75 2 1.5 2.5L3 17h18l-7.5-8.5C14.25 8 15 7.25 15 6a3 3 0 0 0-3-3z" />
              </svg>
            </div>
            <div>
              <h2 class="text-xs font-bold tracking-wider text-zinc-100 uppercase">
                Sanal Kabin Önizleme
              </h2>
              <p id="model-status-text" class="text-[11px] text-zinc-500 font-mono">
                Kahverengi Yelek giyili
              </p>
            </div>
          </div>
          <button id="btn-clear" class="text-xs text-zinc-400 hover:text-amber-300 transition-colors px-2 py-1 rounded bg-zinc-800/60 hover:bg-zinc-800">
            Kıyafeti Çıkar
          </button>
        </div>

        <!-- Manken Önizleme Çerçevesi -->
        <div id="mannequin-frame" class="relative mt-4 aspect-[9/16] max-h-[580px] w-full rounded-2xl overflow-hidden bg-[#0A0B0E] border border-zinc-800/80 shadow-inner flex items-center justify-center">
          
          <img
            id="mannequin-img"
            src="{m_brn}"
            alt="Model Önizleme"
            class="model-transition w-full h-full object-cover object-top"
          />

          <!-- Gradient Overlay -->
          <div class="absolute inset-0 bg-gradient-to-t from-black/85 via-transparent to-transparent pointer-events-none"></div>

          <!-- Model Üzerindeki Aktif Parça Rozeti -->
          <div id="active-item-badge" class="absolute bottom-3.5 left-3.5 right-3.5 p-3.5 rounded-2xl bg-[#16171E]/95 border border-zinc-700/60 backdrop-blur-md flex items-center justify-between transition-all duration-300">
            <div>
              <span class="text-[10px] tracking-wider uppercase text-amber-400 font-mono flex items-center gap-1.5">
                <span class="h-1.5 w-1.5 rounded-full bg-amber-400 animate-ping"></span>
                Model Üzerinde Giyili
              </span>
              <p id="active-item-name" class="text-xs font-bold text-zinc-100 line-clamp-1 mt-0.5">
                Kapitoneli Şişme Yelek (Kahverengi)
              </p>
              <p id="active-item-price" class="text-xs text-zinc-300 font-bold font-mono">
                3.450 ₺
              </p>
            </div>
            <button id="btn-cart-active" class="px-3.5 py-2 rounded-xl bg-gradient-to-r from-amber-500 to-[#E08544] hover:brightness-110 text-black text-xs font-bold transition-transform active:scale-95 shadow-md shadow-amber-500/25">
              Sepete Ekle
            </button>
          </div>

          <!-- Baz Manken Boş Durum Bilgisi -->
          <div id="empty-state-badge" class="hidden absolute bottom-4 left-4 right-4 text-center">
            <span class="text-xs text-zinc-400 bg-black/80 px-4 py-1.5 rounded-full border border-zinc-800">
              Askıdaki bir yeleğe tıklayarak mankene giydirin
            </span>
          </div>
        </div>

        <!-- Kabin Askılığı (Fitting Room Rack) -->
        <div class="mt-4 pt-3.5 border-t border-zinc-800/70">
          <div class="flex items-center justify-between mb-2.5">
            <div class="flex items-center gap-1.5">
              <span class="text-xs font-semibold text-zinc-300">Askıdaki Parçalar</span>
              <span id="rack-count" class="text-[11px] px-1.5 py-0.5 rounded bg-zinc-800 text-amber-400 font-mono">1</span>
            </div>
            <span class="text-[11px] text-zinc-500">Mankene giydirmek için tıkla</span>
          </div>

          <div id="fitting-rack" class="flex gap-2.5 overflow-x-auto pb-1 items-center">
            <!-- JS ile doldurulacak -->
          </div>
        </div>
      </div>
    </aside>

    <!-- ==============================================================
         SAĞ PANEL: GÖNDERİLEN KART TASARIMINDAKİ ÜRÜN LİSTESİ
         ============================================================== -->
    <section class="lg:col-span-7 space-y-5">
      <div class="flex items-center justify-between pb-2 border-b border-zinc-800/60">
        <div>
          <h2 class="text-xl font-bold tracking-tight text-zinc-100">Özel Koleksiyon</h2>
          <p class="text-xs text-zinc-400">
            Model üzerinde görmek için sol üstteki <span class="text-amber-400 font-semibold">askı simgesine</span> tıklayın.
          </p>
        </div>
        <span class="text-xs font-mono text-zinc-500">2 Renk Seçeneği</span>
      </div>

      <!-- Kart Grid -->
      <div class="grid grid-cols-1 sm:grid-cols-2 gap-5" id="product-grid">
        <!-- JS ile çizilecek -->
      </div>
    </section>
  </div>

  <!-- Toast Bildirimi -->
  <div id="toast" class="fixed top-6 right-6 z-50 bg-[#1A1B20] border border-amber-500/50 text-amber-300 text-xs px-4 py-2.5 rounded-xl shadow-2xl shadow-black/80 flex items-center gap-2 transform translate-y-[-100px] opacity-0 transition-all duration-300 pointer-events-none">
    <span class="h-2 w-2 rounded-full bg-amber-400 animate-ping"></span>
    <span id="toast-text">İşlem yapıldı</span>
  </div>

  <!-- JAVASCRIPT & ANİMASYON MANTIĞI -->
  <script>
    const IMAGES = {{
      baseMannequin: "{b_man}",
      brownVest: "{b_brn}",
      blackVest: "{b_blk}",
      modelBrown: "{m_brn}",
      modelBlack: "{m_blk}",
    }};

    const PRODUCTS = [
      {{
        id: 'vest-brown',
        name: 'Kapitoneli Şişme Yelek',
        color: 'Kahverengi',
        price: 3450,
        rating: 4.9,
        card_image: IMAGES.brownVest,
        model_image_url: IMAGES.modelBrown,
      }},
      {{
        id: 'vest-black',
        name: 'Mat Nappa Kapitoneli Yelek',
        color: 'Siyah',
        price: 3650,
        rating: 4.8,
        card_image: IMAGES.blackVest,
        model_image_url: IMAGES.modelBlack,
      }},
    ];

    // State
    let activeItem = PRODUCTS[0];
    let fittingRoomItems = [PRODUCTS[0]];
    let favorites = {{}};

    // DOM
    const mannequinImg = document.getElementById('mannequin-img');
    const mannequinFrame = document.getElementById('mannequin-frame');
    const activeItemBadge = document.getElementById('active-item-badge');
    const emptyStateBadge = document.getElementById('empty-state-badge');
    const activeItemName = document.getElementById('active-item-name');
    const activeItemPrice = document.getElementById('active-item-price');
    const modelStatusText = document.getElementById('model-status-text');
    const fittingRack = document.getElementById('fitting-rack');
    const rackCount = document.getElementById('rack-count');
    const productGrid = document.getElementById('product-grid');
    const toast = document.getElementById('toast');
    const toastText = document.getElementById('toast-text');
    const latencyMetric = document.getElementById('latency-metric');

    let toastTimer = null;
    function showToast(msg) {{
      toastText.textContent = msg;
      toast.classList.remove('translate-y-[-100px]', 'opacity-0');
      toast.classList.add('translate-y-0', 'opacity-100');
      clearTimeout(toastTimer);
      toastTimer = setTimeout(() => {{
        toast.classList.add('translate-y-[-100px]', 'opacity-0');
        toast.classList.remove('translate-y-0', 'opacity-100');
      }}, 2400);
    }}

    // Model Geçişi (Cross-dissolve & Blur)
    function changeModelVisual(targetUrl) {{
      const start = performance.now();
      mannequinImg.style.opacity = '0';
      mannequinImg.style.transform = 'scale(1.02)';
      mannequinImg.style.filter = 'blur(8px)';

      setTimeout(() => {{
        mannequinImg.src = targetUrl;
        mannequinImg.onload = () => {{
          mannequinImg.style.opacity = '1';
          mannequinImg.style.transform = 'scale(1)';
          mannequinImg.style.filter = 'blur(0px)';
          const diff = Math.round(performance.now() - start);
          latencyMetric.textContent = `${{diff}} ms (Data-Mapped)`;
        }};
      }}, 160);
    }}

    // Kullanıcının İstediği Özel Animasyon:
    // Arka planı OLMAYAN, saf şeffaf PNG ürün yerinden fırlar ve büyükten küçülerek mankene uçar!
    function triggerPopAndShrinkFlight(sourceImg, product) {{
      const startRect = sourceImg.getBoundingClientRect();
      const targetRect = mannequinFrame.getBoundingClientRect();

      // Uçan şeffaf klon oluştur (Arka planı yok!)
      const clone = document.createElement('img');
      clone.src = product.card_image; // Saf şeffaf PNG
      clone.className = 'flying-card';
      clone.style.left = `${{startRect.left}}px`;
      clone.style.top = `${{startRect.top}}px`;
      clone.style.width = `${{startRect.width}}px`;
      clone.style.height = `${{startRect.height}}px`;
      clone.style.objectFit = 'contain';

      document.body.appendChild(clone);

      // Aşama 1: Yerinden fırlama ve büyüme (Pop-out & Expand - Arka plansız saf kıyafet)
      requestAnimationFrame(() => {{
        clone.style.transform = 'scale(1.22) rotate(-6deg)';
        clone.style.transition = 'all 280ms cubic-bezier(0.34, 1.56, 0.64, 1)';
      }});

      // Aşama 2: Büyükten küçülerek mankene süzülme (Glide & Shrink to Mannequin Chest)
      setTimeout(() => {{
        const targetX = targetRect.left + (targetRect.width / 2) - 65;
        const targetY = targetRect.top + (targetRect.height * 0.35) - 65;

        clone.style.transition = 'all 560ms cubic-bezier(0.22, 1, 0.36, 1)';
        clone.style.left = `${{targetX}}px`;
        clone.style.top = `${{targetY}}px`;
        clone.style.width = '130px';
        clone.style.height = '130px';
        clone.style.transform = 'scale(0.40) rotate(2deg)';
        clone.style.opacity = '0';
      }}, 260);

      // Aşama 3: Mankenin üzerine giydirilmesi
      setTimeout(() => {{
        clone.remove();
        setActiveProduct(product, false);
      }}, 790);
    }}

    function setActiveProduct(product, runAnimation = false, sourceImg = null) {{
      if (runAnimation && sourceImg && product) {{
        triggerPopAndShrinkFlight(sourceImg, product);
        return;
      }}

      activeItem = product;
      if (product) {{
        if (!fittingRoomItems.some(p => p.id === product.id)) {{
          fittingRoomItems.push(product);
        }}
        changeModelVisual(product.model_image_url);
        activeItemName.textContent = `${{product.name}} (${{product.color}})`;
        activeItemPrice.textContent = `${{product.price.toLocaleString('tr-TR')}} ₺`;
        modelStatusText.textContent = `${{product.color}} Yelek giyili`;
        activeItemBadge.classList.remove('hidden');
        emptyStateBadge.classList.add('hidden');
        showToast(`\"${{product.name}}\" model üzerinde gösteriliyor.`);
      }} else {{
        changeModelVisual(IMAGES.baseMannequin);
        activeItemBadge.classList.add('hidden');
        emptyStateBadge.classList.remove('hidden');
        modelStatusText.textContent = 'Baz manken (Kıyafet yok)';
        showToast('Kıyafet çıkarıldı, baz mankene dönüldü.');
      }}

      renderRack();
      renderCatalog();
    }}

    function removeProductFromRack(productId, e) {{
      e.stopPropagation();
      fittingRoomItems = fittingRoomItems.filter(p => p.id !== productId);
      if (activeItem && activeItem.id === productId) {{
        const next = fittingRoomItems.length > 0 ? fittingRoomItems[fittingRoomItems.length - 1] : null;
        setActiveProduct(next, false);
      }} else {{
        renderRack();
        renderCatalog();
      }}
    }}

    // Sol Paneldeki Askılığı Çiz
    function renderRack() {{
      fittingRack.innerHTML = '';
      rackCount.textContent = fittingRoomItems.length;

      if (fittingRoomItems.length === 0) {{
        fittingRack.innerHTML = `
          <div class="w-full py-3 text-center rounded-xl border border-dashed border-zinc-800 text-xs text-zinc-500">
            Askılık boş. Kartlardaki askı simgesine tıklayın.
          </div>
        `;
        return;
      }}

      fittingRoomItems.forEach(item => {{
        const isActive = activeItem && activeItem.id === item.id;
        const slot = document.createElement('div');
        slot.className = `relative group flex-shrink-0 w-20 cursor-pointer rounded-xl border p-1.5 transition-all ${{
          isActive
            ? 'border-amber-400 bg-amber-400/10 shadow-lg shadow-amber-500/15'
            : 'border-zinc-800 bg-zinc-900/60 hover:border-zinc-700'
        }}`;

        slot.innerHTML = `
          ${{isActive ? '<div class=\"absolute inset-0 rounded-xl border-2 border-amber-400 pointer-events-none\"></div>' : ''}}
          <div class=\"relative aspect-square w-full rounded-lg overflow-hidden bg-zinc-950 mb-1 flex items-center justify-center\">
            <img src=\"${{item.card_image}}\" alt=\"${{item.name}}\" class=\"w-full h-full object-contain p-1 filter drop-shadow\" />
            <button class=\"remove-btn absolute top-0.5 right-0.5 h-4 w-4 rounded-full bg-black/85 hover:bg-red-500 text-zinc-300 hover:text-white flex items-center justify-center text-[10px] opacity-0 group-hover:opacity-100 transition-opacity\">
              ✕
            </button>
          </div>
          <p class=\"text-[10px] font-semibold text-zinc-200 truncate\">${{item.color}}</p>
          <p class=\"text-[9px] text-zinc-400 font-mono\">${{item.price.toLocaleString('tr-TR')}} ₺</p>
        `;

        slot.addEventListener('click', () => setActiveProduct(item, false));
        slot.querySelector('.remove-btn').addEventListener('click', (e) => removeProductFromRack(item.id, e));
        fittingRack.appendChild(slot);
      }});
    }}

    // Kullanıcının Gönderdiği Tasarımdaki Ürün Kartları
    function renderCatalog() {{
      productGrid.innerHTML = '';

      PRODUCTS.forEach(product => {{
        const isCurrentActive = activeItem && activeItem.id === product.id;
        const isFav = !!favorites[product.id];

        const card = document.createElement('div');
        card.className = `relative rounded-[32px] bg-[#1B1C22] border border-zinc-800/80 p-5 shadow-2xl overflow-hidden flex flex-col justify-between group transition-all duration-300 hover:border-zinc-700 ${{
          isCurrentActive ? 'ring-1 ring-amber-500/40 shadow-amber-500/5' : ''
        }}`;

        card.innerHTML = `
          <!-- Kart Üstü: Sol Kalp ve Askı, Sağ Puan -->
          <div class="flex items-start justify-between z-10">
            <div class="flex flex-col gap-2.5">
              
              <!-- Kalp Butonu -->
              <button class="fav-btn h-10 w-10 rounded-full flex items-center justify-center transition-all ${{
                isFav
                  ? 'bg-rose-500/20 text-rose-400 border border-rose-500/40'
                  : 'bg-[#292A32]/80 hover:bg-[#34353F] text-zinc-300'
              }}">
                <svg class="w-4 h-4 ${{isFav ? 'fill-current' : 'fill-none'}}" viewBox="0 0 24 24" stroke="currentColor" strokeWidth="2">
                  <path d="M20.84 4.61a5.5 5.5 0 0 0-7.78 0L12 5.67l-1.06-1.06a5.5 5.5 0 0 0-7.78 7.78l1.06 1.06L12 21.23l7.78-7.78 1.06-1.06a5.5 5.5 0 0 0 0-7.78z" />
                </svg>
              </button>

              <!-- Askı Butonu (Fitting Room Trigger) -->
              <button class="hanger-btn h-10 w-10 rounded-full flex items-center justify-center transition-all duration-300 active:scale-90 ${{
                isCurrentActive
                  ? 'bg-amber-500 text-black shadow-lg shadow-amber-500/30 ring-2 ring-amber-400 scale-105'
                  : 'bg-[#292A32]/80 hover:bg-amber-500 hover:text-black text-zinc-300'
              }}" title="Askıya Al / Modelde Dene">
                <svg class="w-4 h-4" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.2">
                  <path d="M12 3a3 3 0 0 0-3 3c0 1.25.75 2 1.5 2.5L3 17h18l-7.5-8.5C14.25 8 15 7.25 15 6a3 3 0 0 0-3-3z" />
                </svg>
              </button>
            </div>

            <!-- Sağ Üst: Yıldızlı Puan Rozeti (★ 4.9) -->
            <div class="flex items-center gap-1.5 px-3 py-1.5 rounded-full bg-[#292A32]/80 border border-zinc-700/40 text-xs font-semibold text-zinc-200">
              <span class="text-[#FBBF24]">★</span>
              <span>${{product.rating.toFixed(1)}}</span>
            </div>
          </div>

          <!-- Kart Ortası: Şeffaf Dekupe Ürün Görseli (Arka planı yok!) -->
          <div class="relative my-4 aspect-[4/5] w-full flex items-center justify-center">
            <img
              id="card-img-${{product.id}}"
              src="${{product.card_image}}"
              alt="${{product.name}}"
              class="max-h-full max-w-full object-contain filter drop-shadow-[0_20px_30px_rgba(0,0,0,0.7)] transition-transform duration-500 group-hover:scale-105"
            />
          </div>

          <!-- Kart Altı: Sol İsim & Fiyat, Sağ Terracotta Sepet Butonu -->
          <div class="flex items-end justify-between mt-2 pt-2">
            <div class="space-y-1">
              <h3 class="text-sm font-medium text-zinc-300 line-clamp-1">
                ${{product.name}}
              </h3>
              <p class="text-2xl font-bold text-white tracking-tight">
                ${{product.price.toLocaleString('tr-TR')}} ₺
              </p>
            </div>

            <!-- Sağ Alttaki Özel Terracotta Çeyrek-Daire Sepet Butonu -->
            <button
              class="cart-btn absolute bottom-0 right-0 w-24 h-24 bg-[#E08544] hover:bg-[#ea8c49] rounded-tl-[48px] flex items-center justify-center text-white transition-all duration-300 pl-4 pt-4 shadow-xl active:scale-95"
              title="Sepete Ekle"
            >
              <div class="relative flex items-center justify-center">
                <svg class="w-6 h-6" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.2" strokeLinecap="round" strokeLinejoin="round">
                  <path d="M6 2 3 6v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2V6l-3-4Z" />
                  <path d="M3 6h18" />
                  <path d="M16 10a4 4 0 0 1-8 0" />
                </svg>
                <span class="absolute -top-1 -right-2 text-xs font-black">+</span>
              </div>
            </button>
          </div>
        `;

        // Buton Dinleyicileri
        card.querySelector('.fav-btn').addEventListener('click', () => {{
          favorites[product.id] = !favorites[product.id];
          showToast(favorites[product.id] ? 'Favorilere eklendi' : 'Favorilerden çıkarıldı');
          renderCatalog();
        }});

        card.querySelector('.hanger-btn').addEventListener('click', () => {{
          const imgEl = card.querySelector(`#card-img-${{product.id}}`);
          setActiveProduct(product, true, imgEl);
        }});

        card.querySelector('.cart-btn').addEventListener('click', () => {{
          showToast(`\"${{product.name}}\" sepete eklendi!`);
        }});

        productGrid.appendChild(card);
      }});
    }}

    // Genel Butonlar
    document.getElementById('btn-clear').addEventListener('click', () => {{
      setActiveProduct(null, false);
    }});

    document.getElementById('btn-reset-mannequin').addEventListener('click', () => {{
      setActiveProduct(null, false);
    }});

    document.getElementById('btn-cart-active').addEventListener('click', () => {{
      if (activeItem) {{
        showToast(`\"${{activeItem.name}}\" sepete eklendi!`);
      }}
    }});

    // Başlangıç Çizimi
    renderCatalog();
    renderRack();
  </script>
</body>
</html>
'''

with open('/Users/hikmetakan/.gemini/antigravity/brain/208aa92a-c82b-42b8-ba34-de53755bfac3/fitting_room_demo.html', 'w', encoding='utf-8') as f:
    f.write(html_content)

print('SUCCESS: fitting_room_demo.html re-generated with transparent PNG vests!')
