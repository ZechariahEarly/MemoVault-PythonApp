import os
import time

from django.shortcuts import render, redirect
from django.views import View
from .models import Chat
import openai
from pinecone import Pinecone

pc = Pinecone(api_key=os.environ['PINECONE_API_KEY'])
index = pc.Index("text-embedding-3-small")
limit = 3750
# Create your views here.

class ChatView(View):
    def index(request):
        messages = Chat.objects.filter(user=request.user)
        return render(request, 'chat/chat.html', {'messages': messages})

    def add_conversation(request):
        user_message = request.POST.get('message')
        prompt = ChatView.create_prompt(request)
        bot_message = ChatView.complete(prompt=prompt)
        Chat.objects.create(user_message=user_message, bot_message=bot_message)
        messages = Chat.objects.filter(user=request.user)
        return render(request, 'chat/chat.html', {'messages': messages})

    def clear_chat(request):
        Chat.objects.filter(user=request.user).delete()
        messages = Chat.objects.filter(user=request.user)
        return render(request, 'chat/chat.html', {'messages': messages})

    def create_prompt(request):
        model = "text-embedding-3-small"
        openai.api_key = request.user.openai_api_key
        query = request.POST.get('message')
        res = openai.Embedding.create(input=[query], engine=model)

        xq = res['data'][0]['embedding']

        contexts = []
        time_waited = 0
        while(len(contexts)<3 and time_waited < 60 * 12):
            res = index.query(vector=xq, top_k=2, include_metadata=True, namespace=request.user.email)
            contexts = contexts + [
                x['metadata']['text'] for x in res['matches']
            ]
            print(f"Retrieved {len(contexts)} contexts, sleeping for 15 seconds...")
            time.sleep(15)
            time_waited += 15

        if time_waited >= 60 * 12:
            print("Timed out waiting for contexts to be retrieved.")
            contexts = ["No contexts retrieved. Try to answer the question yourself!"]

        prompt_start = (
                "Answer the question based on the context below.\n\n" +
                "Context:\n"
        )
        prompt_end = (
            f"\n\nQuestion: {query}\nAnswer:"
        )
        # append contexts until hitting limit
        for i in range(1, len(contexts)):
            if len("\n\n---\n\n".join(contexts[:i])) >= limit:
                prompt = (
                        prompt_start +
                        "\n\n---\n\n".join(contexts[:i - 1]) +
                        prompt_end
                )
                break
            elif i == len(contexts) - 1:
                prompt = (
                        prompt_start +
                        "\n\n---\n\n".join(contexts) +
                        prompt_end
                )
        return prompt

    def complete(self, prompt):
        # instructions
        sys_prompt = "You are a helpful assistant that always answers questions."
        # query text-davinci-003
        res = openai.ChatCompletion.create(
            model='gpt-3.5-turbo-0613',
            messages=[
                {"role": "system", "content": sys_prompt},
                {"role": "user", "content": prompt}
            ],
            temperature=0
        )
        return res['choices'][0]['message']['content'].strip()

    def get_existing_messages(request) -> list:
        """
        Get all messages from the database and format them for the API.
        """
        formatted_messages = []

        for message in Chat.objects.filter(user=request.user).values('user_message', 'bot_message'):
            formatted_messages.append({"role": "user", "content": message['user_message']})
            formatted_messages.append({"role": "assistant", "content": message['bot_message']})

        return formatted_messages