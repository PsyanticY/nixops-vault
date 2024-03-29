# -*- coding: utf-8 -*-

# Automatic provisioning of Hashicorp Vault policies

import json

import nixops.util
import nixops.resources
from nixops.diff import Diff, Handler
from nixops.state import StateDict
import nixops_vault.vault_common
from .types.vault_policy import VaultPolicyOptions


class VaultPolicyDefinition(nixops.resources.ResourceDefinition):
    """Definition of a vault policy."""

    config: VaultPolicyOptions

    @classmethod
    def get_type(cls):
        return "vault-policy"

    @classmethod
    def get_resource_type(cls):
        return "vaultPolicy"

    def show_type(self):
        return "{0}".format(self.get_type())


class VaultPolicyState(nixops.resources.DiffEngineResourceState[VaultPolicyDefinition]):
    """State of a vault policy."""

    definition_type = VaultPolicyDefinition

    state = nixops.util.attr_property(
        "state", nixops.resources.ResourceState.MISSING, int
    )
    policies = nixops.util.attr_property("policies", {}, "json")
    _reserved_keys = ["vaultToken"]

    @classmethod
    def get_type(cls):
        return "vault-policy"

    def __init__(self, depl, name, id):
        nixops.resources.DiffEngineResourceState.__init__(self, depl, name, id)
        self.handle_create_policy = Handler(
            ["policies", "vaultAddress"], handle=self.realize_create_policy
        )
        self.handle_update_policy = Handler(
            ["policies"], handle=self.realize_create_policy
        )

    def show_type(self):
        s = super(VaultPolicyState, self).show_type()
        return s

    def get_definition_prefix(self):
        return "resources.vaultPolicy."

    def create_after(self, resources, defn):
        return {
            r
            for r in resources
            if isinstance(
                r,
                nixops_vault.resources.vault_kv_secret_engine.VaultKVSecretEngineState,
            )
        }

    def realize_create_policy(self, allow_recreate, update=False):
        config = self.get_defn().config
        self._state["name"] = config.name
        self._state["vaultAddress"] = config.vaultAddress
        self._state["vaultToken"] = config.vaultToken

        if self.policies:
            self.log("Updating policy `{0}`...".format(self._state["name"]))
        else:
            self.log("Creating policy `{0}`...".format(self._state["name"]))

        policy_definition = ""
        for i in config.policies:
            policy_definition = (
                policy_definition
                + 'path "{0}" {{ capabilities = {1} }} '.format(
                    i.path, json.dumps(i.capabilities)
                )
            )

        data = {"policy": policy_definition}

        r = nixops_vault.vault_common.vault_post(
            config.vaultToken, config.vaultAddress, self._state["name"], data, "policy"
        )

        if r.status_code != 204:
            raise Exception("{} {}, {}".format(r.status_code, r.reason, r.json()))

        with self.depl._db:
            self.state = self.UP
            self._state["vaultAddress"] = config.vaultAddress
            self._state["policies"] = config.policies

    def _check(self):
        if self._state["name"] is None:
            return

        r = nixops_vault.vault_common.vault_get(
            self._state["vaultToken"],
            self._state["vaultAddress"],
            self._state["name"],
            "policy",
        )

        if r.status_code == 404:
            self.warn(
                "policy '{0}' was deleted from outside nixops,"
                " it needs to be recreated...".format(self._state["name"])
            )
            self.destroy()
        elif r.status_code != 200:
            raise Exception("{} {}, {}".format(r.status_code, r.reason, r.json()))

    def _destroy(self):
        if self.state != self.UP:
            return
        self.log("deleting policy `{0}`...".format(self._state["name"]))
        r = nixops_vault.vault_common.vault_delete(
            self._state["vaultToken"],
            self._state["vaultAddress"],
            self._state["name"],
            "policy",
        )
        if r.status_code == 204:
            pass
        else:
            raise Exception(r.json())

        with self.depl._db:
            self.state = self.MISSING
            self._state["policies"] = None
            self._state["vaultToken"] = None
            self._state["vaultAddress"] = None
            self._state["name"] = None

    def destroy(self, wipe=False):
        self._destroy()
        return True
