from unittest import TestCase, mock
from . import TLSSysLogHandler
import ssl
import logging
import socket



class LogHandlerTest(TestCase):

    @mock.patch('socket.socket')
    @mock.patch('ssl.wrap_socket')
    def test_log_handler(self, wrap_socket, socket_constructor):
        # Mock the inner TCP socket
        mock_socket = mock.MagicMock()
        socket_constructor.return_value = mock_socket

        # Mock the TLS wrapped socket
        mock_wrapped_socket = mock.MagicMock()
        wrap_socket.return_value = mock_wrapped_socket

        # Build the logging handler
        logger, syslog_handler = self._build_logger()

        # Make sure socket was constructed correctly
        socket_constructor.assert_called_once_with(socket.AF_INET, socket.SOCK_STREAM)
        wrap_socket.assert_called_once_with(mock_socket, ssl_version=ssl.PROTOCOL_TLS)
        mock_wrapped_socket.connect.assert_called_once_with(('logsX.papertrailapp.com', 55555))

        # Send a message and wait for the queue to empty
        logger.info("This is a test message")
        syslog_handler.close()

        # Make sure message was written to the socket
        mock_wrapped_socket.send.assert_called_once_with(b'<14>Jan 01 15:35:48 tcp-log-tester root: INFO This is a test message\n')


    @mock.patch('socket.socket')
    @mock.patch('ssl.wrap_socket')
    def test_socket_throws_os_error(self, wrap_socket, socket_constructor):
        # Mock the inner TCP socket
        mock_socket = mock.MagicMock()
        socket_constructor.return_value = mock_socket

        # Mock the TLS wrapped socket
        mock_wrapped_socket = mock.MagicMock()
        wrap_socket.return_value = mock_wrapped_socket

        # Make the TLS socket throw an OSError when sending data
        mock_wrapped_socket.send.side_effect = OSError('Network is down')

        # Build the logging handler
        logger, syslog_handler = self._build_logger()

        # Make sure socket was constructed correctly
        socket_constructor.assert_called_once_with(socket.AF_INET, socket.SOCK_STREAM)
        wrap_socket.assert_called_once_with(mock_socket, ssl_version=ssl.PROTOCOL_TLS)
        mock_wrapped_socket.connect.assert_called_once_with(('logsX.papertrailapp.com', 55555))

        # Send a message and wait for the queue to empty
        logger.info("This is a test message")
        syslog_handler.close()

        # Make sure thread attempted to reconnect the socket
        self.assertEqual(socket_constructor.call_count, 2)
        self.assertEqual(wrap_socket.call_count, 2)
        self.assertEqual(mock_wrapped_socket.connect.call_count, 2)

        # Make sure message attempted twice
        self.assertEqual(mock_wrapped_socket.send.call_count, 2, 'Should try to send data twice')


    def _build_logger(self):
        logger = logging.getLogger()
        logger.setLevel(logging.INFO)

        formatter = logging.Formatter('Jan 01 15:35:48 tcp-log-tester %(name)s: %(levelname)s %(message)s', datefmt='%b %d %H:%M:%S')

        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)

        syslog_handler = TLSSysLogHandler(
            address=('logsX.papertrailapp.com', 55555),
            timeout=1,
            ssl_kwargs={ 'ssl_version': ssl.PROTOCOL_TLS })
        syslog_handler.setFormatter(formatter)
        logger.addHandler(syslog_handler)

        return logger, syslog_handler
