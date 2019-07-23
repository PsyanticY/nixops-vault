{ nixopsHashicorpvault ? { outPath = ./.; revCount = 0; shortRev = "abcdef"; rev = "HEAD"; }
, nixpkgs ? <nixpkgs>
, officialRelease ? false
}:
let
  pkgs = import nixpkgs {};
  version =  "1.7" + (if officialRelease then "" else "pre${toString nixopshashicorpvault.revCount}_${nixopshashicorpvault.shortRev}");
in
  rec {
    build = pkgs.lib.genAttrs [ "x86_64-linux" "i686-linux" "x86_64-darwin" ] (system:
      with import nixpkgs { inherit system; };
      python2Packages.buildPythonApplication rec {
        name = "nixops-hashicorpvault";
        src = ./.;
        prePatch = ''
          for i in setup.py; do
            substituteInPlace $i --subst-var-by version ${version}
          done
        '';
        # uncomment after adding checks
        #buildInputs = [ python2Packages.nose python2Packages.coverage ];
        #doCheck = true;
        postInstall = ''
          mkdir -p $out/share/nix/nixops-hashicorpvault
          cp -av nix/* $out/share/nix/nixops-hashicorpvault
        '';
        meta.description = "NixOps HashiCorp Vault resources for ${stdenv.system}";
      }
    );
  }

