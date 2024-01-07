import json
import operator
from datetime import datetime

from sqlalchemy import DateTime

from src.core import models
from src.core.models.exeptions import IncorrectFilterExeption

lookup_to_operation = {
    'gt': operator.gt,
    'gte': operator.ge,
    'lt': operator.lt,
    'lte': operator.le,
}


# to filter like in django, should be created exeptions to handle wrong
# filter input and logic should be expanded on possibility to join multiple
# tables
def get_joins_filters(model, filter):
    filter = json.loads(filter)
    joins = []
    filters = []
    try:
        for field, value in filter.items():
            filter_exp = field.split('__')
            if (lookup := filter_exp[-1]) in lookup_to_operation:
                operand = lookup_to_operation[lookup]
                filter_exp = filter_exp[:-1]
                field = field.replace(f'__{lookup}', '')
            else:
                operand = operator.eq
            if len(filter_exp) == 1:
                model_field = getattr(model, field)
                if isinstance(model_field.type, DateTime):
                    value = convert_str_to_datetime(value)
                filters.append(operand(model_field, value))
                continue
            join_table, field = field.split('__')
            join_exp = getattr(model, join_table)
            join_model = getattr(models, join_exp.prop.argument)
            joins.append(join_exp)
            model_field = getattr(join_model, field)
            filters.append(operand(model_field, value))
    except (AttributeError, ValueError):
        raise IncorrectFilterExeption
    return joins, filters


def convert_str_to_datetime(str_datetime):
    return datetime.strptime(str_datetime, '%Y-%m-%dT%H:%M:%S.%f')
