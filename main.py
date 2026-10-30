# -*- coding: utf-8 -*-
"""
UpPack - Tu nube segura
=======================
Para IDLE con Python 3.14: abre este archivo y pulsa F5.
Solo usa la libreria estandar (tkinter incluido en IDLE).

- Sube archivos a tu "boveda" (carpeta ~/UpPack_Vault) cifrados y con
  comprobacion de integridad. Tus archivos originales NUNCA se tocan ni se borran.
- Casilla "Liberar 19GB gratis": sube el limite de 1 GB a 20 GB.
- Escaner de archivos peligrosos/ilegales con 2 botones: Aceptar / Guardar de todos modos.
- 30 idiomas.
- Version celular automatica (Android / iOS / pantallas pequenas).
"""
import os
import sys
import json
import time
import uuid
import hmac
import locale
import hashlib
import secrets
import re
from pathlib import Path

import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from tkinter import font as tkfont

# ----------------------------------------------------------------------------
# Configuracion
# ----------------------------------------------------------------------------
APP = "UpPack"
VAULT = Path.home() / "UpPack_Vault"
BLOBS = VAULT / "files"
INDEX = VAULT / "index.json"
KEYFILE = VAULT / ".key"

GB = 1024 ** 3
BASE_QUOTA = 1 * GB          # espacio inicial
FREE_BONUS = 19 * GB         # lo que da la casilla "Liberar 19GB gratis"
CHUNK = 1 << 20              # 1 MB

ORANGE = "#FF4500"
ORANGE_D = "#D63A00"
BG = "#F3F5F8"
DANGER = "#C62828"

FORCE_MOBILE = None          # True / False para probar; None = autodetectar

# ----------------------------------------------------------------------------
# Idiomas (30)
# ----------------------------------------------------------------------------
KEYS = ("tagline upload files storage free19 download delete language "
        "warn_title warn_msg reason accept save_anyway saved no_space empty "
        "name size date select_first confirm_delete blocked "
        "r_exec r_sig r_pirate").split()

LANGS = [
    ("es", "Español"), ("en", "English"), ("pt", "Português"), ("fr", "Français"),
    ("de", "Deutsch"), ("it", "Italiano"), ("nl", "Nederlands"), ("sv", "Svenska"),
    ("pl", "Polski"), ("tr", "Türkçe"), ("ru", "Русский"), ("uk", "Українська"),
    ("ar", "العربية"), ("he", "עברית"), ("hi", "हिन्दी"), ("bn", "বাংলা"),
    ("zh", "中文"), ("ja", "日本語"), ("ko", "한국어"), ("vi", "Tiếng Việt"),
    ("th", "ไทย"), ("id", "Bahasa Indonesia"), ("ms", "Bahasa Melayu"),
    ("fil", "Filipino"), ("cs", "Čeština"), ("ro", "Română"), ("el", "Ελληνικά"),
    ("hu", "Magyar"), ("fi", "Suomi"), ("da", "Dansk"),
]

T = {
    "es": ["Tu nube segura", "Subir archivos", "Mis archivos", "Almacenamiento",
           "Liberar 19GB gratis", "Descargar", "Eliminar", "Idioma",
           "¡Archivo peligroso o ilegal!", "Este archivo es peligroso o ilegal.",
           "Motivo", "Aceptar", "Guardar de todos modos", "Guardado y protegido",
           "No hay espacio suficiente", "Aún no hay archivos", "Nombre", "Tamaño",
           "Fecha", "Selecciona un archivo primero",
           "¿Eliminar de la nube? (tu PC no se modifica)", "Bloqueado",
           "Ejecutable o script potencialmente peligroso", "Firma de malware conocida",
           "Crack/keygen (software ilegal)"],
    "en": ["Your secure cloud", "Upload files", "My files", "Storage",
           "Unlock 19GB free", "Download", "Delete", "Language",
           "Dangerous or illegal file!", "This file is dangerous or illegal.",
           "Reason", "Accept", "Save anyway", "Saved and protected",
           "Not enough space", "No files yet", "Name", "Size", "Date",
           "Select a file first", "Delete from the cloud? (your PC is not touched)",
           "Blocked", "Potentially dangerous executable or script",
           "Known malware signature", "Crack/keygen (illegal software)"],
    "pt": ["Sua nuvem segura", "Enviar arquivos", "Meus arquivos", "Armazenamento",
           "Liberar 19GB grátis", "Baixar", "Excluir", "Idioma",
           "Arquivo perigoso ou ilegal!", "Este arquivo é perigoso ou ilegal.",
           "Motivo", "Aceitar", "Salvar mesmo assim", "Salvo e protegido",
           "Espaço insuficiente", "Nenhum arquivo ainda", "Nome", "Tamanho", "Data",
           "Selecione um arquivo primeiro",
           "Excluir da nuvem? (seu PC não é alterado)", "Bloqueado",
           "Executável ou script potencialmente perigoso",
           "Assinatura de malware conhecida", "Crack/keygen (software ilegal)"],
    "fr": ["Votre cloud sécurisé", "Téléverser des fichiers", "Mes fichiers", "Stockage",
           "Débloquer 19 Go gratuits", "Télécharger", "Supprimer", "Langue",
           "Fichier dangereux ou illégal !", "Ce fichier est dangereux ou illégal.",
           "Motif", "Accepter", "Enregistrer quand même", "Enregistré et protégé",
           "Espace insuffisant", "Aucun fichier pour l'instant", "Nom", "Taille", "Date",
           "Sélectionnez d'abord un fichier",
           "Supprimer du cloud ? (votre PC n'est pas modifié)", "Bloqué",
           "Exécutable ou script potentiellement dangereux",
           "Signature de malware connue", "Crack/keygen (logiciel illégal)"],
    "de": ["Deine sichere Cloud", "Dateien hochladen", "Meine Dateien", "Speicher",
           "19 GB gratis freischalten", "Herunterladen", "Löschen", "Sprache",
           "Gefährliche oder illegale Datei!", "Diese Datei ist gefährlich oder illegal.",
           "Grund", "Akzeptieren", "Trotzdem speichern", "Gespeichert und geschützt",
           "Nicht genug Speicherplatz", "Noch keine Dateien", "Name", "Größe", "Datum",
           "Wähle zuerst eine Datei",
           "Aus der Cloud löschen? (dein PC bleibt unberührt)", "Blockiert",
           "Potenziell gefährliche ausführbare Datei oder Skript",
           "Bekannte Malware-Signatur", "Crack/Keygen (illegale Software)"],
    "it": ["Il tuo cloud sicuro", "Carica file", "I miei file", "Spazio",
           "Sblocca 19GB gratis", "Scarica", "Elimina", "Lingua",
           "File pericoloso o illegale!", "Questo file è pericoloso o illegale.",
           "Motivo", "Accetta", "Salva comunque", "Salvato e protetto",
           "Spazio insufficiente", "Ancora nessun file", "Nome", "Dimensione", "Data",
           "Seleziona prima un file",
           "Eliminare dal cloud? (il tuo PC non viene toccato)", "Bloccato",
           "Eseguibile o script potenzialmente pericoloso",
           "Firma di malware nota", "Crack/keygen (software illegale)"],
    "nl": ["Je veilige cloud", "Bestanden uploaden", "Mijn bestanden", "Opslag",
           "19GB gratis vrijgeven", "Downloaden", "Verwijderen", "Taal",
           "Gevaarlijk of illegaal bestand!", "Dit bestand is gevaarlijk of illegaal.",
           "Reden", "Accepteren", "Toch opslaan", "Opgeslagen en beschermd",
           "Onvoldoende ruimte", "Nog geen bestanden", "Naam", "Grootte", "Datum",
           "Selecteer eerst een bestand",
           "Uit de cloud verwijderen? (je pc blijft ongewijzigd)", "Geblokkeerd",
           "Mogelijk gevaarlijk uitvoerbaar bestand of script",
           "Bekende malwarehandtekening", "Crack/keygen (illegale software)"],
    "sv": ["Ditt säkra moln", "Ladda upp filer", "Mina filer", "Lagring",
           "Lås upp 19 GB gratis", "Ladda ner", "Ta bort", "Språk",
           "Farlig eller olaglig fil!", "Den här filen är farlig eller olaglig.",
           "Orsak", "Acceptera", "Spara ändå", "Sparad och skyddad",
           "Inte tillräckligt med utrymme", "Inga filer än", "Namn", "Storlek", "Datum",
           "Välj en fil först", "Ta bort från molnet? (din dator påverkas inte)",
           "Blockerad", "Potentiellt farlig körbar fil eller skript",
           "Känd skadlig kodsignatur", "Crack/keygen (olaglig programvara)"],
    "pl": ["Twoja bezpieczna chmura", "Prześlij pliki", "Moje pliki", "Pamięć",
           "Odblokuj 19 GB za darmo", "Pobierz", "Usuń", "Język",
           "Plik niebezpieczny lub nielegalny!", "Ten plik jest niebezpieczny lub nielegalny.",
           "Powód", "Akceptuj", "Zapisz mimo to", "Zapisano i zabezpieczono",
           "Za mało miejsca", "Brak plików", "Nazwa", "Rozmiar", "Data",
           "Najpierw wybierz plik",
           "Usunąć z chmury? (Twój komputer nie zostanie zmieniony)", "Zablokowano",
           "Potencjalnie niebezpieczny plik wykonywalny lub skrypt",
           "Znana sygnatura złośliwego oprogramowania", "Crack/keygen (nielegalne oprogramowanie)"],
    "tr": ["Güvenli bulutunuz", "Dosya yükle", "Dosyalarım", "Depolama",
           "19GB ücretsiz aç", "İndir", "Sil", "Dil",
           "Tehlikeli veya yasa dışı dosya!", "Bu dosya tehlikeli veya yasa dışı.",
           "Neden", "Kabul et", "Yine de kaydet", "Kaydedildi ve korundu",
           "Yeterli alan yok", "Henüz dosya yok", "Ad", "Boyut", "Tarih",
           "Önce bir dosya seçin",
           "Buluttan silinsin mi? (bilgisayarınıza dokunulmaz)", "Engellendi",
           "Potansiyel olarak tehlikeli çalıştırılabilir dosya veya betik",
           "Bilinen kötü amaçlı yazılım imzası", "Crack/keygen (yasa dışı yazılım)"],
    "ru": ["Ваше безопасное облако", "Загрузить файлы", "Мои файлы", "Хранилище",
           "Получить 19 ГБ бесплатно", "Скачать", "Удалить", "Язык",
           "Опасный или незаконный файл!", "Этот файл опасен или незаконен.",
           "Причина", "Принять", "Всё равно сохранить", "Сохранено и защищено",
           "Недостаточно места", "Файлов пока нет", "Имя", "Размер", "Дата",
           "Сначала выберите файл", "Удалить из облака? (ваш ПК не затрагивается)",
           "Заблокировано", "Потенциально опасный исполняемый файл или скрипт",
           "Известная сигнатура вредоносного ПО", "Crack/keygen (нелегальное ПО)"],
    "uk": ["Ваша безпечна хмара", "Вивантажити файли", "Мої файли", "Сховище",
           "Отримати 19 ГБ безкоштовно", "Завантажити", "Видалити", "Мова",
           "Небезпечний або незаконний файл!", "Цей файл небезпечний або незаконний.",
           "Причина", "Прийняти", "Усе одно зберегти", "Збережено та захищено",
           "Недостатньо місця", "Файлів поки немає", "Назва", "Розмір", "Дата",
           "Спочатку виберіть файл", "Видалити з хмари? (ваш ПК не змінюється)",
           "Заблоковано", "Потенційно небезпечний виконуваний файл або скрипт",
           "Відомий підпис шкідливого ПЗ", "Crack/keygen (нелегальне ПЗ)"],
    "ar": ["سحابتك الآمنة", "رفع الملفات", "ملفاتي", "التخزين",
           "احصل على 19GB مجانًا", "تنزيل", "حذف", "اللغة",
           "ملف خطير أو غير قانوني!", "هذا الملف خطير أو غير قانوني.",
           "السبب", "قبول", "احفظ على أي حال", "تم الحفظ والحماية",
           "لا توجد مساحة كافية", "لا توجد ملفات بعد", "الاسم", "الحجم", "التاريخ",
           "اختر ملفًا أولاً", "هل تريد الحذف من السحابة؟ (جهازك لن يتأثر)", "محظور",
           "ملف تنفيذي أو سكربت قد يكون خطيرًا", "توقيع برنامج ضار معروف",
           "Crack/keygen (برمجيات غير قانونية)"],
    "he": ["הענן המאובטח שלך", "העלאת קבצים", "הקבצים שלי", "אחסון",
           "קבל 19GB בחינם", "הורדה", "מחיקה", "שפה",
           "קובץ מסוכן או לא חוקי!", "הקובץ הזה מסוכן או לא חוקי.",
           "סיבה", "אישור", "שמור בכל זאת", "נשמר ומוגן",
           "אין מספיק מקום", "אין קבצים עדיין", "שם", "גודל", "תאריך",
           "בחר קובץ קודם", "למחוק מהענן? (המחשב שלך לא ישתנה)", "נחסם",
           "קובץ הפעלה או סקריפט שעלול להיות מסוכן", "חתימת תוכנה זדונית ידועה",
           "Crack/keygen (תוכנה לא חוקית)"],
    "hi": ["आपका सुरक्षित क्लाउड", "फ़ाइलें अपलोड करें", "मेरी फ़ाइलें", "स्टोरेज",
           "19GB मुफ़्त पाएँ", "डाउनलोड", "हटाएँ", "भाषा",
           "खतरनाक या अवैध फ़ाइल!", "यह फ़ाइल खतरनाक या अवैध है।",
           "कारण", "स्वीकार करें", "फिर भी सेव करें", "सेव और सुरक्षित",
           "पर्याप्त जगह नहीं है", "अभी कोई फ़ाइल नहीं", "नाम", "आकार", "तारीख़",
           "पहले एक फ़ाइल चुनें", "क्लाउड से हटाएँ? (आपके पीसी को नहीं छुआ जाएगा)",
           "ब्लॉक किया गया", "संभावित रूप से खतरनाक एक्ज़ीक्यूटेबल या स्क्रिप्ट",
           "ज्ञात मैलवेयर सिग्नेचर", "Crack/keygen (अवैध सॉफ़्टवेयर)"],
    "bn": ["আপনার নিরাপদ ক্লাউড", "ফাইল আপলোড করুন", "আমার ফাইল", "স্টোরেজ",
           "19GB বিনামূল্যে নিন", "ডাউনলোড", "মুছুন", "ভাষা",
           "বিপজ্জনক বা অবৈধ ফাইল!", "এই ফাইলটি বিপজ্জনক বা অবৈধ।",
           "কারণ", "গ্রহণ করুন", "তবুও সংরক্ষণ করুন", "সংরক্ষিত ও সুরক্ষিত",
           "পর্যাপ্ত জায়গা নেই", "এখনও কোনো ফাইল নেই", "নাম", "আকার", "তারিখ",
           "আগে একটি ফাইল নির্বাচন করুন",
           "ক্লাউড থেকে মুছবেন? (আপনার পিসিতে হাত দেওয়া হবে না)", "ব্লক করা হয়েছে",
           "সম্ভাব্য বিপজ্জনক এক্সিকিউটেবল বা স্ক্রিপ্ট", "পরিচিত ম্যালওয়্যার সিগনেচার",
           "Crack/keygen (অবৈধ সফটওয়্যার)"],
    "zh": ["您的安全云盘", "上传文件", "我的文件", "存储空间",
           "免费解锁 19GB", "下载", "删除", "语言",
           "危险或非法文件！", "此文件危险或非法。",
           "原因", "确定", "仍然保存", "已保存并受保护",
           "空间不足", "暂无文件", "名称", "大小", "日期",
           "请先选择一个文件", "从云端删除？（不会改动您的电脑）", "已拦截",
           "可能有危险的可执行文件或脚本", "已知恶意软件特征",
           "Crack/keygen（非法软件）"],
    "ja": ["安全なあなたのクラウド", "ファイルをアップロード", "マイファイル", "ストレージ",
           "19GBを無料で解放", "ダウンロード", "削除", "言語",
           "危険または違法なファイル！", "このファイルは危険または違法です。",
           "理由", "了解", "それでも保存", "保存して保護しました",
           "空き容量が足りません", "まだファイルがありません", "名前", "サイズ", "日付",
           "先にファイルを選択してください", "クラウドから削除しますか？（PCは変更されません）",
           "ブロックしました", "危険な可能性のある実行ファイルまたはスクリプト",
           "既知のマルウェアシグネチャ", "Crack/keygen（違法ソフト）"],
    "ko": ["안전한 나의 클라우드", "파일 업로드", "내 파일", "저장 공간",
           "19GB 무료로 받기", "다운로드", "삭제", "언어",
           "위험하거나 불법적인 파일!", "이 파일은 위험하거나 불법입니다.",
           "사유", "확인", "그래도 저장", "저장 및 보호됨",
           "공간이 부족합니다", "아직 파일이 없습니다", "이름", "크기", "날짜",
           "먼저 파일을 선택하세요", "클라우드에서 삭제할까요? (PC는 변경되지 않습니다)",
           "차단됨", "위험할 수 있는 실행 파일 또는 스크립트", "알려진 악성코드 시그니처",
           "Crack/keygen (불법 소프트웨어)"],
    "vi": ["Đám mây an toàn của bạn", "Tải tệp lên", "Tệp của tôi", "Dung lượng",
           "Mở khóa 19GB miễn phí", "Tải xuống", "Xóa", "Ngôn ngữ",
           "Tệp nguy hiểm hoặc bất hợp pháp!", "Tệp này nguy hiểm hoặc bất hợp pháp.",
           "Lý do", "Chấp nhận", "Vẫn lưu", "Đã lưu và bảo vệ",
           "Không đủ dung lượng", "Chưa có tệp nào", "Tên", "Kích thước", "Ngày",
           "Hãy chọn một tệp trước",
           "Xóa khỏi đám mây? (máy tính của bạn không bị ảnh hưởng)", "Đã chặn",
           "Tệp thực thi hoặc tập lệnh có thể nguy hiểm", "Chữ ký mã độc đã biết",
           "Crack/keygen (phần mềm bất hợp pháp)"],
    "th": ["คลาวด์ปลอดภัยของคุณ", "อัปโหลดไฟล์", "ไฟล์ของฉัน", "พื้นที่จัดเก็บ",
           "ปลดล็อก 19GB ฟรี", "ดาวน์โหลด", "ลบ", "ภาษา",
           "ไฟล์อันตรายหรือผิดกฎหมาย!", "ไฟล์นี้อันตรายหรือผิดกฎหมาย",
           "เหตุผล", "ยอมรับ", "บันทึกอยู่ดี", "บันทึกและป้องกันแล้ว",
           "พื้นที่ไม่เพียงพอ", "ยังไม่มีไฟล์", "ชื่อ", "ขนาด", "วันที่",
           "กรุณาเลือกไฟล์ก่อน", "ลบออกจากคลาวด์? (พีซีของคุณจะไม่ถูกแตะต้อง)",
           "ถูกบล็อก", "ไฟล์ปฏิบัติการหรือสคริปต์ที่อาจเป็นอันตราย",
           "ลายเซ็นมัลแวร์ที่รู้จัก", "Crack/keygen (ซอฟต์แวร์ผิดกฎหมาย)"],
    "id": ["Cloud aman Anda", "Unggah file", "File saya", "Penyimpanan",
           "Buka 19GB gratis", "Unduh", "Hapus", "Bahasa",
           "File berbahaya atau ilegal!", "File ini berbahaya atau ilegal.",
           "Alasan", "Terima", "Tetap simpan", "Tersimpan dan terlindungi",
           "Ruang tidak cukup", "Belum ada file", "Nama", "Ukuran", "Tanggal",
           "Pilih file terlebih dahulu", "Hapus dari cloud? (PC Anda tidak diubah)",
           "Diblokir", "Executable atau skrip yang berpotensi berbahaya",
           "Tanda tangan malware yang dikenal", "Crack/keygen (perangkat lunak ilegal)"],
    "ms": ["Awan selamat anda", "Muat naik fail", "Fail saya", "Storan",
           "Buka 19GB percuma", "Muat turun", "Padam", "Bahasa",
           "Fail berbahaya atau menyalahi undang-undang!",
           "Fail ini berbahaya atau menyalahi undang-undang.",
           "Sebab", "Terima", "Simpan juga", "Disimpan dan dilindungi",
           "Ruang tidak mencukupi", "Belum ada fail", "Nama", "Saiz", "Tarikh",
           "Pilih fail dahulu", "Padam daripada awan? (PC anda tidak diubah)",
           "Disekat", "Fail boleh laku atau skrip yang berpotensi berbahaya",
           "Tandatangan perisian hasad yang diketahui",
           "Crack/keygen (perisian menyalahi undang-undang)"],
    "fil": ["Ang ligtas mong cloud", "Mag-upload ng mga file", "Aking mga file", "Imbakan",
            "I-unlock ang 19GB nang libre", "I-download", "Burahin", "Wika",
            "Mapanganib o ilegal na file!", "Mapanganib o ilegal ang file na ito.",
            "Dahilan", "Tanggapin", "I-save pa rin", "Na-save at protektado",
            "Kulang ang espasyo", "Wala pang mga file", "Pangalan", "Laki", "Petsa",
            "Pumili muna ng file", "Burahin sa cloud? (hindi gagalawin ang iyong PC)",
            "Na-block", "Posibleng mapanganib na executable o script",
            "Kilalang lagda ng malware", "Crack/keygen (ilegal na software)"],
    "cs": ["Váš bezpečný cloud", "Nahrát soubory", "Moje soubory", "Úložiště",
           "Odemknout 19 GB zdarma", "Stáhnout", "Smazat", "Jazyk",
           "Nebezpečný nebo nelegální soubor!", "Tento soubor je nebezpečný nebo nelegální.",
           "Důvod", "Přijmout", "Přesto uložit", "Uloženo a chráněno",
           "Nedostatek místa", "Zatím žádné soubory", "Název", "Velikost", "Datum",
           "Nejprve vyberte soubor", "Smazat z cloudu? (váš počítač se nezmění)",
           "Zablokováno", "Potenciálně nebezpečný spustitelný soubor nebo skript",
           "Známý podpis malwaru", "Crack/keygen (nelegální software)"],
    "ro": ["Norul tău sigur", "Încarcă fișiere", "Fișierele mele", "Stocare",
           "Deblochează 19 GB gratis", "Descarcă", "Șterge", "Limbă",
           "Fișier periculos sau ilegal!", "Acest fișier este periculos sau ilegal.",
           "Motiv", "Acceptă", "Salvează oricum", "Salvat și protejat",
           "Spațiu insuficient", "Încă nu există fișiere", "Nume", "Dimensiune", "Dată",
           "Selectează mai întâi un fișier",
           "Ștergi din cloud? (PC-ul tău nu este modificat)", "Blocat",
           "Executabil sau script potențial periculos", "Semnătură de malware cunoscută",
           "Crack/keygen (software ilegal)"],
    "el": ["Το ασφαλές σύννεφο σας", "Ανέβασμα αρχείων", "Τα αρχεία μου", "Αποθήκευση",
           "Ξεκλειδώστε 19GB δωρεάν", "Λήψη", "Διαγραφή", "Γλώσσα",
           "Επικίνδυνο ή παράνομο αρχείο!", "Αυτό το αρχείο είναι επικίνδυνο ή παράνομο.",
           "Αιτία", "Αποδοχή", "Αποθήκευση ούτως ή άλλως", "Αποθηκεύτηκε και προστατεύτηκε",
           "Δεν υπάρχει αρκετός χώρος", "Δεν υπάρχουν αρχεία ακόμη", "Όνομα", "Μέγεθος",
           "Ημερομηνία", "Επιλέξτε πρώτα ένα αρχείο",
           "Διαγραφή από το σύννεφο; (ο υπολογιστής σας δεν θα επηρεαστεί)", "Αποκλείστηκε",
           "Δυνητικά επικίνδυνο εκτελέσιμο ή σενάριο", "Γνωστή υπογραφή κακόβουλου λογισμικού",
           "Crack/keygen (παράνομο λογισμικό)"],
    "hu": ["Biztonságos felhőd", "Fájlok feltöltése", "Fájljaim", "Tárhely",
           "19 GB ingyen feloldása", "Letöltés", "Törlés", "Nyelv",
           "Veszélyes vagy illegális fájl!", "Ez a fájl veszélyes vagy illegális.",
           "Ok", "Elfogadom", "Mentés mégis", "Mentve és védve",
           "Nincs elég hely", "Még nincsenek fájlok", "Név", "Méret", "Dátum",
           "Előbb válassz egy fájlt", "Törlöd a felhőből? (a számítógéped nem változik)",
           "Blokkolva", "Potenciálisan veszélyes futtatható fájl vagy szkript",
           "Ismert kártevő-aláírás", "Crack/keygen (illegális szoftver)"],
    "fi": ["Turvallinen pilvesi", "Lähetä tiedostoja", "Omat tiedostot", "Tallennustila",
           "Avaa 19 Gt ilmaiseksi", "Lataa koneelle", "Poista", "Kieli",
           "Vaarallinen tai laiton tiedosto!", "Tämä tiedosto on vaarallinen tai laiton.",
           "Syy", "Hyväksy", "Tallenna silti", "Tallennettu ja suojattu",
           "Tallennustila ei riitä", "Ei vielä tiedostoja", "Nimi", "Koko", "Päivämäärä",
           "Valitse ensin tiedosto", "Poistetaanko pilvestä? (tietokonettasi ei muuteta)",
           "Estetty", "Mahdollisesti vaarallinen suoritettava tiedosto tai komentosarja",
           "Tunnettu haittaohjelman tunniste", "Crack/keygen (laiton ohjelmisto)"],
    "da": ["Din sikre sky", "Upload filer", "Mine filer", "Lager",
           "Lås 19 GB op gratis", "Download", "Slet", "Sprog",
           "Farlig eller ulovlig fil!", "Denne fil er farlig eller ulovlig.",
           "Årsag", "Accepter", "Gem alligevel", "Gemt og beskyttet",
           "Ikke nok plads", "Ingen filer endnu", "Navn", "Størrelse", "Dato",
           "Vælg en fil først", "Slet fra skyen? (din pc berøres ikke)",
           "Blokeret", "Potentielt farlig eksekverbar fil eller script",
           "Kendt malware-signatur", "Crack/keygen (ulovlig software)"],
}
TR = {code: dict(zip(KEYS, vals)) for code, vals in T.items()}


def default_lang():
    raw = ""
    try:
        if sys.platform == "win32":
            import ctypes
            raw = locale.windows_locale.get(
                ctypes.windll.kernel32.GetUserDefaultUILanguage(), "")
        else:
            raw = os.environ.get("LANG", "") or (locale.getlocale()[0] or "")
    except Exception:
        pass
    raw = raw.lower()
    code = "fil" if raw.startswith(("fil", "tl")) else raw[:2]
    return code if code in TR else "es"


# ----------------------------------------------------------------------------
# Proteccion: cifrado de la boveda (solo libreria estandar)
# SHAKE-256 como flujo de claves + HMAC-SHA256 para integridad.
# ----------------------------------------------------------------------------
def _stream(key, nonce, n, ctr):
    return hashlib.shake_256(key + nonce + ctr.to_bytes(8, "big")).digest(n)


def _xor(data, ks):
    return (int.from_bytes(data, "big") ^ int.from_bytes(ks, "big")).to_bytes(len(data), "big")


def encrypt_file(src, dst, key, progress):
    nonce = secrets.token_bytes(16)
    mac = hmac.new(key, nonce, hashlib.sha256)
    total = os.path.getsize(src)
    done = ctr = 0
    with open(src, "rb") as fi, open(dst, "wb") as fo:
        fo.write(nonce)
        while True:
            b = fi.read(CHUNK)
            if not b:
                break
            c = _xor(b, _stream(key, nonce, len(b), ctr))
            ctr += 1
            mac.update(c)
            fo.write(c)
            done += len(b)
            progress(done, total)
        fo.write(mac.digest())


def decrypt_file(src, dst, key, progress):
    total = os.path.getsize(src) - 48
    if total < 0:
        raise ValueError("Corrupt file")
    with open(src, "rb") as fi, open(dst, "wb") as fo:
        nonce = fi.read(16)
        mac = hmac.new(key, nonce, hashlib.sha256)
        left, ctr = total, 0
        while left > 0:
            c = fi.read(min(CHUNK, left))
            if not c:
                raise ValueError("Truncated file")
            left -= len(c)
            mac.update(c)
            fo.write(_xor(c, _stream(key, nonce, len(c), ctr)))
            ctr += 1
            progress(total - left, total)
        if not hmac.compare_digest(mac.digest(), fi.read(32)):
            raise ValueError("Integrity check failed")


def load_key():
    if KEYFILE.exists() and KEYFILE.stat().st_size == 32:
        return KEYFILE.read_bytes()
    k = secrets.token_bytes(32)
    KEYFILE.write_bytes(k)
    try:
        os.chmod(KEYFILE, 0o600)
    except OSError:
        pass
    return k


# ----------------------------------------------------------------------------
# Escaner de archivos peligrosos / ilegales (heuristico, sin internet)
# ----------------------------------------------------------------------------
DANGEROUS_EXT = {
    ".exe", ".scr", ".bat", ".cmd", ".com", ".pif", ".vbs", ".vbe", ".jse",
    ".wsf", ".wsh", ".hta", ".ps1", ".msi", ".msp", ".dll", ".sys", ".lnk",
    ".reg", ".cpl", ".gadget",
}
SIGNATURES = [
    b"EICAR-STANDARD-ANTIVIRUS-TEST-FILE",   # archivo de prueba estandar (inofensivo)
    b"mimikatz",
    b"-EncodedCommand",
]
PIRATE_RE = re.compile(r"(keygen|key[-_ ]gen|warez|nulled|\bcrack(ed)?\b|activator)")


def scan(path):
    """Devuelve una lista de motivos: 'r_exec', 'r_sig', 'r_pirate'."""
    reasons = []
    name = os.path.basename(path).lower()
    ext = os.path.splitext(name)[1]
    try:
        with open(path, "rb") as f:
            head = f.read(1 << 20)
    except OSError:
        head = b""
    disguised = (head[:2] == b"MZ" or head[:4] == b"\x7fELF") and ext not in DANGEROUS_EXT
    if ext in DANGEROUS_EXT or disguised:
        reasons.append("r_exec")
    low = head.lower()
    if any(sig.lower() in low for sig in SIGNATURES):
        reasons.append("r_sig")
    if PIRATE_RE.search(name):
        reasons.append("r_pirate")
    return reasons


# ----------------------------------------------------------------------------
# Utilidades
# ----------------------------------------------------------------------------
def fmt(n):
    n = float(n)
    for u in ("B", "KB", "MB", "GB"):
        if n < 1024:
            return f"{n:.0f} {u}" if u == "B" else f"{n:.1f} {u}"
        n /= 1024
    return f"{n:.1f} TB"


def load_index():
    try:
        with open(INDEX, "r", encoding="utf-8") as f:
            d = json.load(f)
        d.setdefault("files", [])
        d.setdefault("free19", False)
        d.setdefault("lang", None)
        return d
    except Exception:
        return {"files": [], "free19": False, "lang": None}


def detect_mobile(root):
    if FORCE_MOBILE is not None:
        return FORCE_MOBILE
    if sys.platform in ("android", "ios"):
        return True
    env = os.environ
    if any(k in env for k in ("ANDROID_ROOT", "ANDROID_DATA", "ANDROID_ARGUMENT")):
        return True
    w, h = root.winfo_screenwidth(), root.winfo_screenheight()
    return w < 700 or (h > w and w < 900)


# ----------------------------------------------------------------------------
# Logo (recreado con Canvas): flecha naranja + caja con nube + 3 patas grises
# ----------------------------------------------------------------------------
def draw_logo(c, s=0.2):
    def X(v):
        return (v - 30) * s

    def poly(pts, col):
        flat = [X(v) for p in pts for v in p]
        c.create_polygon(flat, fill=col, outline=col)

    def rect(x1, y1, x2, y2, col):
        c.create_rectangle(X(x1), X(y1), X(x2), X(y2), fill=col, outline=col)

    def oval(x1, y1, x2, y2, col):
        c.create_oval(X(x1), X(y1), X(x2), X(y2), fill=col, outline=col)

    # flecha (mitad clara + mitad oscura)
    poly([(188, 33), (41, 195), (113, 195), (113, 350), (188, 350)], "#FF4500")
    poly([(188, 33), (335, 195), (265, 195), (265, 350), (188, 350)], "#D63A00")
    # caja marron
    rect(127, 170, 188, 258, "#C27C50")
    rect(188, 170, 250, 258, "#A9663F")
    rect(120, 142, 188, 170, "#7B5338")
    rect(188, 142, 258, 170, "#6A4630")
    # tarjeta blanca con nube azul
    rect(148, 172, 228, 232, "#F4F4F4")
    oval(160, 203, 180, 223, "#1E9BE8")
    oval(198, 203, 218, 223, "#1E9BE8")
    rect(170, 203, 208, 223, "#1E9BE8")
    oval(164, 186, 192, 214, "#1E9BE8")
    oval(186, 191, 210, 215, "#1E9BE8")
    # patas grises (propulsion)
    for x1, x2 in ((128, 148), (176, 196), (226, 246)):
        rect(x1, 362, x2, 436, "#9B9DA0")
        rect(x1 + 3, 444, x2 - 3, 465, "#8A8C8F")


# ----------------------------------------------------------------------------
# Aplicacion
# ----------------------------------------------------------------------------
class App:
    def __init__(self):
        VAULT.mkdir(parents=True, exist_ok=True)
        BLOBS.mkdir(exist_ok=True)
        self.root = tk.Tk()
        self.root.title(APP)
        self.root.configure(bg=BG)
        self.mobile = detect_mobile(self.root)
        self.key = load_key()
        self.idx = load_index()
        self.lang = self.idx.get("lang") or default_lang()
        self.busy = False
        if self.mobile:
            sw, sh = self.root.winfo_screenwidth(), self.root.winfo_screenheight()
            self.root.geometry(f"{sw}x{sh}+0+0")
        else:
            self.root.geometry("1000x680")
            self.root.minsize(780, 560)
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)
        self.build()

    # --- textos ---
    def t(self, k):
        return TR.get(self.lang, {}).get(k) or TR["en"][k]

    # --- estado de almacenamiento ---
    def used(self):
        return sum(f["size"] for f in self.idx["files"])

    def quota(self):
        return BASE_QUOTA + (FREE_BONUS if self.idx["free19"] else 0)

    def save(self):
        with open(INDEX, "w", encoding="utf-8") as f:
            json.dump(self.idx, f, ensure_ascii=False, indent=1)

    def on_close(self):
        self.save()
        self.root.destroy()

    # --- widgets ---
    def btn(self, parent, text, cmd, kind="plain"):
        m = self.mobile
        if kind == "primary":
            bg, fg, ab = ORANGE, "white", ORANGE_D
        elif kind == "danger":
            bg, fg, ab = DANGER, "white", "#9E1F1F"
        else:
            bg, fg, ab = "#E3E7EB", "#222222", "#D3D8DD"
        return tk.Button(parent, text=text, command=cmd, bg=bg, fg=fg,
                         activebackground=ab, activeforeground=fg, relief="flat",
                         bd=0, cursor="hand2", padx=18 if not m else 10,
                         pady=10 if not m else 16)

    def build(self):
        for w in self.root.winfo_children():
            w.destroy()
        m = self.mobile
        fs = 15 if m else 10
        for name in ("TkDefaultFont", "TkTextFont", "TkMenuFont", "TkHeadingFont"):
            tkfont.nametofont(name).configure(size=fs)
        self.f_bold = tkfont.nametofont("TkDefaultFont").copy()
        self.f_bold.configure(weight="bold")
        self.f_title = tkfont.nametofont("TkDefaultFont").copy()
        self.f_title.configure(weight="bold", size=fs + (6 if m else 10))
        self.f_small = tkfont.nametofont("TkDefaultFont").copy()
        self.f_small.configure(size=max(fs - 2, 8))

        st = ttk.Style(self.root)
        try:
            st.theme_use("clam")
        except tk.TclError:
            pass
        st.configure("Treeview", rowheight=44 if m else 30, background="white",
                     fieldbackground="white", borderwidth=0)
        st.configure("Treeview.Heading", background="#E9EDF1", relief="flat",
                     font=self.f_bold)
        st.map("Treeview", background=[("selected", ORANGE)],
               foreground=[("selected", "white")])
        st.configure("Up.Horizontal.TProgressbar", troughcolor="#E1E5EA",
                     background=ORANGE, bordercolor="#E1E5EA", thickness=14)
        st.configure("Sm.Horizontal.TProgressbar", troughcolor="#E1E5EA",
                     background=ORANGE_D, bordercolor="#E1E5EA", thickness=6)

        pad = 12 if m else 22

        # cabecera
        head = tk.Frame(self.root, bg="white")
        head.pack(fill="x")
        s = 0.15 if m else 0.2
        logo = tk.Canvas(head, width=int(310 * s) + 6, height=int(440 * s) + 6,
                         bg="white", highlightthickness=0)
        logo.pack(side="left", padx=(pad, 10), pady=8)
        draw_logo(logo, s)
        tb = tk.Frame(head, bg="white")
        tb.pack(side="left")
        tk.Label(tb, text=APP, font=self.f_title, fg=ORANGE, bg="white").pack(anchor="w")
        tk.Label(tb, text=self.t("tagline"), fg="#6B7480", bg="white").pack(anchor="w")
        lf = tk.Frame(head, bg="white")
        lf.pack(side="right", padx=pad)
        tk.Label(lf, text=self.t("language"), fg="#6B7480", bg="white",
                 font=self.f_small).pack(anchor="e")
        self.cb = ttk.Combobox(lf, state="readonly", width=12 if m else 16,
                               values=[n for _, n in LANGS])
        self.cb.current([c for c, _ in LANGS].index(self.lang))
        self.cb.pack()
        self.cb.bind("<<ComboboxSelected>>", self.on_lang)
        tk.Frame(self.root, bg=ORANGE, height=3).pack(fill="x")

        body = tk.Frame(self.root, bg=BG)
        body.pack(fill="both", expand=True, padx=pad, pady=pad)

        # tarjeta de almacenamiento
        card = tk.Frame(body, bg="white", padx=16, pady=12)
        card.pack(fill="x")
        tk.Label(card, text=self.t("storage"), font=self.f_bold, bg="white").pack(anchor="w")
        self.sbar = ttk.Progressbar(card, style="Up.Horizontal.TProgressbar",
                                    maximum=100)
        self.sbar.pack(fill="x", pady=6)
        self.slabel = tk.Label(card, bg="white", fg="#444")
        self.slabel.pack(anchor="w")
        self.var19 = tk.BooleanVar(value=self.idx["free19"])
        tk.Checkbutton(card, text=self.t("free19"), variable=self.var19,
                       command=self.on_free19, bg="white", activebackground="white",
                       font=self.f_bold, fg=ORANGE_D, selectcolor="white",
                       cursor="hand2").pack(anchor="w", pady=(8, 0))

        # barra de acciones
        bar = tk.Frame(body, bg=BG)
        bar.pack(fill="x", pady=(14, 8))
        tk.Label(bar, text=self.t("files"), font=self.f_bold, bg=BG).pack(side="left")
        if m:
            self.btn(body, "⬆  " + self.t("upload"), self.on_upload,
                     "primary").pack(fill="x", pady=(0, 8))
        else:
            self.btn(bar, self.t("delete"), self.on_delete).pack(side="right", padx=(8, 0))
            self.btn(bar, self.t("download"), self.on_download).pack(side="right", padx=(8, 0))
            self.btn(bar, "⬆  " + self.t("upload"), self.on_upload,
                     "primary").pack(side="right")

        # lista de archivos
        lf2 = tk.Frame(body, bg="white")
        lf2.pack(fill="both", expand=True)
        cols = ("name", "size", "date")
        self.tree = ttk.Treeview(lf2, columns=cols, show="headings",
                                 selectmode="browse")
        self.tree.heading("name", text=self.t("name"))
        self.tree.heading("size", text=self.t("size"))
        self.tree.heading("date", text=self.t("date"))
        self.tree.column("name", width=420, stretch=True)
        self.tree.column("size", width=110 if not m else 90, anchor="e", stretch=False)
        self.tree.column("date", width=150, anchor="center", stretch=False)
        if m:
            self.tree.configure(displaycolumns=("name", "size"))
        sc = ttk.Scrollbar(lf2, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=sc.set)
        self.tree.pack(side="left", fill="both", expand=True)
        sc.pack(side="right", fill="y")

        if m:
            row = tk.Frame(body, bg=BG)
            row.pack(fill="x", pady=(8, 0))
            self.btn(row, self.t("download"), self.on_download).pack(
                side="left", expand=True, fill="x", padx=(0, 4))
            self.btn(row, self.t("delete"), self.on_delete).pack(
                side="left", expand=True, fill="x", padx=(4, 0))

        # estado + progreso de subida
        self.pbar = ttk.Progressbar(body, style="Sm.Horizontal.TProgressbar", maximum=100)
        self.pbar.pack(fill="x", pady=(10, 2))
        self.status = tk.StringVar(value="")
        tk.Label(body, textvariable=self.status, bg=BG, fg="#555",
                 anchor="w").pack(fill="x")
        self.refresh()

    def refresh(self):
        t = self.tree
        t.delete(*t.get_children())
        files = self.idx["files"]
        if not files:
            t.insert("", "end", iid="_empty", values=(self.t("empty"), "", ""))
        for f in reversed(files):
            mark = "⚠ " if f.get("flag") else "✓ "
            t.insert("", "end", iid=f["id"],
                     values=(mark + f["name"], fmt(f["size"]), f["date"]))
        used, q = self.used(), self.quota()
        self.sbar["value"] = min(100, 100 * used / q)
        self.slabel.config(text=f"{fmt(used)} / {fmt(q)}   ({100 * used / q:.1f}%)")

    def say(self, msg):
        self.status.set(msg)

    def prog(self, done, total):
        self.pbar["value"] = 100 * done / max(total, 1)
        self.root.update()

    # --- eventos ---
    def on_lang(self, _e=None):
        self.lang = LANGS[self.cb.current()][0]
        self.idx["lang"] = self.lang
        self.save()
        self.root.after(10, self.build)

    def on_free19(self):
        if not self.var19.get() and self.used() > BASE_QUOTA:
            self.var19.set(True)
            messagebox.showwarning(APP, self.t("no_space"))
            return
        self.idx["free19"] = bool(self.var19.get())
        self.save()
        self.refresh()

    def selected(self):
        sel = self.tree.selection()
        if not sel:
            return None
        for f in self.idx["files"]:
            if f["id"] == sel[0]:
                return f
        return None

    def on_upload(self):
        if self.busy:
            return
        paths = filedialog.askopenfilenames(title=self.t("upload"))
        if not paths:
            return
        self.busy = True
        try:
            for p in paths:
                self.process(p)
        finally:
            self.busy = False
            self.pbar["value"] = 0
            self.refresh()

    def process(self, path):
        name = os.path.basename(path)
        try:
            size = os.path.getsize(path)
        except OSError:
            return
        flag = False
        reasons = scan(path)
        if reasons:
            if self.warn(name, reasons) == "accept":
                self.say(f"{self.t('blocked')}: {name}")
                return
            flag = True
        if self.used() + size > self.quota():
            self.say(f"{self.t('no_space')}: {name}")
            messagebox.showwarning(APP, self.t("no_space"))
            return
        fid = uuid.uuid4().hex
        blob = BLOBS / (fid + ".upk")
        try:
            # El original solo se LEE: nunca se mueve ni se borra de tu PC.
            encrypt_file(path, blob, self.key, self.prog)
        except Exception as e:
            try:
                os.remove(blob)
            except OSError:
                pass
            messagebox.showerror(APP, str(e))
            return
        self.idx["files"].append({"id": fid, "name": name, "size": size,
                                  "date": time.strftime("%Y-%m-%d %H:%M"),
                                  "flag": flag})
        self.save()
        self.say(f"{self.t('saved')}: {name}")

    def warn(self, name, reasons):
        """Aviso de archivo peligroso/ilegal con 2 botones. Devuelve 'accept' o 'save'."""
        dlg = tk.Toplevel(self.root)
        dlg.title(APP)
        dlg.configure(bg="white")
        dlg.transient(self.root)
        dlg.resizable(False, False)
        res = {"v": "accept"}
        wl = (self.root.winfo_screenwidth() - 90) if self.mobile else 430

        def done(v):
            res["v"] = v
            dlg.destroy()

        top = tk.Frame(dlg, bg=DANGER)
        top.pack(fill="x")
        tk.Label(top, text="⚠  " + self.t("warn_title"), bg=DANGER, fg="white",
                 font=self.f_bold, padx=16, pady=12, wraplength=wl,
                 justify="left").pack(anchor="w")
        tk.Label(dlg, text=self.t("warn_msg"), bg="white", wraplength=wl,
                 justify="left").pack(anchor="w", padx=16, pady=(14, 4))
        tk.Label(dlg, text=name, bg="white", fg=DANGER, font=self.f_bold,
                 wraplength=wl, justify="left").pack(anchor="w", padx=16)
        tk.Label(dlg, text=self.t("reason") + ":", bg="white", fg="#555").pack(
            anchor="w", padx=16, pady=(10, 0))
        for r in reasons:
            tk.Label(dlg, text="•  " + self.t(r), bg="white", wraplength=wl,
                     justify="left").pack(anchor="w", padx=26)
        bf = tk.Frame(dlg, bg="white")
        bf.pack(fill="x", padx=16, pady=16)
        b1 = self.btn(bf, self.t("accept"), lambda: done("accept"), "primary")
        b2 = self.btn(bf, self.t("save_anyway"), lambda: done("save"))
        if self.mobile:
            b1.pack(fill="x", pady=(0, 8))
            b2.pack(fill="x")
        else:
            b2.pack(side="right")
            b1.pack(side="right", padx=(0, 8))
        dlg.protocol("WM_DELETE_WINDOW", lambda: done("accept"))
        dlg.update_idletasks()
        w, h = dlg.winfo_reqwidth(), dlg.winfo_reqheight()
        x = self.root.winfo_x() + max((self.root.winfo_width() - w) // 2, 0)
        y = self.root.winfo_y() + max((self.root.winfo_height() - h) // 3, 0)
        dlg.geometry(f"+{x}+{y}")
        try:
            dlg.wait_visibility()
            dlg.grab_set()
        except tk.TclError:
            pass
        dlg.focus_set()
        self.root.wait_window(dlg)
        return res["v"]

    def on_download(self):
        if self.busy:
            return
        f = self.selected()
        if not f:
            messagebox.showinfo(APP, self.t("select_first"))
            return
        dst = filedialog.asksaveasfilename(initialfile=f["name"])
        if not dst:
            return
        self.busy = True
        try:
            decrypt_file(BLOBS / (f["id"] + ".upk"), dst, self.key, self.prog)
            self.say(f"{self.t('download')}: {f['name']}")
        except Exception as e:
            try:
                os.remove(dst)
            except OSError:
                pass
            messagebox.showerror(APP, str(e))
        finally:
            self.busy = False
            self.pbar["value"] = 0

    def on_delete(self):
        if self.busy:
            return
        f = self.selected()
        if not f:
            messagebox.showinfo(APP, self.t("select_first"))
            return
        if not messagebox.askyesno(APP, self.t("confirm_delete")):
            return
        try:
            os.remove(BLOBS / (f["id"] + ".upk"))
        except OSError:
            pass
        self.idx["files"] = [x for x in self.idx["files"] if x["id"] != f["id"]]
        self.save()
        self.refresh()

    def run(self):
        self.root.mainloop()


if __name__ == "__main__":
    App().run()
