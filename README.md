# 🧥 Atelier Sanal Kabin (Virtual Fitting Room)

Next.js, Tailwind CSS ve Framer Motion ile geliştirilmiş, **Data Mapping** mantığıyla çalışan yüksek performanslı Sanal Kabin (Fitting Room) e-ticaret bileşeni.

Canlı AI görsel üretim modellerinin 8-10 saniyelik gecikmesini ortadan kaldırarak; stüdyoda çekilmiş hazır model fotoğrafları ve şeffaf PNG dekupe mikro-animasyonları ile **<15ms anlık önizleme** sunar.

---

## ✨ Özellikler

- **Şeffaf PNG Uçuş Mikro-Animasyonu (FLIP):** Ürün kartındaki askı simgesine tıklandığında ürün arka plansız olarak yerinden fırlar, kavis çizerek havada büyükten küçülür ve mankenin göğüs hizasına yerleşir.
- **Pürüzsüz Model Değişimi:** Eski kıyafetten yeni modele geçerken sinematik `blur(8px)` + ölçeklenme + cross-dissolve geçişi.
- **Kabin Askılığı (Fitting Room Rack):** Sol panelin altında denenen parçaları saklayan mini askılık; tıklamayla anında kıyafet değiştirme veya askıdan kaldırma.
- **Karanlık Mod (Dark Mode Luxury UI):** Koyu karbon zemin, yarı saydam cam efektleri, organik terracotta çeyrek-daire sepet butonu ve mikro-etkileşimler.

---

## 🚀 Canlı Demo (GitHub Pages)

Bu depo doğrudan **GitHub Pages** üzerinde `index.html` olarak çalışacak şekilde hazırlanmıştır.

```
https://<kullanici-adiniz>.github.io/<depo-adiniz>/
```

---

## 🛠️ Yerel Geliştirme (Next.js)

```bash
# Bağımlılıkları yükleyin
npm install

# Geliştirme sunucusunu başlatın
npm run dev
```

Tarayıcınızda `http://localhost:3000` adresine giderek Next.js sürümünü test edebilirsiniz.
