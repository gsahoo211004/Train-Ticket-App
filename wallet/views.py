from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Wallet, PaymentSource
from .forms import AddMoneyForm

@login_required(login_url='login')
def wallet_view(request):
    wallet, created = Wallet.objects.get_or_create(user=request.user)
    form = AddMoneyForm(user=request.user, data=request.POST or None)

    if request.method == 'POST' and form.is_valid():
        amount = form.cleaned_data['amount']
        source = form.cleaned_data['source']
        new_source_type = form.cleaned_data['new_source_type']
        new_account_number = form.cleaned_data['new_account_number']
        save_source = form.cleaned_data['save_source']

        # If user is adding from a new source
        if new_source_type and new_account_number:
            if save_source:
                source = PaymentSource.objects.create(
                    user=request.user,
                    source_type=new_source_type,
                    account_number=new_account_number,
                    label=form.cleaned_data['new_label']
                )
            # Fund the wallet
            wallet.balance += amount
            wallet.save()
            messages.success(request, f"₹{amount} added to your wallet successfully!")

        elif source:
            # Fund from existing source
            wallet.balance += amount
            wallet.save()
            messages.success(request, f"₹{amount} added from {source.label or source.source_type}!")

        else:
            messages.error(request, "Please select or enter a payment source.")

        return redirect('wallet')

    sources = PaymentSource.objects.filter(user=request.user)
    return render(request, 'wallet/wallet.html', {
        'wallet': wallet,
        'form': form,
        'sources': sources,
    })