import csv

from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render, get_object_or_404, redirect

from player.models import Player
from utils.general import transliterate_name
from system.decorators import tournament_manager_auth_required
from system.tournament_admin.forms import UploadResultsForm, TournamentForm
from tournament.models import Tournament, TournamentResult, TournamentRegistration, OnlineTournamentRegistration


@login_required
@user_passes_test(lambda u: u.is_superuser)
def new_tournaments(request):
    tournaments = Tournament.objects.filter(is_upcoming=True).order_by('start_date')
    return render(request, 'tournament_admin/new_tournaments.html', {
        'tournaments': tournaments
    })


@login_required
@user_passes_test(lambda u: u.is_superuser)
def upload_results(request, tournament_id):
    tournament = get_object_or_404(Tournament, id=tournament_id)
    form = UploadResultsForm()

    not_found_users = []
    file_was_uploaded = False
    success = False

    if request.POST:
        form = UploadResultsForm(request.POST, request.FILES)
        if form.is_valid():
            file_was_uploaded = True

            csv_file = form.cleaned_data['csv_file']

            is_ema = form.cleaned_data['ema']
            decoded_file = csv_file.read().decode('utf-8').splitlines()
            reader = csv.DictReader(decoded_file)

            filtered_results = []
            for row in reader:
                place = row['place']
                name = row.get('name', '')
                scores = row['scores']

                ema_id = row.get('ema', '').strip()

                if is_ema:
                    first_name = row['first_name'].title()
                    last_name = row['last_name'].title()
                else:
                    temp = name.split(' ')

                    if form.cleaned_data['switch_names']:
                        first_name = temp[0].title()
                        last_name = temp[1].title()
                    else:
                        first_name = temp[1].title()
                        last_name = temp[0].title()

                    if first_name == 'Замены':
                        first_name = 'замены'

                data = [place, first_name, last_name, scores, ema_id]

                filtered_results.append(data)

                try:
                    if is_ema:
                        if ema_id:
                            Player.all_objects.get(ema_id=ema_id)
                        else:
                            Player.all_objects.get(first_name_en=first_name, last_name_en=last_name)
                    else:
                        Player.all_objects.get(first_name_ru=first_name, last_name_ru=last_name)
                except Player.DoesNotExist:
                    if is_ema:
                        not_found_users.append(
                            '{} {} {}'.format(
                                first_name,
                                last_name,
                                ema_id
                            )
                        )
                    else:
                        not_found_users.append(
                            '{} {} {} {}'.format(
                                transliterate_name(first_name),
                                first_name,
                                transliterate_name(last_name),
                                last_name,
                            )
                        )

            # everything is fine
            if not not_found_users:
                for result in filtered_results:
                    place = result[0]
                    first_name = result[1]
                    last_name = result[2]
                    scores = result[3]
                    ema_id = result[4]

                    if is_ema:
                        if ema_id:
                            player = Player.all_objects.get(ema_id=ema_id)
                        else:
                            player = Player.all_objects.get(first_name_en=first_name, last_name_en=last_name)
                    else:
                        player = Player.all_objects.get(first_name_ru=first_name, last_name_ru=last_name)

                    TournamentResult.objects.create(
                        player=player,
                        tournament=tournament,
                        place=place,
                        scores=scores,
                    )

                tournament.is_upcoming = False
                tournament.number_of_players = len(filtered_results)
                tournament.save()

                success = True

    return render(request, 'tournament_admin/upload_results.html', {
        'tournament': tournament,
        'form': form,
        'not_found_users': not_found_users,
        'file_was_uploaded': file_was_uploaded,
        'success': success
    })


@login_required
@user_passes_test(lambda u: u.is_superuser or u.is_tournament_manager)
def managed_tournaments(request):
    tournaments = request.user.managed_tournaments.all().order_by('-end_date')
    return render(request, 'tournament_admin/managed_tournaments.html', {
        'tournaments': tournaments
    })


@login_required
@tournament_manager_auth_required
def tournament_manage(request, tournament_id, **kwargs):
    tournament = kwargs['tournament']

    if tournament.is_online():
        tournament_registrations = OnlineTournamentRegistration.objects.filter(tournament=tournament).order_by('-created_on')
    else:
        tournament_registrations = TournamentRegistration.objects.filter(tournament=tournament).order_by('-created_on')

    return render(request, 'tournament_admin/tournament_manage.html', {
        'tournament': tournament,
        'tournament_registrations': tournament_registrations
    })


@login_required
@tournament_manager_auth_required
def tournament_edit(request, tournament_id, **kwargs):
    tournament = kwargs['tournament']
    form = TournamentForm(instance=tournament)
    if request.POST:
        form = TournamentForm(request.POST, instance=tournament)
        if form.is_valid():
            form.save()
            return redirect(tournament_manage, tournament.id)
    return render(request, 'tournament_admin/tournament_edit.html', {
        'tournament': tournament,
        'form': form
    })


@login_required
@tournament_manager_auth_required
def toggle_registration(request, tournament_id, **kwargs):
    tournament = kwargs['tournament']
    tournament.opened_registration = not tournament.opened_registration

    # We need to publish tournament once admin open registration
    if tournament.opened_registration and tournament.is_hidden:
        tournament.is_hidden = False

    tournament.save()

    return redirect(tournament_manage, tournament.id)


@login_required
@tournament_manager_auth_required
def toggle_premoderation(request, tournament_id, **kwargs):
    tournament = kwargs['tournament']
    tournament.registrations_pre_moderation = not tournament.registrations_pre_moderation
    tournament.save()
    return redirect(tournament_manage, tournament.id)


@login_required
@tournament_manager_auth_required
def remove_registration(request, tournament_id, registration_id, **kwargs):
    tournament = kwargs['tournament']

    item_class = TournamentRegistration
    if tournament.is_online():
        item_class = OnlineTournamentRegistration

    registration = get_object_or_404(item_class, tournament=tournament, id=registration_id)
    registration.delete()
    return redirect(tournament_manage, tournament.id)


@login_required
@tournament_manager_auth_required
def toggle_highlight(request, tournament_id, registration_id, **kwargs):
    tournament = kwargs['tournament']

    registration = get_object_or_404(TournamentRegistration, tournament=tournament, id=registration_id)
    registration.is_highlighted = not registration.is_highlighted
    registration.save()

    return redirect(tournament_manage, tournament.id)


@login_required
@tournament_manager_auth_required
def approve_registration(request, tournament_id, registration_id, **kwargs):
    tournament = kwargs['tournament']

    item_class = TournamentRegistration
    if tournament.is_online():
        item_class = OnlineTournamentRegistration

    registration = get_object_or_404(item_class, tournament=tournament, id=registration_id)
    registration.is_approved = True
    registration.save()
    return redirect(tournament_manage, tournament.id)
