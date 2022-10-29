from django.shortcuts import render
from django.db.models import Sum, Q, Count
from django.db import transaction
from .models import *
from django.http import Http404, HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from .forms import *
from django.views.generic import ListView, UpdateView

menu = [
    {'title': 'Devices', 'url': 'inventory:devices'},
    {'title': 'Blueprints', 'url': 'inventory:blueprints'},
    {'title': 'BOMs', 'url': 'inventory:boms'},
    {'title': 'Parts', 'url': 'inventory:parts'},
]


def devices(request):
    if request.method == 'POST':
        form = BlueprintFormChoice(request.POST)
        if form.is_valid():
            try:
                blueprint_id = Blueprint.objects.filter(blueprint_name=form.cleaned_data['blueprints']).values('id')
                blueprint_id = blueprint_id[0]['id']
                with transaction.atomic():
                    device = Device.objects.create(blueprint_id=blueprint_id, parts_price=0)
                    result = create_device_transactions(blueprint_id=blueprint_id, device_id=device.id)
                if not result['error']:
                    device.parts_price = result['data']
                    device.save()
            except:
                form.add_error(None, result['data'])
    else:
        form = BlueprintFormChoice()
    device_list = Device.objects.order_by('-production_date')
    return render(request, 'devices.html', {'device_list': device_list, 'form': form, 'menu': menu})


def create_device_transactions(blueprint_id: int, device_id: int):
    device_price = 0
    part_list = BOM.objects.filter(blueprint=blueprint_id)
    for part in part_list:
        try:
            part_last_transaction = Inventory.objects.filter(Q(part=part.part) & Q(income__gte=part.qty)).last()
            device_price += part_last_transaction.price_per_unit * part.qty
            part_transaction = Inventory(
                part=part.part,
                usage=part.qty,
                income=0,
                price_per_unit=0,
                device_id=device_id,
                blueprint_id=blueprint_id
            )
            part_transaction.save()
        except:
            return {'error': True, 'data': 'Error creating part transaction list'}

    return {'error': False, 'data': device_price}


def parts(request):
    if request.method == 'POST':
        form = PartForm(request.POST)
        if form.is_valid():
            try:
                form.save()
            except:
                form.add_error(None, 'Part adding error')
    else:
        form = PartForm()
    part_list = Part.objects.all()
    return render(request, 'parts.html', {'part_list': part_list, 'form': form, 'menu': menu})


class PartUpdate(UpdateView):
    model = Part
    template_name = 'part_update.html'
    fields = '__all__'
    success_url = "/parts"

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['menu'] = menu
        context['title'] = 'Part update'
        return context


class BOMList(ListView):
    model = Blueprint
    template_name = 'boms.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['menu'] = menu
        context['title'] = 'BOMs'
        return context

    def get_queryset(self):
        query = Blueprint.objects.annotate(num_parts=Count('bom'))
        return query


def edit_bom(request, blueprint_id):
    if request.method == 'POST':
        form = AddPartToBOM(request.POST)
        if form.is_valid():
            try:
                form.save()
            except:
                form.add_error(None, 'Part adding error')
    else:
        form = AddPartToBOM(initial={'blueprint': blueprint_id})
    part_list = BOM.objects.filter(blueprint=blueprint_id)
    return render(request, 'bom_edit.html', {'part_list': part_list, 'menu': menu, 'form': form, 'title': 'BOM Edit', 'blueprint_id': blueprint_id})


def blueprints(request):
    if request.method == 'POST':
        form = AddBlueprintForm(request.POST)
        if form.is_valid():
            try:
                form.save()
            except:
                form.add_error(None, 'Blueprint creating error')
    else:
        form = AddBlueprintForm()
    blueprints_list = Blueprint.objects.all()
    return render(request, 'blueprints.html', {'blueprints_list': blueprints_list, 'form': form, 'menu': menu})


class InventoryList(ListView):
    model = Inventory
    template_name = 'inventory.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['menu'] = menu
        context['title'] = 'Inventory'
        return context


def remainder(request):
    if request.method == 'POST':
        form = FillInventoryForm(request.POST)
        if form.is_valid():
            try:
                form.save()
            except:
                form.add_error(None, 'Part adding error')
    else:
        form = FillInventoryForm(initial={'usage': 0, 'blueprint': None, 'device': None})
    part_list = Part.objects.annotate(res=Sum('inventory__income') - Sum('inventory__usage'))

    return render(request, 'parts_remainder.html', {'part_list': part_list, 'form': form, 'menu': menu, 'title': 'Remainder'})


def part_details(request, part_id: int):
    transaction_list = Inventory.objects.filter(part=part_id)
    measure_unit_obj = Part.objects.get(id=part_id)
    measure_unit = measure_unit_obj.measure_unit
    part_income_usage = transaction_list.aggregate(Sum('income'), Sum('usage'))
    context = [part_income_usage.get('income__sum'), part_income_usage.get('usage__sum'), measure_unit]
    return render(request, 'part_details.html', {'transaction_list': transaction_list, 'menu': menu, 'context': context})


def delete_record(request, context: str, rec_id: int):
    if context == 'parts':
        Part.objects.filter(id=rec_id).delete()
        return HttpResponseRedirect(reverse('inventory:parts'))
    elif context == 'devices':
        Device.objects.filter(id=rec_id).delete()
        return HttpResponseRedirect(reverse('inventory:devices'))
    elif context == 'blueprints':
        Blueprint.objects.filter(id=rec_id).delete()
        return HttpResponseRedirect(reverse('inventory:blueprints'))


def delete_bom_record(request, blueprint_id: int, rec_id: int):
    BOM.objects.filter(id=rec_id).delete()
    return HttpResponseRedirect(reverse('inventory:edit_bom', args=(blueprint_id,)))
