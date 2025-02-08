from fastapi import FastAPI
from main import bot

HOST = "localhost"
PORT = 8000
app = FastAPI()


@app.post("/send-message/")
async def send_message(chat_id: str, text: str):
    """Отправляет сообщение для post запроса в params передать chat_id, text"""
    try:
        await bot.send_message(chat_id=chat_id, text=text)
        return {"status": "Message sent successfully"}
    except Exception as e:
        print(e)
        return {"error": str(e)}

    
def run():
    import uvicorn
    uvicorn.run(app, host=HOST, port=PORT)

if __name__ == "__main__":
    run()