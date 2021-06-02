from typing import (
    Optional,
    Sequence,
    Union,
)
from typing_extensions import Literal

from nixops.resources import ResourceOptions


class DataOptions(ResourceOptions):
    key: str
    value: str


class SecretsOptions(ResourceOptions):
    path: str
    maxVersions: int
    data: Sequence[DataOptions]


class VaultKVSecretEngineOptions(ResourceOptions):
    vaultToken: str
    vaultAddress: str
    name: str
    type: str
    description: str
    local: bool
    sealWrap: bool
    defaultLeaseTtl: str
    maxLeaseTtl: str
    forceNoCache: bool
    auditNonHmacRequestKeys: Sequence[str]
    auditNonHmacResponseKeys: Sequence[str]
    listingVisibility: Literal["hidden", "unauth"]
    passthroughRequestHeaders: Sequence[str]
    allowedResponseHeaders: Sequence[str]
    version: int
    secrets: Sequence[SecretsOptions]
