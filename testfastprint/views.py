from itertools import product
from django.shortcuts import render, redirect
from django.http import JsonResponse
from .service import sync_data_api
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from rest_framework.decorators import api_view
from .serializers import ProdukSerializer, KategoriSerializer, StatusSerializer
# Create your views here.
def produk(request):
    products = Produk.objects.filter(status__nama='bisa dijual')
    return render(request, 'produk.html', {'products': products})

def delete_produk(request, id):
    product = Produk.objects.filter(id=id)
    if product.exists():
        product.delete()
        # Store the success message in the session
        request.session['success'] = 'Produk berhasil dihapus!'
    else:
        request.session['error'] = 'Produk tidak ditemukan.'

    return redirect('produk')

def add_produk(request):
    if request.method == "POST":
        nama = request.POST.get('nama')
        harga = request.POST.get('harga')
        kategori_id = request.POST.get('kategoris')  # ForeignKey to Kategori
        status_id = request.POST.get('statuss')  # ForeignKey to Status

        # Validate and create the product
        if nama and harga and kategori_id and status_id:
            kategori = Kategori.objects.get(id=kategori_id)
            status = Status.objects.get(id=status_id)

            # Create the product
            Produk.objects.create(
                nama=nama,
                harga=harga,
                kategori=kategori,  # Set ForeignKey to Kategori
                status=status  # Set ForeignKey to Status
            )
            return redirect('produk')  # Redirect after successful addition
        else:
            return render(request, 'add_produk.html', {
                'kategori': Kategori.objects.all(),
                'status': Status.objects.all(),
                'error': 'All fields are required.'
            })

        # For GET request, display the form with categories and statuses
    return render(request, 'add_produk.html', {
        'kategori': Kategori.objects.all(),
        'status': Status.objects.all()
    })

from django.shortcuts import render, redirect, get_object_or_404
from .models import Produk, Kategori, Status

def edit_produk(request, id):
    # Get the product by ID or return 404 if not found
    produk = get_object_or_404(Produk, id=id)

    if request.method == 'POST':
        # Update the product with the submitted data
        produk.nama = request.POST.get('nama')
        produk.harga = request.POST.get('harga')
        produk.kategori_id = request.POST.get('kategori')
        produk.status_id = request.POST.get('status')
        produk.save()

        # Add a success message (optional)
        request.session['success'] = 'Produk berhasil diperbarui!'
        return redirect('produk')

    # Render the form with the current product values
    kategoris = Kategori.objects.all()
    statuses = Status.objects.all()

    return render(request, 'edit_produk.html', {
        'produk': produk,
        'kategoris': kategoris,
        'statuses': statuses,
    })


@csrf_exempt
def sync_data_view(request):
    if request.method == "POST":
        sync_data_api()  # Panggil fungsi untuk sinkronisasi data
        return JsonResponse({"status": "success", "message": "Data synced successfully."})

@api_view(['GET'])
def product_list(request):
    products = Produk.objects.filter(status__nama='bisa dijual')
    serializer = ProdukSerializer(products, many=True)
    return render(request,'product_serializer.html', {'products': serializer.data})

@api_view(['POST'])
def product_create(request):
    nama = request.POST.get('nama')
    harga = request.POST.get('harga')
    kategori_id = request.POST.get('kategori')
    status_id = request.POST.get('status')
    if nama and harga and kategori_id and status_id:
        kategori = Kategori.objects.get(id=kategori_id)
        status = Status.objects.get(id=status_id)
        Produk.objects.create(
            nama=nama,
            harga=harga,
            kategori=kategori,
            status=status
        )
        request.session['success'] = 'Produk berhasil diubah!'
        return redirect('produk')
    else:
        return render(request, 'add_produk.html', {
            'kategori': Kategori.objects.all(),
            'status': Status.objects.all(),
            'error': 'All fields are required.'
        })

def product_update(request, id):
    product = Produk.objects.get(id=id)
    if request.method == "POST":
        nama = request.POST.get('nama')
        harga = request.POST.get('harga')
        kategori_id = request.POST.get('kategori')
        status_id = request.POST.get('status')
        if nama and harga and kategori_id and status_id:
            kategori = Kategori.objects.get(id=kategori_id)
            status = Status.objects.get(id=status_id)
            product.nama = nama
            product.harga = harga
            product.kategori = kategori
            product.status = status
            product.save()

            return redirect('produk')
        else:
            return render(request, 'add_produk.html', {
                'kategori': Kategori.objects.all(),
                'status': Status.objects.all(),
                'error': 'All fields are required.'
            })

def product_delete(request, id):
    product = Produk.objects.get(id=id)
    if request.method == "POST":
        product.delete()
        request.session['success'] = 'Produk berhasil dihapus!'
        return redirect('produk')
    else:
        return render(request, 'add_produk.html', {
            'kategori': Kategori.objects.all(),
            'status': Status.objects.all(),
            'error': 'All fields are required.'
        })
