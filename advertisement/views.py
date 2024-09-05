from django.shortcuts import render
from django.views.generic import (
    ListView, DetailView, CreateView, UpdateView, DeleteView)
from .models import Advertisement, Response, Author
from django.contrib.auth.mixins import PermissionRequiredMixin
from .forms import AdvertisementForm, ResponseForm
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404, render, redirect
from .filters import ResponseFilter
from django.core.mail import send_mail
from django.contrib.auth.decorators import login_required
from .forms import SubscriptionForm
from .models import Subscription



class AdvertisementList(ListView):
    model = Advertisement
    ordering = 'time_in'
    template_name = 'advertisements.html'
    context_object_name = 'advertisements'
    paginate_by = 10


class AdvertisementDetail(DetailView):
    model = Advertisement
    template_name = 'advertisement.html'
    context_object_name = 'advertisement'



class AdvertisementCreate(PermissionRequiredMixin, CreateView):
    permission_required = 'advertisement.add_advertisement'
    form_class = AdvertisementForm
    model = Advertisement
    template_name = 'advertisement_update.html'
    success_url = reverse_lazy('advertisement_list')

    def form_valid(self, form):
        # Находим или создаем объект Author для текущего пользователя
        author, created = Author.objects.get_or_create(name=self.request.user)

        # Присваиваем автору объявление
        form.instance.author = author

        return super().form_valid(form)


class AdvertisementUpdate(PermissionRequiredMixin, UpdateView):
    permission_required = ('advertisement.change_advertisement',)
    form_class = AdvertisementForm
    model = Advertisement
    template_name = 'advertisement_update.html'
    success_url = reverse_lazy('advertisement_list')




class AdvertisementDelete(PermissionRequiredMixin, DeleteView):
    permission_required = ('advertisement.change_advertisement',)
    model = Advertisement
    template_name = 'advertisement_delete.html'
    success_url = reverse_lazy('advertisement_list')


class ResponseList(ListView):
    model = Response
    template_name = 'responses.html'
    context_object_name = 'responses'
    paginate_by = 10

    def get_queryset(self):
        user = self.request.user

        # Проверяем, связан ли пользователь с объектом Author
        try:
            author = Author.objects.get(name=user)
        except Author.DoesNotExist:
            return Response.objects.none()

        # Получаем все объявления этого автора
        advertisements = Advertisement.objects.filter(author=author)

        # Фильтруем отклики, чтобы отображать только те, которые сделаны на объявления этого автора
        queryset = Response.objects.filter(advertisement__in=advertisements)

        # Применяем фильтр
        self.filterset = ResponseFilter(self.request.GET, queryset=queryset)

        # Проверяем, есть ли выбранное объявление в фильтре
        if self.filterset.is_valid():
            # Получаем выбранное объявление из формы фильтрации
            selected_advertisement = self.filterset.form.cleaned_data.get('advertisement')

            if selected_advertisement:
                # Если выбрано конкретное объявление, фильтруем отклики по этому объявлению
                return queryset.filter(advertisement=selected_advertisement)
            else:
                # Если не выбрано конкретное объявление, возвращаем все отклики
                return queryset

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset  # Передаем фильтр в контекст
        return context

    def post(self, request, *args, **kwargs):
        response_id = request.POST.get('response_id')
        action = request.POST.get('action')
        response = get_object_or_404(Response, id=response_id)

        # Получаем авторов и пользователей
        advertisement = response.advertisement
        author = advertisement.author
        author_user = author.name  # Получаем объект User через поле 'name'
        sender_user = response.user  # Пользователь, который отправил отклик

        if request.user == author_user:
            if action == 'accept':
                response.answer = True
                response.save()

                # Отправка email уведомления автору объявления
                send_mail(
                    subject=f'Ваш отклик принят',
                    message=f'Здравствуйте, {sender_user.username}!\n\n'
                            f'Ваш отклик на объявление "{advertisement.heading}" был принят автором.',
                    from_email='wr9va@yandex.com',
                    recipient_list=[sender_user.email],
                    fail_silently=False,
                )
            elif action == 'delete':
                response.delete()

        return redirect('responses')


class ResponseCreate(PermissionRequiredMixin, CreateView):
    permission_required = 'advertisement.add_response'
    model = Response
    form_class = ResponseForm
    template_name = 'response_create.html'
    success_url = reverse_lazy('advertisement_list')

    def form_valid(self, form):
        # Получаем идентификатор объявления из URL
        advertisement_id = self.kwargs.get('pk')

        # Проверяем, что идентификатор объявления существует
        if advertisement_id:
            # Получаем объект Advertisement или вызываем ошибку 404, если не найден
            advertisement = get_object_or_404(Advertisement, id=advertisement_id)
            form.instance.advertisement = advertisement  # Устанавливаем поле advertisement
        else:
            # Обработка ошибки, если идентификатор объявления не передан
            return self.form_invalid(form)

        form.instance.user = self.request.user  # Устанавливаем текущего пользователя

        # Сохраняем форму и получаем объект Response
        response = super().form_valid(form)

        # Отправка email уведомления владельцу объявления
        author = form.instance.advertisement.author
        author_user = author.name  # Получаем объект User через поле 'name'

        send_mail(
            subject=f'У вас новый отклик на объявление "{form.instance.advertisement.heading}"',
            message=f'Здравствуйте, {author_user.username}!\n\n'
                    f'Вы получили новый отклик от пользователя {self.request.user.username}. '
                    f'Вы можете просмотреть его на сайте.',
            from_email='wr9va@yandex.com',
            recipient_list=[author_user.email],  # Email владельца объявления
            fail_silently=False,
        )

        return response




@login_required
def subscribe_to_categories(request):
    if request.method == 'POST':
        form = SubscriptionForm(request.POST)
        if form.is_valid():
            categories = form.cleaned_data['categories']
            for category in categories:
                Subscription.objects.get_or_create(user=request.user, category=category)
            return redirect('advertisement_list')
    else:
        form = SubscriptionForm()

    return render(request, 'subscription.html', {'form': form})


