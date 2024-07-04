from django.contrib import messages
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
import django_cleanup
from django.views import View
from .models import Document
import os
import pdfplumber
from langchain_openai import OpenAIEmbeddings
from langchain.text_splitter import CharacterTextSplitter
from langchain_community.vectorstores import ElasticVectorSearch, Pinecone, Weaviate, FAISS
from langchain.chains.question_answering import load_qa_chain
from langchain_openai import OpenAI
from pathlib import Path

from .forms import DocumentForm

from pinecone import Pinecone

pc = Pinecone(api_key=os.environ['PINECONE_API_KEY'])
index = pc.Index("text-embedding-3-small")


class VaultView(View):
    @login_required
    def index(request):
        if request.method == 'POST':
            form = DocumentForm(request.POST, request.FILES)
            if form.is_valid():
                profile = form.save(commit=False)
                profile.user = request.user
                profile.save()
                VaultView.learn_document(request)
            else:
                print(form.errors)
            context = {'form': DocumentForm(), 'files': VaultView.get_vault_files(request)}
        if request.method == 'GET':
            context = {'form': DocumentForm(), 'files': VaultView.get_vault_files(request)}
        return render(request, "vault/vault.html", context)


    def get_vault_files(request):
        return (Document.objects.filter(user=request.user)
                .filter(file__isnull=False)
                )

    def delete_file(request, pk):
        get_object_or_404(Document, pk=pk).delete()
        return redirect('vault:vault')

# Vector Learning methods
    def learn_document(request):
        files = (Document.objects.filter(user=request.user).filter(file__isnull=False))
        file_to_learn = files.last()
        texts = VaultView.clean_document(file_to_learn)
        embeddings = OpenAIEmbeddings(model="text-embedding-3-small", openai_api_key=request.user.openai_api_key)
        doc_vectors = embeddings.embed_documents(texts)
        VaultView.upsert_to_pinecone(request, doc_vectors)


    def clean_document(file_to_open):
        reader = pdfplumber.open(file_to_open.file)
        raw_text = ''
        for i, page in enumerate(reader.pages):
            text = page.extract_text()
            if text:
                raw_text += text
        text_splitter = CharacterTextSplitter(
            separator="\n",
            chunk_size=1000,
            chunk_overlap=200,
            length_function=len,
        )
        reader.close()
        texts = text_splitter.split_text(raw_text)
        return texts

    def upsert_to_pinecone(request, doc_vectors):
        index.upsert(vectors=[(id, embedding) for id, embedding in zip([request.POST.get("name", "0")], doc_vectors)], namespace=request.user.email)