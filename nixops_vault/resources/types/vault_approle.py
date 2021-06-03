from typing import (
    Optional,
    Sequence,
)

from nixops.resources import ResourceOptions


class VaultApproleOptions(ResourceOptions):
    vaultToken: str
    vaultAddress: str
    roleName: str
    roleId: str
    bindSecretId: bool
    secretIdBoundCidrs: Sequence[str]
    tokenBoundCidrs: Sequence[str]
    policies: Sequence[str]
    secretIdNumUses: int
    secretIdTtl: str
    tokenNumUses: int
    tokenMaxTtl: str
    tokenTtl: str
    period: str
    enableLocalSecretIds: bool
    tokenType: str
    secretId: Optional[str]
    cidrList: Sequence[str]
