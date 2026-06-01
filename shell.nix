{ pkgs ? import <nixpkgs> {} }:

let
  pythonEnv = pkgs.python3.withPackages (ps: with ps; [
    ipykernel
    pip
    notebook
  ]);
in

pkgs.mkShell {
  name = "ipykernel-environment";

  buildInputs = [
    pythonEnv
  ];

  shellHook = ''
    echo "Nix environment loaded with ipykernel."
    echo "To register this kernel with your user Jupyter directory, run:"
    echo "  python -m ipykernel install --user --name=nix-env --display-name=\"Python (Nix)\""
  '';
}