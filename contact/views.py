from django.contrib import messages
from django.shortcuts import redirect, render
from .forms import ContactForm

def contact_page(request):
    form = ContactForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        form.save(); messages.success(request, 'Your consultation request has been sent.'); return redirect('contact')
    return render(request, 'contact/contact.html', {'form': form})
