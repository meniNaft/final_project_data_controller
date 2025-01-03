import toolz as t
import app.services.read_source_data_files_service as read_source_data_service
from app.db.postgres.models import Event, City, State, Country, Region, SubTargetType, TargetType, SubWeaponType, \
    WeaponType, TerrorGroup, AttackType, Target
from datetime import date, datetime
import app.db.postgres.repositories.region_repository as region_repo
import app.db.postgres.repositories.country_repository as country_repo
import app.db.postgres.repositories.state_repository as state_repo
import app.db.postgres.repositories.city_repository as city_repo
import app.db.postgres.repositories.target_repository as target_repo
import app.db.postgres.repositories.target_type_repository as target_type_repo
import app.db.postgres.repositories.sub_target_type_repository as sub_target_type_repo
import app.db.postgres.repositories.weapon_type_repository as weapon_type_repo
import app.db.postgres.repositories.sub_weapon_type_repository as sub_weapon_type_repo
import app.db.postgres.repositories.attack_type_repository as attack_type_repo
import app.db.postgres.repositories.terror_group_repository as terror_group_repo
import app.db.postgres.repositories.event_repository as event_repo
import app.db.elastic.repositories.elastic_repository as elastic_repo
import app.db.neo4j.repositories.neo4j_repository as neo4j_repo

regions_map = {}
countries_map = {}
states_map = {}
cities_map = {}
target_types_map = {}
targets_map = {}
sub_target_types_map = {}
weapon_types_map = {}
sub_weapon_types_map = {}
attack_types_map = {}
terror_groups_map = {}


def populate_maps():
    global regions_map, countries_map, states_map, cities_map
    global target_types_map, targets_map, sub_target_types_map
    global weapon_types_map, sub_weapon_types_map, attack_types_map, terror_groups_map

    regions_map = {r.name: r for r in region_repo.get_all()}
    countries_map = {c.name: c for c in country_repo.get_all()}
    states_map = {s.name: s for s in state_repo.get_all()}
    cities_map = {c.name: c for c in city_repo.get_all()}
    target_types_map = {tt.type: tt for tt in target_type_repo.get_all()}
    targets_map = {t.target: t for t in target_repo.get_all()}
    sub_target_types_map = {stt.sub_type: stt for stt in sub_target_type_repo.get_all()}
    weapon_types_map = {wt.type: wt for wt in weapon_type_repo.get_all()}
    sub_weapon_types_map = {swt.sub_type: swt for swt in sub_weapon_type_repo.get_all()}
    attack_types_map = {at.type: at for at in attack_type_repo.get_all()}
    terror_groups_map = {tg.name: tg for tg in terror_group_repo.get_all()}


def upload_data(first_file_path: str, second_file_path: str):
    populate_maps()
    print(datetime.now(), "start processing")
    events = read_source_data_service.read_csv(first_file_path)
    second_csv = read_source_data_service.read_csv(second_file_path)
    correct_keys_name = rename_keys(second_csv)
    for elem in correct_keys_name:
        convert_second_csv_date(elem)

    events.extend(correct_keys_name)
    print(datetime.now(), "csv is loaded")

    new_events = [Event(
        date=date(event['iyear'],
                  event['imonth'] if event['imonth'] > 0 else 1,
                  event['iday'] if event['iday'] > 0 else 1),
        terrorist_participants=max(event.get('nperps', 0) or 0, 0),
        civilian_killed_count=max(event.get('nkill', 0) or 0, 0),
        civilian_injured_count=max(event.get('nwound', 0) or 0, 0),
        terrorist_killed_count=max(event.get('nkillter', 0) or 0, 0),
        terrorist_injured_count=max(event.get('nwoundte', 0) or 0, 0),
        attack_motive=event.get('motive'),
        attack_description=event['summary'],
        city=get_city(event),
        sub_target_types=get_sub_target_types(event),
        sub_weapon_types=get_sub_weapon_types(event),
        terror_groups=get_terror_groups(event),
        attack_types=get_attack_types(event),
        targets=get_targets(event)
    ) for event in events]

    print(datetime.now(), "all event are ready to insert")
    insert_events_to_elastic(new_events)
    insert_events_to_neo4j(new_events)
    batch_insert(new_events, event_repo.insert_range, "postgres_insertion")
    print(datetime.now(), "complete processing")


def rename_keys(data_list):
    column_mapping = {
        'City': 'city',
        'Perpetrator': 'gname',
        'Weapon': 'weapsubtype1_txt',
        'Injuries': 'nwound',
        'Fatalities': 'nkill',
        'Description': 'summary'
    }
    return [{column_mapping.get(key, key): value for key, value in row.items()} for row in data_list]


def convert_second_csv_date(obj: dict):
    try:
        date_obj = datetime.strptime(obj['Date'], "%d-%b-%y")
    except ValueError:
        raise ValueError(f"Invalid date format: {obj['Date']}")

    obj['iyear'] = date_obj.year
    obj['imonth'] = date_obj.month
    obj['iday'] = date_obj.day


def get_city(event: dict):
    if not event['city'] or event['city'] == "Unknown":
        return None

    current_city = cities_map.get(event['city'])
    if not current_city:
        new_city = City(
            name=event.get('city'),
            lat=event.get('latitude'),
            lon=event.get('longitude'),
            state=get_state(event)
        )
        cities_map[event.get('city')] = new_city
        return new_city
    return current_city


def get_state(event: dict):
    if not event.get('provstate'):
        return None

    current_state = states_map.get(event.get('provstate'))
    if not current_state:
        new_state = State(
            name=event.get('provstate'),
            country=get_country(event)
        )
        states_map[event.get('provstate')] = new_state
        return new_state
    return current_state


def get_country(event: dict):
    current_country = countries_map.get(event['country_txt'])
    if not current_country:
        new_country = Country(
            name=event['country_txt'],
            region=get_region(event)
        )
        countries_map[event['country_txt']] = new_country
        return new_country
    return current_country


def get_region(event: dict):
    current_region = regions_map.get(event['region_txt'])
    if not current_region:
        new_region = Region(name=event['region_txt'])
        regions_map[event['region_txt']] = new_region
        return new_region
    return current_region


def get_sub_target_types(event: dict):
    sub_target_types = [s for s in [

        event.get('targsubtype1_txt'),
        event.get('targsubtype2_txt'),
        event.get('targsubtype3_txt')
    ] if s]

    current_sub_target_types = [sub_target_types_map[s] for s in sub_target_types if s in sub_target_types_map]
    if len(current_sub_target_types) == 0 and len(sub_target_types) > 0:
        new_sun_target_type_1 = SubTargetType(
            sub_type=event['targsubtype1_txt'],
            target_type=get_target_type(event['targtype1_txt'])
        ) if event['targsubtype1_txt'] else None

        new_sun_target_type_2 = SubTargetType(
            sub_type=event['targsubtype2_txt'],
            target_type=get_target_type(event['targtype2_txt'])
        ) if event['targsubtype2_txt'] else None

        new_sun_target_type_3 = SubTargetType(
            sub_type=event['targsubtype3_txt'],
            target_type=get_target_type(event['targtype3_txt'])
        ) if event['targsubtype3_txt'] else None
        new_subs = [s for s in [new_sun_target_type_1, new_sun_target_type_2, new_sun_target_type_3] if s]

        for s in new_subs:
            if s.sub_type not in sub_target_types_map:
                sub_target_types_map[s.sub_type] = s
        return new_subs
    return current_sub_target_types


def get_sub_weapon_types(event: dict):
    sub_weapon_types = [s for s in [
        event.get('weapsubtype1_txt'),
        event.get('weapsubtype2_txt'),
        event.get('weapsubtype3_txt'),
        event.get('weapsubtype4_txt')
    ] if s]
    current_sub_weapon_types = [sub_weapon_types_map.get(s) for s in sub_weapon_types if s in sub_weapon_types_map]
    if len(current_sub_weapon_types) == 0 and len(sub_weapon_types) > 0:
        new_sun_weapon_type_1 = SubWeaponType(
            sub_type=event.get('weapsubtype1_txt'),
            weapon_type=get_weapon_type(event.get('weaptype1_txt'))
        ) if event.get('weapsubtype1_txt') else None

        new_sun_weapon_type_2 = SubWeaponType(
            sub_type=event.get('weapsubtype2_txt'),
            weapon_type=get_weapon_type(event.get('weaptype2_txt'))
        ) if event.get('weapsubtype2_txt') else None

        new_sun_weapon_type_3 = SubWeaponType(
            sub_type=event.get('weapsubtype3_txt'),
            weapon_type=get_weapon_type(event.get('weaptype3_txt'))
        ) if event.get('weapsubtype3_txt') else None

        new_sun_weapon_type_4 = SubWeaponType(
            sub_type=event.get('weapsubtype4_txt'),
            weapon_type=get_weapon_type(event.get('weaptype4_txt'))
        ) if event.get('weapsubtype4_txt') else None
        new_subs = [s for s in [
            new_sun_weapon_type_1,
            new_sun_weapon_type_2,
            new_sun_weapon_type_3,
            new_sun_weapon_type_4] if s]

        for s in new_subs:
            if s.sub_type not in sub_weapon_types_map:
                sub_weapon_types_map[s.sub_type] = s
        return new_subs
    return current_sub_weapon_types


def get_terror_groups(event: dict):
    terror_groups = [tg for tg in [event.get('gname'), event.get('gname2'), event.get('gname3')] if tg]
    current_terror_groups = [terror_groups_map.get(tg) for tg in terror_groups if tg in terror_groups_map]
    if len(current_terror_groups) == 0 and len(terror_groups) > 0:
        new_terror_group_1 = TerrorGroup(name=event.get('gname')) if event.get('gname') else None
        new_terror_group_2 = TerrorGroup(name=event.get('gname2')) if event.get('gname2') else None
        new_terror_group_3 = TerrorGroup(name=event.get('gname3')) if event.get('gname3') else None
        new_terror_groups = [tg for tg in [new_terror_group_1, new_terror_group_2, new_terror_group_3] if tg]

        for tg in new_terror_groups:
            if tg.name not in terror_groups_map:
                terror_groups_map[tg.name] = tg
        return new_terror_groups
    return current_terror_groups


def get_attack_types(event: dict):
    attack_types = [at for at in [event.get('attacktype1_txt'), event.get('attacktype2_txt'), event.get('attacktype3_txt')] if at]
    current_attack_types = [attack_types_map.get(at) for at in attack_types if at in attack_types_map]
    if len(current_attack_types) == 0 and len(attack_types) > 0:
        new_attack_type_1 = AttackType(type=event.get('attacktype1_txt')) if event.get('attacktype1_txt') else None
        new_attack_type_2 = AttackType(type=event.get('attacktype2_txt')) if event.get('attacktype2_txt') else None
        new_attack_type_3 = AttackType(type=event.get('attacktype3_txt')) if event.get('attacktype3_txt') else None
        new_attack_types = [at for at in [new_attack_type_1, new_attack_type_2, new_attack_type_3] if at]

        for at in new_attack_types:
            if at.type not in attack_types_map:
                attack_types_map[at.type] = at
        return new_attack_types
    return current_attack_types


def get_targets(event: dict):
    targets = [str(t) for t in [
        event.get('target1'),
        event.get('target2'),
        event.get('target3')
    ] if t]
    current_targets = [targets_map.get(t) for t in targets if t in targets_map]
    if len(current_targets) == 0 and len(targets) > 0:
        new_target_1 = Target(target=str(event.get('target1'))) if event.get('target1') else None
        new_target_2 = Target(target=str(event.get('target2'))) if event.get('target2') else None
        new_target_3 = Target(target=str(event.get('target3'))) if event.get('target3') else None
        new_targets = [t for t in [new_target_1, new_target_2, new_target_3] if t]

        for t in new_targets:
            if t.target not in targets_map:
                targets_map[t.target] = t
        return new_targets
    return current_targets


def get_target_type(type: str):
    current_target_type = regions_map.get(type)
    if not current_target_type:
        new_target_type = TargetType(type=type)
        target_types_map[type] = new_target_type
        return new_target_type
    return current_target_type


def get_weapon_type(type: str):
    current_weapon_type = weapon_types_map.get(type)
    if not current_weapon_type:
        new_weapon_type = WeaponType(type=type)
        weapon_types_map[type] = new_weapon_type
        return new_weapon_type
    return current_weapon_type


def insert_events_to_elastic(events: list[Event]):
    arr = [{
        "body": event.attack_description if event.attack_description else '',
        "title": event.attack_motive if event.attack_motive else '',
        "lat": event.city.lat if event.city and event.city.lat else 0.0,
        "lon": event.city.lon if event.city and event.city.lon else 0.0,
        "date": event.date,
        "category": 'history',
    } for event in events]
    batch_insert(arr, elastic_repo.insert_new_documents, "elastic_insertion")


def insert_events_to_neo4j(events: list[Event]):
    arr = [{
        "City": event.city.name if event.city and hasattr(event.city, 'name') else None,
        "Country": event.city.state.country.name if event.city and event.city.state and event.city.state.country else None,
        "State": event.city.state.name if event.city and event.city.state else None,
        "Region": event.city.state.country.region.name if event.city and event.city.state and event.city.state.country and event.city.state.country.region else None,
        "Attack_type": event.attack_types[0].type if event.attack_types and event.attack_types[0] else None,
        "Target_type": event.sub_target_types[0].target_type.type if event.sub_target_types and event.sub_target_types[
            0] and event.sub_target_types[0].target_type else None,
        "Group_name": [group.name for group in event.terror_groups] if event.terror_groups else [],
        "date": event.date if event.date else None,
        "lat": event.city.lat if event.city and event.city.lat else 0.0,
        "lon": event.city.lon if event.city and event.city.lon else 0.0
    } for event in events]

    batch_insert(arr, neo4j_repo.insert_bulk_data, "neo4j_insertion")


def batch_insert(arr: list, callback, insertion_type: str):
    counter = 1
    batch_size = 1000
    for li in list(t.partition_all(batch_size, arr)):
        callback(li)
        print(datetime.now(), insertion_type, "inserted - ", counter * batch_size)
        counter += 1
