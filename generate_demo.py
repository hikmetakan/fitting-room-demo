import base64

def get_b64(path, mime='image/jpeg'):
    with open(path, 'rb') as f:
        return f'data:{mime};base64,' + base64.b64encode(f.read()).decode('utf-8')

b_man = get_b64('/Users/hikmetakan/.gemini/antigravity/scratch/fitting-room-demo/public/images/base-mannequin.jpg', 'image/jpeg')
b_brn = get_b64('/Users/hikmetakan/.gemini/antigravity/scratch/fitting-room-demo/public/images/brown-vest.png', 'image/png')
b_blk = get_b64('/Users/hikmetakan/.gemini/antigravity/scratch/fitting-room-demo/public/images/black-vest.png', 'image/png')
b_grn = get_b64('/Users/hikmetakan/.gemini/antigravity/scratch/fitting-room-demo/public/images/green-jacket.png', 'image/png')
m_brn = get_b64('/Users/hikmetakan/.gemini/antigravity/scratch/fitting-room-demo/public/images/model-brown-vest.jpg', 'image/jpeg')
m_blk = get_b64('/Users/hikmetakan/.gemini/antigravity/scratch/fitting-room-demo/public/images/model-black-vest.jpg', 'image/jpeg')
m_grn = get_b64('/Users/hikmetakan/.gemini/antigravity/scratch/fitting-room-demo/public/images/model-green-vest.jpg', 'image/jpeg')

html_content = f'''<!DOCTYPE html>
<html lang="tr" class="dark">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
  <title>Sanal Kabin - Mobil Uyumlu Minimal Tasarım</title>
  <script src="https://www.gstatic.com/antigravity/web/dev/tailwindcss.min.js"></script>
  <style>
    .model-transition {{
      transition: opacity 400ms cubic-bezier(0.22, 1, 0.36, 1), transform 400ms cubic-bezier(0.22, 1, 0.36, 1), filter 400ms cubic-bezier(0.22, 1, 0.36, 1);
    }}
    .flying-card {{
      position: fixed;
      z-index: 9999;
      pointer-events: none;
      background: transparent !important;
      border: none !important;
      box-shadow: none !important;
      filter: drop-shadow(0 20px 30px rgba(224, 133, 68, 0.6)) drop-shadow(0 10px 15px rgba(0, 0, 0, 0.7));
    }}
    ::-webkit-scrollbar {{
      height: 4px;
      width: 4px;
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
<body class="bg-[#0D0C12] text-zinc-100 antialiased min-h-screen p-3 sm:p-5 lg:p-8 selection:bg-amber-500/30 selection:text-amber-200">

  <!-- Üst Bar: Minimal ve Mobil Uyumlu -->
  <header class="max-w-7xl mx-auto mb-4 sm:mb-6">
    <div class="rounded-2xl border border-zinc-800/80 bg-[#15141B]/90 backdrop-blur-xl px-3.5 py-2.5 sm:px-4 sm:py-3 shadow-lg flex items-center justify-between gap-3">
      <div class="flex items-center gap-2.5">
        <div class="h-8 w-8 rounded-xl bg-gradient-to-tr from-[#E08544] to-amber-300 flex items-center justify-center text-black font-black text-sm shadow-md shadow-[#E08544]/20">
          V
        </div>
        <div>
          <div class="flex items-center gap-1.5">
            <h1 class="text-xs sm:text-sm font-bold tracking-wider uppercase text-zinc-100">Atelier Sanal Kabin</h1>
            <span class="text-[10px] px-1.5 py-0.2 rounded-full bg-emerald-500/10 text-emerald-400 border border-emerald-500/20 font-mono">MOBİL UYUMLU</span>
          </div>
          <p class="text-[11px] text-zinc-400 hidden sm:block">Şeffaf PNG Uçuşu &amp; Canlı Model Eşlemesi</p>
        </div>
      </div>

      <div class="flex items-center gap-2">
        <button id="btn-reset-mannequin" class="px-2.5 py-1.5 rounded-xl bg-zinc-800/90 hover:bg-zinc-700 text-zinc-300 hover:text-white transition-all text-[11px] sm:text-xs font-medium border border-zinc-700/60 flex items-center gap-1">
          <svg class="w-3.5 h-3.5 text-zinc-400" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2"><path d="M3 12a9 9 0 0 1 9-9 9.75 9.75 0 0 1 6.74 2.74L21 8"/><path d="M21 3v5h-5"/></svg>
          <span class="hidden sm:inline">Mankeni Sıfırla</span>
          <span class="sm:hidden">Sıfırla</span>
        </button>
      </div>
    </div>
  </header>

  <!-- Ana Izgara: Mobilde Kompakt Model Üstte, Minimal Kartlar 2 Kolon Halinde Altta -->
  <main class="max-w-7xl mx-auto grid grid-cols-1 lg:grid-cols-12 gap-4 sm:gap-6 items-start">

    <!-- ==============================================================
         SOL PANEL: SANAL KABİN (MOBİLDE KOMPAKT & KULLANIŞLI)
         ============================================================== -->
    <aside class="lg:col-span-5 lg:sticky lg:top-6 space-y-3">
      <div id="fitting-room-container" class="rounded-2xl sm:rounded-3xl border border-zinc-800/90 bg-[#15141B]/95 backdrop-blur-2xl p-3 sm:p-4 shadow-2xl relative overflow-hidden">
        
        <!-- Kabin Üst Başlığı -->
        <div class="flex items-center justify-between pb-2.5 border-b border-zinc-800/70">
          <div class="flex items-center gap-2">
            <div class="h-6 w-6 rounded-lg bg-[#E08544]/15 border border-[#E08544]/30 flex items-center justify-center">
              <svg class="w-3.5 h-3.5 text-[#E08544]" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                <path d="M12 3a3 3 0 0 0-3 3c0 1.25.75 2 1.5 2.5L3 17h18l-7.5-8.5C14.25 8 15 7.25 15 6a3 3 0 0 0-3-3z" />
              </svg>
            </div>
            <div>
              <h2 class="text-[11px] sm:text-xs font-bold tracking-wider text-zinc-100 uppercase">
                Sanal Kabin Önizleme
              </h2>
            </div>
          </div>
          <div class="flex items-center gap-2">
            <span id="model-status-pill" class="text-[10px] sm:text-[11px] px-2 py-0.5 rounded-full bg-emerald-500/10 text-emerald-400 font-mono flex items-center gap-1 border border-emerald-500/20">
              <span class="h-1.5 w-1.5 rounded-full bg-emerald-400 animate-pulse"></span>
              <span id="model-status-text">Kahverengi Yelek</span>
            </span>
            <button id="btn-clear" class="text-[11px] text-zinc-400 hover:text-amber-300 transition-colors px-1.5 py-0.5 rounded bg-zinc-800/80">
              Çıkar
            </button>
          </div>
        </div>

        <!-- Manken Önizleme Çerçevesi (Mobilde yüksekliği sınırlandırılmış kompakt oran) -->
        <div id="mannequin-frame" class="relative mt-2.5 aspect-[4/5] sm:aspect-[3/4] lg:aspect-[9/16] max-h-[310px] sm:max-h-[380px] lg:max-h-[560px] w-full rounded-xl sm:rounded-2xl overflow-hidden bg-[#07060A] border border-zinc-800/80 shadow-inner flex items-center justify-center">
          
          <img
            id="mannequin-img"
            src="{m_brn}"
            alt="Model Önizleme"
            class="model-transition w-full h-full object-cover object-top"
          />

          <!-- Gradient Karartma -->
          <div class="absolute inset-0 bg-gradient-to-t from-black/85 via-black/10 to-transparent pointer-events-none"></div>

          <!-- Model Üzerindeki Aktif Ürün Rozeti -->
          <div id="active-item-badge" class="absolute bottom-2.5 left-2.5 right-2.5 p-2.5 sm:p-3 rounded-xl sm:rounded-2xl bg-[#16151E]/95 border border-zinc-700/60 backdrop-blur-md flex items-center justify-between transition-all duration-300">
            <div>
              <span class="text-[9px] sm:text-[10px] tracking-wider uppercase text-[#E08544] font-mono flex items-center gap-1">
                <span class="h-1 w-1 rounded-full bg-[#E08544] animate-ping"></span>
                Model Üzerinde Giyili
              </span>
              <p id="active-item-name" class="text-[11px] sm:text-xs font-bold text-zinc-100 line-clamp-1 mt-0.5">
                Kapitoneli Şişme Yelek (Kahverengi)
              </p>
              <p id="active-item-price" class="text-xs sm:text-sm text-[#E08544] font-bold font-mono">
                $189 <span class="text-zinc-500 line-through text-[10px] font-normal ml-1">$229</span>
              </p>
            </div>
            <button id="btn-cart-active" class="px-2.5 py-1.5 sm:px-3 sm:py-2 rounded-lg sm:rounded-xl bg-[#E08544] hover:bg-[#eb8c49] text-white text-[11px] sm:text-xs font-bold transition-transform active:scale-95 shadow-md shadow-[#E08544]/30">
              Sepete Ekle
            </button>
          </div>

          <!-- Baz Manken Boş Durum Bilgisi -->
          <div id="empty-state-badge" class="hidden absolute bottom-3 left-3 right-3 text-center">
            <span class="text-[11px] text-zinc-400 bg-black/80 px-3 py-1 rounded-full border border-zinc-800">
              Karttaki askı simgesine basarak mankene giydirin
            </span>
          </div>
        </div>

        <!-- Kabin Askılığı (Kompakt Yatay Şerit) -->
        <div class="mt-2.5 pt-2 border-t border-zinc-800/70">
          <div class="flex items-center justify-between mb-1.5">
            <span class="text-[11px] font-medium text-zinc-400">
              Kabin Askılığı (<span id="rack-count">1</span>)
            </span>
            <span class="text-[10px] text-zinc-500">Giydirmek için tıkla</span>
          </div>

          <div id="fitting-rack" class="flex gap-2 overflow-x-auto pb-1 items-center">
            <!-- Dinamik doldurulacak -->
          </div>
        </div>
      </div>
    </aside>

    <!-- ==============================================================
         SAĞ PANEL: MİNİMAL VE MOBİLDE 2 KOLONLU ÜRÜN KATALOĞU
         ============================================================== -->
    <section class="lg:col-span-7 space-y-3 sm:space-y-4">
      <div class="flex items-center justify-between pb-1.5 border-b border-zinc-800/60">
        <div>
          <h2 class="text-sm sm:text-base font-bold tracking-tight text-zinc-100">Koleksiyon</h2>
          <p class="text-[11px] text-zinc-400">
            Modelde denemek için <span class="text-[#E08544] font-semibold">turuncu askı</span> simgesine tıklayın.
          </p>
        </div>
        <span class="text-[11px] font-mono text-zinc-500" id="catalog-count">3 Ürün</span>
      </div>

      <!-- MOBİLDE 2 KOLONLU MİNİMAL GRID (grid-cols-2) -->
      <div class="grid grid-cols-2 gap-2.5 sm:gap-3.5 lg:grid-cols-2" id="product-grid">
        <!-- JS ile çizilecek -->
      </div>
    </section>
  </main>

  <!-- Toast Bildirimi -->
  <div id="toast" class="fixed top-5 right-4 z-50 bg-[#16151E] border border-[#E08544]/60 text-amber-200 text-xs px-3.5 py-2 rounded-xl shadow-2xl shadow-black/80 flex items-center gap-2 transform translate-y-[-100px] opacity-0 transition-all duration-300 pointer-events-none">
    <span class="h-2 w-2 rounded-full bg-[#E08544] animate-ping"></span>
    <span id="toast-text">İşlem yapıldı</span>
  </div>

  <!-- JAVASCRIPT & ANİMASYON MANTIĞI -->
  <script>
    const IMAGES = {{
      baseMannequin: "{b_man}",
      brownVest: "{b_brn}",
      blackVest: "{b_blk}",
      greenJacket: "{b_grn}",
      modelBrown: "{m_brn}",
      modelBlack: "{m_blk}",
      modelGreen: "{m_grn}",
    }};

    const PRODUCTS = [
      {{
        id: 'jacket-green',
        name: 'Army Green Puffer Jacket',
        color: 'Asker Yeşili',
        price: 189,
        oldPrice: 229,
        rating: 4.3,
        card_image: IMAGES.greenJacket,
        model_image_url: IMAGES.modelGreen,
      }},
      {{
        id: 'vest-brown',
        name: 'Kapitoneli Şişme Yelek',
        color: 'Kahverengi',
        price: 189,
        oldPrice: 229,
        rating: 4.8,
        card_image: IMAGES.brownVest,
        model_image_url: IMAGES.modelBrown,
      }},
      {{
        id: 'vest-black',
        name: 'Mat Nappa Kapitoneli Yelek',
        color: 'Siyah',
        price: 199,
        oldPrice: 239,
        rating: 4.9,
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

    // Model Geçişi
    function changeModelVisual(targetUrl) {{
      mannequinImg.style.opacity = '0';
      mannequinImg.style.transform = 'scale(1.02)';
      mannequinImg.style.filter = 'blur(6px)';

      setTimeout(() => {{
        mannequinImg.src = targetUrl;
        mannequinImg.onload = () => {{
          mannequinImg.style.opacity = '1';
          mannequinImg.style.transform = 'scale(1)';
          mannequinImg.style.filter = 'blur(0px)';
        }};
      }}, 140);
    }}

    // Uçuş & Büyükten Küçülme Animasyonu (Şeffaf PNG Dekupe)
    function triggerPopAndShrinkFlight(sourceImg, product) {{
      const startRect = sourceImg.getBoundingClientRect();
      const targetRect = mannequinFrame.getBoundingClientRect();

      // Uçan şeffaf klon oluştur
      const clone = document.createElement('img');
      clone.src = product.card_image;
      clone.className = 'flying-card';
      clone.style.left = `${{startRect.left}}px`;
      clone.style.top = `${{startRect.top}}px`;
      clone.style.width = `${{startRect.width}}px`;
      clone.style.height = `${{startRect.height}}px`;
      clone.style.objectFit = 'contain';

      document.body.appendChild(clone);

      // Aşama 1: Yerinden fırlama ve büyüme (Pop-out)
      requestAnimationFrame(() => {{
        clone.style.transform = 'scale(1.2) rotate(-5deg)';
        clone.style.transition = 'all 240ms cubic-bezier(0.34, 1.56, 0.64, 1)';
      }});

      // Aşama 2: Büyükten küçülerek manken göğsüne süzülme
      setTimeout(() => {{
        const targetX = targetRect.left + (targetRect.width / 2) - 50;
        const targetY = targetRect.top + (targetRect.height * 0.35) - 50;

        clone.style.transition = 'all 500ms cubic-bezier(0.22, 1, 0.36, 1)';
        clone.style.left = `${{targetX}}px`;
        clone.style.top = `${{targetY}}px`;
        clone.style.width = '100px';
        clone.style.height = '100px';
        clone.style.transform = 'scale(0.38) rotate(2deg)';
        clone.style.opacity = '0';
      }}, 230);

      // Aşama 3: Mankenin üzerine oturma
      setTimeout(() => {{
        clone.remove();
        setActiveProduct(product, false);
      }}, 730);
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
        activeItemPrice.innerHTML = `$${{product.price}} <span class="text-zinc-500 line-through text-[10px] font-normal ml-1">$${{product.oldPrice}}</span>`;
        modelStatusText.textContent = product.color;
        activeItemBadge.classList.remove('hidden');
        emptyStateBadge.classList.add('hidden');
        showToast(`\"${{product.name}}\" model üzerinde giyildi.`);
      }} else {{
        changeModelVisual(IMAGES.baseMannequin);
        activeItemBadge.classList.add('hidden');
        emptyStateBadge.classList.remove('hidden');
        modelStatusText.textContent = 'Boş';
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
          <div class="w-full py-2 text-center rounded-lg border border-dashed border-zinc-800 text-[10px] text-zinc-500">
            Askılık boş.
          </div>
        `;
        return;
      }}

      fittingRoomItems.forEach(item => {{
        const isActive = activeItem && activeItem.id === item.id;
        const slot = document.createElement('div');
        slot.className = `relative group flex-shrink-0 w-14 cursor-pointer rounded-lg border p-1 transition-all ${{
          isActive
            ? 'border-[#E08544] bg-[#E08544]/10 shadow-sm shadow-[#E08544]/20'
            : 'border-zinc-800 bg-zinc-900/60 hover:border-zinc-700'
        }}`;

        slot.innerHTML = `
          ${{isActive ? '<div class=\"absolute inset-0 rounded-lg border-2 border-[#E08544] pointer-events-none\"></div>' : ''}}
          <div class=\"relative aspect-square w-full rounded overflow-hidden bg-zinc-950 mb-0.5 flex items-center justify-center\">
            <img src=\"${{item.card_image}}\" alt=\"${{item.name}}\" class=\"w-full h-full object-contain p-0.5\" />
            <button class=\"remove-btn absolute top-0.5 right-0.5 h-3.5 w-3.5 rounded-full bg-black/85 hover:bg-red-500 text-zinc-300 hover:text-white flex items-center justify-center text-[8px] opacity-0 group-hover:opacity-100 transition-opacity\">
              ✕
            </button>
          </div>
          <p class=\"text-[9px] font-semibold text-zinc-200 truncate\">${{item.color}}</p>
        `;

        slot.addEventListener('click', () => setActiveProduct(item, false));
        slot.querySelector('.remove-btn').addEventListener('click', (e) => removeProductFromRack(item.id, e));
        fittingRack.appendChild(slot);
      }});
    }}

    // GÖNDERİLEN GÖRSELE SADIK KALINAN MİNİMAL ÜRÜN KARTLARI
    function renderCatalog() {{
      productGrid.innerHTML = '';

      PRODUCTS.forEach(product => {{
        const isCurrentActive = activeItem && activeItem.id === product.id;
        const isFav = !!favorites[product.id];

        const card = document.createElement('div');
        card.className = `relative rounded-2xl bg-[#17161D] border border-zinc-800/80 p-2.5 sm:p-3.5 shadow-lg overflow-hidden flex flex-col justify-between group transition-all duration-300 hover:border-zinc-700 ${{
          isCurrentActive ? 'ring-1 ring-[#E08544]/50 shadow-[#E08544]/10' : ''
        }}`;

        card.innerHTML = `
          <!-- Kart Üstü: Sol Kalp ve Askı, Sağ Puan -->
          <div>
            <div class=\"flex items-start justify-between z-10\">
              
              <!-- Sol Üst Butonlar (Kalp & Turuncu Askı) -->
              <div class=\"flex flex-col gap-1.5\">
                <!-- Kalp Butonu -->
                <button class=\"fav-btn h-7 w-7 sm:h-8 sm:w-8 rounded-full flex items-center justify-center transition-all ${{
                  isFav
                    ? 'bg-rose-500/20 text-rose-400 border border-rose-500/40'
                    : 'bg-[#2B2A34] hover:bg-[#383742] text-zinc-300'
                }}\">
                  <svg class=\"w-3.5 h-3.5 ${{isFav ? 'fill-current' : 'fill-none'}}\" viewBox=\"0 0 24 24\" stroke=\"currentColor\" strokeWidth=\"2\">
                    <path d=\"M20.84 4.61a5.5 5.5 0 0 0-7.78 0L12 5.67l-1.06-1.06a5.5 5.5 0 0 0-7.78 7.78l1.06 1.06L12 21.23l7.78-7.78 1.06-1.06a5.5 5.5 0 0 0 0-7.78z\" />
                  </svg>
                </button>

                <!-- Askı Butonu (Gönderdiğiniz görseldeki gibi turuncu #E08544) -->
                <button class=\"hanger-btn h-7 w-7 sm:h-8 sm:w-8 rounded-full flex items-center justify-center transition-all duration-300 active:scale-90 ${{
                  isCurrentActive
                    ? 'bg-[#E08544] text-white shadow-md shadow-[#E08544]/40 ring-2 ring-white/30 scale-105'
                    : 'bg-[#E08544] hover:brightness-110 text-white shadow-sm shadow-[#E08544]/25'
                }}\" title=\"Askıya Al / Modelde Dene\">
                  <svg class=\"w-3.5 h-3.5\" viewBox=\"0 0 24 24\" fill=\"none\" stroke=\"currentColor\" strokeWidth=\"2.2\">
                    <path d=\"M12 3a3 3 0 0 0-3 3c0 1.25.75 2 1.5 2.5L3 17h18l-7.5-8.5C14.25 8 15 7.25 15 6a3 3 0 0 0-3-3z\" />
                  </svg>
                </button>
              </div>

              <!-- Sağ Üst: Minimal Yıldız Rozeti (★ 4.3) -->
              <div class=\"flex items-center gap-1 px-2 py-0.5 rounded-full bg-[#272630] border border-zinc-700/40 text-[10px] sm:text-xs font-semibold text-zinc-200\">
                <span class=\"text-[#FBBF24]\">★</span>
                <span>${{product.rating.toFixed(1)}}</span>
              </div>
            </div>

            <!-- Kart Ortası: Dekupe Ürün Görseli (Kompakt Yükseklik) -->
            <div class=\"relative my-1 sm:my-2 h-24 sm:h-32 md:h-36 w-full flex items-center justify-center\">
              <img
                id=\"card-img-${{product.id}}\"
                src=\"${{product.card_image}}\"
                alt=\"${{product.name}}\"
                class=\"max-h-full max-w-full object-contain filter drop-shadow-[0_12px_20px_rgba(0,0,0,0.65)] transition-transform duration-300 group-hover:scale-105\"
              />
            </div>
          </div>

          <!-- Kart Altı: Başlık, Fiyat Satırı ve Minimal Sepet+ Simgesi -->
          <div class=\"mt-1 pt-1.5\">
            <h3 class=\"text-[11px] sm:text-xs text-zinc-400 font-normal truncate\">
              ${{product.name}}
            </h3>

            <div class=\"flex items-center justify-between mt-0.5\">
              <div class=\"flex items-center gap-1 sm:gap-1.5 flex-wrap\">
                <span class=\"text-sm sm:text-base font-bold text-[#E08544] tracking-tight\">
                  $${{product.price}}
                </span>
                <span class=\"text-[10px] sm:text-xs text-zinc-500 line-through\">
                  $${{product.oldPrice}}
                </span>
                <span class=\"text-[9px] font-semibold bg-[#2E2827] text-[#E08544] px-1.5 py-0.2 rounded-full\">
                  Sale
                </span>
              </div>

              <!-- Gönderilen Görseldeki Minimal Beyaz Sepet+ Simgesi (Kutu veya Köşe Kaplama Yok) -->
              <button class=\"cart-btn p-1 text-zinc-300 hover:text-white active:scale-90 transition-transform\" title=\"Sepete Ekle\">
                <svg class=\"w-5 h-5\" viewBox=\"0 0 24 24\" fill=\"none\" stroke=\"currentColor\" strokeWidth=\"1.9\" strokeLinecap=\"round\" strokeLinejoin=\"round\">
                  <path d=\"M6 2 3 6v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2V6l-3-4Z\" />
                  <path d=\"M3 6h18\" />
                  <path d=\"M16 10a4 4 0 0 1-8 0\" />
                  <path d=\"M19 19v-4m-2 2h4\" strokeWidth=\"2\" />
                </svg>
              </button>
            </div>
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

    // Genel Kontroller
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

with open('/Users/hikmetakan/.gemini/antigravity/scratch/fitting-room-demo/index.html', 'w', encoding='utf-8') as f:
    f.write(html_content)

print('SUCCESS: fitting_room_demo.html and index.html updated with responsive minimal cards!')
