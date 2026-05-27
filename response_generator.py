import random
from datetime import datetime




LIGHT_RECOVERY_ACTIVITIES = [
    "baca beberapa halaman buku kesukaanmu",
    "main game sebentar aja",
    "dengerin playlist favorite",
    "nonton video ringan yang bikin moodmu naik",
    "bikin minuman hangat kesukaanmu",
    "jalan kecil di sekitar ruangan",
    "isi jurnal sebentar",
    "rapihin meja sedikit biar pikiran lebih lega",
    "stretching ringan",
    "lihat udara luar sebentar",
    "narik diri dari kerumunan orang sebentar",
    "dengerin satu lagu yang bikin kamu nyaman",
    "cuci muka biar badan terasa lebih segar",
    "gambar atau coret-coret bebas tanpa harus bagus",
    "tulis tiga hal kecil yang berhasil kamu lewati hari ini",
    "buat camilan kecil yang gampang disiapkan",
    "lihat foto-foto yang bikin kamu merasa tenang",
]

TAKE_BREAK_ACTIVITIES = [
    "letakkan HP sebentar",
    "duduk tenang dengan posisi ternyamanmu",
    "tarik napas pelan 3 kali tanpa memikirkan agenda berikutnya",
    "pejamkan mata sambil membiarkan badan istirahat sebentar",
    "minum air pelan-pelan tapi jangan multitasking",
    "diam di tempat yang lebih sepi beberapa menit",
    "sandarkan badan dan lepas tegang di bahu",
    "ambil jeda tanpa merasa harus langsung produktif lagi",
    "biarkan diri kamu tidak membuka chat dulu beberapa menit",
    "atur napas sambil menghitung pelan sampai sepuluh",
    "jauhkan diri sebentar dari layar laptop atau HP",
    "duduk diam sambil menatap satu titik yang netral",
    "berhenti sebentar dari obrolan yang menguras energi",
    "beri waktu buat tubuhmu tenang sebelum lanjut aktivitas berikutnya",
]


def get_light_recovery_activities():
    activities = random.sample(LIGHT_RECOVERY_ACTIVITIES, 3)
    return f"{activities[0]}, {activities[1]}, atau {activities[2]}"


def get_take_break_activity():
    activities = random.sample(TAKE_BREAK_ACTIVITIES, 2)
    return f"{activities[0]} atau {activities[1]}"




def normalize_battery_status(status):
    status = str(status).lower().strip()

    if status == "low":
        return "LOW"
    elif status == "medium":
        return "MEDIUM"
    elif status == "high":
        return "HIGH"

    return "MEDIUM"


def format_time(dt):
    try:
        return datetime.fromisoformat(str(dt).replace("Z", "+00:00")).strftime("%H:%M")
    except Exception:
        return str(dt)




AI_INSIGHT_HIGH = [
    lambda total_events, total_duration, battery_score, **kw: (
        f"Hari ini energimu kelihatan cukup penuh. "
        f"Ada {total_events} agenda dengan total {total_duration} menit, "
        f"tapi sepertinya kamu masih punya ruang untuk menjalaninya dengan nyaman. "
        f"Have a great day ✨"
    ),
    lambda total_events, total_duration, battery_score, **kw: (
        f"Social battery-mu hari ini lagi dalam kondisi yang baik. "
        f"Dengan {total_events} kegiatan selama {total_duration} menit, "
        f"kamu masih kelihatan punya cukup energi buat banyak berinteraksi. "
        f"Jalani senyamannya kamu, ya. 🌿"
    ),
    lambda total_events, total_duration, battery_score, **kw: (
        f"Sepertinya jadwal hari ini cukup bersahabat. "
        f"Ada {total_events} aktivitas dengan total {total_duration} menit, "
        f"dan baterai sosialmu masih berada di level yang aman. "
        f"Semoga harimu menyenangkan ya. 🤍"
    ),

    lambda total_events, total_duration, battery_score, **kw: (
        f"Energimu hari ini cukup stabil. "
        f"Walaupun ada {total_events} agenda yang perlu kamu jalani, "
        f"dengan total durasi sekitar {total_duration} menit, sepertinya kamu masih bisa menjalaninya tanpa merasa kewalahan. 🍃"
    ),
    lambda total_events, total_duration, battery_score, **kw: (
        f"Sepertinya kamu punya energi sosial yang cukup untuk hari ini. "
        f"{total_events} kegiatan dengan total {total_duration} menit masih terlihat bisa kamu lalui dengan baik. "
        f"Tetap perhatikan dirimu juga di sela-sela aktivitas, ya. 🌸"
    ),
    lambda total_events, total_duration, battery_score, **kw: (
        f"Kapasitas energimu untuk berinteraksi sosial sedang dalam kondisi yang sangat baik. "
        f"Agenda hari ini ada {total_events} kegiatan selama {total_duration} menit, "
        f"dan sejauh ini energimu masih terlihat mendukung. "
        f"Semoga semuanya berjalan lancar yaa. ☁️"
    ),
    lambda total_events, total_duration, battery_score, **kw: (
        f"Hari ini energimu kelihatannya lagi bagus banget! "
        f"Dengan {total_events} agenda dan total durasi {total_duration} menit, "
        f"kamu masih punya cukup ruang untuk menikmati interaksi yang ada. 🌼"
    ),
    lambda total_events, total_duration, battery_score, **kw: (
        f"Social battery-mu masih cukup kuat hari ini. "
        f"Ada {total_events} kegiatan yang menunggu, totalnya sekitar {total_duration} menit. "
        f"Kamu bisa menjalaninya satu per satu tanpa perlu terburu-buru. 🧸"
    ),
    lambda total_events, total_duration, battery_score, **kw: (
        f"Kondisi energimu hari ini cukup baik. "
        f"Meski ada {total_events} aktivitas dengan total {total_duration} menit, "
        f"kamu masih terlihat punya kapasitas untuk menyelesaikan kegiatanmu dengan nyaman. ✨"
    ),
    lambda total_events, total_duration, battery_score, **kw: (
        f"Hari ini baterai sosialmu berada di level yang menyenangkan. "
        f"{total_events} agenda selama {total_duration} menit masih terasa cukup aman untuk energimu. "
        f"Take it easy dan enjoy, ya! 🌿"
    ),
]


AI_INSIGHT_MEDIUM = [
    lambda total_events, total_duration, battery_score, **kw: (
        f"Energimu hari ini ada di level sedang. "
        f"Dengan {total_events} kegiatan selama {total_duration} menit, "
        f"wajar kalau kamu mulai merasa sedikit lelah. "
        f"Coba beri dirimu jeda sebentar kalau ada kesempatan. ☕"
    ),
    lambda total_events, total_duration, battery_score, **kw: (
        f"Social battery-mu sedang berada di level sedang. "
        f"Hari ini ada {total_events} aktivitas dengan total {total_duration} menit, "
        f"jadi masuk akal kalau energimu mulai terasa berkurang. "
        f"Pelan-pelan saja, ya. 🌿"
    ),
    lambda total_events, total_duration, battery_score, **kw: (
        f"Hari ini sepertinya cukup menguras energimu. "
        f"Kamu punya {total_events} aktivitas selama {total_duration} menit, "
        f"jadi tubuh dan pikiranmu mungkin mulai butuh istirahat. "
        f"Jangan terlalu keras ke diri sendiri, ya. 🧸"
    ),


    lambda total_events, total_duration, battery_score, **kw: (
        f"Hari ini kelihatannya cukup menguras energimu. "
        f"Ada {total_events} agenda selama {total_duration} menit. "
        f"Jangan lupa beri ruang untuk dirimu sendiri. 🤍"
    ),
    lambda total_events, total_duration, battery_score, **kw: (
        f"Hari ini jadwalmu lumayan penuh, ya. "
        f"{total_events} aktivitas selama {total_duration} menit bisa saja terasa melelahkan, "
        f"jadi nggak apa-apa kalau kamu melanjutkan aktivitasmu secara perlahan. 🧸"
    ),
    lambda total_events, total_duration, battery_score, **kw: (
        f"Baterai sosialmu sedang berada di zona kuning. "
        f"Ada {total_events} agenda dengan total {total_duration} menit. "
        f"Ini waktu yang baik untuk mulai menjaga energi, bukan memaksakannya. 🌙"
    ),
    lambda total_events, total_duration, battery_score, **kw: (
        f"Energimu masih cukup, tapi sudah mulai terpakai banyak. "
        f"Hari ini kamu punya {total_events} kegiatan selama {total_duration} menit, "
        f"jadi coba sisipkan waktu istirahat walau sebentar. "
        f"Hal kecil juga bisa bantu kamu merasa lebih ringan dalam menjalani harimu. ☁️"
    ),
    lambda total_events, total_duration, battery_score, **kw: (
        f"Social battery-mu lagi di fase perlu diperhatikan. "
        f"Dengan {total_events} aktivitas dan total {total_duration} menit, "
        f"kamu mungkin masih bisa lanjut, tapi akan lebih baik kalau tidak memaksakan diri. 🌸"
    ),
    lambda total_events, total_duration, battery_score, **kw: (
        f"Hari ini energimu terasa cukup terpakai. "
        f"Ada {total_events} kegiatan selama {total_duration} menit, "
        f"kamu mungkin masih bisa melanjutkan aktivitasmu, tapi jangan sampai memaksakan diri. "
        f"Istirahat sebentar itu boleh banget kok. 🌸"
    ),
    lambda total_events, total_duration, battery_score, **kw: (
        f"Baterai sosialmu sedang berada di posisi menengah. "
        f"{total_events} agenda dengan total {total_duration} menit bukan hal kecil. "
        f"Jalani perlahan, dan beri dirimu waktu sebentar untuk istirahat. 🍵"
    ),
]


AI_INSIGHT_LOW = [
    lambda total_events, total_duration, battery_score, **kw: (
        f"Energimu hari ini terlihat sangat rendah. "
        f"Dengan {total_events} agenda selama {total_duration} menit, "
        f"wajar sekali kalau kamu merasa lelah. "
        f"Kalau memungkinkan, prioritaskan istirahat dan kurangi interaksi yang tidak mendesak yaa. 🌙"
    ),
    lambda total_events, total_duration, battery_score, **kw: (
        f"Social battery-mu sedang butuh diisi ulang. "
        f"Hari ini ada {total_events} kegiatan dengan total {total_duration} menit, "
        f"dan itu bisa terasa berat. "
        f"Nggak apa-apa kalau kamu butuh waktu untuk beristirahat. 🤍"
    ),
    lambda total_events, total_duration, battery_score, **kw: (
        f"Kegiatan hari ini sepertinya cukup menguras energimu. "
        f"Kamu punya {total_events} aktivitas selama {total_duration} menit, "
        f"jadi tubuh dan pikiranmu mungkin benar-benar butuh istirahat. "
        f"Jangan terlalu keras ke diri sendiri, ya. 🧸"
    ),

  
    lambda total_events, total_duration, battery_score, **kw: (
        f"Baterai sosialmu sedang berada di level rendah. "
        f"Dengan {total_events} agenda dan total durasi {total_duration} menit, "
        f"kamu sudah mengeluarkan banyak energi. "
        f"Sekarang waktunya menjaga sisa tenaga yang ada. 🍃"
    ),
    lambda total_events, total_duration, battery_score, **kw: (
        f"Energimu hari ini tampaknya sudah banyak terpakai. "
        f"{total_events} kegiatan selama {total_duration} menit bukan hal ringan. "
        f"Kalau bisa, beri dirimu ruang untuk beristirahat sebentar ya. 🕯️"
    ),
    lambda total_events, total_duration, battery_score, **kw: (
        f"Social battery-mu lagi rendah hari ini. "
        f"Dengan {total_events} agenda selama {total_duration} menit, "
        f"wajar kalau rasanya ingin berhenti sebentar dari banyak hal. "
        f"Istirahat bukan menyerah, kok. Itu cara kamu menjaga diri. 🤍"
    ),
    lambda total_events, total_duration, battery_score, **kw: (
        f"Hari ini baterai sosialmu kelihatannya hampir habis. "
        f"{total_events} aktivitas dengan total {total_duration} menit bisa terasa melelahkan, "
        f"apalagi kalau kamu harus terus berinteraksi. "
        f"Kalau ada pilihan, pilih yang paling penting dulu dan sisakan ruang untuk beristirahat ya. 🌙"
    ),
    lambda total_events, total_duration, battery_score, **kw: (
        f"Energimu sedang sangat terbatas. "
        f"Kamu sudah menghadapi {total_events} kegiatan dengan total {total_duration} menit. "
        f"Sangat wajar kalau kamu ingin menarik diri sebentar. "
        f"Kamu sudah melakukan semuanya dengan baik untuk hari ini. Jangan lupa beristirahat ya. 🤍"
    ),
    lambda total_events, total_duration, battery_score, **kw: (
        f"Hari ini baterai sosialmu terlihat hampir habis. "
        f"{total_events} aktivitas selama {total_duration} menit bisa terasa melelahkan. "
        f"Kalau ada pilihan, pilih hal yang paling penting saja dan sisakan ruang untuk beristirahat ya. 🌙"
    ),
    lambda total_events, total_duration, battery_score, **kw: (
        f"Kamu kelihatannya sudah cukup banyak mengeluarkan energi hari ini. "
        f"Dengan {total_events} kegiatan selama {total_duration} menit, "
        f"energimu mungkin sudah banyak terkuras. "
        f"Ambil jeda, tarik napas, dan jangan paksa semuanya harus sempurna, okeyy. 🧸"
    ),
]


AI_INSIGHT_TEMPLATES = {
    "HIGH": AI_INSIGHT_HIGH,
    "MEDIUM": AI_INSIGHT_MEDIUM,
    "LOW": AI_INSIGHT_LOW,
}




AI_SCORE_EXPLANATION_HIGH = [
    lambda battery_score, total_events, total_duration, social_intensity, **kw: (
        f"Skor {battery_score:.1f}/100 menunjukkan energimu masih cukup tinggi. "
        f"Hari ini ada {total_events} kegiatan dengan total {total_duration} menit, "
        f"dan intensitas sosialnya berada di {social_intensity:.1f}. "
        f"Artinya, beban interaksimu masih tergolong ringan untuk saat ini. 🌿"
    ),
    lambda battery_score, total_events, total_duration, social_intensity, **kw: (
        f"Baterai sosialmu berada di {battery_score:.1f}/100, jadi kondisimu cukup baik. "
        f"Jumlah agenda hari ini, yaitu {total_events} kegiatan selama {total_duration} menit, "
        f"masih terlihat seimbang dengan intensitas sosial {social_intensity:.1f}. ✨"
    ),
    lambda battery_score, total_events, total_duration, social_intensity, **kw: (
        f"Skor ini cukup aman karena jadwalmu belum terlalu menekan energimu. "
        f"Ada {total_events} aktivitas selama {total_duration} menit, "
        f"dengan tingkat intensitas sosial {social_intensity:.1f}. "
        f"Kamu masih punya ruang untuk menjalani hari dengan nyaman. 🍃"
    ),
]


AI_SCORE_EXPLANATION_MEDIUM = [
    lambda battery_score, total_events, total_duration, social_intensity, **kw: (
        f"Skor {battery_score:.1f}/100 menunjukkan energimu sedang berada di tengah. "
        f"Ada {total_events} kegiatan selama {total_duration} menit, "
        f"dengan intensitas sosial {social_intensity:.1f}. "
        f"Beban ini mulai terasa, tapi masih bisa kamu kelola dengan baik. 🌿"
    ),
    lambda battery_score, total_events, total_duration, social_intensity, **kw: (
        f"Baterai sosialmu ada di {battery_score:.1f}/100. "
        f"Hal ini menandakan energimu mulai terpakai oleh {total_events} aktivitas "
        f"selama {total_duration} menit, terutama dengan intensitas sosial {social_intensity:.1f}. ☕"
    ),
    lambda battery_score, total_events, total_duration, social_intensity, **kw: (
        f"Skor ini muncul karena harimu cukup terisi secara sosial. "
        f"Kamu punya {total_events} agenda dengan total {total_duration} menit, "
        f"dan tingkat interaksinya berada di {social_intensity:.1f}. "
        f"Masih aman, tapi tetap perlu dijaga ya. 🍃"
    ),
]


AI_SCORE_EXPLANATION_LOW = [
    lambda battery_score, total_events, total_duration, social_intensity, **kw: (
        f"Skor {battery_score:.1f}/100 menunjukkan energimu sedang rendah. "
        f"Hari ini ada {total_events} kegiatan selama {total_duration} menit, "
        f"dengan intensitas sosial {social_intensity:.1f}. "
        f"Jadwalmu hari ini cukup menguras energimu, jadi istirahat perlu jadi prioritas. 🌙"
    ),
    lambda battery_score, total_events, total_duration, social_intensity, **kw: (
        f"Baterai sosialmu berada di {battery_score:.1f}/100. "
        f"Kemungkinan hal ini dipengaruhi oleh {total_events} aktivitas, total {total_duration} menit, "
        f"dan intensitas interaksi {social_intensity:.1f}. "
        f"Energimu memang sedang butuh dipulihkan. 🤍"
    ),
    lambda battery_score, total_events, total_duration, social_intensity, **kw: (
        f"Skor ini menandakan hari yang cukup berat secara sosial. "
        f"Kamu punya {total_events} agenda selama {total_duration} menit, "
        f"dengan intensitas {social_intensity:.1f}. "
        f"Wajar kalau kamu merasa lelah. 🧸"
    ),
]


AI_SCORE_EXPLANATION_TEMPLATES = {
    "HIGH": AI_SCORE_EXPLANATION_HIGH,
    "MEDIUM": AI_SCORE_EXPLANATION_MEDIUM,
    "LOW": AI_SCORE_EXPLANATION_LOW,
}




RECOVERY_SUGGESTION_LIGHT_RECOVERY = [
  
    lambda slot_start, slot_end, after_event, before_event, **kw: (
        f"Energimu masih cukup baik. "
        f"Kalau bisa, manfaatkan jeda {slot_start}–{slot_end} setelah {after_event} "
        f"untuk istirahat sebentar sebelum {before_event}. "
        f"Gapapa ga perlu terlalu lama, yang penting kamu punya waktu beristirahat sebentar. 🌿"
    ),
    lambda slot_start, slot_end, after_event, before_event, **kw: (
        f"Ada jeda kecil di {slot_start}–{slot_end} setelah {after_event}. "
        f"Coba pakai waktu itu untuk minum, duduk tenang, atau sekadar menjauh dari layar "
        f"sebelum lanjut ke {before_event}. ☕"
    ),
    lambda slot_start, slot_end, after_event, before_event, **kw: (
        f"Kondisimu masih stabil, tapi jeda tetap penting. "
        f"Setelah {after_event}, kamu punya waktu {slot_start}–{slot_end}. "
        f"Gunakan untuk recharge ringan sebelum {before_event} yaa. 🍃"
    ),
    lambda slot_start, slot_end, after_event, before_event, **kw: (
        f"Sebelum masuk ke {before_event}, ada waktu kosong di {slot_start}–{slot_end} "
        f"setelah {after_event}. "
        f"Coba gunakan untuk melakukan hal kecil yang bikin kamu lebih rileks. 🤍"
    ),
    lambda slot_start, slot_end, after_event, before_event, **kw: (
        f"Jeda {slot_start}–{slot_end} setelah {after_event} bisa jadi waktu yang pas "
        f"untuk menjaga energimu tetap stabil sebelum {before_event}. "
        f"Ambil napas pelan-pelan, ya. 🌸"
    ),
    lambda slot_start, slot_end, after_event, before_event, **kw: (
        f"Energimu masih aman, jadi cukup ambil jeda ringan saja. "
        f"Manfaatkan waktu {slot_start}–{slot_end} setelah {after_event} "
        f"sebelum lanjut ke {before_event}. ☁️"
    ),
    lambda slot_start, slot_end, after_event, before_event, **kw: (
        f"Kalau ada kesempatan, isi jeda {slot_start}–{slot_end} setelah {after_event} "
        f"dengan sesuatu yang menenangkan. "
        f"Ini bisa bantu kamu tetap nyaman saat masuk ke {before_event}. 🌿"
    ),
    lambda slot_start, slot_end, after_event, before_event, **kw: (
        f"Ada ruang kecil untuk beristirahat sebentar di {slot_start}–{slot_end}. "
        f"Setelah {after_event}, coba jangan langsung buru-buru masuk ke mode aktif beraktivitas lagi sebelum {before_event}. 🧸"
    ),
    lambda slot_start, slot_end, after_event, before_event, **kw: (
        f"Jadwalmu masih bisa dikelola. "
        f"Tetap, beristirahat senjenak pada {slot_start}–{slot_end} setelah {after_event} ya "
        f"untuk menjaga energimu sebelum {before_event}. ✨"
    ),
    lambda slot_start, slot_end, after_event, before_event, **kw: (
        f"Gunakan waktu kosong {slot_start}–{slot_end} setelah {after_event} "
        f"untuk recharge energimu sebelum {before_event}. "
        f"Kadang jeda kecil sudah cukup untuk bikin hari terasa lebih ringan. 🍵"
    ),

    lambda slot_start, slot_end, after_event, before_event, **kw: (
        f"Ada jeda sebentar di {slot_start}–{slot_end} setelah {after_event}. "
        f"Kalau kamu mau, waktu ini bisa jadi momen kecil buat recharge—"
        f"{get_light_recovery_activities()} sebelum lanjut ke {before_event}. ✨"
    ),
    lambda slot_start, slot_end, after_event, before_event, **kw: (
        f"Kamu punya sedikit ruang kosong di {slot_start}–{slot_end} setelah {after_event}. "
        f"Nggak harus dipakai buat hal besar, cukup buat {get_light_recovery_activities()} "
        f"sebelum masuk ke {before_event}. 🌿"
    ),
    lambda slot_start, slot_end, after_event, before_event, **kw: (
        f"Ada jeda kecil di {slot_start}–{slot_end} setelah {after_event}. "
        f"Ini bisa jadi waktu yang enak buat {get_light_recovery_activities()}, "
        f"biar kamu punya tenaga lagi sebelum {before_event}. ☕"
    ),
    lambda slot_start, slot_end, after_event, before_event, **kw: (
        f"Setelah {after_event}, kamu punya waktu kosong di {slot_start}–{slot_end}. "
        f"Daripada langsung memaksa diri lanjut, kamu bisa pakai jeda ini buat "
        f"{get_light_recovery_activities()} sebelum {before_event}. 🤍"
    ),
    lambda slot_start, slot_end, after_event, before_event, **kw: (
        f"Jeda di {slot_start}–{slot_end} setelah {after_event} bisa kamu pakai pelan-pelan. "
        f"Nggak perlu yang berat, cukup {get_light_recovery_activities()} "
        f"supaya badan dan pikiranmu lebih siap sebelum {before_event}. 🍃"
    ),
    lambda slot_start, slot_end, after_event, before_event, **kw: (
        f"Kamu nggak harus langsung lanjut setelah {after_event}. "
        f"Ada ruang kecil di {slot_start}–{slot_end} yang bisa dipakai buat "
        f"{get_light_recovery_activities()}. Setelah itu, baru lanjut ke {before_event}. ✨"
    ),
    lambda slot_start, slot_end, after_event, before_event, **kw: (
        f"Di antara {after_event} dan {before_event}, ada jeda di {slot_start}–{slot_end}. "
        f"Ini bisa jadi waktu kecil buat balikin energi, misalnya dengan "
        f"{get_light_recovery_activities()}. 🌿"
    ),
    lambda slot_start, slot_end, after_event, before_event, **kw: (
        f"Sebelum masuk ke {before_event}, kamu punya jeda setelah {after_event}. "
        f"Pakai waktu {slot_start}–{slot_end} ini buat hal yang ringan aja, seperti "
        f"{get_light_recovery_activities()}. ☁️"
    ),
]


RECOVERY_SUGGESTION_TAKE_BREAK = [

    lambda slot_start, slot_end, after_event, before_event, recovery_duration, **kw: (
        f"Kamu punya sekitar {recovery_duration} menit di {slot_start}–{slot_end} setelah {after_event}. "
        f"Ini waktu yang pas untuk benar-benar berhenti sebentar sebelum {before_event}. "
        f"Coba jauhkan notifikasi dan beri ruang untuk dirimu. 🌙"
    ),
    lambda slot_start, slot_end, after_event, before_event, recovery_duration, **kw: (
        f"Ambil jeda dulu, ya. "
        f"Ada {recovery_duration} menit kosong di {slot_start}–{slot_end} setelah {after_event}. "
        f"Sebelum lanjut ke {before_event}, kamu boleh istirahat tanpa harus merasa bersalah. 🤍"
    ),
    lambda slot_start, slot_end, after_event, before_event, recovery_duration, **kw: (
        f"Setelah {after_event}, ada waktu {slot_start}–{slot_end} yang bisa kamu pakai untuk pulih. "
        f"Gunakan sekitar {recovery_duration} menit itu untuk duduk tenang, minum, atau diam sebentar "
        f"sebelum {before_event}. 🍃"
    ),
    lambda slot_start, slot_end, after_event, before_event, recovery_duration, **kw: (
        f"Energimu butuh jeda yang lebih nyata. "
        f"Manfaatkan {recovery_duration} menit di {slot_start}–{slot_end} setelah {after_event} "
        f"sebelum masuk ke {before_event}. 🧸"
    ),
    lambda slot_start, slot_end, after_event, before_event, recovery_duration, **kw: (
        f"Jeda {recovery_duration} menit di {slot_start}–{slot_end} bisa sangat membantu. "
        f"Setelah {after_event}, coba beri tubuh dan pikiranmu waktu tenang sebelum {before_event}. ☁️"
    ),
    lambda slot_start, slot_end, after_event, before_event, recovery_duration, **kw: (
        f"Ada kesempatan untuk recharge di {slot_start}–{slot_end}. "
        f"Pakai {recovery_duration} menit setelah {after_event} untuk benar-benar istirahat "
        f"sebelum lanjut ke {before_event}. 🌿"
    ),
    lambda slot_start, slot_end, after_event, before_event, recovery_duration, **kw: (
        f"Sebelum {before_event}, kamu punya {recovery_duration} menit untuk menarik napas setelah {after_event}. "
        f"Gunakan waktu {slot_start}–{slot_end} ini untuk menurunkan tempo sebentar. 🤍"
    ),
    lambda slot_start, slot_end, after_event, before_event, recovery_duration, **kw: (
        f"Kalau memungkinkan, jadikan {slot_start}–{slot_end} sebagai waktu istirahatmu. "
        f"Ada sekitar {recovery_duration} menit setelah {after_event}, "
        f"dan itu bisa bantu kamu masuk ke {before_event} dengan lebih tenang. 🍵"
    ),
    lambda slot_start, slot_end, after_event, before_event, recovery_duration, **kw: (
        f"Kamu nggak harus langsung lanjut terus. "
        f"Setelah {after_event}, ada {recovery_duration} menit di {slot_start}–{slot_end}. "
        f"Pakai untuk mengisi ulang energi sebelum {before_event}. 🌸"
    ),
    lambda slot_start, slot_end, after_event, before_event, recovery_duration, **kw: (
        f"Jeda ini penting. "
        f"Gunakan {recovery_duration} menit di {slot_start}–{slot_end} setelah {after_event} "
        f"untuk istirahat yang benar-benar terasa sebelum {before_event}. 🕯️"
    ),

    lambda slot_start, slot_end, after_event, before_event, recovery_duration, **kw: (
        f"Ada jeda {recovery_duration} menit di {slot_start}–{slot_end} setelah {after_event}. "
        f"Sebelum lanjut ke {before_event}, coba pakai waktu ini buat {get_take_break_activity()}. "
        f"Nggak perlu produktif dulu, yang penting kamu punya ruang buat napas. 🌙"
    ),
    lambda slot_start, slot_end, after_event, before_event, recovery_duration, **kw: (
        f"Kamu punya waktu sekitar {recovery_duration} menit di {slot_start}–{slot_end} "
        f"setelah {after_event}. Kalau memungkinkan, pakai jeda ini buat {get_take_break_activity()} "
        f"sebelum masuk ke {before_event}. Pelan-pelan aja dulu. 🧸"
    ),
    lambda slot_start, slot_end, after_event, before_event, recovery_duration, **kw: (
        f"Setelah {after_event}, ada jeda {recovery_duration} menit di {slot_start}–{slot_end}. "
        f"Ini waktu yang pas buat {get_take_break_activity()}. "
        f"Sebelum {before_event}, kasih dirimu kesempatan buat tenang sebentar. 🌿"
    ),
    lambda slot_start, slot_end, after_event, before_event, recovery_duration, **kw: (
        f"Jeda {recovery_duration} menit di {slot_start}–{slot_end} ini bisa kamu pakai untuk berhenti sebentar. "
        f"Setelah {after_event}, coba {get_take_break_activity()} dulu "
        f"sebelum lanjut ke {before_event}. 🤍"
    ),
    lambda slot_start, slot_end, after_event, before_event, recovery_duration, **kw: (
        f"Kamu sudah melewati {after_event}, jadi nggak apa-apa kalau ambil jeda dulu. "
        f"Di {slot_start}–{slot_end}, kamu bisa {get_take_break_activity()} "
        f"biar lebih tenang sebelum {before_event}. 🌙"
    ),
    lambda slot_start, slot_end, after_event, before_event, recovery_duration, **kw: (
        f"Sebelum lanjut ke {before_event}, coba jangan langsung memaksa diri. "
        f"Ada sekitar {recovery_duration} menit setelah {after_event}; "
        f"pakai sebentar buat {get_take_break_activity()}. 🍃"
    ),
    lambda slot_start, slot_end, after_event, before_event, recovery_duration, **kw: (
        f"Setelah {after_event}, tubuhmu mungkin butuh jeda kecil. "
        f"Di {slot_start}–{slot_end}, coba {get_take_break_activity()} dulu. "
        f"Nanti baru lanjut ke {before_event} pelan-pelan. 🧸"
    ),
]


RECOVERY_SUGGESTION_RESCHEDULE = [
    lambda move_text, **kw: (
        f"Energimu sedang cukup terbatas. "
        f"Kalau memungkinkan, pertimbangkan untuk memindahkan {move_text} ke waktu lain "
        f"supaya kamu punya ruang untuk benar-benar istirahat. 🌙"
    ),
    lambda move_text, **kw: (
        f"Hari ini sepertinya terlalu penuh untuk energimu. "
        f"Jika masih bisa diatur, coba geser {move_text} ke hari yang lebih longgar. "
        f"Menjaga diri juga bagian dari membuat keputusan yang baik. 🤍"
    ),
    lambda move_text, **kw: (
        f"Baterai sosialmu sedang rendah. "
        f"Daripada memaksakan semuanya hari ini, kamu bisa mempertimbangkan untuk menjadwalkan ulang {move_text}. 🍃"
    ),
    lambda move_text, **kw: (
        f"Kalau {move_text} tidak terlalu mendesak, mungkin lebih baik dipindahkan ke waktu lain. "
        f"Hari ini, tubuh dan pikiranmu sepertinya butuh ruang untuk pulih. 🧸"
    ),
    lambda move_text, **kw: (
        f"Kamu boleh memilih untuk tidak memaksakan diri. "
        f"Pertimbangkan memindahkan {move_text} agar energimu tidak semakin terkuras hari ini. 🌿"
    ),
    lambda move_text, **kw: (
        f"Melihat kondisi energimu, akan lebih aman kalau {move_text} bisa digeser ke jadwal lain. "
        f"Memberi waktu pulih ke diri sendiri itu penting. ☁️"
    ),
    lambda move_text, **kw: (
        f"Jika ada ruang untuk mengatur ulang jadwal, coba pindahkan {move_text}. "
        f"Lebih baik hadir dengan energi yang cukup di lain waktu daripada memaksakan diri sekarang. 🤍"
    ),
    lambda move_text, **kw: (
        f"Energimu sedang minta diprioritaskan. "
        f"Kalau bisa, jadwalkan ulang {move_text} dan gunakan waktu yang ada untuk istirahat. 🌙"
    ),
    lambda move_text, **kw: (
        f"Hari ini kamu tidak harus menanggung semuanya sekaligus. "
        f"Pertimbangkan untuk menggeser {move_text} supaya beban sosialmu lebih ringan. 🍵"
    ),
    lambda move_text, **kw: (
        f"Kalau memungkinkan, pindahkan {move_text} ke waktu yang lebih nyaman. "
        f"Keputusan seperti ini bukan berarti kamu gagal, tapi kamu sedang menjaga kapasitas dirimu. 🕯️"
    ),
]

RECOVERY_SUGGESTION_EMPTY_DAY = [
    "Hari ini jadwalmu masih kosong, jadi energimu terlihat sangat aman. "
    "Kamu bisa pakai waktu ini untuk hal ringan yang bikin nyaman, "
    "atau sekadar menikmati hari tanpa terburu-buru. 🌿",

    "Belum ada agenda yang tercatat hari ini. "
    "Social battery-mu masih penuh, jadi kamu punya ruang yang cukup luas "
    "untuk beristirahat, melakukan hal yang kamu suka, atau menyiapkan diri pelan-pelan. ✨",

    "Hari ini belum ada aktivitas sosial yang masuk kalender. "
    "Ini tanda bagus kalau energimu masih terjaga. "
    "Manfaatkan harimu dengan santai dan tetap beri ruang buat diri sendiri. 🤍",

    "Sepertinya hari ini masih cukup kosong dari aktivitas sosial. "
    "Energimu masih aman, jadi kamu bisa menjalaninya dengan lebih santai "
    "tanpa merasa harus terburu-buru. 🍃",

    "Belum ada jadwal yang masuk hari ini, jadi social battery-mu masih terlihat penuh. "
    "Kalau mau, kamu bisa pakai waktu ini untuk melakukan hal kecil yang bikin kamu nyaman. 🌸",
]


RECOVERY_SUGGESTION_HIGH_NO_SLOT = [
    lambda **kw: (
        f"Energimu masih cukup penuh dan jadwalmu belum terasa berat. "
        f"Kalau mau, kamu bisa pakai waktu ini untuk {get_light_recovery_activities()} "
        f"atau sekadar menikmati jeda tanpa tekanan. 🌿"
    ),

    lambda **kw: (
        f"Social battery-mu masih aman. "
        f"Tidak perlu recovery yang berat hari ini, cukup lakukan hal ringan seperti "
        f"{get_light_recovery_activities()} supaya energimu tetap stabil. ✨"
    ),

    lambda **kw: (
        f"Kondisimu masih cukup baik, jadi belum perlu mengurangi banyak hal. "
        f"Kamu bisa tetap menjaga energi dengan aktivitas ringan seperti "
        f"{get_light_recovery_activities()}. 🤍"
    ),

    lambda **kw: (
        f"Energimu masih terasa stabil. "
        f"Kalau ingin tetap nyaman sepanjang hari, kamu bisa menyisipkan hal ringan seperti "
        f"{get_light_recovery_activities()} tanpa perlu memaksakan diri. 🍃"
    ),

    lambda **kw: (
        f"Hari ini social battery-mu masih cukup kuat. "
        f"Jadi cukup jaga ritme dengan hal-hal kecil yang menyenangkan, misalnya "
        f"{get_light_recovery_activities()}. 🌸"
    ),
]





def get_ai_insight(ai_payload):
    battery_status = normalize_battery_status(ai_payload.get("batteryStatus", "medium"))
    total_events = int(ai_payload.get("totalEvents", 0))
    total_duration = int(ai_payload.get("totalDurationMinutes", 0))
    battery_score = float(ai_payload.get("batteryScore", 50))

    template = random.choice(AI_INSIGHT_TEMPLATES[battery_status])

    return template(
        total_events=total_events,
        total_duration=total_duration,
        battery_score=battery_score,
    )


def get_ai_score_explanation(ai_payload):
    battery_status = normalize_battery_status(ai_payload.get("batteryStatus", "medium"))
    battery_score = float(ai_payload.get("batteryScore", 50))
    total_events = int(ai_payload.get("totalEvents", 0))
    total_duration = int(ai_payload.get("totalDurationMinutes", 0))
    social_intensity = float(ai_payload.get("socialIntensityScore", 0))

    template = random.choice(AI_SCORE_EXPLANATION_TEMPLATES[battery_status])

    return template(
        battery_score=battery_score,
        total_events=total_events,
        total_duration=total_duration,
        social_intensity=social_intensity,
    )


def get_recovery_suggestion(ai_payload, recovery_strategy, free_slots=None, movable_events=None):
    free_slots = free_slots or []
    movable_events = movable_events or []

    total_events = int(ai_payload.get("totalEvents", 0))
    total_duration = int(ai_payload.get("totalDurationMinutes", 0))
    battery_score = float(ai_payload.get("batteryScore", 50))
    battery_status = normalize_battery_status(ai_payload.get("batteryStatus", "medium"))

    
    if total_events == 0 and total_duration == 0:
        return random.choice(RECOVERY_SUGGESTION_EMPTY_DAY)

    
    if battery_status == "HIGH" and battery_score >= 80 and len(free_slots) == 0:
        template = random.choice(RECOVERY_SUGGESTION_HIGH_NO_SLOT)
        return template()

    if recovery_strategy in ["LIGHT_RECOVERY", "TAKE_BREAK"] and len(free_slots) > 0:
        best_slot = max(free_slots, key=lambda x: x.get("durationMinutes", 0))

        recovery_duration = min(30, int(best_slot.get("durationMinutes", 0)))
        slot_start = format_time(best_slot.get("startTime", ""))
        slot_end = format_time(best_slot.get("endTime", ""))
        after_event = best_slot.get("afterEvent", "aktivitas sebelumnya")
        before_event = best_slot.get("beforeEvent", "aktivitas berikutnya")

        if recovery_strategy == "LIGHT_RECOVERY":
            template = random.choice(RECOVERY_SUGGESTION_LIGHT_RECOVERY)
            return template(
                slot_start=slot_start,
                slot_end=slot_end,
                after_event=after_event,
                before_event=before_event,
            )

        if recovery_strategy == "TAKE_BREAK":
            template = random.choice(RECOVERY_SUGGESTION_TAKE_BREAK)
            return template(
                slot_start=slot_start,
                slot_end=slot_end,
                after_event=after_event,
                before_event=before_event,
                recovery_duration=recovery_duration,
            )

    if recovery_strategy == "RESCHEDULE_ACTIVITY" and len(movable_events) > 0:
        titles = []

        for event in movable_events[:3]:
            title = event.get("title", "aktivitas")
            start = format_time(event.get("startTime", ""))
            end = format_time(event.get("endTime", ""))

            if start and end:
                titles.append(f"{title} ({start}–{end})")
            else:
                titles.append(title)

        if len(titles) == 1:
            move_text = titles[0]
        elif len(titles) == 2:
            move_text = f"{titles[0]} dan {titles[1]}"
        else:
            move_text = f"{titles[0]}, {titles[1]}, dan {titles[2]}"

        template = random.choice(RECOVERY_SUGGESTION_RESCHEDULE)
        return template(move_text=move_text)

    return random.choice(RECOVERY_SUGGESTION_NO_SLOT)