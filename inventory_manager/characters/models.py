# -*- coding: utf-8 -*-
import datetime

from django.contrib.auth.models import User
from django.db import models

from eve.models import Item
from eve.models import SolarSystem
from eve.models import Station

FLAGS = {
    0: (None, None),
    1: ('Wallet', 'Wallet'),
    2: ('Factory', 'Factory'),
    3: ('Wardrobe', 'Wardrobe'),
    4: ('Hangar', 'Hangar'),
    5: ('Cargo', 'Cargo'),
    6: ('Briefcase', 'Briefcase'),
    7: ('Skill', 'Skill'),
    8: ('Reward', 'Reward'),
    9: ('Connected', 'Character in station connected'),
    10: ('Disconnected', 'Character in station offline'),
    11: ('LoSlot0', 'Low power slot 1'),
    12: ('LoSlot1', 'Low power slot 2'),
    13: ('LoSlot2', 'Low power slot 3'),
    14: ('LoSlot3', 'Low power slot 4'),
    15: ('LoSlot4', 'Low power slot 5'),
    16: ('LoSlot5', 'Low power slot 6'),
    17: ('LoSlot6', 'Low power slot 7'),
    18: ('LoSlot7', 'Low power slot 8'),
    19: ('MedSlot0', 'Medium power slot 1'),
    20: ('MedSlot1', 'Medium power slot 2'),
    21: ('MedSlot2', 'Medium power slot 3'),
    22: ('MedSlot3', 'Medium power slot 4'),
    23: ('MedSlot4', 'Medium power slot 5'),
    24: ('MedSlot5', 'Medium power slot 6'),
    25: ('MedSlot6', 'Medium power slot 7'),
    26: ('MedSlot7', 'Medium power slot 8'),
    27: ('HiSlot0', 'High power slot 1'),
    28: ('HiSlot1', 'High power slot 2'),
    29: ('HiSlot2', 'High power slot 3'),
    30: ('HiSlot3', 'High power slot 4'),
    31: ('HiSlot4', 'High power slot 5'),
    32: ('HiSlot5', 'High power slot 6'),
    33: ('HiSlot6', 'High power slot 7'),
    34: ('HiSlot7', 'High power slot 8'),
    35: ('Fixed Slot',  'Fixed Slot'),
    40: ('PromenadeSlot1', 'Promenade Slot 1'),
    41: ('PromenadeSlot2', 'Promenade Slot 2'),
    42: ('PromenadeSlot3', 'Promenade Slot 3'),
    43: ('PromenadeSlot4', 'Promenade Slot 4'),
    44: ('PromenadeSlot5', 'Promenade Slot 5'),
    45: ('PromenadeSlot6', 'Promenade Slot 6'),
    46: ('PromenadeSlot7', 'Promenade Slot 7'),
    47: ('PromenadeSlot8', 'Promenade Slot 8'),
    48: ('PromenadeSlot9', 'Promenade Slot 9'),
    49: ('PromenadeSlot10', 'Promenade Slot 10'),
    50: ('PromenadeSlot11', 'Promenade Slot 11'),
    51: ('PromenadeSlot12', 'Promenade Slot 12'),
    52: ('PromenadeSlot13', 'Promenade Slot 13'),
    53: ('PromenadeSlot14', 'Promenade Slot 14'),
    54: ('PromenadeSlot15', 'Promenade Slot 15'),
    55: ('PromenadeSlot16', 'Promenade Slot 16'),
    56: ('Capsule', 'Capsule'),
    57: ('Pilot', 'Pilot'),
    58: ('Passenger', 'Passenger'),
    59: ('Boarding Gate', 'Boarding gate'),
    60: ('Crew', 'Crew'),
    61: ('Skill In Training', 'Skill in training'),
    62: ('CorpMarket', 'Corporation Market Deliveries / Returns'),
    63: ('Locked', 'Locked item, can not be moved unless unlocked'),
    64: ('Unlocked', 'Unlocked item, can be moved'),
    70: ('Office Slot 1', 'Office slot 1'),
    71: ('Office Slot 2', 'Office slot 2'),
    72: ('Office Slot 3', 'Office slot 3'),
    73: ('Office Slot 4', 'Office slot 4'),
    74: ('Office Slot 5', 'Office slot 5'),
    75: ('Office Slot 6', 'Office slot 6'),
    76: ('Office Slot 7', 'Office slot 7'),
    77: ('Office Slot 8', 'Office slot 8'),
    78: ('Office Slot 9', 'Office slot 9'),
    79: ('Office Slot 10', 'Office slot 10'),
    80: ('Office Slot 11', 'Office slot 11'),
    81: ('Office Slot 12', 'Office slot 12'),
    82: ('Office Slot 13', 'Office slot 13'),
    83: ('Office Slot 14', 'Office slot 14'),
    84: ('Office Slot 15', 'Office slot 15'),
    85: ('Office Slot 16', 'Office slot 16'),
    86: ('Bonus', 'Bonus'),
    87: ('DroneBay', 'Drone Bay'),
    88: ('Booster', 'Booster'),
    89: ('Implant', 'Implant'),
    90: ('ShipHangar', 'Ship Hangar'),
    91: ('ShipOffline', 'Ship Offline'),
    92: ('RigSlot0', 'Rig power slot 1'),
    93: ('RigSlot1', 'Rig power slot 2'),
    94: ('RigSlot2', 'Rig power slot 3'),
    95: ('RigSlot3', 'Rig power slot 4'),
    96: ('RigSlot4', 'Rig power slot 5'),
    97: ('RigSlot5', 'Rig power slot 6'),
    98: ('RigSlot6', 'Rig power slot 7'),
    99: ('RigSlot7', 'Rig power slot 8'),
    100: ('Factory Operation', 'Factory Background Operation'),
    116: ('CorpSAG2', 'Corp Security Access Group 2'),
    117: ('CorpSAG3', 'Corp Security Access Group 3'),
    118: ('CorpSAG4', 'Corp Security Access Group 4'),
    119: ('CorpSAG5', 'Corp Security Access Group 5'),
    120: ('CorpSAG6', 'Corp Security Access Group 6'),
    121: ('CorpSAG7', 'Corp Security Access Group 7'),
    122: ('SecondaryStorage', 'Secondary Storage'),
    123: ('CaptainsQuarters', 'Captains Quarters'),
    124: ('Wis Promenade', 'Wis Promenade'),
    125: ('SubSystem0', 'Sub system slot 0'),
    126: ('SubSystem1', 'Sub system slot 1'),
    127: ('SubSystem2', 'Sub system slot 2'),
    128: ('SubSystem3', 'Sub system slot 3'),
    129: ('SubSystem4', 'Sub system slot 4'),
    130: ('SubSystem5', 'Sub system slot 5'),
    131: ('SubSystem6', 'Sub system slot 6'),
    132: ('SubSystem7', 'Sub system slot 7'),
    133: ('SpecializedFuelBay', 'Specialized Fuel Bay'),
    134: ('SpecializedOreHold', 'Specialized Ore Hold'),
    135: ('SpecializedGasHold', 'Specialized Gas Hold'),
    136: ('SpecializedMineralHold', 'Specialized Mineral Hold'),
    137: ('SpecializedSalvageHold', 'Specialized Salvage Hold'),
    138: ('SpecializedShipHold', 'Specialized Ship Hold'),
    139: ('SpecializedSmallShipHold', 'Specialized Small Ship Hold'),
    140: ('SpecializedMediumShipHold', 'Specialized Medium Ship Hold'),
    141: ('SpecializedLargeShipHold', 'Specialized Large Ship Hold'),
    142: ('SpecializedIndustrialShipHold', 'Specialized Industrial Ship Hold'),
    143: ('SpecializedAmmoHold', 'Specialized Ammo Hold'),
    144: ('StructureActive', 'StructureActive'),
    145: ('StructureInactive', 'StructureInactive'),
    146: ('JunkyardReprocessed', 'This item was put into a junkyard through reprocession.'),
    147: ('JunkyardTrashed', 'This item was put into a junkyard through being trashed by its owner.'),
    148: ('SpecializedCommandCenterHold', 'Specialized Command Center Hold'),
    149: ('SpecializedPlanetaryCommoditiesHold', 'Specialized Planetary Commodities Hold'),
    150: ('PlanetSurface', 'Planet Surface'),
    151: ('SpecializedMaterialBay', 'Specialized Material Bay'),
    152: ('DustCharacterDatabank', 'Dust Character Databank'),
    153: ('DustCharacterBattle', 'Dust Character Battle'),
    154: ('QuafeBay', 'Quafe Bay'),
    155: ('FleetHangar', 'Fleet Hangar'),
}


# http://stackoverflow.com/a/8907269/1770233
def strfdelta(tdelta, fmt):
    d = {'days': tdelta.days}
    d['hours'], rem = divmod(tdelta.seconds, 3600)
    d['minutes'], d['seconds'] = divmod(rem, 60)

    return fmt.format(**d)


class ActiveOrderManager(models.Manager):

    def get_queryset(self):
        return super(ActiveOrderManager, self).get_queryset().filter(order_state='active')


class Character(models.Model):

    """
    A model representing a single character
    """
    # Relationships
    user = models.ForeignKey(User, related_name='characters')

    name = models.CharField(max_length=255)
    char_id = models.IntegerField(unique=True)
    key_id = models.IntegerField()
    v_code = models.CharField(max_length=255)

    class Meta:
        ordering = ['name']

    def get_api_key(self):
        return (self.key_id, self.v_code)

    def __unicode__(self):
        return self.name


class Asset(models.Model):

    """
    A model representing a single character
    """

    # Relationships
    character = models.ForeignKey(Character, related_name='assets')
    item = models.ForeignKey(Item, related_name='assets')
    solar_system = models.ForeignKey(SolarSystem, null=True, related_name='assets')
    station = models.ForeignKey(Station, null=True, related_name='assets')

    quantity = models.IntegerField()
    unique_item_id = models.BigIntegerField()
    flag = models.SmallIntegerField()
    flag_name = models.CharField(max_length=255)
    packaged = models.BooleanField()

    class Meta:
        ordering = ['item__type_name']

    def save(self, *args, **kwargs):
        self.flag_name = FLAGS[self.flag][1]
        super(Asset, self).save(*args, **kwargs)

    def __unicode__(self):
        return '{} ({})'.format(self.character.name, self.item.type_name)


class Order(models.Model):

    """
    A model representing a single market order
    """

    # Relationships
    character = models.ForeignKey(Character, related_name='orders')
    item = models.ForeignKey(Item, related_name='orders')
    station = models.ForeignKey(Station, related_name='orders')

    order_id = models.BigIntegerField(unique=True)
    vol_entered = models.BigIntegerField()
    vol_remaining = models.BigIntegerField()
    order_state = models.CharField(max_length=255)
    order_type = models.CharField(max_length=255)
    duration = models.IntegerField()
    price = models.FloatField()
    issued = models.DateTimeField()
    qty_threshold = models.IntegerField(null=True, blank=True)

    objects = models.Manager()
    active_orders = ActiveOrderManager()

    class Meta:
        ordering = ['-issued']

    @property
    def met_qty_threshold(self):
        return self.vol_remaining <= self.qty_threshold

    def expires_in(self):
        tdelta = (self.issued + datetime.timedelta(days=self.duration)) - datetime.datetime.utcnow()
        return strfdelta(tdelta, '{days}d {hours}h {minutes}m {seconds}s')

    def __unicode__(self):
        return 'Character: {}, Item: {}'.format(self.character.name, self.item.type_name)
