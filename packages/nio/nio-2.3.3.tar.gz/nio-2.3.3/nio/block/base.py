""" The base class for creating nio Blocks.

A block contains modular functionality to be used inside of Services. To create
a custom block, extend this Block class and override the appropriate methods.
"""
from nio.block.context import BlockContext
from nio.block.terminals import Terminal, TerminalType, input, output, \
    DEFAULT_TERMINAL
from nio.command import command
from nio.command.holder import CommandHolder
from nio.router.base import BlockRouter
from nio.properties import PropertyHolder, StringProperty, \
    VersionProperty, SelectProperty
from nio.util.logging import get_nio_logger
from nio.util.logging.levels import LogLevel
from nio.util.runner import Runner
from nio.signal.status import BlockStatusSignal
from nio.signal.base import Signal


@command('properties')
class Base(PropertyHolder, CommandHolder, Runner):

    """The base class for blocks to inherit from."""

    version = VersionProperty(version='0.0.0')
    type = StringProperty(title="Type", visible=False, readonly=True)
    name = StringProperty(title="Name", visible=False)
    log_level = SelectProperty(enum=LogLevel,
                               title="Log Level", default="NOTSET")

    def __init__(self, status_change_callback=None):
        """ Create a new block instance.

        Take care of setting up instance variables in your block's constructor.
        Note that the properties of the block are not available when the block
        is created. Those will be available when the block is configured.

        It is normally meaningless to pass variables to the constructor of the
        block. Any data the block requires will be passed through the
        BlockContext when the block is configured.
        """

        # We will replace the block's logger with its own name once we learn
        # what that name is during configure()
        self.logger = get_nio_logger('default')

        super().__init__(status_change_callback=status_change_callback)

        # store block type so that it gets serialized
        self.type = self.__class__.__name__

        self._block_router = None
        self._service_name = None
        self._default_input = Terminal.get_default_terminal_on_class(
            self.__class__, TerminalType.input)
        self._default_output = Terminal.get_default_terminal_on_class(
            self.__class__, TerminalType.output)

    def configure(self, context):
        """Overrideable method to be called when the block configures.

        The block creator should call the configure method on the parent,
        after which it can assume that any parent configuration options present
        on the block are loaded in as class variables. They can also assume
        that all functional modules in the service process are loaded and
        started.

        Args:
            context (BlockContext): The context to use to configure the block.

        Raises:
            TypeError: If the specified router is not a BlockRouter
        """
        if not isinstance(context, BlockContext):
            raise TypeError("Block must be configured with a BlockContext")
        # Ensure it is a BlockRouter so we can safely notify
        if not isinstance(context.block_router, BlockRouter):
            raise TypeError("Block's router must be instance of BlockRouter")

        self._block_router = context.block_router

        # load the configuration as class variables
        self.from_dict(context.properties, self.logger)
        # verify that block properties are valid
        self.validate()

        self.logger = get_nio_logger(self.name())
        self.logger.setLevel(self.log_level())
        self._service_name = context.service_name

    def start(self):
        """Overrideable method to be called when the block starts.

        The block creator can assume at this point that the block's
        initialization is complete and that the service and block router
        are in "starting" state.
        """
        pass  # pragma: no cover

    def stop(self):
        """Overrideable method to be called when the block stops.

        The block creator can assume at this point that the service and block
        router are in "stopping" state. All modules are still available for use
        in the service process.
        """
        pass  # pragma: no cover

    def notify_signals(self, signals, output_id=None):
        """Notify signals to router.

        This is the method the block should call whenever it would like
        to "output" signals for the router to send downstream.

        Args:
            signals (list): A list of signals to notify to the router
            output_id: The identifier of the output terminal to notify the
                signals on

        The signals argument is handled as follows:
            - a dictionary is not allowed
            - if a single signal is notified not as an iterable, it will get
            wrapped inside a list before forwarding to block router.

        Raises:
            TypeError: when signals are not instances of class Signal
        """

        if isinstance(signals, dict):
            raise TypeError("Signals cannot be a dictionary")

        # if a single Signal is being notified, make it a list
        if isinstance(signals, Signal):
            signals = [signals]

        self._block_router.notify_signals(self, signals, output_id)

    def notify_management_signal(self, signal):
        """Notify a management signal to router.

        Args:
            signal: signal to notify

        This is a special type of signal notification that does not actually
        propogate signals in the service. Instead, it is used to communicate
        some information to the block router about the block. For example,
        the block can report itself in an error state and thus prevent other
        signals from being delivered to it.
        """
        if isinstance(signal, BlockStatusSignal):
            # set service block is part of
            signal.service_name = self._service_name
            signal.block_name = self.name()
            self.status.add(signal.status)
        self._block_router.notify_management_signal(self, signal)

    def process_signals(self, signals, input_id=DEFAULT_TERMINAL):
        """Overrideable method to be called when signals are delivered.

        This method will be called by the block router whenever signals
        are sent to the block. The method should not return the modified
        signals, but rather call `notify_signals` so that the router
        can route them properly.

        Args:
            signals (list): A list of signals to be processed by the block
            input_id: The identifier of the input terminal the signals are
                being delivered to
        """
        pass  # pragma: no cover

    @classmethod
    def get_description(cls):
        """ Get a dictionary description of this block.

        Returns:
            dict: A dictionary containing the blocks properties and commands
        """
        properties = super().get_description()
        commands = cls.get_command_description()

        return {
            'properties': properties,
            'commands': commands
        }

    def properties(self):
        """ Returns block runtime properties """
        return self.to_dict()

    @classmethod
    def inputs(cls):
        """ A list of the block's input terminals """
        return Terminal.get_terminals_on_class(cls, TerminalType.input)

    @classmethod
    def outputs(cls):
        """ A list of the block's output terminals """
        return Terminal.get_terminals_on_class(cls, TerminalType.output)

    def is_input_valid(self, input_id):
        """ Find out if input is valid

        Args:
            input_id: input identifier

        Returns:
            bool: True if the input ID exists on this block
        """
        return input_id in [i.id for i in self.__class__.inputs()]

    def is_output_valid(self, output_id):
        """ Find out if output is valid

        Args:
            output_id: output identifier

        Returns:
            bool: True if the output ID exists on this block
        """
        return output_id in [o.id for o in self.__class__.outputs()]


@input(DEFAULT_TERMINAL, default=True, label="default")
@output(DEFAULT_TERMINAL, default=True, label="default")
class Block(Base):
    pass
