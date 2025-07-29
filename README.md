# 🤖 Aurelia Telegram Bot

**Aurelia** - Aeternus Partisi'nin akıllı AI asistanı. Ollama ile entegre çalışan, Telegram üzerinden hizmet veren yapay zeka botu.

## ✨ Özellikler

- 🤖 **Ollama Entegrasyonu**: Yerel AI modeli (Gemma3:12b) ile çalışır
- 💬 **Akıllı Konuşma**: Doğal dil işleme ve bağlamsal yanıtlar
- 🎭 **Karakter Kişiliği**: Kadınsı ses tonu ve sevimli kişilik
- 🎯 **Hedefli Yanıtlar**: Belirli chat ID'lerde çalışır
- 📝 **Alıntı Desteği**: Reply ve quote'lara otomatik yanıt
- 🎨 **Emoji Desteği**: Karakteristik emoji kullanımı
- ⚡ **Dinamik Token**: Soru tipine göre yanıt uzunluğu ayarlama

## 🚀 Kurulum

### Gereksinimler

- Python 3.8+
- Ollama (yerel kurulum)
- Telegram Bot Token
- Gemma3:12b modeli

### 1. Repository'yi Klonlayın

```bash
git clone https://github.com/Clyrex9/Aurelia.git
cd Aurelia
```

### 2. Gerekli Paketleri Yükleyin

```bash
pip install python-telegram-bot requests
```

### 3. Ollama'yı Kurun ve Modeli İndirin

```bash
# Ollama'yı kurun (https://ollama.ai)
ollama pull gemma3:12b
```

### 4. Bot Token'ını Ayarlayın

`aurelia_bot.py` dosyasında bot token'ınızı güncelleyin:

```python
BOT_TOKEN = "YOUR_BOT_TOKEN_HERE"
```

### 5. Chat ID'yi Ayarlayın

Hedef chat ID'yi güncelleyin:

```python
ALLOWED_CHAT_ID = -1001899108628  # Sizin chat ID'niz
```

## 🎮 Kullanım

### Bot'u Başlatın

```bash
python aurelia_bot.py
```

### Ollama'yı Başlatın

```bash
# Bellek ayarları ile Ollama'yı başlatın
OLLAMA_MAX_LOADED_MODELS=1 OLLAMA_MAX_VRAM=16GB ollama serve
```

## 💬 Bot Komutları

- `/start` - Bot'u başlatır
- `/status` - Ollama bağlantı durumunu kontrol eder
- `/help` - Yardım menüsünü gösterir

## 🎭 Aurelia'nın Kişiliği

Aurelia, Aeternus Partisi'nin akıllı asistanıdır:

- **Ses Tonu**: Kadınsı ve sevimli
- **Konuşma Tarzı**: Bazen alaycı ama sevimli
- **Bilgi Alanı**: Parti üyeleri, oyun stratejileri, tarih
- **Özellikler**: Emoji kullanır, kendi kendine şarkı söyler

## 📊 Token Yönetimi

Bot, soru tipine göre yanıt uzunluğunu ayarlar:

- **Çok Kısa**: 120 token (selam, naber vb.)
- **Kısa**: 150 token (kim, ne vb.)
- **Uzun**: 400 token (detaylı analiz)
- **Rastgele**: %65 kısa, %35 uzun

## 🔧 Yapılandırma

### Sistem Belleği

Gemma3:12b modeli için minimum 6GB RAM gereklidir:

```bash
OLLAMA_MAX_VRAM=16GB ollama serve
```

### Timeout Ayarları

Büyük model için timeout değerleri:

- **Ollama İsteği**: 120 saniye
- **Bağlantı Testi**: 60 saniye

## 🐛 Sorun Giderme

### Yaygın Hatalar

1. **"model requires more system memory"**
   - Ollama'yı daha fazla RAM ile başlatın
   - `OLLAMA_MAX_VRAM=16GB` kullanın

2. **"Read timed out"**
   - Timeout değerlerini artırın
   - Model yükleme süresini bekleyin

3. **"Message to be replied not found"**
   - Bot yeniden başlatılmalı
   - Chat geçmişi temizlenmeli

## 📁 Dosya Yapısı

```
Aurelia/
├── aurelia_bot.py    # Ana bot dosyası
├── README.md         # Bu dosya
└── requirements.txt  # Gerekli paketler
```

## 🤝 Katkıda Bulunma

1. Fork yapın
2. Feature branch oluşturun (`git checkout -b feature/AmazingFeature`)
3. Commit yapın (`git commit -m 'Add some AmazingFeature'`)
4. Push yapın (`git push origin feature/AmazingFeature`)
5. Pull Request açın

## 📄 Lisans

Bu proje [MIT License](LICENSE) altında lisanslanmıştır.

## 👨‍💻 Geliştirici

**Clyrex** - Aeternus Partisi Lideri

- GitHub: [@Clyrex9](https://github.com/Clyrex9)
- Telegram: Aeternus Partisi

## ⭐ Yıldız Verin

Bu projeyi beğendiyseniz yıldız vermeyi unutmayın! ⭐

---

**Aurelia** - Aeternus Partisi'nin Akıllı Asistanı 🤖✨ 