#!/usr/bin/python
# -*- coding: utf-8 -*-

# Hive Colony Framework
# Copyright (c) 2008-2024 Hive Solutions Lda.
#
# This file is part of Hive Colony Framework
#
# Hive Colony Framework is free software: you can redistribute it and/or modify
# it under the terms of the Apache License as published by the Apache
# Foundation, either version 2.0 of the License, or (at your option) any
# later version.
#
# Hive Colony Framework is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# Apache License for more details.
#
# You should have received a copy of the Apache License along with
# Hive Colony Framework If not, see <http://www.apache.org/licenses/>.

__author__ = "João Magalhães <joamag@hive.pt>"
""" The author(s) of the module """

__copyright__ = "Copyright (c) 2008-2024 Hive Solutions Lda."
""" The copyright for the module """

__license__ = "Apache License, Version 2.0"
""" The license for the module """

import colony

from colony.libs import observer_util

try:
    import unittest.mock as mock
except ImportError:
    mock = None


class ObserverTest(colony.ColonyTestCase):
    """
    Class that tests the utility functions that are
    associated with the observer, namely the ones that
    build the Kafka configuration and producer.
    """

    def setUp(self):
        # saves the current Kafka global state (configuration values
        # and caches) and clears it, so that every test starts from
        # an empty Kafka configuration and without cached values
        self.configs = colony.conf_prefix("KAFKA_")
        self.kafka_config = observer_util._KAFKA_CONFIG
        self.kafka_producers = dict(observer_util.KAFKA_PRODUCERS)
        for name in self.configs:
            colony.conf_r(name)
        observer_util._KAFKA_CONFIG = None
        observer_util.KAFKA_PRODUCERS.clear()

    def tearDown(self):
        # removes the Kafka configuration values set by the test and
        # restores the global state that was saved in the setup
        for name in colony.conf_prefix("KAFKA_"):
            colony.conf_r(name)
        for name, value in self.configs.items():
            colony.conf_s(name, value)
        observer_util._KAFKA_CONFIG = self.kafka_config
        observer_util.KAFKA_PRODUCERS.clear()
        observer_util.KAFKA_PRODUCERS.update(self.kafka_producers)

    def test_kafka_config(self):
        """
        Tests that the Kafka configuration contains the SSL values
        with the defaults of kafka-python when none of them is set.
        """

        if mock == None:
            self.skipTest("Skipping test: mock unavailable")

        kafka = mock.Mock()
        kafka.__version__ = "2.0.2"

        colony.conf_s("KAFKA_SERVER", "localhost:9092")

        with mock.patch.dict("sys.modules", dict(kafka=kafka)):
            result = colony.kafka_config()

        self.assertEqual(
            result,
            dict(
                kafka_server="localhost:9092",
                security_protocol="PLAINTEXT",
                sasl_mechanism=None,
                sasl_plain_username=None,
                sasl_plain_password=None,
                ssl_cafile=None,
                ssl_certfile=None,
                ssl_keyfile=None,
                ssl_password=None,
                ssl_check_hostname=True,
                default_topic="colony",
                client_version="2.0.2",
            ),
        )

    def test_kafka_config_ssl(self):
        """
        Tests that the Kafka configuration contains the SSL values
        that are set, with the hostname check cast to a boolean.
        """

        if mock == None:
            self.skipTest("Skipping test: mock unavailable")

        kafka = mock.Mock()
        kafka.__version__ = "2.0.2"

        colony.conf_s("KAFKA_SERVER", "localhost:9093")
        colony.conf_s("KAFKA_SECURITY_PROTOCOL", "SASL_SSL")
        colony.conf_s("KAFKA_SSL_CAFILE", "/etc/kafka/ca.pem")
        colony.conf_s("KAFKA_SSL_CERTFILE", "/etc/kafka/client.pem")
        colony.conf_s("KAFKA_SSL_KEYFILE", "/etc/kafka/client.key")
        colony.conf_s("KAFKA_SSL_PASSWORD", "password")
        colony.conf_s("KAFKA_SSL_CHECK_HOSTNAME", "0")

        with mock.patch.dict("sys.modules", dict(kafka=kafka)):
            result = colony.kafka_config()

        self.assertEqual(result["kafka_server"], "localhost:9093")
        self.assertEqual(result["security_protocol"], "SASL_SSL")
        self.assertEqual(result["ssl_cafile"], "/etc/kafka/ca.pem")
        self.assertEqual(result["ssl_certfile"], "/etc/kafka/client.pem")
        self.assertEqual(result["ssl_keyfile"], "/etc/kafka/client.key")
        self.assertEqual(result["ssl_password"], "password")
        self.assertEqual(result["ssl_check_hostname"], False)

    def test_kafka_config_empty(self):
        """
        Tests that the SSL values set as empty strings are kept as
        such (unlike the unset ones that are None), as kafka-python
        handles both in the same way for the paths and the password.
        """

        if mock == None:
            self.skipTest("Skipping test: mock unavailable")

        kafka = mock.Mock()
        kafka.__version__ = "2.0.2"

        colony.conf_s("KAFKA_SERVER", "localhost:9093")
        colony.conf_s("KAFKA_SSL_CAFILE", "")
        colony.conf_s("KAFKA_SSL_CERTFILE", "")
        colony.conf_s("KAFKA_SSL_KEYFILE", "")
        colony.conf_s("KAFKA_SSL_PASSWORD", "")

        with mock.patch.dict("sys.modules", dict(kafka=kafka)):
            result = colony.kafka_config()

        self.assertEqual(result["ssl_cafile"], "")
        self.assertEqual(result["ssl_certfile"], "")
        self.assertEqual(result["ssl_keyfile"], "")
        self.assertEqual(result["ssl_password"], "")
        self.assertEqual(result["ssl_check_hostname"], True)

    def test_kafka_config_check_hostname(self):
        """
        Tests the cast of the hostname check value to a boolean,
        for both the string and the boolean values.
        """

        if mock == None:
            self.skipTest("Skipping test: mock unavailable")

        kafka = mock.Mock()
        kafka.__version__ = "2.0.2"

        colony.conf_s("KAFKA_SERVER", "localhost:9093")

        # the boolean cast of the configuration only considers the
        # 1, true and True strings as true values, meaning that any
        # other value that is set (eg: TRUE, yes or an empty string)
        # disables the check of the hostname of the broker
        values = (
            ("1", True),
            ("true", True),
            ("True", True),
            ("0", False),
            ("false", False),
            ("False", False),
            ("TRUE", False),
            ("yes", False),
            ("", False),
            (True, True),
            (False, False),
        )

        for value, expected in values:
            colony.conf_s("KAFKA_SSL_CHECK_HOSTNAME", value)
            observer_util._KAFKA_CONFIG = None

            with mock.patch.dict("sys.modules", dict(kafka=kafka)):
                result = colony.kafka_config()

            self.assertEqual(result["ssl_check_hostname"], expected)

    def test_kafka_config_cache(self):
        """
        Tests that the Kafka configuration is cached, meaning that
        changes to the SSL values are only used once the cache
        is cleared.
        """

        if mock == None:
            self.skipTest("Skipping test: mock unavailable")

        kafka = mock.Mock()
        kafka.__version__ = "2.0.2"

        colony.conf_s("KAFKA_SERVER", "localhost:9093")
        colony.conf_s("KAFKA_SSL_CAFILE", "/etc/kafka/ca.pem")

        with mock.patch.dict("sys.modules", dict(kafka=kafka)):
            result = colony.kafka_config()
            colony.conf_s("KAFKA_SSL_CAFILE", "/etc/kafka/other.pem")
            result_cached = colony.kafka_config()

        self.assertTrue(result_cached is result)
        self.assertTrue(observer_util._KAFKA_CONFIG is result)
        self.assertEqual(result_cached["ssl_cafile"], "/etc/kafka/ca.pem")

        observer_util._KAFKA_CONFIG = None

        with mock.patch.dict("sys.modules", dict(kafka=kafka)):
            result = colony.kafka_config()

        self.assertEqual(result["ssl_cafile"], "/etc/kafka/other.pem")

    def test_kafka_config_no_server(self):
        """
        Tests that no Kafka configuration exists (nor is cached)
        when no server is set, even if the SSL values are set.
        """

        if mock == None:
            self.skipTest("Skipping test: mock unavailable")

        kafka = mock.Mock()
        kafka.__version__ = "2.0.2"

        colony.conf_s("KAFKA_SSL_CAFILE", "/etc/kafka/ca.pem")

        with mock.patch.dict("sys.modules", dict(kafka=kafka)):
            result = colony.kafka_config()

        self.assertEqual(result, None)
        self.assertEqual(observer_util._KAFKA_CONFIG, None)

    def test_kafka_config_no_kafka(self):
        """
        Tests that no Kafka configuration exists (nor is cached)
        when the kafka module is not available.
        """

        if mock == None:
            self.skipTest("Skipping test: mock unavailable")

        colony.conf_s("KAFKA_SERVER", "localhost:9093")
        colony.conf_s("KAFKA_SSL_CAFILE", "/etc/kafka/ca.pem")

        with mock.patch.dict("sys.modules", dict(kafka=None)):
            result = colony.kafka_config()

        self.assertEqual(result, None)
        self.assertEqual(observer_util._KAFKA_CONFIG, None)

    def test_kafka_producer(self):
        """
        Tests that the Kafka producer is created with exactly the
        default SSL options of kafka-python when none of them is set.
        """

        if mock == None:
            self.skipTest("Skipping test: mock unavailable")

        kafka = mock.Mock()
        kafka.__version__ = "2.0.2"

        colony.conf_s("KAFKA_SERVER", "localhost:9092")

        with mock.patch.dict("sys.modules", dict(kafka=kafka)):
            result = observer_util._kafka_producer()

        kafka.KafkaProducer.assert_called_once_with(
            bootstrap_servers="localhost:9092",
            security_protocol="PLAINTEXT",
            sasl_mechanism=None,
            sasl_plain_username=None,
            sasl_plain_password=None,
            ssl_cafile=None,
            ssl_certfile=None,
            ssl_keyfile=None,
            ssl_password=None,
            ssl_check_hostname=True,
            reconnect_backoff_ms=150,
            reconnect_backoff_max_ms=120000,
        )
        self.assertEqual(result, kafka.KafkaProducer.return_value)
        self.assertEqual(observer_util.KAFKA_PRODUCERS, {"localhost:9092": result})

    def test_kafka_producer_ssl(self):
        """
        Tests that the Kafka producer is created with exactly the
        SSL options that are set.
        """

        if mock == None:
            self.skipTest("Skipping test: mock unavailable")

        kafka = mock.Mock()
        kafka.__version__ = "2.0.2"

        colony.conf_s("KAFKA_SERVER", "localhost:9093")
        colony.conf_s("KAFKA_SECURITY_PROTOCOL", "SASL_SSL")
        colony.conf_s("KAFKA_SASL_MECHANISM", "PLAIN")
        colony.conf_s("KAFKA_SASL_USERNAME", "username")
        colony.conf_s("KAFKA_SASL_PASSWORD", "password")
        colony.conf_s("KAFKA_SSL_CAFILE", "/etc/kafka/ca.pem")
        colony.conf_s("KAFKA_SSL_CERTFILE", "/etc/kafka/client.pem")
        colony.conf_s("KAFKA_SSL_KEYFILE", "/etc/kafka/client.key")
        colony.conf_s("KAFKA_SSL_PASSWORD", "key_password")
        colony.conf_s("KAFKA_SSL_CHECK_HOSTNAME", "0")

        with mock.patch.dict("sys.modules", dict(kafka=kafka)):
            result = observer_util._kafka_producer()

        kafka.KafkaProducer.assert_called_once_with(
            bootstrap_servers="localhost:9093",
            security_protocol="SASL_SSL",
            sasl_mechanism="PLAIN",
            sasl_plain_username="username",
            sasl_plain_password="password",
            ssl_cafile="/etc/kafka/ca.pem",
            ssl_certfile="/etc/kafka/client.pem",
            ssl_keyfile="/etc/kafka/client.key",
            ssl_password="key_password",
            ssl_check_hostname=False,
            reconnect_backoff_ms=150,
            reconnect_backoff_max_ms=120000,
        )
        self.assertEqual(result, kafka.KafkaProducer.return_value)

    def test_kafka_producer_cache(self):
        """
        Tests that the Kafka producer is cached per server, so that
        a single producer is created for the same server.
        """

        if mock == None:
            self.skipTest("Skipping test: mock unavailable")

        kafka = mock.Mock()
        kafka.__version__ = "2.0.2"

        colony.conf_s("KAFKA_SERVER", "localhost:9093")
        colony.conf_s("KAFKA_SSL_CAFILE", "/etc/kafka/ca.pem")

        with mock.patch.dict("sys.modules", dict(kafka=kafka)):
            result = observer_util._kafka_producer()
            result_cached = observer_util._kafka_producer()

        self.assertEqual(kafka.KafkaProducer.call_count, 1)
        self.assertEqual(result_cached, result)
        self.assertEqual(observer_util.KAFKA_PRODUCERS, {"localhost:9093": result})

    def test_kafka_producer_no_server(self):
        """
        Tests that no Kafka producer is created when no server
        is set, even if the SSL values are set.
        """

        if mock == None:
            self.skipTest("Skipping test: mock unavailable")

        kafka = mock.Mock()
        kafka.__version__ = "2.0.2"

        colony.conf_s("KAFKA_SSL_CAFILE", "/etc/kafka/ca.pem")

        with mock.patch.dict("sys.modules", dict(kafka=kafka)):
            result = observer_util._kafka_producer()

        self.assertEqual(result, None)
        self.assertEqual(kafka.KafkaProducer.call_count, 0)
        self.assertEqual(observer_util.KAFKA_PRODUCERS, dict())

    def test_kafka_producer_no_kafka(self):
        """
        Tests that no Kafka producer is created when the kafka
        module is not available.
        """

        if mock == None:
            self.skipTest("Skipping test: mock unavailable")

        colony.conf_s("KAFKA_SERVER", "localhost:9093")
        colony.conf_s("KAFKA_SSL_CAFILE", "/etc/kafka/ca.pem")

        with mock.patch.dict("sys.modules", dict(kafka=None)):
            result = observer_util._kafka_producer()

        self.assertEqual(result, None)
        self.assertEqual(observer_util.KAFKA_PRODUCERS, dict())
