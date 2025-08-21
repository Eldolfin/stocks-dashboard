{
  inputs = {
    nixpkgs.url = "nixpkgs/nixos-unstable";
    utils.url = "github:numtide/flake-utils";
    fenix = {
      url = "github:nix-community/fenix";
      inputs.nixpkgs.follows = "nixpkgs";
    };
  };
  outputs = {
    self,
    nixpkgs,
    utils,
    fenix,
  }:
    utils.lib.eachDefaultSystem (
      system: let
        pkgs = import nixpkgs {
          inherit system;
          config.allowUnfree = true;
        };
        # toolchain1 = with fenix.packages.${system};
        #   combine [
        #     minimal.cargo
        #     minimal.rustc
        #     targets."armv7-linux-androideabi".latest.rust-std
        #   ];
        # toolchain2 = with fenix.packages.${system};
        #   combine [
        #     minimal.cargo
        #     minimal.rustc
        #     targets."aarch64-linux-android".latest.rust-std
        #   ];
      in {
        devShell =
          (pkgs.buildFHSEnv
            {
              name = "clang-fhs";
              targetPkgs = p:
                with p; [
                  just
                  jdk17
                  deno
                  svelte-language-server
                  zlib
                  bionic
                  glibc_multi
                  cargo-tauri
                  android-studio
                  # toolchain1
                  # toolchain2
                  # androidenv.androidPkgs.ndk-bundle
                  fastlane
                ];
              runScript = "fish";
            }).env;
      }
    );
}
