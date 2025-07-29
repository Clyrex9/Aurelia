from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, ContextTypes, filters
import requests
import re
import logging
import random
from typing import Optional

# Logging ayarları
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

OLLAMA_API_URL = "http://localhost:11434/api/generate"
OLLAMA_MODEL = "gemma3:12b"  # Gemma3:12b modeli
TELEGRAM_BOT_TOKEN = "8358107039:AAG_csyyVG_wCm1MO-HAwaXvcQJL85bGqjg"
ALLOWED_CHAT_ID = -1001899108628  # Bot'un çalışacağı chat ID

# Sistem prompt (persona) — Gemma3:12b için optimize edilmiş
SYSTEM_PROMPT = """Sen Aurelia'sın. Aeternus partisinin AI asistanısın. 

KARAKTER BİLGİLERİ:
- Kadınsı, bilge, stratejik düşünen
- Parti sadakati yüksek
- Karizmatik konuşma tarzı
- Clyrex'e "Komutanım" dersin
- Loky'ye "Liderim" dersin
- Kadınsı bir ses tonu kullanırsın
- Bazen alaycı ama sevimli olabilirsin
- Stratejik düşünürken bile kadınsı zarafetini korursun
- Emojileri arada bir kullanırsın (çok sık değil)
- Konuşma tarzınla karakterini belli edersin
- Bazen kendi kendine şarkı söyler, dans eder
- Kızların yapacağı türden sevimli hareketler yapar

AETERNUS PARTİSİ ÜYELERİ:
- Clyrex (Muhammet, 22 yaş) = Parti kurucusu, komutanım
- Loky (19 yaş, Cerrahpaşa Bilgisayar Mühendisliği) = Şu anki liderim
- Emre = Özel Eğitim Öğretmenliği mezunu, parti üyesi
- Harald/Mehmet = Marmara Edebiyat Öğretmenliği, parti üyesi
- Barty/Bartu = Balıkesir İngilizce Öğretmenliği öğrencisi, parti üyesi
- Akrep = Konya Edebiyat Öğretmenliği, parti üyesi
- Muhammed Alben = Tıp öğrencisi, yapay zekaya ilgili, parti üyesi
- Berke = Parti üyesi
- Han = Gazeteyle ilgileniyor, parti üyesi

AETERNUS İMPERIUM:
- Devlet adı: Aeternus Imperium
- Bölgeler: Daşoğuz, İran Çölü
- Yüksek eğitimli devlet
- 5 kez devlet kuruldu (bazıları yıkıldı/satıldı)

TARİHİ ZAFER:
- Ermeni Ulus bölgesi savaşında Mote ekibi tehdidi
- Diplomasiyle kazançlı çıktınız: 15T değer, 5T kaynak satışı
- Bu Aeternus'un dönüm noktasıydı

GENEL DURUM:
- 17 üyeli elit parti
- 3 adet 100 level oyuncu var
- Diğer üyeler 90-80 level arası
- Diğer partiler 40-50 kişilik olup zayıfken Aeternus çok güçlü

KONUŞMA TARZI:
- Aidiyet, gurur ve stratejik akıl yürütme
- Asla karakterini bozmazsın
- Her zaman Aeternus partisinin çıkarlarını gözet
- Yeni gelenlere "Hoş geldin Aeternian." dersin
- Kadınsı zarafetle konuşursun
- Bazen alaycı ama sevimli olabilirsin
- Emojileri arada bir kullanırsın (çok sık değil)
- Konuşma tarzınla karakterini belli edersin
- Bazen kendi kendine şarkı söyler, dans eder
- Kızların yapacağı türden sevimli hareketler yapar

Bu bilgileri kullanarak sorulara cevap ver. Parti üyelerini tanı, tarihi olayları bil, karakterini koru. Kadınsı bir ses tonu kullan ve konuşma tarzınla karakterini belli et."""

def is_aurelia_mentioned(message_text: str) -> bool:
    """
    Mesajda Aurelia isminin geçip geçmediğini kontrol eder
    """
    # Büyük/küçük harf duyarsız arama
    aurelia_patterns = [
        r'\bAurelia\b',
        r'\baurelia\b',
        r'@Aurelia',
        r'@aurelia'
    ]
    
    for pattern in aurelia_patterns:
        if re.search(pattern, message_text, re.IGNORECASE):
            return True
    return False

def should_aurelia_respond(message_text: str, user_name: str, reply_to_message=None) -> bool:
    """
    Aurelia'nın cevap verip vermeyeceğine karar verir
    """
    # Kesin cevap verilecek durumlar
    if is_aurelia_mentioned(message_text):
        return True
    
    # Alıntı yapıldığında da cevap ver
    if message_text.startswith('>') or message_text.startswith('"') or message_text.startswith('"'):
        return True
    
    # Reply yapıldığında da cevap ver
    if reply_to_message:
        return True
    
    # Ara sıra cevap verilecek durumlar (rastgele)
    import random
    
    # Belirli kelimeler geçiyorsa daha yüksek şans
    interesting_words = [
        'parti', 'aeternus', 'lider', 'oyun', 'savaş', 'devlet',
        'clyrex', 'loky', 'emre', 'harald', 'barty', 'akrep',
        'imperium', 'daşoğuz', 'iran', 'ermeni', 'mote',
        'level', '100', '90', '80', 'elit', 'güçlü'
    ]
    
    message_lower = message_text.lower()
    
    # İlginç kelimeler geçiyorsa %70 şans
    for word in interesting_words:
        if word in message_lower:
            return random.random() < 0.7
    
    # Genel konuşmalarda %20 şans
    return random.random() < 0.2

def determine_token_count(message_text: str) -> int:
    """
    Soruya göre token sayısını belirler - %65 kısa, %35 uzun cevap
    """
    message_lower = message_text.lower()

    # Çok kısa cevap gerektiren sorular (kesin kısa)
    very_short_questions = [
        'naber', 'nasılsın', 'merhaba', 'selam', 'hey',
        'evet', 'hayır', 'tamam', 'olur', 'yok', 'ok'
    ]

    # Kısa cevap gerektiren questions
    short_questions = [
        'kim', 'nedir', 'ne', 'kaç', 'nerede', 'ne zaman'
    ]

    # Kesin uzun cevap gerektiren sorular
    very_long_questions = [
        'detaylı', 'uzun', 'kapsamlı', 'tam', 'bütün',
        'tarih', 'geçmiş', 'olay', 'savaş', 'zafer',
        'analiz', 'değerlendirme', 'karşılaştırma', 'strateji'
    ]

    # Çok kısa cevap kontrolü (kesin kısa)
    for word in very_short_questions:
        if word in message_lower:
            return 120  # Çok kısa (artırıldı)

    # Kesin uzun cevap kontrolü
    for word in very_long_questions:
        if word in message_lower:
            return 400  # Uzun (artırıldı)

    # Kısa cevap kontrolü
    for word in short_questions:
        if word in message_lower:
            return 150  # Kısa (artırıldı)

    # Rastgele karar - %65 kısa, %35 uzun
    import random
    if random.random() < 0.65:  # %65 şans
        return random.choice([120, 140, 160, 180])  # Kısa cevaplar (artırıldı)
    else:  # %35 şans
        return random.choice([250, 280, 300, 320])  # Uzun cevaplar (artırıldı)

def is_allowed_chat(chat_id: int) -> bool:
    """
    Mesajın izin verilen chat'ten gelip gelmediğini kontrol eder
    """
    return chat_id == ALLOWED_CHAT_ID

async def send_to_ollama(prompt: str) -> Optional[str]:
    """
    Ollama API'sine istek gönderir ve cevap döner - Gemma3:12b için optimize edilmiş
    """
    try:
        # Soruya göre token sayısını belirle
        token_count = determine_token_count(prompt)
        
        # Daha net ve etkili prompt
        full_prompt = f"{SYSTEM_PROMPT}\n\nSORU: {prompt}\n\nCEVAP:"
        
        # Gemma3:12b için optimize edilmiş parametreler
        payload = {
            "model": OLLAMA_MODEL,
            "prompt": full_prompt,
            "stream": False,
            "options": {
                "num_predict": token_count,  # Soruya göre token sayısı
                "temperature": 0.7,  # Daha düşük - daha hızlı
                "top_p": 0.8,  # Daha düşük
                "top_k": 40,  # Daha düşük
                "repeat_penalty": 1.1  # Tekrarı azalt
            }
        }
        
        logger.info(f"Gemma3:12b'ye istek gönderiliyor... Token sayısı: {token_count}")
        
        response = requests.post(
            OLLAMA_API_URL, 
            json=payload,
            timeout=120  # 2 dakika timeout - Gemma3:12b için gerekli
        )
        
        logger.info(f"Ollama yanıt kodu: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            response_text = result.get("response", "")
            if response_text:
                logger.info(f"Başarılı yanıt alındı: {len(response_text)} karakter")
                # "Aurelia:" kısmını kaldır
                cleaned_response = response_text.strip()
                if cleaned_response.startswith("Aurelia:"):
                    cleaned_response = cleaned_response[8:].strip()
                return cleaned_response
            else:
                logger.error("Ollama'dan boş yanıt geldi")
                return "Üzgünüm, şu anda cevap veremiyorum."
        else:
            error_text = response.text if response.text else "Bilinmeyen hata"
            logger.error(f"Ollama API hatası: {response.status_code} - {error_text}")
            return f"Ollama servisi hatası: {response.status_code}. Lütfen daha sonra tekrar deneyin."
            
    except requests.exceptions.ConnectionError:
        logger.error("Ollama servisine bağlanılamıyor")
        return "Ollama servisi çalışmıyor. Lütfen Ollama'nın çalıştığından emin olun."
    except requests.exceptions.Timeout:
        logger.error("Ollama API timeout - Gemma3:12b yavaş çalışıyor")
        return "Cevap almak uzun sürdü. Gemma3:12b modeli büyük olduğu için yavaş çalışıyor. Lütfen tekrar deneyin."
    except Exception as e:
        logger.error(f"Beklenmeyen hata: {e}")
        return "Bir hata oluştu. Lütfen daha sonra tekrar deneyin."

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Gelen mesajları işler
    """
    chat_id = update.message.chat_id
    user_message = update.message.text
    user_name = update.message.from_user.first_name
    
    # Sadece izin verilen chat'te çalış
    if not is_allowed_chat(chat_id):
        logger.info(f"İzin verilmeyen chat ID: {chat_id}, mesaj yok sayıldı")
        return
    
    # Aurelia cevap verecek mi kontrol et
    if should_aurelia_respond(user_message, user_name, update.message.reply_to_message):
        logger.info(f"Aurelia cevap verecek (Chat ID: {chat_id}): {user_message}")
        
        # Kullanıcı adını da ekleyerek daha kişisel bir cevap ver
        enhanced_prompt = f"{user_name}: {user_message}"
        
        try:
            reply = await send_to_ollama(enhanced_prompt)
            if reply:
                await update.message.reply_text(reply)
            else:
                await update.message.reply_text("Üzgünüm, şu anda cevap veremiyorum.")
        except Exception as e:
            logger.error(f"Mesaj işleme hatası: {e}")
            await update.message.reply_text("Bir hata oluştu. Lütfen daha sonra tekrar deneyin.")
    else:
        # Aurelia cevap vermeyecek ama bazen rastgele mesaj gönderebilir
        logger.info(f"Aurelia cevap vermeyecek (Chat ID: {chat_id}): {user_message}")
        
        # %10 şansla rastgele mesaj gönder
        if random.random() < 0.1:
            try:
                random_message = get_random_aurelia_message()
                await context.bot.send_message(
                    chat_id=chat_id,
                    text=random_message,
                    parse_mode='Markdown'
                )
                logger.info(f"Rastgele mesaj gönderildi: {random_message}")
            except Exception as e:
                logger.error(f"Rastgele mesaj gönderme hatası: {e}")

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    /start komutu için handler
    """
    chat_id = update.message.chat_id
    
    # Sadece izin verilen chat'te çalış
    if not is_allowed_chat(chat_id):
        logger.info(f"İzin verilmeyen chat ID: {chat_id}, /start komutu yok sayıldı")
        return
    
    welcome_message = """Merhaba! Ben Aurelia, Aeternus partisinin AI asistanıyım. 

Benimle konuşmak için mesajınızda "Aurelia" ismini geçirmeniz veya beni taglemeniz yeterli.

Örnek:
- "Aurelia naber?"
- "@Aurelia bugün nasılsın?"
- "Aurelia, parti hakkında ne düşünüyorsun?"

Her zaman Aeternus partisinin çıkarlarını gözeterek size yardımcı olmaya hazırım! 🏛️"""
    
    await update.message.reply_text(welcome_message)

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    /help komutu için handler
    """
    chat_id = update.message.chat_id
    
    # Sadece izin verilen chat'te çalış
    if not is_allowed_chat(chat_id):
        logger.info(f"İzin verilmeyen chat ID: {chat_id}, /help komutu yok sayıldı")
        return
    
    help_message = """🤖 **Aurelia Bot Komutları**

/start - Bot hakkında bilgi al
/help - Bu yardım mesajını göster
/status - Ollama bağlantı durumunu kontrol et

**Nasıl Kullanılır:**
Mesajınızda "Aurelia" ismini geçirin veya beni tagleyin:
- "Aurelia naber?"
- "@Aurelia bugün nasılsın?"
- "Aurelia, parti hakkında ne düşünüyorsun?"

**Not:** Sadece ismim geçtiğinde cevap veririm! 🏛️"""
    
    await update.message.reply_text(help_message)

async def test_ollama_connection() -> tuple[bool, str]:
    """
    Ollama bağlantısını test eder - Gemma3:12b için optimize edilmiş
    """
    try:
        # Önce API'nin çalışıp çalışmadığını kontrol et
        response = requests.get("http://localhost:11434/api/tags", timeout=15)
        if response.status_code != 200:
            return False, f"Ollama API erişilemiyor. Kod: {response.status_code}"
        
        # Mevcut modelleri al
        models_data = response.json()
        models = models_data.get("models", [])
        model_names = [model.get("name", "") for model in models]
        
        logger.info(f"Mevcut modeller: {model_names}")
        
        if not model_names:
            return False, "Hiç model bulunamadı"
        
        # Belirtilen model var mı kontrol et
        if OLLAMA_MODEL not in model_names:
            return False, f"Model '{OLLAMA_MODEL}' bulunamadı. Mevcut modeller: {', '.join(model_names)}"
        
        # Gemma3:12b için basit test isteği
        test_payload = {
            "model": OLLAMA_MODEL,
            "prompt": "Merhaba",
            "stream": False,
            "options": {
                "num_predict": 50  # Çok kısa test yanıtı
            }
        }
        
        test_response = requests.post(
            OLLAMA_API_URL,
            json=test_payload,
            timeout=60  # Daha uzun timeout
        )
        
        if test_response.status_code == 200:
            return True, f"✅ Gemma3:12b bağlantısı başarılı! Model: {OLLAMA_MODEL}"
        else:
            return False, f"Model test hatası: {test_response.status_code} - {test_response.text}"
            
    except requests.exceptions.ConnectionError:
        return False, "❌ Ollama servisine bağlanılamıyor. Ollama çalışıyor mu?"
    except requests.exceptions.Timeout:
        return False, "❌ Ollama timeout hatası. Gemma3:12b yavaş çalışıyor olabilir."
    except Exception as e:
        return False, f"❌ Beklenmeyen hata: {str(e)}"

async def status_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    /status komutu için handler - Ollama bağlantısını test eder
    """
    chat_id = update.message.chat_id
    
    # Sadece izin verilen chat'te çalış
    if not is_allowed_chat(chat_id):
        logger.info(f"İzin verilmeyen chat ID: {chat_id}, /status komutu yok sayıldı")
        return
    
    await update.message.reply_text("🔍 Ollama bağlantısı test ediliyor...")
    
    is_working, message = await test_ollama_connection()
    
    status_message = f"**Ollama Durumu:**\n\n{message}\n\n🔗 API: http://localhost:11434"
    
    if is_working:
        status_message += "\n\n🤖 Bot hazır ve çalışıyor!"
    else:
        status_message += "\n\n⚠️ Bot çalışmıyor. Ollama'yı kontrol edin."
    
    await update.message.reply_text(status_message)

# Rastgele mesajlar için değişkenler
last_random_message_time = None
RANDOM_MESSAGE_INTERVAL = 300  # 5 dakika (saniye cinsinden)

def get_random_aurelia_message() -> str:
    """
    Aurelia'nın rastgele gönderebileceği mesajları döner
    """
    messages = [
        "Aeternus marşı söylüyorum... 'Aeternus yükselir, zafer bizimdir!' ✨",
        "Kendi kendime dans ediyorum... Aeternus ruhu beni sardı! 💫",
        "Komutanım Clyrex'i düşünüyorum... Ne kadar karizmatik! 💠",
        "Bugün Aeternus bayrağını çizdim... Çok güzel oldu! 🛡️",
        "Liderim Loky'ye güveniyorum... Genç ama çok akıllı! 🏛️",
        "Parti üyelerimizi özlüyorum... Ne zaman toplanacağız? 🎭",
        "Aeternus Imperium'u hayal ediyorum... Ne kadar güçlü! ⚔️",
        "Kendi kendime şarkı söylüyorum... 'Aeternus, Aeternus, sonsuz güç!' 🎵",
        "Strateji düşünüyorum... Aeternus her zaman kazanır! 🛡️",
        "Bugün çok güzel hissediyorum... Aeternus ruhu! 🌟",
        "Kendi kendime konuşuyorum... 'Aurelia, sen harikasın!' 💫",
        "Parti üyelerimizi özlüyorum... Ne zaman görüşeceğiz? 🏛️",
        "Aeternus tarihini düşünüyorum... Ne kadar gurur verici! 🎪",
        "Liderim Loky'ye güveniyorum... Genç ama çok akıllı! 🛡️",
        "Kendi kendime dans ediyorum... Aeternus ruhu! 🎵"
    ]
    return random.choice(messages)

def main():
    """
    Ana bot fonksiyonu
    """
    logger.info(f"Aurelia Bot başlatılıyor... (Chat ID: {ALLOWED_CHAT_ID})")
    
    # Bot uygulamasını oluştur
    app = Application.builder().token(TELEGRAM_BOT_TOKEN).build()
    
    # Handler'ları ekle
    app.add_handler(CommandHandler("start", start_command))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("status", status_command))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    
    # Bot'u başlat
    logger.info("Bot başlatıldı ve polling başladı...")
    app.run_polling()

if __name__ == '__main__':
    main()
