{
  description = "Simple wallpaper changer for Hyprland";

  inputs = {
    nixpkgs.url = "nixpkgs/nixos-unstable";
    systems.url = "github:nix-systems/default-linux";
    flake-utils = {
      url = "github:numtide/flake-utils";
      inputs.systems.follows = "systems";
    };
    pyproject-nix = {
      url = "github:nix-community/pyproject.nix";
      inputs.nixpkgs.follows = "nixpkgs";
    };
  };

  outputs = { nixpkgs, flake-utils, pyproject-nix, ... }:
    flake-utils.lib.eachDefaultSystem (system: let
      pkgs = nixpkgs.legacyPackages.${system};
      python = pkgs.python314;
      project = pyproject-nix.lib.project.loadPyproject {
        projectRoot = ./.;
      };
    in {
      devShells.default =
        pkgs.mkShell {
          packages = [ python ];
          shellHook = ''
            echo "Successfully initialized development shell!"
          '';
        };
      
      packages.default = 
        let
          attrs = project.renderers.buildPythonPackage { inherit python; };
        in 
          python.pkgs.buildPythonPackage (attrs // {});
    });
}
