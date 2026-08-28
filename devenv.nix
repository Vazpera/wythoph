{ pkgs, lib, config, inputs, ... }:

{
  # https://devenv.sh/basics/
  env.GREET = "devenv";

  packages = [ pkgs.git ];

  languages.rust.enable = true;
  languages.python.enable = true;
  languages.python.package = pkgs.python313; # Forces Python 3.13
  languages.python.poetry.enable = true;
  languages.python.poetry.activate.enable = true; 
  languages.python.poetry.install.enable = true; 

  scripts.hello.exec = ''
    echo hello from $GREET
  '';
  scripts.build-core.exec = ''
    echo "Building Rust backend..."
    cargo build --release
    cp $DEVENV_ROOT/target/release/libwythoph_core.so ./rust_core.so
  '';
  scripts.compile-addon.exec = ''
    echo "Compiling Addon..."
    echo "Creating dummy directory"
    mkdir ./wythoph
    echo "Copying files..."
    cp $DEVENV_ROOT/__init__.py ./wythoph
    cp $DEVENV_ROOT/rust_core.so ./wythoph
    echo "Zipping addon..."
    rm $DEVENV_ROOT/wythoph.zip && zip wythoph.zip ./wythoph/ -r
    echo "Deleting dummy directory"
    rm ./wythoph -r
  '';

  scripts.scripts.exec = ''
    echo "build-core    # Build Rust backend"
    echo "compile-addon # Compile the full addon"
  '';

  # https://devenv.sh/basics/
  enterShell = ''
    hello         # Run scripts directly
    git --version # Use packages
    scripts       # List scripts
  '';

  # https://devenv.sh/tasks/
  # tasks = {
  #   "myproj:setup".exec = "mytool build";
  #   "devenv:enterShell".after = [ "myproj:setup" ];
  # };

  # https://devenv.sh/tests/
  enterTest = ''
    echo "Running tests"
    git --version | grep --color=auto "${pkgs.git.version}" echo
  '';

  # https://devenv.sh/git-hooks/
  # git-hooks.hooks.shellcheck.enable = true;

  # See full reference at https://devenv.sh/reference/options/
}
