from ._frame import Command
from ._base import ResponseException, Functionality, Irq
try:
  from enum import Enum
except ImportError:
  from enum34 import Enum


class DigitalInputs(Functionality):
    """Attributes and methods needed for operating the digital inputs channels.

    Args:
        i2c_hat (:obj:`raspihats.i2c_hats._base.I2CHat`): I2CHat instance
        labels (:obj:`list` of :obj:`str`): Labels of digital input channels

    Attributes:
        channels (:obj:`list` of :obj:`bool`): List like object, provides access to digital inputs channels.
        r_counters (:obj:`list` of :obj:`int`): List like object, provides access to raising edge digital input counters.
        f_counters (:obj:`list` of :obj:`int`): List like object, provides access to falling edge digital input counters.
    """

    def __init__(self, i2c_hat, labels):
        Functionality.__init__(self, i2c_hat, labels)
        outer_instance = self

        class IRQReg(object):
            """IRQ registers"""

            @property
            def rising_edge_control(self):
                """:obj:`int`: The value of all IRQ Control reg, 1 bit represents 1 channel."""
                return i2c_hat.irq.get_reg(Irq.RegName.DI_RISING_EDGE_CONTROL.value)

            @rising_edge_control.setter
            def rising_edge_control(self, value):
                outer_instance._validate_value(value)
                i2c_hat.irq.set_reg(Irq.RegName.DI_RISING_EDGE_CONTROL.value, value)

            @property
            def falling_edge_control(self):
                """:obj:`int`: The value of all IRQ Control reg, 1 bit represents 1 channel."""
                return i2c_hat.irq.get_reg(Irq.RegName.DI_FALLING_EDGE_CONTROL.value)

            @falling_edge_control.setter
            def falling_edge_control(self, value):
                outer_instance._validate_value(value)
                i2c_hat.irq.set_reg(Irq.RegName.DI_FALLING_EDGE_CONTROL.value, value)

            @property
            def capture(self):
                """:obj:`int`: The value of all IRQ Control reg, 1 bit represents 1 channel."""
                return i2c_hat.irq.get_reg(Irq.RegName.DI_CAPTURE.value)

            @capture.setter
            def capture(self, value):
                if value != 0:
                    raise Exception("Value " + str(value) + " not allowed, only 0 is allowed, use 0 to clear the DI IRQ Capture Queue")
                i2c_hat.irq.set_reg(Irq.RegName.DI_CAPTURE.value, value)


        class Channels(object):
            def __getitem__(self, index):
                index = outer_instance._validate_channel_index(index)
                request = outer_instance._i2c_hat._request_frame_(Command.DI_GET_CHANNEL_STATE, [index])
                response = outer_instance._i2c_hat._transfer_(request, 2)
                data = response.data
                if len(data) != 2 or data[0] != index:
                    raise ResponseException('Invalid data')
                return data[1] > 0

            def __len__(self):
                return len(outer_instance.labels)

        class Counters(object):
            def __init__(self, counter_type):
                self.__counter_type = counter_type

            def __getitem__(self, index):
                index = outer_instance._validate_channel_index(index)
                request = outer_instance._i2c_hat._request_frame_(Command.DI_GET_COUNTER, [index, self.__counter_type])
                response = outer_instance._i2c_hat._transfer_(request, 6)
                data = response.data
                if (len(data) != 1 + 1 + 4) or (index != data[0]) or (self.__counter_type != data[1]):
                    raise ResponseException('Invalid data')
                return data[2] + (data[3] << 8) + (data[4] << 16) + (data[5] << 24)

            def __setitem__(self, index, value):
                index = outer_instance._validate_channel_index(index)
                if value != 0:
                    raise ValueError("only '0' is valid, it will reset the counter")
                request = outer_instance._i2c_hat._request_frame_(Command.DI_RESET_COUNTER, [index, self.__counter_type])
                response = outer_instance._i2c_hat._transfer_(request, 2)
                data = response.data
                if (len(data) != 2) or (index != data[0]) or (self.__counter_type != data[1]):
                    raise ResponseException('Invalid data')

            def __len__(self):
                return len(outer_instance.labels)

        self.channels = Channels()
        self.r_counters = Counters(1)
        self.f_counters = Counters(0)
        self.irq_reg = IRQReg()

    @property
    def value(self):
        """:obj:`int`: The value of all the digital inputs, 1 bit represents 1 channel."""
        return self._i2c_hat._get_u32_value_(Command.DI_GET_ALL_CHANNEL_STATES)

    def reset_counters(self):
        """Resets all digital input channel counters of all types(falling and rising edge).

        Raises:
            :obj:`raspihats.i2c_hats._base.ResponseException`: If the response hasn't got the expected format

        """
        request = self._i2c_hat._request_frame_(Command.DI_RESET_ALL_COUNTERS)
        response = self._i2c_hat._transfer_(request, 0)
        data = response.data
        if len(data) != 0:
            raise ResponseException('Invalid data')


class DigitalOutputs(Functionality):
    """Attributes and methods needed for operating the digital outputs channels.

    Args:
        i2c_hat (:obj:`raspihats.i2c_hats._base.I2CHat`): I2CHat instance
        labels (:obj:`list` of :obj:`str`): Labels of digital output channels

    Attributes:
        channels (:obj:`list` of :obj:`bool`): List like object, provides single channel access to digital outputs.

    """

    def __init__(self, i2c_hat, labels):
        Functionality.__init__(self, i2c_hat, labels)
        outer_instance = self

        class Channels(object):
            def __getitem__(self, index):
                index = outer_instance._validate_channel_index(index)
                request = outer_instance._i2c_hat._request_frame_(Command.DQ_GET_CHANNEL_STATE, [index])
                response = outer_instance._i2c_hat._transfer_(request, 2)
                data = response.data
                if len(data) != 2 or data[0] != index:
                    raise ResponseException('unexpected format')
                return data[1] > 0

            def __setitem__(self, index, value):
                index = outer_instance._validate_channel_index(index)
                value = int(value)
                if not (0 <= value <= 1):
                    raise ValueError("'" + str(value) + "' is not a valid value, use: 0 or 1, True or False")
                data = [index, value]
                request = outer_instance._i2c_hat._request_frame_(Command.DQ_SET_CHANNEL_STATE, data)
                response = outer_instance._i2c_hat._transfer_(request, 2)
                if data != response.data:
                    raise ResponseException('unexpected format')

            def __len__(self):
                return len(outer_instance.labels)

        self.channels = Channels()

    @property
    def value(self):
        """:obj:`int`: The value of all the digital outputs, 1 bit represents 1 channel."""
        return self._i2c_hat._get_u32_value_(Command.DQ_GET_ALL_CHANNEL_STATES)

    @value.setter
    def value(self, value):
        self._validate_value(value)
        self._i2c_hat._set_u32_value_(Command.DQ_SET_ALL_CHANNEL_STATES, value)

    @property
    def power_on_value(self):
        """:obj:`int`: Power On Value, this is loaded to outputs at power on."""
        return self._i2c_hat._get_u32_value_(Command.DQ_GET_POWER_ON_VALUE)

    @power_on_value.setter
    def power_on_value(self, value):
        self._validate_value(value)
        self._i2c_hat._set_u32_value_(Command.DQ_SET_POWER_ON_VALUE, value)

    @property
    def safety_value(self):
        """:obj:`int`: Safety Value, this is loaded to outputs at Cwdt Timeout."""

        return self._i2c_hat._get_u32_value_(Command.DQ_GET_SAFETY_VALUE)

    @safety_value.setter
    def safety_value(self, value):
        self._validate_value(value)
        self._i2c_hat._set_u32_value_(Command.DQ_SET_SAFETY_VALUE, value)
