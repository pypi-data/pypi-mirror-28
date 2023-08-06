from typing import Dict, Any

from anji_orm.model import Model
import rethinkdb as R
from sanic.request import Request
from sanic.response import json

__author__ = "Bogdan Gladyshev"
__copyright__ = "Copyright 2017, Bogdan Gladyshev"
__credits__ = ["Bogdan Gladyshev"]
__license__ = "MIT"
__version__ = "0.1.1"
__maintainer__ = "Bogdan Gladyshev"
__email__ = "siredvin.dark@gmail.com"
__status__ = "Production"

__all__ = ['DataTableMixin']


SEARCH_TARGET_FIELD_MARK = 'search_target'


class DataTableMixin(Model):

    async def convert_to_web_info(self) -> Dict[str, Any]:
        return await self.async_to_describe_dict()

    @classmethod
    async def process_after_filter(cls, db_request: R. RqlQuery) -> R.RqlQuery:
        return db_request

    @classmethod
    async def process_web_request(cls, request: Request) -> Dict[str, Any]:
        search_target_field_name = cls._field_marks.get(SEARCH_TARGET_FIELD_MARK, None)
        db_request: R.RqlQuery = cls.all()
        if 'filter' in request.args and search_target_field_name is not None:
            db_request = db_request.filter(lambda doc: doc[search_target_field_name].match(request.args.get('filter')))
        db_request = await cls.process_after_filter(db_request)
        total_count = await cls.async_execute(db_request.count())
        if 'sortColumn' in request.args:
            column_link = request.args.get('sortColumn')
            if request.args.get('sortDirection') == 'desc':
                column_link = R.desc(column_link)
            db_request = db_request.order_by(column_link)
        if 'pageIndex' in request.args and 'pageSize' in request.args:
            page_index = int(request.args.get('pageIndex'))
            page_size = int(request.args.get('pageSize'))
            db_request = db_request.skip(page_index * page_size).limit(page_size)
        records = await cls.async_execute(db_request)
        return json(
            {
                'data': [await record.convert_to_web_info() for record in records],
                'total': total_count
            }
        )
