import operator
from collections import OrderedDict
from functools import reduce

from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from django.core.paginator import Paginator
from django.db.models import Q
from django.db.models.constants import LOOKUP_SEP
from django.db.models.query import QuerySet
from rest_framework import viewsets, exceptions
from rest_framework.authentication import get_authorization_header
from rest_framework.decorators import list_route

from . import rpc_errors
from .rpc_mixin import RpcMixin
from .rpc_view import RpcView
from .rpc_decorator import rpc_error_handler


def querydict_to_dict(querydict):
    return {k: v[0] if len(v) == 1 else v for k, v in querydict.lists()}


class RpcDrfMixin(RpcView):
    """
    Provides common DRF ViewSet-like abstractions for interacting with models
    and serializers via RPC.
    """
    queryset = None
    serializer_class = None
    lookup_field = "pk"
    lookup_kwarg = None
    search_fields = None
    search_lookup_prefixes = {
        "^": "istartswith",
        "=": "iexact",
        "@": "search",
        "$": "iregex",
    }

    def get_queryset(self):
        assert self.queryset is not None, (
            "'%s' should either include a `queryset` attribute, "
            "or override the `get_queryset()` method."
            % self.__class__.__name__
        )

        queryset = self.queryset
        if isinstance(queryset, QuerySet):
            # Ensure queryset is re-evaluated on each request.
            queryset = queryset.all()
        return queryset

    def get_object(self, **kwargs):
        queryset = self.queryset

        # Perform the lookup filtering.
        lookup_kwarg = self.lookup_kwarg or self.lookup_field

        assert lookup_kwarg in kwargs, (
            'Expected a keyword argument '
            'named "%s". Fix your RPC call, or set the `.lookup_field` '
            'attribute on the service correctly.' %
            (lookup_kwarg,)
        )

        filter_kwargs = {self.lookup_field: kwargs[lookup_kwarg]}

        obj = queryset.get(**filter_kwargs)
        return obj

    def get_serializer_class(self):
        assert self.serializer_class is not None, (
            "'%s' should either include a `serializer_class` attribute, "
            "or override the `get_serializer_class()` method."
            % self.__class__.__name__
        )

        return self.serializer_class

    def get_serializer(self, *args, **kwargs):
        serializer_class = self.get_serializer_class()
        return serializer_class(*args, **kwargs)

    def paginate_queryset(self, queryset, page_num, page_size):
        self.page_num = int(page_num)
        self.page_size = int(page_size)
        paginator = Paginator(queryset, self.page_size)
        self.page = paginator.page(self.page_num)
        return self.page

    def get_paginated_response(self, data):
        return OrderedDict([
            ("results", data),
            ("meta", {
                "total_results": self.page.paginator.count,
                "total_pages": self.page.paginator.num_pages,
                "page": self.page_num,
                "page_size": self.page_size,
            })
        ])

    def get_search_fields(self):
        return self.search_fields

    def construct_search(self, field_name):
        lookup = self.search_lookup_prefixes.get(field_name[0])
        if lookup:
            field_name = field_name[1:]
        else:
            lookup = "icontains"
        return LOOKUP_SEP.join([field_name, lookup])

    def search_queryset(self, queryset, search_terms):
        search_fields = self.get_search_fields()
        search_terms = search_terms.replace(",", " ").split()

        if not search_fields or not search_terms:
            return queryset

        orm_lookups = [
            self.construct_search(search_field)
            for search_field in search_fields
        ]

        base = queryset
        conditions = []
        for search_term in search_terms:
            queries = [
                Q(**{orm_lookup: search_term})
                for orm_lookup in orm_lookups
            ]
            conditions.append(reduce(operator.or_, queries))
        queryset = queryset.filter(reduce(operator.and_, conditions))

        return queryset

    @RpcView.auth
    def create(self, *args, **kwargs):
        serializer = self.get_serializer(data=kwargs)

        if not serializer.is_valid():
            return {rpc_errors.VALIDATION_ERRORS_KEY: serializer.errors}

        serializer.save()
        return serializer.data

    @RpcView.auth
    def list(self, *args, **kwargs):
        queryset = self.get_queryset()
        page_num = int(kwargs.pop("page", 1))
        page_size = int(kwargs.pop("page_size", settings.PAGINATION["PAGE_SIZE"]))

        if page_size > settings.PAGINATION["MAX_PAGE_SIZE"]:
            page_size = settings.PAGINATION["MAX_PAGE_SIZE"]

        page = self.paginate_queryset(queryset, page_num, page_size)
        if page is not None:
            serializer = self.get_serializer(page, many=True, *args, **kwargs)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True, *args, **kwargs)
        return serializer.data

    @RpcView.auth
    def retrieve(self, *args, **kwargs):
        try:
            instance = self.get_object(**kwargs)
        except ObjectDoesNotExist:
            return {rpc_errors.ERRORS_KEY: {rpc_errors.OBJ_NOT_FOUND_KEY: rpc_errors.OBJ_NOT_FOUND_ERROR_VALUE}}

        serializer = self.get_serializer(instance)
        return serializer.data

    @RpcView.auth
    def update(self, *args, **kwargs):
        partial = kwargs.pop("partial", False)

        try:
            instance = self.get_object(**kwargs)
        except ObjectDoesNotExist:
            return {rpc_errors.ERRORS_KEY: {rpc_errors.OBJ_NOT_FOUND_KEY: rpc_errors.OBJ_NOT_FOUND_ERROR_VALUE}}

        serializer = self.get_serializer(instance, data=kwargs, partial=partial)

        if not serializer.is_valid():
            return {rpc_errors.VALIDATION_ERRORS_KEY: serializer.errors}

        serializer.save()
        return serializer.data

    @RpcView.auth
    def delete(self, *args, **kwargs):
        try:
            instance = self.get_object(**kwargs)
        except ObjectDoesNotExist:
            return {rpc_errors.ERRORS_KEY: {rpc_errors.OBJ_NOT_FOUND_KEY: rpc_errors.OBJ_NOT_FOUND_ERROR_VALUE}}

        instance_id = instance.id
        instance.delete()
        return {"id": str(instance_id)}

    @RpcView.auth
    def search(self, *args, **kwargs):
        page_num = int(kwargs.pop("page", 1))
        page_size = int(kwargs.pop("page_size", settings.PAGINATION["PAGE_SIZE"]))

        if page_size > settings.PAGINATION["MAX_PAGE_SIZE"]:
            page_size = settings.PAGINATION["MAX_PAGE_SIZE"]

        search_terms = kwargs.pop("query", "")

        if not search_terms:
            return {rpc_errors.ERRORS_KEY: {rpc_errors.MISSING_SEARCH_PARAM_KEY: rpc_errors.MISSING_SEARCH_PARAM_VALUE}}

        queryset = self.search_queryset(self.get_queryset(), search_terms)
        page = self.paginate_queryset(queryset, page_num, page_size)
        if page is not None:
            serializer = self.get_serializer(page, many=True, *args, **kwargs)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True, *args, **kwargs)
        return serializer.data


class RpcDrfViewSet(viewsets.ViewSet, RpcMixin):
    """
    A DRF based ViewSet base class that provides a CRUDL HTTP API gateway
    to interact with Nameko RPC calls.
    """
    rpc_service_name = None

    def _getJwt(self, request):
        jwt = None

        try:
            jwt = get_authorization_header(request).decode().split()[1]
        except Exception as ex:
            jwt = None

        return jwt


    def get_rpc_service_name(self):
        assert self.rpc_service_name is not None, (
            "'%s' should either include a `rpc_service_name` attribute, "
            "or override the `get_rpc_service_name()` method."
            % self.__class__.__name__
        )

        rpc_service_name = self.rpc_service_name
        return rpc_service_name

    @list_route(methods=["get"], url_path="search")
    @rpc_error_handler
    def search(self, request, *args, **kwargs):
        jwt = self._getJwt(request)
        params = querydict_to_dict(request.query_params)

        return self.call_service_method(
            self.get_rpc_service_name(),
            "search",
            False,
            **{**{"jwt": jwt}, **params},
        )

    @rpc_error_handler
    def list(self, request, *args, **kwargs):
        jwt = self._getJwt(request)
        params = querydict_to_dict(request.query_params)

        return self.call_service_method(
            self.get_rpc_service_name(),
            "list",
            False,
            **{**{"jwt": jwt}, **params},
        )

    @rpc_error_handler
    def retrieve(self, request, pk, *args, **kwargs):
        jwt = self._getJwt(request)
        params = querydict_to_dict(request.query_params)

        return self.call_service_method(
            self.get_rpc_service_name(),
            "retrieve",
            False,
            **{**{"jwt": jwt}, **{"pk": pk}, **params},
        )

    @rpc_error_handler
    def create(self, request, *args, **kwargs):
        jwt = self._getJwt(request)

        return self.call_service_method(
            self.get_rpc_service_name(),
            "create",
            False,
            **{**{"jwt": jwt}, **request.data}
        )

    @rpc_error_handler
    def update(self, request, pk, *args, **kwargs):
        jwt = self._getJwt(request)
        request_data = request.data
        request_data["partial"] = kwargs.pop("partial", False)

        return self.call_service_method(
            self.get_rpc_service_name(),
            "update",
            False,
            **{**{"jwt": jwt}, **{"pk": pk}, **request_data}
        )

    @rpc_error_handler
    def delete(self, request, pk, *args, **kwargs):
        jwt = self._getJwt(request)
        request_data = request.data

        return self.call_service_method(
            self.get_rpc_service_name(),
            "delete",
            False,
            **{**{"jwt": jwt}, **{"pk": pk}, **request_data}
        )

    def partial_update(self, request, pk, *args, **kwargs):
        kwargs["partial"] = True
        return self.update(request, pk, *args, **kwargs)
