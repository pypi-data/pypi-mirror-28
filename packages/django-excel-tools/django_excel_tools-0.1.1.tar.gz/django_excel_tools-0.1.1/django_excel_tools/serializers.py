#!/usr/bin/env python
# -*- coding: utf-8 -*-
from collections import OrderedDict

import datetime

import sys

from .exceptions import ValidationError, ColumnNotEqualError, FieldNotExist, ImportOperationFailed, \
    SerializerConfigError
from .fields import BaseField, BASE_MESSAGE, DigitBaseField, BaseDateTimeField


class BaseSerializer(object):

    def __init__(self, worksheet, **kwargs):
        self.kwargs = kwargs
        self._class_meta_validation()

        self.class_fields = [field for field in dir(self)
                             if not (field.startswith("__") or field.startswith("_"))
                             and not callable(getattr(self, field))]
        assert self.class_fields, 'There no fields added to class.'

        self.errors = []
        self.operation_errors = []
        self.cleaned_data = []
        self.fields = OrderedDict()
        self.worksheet = worksheet

        self._set_fields()

        try:
            self._validate_column()
        except ColumnNotEqualError as e:
            self.invalid([e.message])
            return

        self._set_values()
        if not self.errors:
            self.validated()
            self._start_operation()
        else:
            self.invalid(self.errors)

    def _class_meta_validation(self):
        assert hasattr(self, 'Meta'), 'class Meta is required'

        assert hasattr(self.Meta, 'start_index'), 'Meta.start_index in class Meta is required.'
        assert type(self.Meta.start_index) is int, 'Meta.start_index type is int.'

        assert hasattr(self.Meta, 'fields'), 'Meta.fields in class Meta is required.'
        fields_is_list_or_tuple = type(self.Meta.fields) is list or type(self.Meta.fields) is tuple
        assert fields_is_list_or_tuple, 'Meta.fields type must be either list or tuple.'

        if hasattr(self.Meta, 'enable_django_transaction'):
            assert type(self.Meta.enable_django_transaction) is bool, 'Meta.enable_django_transaction is bool type.'
            self.enable_django_transaction = self.Meta.enable_django_transaction
        else:
            self.enable_django_transaction = True

        self.field_names = self.Meta.fields
        self.start_index = self.Meta.start_index

    def _set_fields(self):
        for field_name in self.field_names:
            try:
                self.fields[field_name] = getattr(self, field_name)
            except AttributeError:
                raise FieldNotExist(message='{} is not defined in class field.'.format(field_name))

    def _validate_column(self):
        if self.worksheet.max_column != len(self.fields):
            raise ColumnNotEqualError(message='Required {} fields, but given excel has {} fields, amount of field '
                                              'should be the same. [Tip] You might select the wrong excel format.'
                                      .format(len(self.fields), self.worksheet.max_column))

    def _set_values(self):
        for row_index, row in enumerate(self.worksheet.rows):
            if row_index < self.start_index:
                continue

            for index, cell in enumerate(row):
                key = self.field_names[index]
                self.fields[key].value = cell.value
                try:
                    self.fields[key].validate(index=row_index + 1)
                except ValidationError as error:
                    self.errors.append(error.message)

            self._set_cleaned_values(self.fields)
            self._reset_fields_value()

    def _reset_fields_value(self):
        for key in self.field_names:
            self.fields[key].reset()

    def _set_cleaned_values(self, validated_fields):
        cleaned_row = {}
        for key in validated_fields:
            cleaned_value = validated_fields[key].cleaned_value
            try:
                extra_clean = 'extra_clean_{}'.format(key)
                extra_clean_def = getattr(self, extra_clean)
                if callable(extra_clean_def):
                    cleaned_value = extra_clean_def(cleaned_value)
            except AttributeError:
                pass
            cleaned_row[key] = cleaned_value
        self.cleaned_data.append(cleaned_row)

    def _start_operation(self):
        if self.enable_django_transaction:
            try:
                self.import_operation(self.cleaned_data)
                self.operation_success()
            except ImportOperationFailed:
                self.operation_failed(self.operation_errors)
            return

        try:
            from django.db import transaction
        except ImportError:
            raise SerializerConfigError(message='Django is required, please make sure you installed Django via pip.')

        try:
            with transaction.atomic():
                self.import_operation(self.cleaned_data)
            self.operation_success()
        except ImportOperationFailed:
            self.operation_failed(self.operation_errors)

    def import_operation(self, cleaned_data):
        pass

    def validated(self):
        pass

    def invalid(self, errors):
        pass

    def operation_failed(self, errors):
        pass

    def operation_success(self):
        pass


class ExcelSerializer(BaseSerializer):

    def gen_error(self, index, error):
        # + 1 to make it equal to sheet index
        sheet_index = self.start_index + index + 1
        return '[Row {sheet_index}] {error}'.format(sheet_index=sheet_index, error=error)


class BooleanField(BaseField):

    def __init__(self, verbose_name):
        super(BooleanField, self).__init__(verbose_name=verbose_name, blank=True, default=False)

    def data_type_validate(self, index):
        super(BooleanField, self).data_type_validate(index)
        self.cleaned_value = True if self.value else False


class CharField(BaseField):

    def __init__(self, max_length, verbose_name, convert_number=True, blank=False, choices=None, default=None):
        super(CharField, self).__init__(verbose_name, blank, default)
        self.max_length = max_length
        self.convert_number = convert_number
        self.choices = choices

    def data_type_validate(self, index):
        super(CharField, self).data_type_validate(index)

        value = self.value
        if self.convert_number:
            if sys.version_info >= (3, 0):
                value = str(value).strip()
            else:
                value = unicode(value).strip()

        type_error_message = BASE_MESSAGE.format(
            index=index,
            verbose_name=self.verbose_name,
            message='must be text.'
        )

        if sys.version_info >= (3, 0):
            if type(value) is not str:
                raise ValidationError(message=type_error_message)
        else:
            if type(value) is not str and type(value) is not unicode:
                raise ValidationError(message=type_error_message)

        if len(value) > self.max_length:
            raise ValidationError(message=BASE_MESSAGE.format(
                index=index,
                verbose_name=self.verbose_name,
                message='cannot be more than {} characters.'.format(self.max_length)
            ))

        if self.choices:
            self._choice_validation_helper(index, value, self.choices)

        self.cleaned_value = value


class IntegerField(DigitBaseField):

    def data_type_validate(self, index):
        super(IntegerField, self).data_type_validate(index)

        value = self.value

        if self.default is not None and not self.value:
            value = self.default

        if self.convert_str and type(value) is not int:
            try:
                value = int(value)
            except ValueError:
                raise ValidationError(message=BASE_MESSAGE.format(
                    index=index,
                    verbose_name=self.verbose_name,
                    message='cannot convert {} to number.'.format(value)
                ))

        self._data_type_validation_helper(
            index=index,
            value=value,
            data_type=int,
            error_message='expected type is number but received {}.'.format(type(value).__name__)
        )

        if self.choices:
            self._choice_validation_helper(index, value, self.choices)

        self.cleaned_value = value


class DateField(BaseDateTimeField):

    def data_type_validate(self, index):
        super(DateField, self).data_type_validate(index)

        value = self.value
        type_error_message = BASE_MESSAGE.format(
                    index=index,
                    verbose_name=self.verbose_name,
                    message='"{}" is incorrect format, it should be "{}".'.format(value, self.date_format_verbose)
                )

        def convert_date():
            if not value and self.blank:
                return None
            try:
                return datetime.datetime.strptime(value, self.date_format).date()
            except ValueError:
                raise ValidationError(message=type_error_message)

        if sys.version_info >= (3, 0):
            if type(value) is str:
                value = convert_date()
        else:
            if type(value) is str or type(value) is unicode:
                value = convert_date()

        if type(value) is int:
            value = str(value)
            value = convert_date()

        if type(value) is datetime.datetime:
            value = value.date()

        self._data_type_validation_helper(
            index=index,
            value=value,
            data_type=datetime.date,
            error_message='expected type is date but received {}.'.format(type(value).__name__)
        )

        self.cleaned_value = value


class DateTimeField(BaseDateTimeField):

    def data_type_validate(self, index):
        super(DateTimeField, self).data_type_validate(index)

        value = self.value
        type_error_message = BASE_MESSAGE.format(
                        index=index,
                        verbose_name=self.verbose_name,
                        message='"{}" is incorrect format, it should be "{}"'.format(value, self.date_format_verbose)
                    )

        def convert_date_time():
            if not value and self.blank:
                return None
            try:
                return datetime.datetime.strptime(value, self.date_format)
            except ValueError:
                raise ValidationError(message=type_error_message)

        if sys.version_info >= (3, 0):
            if type(value) is str:
                value = convert_date_time()
        else:
            if type(value) is str or type(value) is unicode:
                value = convert_date_time()

        if type(value) is int:
            value = str(value)
            value = convert_date_time()

        self._data_type_validation_helper(
            index=index,
            value=value,
            data_type=datetime.datetime,
            error_message='expected type is datetime but received {}.'.format(type(value).__name__)
        )

        self.cleaned_value = value
