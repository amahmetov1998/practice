import datetime
from contextlib import nullcontext as does_not_raise


TEST_REPO_GET_DATES = [
    ({'date_num': 3},
     [datetime.date(2024, 4, 23),
      datetime.date(2024, 4, 22),
      datetime.date(2024, 4, 19)],
     does_not_raise())
]

TEST_REPO_GET_TRADES = [
    ({'start_date': datetime.date(2024, 4, 17),
      'end_date': datetime.date(2024, 4, 22),
      'oil_id': 'A592',
      'delivery_type_id': 'A',
      'delivery_basis_id': 'ZHL'},
     4,
     does_not_raise())
]

TEST_REPO_GET_TRADES_BY_DATE = [
    ({'date': datetime.date(2024, 4, 22),
      'oil_id': 'A592',
      'delivery_type_id': 'A',
      'delivery_basis_id': 'ZHL'},
     1,
     does_not_raise())
]
