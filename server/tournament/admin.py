from django import forms
from django.contrib import admin

from tournament.models import Tournament, TournamentRegistration, OnlineTournamentRegistration, TournamentApplication, \
    TournamentResult


class TournamentForm(forms.ModelForm):

    class Meta:
        model = Tournament
        exclude = ['name', 'registration_description', 'results_description']


class TournamentAdmin(admin.ModelAdmin):
    form = TournamentForm

    prepopulated_fields = {'slug': ['name_en']}
    list_display = ['name', 'country', 'end_date', 'is_upcoming']
    list_filter = ['tournament_type','need_qualification', 'country']
    search_fields = ['name_ru', 'name_en']

    ordering = ['-end_date']

    filter_horizontal = ['clubs']

    def changelist_view(self, request, extra_context=None):
        ref = request.META.get('HTTP_REFERER','')
        if '/?' not in ref:
            q = request.GET.copy()
            q['country__id__exact'] = 9
            request.GET = q
            request.META['QUERY_STRING'] = request.GET.urlencode()
        return super(TournamentAdmin,self).changelist_view(request, extra_context=extra_context)


class TournamentRegistrationAdmin(admin.ModelAdmin):
    list_display = ['id', 'is_approved', 'tournament', 'first_name', 'last_name', 'city', 'phone', 'player',
                    'city_object', 'allow_to_save_data']

    raw_id_fields = ['tournament', 'player', 'city_object']


class OnlineTournamentRegistrationAdmin(admin.ModelAdmin):
    list_display = ['id', 'is_approved', 'tournament', 'first_name', 'last_name', 'city', 'tenhou_nickname',
                    'contact', 'player', 'city_object', 'allow_to_save_data']

    raw_id_fields = ['tournament', 'player', 'city_object']


class TournamentApplicationAdmin(admin.ModelAdmin):
    list_display = ['tournament_name', 'city', 'start_date', 'created_on']


class TournamentResultAdmin(admin.ModelAdmin):
    list_display = ['tournament', 'player', 'place', 'scores']
    search_fields = ['tournament__name', 'player__last_name_ru', 'player__first_name_ru', 'player__last_name_en',
                     'player__first_name_en']
    raw_id_fields = ['tournament', 'player']


admin.site.register(Tournament, TournamentAdmin)
admin.site.register(TournamentRegistration, TournamentRegistrationAdmin)
admin.site.register(OnlineTournamentRegistration, OnlineTournamentRegistrationAdmin)
admin.site.register(TournamentApplication, TournamentApplicationAdmin)
admin.site.register(TournamentResult, TournamentResultAdmin)
