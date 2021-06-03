{
 # config_exporters = { optionalAttrs, ... }: [];
 # options = [];
  resources = { evalResources, zipAttrs, resourcesByType, ... }: {
    vaultApprole = evalResources ./vault-approle.nix (zipAttrs resourcesByType.vaultApprole or []);
    vaultPolicy = evalResources ./vault-policy.nix (zipAttrs resourcesByType.vaultPolicy or []);
    vaultKVSecretEngine = evalResources ./vault-kv-secret-engine.nix (zipAttrs resourcesByType.vaultKVSecretEngine or []);
  };
}
