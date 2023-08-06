#!/usr/bin/python
# -*- coding: utf-8 -*-
from cloudshell.layer_one.core.response.resource_info.entities.attributes import StringAttribute
from cloudshell.layer_one.core.response.resource_info.entities.base import ResourceInfo


class Chassis(ResourceInfo):
    """
    Chassis resource entity
    """
    NAME_TEMPLATE = 'Chassis {}'
    FAMILY_NAME = 'L1 Switch'

    def __init__(self, resource_id, address, model_name, serial_number):
        self._address = address
        name = self.NAME_TEMPLATE.format(resource_id if len(str(resource_id)) > 1 else '0' + str(resource_id))
        family_name = self.FAMILY_NAME
        super(Chassis, self).__init__(resource_id, name, family_name, model_name, serial_number)

    @property
    def address(self):
        return self._address

    def set_model_name(self, value):
        if value:
            self.attributes.append(StringAttribute('Model Name', value))

    def set_serial_number(self, value):
        if value:
            self.attributes.append(StringAttribute('Serial Number', value))

    def set_os_version(self, value):
        if value:
            self.attributes.append(StringAttribute('OS Version', value))
