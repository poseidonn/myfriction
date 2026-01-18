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
# Mevcut dizini temizle ve kodu doğrudan git ile çek
cd ..
rm -rf myfriction
git clone --recursive https://github.com/poseidonn/myfriction.git myfriction
cd myfriction

# Alt modüllerin tam indiğinden emin ol
git submodule update --init --recursive

%build
cd myfriction
export CC=clang
export CXX=clang++
%cmake -DCMAKE_C_COMPILER=clang -DCMAKE_CXX_COMPILER=clang++
%cmake_build

%install
cd myfriction
%cmake_install

%files
%{_bindir}/friction
