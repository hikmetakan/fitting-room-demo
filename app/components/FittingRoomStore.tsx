'use client';

import React, { useState, useRef } from 'react';
import { motion, AnimatePresence } from 'framer-motion';

// --------------------------------------------------------------------------
// 1. Tip Tanımları (Product Schema)
// --------------------------------------------------------------------------
export interface Product {
  id: string;
  name: string;
  category: string;
  price: number;
  currency: string;
  rating: number;
  color: string;
  card_image: string;       // Ürün dekupe görseli
  model_image_url: string;  // Gönderilen modelin o kıyafeti giydiği fotoğraf
}

interface FlyingItemState {
  product: Product;
  startRect: { left: number; top: number; width: number; height: number };
  targetRect: { left: number; top: number; width: number; height: number };
}

// --------------------------------------------------------------------------
// 2. Kullanıcının Yüklediği Gerçek Ürün ve Model Veri Eşlemesi (Data Mapping)
// --------------------------------------------------------------------------
const BASE_MANNEQUIN_IMAGE = '/images/base-mannequin.jpg';

export const PRODUCTS: Product[] = [
  {
    id: 'vest-brown',
    name: 'Kapitoneli Şişme Yelek',
    category: 'Yelek & Dış Giyim',
    price: 3450,
    currency: '₺',
    rating: 4.9,
    color: 'Kahverengi',
    card_image: '/images/brown-vest.png',
    model_image_url: '/images/model-brown-vest.jpg',
  },
  {
    id: 'vest-black',
    name: 'Mat Nappa Kapitoneli Yelek',
    category: 'Yelek & Dış Giyim',
    price: 3650,
    currency: '₺',
    rating: 4.8,
    color: 'Siyah',
    card_image: '/images/black-vest.png',
    model_image_url: '/images/model-black-vest.jpg',
  },
];

// --------------------------------------------------------------------------
// 3. Ana Sanal Kabin Bileşeni
// --------------------------------------------------------------------------
export default function FittingRoomStore() {
  // Manken üzerinde aktif olan kıyafet (null ise baz gri manken gösterilir)
  const [activeItem, setActiveItem] = useState<Product | null>(PRODUCTS[0]);
  
  // Sol paneldeki askılık listesi
  const [fittingRoomItems, setFittingRoomItems] = useState<Product[]>([PRODUCTS[0]]);
  
  // Favori ürünler
  const [favorites, setFavorites] = useState<Record<string, boolean>>({});

  // Uçan/Küçülen Ürün Animasyon State'i
  const [flyingItem, setFlyingItem] = useState<FlyingItemState | null>(null);

  // Toast bildirimi
  const [toastMessage, setToastMessage] = useState<string | null>(null);

  // Manken referansı
  const mannequinRef = useRef<HTMLDivElement>(null);

  const showToast = (msg: string) => {
    setToastMessage(msg);
    setTimeout(() => setToastMessage(null), 2400);
  };

  const toggleFavorite = (productId: string, e: React.MouseEvent) => {
    e.stopPropagation();
    setFavorites((prev) => {
      const next = !prev[productId];
      showToast(next ? 'Favorilere eklendi' : 'Favorilerden çıkarıldı');
      return { ...prev, [productId]: next };
    });
  };

  // Askı simgesine tıklandığında: Büyükten küçülerek uçuş animasyonunu başlat
  const handleHangerClick = (product: Product) => {
    const cardImgEl = document.getElementById(`product-img-${product.id}`);
    const mannequinEl = mannequinRef.current;

    if (cardImgEl && mannequinEl) {
      const startRect = cardImgEl.getBoundingClientRect();
      const targetRect = mannequinEl.getBoundingClientRect();

      // Uçuş animasyonunu tetikle
      setFlyingItem({
        product,
        startRect: {
          left: startRect.left,
          top: startRect.top,
          width: startRect.width,
          height: startRect.height,
        },
        targetRect: {
          left: targetRect.left,
          top: targetRect.top,
          width: targetRect.width,
          height: targetRect.height,
        },
      });
    } else {
      // Fallback: Doğrudan aktifleştir
      setActiveItem(product);
    }

    // Askılığa ekle (yoksa)
    setFittingRoomItems((prev) => {
      if (!prev.some((p) => p.id === product.id)) {
        return [...prev, product];
      }
      return prev;
    });
  };

  // Uçuş animasyonu tamamlandığında mankeni giydir
  const handleFlightComplete = () => {
    if (flyingItem) {
      setActiveItem(flyingItem.product);
      showToast(`"${flyingItem.product.name}" mankene giydirildi.`);
      setFlyingItem(null);
    }
  };

  // Askılıktan ürün kaldırma
  const handleRemoveFromRack = (productId: string, e: React.MouseEvent) => {
    e.stopPropagation();
    const updated = fittingRoomItems.filter((p) => p.id !== productId);
    setFittingRoomItems(updated);

    if (activeItem?.id === productId) {
      setActiveItem(updated.length > 0 ? updated[updated.length - 1] : null);
    }
  };

  return (
    <div className="min-h-screen bg-[#0E0F12] text-zinc-100 selection:bg-amber-500/30 selection:text-amber-200">
      
      {/* Toast Notification */}
      <AnimatePresence>
        {toastMessage && (
          <motion.div
            initial={{ opacity: 0, y: -20, scale: 0.95 }}
            animate={{ opacity: 1, y: 0, scale: 1 }}
            exit={{ opacity: 0, y: -20, scale: 0.95 }}
            className="fixed top-20 right-6 z-50 bg-[#1A1B20] border border-amber-500/50 text-amber-300 text-xs px-4 py-2.5 rounded-xl shadow-2xl shadow-black/80 flex items-center gap-2"
          >
            <span className="h-2 w-2 rounded-full bg-amber-400 animate-ping" />
            {toastMessage}
          </motion.div>
        )}
      </AnimatePresence>

      {/* ================================================================
          UÇAN & BÜYÜKTEN KÜÇÜLEN ÜRÜN ANİMASYONU (FLIP MICRO-INTERACTION)
         ================================================================ */}
      <AnimatePresence>
        {flyingItem && (
          <motion.div
            initial={{
              position: 'fixed',
              left: flyingItem.startRect.left,
              top: flyingItem.startRect.top,
              width: flyingItem.startRect.width,
              height: flyingItem.startRect.height,
              scale: 1,
              rotate: 0,
              opacity: 1,
              zIndex: 9999,
              pointerEvents: 'none',
            }}
            animate={{
              left: [
                flyingItem.startRect.left,
                flyingItem.startRect.left - 40,
                flyingItem.targetRect.left + flyingItem.targetRect.width / 2 - (flyingItem.startRect.width * 0.42) / 2,
              ],
              top: [
                flyingItem.startRect.top,
                flyingItem.startRect.top - 50,
                flyingItem.targetRect.top + flyingItem.targetRect.height * 0.35 - (flyingItem.startRect.height * 0.42) / 2,
              ],
              // Büyükten küçülerek: 1 -> 1.18 (yerinden fırlama) -> 0.42 (manken göğsüne oturma)
              scale: [1, 1.18, 0.42],
              rotate: [0, -8, 2],
              opacity: [1, 1, 0.95, 0],
            }}
            transition={{
              duration: 0.85,
              times: [0, 0.25, 1],
              ease: [0.22, 1, 0.36, 1],
            }}
            onAnimationComplete={handleFlightComplete}
            className="flex items-center justify-center filter drop-shadow-[0_25px_35px_rgba(224,133,68,0.45)]"
          >
            {/* eslint-disable-next-line @next/next/no-img-element */}
            <img
              src={flyingItem.product.card_image}
              alt="Uçan Kıyafet"
              className="w-full h-full object-contain"
            />
          </motion.div>
        )}
      </AnimatePresence>

      {/* Header */}
      <header className="border-b border-zinc-800/80 bg-[#121318]/80 backdrop-blur-md sticky top-0 z-40">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 h-16 flex items-center justify-between">
          <div className="flex items-center gap-3">
            <div className="h-9 w-9 rounded-xl bg-gradient-to-tr from-amber-500 to-amber-300 flex items-center justify-center text-black font-black text-sm shadow-lg shadow-amber-500/20">
              V
            </div>
            <div>
              <span className="font-bold tracking-wider text-sm uppercase text-zinc-100">Atelier Sanal Kabin</span>
              <span className="text-zinc-500 text-xs ml-2 font-mono">/ Live Model Mapping</span>
            </div>
          </div>

          <div className="flex items-center gap-3">
            <span className="inline-flex items-center gap-2 px-3 py-1 rounded-full text-xs font-medium bg-emerald-950/60 text-emerald-400 border border-emerald-800/50">
              <span className="h-1.5 w-1.5 rounded-full bg-emerald-400 animate-pulse" />
              Hazır Model Eşlemesi Aktif
            </span>
          </div>
        </div>
      </header>

      {/* Main Grid */}
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="grid grid-cols-1 lg:grid-cols-12 gap-8 items-start">
          
          {/* ================================================================
              SOL PANEL: SANAL KABİN & GÖNDERİLEN MODEL (STICKY)
             ================================================================ */}
          <aside className="lg:col-span-5 lg:sticky lg:top-24 space-y-4">
            <div className="rounded-3xl border border-zinc-800/90 bg-[#16171D]/90 backdrop-blur-2xl p-5 shadow-2xl relative overflow-hidden">
              
              {/* Başlık Alanı */}
              <div className="flex items-center justify-between pb-3.5 border-b border-zinc-800/70">
                <div className="flex items-center gap-2.5">
                  <div className="h-7 w-7 rounded-lg bg-amber-500/10 border border-amber-500/20 flex items-center justify-center">
                    <svg className="w-4 h-4 text-amber-400" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                      <path d="M12 3a3 3 0 0 0-3 3c0 1.25.75 2 1.5 2.5L3 17h18l-7.5-8.5C14.25 8 15 7.25 15 6a3 3 0 0 0-3-3z" />
                    </svg>
                  </div>
                  <div>
                    <h2 className="text-xs font-bold tracking-wider text-zinc-100 uppercase">
                      Sanal Kabin Önizleme
                    </h2>
                    <p className="text-[11px] text-zinc-500">
                      {activeItem ? `Model üzerinde: ${activeItem.name}` : 'Manken boş durumda'}
                    </p>
                  </div>
                </div>

                {activeItem && (
                  <button
                    onClick={() => {
                      setActiveItem(null);
                      showToast('Kıyafet çıkarıldı, baz mankene dönüldü.');
                    }}
                    className="text-xs text-zinc-400 hover:text-amber-300 transition-colors px-2 py-1 rounded bg-zinc-800/60 hover:bg-zinc-800"
                  >
                    Çıkar / Sıfırla
                  </button>
                )}
              </div>

              {/* Manken & Model Önizleme Çerçevesi */}
              <div
                ref={mannequinRef}
                id="mannequin-container"
                className="relative mt-4 aspect-[9/16] max-h-[580px] w-full rounded-2xl overflow-hidden bg-[#0A0B0E] border border-zinc-800/80 shadow-inner flex items-center justify-center"
              >
                {/* AnimatePresence ile Pürüzsüz Cross-Dissolve + Blur Model Değişimi */}
                <AnimatePresence mode="wait">
                  <motion.div
                    key={activeItem ? activeItem.id : 'base-mannequin'}
                    initial={{ opacity: 0, scale: 0.98, filter: 'blur(10px)' }}
                    animate={{ opacity: 1, scale: 1, filter: 'blur(0px)' }}
                    exit={{ opacity: 0, scale: 1.02, filter: 'blur(8px)' }}
                    transition={{ duration: 0.5, ease: [0.22, 1, 0.36, 1] }}
                    className="absolute inset-0 w-full h-full"
                  >
                    {/* eslint-disable-next-line @next/next/no-img-element */}
                    <img
                      src={activeItem ? activeItem.model_image_url : BASE_MANNEQUIN_IMAGE}
                      alt={activeItem ? activeItem.name : 'Baz Manken'}
                      className="w-full h-full object-cover object-top"
                    />
                    <div className="absolute inset-0 bg-gradient-to-t from-black/80 via-transparent to-transparent pointer-events-none" />
                  </motion.div>
                </AnimatePresence>

                {/* Model Üzerindeki Aktif Ürün Kartı */}
                {activeItem ? (
                  <motion.div
                    initial={{ opacity: 0, y: 20 }}
                    animate={{ opacity: 1, y: 0 }}
                    transition={{ delay: 0.2, duration: 0.35 }}
                    className="absolute bottom-3 left-3 right-3 p-3.5 rounded-2xl bg-[#16171E]/90 border border-zinc-700/60 backdrop-blur-md flex items-center justify-between"
                  >
                    <div>
                      <span className="text-[10px] tracking-wider uppercase text-amber-400 font-mono flex items-center gap-1.5">
                        <span className="h-1.5 w-1.5 rounded-full bg-amber-400 animate-ping" />
                        Model Üzerinde Giyili
                      </span>
                      <p className="text-xs font-bold text-zinc-100 line-clamp-1 mt-0.5">
                        {activeItem.name} ({activeItem.color})
                      </p>
                      <p className="text-xs text-zinc-300 font-bold font-mono">
                        {activeItem.price.toLocaleString('tr-TR')} {activeItem.currency}
                      </p>
                    </div>

                    <button
                      onClick={() => showToast(`"${activeItem.name}" sepete eklendi!`)}
                      className="px-3.5 py-2 rounded-xl bg-gradient-to-r from-amber-500 to-[#E08544] hover:brightness-110 text-black text-xs font-bold transition-transform active:scale-95 shadow-md shadow-amber-500/25"
                    >
                      Sepete Ekle
                    </button>
                  </motion.div>
                ) : (
                  <div className="absolute bottom-4 left-4 right-4 text-center">
                    <span className="text-xs text-zinc-400 bg-black/70 px-4 py-1.5 rounded-full border border-zinc-800">
                      Askıdaki bir ürüne tıklayarak mankene giydirin
                    </span>
                  </div>
                )}
              </div>

              {/* Kabin Askılığı (Fitting Room Rack) */}
              <div className="mt-4 pt-3.5 border-t border-zinc-800/70">
                <div className="flex items-center justify-between mb-2.5">
                  <span className="text-xs font-semibold text-zinc-300">
                    Askıdaki Parçalar ({fittingRoomItems.length})
                  </span>
                  <span className="text-[11px] text-zinc-500">Mankene giydirmek için tıkla</span>
                </div>

                <div className="flex gap-2.5 overflow-x-auto pb-1 scrollbar-thin">
                  {fittingRoomItems.map((item) => {
                    const isActive = activeItem?.id === item.id;
                    return (
                      <div
                        key={item.id}
                        onClick={() => setActiveItem(item)}
                        className={`relative group flex-shrink-0 w-20 cursor-pointer rounded-xl border p-1.5 transition-all ${
                          isActive
                            ? 'border-amber-400 bg-amber-400/10'
                            : 'border-zinc-800 bg-zinc-900/60 hover:border-zinc-700'
                        }`}
                      >
                        {isActive && (
                          <motion.div
                            layoutId="rack-active-glow"
                            className="absolute inset-0 rounded-xl border-2 border-amber-400 pointer-events-none"
                            transition={{ type: 'spring', stiffness: 350, damping: 28 }}
                          />
                        )}

                        <div className="relative aspect-square w-full rounded-lg overflow-hidden bg-zinc-950 mb-1">
                          {/* eslint-disable-next-line @next/next/no-img-element */}
                          <img
                            src={item.card_image}
                            alt={item.name}
                            className="w-full h-full object-cover"
                          />
                          <button
                            onClick={(e) => handleRemoveFromRack(item.id, e)}
                            className="absolute top-0.5 right-0.5 h-4 w-4 rounded-full bg-black/80 hover:bg-red-500 text-zinc-300 hover:text-white flex items-center justify-center text-[10px] opacity-0 group-hover:opacity-100 transition-opacity"
                            title="Askıdan Çıkar"
                          >
                            ✕
                          </button>
                        </div>
                        <p className="text-[10px] font-medium text-zinc-300 truncate">
                          {item.name}
                        </p>
                        <p className="text-[9px] text-zinc-500 font-mono">
                          {item.price.toLocaleString('tr-TR')} {item.currency}
                        </p>
                      </div>
                    );
                  })}
                </div>
              </div>
            </div>
          </aside>

          {/* ================================================================
              SAĞ PANEL: KULLANICININ GÖNDERDİĞİ KART TASARIMI (GRID)
             ================================================================ */}
          <section className="lg:col-span-7 space-y-5">
            <div className="flex items-center justify-between pb-2 border-b border-zinc-800/60">
              <div>
                <h1 className="text-xl font-bold tracking-tight text-zinc-100">Özel Koleksiyon</h1>
                <p className="text-xs text-zinc-400">
                  Model üzerinde canlı görmek için ürün kartındaki <span className="text-amber-400 font-semibold">askı simgesine</span> tıklayın.
                </p>
              </div>
              <span className="text-xs font-mono text-zinc-500">{PRODUCTS.length} Renk Seçeneği</span>
            </div>

            <div className="grid grid-cols-1 sm:grid-cols-2 gap-5">
              {PRODUCTS.map((product) => {
                const isCurrentActive = activeItem?.id === product.id;
                const isFav = !!favorites[product.id];

                return (
                  /* ==========================================================
                     GÖNDERİLEN GÖRSELE SADIK KALINAN ÜRÜN KARTI TASARIMI
                     ========================================================== */
                  <div
                    key={product.id}
                    className="relative rounded-[32px] bg-[#1B1C22] border border-zinc-800/80 p-5 shadow-2xl overflow-hidden flex flex-col justify-between group transition-all duration-300 hover:border-zinc-700"
                  >
                    {/* Kart Üst Bölümü (Sol: Kalp + Askı, Sağ: Puan Rozeti) */}
                    <div className="flex items-start justify-between z-10">
                      
                      {/* Sol Üst Buton Grubu: Kalp ve Askı */}
                      <div className="flex flex-col gap-2.5">
                        
                        {/* Kalp (Favori) Butonu */}
                        <button
                          onClick={(e) => toggleFavorite(product.id, e)}
                          className={`h-10 w-10 rounded-full flex items-center justify-center transition-all ${
                            isFav
                              ? 'bg-rose-500/20 text-rose-400 border border-rose-500/40'
                              : 'bg-[#292A32]/80 hover:bg-[#34353F] text-zinc-300'
                          }`}
                          title="Favorilere Ekle"
                        >
                          <svg
                            className={`w-4 h-4 ${isFav ? 'fill-current' : 'fill-none'}`}
                            viewBox="0 0 24 24"
                            stroke="currentColor"
                            strokeWidth="2"
                          >
                            <path d="M20.84 4.61a5.5 5.5 0 0 0-7.78 0L12 5.67l-1.06-1.06a5.5 5.5 0 0 0-7.78 7.78l1.06 1.06L12 21.23l7.78-7.78 1.06-1.06a5.5 5.5 0 0 0 0-7.78z" />
                          </svg>
                        </button>

                        {/* Askı Butonu (Fitting Room Trigger) */}
                        <motion.button
                          whileTap={{ scale: 0.9 }}
                          whileHover={{ scale: 1.06 }}
                          onClick={() => handleHangerClick(product)}
                          className={`h-10 w-10 rounded-full flex items-center justify-center transition-all duration-300 ${
                            isCurrentActive
                              ? 'bg-amber-500 text-black shadow-lg shadow-amber-500/30 ring-2 ring-amber-400'
                              : 'bg-[#292A32]/80 hover:bg-amber-500 hover:text-black text-zinc-300'
                          }`}
                          title="Askıya Al / Kabinde Dene"
                        >
                          <svg className="w-4 h-4" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.2">
                            <path d="M12 3a3 3 0 0 0-3 3c0 1.25.75 2 1.5 2.5L3 17h18l-7.5-8.5C14.25 8 15 7.25 15 6a3 3 0 0 0-3-3z" />
                          </svg>
                        </motion.button>
                      </div>

                      {/* Sağ Üst: Yıldızlı Puan Rozeti (★ 4.9) */}
                      <div className="flex items-center gap-1.5 px-3 py-1.5 rounded-full bg-[#292A32]/80 border border-zinc-700/40 text-xs font-semibold text-zinc-200">
                        <span className="text-[#FBBF24]">★</span>
                        <span>{product.rating.toFixed(1)}</span>
                      </div>
                    </div>

                    {/* Kart Ortası: Ürün Dekupe Görseli */}
                    <div className="relative my-4 aspect-[4/5] w-full flex items-center justify-center">
                      {/* eslint-disable-next-line @next/next/no-img-element */}
                      <img
                        id={`product-img-${product.id}`}
                        src={product.card_image}
                        alt={product.name}
                        className="max-h-full max-w-full object-contain filter drop-shadow-[0_15px_25px_rgba(0,0,0,0.6)] transition-transform duration-500 group-hover:scale-105"
                      />
                    </div>

                    {/* Kart Altı: Sol İsim & Fiyat, Sağ Terracotta Sepet Butonu */}
                    <div className="flex items-end justify-between mt-2 pt-2">
                      <div className="space-y-1">
                        <h3 className="text-sm font-medium text-zinc-300 line-clamp-1">
                          {product.name} ({product.color})
                        </h3>
                        <p className="text-2xl font-bold text-white tracking-tight">
                          {product.price.toLocaleString('tr-TR')} {product.currency}
                        </p>
                      </div>

                      {/* Sağ Alttaki Özel Terracotta Çeyrek-Daire Sepet Butonu */}
                      <button
                        onClick={() => showToast(`"${product.name}" sepete eklendi!`)}
                        className="absolute bottom-0 right-0 w-24 h-24 bg-[#E08544] hover:bg-[#ea8c49] rounded-tl-[48px] flex items-center justify-center text-white transition-all duration-300 pl-4 pt-4 shadow-xl active:scale-95 group/cart"
                        title="Sepete Ekle"
                      >
                        {/* Sepet + Artı İkonu */}
                        <div className="relative flex items-center justify-center">
                          <svg className="w-6 h-6" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.2" strokeLinecap="round" strokeLinejoin="round">
                            <path d="M6 2 3 6v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2V6l-3-4Z" />
                            <path d="M3 6h18" />
                            <path d="M16 10a4 4 0 0 1-8 0" />
                          </svg>
                          <span className="absolute -top-1 -right-2 text-xs font-black">+</span>
                        </div>
                      </button>
                    </div>

                  </div>
                );
              })}
            </div>
          </section>
        </div>
      </main>
    </div>
  );
}
