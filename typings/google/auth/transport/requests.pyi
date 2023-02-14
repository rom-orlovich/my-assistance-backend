"""
This type stub file was generated by pyright.
"""

import requests.adapters
from google.auth import transport

"""Transport adapter for Requests."""
_LOGGER = ...
_DEFAULT_TIMEOUT = ...
class _Response(transport.Response):
    """Requests transport response adapter.

    Args:
        response (requests.Response): The raw Requests response.
    """
    def __init__(self, response) -> None:
        ...
    
    @property
    def status(self):
        ...
    
    @property
    def headers(self):
        ...
    
    @property
    def data(self):
        ...
    


class TimeoutGuard:
    """A context manager raising an error if the suite execution took too long.

    Args:
        timeout (Union[None, Union[float, Tuple[float, float]]]):
            The maximum number of seconds a suite can run without the context
            manager raising a timeout exception on exit. If passed as a tuple,
            the smaller of the values is taken as a timeout. If ``None``, a
            timeout error is never raised.
        timeout_error_type (Optional[Exception]):
            The type of the error to raise on timeout. Defaults to
            :class:`requests.exceptions.Timeout`.
    """
    def __init__(self, timeout, timeout_error_type=...) -> None:
        ...
    
    def __enter__(self): # -> Self@TimeoutGuard:
        ...
    
    def __exit__(self, exc_type, exc_value, traceback): # -> None:
        ...
    


class Request(transport.Request):
    """Requests request adapter.

    This class is used internally for making requests using various transports
    in a consistent way. If you use :class:`AuthorizedSession` you do not need
    to construct or use this class directly.

    This class can be useful if you want to manually refresh a
    :class:`~google.auth.credentials.Credentials` instance::

        import google.auth.transport.requests
        import requests

        request = google.auth.transport.requests.Request()

        credentials.refresh(request)

    Args:
        session (requests.Session): An instance :class:`requests.Session` used
            to make HTTP requests. If not specified, a session will be created.

    .. automethod:: __call__
    """
    def __init__(self, session=...) -> None:
        ...
    
    def __del__(self): # -> None:
        ...
    
    def __call__(self, url, method=..., body=..., headers=..., timeout=..., **kwargs): # -> _Response:
        """Make an HTTP request using requests.

        Args:
            url (str): The URI to be requested.
            method (str): The HTTP method to use for the request. Defaults
                to 'GET'.
            body (bytes): The payload or body in HTTP request.
            headers (Mapping[str, str]): Request headers.
            timeout (Optional[int]): The number of seconds to wait for a
                response from the server. If not specified or if None, the
                requests default timeout will be used.
            kwargs: Additional arguments passed through to the underlying
                requests :meth:`~requests.Session.request` method.

        Returns:
            google.auth.transport.Response: The HTTP response.

        Raises:
            google.auth.exceptions.TransportError: If any exception occurred.
        """
        ...
    


class _MutualTlsAdapter(requests.adapters.HTTPAdapter):
    """
    A TransportAdapter that enables mutual TLS.

    Args:
        cert (bytes): client certificate in PEM format
        key (bytes): client private key in PEM format

    Raises:
        ImportError: if certifi or pyOpenSSL is not installed
        OpenSSL.crypto.Error: if client cert or key is invalid
    """
    def __init__(self, cert, key) -> None:
        ...
    
    def init_poolmanager(self, *args, **kwargs): # -> None:
        ...
    
    def proxy_manager_for(self, *args, **kwargs):
        ...
    


class _MutualTlsOffloadAdapter(requests.adapters.HTTPAdapter):
    """
    A TransportAdapter that enables mutual TLS and offloads the client side
    signing operation to the signing library.

    Args:
        enterprise_cert_file_path (str): the path to a enterprise cert JSON
            file. The file should contain the following field:

                {
                    "libs": {
                        "signer_library": "...",
                        "offload_library": "..."
                    }
                }

    Raises:
        ImportError: if certifi or pyOpenSSL is not installed
        google.auth.exceptions.MutualTLSChannelError: If mutual TLS channel
            creation failed for any reason.
    """
    def __init__(self, enterprise_cert_file_path) -> None:
        ...
    
    def init_poolmanager(self, *args, **kwargs): # -> None:
        ...
    
    def proxy_manager_for(self, *args, **kwargs):
        ...
    


class AuthorizedSession(requests.Session):
    """A Requests Session class with credentials.

    This class is used to perform requests to API endpoints that require
    authorization::

        from google.auth.transport.requests import AuthorizedSession

        authed_session = AuthorizedSession(credentials)

        response = authed_session.request(
            'GET', 'https://www.googleapis.com/storage/v1/b')


    The underlying :meth:`request` implementation handles adding the
    credentials' headers to the request and refreshing credentials as needed.

    This class also supports mutual TLS via :meth:`configure_mtls_channel`
    method. In order to use this method, the `GOOGLE_API_USE_CLIENT_CERTIFICATE`
    environment variable must be explicitly set to ``true``, otherwise it does
    nothing. Assume the environment is set to ``true``, the method behaves in the
    following manner:

    If client_cert_callback is provided, client certificate and private
    key are loaded using the callback; if client_cert_callback is None,
    application default SSL credentials will be used. Exceptions are raised if
    there are problems with the certificate, private key, or the loading process,
    so it should be called within a try/except block.

    First we set the environment variable to ``true``, then create an :class:`AuthorizedSession`
    instance and specify the endpoints::

        regular_endpoint = 'https://pubsub.googleapis.com/v1/projects/{my_project_id}/topics'
        mtls_endpoint = 'https://pubsub.mtls.googleapis.com/v1/projects/{my_project_id}/topics'

        authed_session = AuthorizedSession(credentials)

    Now we can pass a callback to :meth:`configure_mtls_channel`::

        def my_cert_callback():
            # some code to load client cert bytes and private key bytes, both in
            # PEM format.
            some_code_to_load_client_cert_and_key()
            if loaded:
                return cert, key
            raise MyClientCertFailureException()

        # Always call configure_mtls_channel within a try/except block.
        try:
            authed_session.configure_mtls_channel(my_cert_callback)
        except:
            # handle exceptions.

        if authed_session.is_mtls:
            response = authed_session.request('GET', mtls_endpoint)
        else:
            response = authed_session.request('GET', regular_endpoint)


    You can alternatively use application default SSL credentials like this::

        try:
            authed_session.configure_mtls_channel()
        except:
            # handle exceptions.

    Args:
        credentials (google.auth.credentials.Credentials): The credentials to
            add to the request.
        refresh_status_codes (Sequence[int]): Which HTTP status codes indicate
            that credentials should be refreshed and the request should be
            retried.
        max_refresh_attempts (int): The maximum number of times to attempt to
            refresh the credentials and retry the request.
        refresh_timeout (Optional[int]): The timeout value in seconds for
            credential refresh HTTP requests.
        auth_request (google.auth.transport.requests.Request):
            (Optional) An instance of
            :class:`~google.auth.transport.requests.Request` used when
            refreshing credentials. If not passed,
            an instance of :class:`~google.auth.transport.requests.Request`
            is created.
        default_host (Optional[str]): A host like "pubsub.googleapis.com".
            This is used when a self-signed JWT is created from service
            account credentials.
    """
    def __init__(self, credentials, refresh_status_codes=..., max_refresh_attempts=..., refresh_timeout=..., auth_request=..., default_host=...) -> None:
        ...
    
    def configure_mtls_channel(self, client_cert_callback=...): # -> None:
        """Configure the client certificate and key for SSL connection.

        The function does nothing unless `GOOGLE_API_USE_CLIENT_CERTIFICATE` is
        explicitly set to `true`. In this case if client certificate and key are
        successfully obtained (from the given client_cert_callback or from application
        default SSL credentials), a :class:`_MutualTlsAdapter` instance will be mounted
        to "https://" prefix.

        Args:
            client_cert_callback (Optional[Callable[[], (bytes, bytes)]]):
                The optional callback returns the client certificate and private
                key bytes both in PEM format.
                If the callback is None, application default SSL credentials
                will be used.

        Raises:
            google.auth.exceptions.MutualTLSChannelError: If mutual TLS channel
                creation failed for any reason.
        """
        ...
    
    def request(self, method, url, data=..., headers=..., max_allowed_time=..., timeout=..., **kwargs): # -> Response:
        """Implementation of Requests' request.

        Args:
            timeout (Optional[Union[float, Tuple[float, float]]]):
                The amount of time in seconds to wait for the server response
                with each individual request. Can also be passed as a tuple
                ``(connect_timeout, read_timeout)``. See :meth:`requests.Session.request`
                documentation for details.
            max_allowed_time (Optional[float]):
                If the method runs longer than this, a ``Timeout`` exception is
                automatically raised. Unlike the ``timeout`` parameter, this
                value applies to the total method execution time, even if
                multiple requests are made under the hood.

                Mind that it is not guaranteed that the timeout error is raised
                at ``max_allowed_time``. It might take longer, for example, if
                an underlying request takes a lot of time, but the request
                itself does not timeout, e.g. if a large file is being
                transmitted. The timout error will be raised after such
                request completes.
        """
        ...
    
    @property
    def is_mtls(self): # -> bool:
        """Indicates if the created SSL channel is mutual TLS."""
        ...
    
    def close(self): # -> None:
        ...
    

