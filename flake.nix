# SPDX-FileCopyrightText: 2024 Guilherme Leoi
#
# SPDX-License-Identifier: Apache-2.0

{
  description = "Python+Poetry Template";

  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";
    flake-utils.url = "github:numtide/flake-utils";
    poetry2nix.url = "github:nix-community/poetry2nix";
  };

  outputs = { self, nixpkgs, flake-utils, poetry2nix, ... }:
    flake-utils.lib.eachDefaultSystem (system:
      let
        # Get set of packages
        pkgs = import nixpkgs {
          inherit system;
        };
        # Get package specifications
        inherit (poetry2nix.lib.mkPoetry2Nix { inherit pkgs; }) mkPoetryApplication;
      in {
        packages = {
          poetryPackage = mkPoetryApplication {
            projectDir = self;
          };
          default = self.packages.${system}.poetryPackage;
        };
        devShells.default = pkgs.mkShell {
          inputsFrom = [ self.packages.${system}.poetryPackage ];
        };
        # Run `nix develop .#poetry` to access Poetry and update
        # pyproject.toml and poetry.lock
        devShells.poetry = pkgs.mkShell {
          packages = [ pkgs.poetry ];
        };
      }
    );
}