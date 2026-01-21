from django.shortcuts import get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from .models import Document
from .forms import DocumentForm, DocumentEditForm
from django.http import Http404, FileResponse
import mimetypes
from django.views.decorators.clickjacking import xframe_options_exempt
from .utils import generate_thumbnail



@login_required
def dashboard(request):
    query = request.GET.get('q', '')
    category = request.GET.get("category")

    documents = Document.objects.filter(user=request.user)

    if query:
        documents = documents.filter(title__icontains=query)
    if category:
        documents = documents.filter(category=category)

    documents = documents.order_by('-uploaded_at')

    return render(
        request,
        "locker/dashboard.html",
        {
            'documents': documents,
            'query': query
        }
    )

@login_required
def upload_document(request):
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            document = form.save(commit=False)
            document.user = request.user
            document.save()
            generate_thumbnail(document) 
            return redirect('dashboard')
        else:
            messages.error(request, "Error uploading document. Please check the form.")
    else:
        form = DocumentForm()
    return render(request, "locker/upload.html", {'form': form})

@login_required
def edit_document(request, pk):
    document = get_object_or_404(Document, pk=pk, user=request.user)

    if request.method == 'POST':
        form = DocumentEditForm(request.POST, instance=document)
        if form.is_valid():
            form.save()
            messages.success(request, "Document updated successfully.")
            return redirect('dashboard')
    else:
        form = DocumentEditForm(instance=document)

    return render(request, 'locker/edit_document.html', {
        'form': form,
        'document': document
    })

@login_required
def download_document(request, doc_id):
    try:
        doc = Document.objects.get(id=doc_id, user=request.user)
    except Document.DoesNotExist:
        raise Http404("Document not found")

    file_path = doc.file.path

    content_type, _ = mimetypes.guess_type(file_path)

    response = FileResponse(open(file_path, 'rb'), content_type=content_type, as_attachment=True)
    return response

@login_required
def delete_document(request, doc_id):
    try:
        doc = Document.objects.filter(id=doc_id, user=request.user)
    except Document.DoesNotExist:
        raise Http404("Document does not exist")
    if request.method == 'POST':
        doc.delete()
        return redirect('dashboard')
    return render(request, "locker/confirm_delete.html", {'doc': doc})

@login_required
def preview_document(request, doc_id):
    try:
        doc = Document.objects.get(id=doc_id, user=request.user)
    except Document.DoesNotExist:
        raise Http404("Document not found")
       
    file_path = doc.file.path
    content_type, _ = mimetypes.guess_type(file_path)
    preview_type = None
    if content_type:
        if content_type.startswith('image'):
            preview_type = 'image'
        elif content_type == 'application/pdf':
            preview_type = 'pdf'
    return render(request, "locker/preview.html", {'doc': doc, 'preview_type': preview_type})

@login_required
@xframe_options_exempt
def stream_pdf(request, doc_id):
    try:
        doc = Document.objects.get(id=doc_id, user=request.user)
    except Document.DoesNotExist:
        raise Http404("Document not found")

    response = FileResponse(
        open(doc.file.path, 'rb'),
        content_type='application/pdf'
    )
    response['Content-Disposition'] = f'inline; filename="{doc.file.name}"'

    return response

@login_required
def bulk_delete_confirm(request):
    if request.method == "POST":
        ids = request.POST.getlist("selected_docs")
        if ids:
            documents = Document.objects.filter(id__in=ids, user=request.user)
            return render(request, "locker/confirm_bulk_delete.html", {
                "documents": documents
            })
        else:
            messages.error(request, "No documents selected for deletion.")
            return redirect("dashboard")
    return redirect("dashboard")

@login_required
def bulk_delete(request):
    if request.method == "POST":
        ids = request.POST.getlist("doc_ids")
        docs = Document.objects.filter(id__in=ids, user=request.user)
        docs.delete()
        messages.success(request, "Selected documents deleted successfully.")
        return redirect("dashboard")
    return redirect("dashboard")