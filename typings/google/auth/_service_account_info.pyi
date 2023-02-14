"""
This type stub file was generated by pyright.
"""

"""Helper functions for loading data from a Google service account file."""
def from_dict(data, require=..., use_rsa_signer=...):
    """Validates a dictionary containing Google service account data.

    Creates and returns a :class:`google.auth.crypt.Signer` instance from the
    private key specified in the data.

    Args:
        data (Mapping[str, str]): The service account data
        require (Sequence[str]): List of keys required to be present in the
            info.
        use_rsa_signer (Optional[bool]): Whether to use RSA signer or EC signer.
            We use RSA signer by default.

    Returns:
        google.auth.crypt.Signer: A signer created from the private key in the
            service account file.

    Raises:
        MalformedError: if the data was in the wrong format, or if one of the
            required keys is missing.
    """
    ...

def from_filename(filename, require=..., use_rsa_signer=...): # -> tuple[Any, Unknown]:
    """Reads a Google service account JSON file and returns its parsed info.

    Args:
        filename (str): The path to the service account .json file.
        require (Sequence[str]): List of keys required to be present in the
            info.
        use_rsa_signer (Optional[bool]): Whether to use RSA signer or EC signer.
            We use RSA signer by default.

    Returns:
        Tuple[ Mapping[str, str], google.auth.crypt.Signer ]: The verified
            info and a signer instance.
    """
    ...
