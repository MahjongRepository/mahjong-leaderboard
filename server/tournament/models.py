from django.db import models
from django.urls import reverse
from django.utils.translation import ugettext_lazy as _

from club.models import Club
from mahjong_portal.models import BaseModel
from player.models import Player
from settings.models import City, Country


class PublicTournamentManager(models.Manager):

    def get_queryset(self):
        queryset = super(PublicTournamentManager, self).get_queryset()
        return queryset.exclude(is_hidden=True)


class Tournament(BaseModel):
    RIICHI = 0
    MCR = 1

    RR = 'rr'
    CRR = 'crr'
    EMA = 'ema'
    FOREIGN_EMA = 'fema'
    OTHER = 'other'
    ONLINE = 'online'

    GAME_TYPES = [
        [RIICHI, 'Riichi'],
        [MCR, 'MCR']
    ]

    TOURNAMENT_TYPES = [
        [RR, 'rr'],
        [CRR, 'crr'],
        [EMA, 'ema'],
        [FOREIGN_EMA, 'fema'],
        [OTHER, 'other'],
        [ONLINE, 'online'],
    ]

    objects = models.Manager()
    public = PublicTournamentManager()

    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True, max_length=255)

    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField()

    number_of_sessions = models.PositiveSmallIntegerField(default=0, blank=True)
    number_of_players = models.PositiveSmallIntegerField(default=0, blank=True)

    registration_description = models.TextField(null=True, blank=True, default='')
    registration_link = models.URLField(null=True, blank=True, default='')
    results_description = models.TextField(null=True, blank=True, default='')

    clubs = models.ManyToManyField(Club, blank=True)
    country = models.ForeignKey(Country, on_delete=models.PROTECT)
    city = models.ForeignKey(City, on_delete=models.PROTECT, null=True, blank=True)

    tournament_type = models.CharField(max_length=10, choices=TOURNAMENT_TYPES, default=RR)

    is_upcoming = models.BooleanField(default=False)
    is_hidden = models.BooleanField(default=False)
    # we need it only to EMA rating, probably can be removed
    need_qualification = models.BooleanField(default=False)

    # tournament setting, tournament admin can change them
    fill_city_in_registration = models.BooleanField(default=True)
    opened_registration = models.BooleanField(default=False)
    registrations_pre_moderation = models.BooleanField(default=False)

    # Sometimes people need to leave notes in registration form
    display_notes = models.BooleanField(default=False)

    pantheon_id = models.CharField(max_length=20, null=True, blank=True)
    ema_id = models.CharField(max_length=20, null=True, blank=True)

    def __unicode__(self):
        return self.name

    def get_url(self):
        if self.is_upcoming:
            return reverse('tournament_announcement', kwargs={'slug': self.slug})
        else:
            return reverse('tournament_details', kwargs={'slug': self.slug})

    @property
    def type_badge_class(self):
        if self.is_ema():
            return 'success'

        if self.is_rr():
            return 'primary'

        if self.is_crr():
            return 'info'

        if self.is_online():
            return 'warning'

        return 'info'

    @property
    def type_help_text(self):
        if self.is_ema():
            return 'EMA, RR, CRR'

        if self.is_rr():
            return 'RR, CRR'

        if self.is_crr():
            return 'CRR'

        if self.is_online():
            return 'Online'

        return ''

    @property
    def type_display(self):
        if self.tournament_type == self.FOREIGN_EMA:
            return 'EMA'
        else:
            return self.get_tournament_type_display()

    @property
    def rating_link(self):
        if self.is_other():
            return '#'

        tournament_type = self.tournament_type
        if tournament_type == self.FOREIGN_EMA:
            tournament_type = self.EMA

        return reverse('rating', kwargs={'slug': tournament_type})

    def is_ema(self):
        return self.tournament_type == self.EMA or self.tournament_type == self.FOREIGN_EMA

    def is_rr(self):
        return self.tournament_type == self.RR

    def is_crr(self):
        return self.tournament_type == self.CRR

    def is_online(self):
        return self.tournament_type == self.ONLINE

    def is_other(self):
        return self.tournament_type == self.OTHER

    def get_tournament_registrations(self):
        if self.is_online():
            return self.online_tournament_registrations.filter(is_approved=True)
        else:
            return self.tournament_registrations.filter(is_approved=True)


class TournamentResult(BaseModel):
    tournament = models.ForeignKey(Tournament, related_name='results', on_delete=models.PROTECT)
    player = models.ForeignKey(Player, on_delete=models.PROTECT, related_name='tournament_results')
    place = models.PositiveSmallIntegerField()
    scores = models.DecimalField(default=None, decimal_places=2, max_digits=10, null=True, blank=True)
    exclude_from_rating = models.BooleanField(default=False)

    def __unicode__(self):
        return self.tournament.name

    @property
    def base_rank(self):
        number_of_players = self.tournament.number_of_players
        place = self.place

        # first place
        if place == 1:
            return 1000

        if place == number_of_players:
            return 0

        return round(((number_of_players - place) / (number_of_players - 1)) * 1000, 2)


class TournamentRegistration(BaseModel):
    tournament = models.ForeignKey(Tournament, related_name='tournament_registrations', on_delete=models.PROTECT)
    is_approved = models.BooleanField(default=True)

    first_name = models.CharField(max_length=255, verbose_name=_('First name'))
    last_name = models.CharField(max_length=255, verbose_name=_('Last name'))
    city = models.CharField(max_length=255, verbose_name=_('City'))
    phone = models.CharField(max_length=255, verbose_name=_('Phone'),
                             help_text=_('It will be visible only to the administrator'))
    additional_contact = models.CharField(max_length=255, verbose_name=_('Additional contact. Optional'),
                                          help_text=_('It will be visible only to the administrator'),
                                          default='', null=True, blank=True)

    is_highlighted = models.BooleanField(default=False)
    notes = models.TextField(null=True, blank=True, default='', verbose_name=_('Notes. Optional'),
                             help_text=_('Tell us about yourself'))

    player = models.ForeignKey(Player, null=True, blank=True, related_name='tournament_registrations')
    city_object = models.ForeignKey(City, null=True, blank=True)

    allow_to_save_data = models.BooleanField(default=False, verbose_name=_('I allow to store my personal data'))

    def __unicode__(self):
        return self.full_name

    @property
    def full_name(self):
        return u'{} {}'.format(self.last_name, self.first_name)


class OnlineTournamentRegistration(BaseModel):
    tournament = models.ForeignKey(Tournament, related_name='online_tournament_registrations', on_delete=models.PROTECT)
    is_approved = models.BooleanField(default=True)

    first_name = models.CharField(max_length=255, verbose_name=_('First name'))
    last_name = models.CharField(max_length=255, verbose_name=_('Last name'))
    city = models.CharField(max_length=255, verbose_name=_('City'))
    tenhou_nickname = models.CharField(max_length=255, verbose_name=_('Tenhou.net nickname'))
    contact = models.CharField(max_length=255, verbose_name=_('Your contact (email, phone, etc.)'),
                               help_text=_('It will be visible only to the administrator'))

    player = models.ForeignKey(Player, null=True, blank=True, related_name='online_tournament_registrations')
    city_object = models.ForeignKey(City, null=True, blank=True)

    allow_to_save_data = models.BooleanField(default=False, verbose_name=_('I allow to store my personal data'))

    class Meta:
        unique_together = ['tenhou_nickname', 'tournament']

    def __unicode__(self):
        return self.full_name

    @property
    def full_name(self):
        return u'{} {}'.format(self.last_name, self.first_name)


class TournamentApplication(BaseModel):
    tournament_name = models.CharField(max_length=255, verbose_name=_('Tournament name'))
    city = models.CharField(max_length=255, verbose_name=_('City'))
    tournament_type = models.PositiveSmallIntegerField(verbose_name=_('Tournament type'),
                                                       choices=[[0, 'CRR'], [1, 'RR'], [2, 'EMA']], default=0)
    start_date = models.CharField(max_length=255, verbose_name=_('Start date'))
    end_date = models.CharField(max_length=255, verbose_name=_('End date'), null=True, blank=True,
                                help_text=_('Leave empty if tournament has one day'))
    address = models.TextField(verbose_name=_('Address'), help_text=_('How to reach your tournament venue'))
    additional_info_link = models.URLField(null=True, blank=True,
                                           verbose_name=_('Link to additional tournament information'))

    organizer_name = models.CharField(max_length=255, verbose_name=_('Organizer name'))
    organizer_phone = models.CharField(max_length=255, verbose_name=_('Organizer phone'))
    organizer_additional_contact = models.CharField(max_length=255, verbose_name=_('Organizer additional contact'),
                                                    null=True, blank=True,
                                                    help_text=_('Email, link to vk or something else'))

    referee_name = models.CharField(max_length=255, verbose_name=_('Referee name'))
    referee_phone = models.CharField(max_length=255, verbose_name=_('Referee phone'))
    referee_additional_contact = models.CharField(max_length=255, verbose_name=_('Referee additional contact'),
                                                  null=True, blank=True,
                                                  help_text=_('Email, link to vk or something else'))
    referee_english = models.PositiveSmallIntegerField(choices=[[0, _('No')], [1, _('Yes')]], default=1,
                                                       verbose_name=_('Referee english'))

    max_number_of_participants = models.PositiveSmallIntegerField(null=True, blank=True,
                                                                  verbose_name=_('Max number of participants'))
    number_of_games = models.PositiveSmallIntegerField(verbose_name=_('Number of hanchans'))
    entry_fee = models.PositiveSmallIntegerField(null=True, blank=True, verbose_name=_('Entry fee'),
                                                 help_text=_('Leave empty if it is free tournament'))
    pantheon_needed = models.PositiveSmallIntegerField(choices=[[0, _('No')], [1, _('Yes')]], default=1, 
                                                       verbose_name=_('Pantheon needed'))
    rules = models.PositiveSmallIntegerField(
        verbose_name=_('Tournament rules'),
        choices=[[0, _('EMA')], [1, _('WRC')], [2, _('JPML-A')], [3, _('JPML-B')], [4, _('Other')]],
        default=0)
    registration_type = models.PositiveSmallIntegerField(choices=[[0, _('Open')], [1, _('Closed')], [2, _('Limited')]],
                                                         verbose_name=_('Registration type'),
                                                         default=0)
    additional_info = models.TextField(verbose_name=_('Additional info'), 
                                       help_text=_('More information about tournament'))
    allow_to_save_data = models.BooleanField(help_text=_('I allow to store my personal data'))

    def __unicode__(self):
        return ''
