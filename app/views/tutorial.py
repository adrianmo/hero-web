from django.shortcuts import render
from django.views import View


class TutorialView(View):
    template_name = 'tutorial.html'

    def get(self, request):
        return render(request, self.template_name, {})