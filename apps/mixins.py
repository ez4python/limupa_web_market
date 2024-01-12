from django.contrib.auth.mixins import AccessMixin
from django.shortcuts import redirect


class NotLoginRequiredMixin(AccessMixin):

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('index_page')
        return super().dispatch(request, *args, **kwargs)
