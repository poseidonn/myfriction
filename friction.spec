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
BuildRequires:  qt5-qtbase-devel
BuildRequires:  qt5-qtmultimedia-devel
BuildRequires:  qt5-qtsvg-devel
BuildRequires:  pkgconfig(libavcodec)
BuildRequires:  pkgconfig(libavformat)
BuildRequires:  pkgconfig(libswscale)
BuildRequires:  pkgconfig(libavutil)
BuildRequires:  mesa-libGL-devel
BuildRequires:  git

%description
Friction is a professional 2D motion graphics application.

%prep
# Mevcut dizini temizle (builddir/build/BUILD)
# rpkg tarafından oluşturulan geçici dosyaları silmek için:
rm -rf %{_builddir}/*
cd %{_builddir}

# Kodu doğrudan BUILD dizininin içine, alt klasör olmadan çekin (nokta işareti önemli)
git clone --recursive https://github.com/poseidonn/myfriction.git .

%build
# Artık 'cd myfriction' yapmaya gerek yok, çünkü kod doğrudan kök dizinde
export CC=clang
export CXX=clang++

# Fedora'nın standart cmake makrosunu kullanırken dizini belirtiyoruz
%cmake -DCMAKE_C_COMPILER=clang -DCMAKE_CXX_COMPILER=clang++ -S . -B redhat-linux-build
%cmake_build

%install
# Kurulum aşamasında cmake'in oluşturduğu build klasörüne bakmasını sağlıyoruz
%cmake_install

%files
%{_bindir}/friction
