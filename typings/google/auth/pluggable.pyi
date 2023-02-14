"""
This type stub file was generated by pyright.
"""

from google.auth import _helpers, external_account

"""Pluggable Credentials.
Pluggable Credentials are initialized using external_account arguments which
are typically loaded from third-party executables. Unlike other
credentials that can be initialized with a list of explicit arguments, secrets
or credentials, external account clients use the environment and hints/guidelines
provided by the external_account JSON file to retrieve credentials and exchange
them for Google access tokens.

Example credential_source for pluggable credential:
{
    "executable": {
        "command": "/path/to/get/credentials.sh --arg1=value1 --arg2=value2",
        "timeout_millis": 5000,
        "output_file": "/path/to/generated/cached/credentials"
    }
}
"""
EXECUTABLE_SUPPORTED_MAX_VERSION = ...
EXECUTABLE_TIMEOUT_MILLIS_DEFAULT = ...
EXECUTABLE_TIMEOUT_MILLIS_LOWER_BOUND = ...
EXECUTABLE_TIMEOUT_MILLIS_UPPER_BOUND = ...
EXECUTABLE_INTERACTIVE_TIMEOUT_MILLIS_LOWER_BOUND = ...
EXECUTABLE_INTERACTIVE_TIMEOUT_MILLIS_UPPER_BOUND = ...
class Credentials(external_account.Credentials):
    """External account credentials sourced from executables."""
    def __init__(self, audience, subject_token_type, token_url, credential_source, *args, **kwargs) -> None:
        """Instantiates an external account credentials object from a executables.

        Args:
            audience (str): The STS audience field.
            subject_token_type (str): The subject token type.
            token_url (str): The STS endpoint URL.
            credential_source (Mapping): The credential source dictionary used to
                provide instructions on how to retrieve external credential to be
                exchanged for Google access tokens.

                Example credential_source for pluggable credential:

                    {
                        "executable": {
                            "command": "/path/to/get/credentials.sh --arg1=value1 --arg2=value2",
                            "timeout_millis": 5000,
                            "output_file": "/path/to/generated/cached/credentials"
                        }
                    }
            args (List): Optional positional arguments passed into the underlying :meth:`~external_account.Credentials.__init__` method.
            kwargs (Mapping): Optional keyword arguments passed into the underlying :meth:`~external_account.Credentials.__init__` method.

        Raises:
            google.auth.exceptions.RefreshError: If an error is encountered during
                access token retrieval logic.
            google.auth.exceptions.InvalidValue: For invalid parameters.
            google.auth.exceptions.MalformedError: For invalid parameters.

        .. note:: Typically one of the helper constructors
            :meth:`from_file` or
            :meth:`from_info` are used instead of calling the constructor directly.
        """
        ...
    
    @_helpers.copy_docstring(external_account.Credentials)
    def retrieve_subject_token(self, request): # -> Any:
        ...
    
    def revoke(self, request): # -> None:
        """Revokes the subject token using the credential_source object.

        Args:
            request (google.auth.transport.Request): A callable used to make
                HTTP requests.
        Raises:
            google.auth.exceptions.RefreshError: If the executable revocation
                not properly executed.

        """
        ...
    
    @property
    def external_account_id(self): # -> str:
        """Returns the external account identifier.

        When service account impersonation is used the identifier is the service
        account email.

        Without service account impersonation, this returns None, unless it is
        being used by the Google Cloud CLI which populates this field.
        """
        ...
    
    @classmethod
    def from_info(cls, info, **kwargs): # -> Credentials:
        """Creates a Pluggable Credentials instance from parsed external account info.

        Args:
            info (Mapping[str, str]): The Pluggable external account info in Google
                format.
            kwargs: Additional arguments to pass to the constructor.

        Returns:
            google.auth.pluggable.Credentials: The constructed
                credentials.

        Raises:
            google.auth.exceptions.InvalidValue: For invalid parameters.
            google.auth.exceptions.MalformedError: For invalid parameters.
        """
        ...
    
    @classmethod
    def from_file(cls, filename, **kwargs): # -> Credentials:
        """Creates an Pluggable Credentials instance from an external account json file.

        Args:
            filename (str): The path to the Pluggable external account json file.
            kwargs: Additional arguments to pass to the constructor.

        Returns:
            google.auth.pluggable.Credentials: The constructed
                credentials.
        """
        ...
    

