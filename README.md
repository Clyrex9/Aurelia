# 🤖 Aurelia Telegram Bot

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Telegram](https://img.shields.io/badge/Telegram-Bot-blue.svg)](https://core.telegram.org/bots)
[![Ollama](https://img.shields.io/badge/Ollama-AI%20Model-green.svg)](https://ollama.ai/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Stars](https://img.shields.io/github/stars/Clyrex9/Aurelia?style=social)](https://github.com/Clyrex9/Aurelia)

> **Aurelia** - Akıllı AI asistanı. Ollama ile entegre çalışan, Telegram üzerinden hizmet veren yapay zeka botu.

<div align="center">
  <img src="https://img.shields.io/badge/AI%20Assistant-Elite%20Bot-red?style=for-the-badge&logo=telegram" alt="AI Assistant">
  <br>
  <em>🎭 Kadınsı AI Asistan • 🧠 Gemma3:12b Modeli • ⚡ Gerçek Zamanlı Yanıt</em>
</div>

---

## ✨ Özellikler

<table>
<tr>
<td width="50%">

### 🤖 AI Entegrasyonu
- **Ollama Entegrasyonu**: Yerel AI modeli (Gemma3:12b) ile çalışır
- **Akıllı Konuşma**: Doğal dil işleme ve bağlamsal yanıtlar
- **Dinamik Token**: Soru tipine göre yanıt uzunluğu ayarlama

</td>
<td width="50%">

### 🎭 Karakter Kişiliği
- **Kadınsı Ses Tonu**: Sevimli ve zarif konuşma tarzı
- **Emoji Desteği**: Karakteristik emoji kullanımı
- **Özel Diyaloglar**: Kendi kendine şarkı söyleme, dans etme

</td>
</tr>
<tr>
<td width="50%">

### 🎯 Hedefli Çalışma
- **Belirli Chat ID**: Sadece izin verilen gruplarda çalışır
- **Alıntı Desteği**: Reply ve quote'lara otomatik yanıt
- **Mention Sistemi**: @Aurelia ile çağırma

</td>
<td width="50%">

### ⚡ Performans
- **Hızlı Yanıt**: Optimize edilmiş token yönetimi
- **Bellek Optimizasyonu**: 16GB VRAM desteği
- **Timeout Yönetimi**: Büyük modeller için özel ayarlar

</td>
</tr>
</table>

---

## 🚀 Hızlı Başlangıç

### 📋 Gereksinimler

- ✅ Python 3.8+
- ✅ Ollama (yerel kurulum)
- ✅ Telegram Bot Token
- ✅ Gemma3:12b modeli
- ✅ Minimum 6GB RAM

### 🔧 Kurulum Adımları

<details>
<summary><b>1️⃣ Repository'yi Klonlayın</b></summary>

```bash
git clone https://github.com/Clyrex9/Aurelia.git
cd Aurelia
```

</details>

<details>
<summary><b>2️⃣ Gerekli Paketleri Yükleyin</b></summary>

```bash
pip install -r requirements.txt
```

</details>

<details>
<summary><b>3️⃣ Ollama'yı Kurun ve Modeli İndirin</b></summary>

```bash
# Ollama'yı kurun (https://ollama.ai)
ollama pull gemma3:12b
```

</details>

<details>
<summary><b>4️⃣ Bot Token'ını Ayarlayın</b></summary>

`aurelia_bot.py` dosyasında bot token'ınızı güncelleyin:

```python
TELEGRAM_BOT_TOKEN = "YOUR_BOT_TOKEN_HERE"
```

</details>

<details>
<summary><b>5️⃣ Chat ID'yi Ayarlayın</b></summary>

Hedef chat ID'yi güncelleyin:

```python
ALLOWED_CHAT_ID = YOUR_CHAT_ID_HERE  # Sizin chat ID'niz
```

</details>

---

## 🎮 Kullanım

### 🚀 Bot'u Başlatın

```bash
python aurelia_bot.py
```

### 🧠 Ollama'yı Başlatın

```bash
# Bellek ayarları ile Ollama'yı başlatın
OLLAMA_MAX_LOADED_MODELS=1 OLLAMA_MAX_VRAM=16GB ollama serve
```

### 💬 Bot Komutları

| Komut | Açıklama |
|-------|----------|
| `/start` | Bot'u başlatır |
| `/status` | Ollama bağlantı durumunu kontrol eder |
| `/help` | Yardım menüsünü gösterir |

---

## 🎭 Aurelia'nın Kişiliği

<div align="center">
  <img src="https://img.shields.io/badge/Personality-Feminine%20AI-pink?style=for-the-badge" alt="Feminine AI">
</div>

### 👑 Karakter Özellikleri

- **🎭 Ses Tonu**: Kadınsı ve sevimli
- **🗣️ Konuşma Tarzı**: Bazen alaycı ama sevimli
- **🧠 Bilgi Alanı**: Genel konular, oyun stratejileri, tarih
- **✨ Özellikler**: Emoji kullanır, kendi kendine şarkı söyler

### 🏛️ Özelleştirilebilir İçerik

Bot, kendi ihtiyaçlarınıza göre özelleştirilebilir:

- **Üye Bilgileri**: Kendi üyelerinizi ekleyebilirsiniz
- **Tarih Bilgileri**: Kendi tarihsel olaylarınızı ekleyebilirsiniz
- **Karakter Kişiliği**: Bot'un kişiliğini değiştirebilirsiniz

---

## 📊 Token Yönetimi

Bot, soru tipine göre yanıt uzunluğunu akıllıca ayarlar:

| Soru Tipi | Token Sayısı | Kullanım |
|------------|---------------|----------|
| **Çok Kısa** | 120 token | Selam, naber vb. |
| **Kısa** | 150 token | Kim, ne vb. |
| **Uzun** | 400 token | Detaylı analiz |
| **Rastgele** | %65 kısa, %35 uzun | Dinamik ayarlama |

---

## 🔧 Yapılandırma

### 💾 Sistem Belleği

Gemma3:12b modeli için minimum 6GB RAM gereklidir:

```bash
OLLAMA_MAX_VRAM=16GB ollama serve
```

### ⏱️ Timeout Ayarları

Büyük model için optimize edilmiş timeout değerleri:

```python
# Ollama İsteği: 120 saniye
# Bağlantı Testi: 60 saniye
```

---

## 🐛 Sorun Giderme

### ❌ Yaygın Hatalar ve Çözümleri

<details>
<summary><b>🔴 "model requires more system memory"</b></summary>

```bash
# Çözüm: Ollama'yı daha fazla RAM ile başlatın
OLLAMA_MAX_VRAM=16GB ollama serve
```

</details>

<details>
<summary><b>🔴 "Read timed out"</b></summary>

```bash
# Çözüm: Timeout değerlerini artırın
# Model yükleme süresini bekleyin
```

</details>

<details>
<summary><b>🔴 "Message to be replied not found"</b></summary>

```bash
# Çözüm: Bot yeniden başlatılmalı
# Chat geçmişi temizlenmeli
```

</details>

---

## 📁 Dosya Yapısı

```
Aurelia/
├── 📄 aurelia_bot.py    # Ana bot dosyası
├── 📖 README.md         # Bu dosya
└── 📦 requirements.txt  # Gerekli paketler
```

---

## 🤝 Katkıda Bulunma

1. 🍴 Fork yapın
2. 🌿 Feature branch oluşturun (`git checkout -b feature/AmazingFeature`)
3. 💾 Commit yapın (`git commit -m 'Add some AmazingFeature'`)
4. 🚀 Push yapın (`git push origin feature/AmazingFeature`)
5. 📝 Pull Request açın

---

## 📄 Lisans

Bu proje [MIT License](LICENSE) altında lisanslanmıştır.

---

## 👨‍💻 Geliştirici

<div align="center">
  <img src="https://img.shields.io/badge/Developer-Clyrex-purple?style=for-the-badge" alt="Clyrex">
  <br>
  <strong>Clyrex</strong> - Proje Geliştiricisi
</div>

- 🌐 GitHub: [@Clyrex9](https://github.com/Clyrex9)

---

## ⭐ Yıldız Verin

Bu projeyi beğendiyseniz yıldız vermeyi unutmayın! ⭐

<div align="center">
  <a href="https://github.com/Clyrex9/Aurelia/stargazers">
    <img src="https://img.shields.io/github/stars/Clyrex9/Aurelia?style=for-the-badge&logo=github" alt="Stars">
  </a>
  <a href="https://github.com/Clyrex9/Aurelia/network">
    <img src="https://img.shields.io/github/forks/Clyrex9/Aurelia?style=for-the-badge&logo=github" alt="Forks">
  </a>
  <a href="https://github.com/Clyrex9/Aurelia/issues">
    <img src="https://img.shields.io/github/issues/Clyrex9/Aurelia?style=for-the-badge&logo=github" alt="Issues">
  </a>
</div>

---

<div align="center">
  <h3>🤖 Aurelia - Akıllı AI Asistanı</h3>
  <em>🎭 Kadınsı AI • 🧠 Gemma3:12b • ⚡ Gerçek Zamanlı</em>
</div> 