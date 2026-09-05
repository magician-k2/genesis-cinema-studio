{ pkgs }: {
  deps = [
    pkgs.python311
    pkgs.python311Packages.pip
    pkgs.ffmpeg-full
    pkgs.libGL
    pkgs.glib
    pkgs.xorg.libX11
    pkgs.xorg.libXext
    pkgs.xorg.libXrender
  ];
}
