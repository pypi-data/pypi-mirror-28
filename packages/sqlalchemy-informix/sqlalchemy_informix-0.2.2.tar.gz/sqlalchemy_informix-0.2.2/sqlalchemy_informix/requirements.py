from sqlalchemy.testing.requirements import SuiteRequirements
from sqlalchemy.testing import exclusions


class Requirements(SuiteRequirements):
    @property  # TODO/WTF
    def order_by_col_from_union(self):
        return exclusions.closed()

    @property  # TODO
    def independent_connections(self):
        return exclusions.closed()

    @property
    def autocommit(self):
        return exclusions.open()

    @property  # TODO
    def unicode_data(self):
        return exclusions.closed()

    @property
    def date_coerces_from_datetime(self):
        return exclusions.closed()

    @property
    def datetime_microseconds(self):
        return exclusions.closed()

    @property
    def time_microseconds(self):
        return exclusions.closed()

    @property
    def unbounded_varchar(self):
        return exclusions.closed()

    @property
    def precision_generic_float_type(self):
        return exclusions.closed()

    @property
    def floats_to_four_decimals(self):
        return exclusions.closed()

    @property  # TODO
    def schemas(self):
        return exclusions.closed()

    @property  # TODO
    def schema_reflection(self):
        return exclusions.closed()

    @property
    def view_column_reflection(self):
        return exclusions.open()

    @property
    def check_constraint_reflection(self):
        return exclusions.open()

    @property
    def temp_table_reflection(self):
        return exclusions.closed()

    @property
    def parens_in_union_contained_select_w_limit_offset(self):
        return exclusions.closed()

    @property
    def parens_in_union_contained_select_wo_limit_offset(self):
        return exclusions.closed()

    @property
    def empty_inserts(self):
        return exclusions.closed()

    @property
    def insert_from_select(self):
        return exclusions.closed()

    @property
    def bound_limit_offset(self):
        return exclusions.closed()

    @property
    def implicitly_named_constraints(self):
        return exclusions.open()
