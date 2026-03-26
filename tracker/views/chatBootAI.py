from rest_framework.decorators import api_view
from rest_framework.response import Response
from openai import OpenAI
import os

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

@api_view(['POST'])
def AiChat(request):
    user_msg = request.data.get("message")

    # Send request to AI model
    completion = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[
            {"role": "system", "content": "You are a helpful Budget Tracking Assistant."},
            {"role": "user", "content": user_msg}
        ]
    )

    reply = completion.choices[0].message["content"]
    return Response({"reply": reply})
