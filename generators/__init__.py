import traceback
import datetime
from datetime import datetime

import generators.constants as consts
import generators.IdGenerator as idgen
import generators.StatusGenerator as statgen
import generators.CurrencyGenerator as curgen
import generators.DirectionGenerator as dirgen
import generators.DescriptionGenerator as descgen
import generators.TagGenerator as taggen
import generators.TimestampGenerator as dategen
import generators.PriceGenerator as pricegen
import generators.VolumeGenerator as volgen
import config
import utils


def setup_generators():
    """
     Setup order data generators
     'id_generator' - fixed length ids
     'currency_generator' - id of currency pair
     'direction_generator' - id of direction
     'description_generator' - id of direction
     'tag_generator' - array of tag ids
     'date_generator' - date from constants + additive,
     that depends on orders amount, days amount, weekends
     'price_generator' - additive to currency pair value
     'volume_generator' - order volume, just integers
     'last_status_generator' - id of status of set 'rejected/partial_filled/filled'
     All data related to ids etc. can be found in generators.constants
    """
    global id_generator, currency_generator, direction_generator, description_generator, tag_generator,\
        date_generator, price_generator, volume_generator, last_status_generator,\
        date_add_sec_generator, date_add_ms_generator

    try:
        id_generator = idgen.get_sequence(orders_amount)
        currency_generator = curgen.get_sequence(orders_amount)
        direction_generator = dirgen.get_sequence(orders_amount)
        description_generator = descgen.get_sequence(orders_amount)
        tag_generator = taggen.get_arr_sequence(orders_amount)
        date_generator = dategen.get_sequence(orders_amount)
        price_generator = pricegen.get_sequence(orders_amount)
        volume_generator = volgen.get_sequence(orders_amount)
        last_status_generator = statgen.get_sequence(orders_amount)
        date_add_sec_generator = dategen.get_additive_sec_sequence(orders_amount*3)
        date_add_ms_generator = dategen.get_additive_ms_sequence(orders_amount*3)
    except:
        utils.logger.log_error(traceback.format_exc())
    else:
        utils.logger.log_info("Generators initialized successfully")


def get_tags_string(next_arr):
    """
    Convert ids array to tag string
    """
    tags = ""
    for id in next_arr:
        tags += consts.tags[id] + ','
    return tags[:-1]


def create_order(position):
    """
    Creates order with data generators
    """
    order = dict()
    try:
        currency_next = currency_generator.__next__()
        price_additive = price_generator.__next__()
        price_diff = 1 - price_additive
        volume = volume_generator.__next__()
        order["position"] = position
        order["id"] = id_generator.__next__()
        order["currency_pair"] = consts.currency_pairs[currency_next]
        order["direction"] = consts.direction[direction_generator.__next__()]
        order["description"] = consts.descriptions[description_generator.__next__()]
        order["tags"] = get_tags_string(tag_generator.__next__())
        order["initial_date"] = date_generator.__next__()
        order["init_price"] = consts.currency_values[currency_next]
        order["fill_price"] = consts.currency_values[currency_next] + price_additive
        order["init_volume"] = volume
        order["fill_volume"] = volume * price_diff
    except Exception as ex:
        raise ex
    else:
        return order


def get_orders_sequence():
    """
    Returns orders generator
    """
    utils.logger.log_info("Generating {} orders...".format(orders_amount))
    i = 0
    try:
        for i in range(orders_amount):
            order = create_order(i)
            utils.logger.log_trace(order)
            yield order
    except:
        utils.logger.log_error(traceback.format_exc())
    finally:
        utils.logger.log_info("Generated {} orders...".format(i + 1))


def get_note_date(status, order):
    """
    Returns date of order note depending on the note status:
    'New' : initial date - additive
    'To provider' : just initial date
    'Rejected/Partial filled/Filled' : initial date + additive
    """
    date = order["initial_date"]
    date_additive = date_add_sec_generator.__next__() + date_add_ms_generator.__next__()

    if status == consts.statuses[0]:
        date -= date_additive
    elif status in consts.statuses[2:4]:
        date += date_additive
    return date


def get_note_fill_values(status, order):
    """
    Returns fill price and volume of order note depending on the note status
    'New/To provider/Rejected' : zeros
    'Partial filled' : fill values
    'Filled' : initial values
    """
    if status == consts.statuses[4]:
        return order["initial_price"], order["initial_volume"]
    elif status == consts.statuses[3]:
        return order["fill_price"], order["fill_volume"]
    else:
        return 0, 0


def __is_weekend(timestamp):
    """
    Checks is timestamp weekend
    """
    return datetime.fromtimestamp(timestamp).weekday() in consts.constants["weekends"]


def create_note(status, order):
    """
    Creates note with status and status date, adds to note order data
    """
    try:
        fill_price, fill_volume = get_note_fill_values(status, order)
        timestamp = round(get_note_date(status, order), 3)
        if __is_weekend(timestamp):
            if status != consts.statuses[0]:
                old_timestamp = timestamp
                while __is_weekend(timestamp):
                    timestamp += 86400
                utils.logger.log_trace("[Order][{}] Add {} sec to timestamp: {}. Previous value {} was a weekend".format
                                       (order["id"], timestamp - old_timestamp, timestamp, old_timestamp))
        note = {
            "status": status,
            "date": timestamp,
            "fill_price": round(fill_price, config.settings["price_precision"]),
            "fill_volume": round(fill_volume, config.settings["volume_precision"])
        }
        note.update(order)
    except Exception as ex:
        raise ex
    else:
        return note


def get_red_notes(order):
    """
    Creates at least 1 order note in red zone.
    Amount depends on order zone/position:
    it may be note only with 'rejected/filled/p_filled'
    or two notes - second with 'to_provider'
    """
    try:
        result = [create_note(last_status_generator.__next__(), order)]
        if order["position"] > one_state_red_finish:
            result.append(create_note(consts.statuses[1], order))
    except Exception as ex:
        raise ex
    else:
        return result


def get_green_notes(order):
    """
    Creates 3 order notes with statuses 'new', 'to_provider' and 'rejected/filled/p_filled'
    """
    try:
        result = []
        i = 0
        while i < 3:
            result.append(create_note(consts.statuses[i], order))
            i += 1
    except Exception as ex:
        raise ex
    else:
        return result


def get_blue_notes(order):
    """
    Creates at least 1 order note in blue zone.
    Amount depends on order zone/position:
    it may be note only with 'new'
    or two notes - second with 'to_provider'
    """
    try:
        result = [create_note(consts.statuses[0], order)]
        if order["position"] <= one_state_blue_start:
            result.append(create_note(consts.statuses[1], order))
    except Exception as ex:
        raise ex
    else:
        return result


def setup():
    """

    """
    global orders_amount, red_zone_finish, green_zone_finish, blue_zone_finish, \
        one_state_red_finish, one_state_blue_start,\
        red_percent, green_percent, blue_percent, one_state_red_percent, one_state_blue_percent

    orders_amount = config.settings["orders_amount"]

    red_percent = consts.constants["zones_percent"][0]
    green_percent = consts.constants["zones_percent"][1]
    blue_percent = consts.constants["zones_percent"][2]

    one_state_red_percent = consts.constants["1-state_percent"]["Red"]
    one_state_blue_percent = consts.constants["1-state_percent"]["Blue"]

    red_zone_amount = orders_amount * red_percent
    green_zone_amount = orders_amount * green_percent
    blue_zone_amount = orders_amount * blue_percent

    red_zone_finish = red_zone_amount
    green_zone_finish = red_zone_finish + green_zone_amount
    blue_zone_finish = green_zone_finish + blue_zone_amount

    one_state_red_finish = red_zone_finish * one_state_red_percent
    one_state_blue_start = green_zone_finish + (1 - one_state_blue_percent) * blue_zone_amount


def to_sql_string(note):
    """
    Converts note into sql insert command and returns formatted string
    """
    return "insert into order_notes values({},'{}',{},'{}','{}',{},{},{},{},'{}','{}');".format(
        note["id"], note["status"], note["date"], note["currency_pair"], note["direction"],
        note["init_price"], note["fill_price"], note["init_volume"], note["fill_volume"],
        note["description"], note["tags"])


def generate_notes_from(order):
    """
    Generate notes from order depending on the order position/zone
    """
    global red_zone_finish, green_zone_finish, blue_zone_finish
    try:
        if order["position"] <= red_zone_finish:
            return get_red_notes(order)
        elif order["position"] <= green_zone_finish:
            return get_green_notes(order)
        elif order["position"] <= blue_zone_finish:
            return get_blue_notes(order)
        return None
    except:
        utils.logger.log_error(traceback.format_exc())


def get_notes_sequence(orders_sequence=get_orders_sequence()):
    """
    Returns notes generator, based on orders generator
    for 'red' and 'blue' zone orders there may be 1 or 2 notes
    depends on its position. For 'green' zone orders have all 3 notes.
    More details in get_red_notes, get_green_notes and get_blue_notes description.
    Generates about 2.2-3x order_amount notes.
    """
    setup_generators()
    utils.logger.log_info("Generating order notes...")
    i = 0
    try:
        for order in orders_sequence:
            for item in generate_notes_from(order):
                utils.logger.log_trace(item)
                i += 1
                yield to_sql_string(item)
    except:
        utils.logger.log_error(traceback.format_exc())
    finally:
        utils.logger.log_info("Generated {} order notes...".format(i))


def get_notes_amount():
    """
    Returns notes amount depending on the zone colors and 1-state percents
    """
    global red_percent, green_percent, blue_percent

    notes_amount = config.settings["orders_amount"] * (green_percent * 3 +
                                                       red_percent * (2 - one_state_red_percent) +
                                                       blue_percent * (2 - one_state_blue_percent))
    return notes_amount
