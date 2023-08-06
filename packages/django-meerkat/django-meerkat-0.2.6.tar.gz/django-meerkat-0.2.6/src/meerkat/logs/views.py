# -*- coding: utf-8 -*-

"""Views for logs submodule."""

from django.utils.translation import ugettext_lazy as _

from suit_dashboard import Column, Grid, Row

from ..views import HomeView
from .boxes import (
    BoxLogsLinks, BoxLogsMostVisitedPages, BoxLogsMostVisitedPagesLegend,
    BoxLogsStatusCodes, BoxLogsStatusCodesByDate)


class LogsMenu(HomeView):
    """View for logs menu."""

    crumbs = ({'name': 'Logs analysis', 'url': 'admin:logs'}, )
    grid = Grid(Row(Column(BoxLogsLinks())))


class LogsStatusCodes(LogsMenu):
    """View for status codes."""

    crumbs = (
        {'name': _('Status codes'), 'url': 'admin:logs_status_codes'},
    )
    grid = Grid(Row(Column(BoxLogsLinks(), BoxLogsStatusCodes())))


class LogsStatusCodesByDate(LogsMenu):
    """View for status codes by date."""

    crumbs = ({'name': _('Status codes by date'),
               'url': 'admin:logs_status_code_by_date'},)
    grid = Grid(Row(Column(BoxLogsLinks())),
                Row(Column(BoxLogsStatusCodesByDate())))


class LogsMostVisitedPages(LogsMenu):
    """View for most visited pages."""

    crumbs = ({'name': _('Most visited pages'),
               'url': 'admin:logs_most_visited_pages'}, )
    grid = Grid(Row(Column(BoxLogsLinks(), width=5),
                    Column(BoxLogsMostVisitedPagesLegend(), width=7)),
                Row(Column(BoxLogsMostVisitedPages())))
