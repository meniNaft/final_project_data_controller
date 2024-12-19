from sqlalchemy.orm import declarative_base

Base = declarative_base()
from .attack_type import AttackType
from .city import City
from .country import Country
from .event import Event
from .region import Region
from .state import State
from .sub_target_type import SubTargetType
from .sub_weapon_type import SubWeaponType
from .target_type import TargetType
from .terror_group import TerrorGroup
from .weapon_type import WeaponType
from .event_attack_type_association import event_attack_type
from .event_sub_target_type_association import event_sub_target_type
from .event_sub_weapon_type_association import event_sub_weapon_type
from .event_terror_group_association import event_terror_group
from .event_target_association import event_target
from .target import Target