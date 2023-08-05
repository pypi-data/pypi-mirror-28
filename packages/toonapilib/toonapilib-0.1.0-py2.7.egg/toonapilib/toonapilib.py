#!/usr/bin/env python
# -*- coding: utf-8 -*-
# File: toonapilib.py
#
# Copyright 2017 Costas Tyfoxylos
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
#  of this software and associated documentation files (the "Software"), to
#  deal in the Software without restriction, including without limitation the
#  rights to use, copy, modify, merge, publish, distribute, sublicense, and/or
#  sell copies of the Software, and to permit persons to whom the Software is
#  furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
#  all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#  IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#  FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
#  AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#  LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
#  FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
#  DEALINGS IN THE SOFTWARE.
#

"""
Main code for toonapilib

.. _Google Python Style Guide:
   http://google.github.io/styleguide/pyguide.html

"""

import logging
import requests
import json
from cachetools import cached, TTLCache
from .toonapilibexceptions import ChallengeCodeError, InvalidThermostatState
from .configuration import STATES, STATE_CACHING_SECONDS
from .helpers import (Agreement,
                      SmartPlug,
                      SmokeDetector,
                      Solar,
                      PowerUsage,
                      Light,
                      Usage,
                      ThermostatInfo,
                      ThermostatState,
                      Token)

__author__ = '''Costas Tyfoxylos <costas.tyf@gmail.com>'''
__docformat__ = '''google'''
__date__ = '''2017-12-09'''
__copyright__ = '''Copyright 2017, Costas Tyfoxylos'''
__credits__ = ["Costas Tyfoxylos"]
__license__ = '''MIT'''
__maintainer__ = '''Costas Tyfoxylos'''
__email__ = '''<costas.tyf@gmail.com>'''
__status__ = '''Development'''  # "Prototype", "Development", "Production".


# This is the main prefix used for logging
LOGGER_BASENAME = '''toonapilib'''
LOGGER = logging.getLogger(LOGGER_BASENAME)
LOGGER.addHandler(logging.NullHandler())

state_cache = TTLCache(maxsize=1, ttl=STATE_CACHING_SECONDS)


# TODO authentication error hanlding for wrong credentials etc.

class Toon(object):
    """Model of the toon smart meter from eneco."""

    def __init__(self,
                 eneco_username,
                 eneco_password,
                 consumer_key,
                 consumer_secret):
        logger_name = u'{base}.{suffix}'.format(base=LOGGER_BASENAME,
                                                suffix=self.__class__.__name__)
        self._logger = logging.getLogger(logger_name)
        self._base_url = 'https://api.toon.eu/'
        self._api_url = None
        self._username = eneco_username
        self._password = eneco_password
        self._client_id = consumer_key
        self._client_secret = consumer_secret
        self.agreements = None
        self.agreement = None
        self._headers = None
        self._token = None
        self._authenticate()

    def _get_challenge_code(self):
        url = '{base_url}/authorize/legacy'.format(base_url=self._base_url)
        payload = {'username': self._username,
                   'password': self._password,
                   'tenant_id': 'eneco',
                   'response_type': 'code',
                   'client_id': self._client_id,
                   'state': '',
                   'scope': ''}
        response = requests.post(url, data=payload, allow_redirects=False)
        if response.status_code != 302:
            raise ChallengeCodeError(response.content)
        try:
            location = response.headers.get('Location')
            code = location.split('code=')[1].split('&state')[0]
        except IndexError:
            message = ('Please make sure your credentials and keys are correct.'
                       'Response received :{}'.format(response.content))
            raise ChallengeCodeError(message)
        return code

    def _authenticate(self):
        self._monkey_patch_requests()
        code = self._get_challenge_code()
        self._token = self._get_token(code)
        self._set_headers(self._token)
        self._get_agreements()
        self._api_url = '{}/toon/v3/{}'.format(self._base_url,
                                               self.agreement.id)

    def _set_headers(self, token):
        self._headers = {'Authorization': 'Bearer {}'.format(token.access_token),
                         'content-type': 'application/json',
                         'cache-control': 'no-cache'}

    def _get_agreements(self):
        url = '{base_url}/toon/v3/agreements'.format(base_url=self._base_url)
        response = requests.get(url, headers=self._headers)
        agreements = response.json()
        self.agreements = [Agreement(agreement.get('agreementId'),
                                     agreement.get('agreementIdChecksum'),
                                     agreement.get('heatingType'),
                                     agreement.get('displayCommonName'),
                                     agreement.get('displayHardwareVersion'),
                                     agreement.get('displaySoftwareVersion'),
                                     agreement.get('isToonSolar'),
                                     agreement.get('isToonly'))
                           for agreement in agreements]
        self.agreement = self.agreements[0]

    def _get_token(self, code):
        payload = {'client_id': self._client_id,
                   'client_secret': self._client_secret,
                   'grant_type': 'authorization_code',
                   'code': code}
        return self._retrieve_token(payload)

    def _refresh_token(self):
        payload = {'client_id': self._client_id,
                   'client_secret': self._client_secret,
                   'grant_type': 'refresh_token',
                   'refresh_token': self._token.refresh_token}
        return self._retrieve_token(payload)

    def _retrieve_token(self, payload):
        headers = {'content-type': 'application/x-www-form-urlencoded'}
        url = '{base_url}/token'.format(base_url=self._base_url)
        response = requests.post(url, headers=headers, data=payload)
        tokens = response.json()
        self._logger.debug(tokens)
        token_values = [tokens.get(key) for key in Token._fields]
        if not all(token_values):
            self._logger.exception(response.content)
            raise ValueError('Incomplete token response received. '
                             'Got: {}'.format(response.json()))
        return Token(*token_values)

    def _reset(self):
        self.agreements = None
        self.agreement = None
        self.client = None

    @property
    @cached(state_cache)
    def status(self):
        url = ('{base_url}/toon/v3/'
               '{agreement_id}/status').format(base_url=self._base_url,
                                               agreement_id=self.agreement.id)
        response = requests.get(url, headers=self._headers)
        return response.json()

    def _monkey_patch_requests(self):
        self.original_request = requests.get
        requests.get = self._patched_request

    def _patched_request(self, url, **kwargs):
        self._logger.debug('Using patched request for url {}'.format(url))
        response = self.original_request(url, **kwargs)
        if response.status_code == 401 and \
                response.json().get('fault', {}
                                    ).get('faultstring', {}
                                          ) == 'Access Token expired':
            self._logger.info('Expired token detected, trying to refresh!')
            self._token = self._refresh_token()
            self._set_headers(self._token)
            kwargs['headers'].update(
                {'Authorization': 'Bearer {}'.format(self._token.access_token)})
            self._logger.debug('Updated headers, trying again initial request')
            response = self.original_request(url, **kwargs)
        return response

    def _clear_cache(self):
        self._logger.debug('Clearing state cache.')
        state_cache.clear()

    @property
    def smokedetectors(self):
        """:return: A list of smokedetector objects modeled as named tuples"""
        return [SmokeDetector(smokedetector.get('devUuid'),
                              smokedetector.get('name'),
                              smokedetector.get('lastConnectedChange'),
                              smokedetector.get('connected'),
                              smokedetector.get('batteryLevel'),
                              smokedetector.get('type'))
                for smokedetector in self.status.get('smokeDetectors',
                                                     {}).get('device', [])]

    def get_smokedetector_by_name(self, name):
        """Retrieves a smokedetector object by its name

        :param name: The name of the smokedetector to return
        :return: A smokedetector object
        """
        return next((smokedetector for smokedetector in self.smokedetectors
                     if smokedetector.name.lower() == name.lower()), None)

    @property
    def lights(self):
        """:return: A list of light objects"""
        return [Light(self, light.get('name'))
                for light in self.status.get('deviceStatusInfo',
                                             {}).get('device', [])
                if light.get('rgbColor')]

    def get_light_by_name(self, name):
        """Retrieves a light object by its name

        :param name: The name of the light to return
        :return: A light object
        """
        return next((light for light in self.lights
                     if light.name.lower() == name.lower()), None)

    @property
    def smartplugs(self):
        """:return: A list of smartplug objects."""
        return [SmartPlug(self, plug.get('name'))
                for plug in self.status.get('deviceStatusInfo',
                                            {}).get('device', [])
                if plug.get('networkHealthState')]

    def get_smartplug_by_name(self, name):
        """Retrieves a smartplug object by its name

        :param name: The name of the smartplug to return
        :return: A smartplug object
        """
        return next((plug for plug in self.smartplugs
                     if plug.name.lower() == name.lower()), None)

    @property
    def gas(self):
        """:return: A gas object modeled as a named tuple"""
        usage = self.status['gasUsage']
        return Usage(usage.get('avgDayValue'),
                     usage.get('avgValue'),
                     usage.get('dayCost'),
                     usage.get('dayUsage'),
                     usage.get('isSmart'),
                     usage.get('meterReading'),
                     usage.get('value'))

    @property
    def power(self):
        """:return: A power object modeled as a named tuple"""
        power = self.status['powerUsage']
        return PowerUsage(power.get('avgDayValue'),
                          power.get('avgValue'),
                          power.get('dayCost'),
                          power.get('dayUsage'),
                          power.get('isSmart'),
                          power.get('meterReading'),
                          power.get('value'),
                          power.get('meterReadingLow'),
                          power.get('dayLowUsage'))

    @property
    def solar(self):
        """:return: A solar object modeled as a named tuple"""
        power = self.status['powerUsage']
        return Solar(power.get('maxSolar'),
                     power.get('valueProduced'),
                     power.get('valueSolar'),
                     power.get('avgProduValue'),
                     power.get('meterReadingLowProdu'),
                     power.get('meterReadingProdu'),
                     power.get('dayCostProduced'))

    @property
    def thermostat_info(self):
        """:return: A thermostatinfo object modeled as a named tuple"""
        info = self.status['thermostatInfo']
        return ThermostatInfo(info.get('activeState'),
                              info.get('boilerModuleConnected'),
                              info.get('burnerInfo'),
                              info.get('currentDisplayTemp'),
                              info.get('currentModulationLevel'),
                              info.get('currentSetpoint'),
                              info.get('errorFound'),
                              info.get('haveOTBoiler'),
                              info.get('nextProgram'),
                              info.get('nextSetpoint'),
                              info.get('nextState'),
                              info.get('nextTime'),
                              info.get('otCommError'),
                              info.get('programState'),
                              info.get('realSetpoint'))

    @property
    def thermostat_states(self):
        """:return: A list of thermostatstate object modeled as named tuples"""
        return [ThermostatState(STATES[state.get('id')],
                                state.get('id'),
                                state.get('tempValue'),
                                state.get('dhw'))
                for state in self.status['thermostatStates']['state']]

    def get_thermostat_state_by_name(self, name):
        """Retrieves a thermostat state object by its assigned name

        :param name: The name of the thermostat state
        :return: The thermostat state object
        """
        self._validate_thermostat_state_name(name)
        return next((state for state in self.thermostat_states
                     if state.name.lower() == name.lower()), None)

    def get_thermostat_state_by_id(self, id_):
        """Retrieves a thermostat state object by its id

        :param id_: The id of the thermostat state
        :return: The thermostat state object
        """
        return next((state for state in self.thermostat_states
                     if state.id == id_), None)

    @property
    def burner_on(self):
        return True if int(self.thermostat_info.burner_info) else False

    @staticmethod
    def _validate_thermostat_state_name(name):
        if name.lower() not in [value.lower() for value in STATES.values()
                                if not value.lower() == 'unknown']:
            raise InvalidThermostatState(name)

    @property
    def thermostat_state(self):
        """The state of the thermostat programming

        :return: A thermostat state object of the current setting
        """
        current_state = self.thermostat_info.active_state
        state = self.get_thermostat_state_by_id(current_state)
        if not state:
            self._logger.debug('Manually set temperature, no Thermostat '
                               'State chosen!')
        return state

    @thermostat_state.setter
    def thermostat_state(self, name):
        """Changes the thermostat state to the one passed as an argument

        :param name: The name of the thermostat state to change to.
        """
        self._validate_thermostat_state_name(name)
        id_ = next((key for key in STATES.keys()
                    if STATES[key].lower() == name.lower()), None)
        url = '{api_url}/thermostat'.format(api_url=self._api_url)
        data = requests.get(url, headers=self._headers).json()
        data["activeState"] = id_
        response = requests.put(url,
                                data=json.dumps(data),
                                headers=self._headers)
        self._logger.debug('Response received {}'.format(response.content))
        self._clear_cache()

    @property
    def thermostat(self):
        """The current setting of the thermostat as temperature

        :return: A float of the current setting of the temperature of the
        thermostat
        """
        return float(self.thermostat_info.current_set_point / 100)

    @thermostat.setter
    def thermostat(self, temperature):
        """A temperature to set the thermostat to. Requires a float.

        :param temperature: A float of the desired temperature to change to.
        """
        try:
            target = int(temperature * 100)
        except ValueError:
            self._logger.error('Please supply a valid temperature e.g: 20')
            return
        url = '{api_url}/thermostat'.format(api_url=self._api_url)
        response = requests.get(url, headers=self._headers)
        if not response.ok:
            self._logger.error(response.json)
            return
        data = response.json()
        data["currentSetpoint"] = target
        data["activeState"] = -1
        response = requests.put(url,
                                data=json.dumps(data),
                                headers=self._headers)
        if not response.ok:
            self._logger.error(response.json)
            return
        self._logger.debug('Response received {}'.format(response.content))
        self._clear_cache()

    @property
    def temperature(self):
        """The current actual temperature as perceived by toon.

        :return: A float of the current temperature
        """
        return float(self.thermostat_info.current_displayed_temperature / 100)
