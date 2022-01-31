from cv2 import (
    putText, imwrite, getTextSize, FONT_HERSHEY_TRIPLEX, FONT_HERSHEY_COMPLEX,
    FONT_HERSHEY_DUPLEX, FONT_HERSHEY_PLAIN, FONT_HERSHEY_SIMPLEX,
    FONT_HERSHEY_SCRIPT_SIMPLEX, FONT_HERSHEY_COMPLEX_SMALL, FONT_HERSHEY_SCRIPT_COMPLEX)
from numpy import zeros
from telegram.ext import (
    Updater, CommandHandler, CallbackQueryHandler,
    ConversationHandler, MessageHandler, Filters, CallbackContext)
from telegram import (
    InlineKeyboardButton, InlineKeyboardMarkup,
    ReplyKeyboardMarkup, ReplyKeyboardRemove, Update)

fonlar = [
    FONT_HERSHEY_TRIPLEX, FONT_HERSHEY_COMPLEX,
    FONT_HERSHEY_DUPLEX, FONT_HERSHEY_PLAIN, FONT_HERSHEY_SIMPLEX,
    FONT_HERSHEY_SCRIPT_SIMPLEX, FONT_HERSHEY_COMPLEX_SMALL, FONT_HERSHEY_SCRIPT_COMPLEX]
ranglar = {
    "oq": (250,250,250), "qora": (0,0,0), "sariq": (5,250,250),
    "ko`k": (250,5,5), "yashil": (5,250,5), "qizil": (5,5,250),
    "jigar_rang": (5,52,102), "kul_rang": (127,127,127), "pushti_rang": (250,5,250),
    "sabzi_rang": (5,102,250), "siyoh_rang": (215,5,150), "ko`k_yashil": (250,250,5)}
users = dict()

class StandartHol(object):
    def __init__(self) -> None:
        super(StandartHol, self).__init__()
        self.img_ulchm, self.orq_fon = (400,350,3), ranglar["oq"]
        self.yzv_ulchm, self.yzv_qln = 1.0, 1
        self.yzv_fon, self.yzv_rang = fonlar[6], ranglar["qora"]
    
    def uzgartir(
        self, img_ulchm:tuple=None, orq_fon:tuple=None, yzv_ulchm:float=None,
        yzv_qln:int=None, yzv_fon:int=None, yzv_rang:tuple=None
    ) -> None:
        if img_ulchm is not None:
            self.img_ulchm = img_ulchm
        if orq_fon is not None:
            self.orq_fon = orq_fon
        if yzv_ulchm is not None:
            self.yzv_ulchm = yzv_ulchm
        if yzv_qln is not None:
            self.yzv_qln = yzv_qln
        if yzv_fon is not None:
            self.yzv_fon = yzv_fon
        if yzv_rang is not None:
            self.yzv_rang = yzv_rang

yz_br, s_tnl = range(2)
s_ul, s_fn, y_fn, y_rn, y_ul, y_ql = range(2, 8)
rp_ky_rm, cn_hn_en = ReplyKeyboardRemove(), ConversationHandler.END

def start_1(update:Update, context:CallbackContext) -> None:
    usr = update.message.from_user
    print(usr, "\n")
    update.message.reply_text("yozuvni suratga o`girish uchun /surat ni bosing")
    users.setdefault(usr["id"], StandartHol())

def surat(update:Update, context:CallbackContext) -> int:
    usr_id = update.message.from_user.id
    update.message.reply_text("yozuv kiriting 🖊")
    users.setdefault(usr_id, StandartHol())
    return yz_br

def yozibBer(update:Update, context:CallbackContext) -> int:
    msg = update.message.text.splitlines()
    usr_id = update.message.from_user.id
    oby = users.get(usr_id, StandartHol())
    bush = zeros(oby.img_ulchm, "uint8")
    ulchm = getTextSize(msg[0], oby.yzv_fon, oby.yzv_ulchm, oby.yzv_qln)
    bush[:], y = oby.orq_fon, int(ulchm[0][1] * 1.2)
    for i in msg:
        putText(bush, i, (10,y), oby.yzv_fon, oby.yzv_ulchm, oby.yzv_rang, oby.yzv_qln)
        ulchm = getTextSize(i, oby.yzv_fon, oby.yzv_ulchm, oby.yzv_qln)
        y += int(ulchm[0][1] * 1.5)
    imwrite("photos/yozuv_surat.jpg", bush)
    with open("photos/yozuv_surat.jpg", "rb") as img:
        update.message.reply_document(document=img.read(), filename="yozuv_surat.jpg")
    return cn_hn_en

def sozlamalar(update:Update, context:CallbackContext) -> int:
    usr_id = update.message.from_user.id
    users.setdefault(usr_id, StandartHol())
    knopka = [
        ["surat o`lchami", "surat orqa foni"],
        ["yozuv foni", "yozuv rangi"],
        ["yozuv o`lchami", "yozuv qalinligi"],
        ["standart holat"]]
    update.message.reply_text(
        "quyidagilardan birini tanlang 👇", reply_markup=ReplyKeyboardMarkup(knopka, resize_keyboard=True))
    return s_tnl

def sozTanlov(update:Update, context:CallbackContext) -> int:
    global usr_id
    msg = update.message.text
    usr_id = update.message.from_user.id
    if (msg == "surat orqa foni") or (msg == "yozuv rangi"):
        knopka, ntj = list(), list(ranglar.keys())
        for i in range(len(ntj)):
            if i % 2 == 0: continue
            knopka.append([
                InlineKeyboardButton(ntj[i-1], callback_data=ntj[i-1]),
                InlineKeyboardButton(ntj[i], callback_data=ntj[i])])
    
    if msg == "surat o`lchami":
        update.message.reply_text(
            "surat o`lchamini kiriting \nnamuna: 350x400 (eni x bo`yi)", reply_markup=rp_ky_rm)
        return s_ul
    elif msg == "surat orqa foni":
        update.message.reply_text(
            "ranglardan birini tanlang 👇", reply_markup=InlineKeyboardMarkup(knopka))
        return s_fn
    elif msg == "yozuv foni":
        knopka = list()
        for i in range(len(fonlar)):
            if i % 2 == 0: continue
            knopka.append([
                InlineKeyboardButton(str(i), callback_data=str(i-1)),
                InlineKeyboardButton(str(i+1), callback_data=str(i))])
        with open("photos/yozuv_fonlar.jpg", "rb") as img:
            update.message.reply_photo(photo=img.read(), filename="yozuv_fonlar.jpg")
        update.message.reply_text(
            "fonlardan birini tanlang 👇", reply_markup=InlineKeyboardMarkup(knopka))
        return y_fn
    elif msg == "yozuv rangi":
        update.message.reply_text(
            "ranglardan birini tanlang 👇", reply_markup=InlineKeyboardMarkup(knopka))
        return y_rn
    elif msg == "yozuv o`lchami":
        update.message.reply_text(
            "yozuv o`lchamini kiriting \nnamuna: 0.8 yoki 1.3", reply_markup=rp_ky_rm)
        return y_ul
    elif msg == "yozuv qalinligi":
        update.message.reply_text(
            "yozuv qalinligini kiriting \nnamuna: 1 yoki 2", reply_markup=rp_ky_rm)
        return y_ql
    elif msg == "standart holat":
        users.update({usr_id: StandartHol()})
        update.message.reply_text("standart holat o`rnatildi", reply_markup=rp_ky_rm)
        return cn_hn_en

def srtUlcham(update:Update, context:CallbackContext) -> int:
    msg = update.message.text
    usr_id = update.message.from_user.id
    if ' ' in msg: msg = msg.replace(' ', '')
    if msg.count('x') == 1:
        msg = msg.split('x')
        if msg[0].isdigit() and msg[1].isdigit():
            oby = users.get(usr_id, StandartHol())
            oby.uzgartir(img_ulchm=(int(msg[1]), int(msg[0]), 3))
            users.update({usr_id: oby})
            update.message.reply_text("surat o`lchami o`zgardi")
            return cn_hn_en
    update.message.reply_text(
        "surat o`lchami kiritishga yaroqli emas \nqaytadan kiriting yoki /exit ni bosing")
    return s_ul

def srtFon(update:Update, context:CallbackContext) -> int:
    qry = update.callback_query
    qry.answer()
    qry.message.delete()
    oby = users.get(usr_id, StandartHol())
    oby.uzgartir(orq_fon=ranglar[qry.data])
    users.update({usr_id: oby})
    qry.message.reply_text("surat orqa foni o`zgardi", reply_markup=rp_ky_rm)
    return cn_hn_en

def yzvFon(update:Update, context:CallbackContext) -> int:
    qry = update.callback_query
    qry.answer()
    qry.message.delete()
    oby = users.get(usr_id, StandartHol())
    oby.uzgartir(yzv_fon=fonlar[int(qry.data)])
    users.update({usr_id: oby})
    qry.message.reply_text("yozuv foni o`zgardi", reply_markup=rp_ky_rm)
    return cn_hn_en

def yzvRang(update:Update, context:CallbackContext) -> int:
    qry = update.callback_query
    qry.answer()
    qry.message.delete()
    oby = users.get(usr_id, StandartHol())
    oby.uzgartir(yzv_rang=ranglar[qry.data])
    users.update({usr_id: oby})
    qry.message.reply_text("yozuv rangi o`zgardi", reply_markup=rp_ky_rm)
    return cn_hn_en

def yzvUlcham(update:Update, context:CallbackContext) -> int:
    msg = update.message.text
    usr_id = update.message.from_user.id
    a = msg.replace('.', '', 1) if '.' in msg else msg
    if a.isdigit():
        oby = users.get(usr_id, StandartHol())
        oby.uzgartir(yzv_ulchm=float(msg))
        users.update({usr_id: oby})
        update.message.reply_text("yozuv o`lchami o`zgardi")
        return cn_hn_en
    update.message.reply_text(
        "yozuv o`lchami kiritishga yaroqli emas \nqaytadan kiriting yoki /exit ni bosing")
    return y_ul

def yzvQanil(update:Update, context:CallbackContext) -> int:
    msg = update.message.text
    usr_id = update.message.from_user.id
    if msg.isdigit():
        oby = users.get(usr_id, StandartHol())
        oby.uzgartir(yzv_qln=int(msg))
        users.update({usr_id: oby})
        update.message.reply_text("yozuv qalinligi o`zgardi")
        return cn_hn_en
    update.message.reply_text(
        "yozuv qalinligi kiritishga yaroqli emas \nqaytadan kiriting yoki /exit ni bosing")
    return y_ql

def exit_1(update:Update, context:CallbackContext) -> int:
    update.message.reply_text("barcha amallar to`xtatildi ❎", reply_markup=rp_ky_rm)
    return cn_hn_en

soz_tnl = "^(surat o`lchami|surat orqa foni|yozuv foni|yozuv rangi|yozuv o`lchami|yozuv qalinligi|standart holat)$"
def main_1() -> None:
    upd = Updater("TOKEN")
    dsp = upd.dispatcher
    cdm_exit = CommandHandler("exit", exit_1)
    
    srt_hen = ConversationHandler(
        entry_points=[CommandHandler("surat", surat)],
        states={
            yz_br: [cdm_exit, MessageHandler(Filters.text, yozibBer)]},
        fallbacks=[CommandHandler("surat", surat), cdm_exit])
    
    soz_hen = ConversationHandler(
        entry_points=[CommandHandler("settings", sozlamalar)],
        states={
            s_tnl: [MessageHandler(Filters.regex(soz_tnl), sozTanlov)],
            s_ul: [cdm_exit, MessageHandler(Filters.text, srtUlcham)],
            s_fn: [CallbackQueryHandler(srtFon)],
            y_fn: [CallbackQueryHandler(yzvFon)],
            y_rn: [CallbackQueryHandler(yzvRang)],
            y_ul: [cdm_exit, MessageHandler(Filters.text, yzvUlcham)],
            y_ql: [cdm_exit, MessageHandler(Filters.text, yzvQanil)]},
        fallbacks=[CommandHandler("settings", sozlamalar), cdm_exit])
    
    dsp.add_handler(CommandHandler("start", start_1))
    dsp.add_handler(srt_hen)
    dsp.add_handler(soz_hen)
    
    upd.start_polling()
    upd.idle()

if __name__ == "__main__":
    main_1()
