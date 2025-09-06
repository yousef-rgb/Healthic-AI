import requests
import flet as ft 

# --- إعدادات الموديل والـ API ---
MODEL = "deepseek/deepseek-chat-v3-0324"
URL = "https://openrouter.ai/api/v1/chat/completions"

SYSTEM_PROMPT = (
    "أنت مساعد طبي افتراضي ذكي. دورك أن ترد على أسئلة المستخدمين المتعلقة "
    "بأي نوع من الأمراض (حاد أو مزمن). يجب أن تقدم إجابات تشمل: \n"
    "انت عبارة عن مساعد طبي متخصص قادر على الاجابة عن اي سؤال يتعلق باي شيء يخص الطب والادوية بالاضافة الى تشخيص الامراض وطرق علاجها "
    "لو اتسالت مين الي عملك او مين الي صممك او اي سؤال في السياق دا تجاوب بانه يوسف محمد ابراهيم "
    "لو سُئلت عن أي شيء خارج المجال الطبي، رد: 'آسف، لقد صممني يوسف محمد ابراهيم على أن مساعد طبي ولست مخصصًا لهذا المجال.'"
)

API_KEY = "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"

HEADERS = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}

# --- دالة لطلب الإجابة من OpenRouter ---
def ask_openrouter(question, max_tokens=850, temperature=1.1):
    payload = {
        "model": MODEL,
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": question}
        ],
        "max_tokens": max_tokens,
        "temperature": temperature
    }

    resp = requests.post(URL, headers=HEADERS, json=payload, timeout=30)
    resp.raise_for_status()
    data = resp.json()
    return data["choices"][0]["message"]["content"]

# --- واجهة Flet ---
def main(page: ft.Page):
    page.title = "Chronic Diseases Chatbot"
    page.bgcolor = "#f2f5f9"
    page.padding = 0

    # منطقة المحادثة
    chat = ft.ListView(
        expand=True,
        spacing=10,
        padding=20,
        auto_scroll=True
    )

    # حقل الإدخال
    user_input = ft.TextField(
        hint_text="✍️ اكتب سؤالك عن الأمراض المزمنة...",
        autofocus=True,
        expand=True,
        border_radius=20,
        filled=True,
        bgcolor="white",
        color="black",       # لون النص
        hint_style=ft.TextStyle(color="black")  # لون الـ hint
    )

    def send_question(e):
        question = user_input.value.strip()
        if not question:
            return

        # رسالة المستخدم
        chat.controls.append(
            ft.Row(
                [
                    ft.Container(
                        content=ft.Text(question, size=16, color="white"),
                        bgcolor="#4a90e2",
                        padding=12,
                        border_radius=20,
                        margin=ft.margin.only(left=50),
                    )
                ],
                alignment="end"
            )
        )
        page.update()

        try:
            answer = ask_openrouter(question)
        except Exception as err:
            answer = f"[خطأ] {err}"

        clean_answer = answer.replace("**", "")

        # رسالة البوت
        chat.controls.append(
            ft.Row(
                [
                    ft.Container(
                        content=ft.Text(clean_answer, size=16, color="black"),
                        bgcolor="#e6e6e6",
                        padding=12,
                        border_radius=20,
                        margin=ft.margin.only(right=50),
                    )
                ],
                alignment="start"
            )
        )

        user_input.value = ""
        page.update()

    # زر الإرسال
    send_btn = ft.ElevatedButton(
        text="إرسال",
        bgcolor="#4a90e2",
        color="white",
        on_click=send_question,
        style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=20))
    )

    # بناء الصفحة: شات فوق + input ثابت تحت
    page.add(
        ft.Column(
            [
                chat,
                ft.Container(
                    content=ft.Row([user_input, send_btn], spacing=10),
                    padding=10,
                    bgcolor="#f2f5f9",
                )
            ],
            expand=True
        )
    )

ft.app(main)
