from typing import (
    Optional,
    Sequence,
    Union,
)
from typing_extensions import Literal

from nixops.resources import (
    ResourceOptions,
    ResourceEval,
)


class PolicyOptions(ResourceOptions):
    path: Union[str, ResourceEval]
    capabilities: Sequence[Literal["create", "read", "update", "delete", "list", "sudo", "deny"]]


class VaultPolicyOptions(ResourceOptions):
    vaultToken: str
    vaultAddress: str
    name: str
    policies: Sequence[PolicyOptions]
