import logging
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from fastai.vision.all import load_learner
import os
PORT = int(os.environ.get('PORT', 5000))

def start(update, context):
    update.message.reply_text(
        "Bot by @kevindegila on Twitter \n\n "
        "EN : Just send me a photo of you and I will tell you if you're wearing a mask 😏 \n"
        "FR : Envoie moi une photo de toi et je te dirai si tu portes un masque 😏"
    )


def help_command(update, context):
    update.message.reply_text('My only purpose is to tell you if you are wearing a mask. Send a photo')
    
def load_model():
    global model
    model = load_learner('model.pkl')
    print('Model loaded')
def detect_mask(update, context):
    user = update.message.from_user
    photo_file = update.message.photo[-1].get_file()
    photo_file.download('user_photo.jpg')
    
    label = model.predict('user_photo.jpg')[0]
    if label == "with_mask":
        update.message.reply_text(
            "EN: Looks like you are wearing a mask 😷. I hope you don't forget it when going out!😉 \n\n"
            "FR: On dirait que tu portes un masque 😷, J'espère que tu ne l'oublies pas quand tu sors! 😉"
        )
    else:
        update.message.reply_text(
            "EN: Looks like you are not wearing a mask 😷. Please wear one and stay safe 🙄\n\n"
            "FR: On dirait que tu ne portes pas un masque 😷. S'il te plait, va en porter un. Fais attention 🙄"
        )

def main():
    load_model()
    TOKEN = "1476148585:AAFvhNUzQZPLQPKssgSGNromrbvduAizHIk"
    updater = Updater(token = TOKEN, use_context=True)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help_command))

    dp.add_handler(MessageHandler(Filters.photo, detect_mask))
    updater.start_webhook(listen="0.0.0.0",
                          port=int(PORT),
                          url_path=TOKEN)
    updater.bot.setWebhook('https://facemaskdetectsa.herokuapp.com/' + TOKEN)
    updater.idle()

if __name__ == '__main__':
    main()