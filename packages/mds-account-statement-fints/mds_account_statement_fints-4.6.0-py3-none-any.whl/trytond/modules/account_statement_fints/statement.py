# -*- coding: utf-8 -*-
# This file is part of Tryton.  The COPYRIGHT file at the top level of
# this repository contains the full copyright notices and license terms.

from trytond.model import Workflow, ModelView, ModelSQL, fields, Unique
from trytond.pool import Pool, PoolMeta
from trytond.modules.account_statement.statement import _STATES, _DEPENDS

__all__ = ['Statement','AccountStatementLine']
__metaclass__ = PoolMeta


class Statement(Workflow, ModelSQL, ModelView):
    'Account Statement'
    __name__ = 'account.statement'

    start_date = fields.Date(string=u'Start Date', states=_STATES, depends=_DEPENDS, 
                    help=u'final opening balance provided by your bank')
    end_date = fields.Date(string=u'End Date', states=_STATES, depends=_DEPENDS,
                    help=u'final closing balance provided by your bank')

# Statement


class AccountStatementLine(ModelSQL, ModelView):
    'Account Statement Line'
    __name__ = 'account.statement.line'

    fints_data = fields.Text(string=u'SEPA-Data', readonly=True)

# end AccountStatementLine
