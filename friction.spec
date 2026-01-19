Name:           friction
Version:        {{{ git_dir_version }}}
Release:        1%{?dist}
Summary:        A modern 2D motion graphics app

License:        GPLv3
URL:            https://github.com/poseidonn/myfriction.git
# Copr bunu sizin için orijinal repodan çekecek
Source:         {{{ git_dir_pack }}}

BuildRequires:  cmake
BuildRequires:  clang
BuildRequires:  llvm
BuildRequires:  ninja-build
BuildRequires:  fontconfig-devel 
BuildRequires:  freetype-devel
BuildRequires:  libunwind-devel
BuildRequires:  libatomic
BuildRequires:  python3
BuildRequires:  qt5-qtbase-devel
BuildRequires:  qt5-qtmultimedia-devel
BuildRequires:  qt5-qtsvg-devel
BuildRequires:  pkgconfig(libavcodec)
BuildRequires:  pkgconfig(libavformat)
BuildRequires:  pkgconfig(libswscale)
BuildRequires:  pkgconfig(libavutil)
BuildRequires:  mesa-libGL-devel
BuildRequires:  git
BuildRequires:  expat-devel
BuildRequires:  libuuid-devel
# Mevcutlara ekleyin
BuildRequires:  libjpeg-turbo-devel
BuildRequires:  libpng-devel
BuildRequires:  libwebp-devel
BuildRequires:  zlib-devel
BuildRequires:  libatomic
BuildRequires:  mesa-libGLU-devel
BuildRequires:  libXcursor-devel
BuildRequires:  libXi-devel
BuildRequires:  libXinerama-devel
BuildRequires:  libXrandr-devel
BuildRequires:  libstdc++-static
BuildRequires:  libjpeg-turbo-devel
BuildRequires:  libpng-devel
BuildRequires:  libwebp-devel

%description
Friction is a professional 2D motion graphics application.

%prep
# Mevcut dizini temizle ve kodu çek
rm -rf %{_builddir}/*
cd %{_builddir}
git clone --recursive https://github.com/poseidonn/myfriction.git .

# --- FFmpeg 7+ Uyumluluk Yamaları (Kritik Bölüm) ---
# av_get_channel_layout_nb_channels -> av_get_channel_layout_nb_channels (Eskisi) 
# Yerine modern olan av_get_channel_layout_nb_channels kullanmak yerine 
# kodun çalışması için basit bir makro ekleyelim veya doğrudan kanalları manuel alalım.

sed -i 's/av_get_channel_layout_nb_channels/av_get_channel_layout_nb_channels/g' src/core/CacheHandlers/samples.h

# AVFrame->channel_layout hatasını aşmak için (Kaba ama etkili bir çözüm)
sed -i 's/frame->channel_layout/frame->ch_layout.nb_channels/g' src/core/videoencoder.h

%build
# Artık 'cd myfriction' yapmaya gerek yok, çünkü kod doğrudan kök dizinde
export CC=clang
export CXX=clang++

# -Wno-error ekleyerek eski kod hatalarını 'uyarı' seviyesine çekiyoruz
%cmake -DCMAKE_C_COMPILER=clang -DCMAKE_CXX_COMPILER=clang++ -G Ninja \
       -DCMAKE_CXX_FLAGS="-Wno-error=deprecated-declarations -Wno-error=unused-command-line-argument" \
       -S . -B redhat-linux-build

%cmake_build -- -j2

%install
# Kurulum aşamasında cmake'in oluşturduğu build klasörüne bakmasını sağlıyoruz
%cmake_install

%files
%{_bindir}/friction
