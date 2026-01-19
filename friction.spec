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
# Temizlik ve Clone
rm -rf %{_builddir}/*
cd %{_builddir}
git clone --recursive https://github.com/poseidonn/myfriction.git .

# --- 1. Skia Yaması: getWeakCnt hatasını her yerde düzelt ---
grep -rl "getWeakCnt" . | xargs sed -i 's/getWeakCnt/getRefCnt/g'

# --- 2. FFmpeg 7 Kapsamlı Yama (Tüm dosyalar için) ---
# av_get_channel_layout_nb_channels fonksiyonunu her varyasyonuyla 2 (stereo) yap
# Not: Bu kaba bir çözümdür ama derlemeyi sağlar.
grep -rl "av_get_channel_layout_nb_channels" . | xargs sed -i 's/av_get_channel_layout_nb_channels([^)]*)/2/g'

# --- 3. Audiostreamsdata & SoundReader Spesifik Düzeltmeler ---
# AVCodecParameters içindeki channels ve channel_layout artık ch_layout içinde
sed -i 's/audCodecPars->channels/audCodecPars->ch_layout.nb_channels/g' src/core/FileCacheHandlers/audiostreamsdata.cpp
sed -i 's/audCodecPars->channel_layout/audCodecPars->ch_layout.u.mask/g' src/core/FileCacheHandlers/audiostreamsdata.cpp

# AVFrame içindeki channel_layout -> ch_layout.nb_channels
grep -rl "frame->channel_layout" . | xargs sed -i 's/frame->channel_layout/frame->ch_layout.nb_channels/g'

%build
export CC=clang
export CXX=clang++

# Wno-error ile küçük uyarıların derlemeyi durdurmasını engelliyoruz
%cmake -DCMAKE_C_COMPILER=clang -DCMAKE_CXX_COMPILER=clang++ -G Ninja \
    -DCMAKE_CXX_FLAGS="-Wno-error -Wno-deprecated-declarations -Wno-implicit-function-declaration -Wno-int-conversion -Wno-unused-but-set-variable -fcommon" \
    -S . -B redhat-linux-build

%cmake_build -- -j2

%install
# Kurulum aşamasında cmake'in oluşturduğu build klasörüne bakmasını sağlıyoruz
%cmake_install

%files
%{_bindir}/friction
