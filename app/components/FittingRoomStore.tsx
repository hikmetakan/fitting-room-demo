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
  oldPrice: number;
  currency: string;
  rating: number;
  color: string;
  card_image: string;       // Şeffaf dekupe görsel
  model_image_url: string;  // Modelin o kıyafeti giydiği fotoğraf
}

interface FlyingItemState {
  product: Product;
  startRect: { left: number; top: number; width: number; height: number };
  targetRect: { left: number; top: number; width: number; height: number };
}

// --------------------------------------------------------------------------
// 2. Ürün Kataloğu & Data Mapping
// --------------------------------------------------------------------------
const BASE_MANNEQUIN_IMAGE = '/images/base-mannequin.jpg';

export const PRODUCTS: Product[] = [
  {
    id: 'jacket-green',
    name: 'Army Green Puffer Jacket',
    category: 'Şişme Mont',
    price: 189,
    oldPrice: 229,
    currency: '$',
    rating: 4.3,
    color: 'Asker Yeşili',
    card_image: '/images/green-jacket.png',
    model_image_url: '/images/model-green-vest.jpg',
  },
  {
    id: 'vest-brown',
    name: 'Kapitoneli Şişme Yelek',
    category: 'Yelek',
    price: 189,
    oldPrice: 229,
    currency: '$',
    rating: 4.8,
    color: 'Kahverengi',
    card_image: '/images/brown-vest.png',
    model_image_url: '/images/model-brown-vest.jpg',
  },
  {
    id: 'vest-black',
    name: 'Mat Nappa Kapitoneli Yelek',
    category: 'Yelek',
    price: 199,
    oldPrice: 239,
    currency: '$',
    rating: 4.9,
    color: 'Siyah',
    card_image: '/images/black-vest.png',
    model_image_url: '/images/model-black-vest.jpg',
  },
];

// --------------------------------------------------------------------------
// 3. Ana Sanal Kabin Bileşeni (Mobil Uyumlu & Minimal Tasarım)
// --------------------------------------------------------------------------
export default function FittingRoomStore() {
  const [activeItem, setActiveItem] = useState<Product | null>(PRODUCTS[0]);
  const [fittingRoomItems, setFittingRoomItems] = useState<Product[]>([PRODUCTS[0]]);
  const [favorites, setFavorites] = useState<Record<string, boolean>>({});
  const [flyingItem, setFlyingItem] = useState<FlyingItemState | null>(null);
  const [toastMessage, setToastMessage] = useState<string | null>(null);

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

  const handleHangerClick = (product: Product) => {
    const cardImgEl = document.getElementById(`product-img-${product.id}`);
    const mannequinEl = mannequinRef.current;

    if (cardImgEl && mannequinEl) {
      const startRect = cardImgEl.getBoundingClientRect();
      const targetRect = mannequinEl.getBoundingClientRect();

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
      setActiveItem(product);
    }

    setFittingRoomItems((prev) => {
      if (!prev.some((p) => p.id === product.id)) {
        return [...prev, product];
      }
      return prev;
    });
  };

  const handleFlightComplete = () => {
    if (flyingItem) {
      setActiveItem(flyingItem.product);
      showToast(`"${flyingItem.product.name}" model üzerine giyildi.`);
      setFlyingItem(null);
    }
  };

  const handleRemoveFromRack = (productId: string, e: React.MouseEvent) => {
    e.stopPropagation();
    const updated = fittingRoomItems.filter((p) => p.id !== productId);
    setFittingRoomItems(updated);

    if (activeItem?.id === productId) {
      setActiveItem(updated.length > 0 ? updated[updated.length - 1] : null);
    }
  };

  return (
    <div className="min-h-screen bg-[#0D0C12] text-zinc-100 selection:bg-amber-500/30 selection:text-amber-200 p-3 sm:p-5 lg:p-8">
      
      {/* Toast Notification */}
      <AnimatePresence>
        {toastMessage && (
          <motion.div
            initial={{ opacity: 0, y: -20, scale: 0.95 }}
            animate={{ opacity: 1, y: 0, scale: 1 }}
            exit={{ opacity: 0, y: -20, scale: 0.95 }}
            className="fixed top-5 right-4 z-50 bg-[#16151E] border border-[#E08544]/60 text-amber-200 text-xs px-3.5 py-2 rounded-xl shadow-2xl shadow-black/80 flex items-center gap-2"
          >
            <span className="h-2 w-2 rounded-full bg-[#E08544] animate-ping" />
            {toastMessage}
          </motion.div>
        )}
      </AnimatePresence>

      {/* ================================================================
          UÇAN ŞEFFAF PNG KIYAFET ANİMASYONU
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
                flyingItem.startRect.left - 30,
                flyingItem.targetRect.left + flyingItem.targetRect.width / 2 - (flyingItem.startRect.width * 0.40) / 2,
              ],
              top: [
                flyingItem.startRect.top,
                flyingItem.startRect.top - 40,
                flyingItem.targetRect.top + flyingItem.targetRect.height * 0.35 - (flyingItem.startRect.height * 0.40) / 2,
              ],
              scale: [1, 1.2, 0.40],
              rotate: [0, -6, 2],
              opacity: [1, 1, 0.95, 0],
            }}
            transition={{
              duration: 0.75,
              times: [0, 0.25, 1],
              ease: [0.22, 1, 0.36, 1],
            }}
            onAnimationComplete={handleFlightComplete}
            className="flex items-center justify-center filter drop-shadow-[0_20px_30px_rgba(224,133,68,0.55)]"
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

      {/* Üst Başlık Barı */}
      <header className="max-w-7xl mx-auto mb-4 sm:mb-6">
        <div className="rounded-2xl border border-zinc-800/80 bg-[#15141B]/90 backdrop-blur-xl px-3.5 py-2.5 sm:px-4 sm:py-3 shadow-lg flex items-center justify-between gap-3">
          <div className="flex items-center gap-2.5">
            <div className="h-8 w-8 rounded-xl bg-gradient-to-tr from-[#E08544] to-amber-300 flex items-center justify-center text-black font-black text-sm shadow-md shadow-[#E08544]/20">
              V
            </div>
            <div>
              <div className="flex items-center gap-1.5">
                <span className="text-xs sm:text-sm font-bold tracking-wider uppercase text-zinc-100">Atelier Studio</span>
                <span className="text-[10px] px-1.5 py-0.2 rounded-full bg-emerald-500/10 text-emerald-400 border border-emerald-500/20 font-mono">MOBİL UYUMLU</span>
              </div>
              <p className="text-[11px] text-zinc-400 hidden sm:block">Şeffaf PNG Uçuşu &amp; Canlı Model Eşlemesi</p>
            </div>
          </div>

          <div className="flex items-center gap-2">
            <button
              onClick={() => {
                setActiveItem(null);
                showToast('Kıyafet çıkarıldı, baz mankene dönüldü.');
              }}
              className="px-2.5 py-1.5 rounded-xl bg-zinc-800/90 hover:bg-zinc-700 text-zinc-300 hover:text-white transition-all text-[11px] sm:text-xs font-medium border border-zinc-700/60 flex items-center gap-1"
            >
              <svg className="w-3.5 h-3.5 text-zinc-400" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2"><path d="M3 12a9 9 0 0 1 9-9 9.75 9.75 0 0 1 6.74 2.74L21 8"/><path d="M21 3v5h-5"/></svg>
              <span className="hidden sm:inline">Mankeni Sıfırla</span>
              <span className="sm:hidden">Sıfırla</span>
            </button>
          </div>
        </div>
      </header>

      {/* Ana Çalışma Alanı: Mobilde Kompakt Model Üstte, 2 Kolon Minimal Kartlar Altta */}
      <main className="max-w-7xl mx-auto grid grid-cols-1 lg:grid-cols-12 gap-4 sm:gap-6 items-start">
        
        {/* ================================================================
            SOL PANEL: SANAL KABİN (MOBİLDE DERLİ TOPLU VE KOMPAKT)
           ================================================================ */}
        <aside className="lg:col-span-5 lg:sticky lg:top-6 space-y-3">
          <div className="rounded-2xl sm:rounded-3xl border border-zinc-800/90 bg-[#15141B]/95 backdrop-blur-2xl p-3 sm:p-4 shadow-2xl relative overflow-hidden">
            
            {/* Başlık */}
            <div className="flex items-center justify-between pb-2.5 border-b border-zinc-800/70">
              <div className="flex items-center gap-2">
                <div className="h-6 w-6 rounded-lg bg-[#E08544]/15 border border-[#E08544]/30 flex items-center justify-center">
                  <svg className="w-3.5 h-3.5 text-[#E08544]" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                    <path d="M12 3a3 3 0 0 0-3 3c0 1.25.75 2 1.5 2.5L3 17h18l-7.5-8.5C14.25 8 15 7.25 15 6a3 3 0 0 0-3-3z" />
                  </svg>
                </div>
                <h2 className="text-[11px] sm:text-xs font-bold tracking-wider text-zinc-100 uppercase">
                  Sanal Kabin Önizleme
                </h2>
              </div>

              <div className="flex items-center gap-2">
                <span className="text-[10px] sm:text-[11px] px-2 py-0.5 rounded-full bg-emerald-500/10 text-emerald-400 font-mono flex items-center gap-1 border border-emerald-500/20">
                  <span className="h-1.5 w-1.5 rounded-full bg-emerald-400 animate-pulse" />
                  {activeItem ? activeItem.color : 'Boş'}
                </span>
                {activeItem && (
                  <button
                    onClick={() => setActiveItem(null)}
                    className="text-[11px] text-zinc-400 hover:text-amber-300 transition-colors px-1.5 py-0.5 rounded bg-zinc-800/80"
                  >
                    Çıkar
                  </button>
                )}
              </div>
            </div>

            {/* Manken Önizleme Çerçevesi */}
            <div
              ref={mannequinRef}
              className="relative mt-2.5 aspect-[4/5] sm:aspect-[3/4] lg:aspect-[9/16] max-h-[310px] sm:max-h-[380px] lg:max-h-[560px] w-full rounded-xl sm:rounded-2xl overflow-hidden bg-[#07060A] border border-zinc-800/80 shadow-inner flex items-center justify-center"
            >
              <AnimatePresence mode="wait">
                <motion.div
                  key={activeItem ? activeItem.id : 'base-mannequin'}
                  initial={{ opacity: 0, scale: 0.98, filter: 'blur(8px)' }}
                  animate={{ opacity: 1, scale: 1, filter: 'blur(0px)' }}
                  exit={{ opacity: 0, scale: 1.02, filter: 'blur(6px)' }}
                  transition={{ duration: 0.45, ease: [0.22, 1, 0.36, 1] }}
                  className="absolute inset-0 w-full h-full"
                >
                  {/* eslint-disable-next-line @next/next/no-img-element */}
                  <img
                    src={activeItem ? activeItem.model_image_url : BASE_MANNEQUIN_IMAGE}
                    alt={activeItem ? activeItem.name : 'Baz Manken'}
                    className="w-full h-full object-cover object-top"
                  />
                  <div className="absolute inset-0 bg-gradient-to-t from-black/85 via-black/10 to-transparent pointer-events-none" />
                </motion.div>
              </AnimatePresence>

              {/* Model Üzerindeki Aktif Parça Rozeti */}
              {activeItem ? (
                <div className="absolute bottom-2.5 left-2.5 right-2.5 p-2.5 sm:p-3 rounded-xl sm:rounded-2xl bg-[#16151E]/95 border border-zinc-700/60 backdrop-blur-md flex items-center justify-between">
                  <div>
                    <span className="text-[9px] sm:text-[10px] tracking-wider uppercase text-[#E08544] font-mono flex items-center gap-1">
                      <span className="h-1 w-1 rounded-full bg-[#E08544] animate-ping" />
                      Model Üzerinde Giyili
                    </span>
                    <p className="text-[11px] sm:text-xs font-bold text-zinc-100 line-clamp-1 mt-0.5">
                      {activeItem.name} ({activeItem.color})
                    </p>
                    <p className="text-xs sm:text-sm text-[#E08544] font-bold font-mono">
                      {activeItem.currency}{activeItem.price} <span className="text-zinc-500 line-through text-[10px] font-normal ml-1">{activeItem.currency}{activeItem.oldPrice}</span>
                    </p>
                  </div>
                  <button
                    onClick={() => showToast(`"${activeItem.name}" sepete eklendi!`)}
                    className="px-2.5 py-1.5 sm:px-3 sm:py-2 rounded-lg sm:rounded-xl bg-[#E08544] hover:bg-[#eb8c49] text-white text-[11px] sm:text-xs font-bold transition-transform active:scale-95 shadow-md shadow-[#E08544]/30"
                  >
                    Sepete Ekle
                  </button>
                </div>
              ) : (
                <div className="absolute bottom-3 left-3 right-3 text-center">
                  <span className="text-[11px] text-zinc-400 bg-black/80 px-3 py-1 rounded-full border border-zinc-800">
                    Karttaki askı simgesine basarak mankene giydirin
                  </span>
                </div>
              )}
            </div>

            {/* Kabin Askılığı */}
            <div className="mt-2.5 pt-2 border-t border-zinc-800/70">
              <div className="flex items-center justify-between mb-1.5">
                <span className="text-[11px] font-medium text-zinc-400">
                  Kabin Askılığı ({fittingRoomItems.length})
                </span>
                <span className="text-[10px] text-zinc-500">Giydirmek için tıkla</span>
              </div>

              <div className="flex gap-2 overflow-x-auto pb-1 items-center">
                {fittingRoomItems.map((item) => {
                  const isActive = activeItem?.id === item.id;
                  return (
                    <div
                      key={item.id}
                      onClick={() => setActiveItem(item)}
                      className={`relative group flex-shrink-0 w-14 cursor-pointer rounded-lg border p-1 transition-all ${
                        isActive
                          ? 'border-[#E08544] bg-[#E08544]/10 shadow-sm shadow-[#E08544]/20'
                          : 'border-zinc-800 bg-zinc-900/60 hover:border-zinc-700'
                      }`}
                    >
                      <div className="relative aspect-square w-full rounded overflow-hidden bg-zinc-950 mb-0.5 flex items-center justify-center">
                        {/* eslint-disable-next-line @next/next/no-img-element */}
                        <img
                          src={item.card_image}
                          alt={item.name}
                          className="w-full h-full object-contain p-0.5"
                        />
                        <button
                          onClick={(e) => handleRemoveFromRack(item.id, e)}
                          className="absolute top-0.5 right-0.5 h-3.5 w-3.5 rounded-full bg-black/85 hover:bg-red-500 text-zinc-300 hover:text-white flex items-center justify-center text-[8px] opacity-0 group-hover:opacity-100 transition-opacity"
                        >
                          ✕
                        </button>
                      </div>
                      <p className="text-[9px] font-semibold text-zinc-200 truncate">
                        {item.color}
                      </p>
                    </div>
                  );
                })}
              </div>
            </div>
          </div>
        </aside>

        {/* ================================================================
            SAĞ PANEL: MOBİLDE 2 KOLONLU MİNİMAL ÜRÜN KARTLARI
           ================================================================ */}
        <section className="lg:col-span-7 space-y-3 sm:space-y-4">
          <div className="flex items-center justify-between pb-1.5 border-b border-zinc-800/60">
            <div>
              <h2 className="text-sm sm:text-base font-bold tracking-tight text-zinc-100">Koleksiyon</h2>
              <p className="text-[11px] text-zinc-400">
                Modelde denemek için <span className="text-[#E08544] font-semibold">turuncu askı</span> simgesine tıklayın.
              </p>
            </div>
            <span className="text-[11px] font-mono text-zinc-500">{PRODUCTS.length} Ürün</span>
          </div>

          {/* MOBİLDE 2 KOLONLU GRID (grid-cols-2) */}
          <div className="grid grid-cols-2 gap-2.5 sm:gap-3.5 lg:grid-cols-2">
            {PRODUCTS.map((product) => {
              const isCurrentActive = activeItem?.id === product.id;
              const isFav = !!favorites[product.id];

              return (
                /* GÖNDERİLEN GÖRSELE SADIK KALINAN MİNİMAL ÜRÜN KARTI */
                <div
                  key={product.id}
                  className={`relative rounded-2xl bg-[#17161D] border border-zinc-800/80 p-2.5 sm:p-3.5 shadow-lg overflow-hidden flex flex-col justify-between group transition-all duration-300 hover:border-zinc-700 ${
                    isCurrentActive ? 'ring-1 ring-[#E08544]/50 shadow-[#E08544]/10' : ''
                  }`}
                >
                  <div>
                    {/* Kart Üstü: Sol Kalp ve Turuncu Askı, Sağ Puan Rozeti */}
                    <div className="flex items-start justify-between z-10">
                      
                      <div className="flex flex-col gap-1.5">
                        {/* Kalp Butonu */}
                        <button
                          onClick={(e) => toggleFavorite(product.id, e)}
                          className={`h-7 w-7 sm:h-8 sm:w-8 rounded-full flex items-center justify-center transition-all ${
                            isFav
                              ? 'bg-rose-500/20 text-rose-400 border border-rose-500/40'
                              : 'bg-[#2B2A34] hover:bg-[#383742] text-zinc-300'
                          }`}
                        >
                          <svg
                            className={`w-3.5 h-3.5 ${isFav ? 'fill-current' : 'fill-none'}`}
                            viewBox="0 0 24 24"
                            stroke="currentColor"
                            strokeWidth="2"
                          >
                            <path d="M20.84 4.61a5.5 5.5 0 0 0-7.78 0L12 5.67l-1.06-1.06a5.5 5.5 0 0 0-7.78 7.78l1.06 1.06L12 21.23l7.78-7.78 1.06-1.06a5.5 5.5 0 0 0 0-7.78z" />
                          </svg>
                        </button>

                        {/* Turuncu Askı Butonu (Fitting Room Trigger) */}
                        <button
                          onClick={() => handleHangerClick(product)}
                          className={`h-7 w-7 sm:h-8 sm:w-8 rounded-full flex items-center justify-center transition-all duration-300 active:scale-90 ${
                            isCurrentActive
                              ? 'bg-[#E08544] text-white shadow-md shadow-[#E08544]/40 ring-2 ring-white/30 scale-105'
                              : 'bg-[#E08544] hover:brightness-110 text-white shadow-sm shadow-[#E08544]/25'
                          }`}
                          title="Askıya Al / Modelde Dene"
                        >
                          <svg className="w-3.5 h-3.5" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.2">
                            <path d="M12 3a3 3 0 0 0-3 3c0 1.25.75 2 1.5 2.5L3 17h18l-7.5-8.5C14.25 8 15 7.25 15 6a3 3 0 0 0-3-3z" />
                          </svg>
                        </button>
                      </div>

                      {/* Sağ Üst: Minimal Yıldız Rozeti (★ 4.3) */}
                      <div className="flex items-center gap-1 px-2 py-0.5 rounded-full bg-[#272630] border border-zinc-700/40 text-[10px] sm:text-xs font-semibold text-zinc-200">
                        <span className="text-[#FBBF24]">★</span>
                        <span>{product.rating.toFixed(1)}</span>
                      </div>
                    </div>

                    {/* Kart Ortası: Dekupe Şeffaf Ürün Görseli (Kompakt Yükseklik) */}
                    <div className="relative my-1 sm:my-2 h-24 sm:h-32 md:h-36 w-full flex items-center justify-center">
                      {/* eslint-disable-next-line @next/next/no-img-element */}
                      <img
                        id={`product-img-${product.id}`}
                        src={product.card_image}
                        alt={product.name}
                        className="max-h-full max-w-full object-contain filter drop-shadow-[0_12px_20px_rgba(0,0,0,0.65)] transition-transform duration-300 group-hover:scale-105"
                      />
                    </div>
                  </div>

                  {/* Kart Altı: Başlık, Fiyat Satırı ve Minimal Sepet+ Simgesi */}
                  <div className="mt-1 pt-1.5">
                    <h3 className="text-[11px] sm:text-xs text-zinc-400 font-normal truncate">
                      {product.name}
                    </h3>

                    <div className="flex items-center justify-between mt-0.5">
                      <div className="flex items-center gap-1 sm:gap-1.5 flex-wrap">
                        <span className="text-sm sm:text-base font-bold text-[#E08544] tracking-tight">
                          {product.currency}{product.price}
                        </span>
                        <span className="text-[10px] sm:text-xs text-zinc-500 line-through">
                          {product.currency}{product.oldPrice}
                        </span>
                        <span className="text-[9px] font-semibold bg-[#2E2827] text-[#E08544] px-1.5 py-0.2 rounded-full">
                          Sale
                        </span>
                      </div>

                      {/* Minimal Beyaz Sepet+ Simgesi */}
                      <button
                        onClick={() => showToast(`"${product.name}" sepete eklendi!`)}
                        className="p-1 text-zinc-300 hover:text-white active:scale-90 transition-transform"
                        title="Sepete Ekle"
                      >
                        <svg className="w-5 h-5" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.9" strokeLinecap="round" strokeLinejoin="round">
                          <path d="M6 2 3 6v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2V6l-3-4Z" />
                          <path d="M3 6h18" />
                          <path d="M16 10a4 4 0 0 1-8 0" />
                          <path d="M19 19v-4m-2 2h4" strokeWidth="2" />
                        </svg>
                      </button>
                    </div>
                  </div>

                </div>
              );
            })}
          </div>
        </section>
      </main>
    </div>
  );
}
