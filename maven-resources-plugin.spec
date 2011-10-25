Name:           maven-resources-plugin
Version:        2.4.3
Release:        2
Summary:        Maven Resources Plugin

Group:          Development/Java
License:        ASL 2.0
URL:            http://maven.apache.org/plugins/maven-resources-plugin
#svn export http://svn.apache.org/repos/asf/maven/plugins/tags/maven-resources-plugin-2.4.3 maven-resources-plugin-2.4.3
#tar zcf maven-resources-plugin-2.4.3.tar.gz maven-resources-plugin-2.4.3/
Source0:        %{name}-%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildArch: noarch

BuildRequires: java-devel >= 0:1.6.0
BuildRequires: maven2
BuildRequires: maven2-plugin-plugin
BuildRequires: maven2-plugin-resources
BuildRequires: maven-jar-plugin
BuildRequires: maven-install-plugin
BuildRequires: maven-compiler-plugin
BuildRequires: maven-javadoc-plugin
BuildRequires: maven-surefire-maven-plugin
BuildRequires: maven-surefire-provider-junit
BuildRequires: maven-doxia-sitetools
BuildRequires: maven-plugin-testing-harness
BuildRequires: maven-shared-reporting-impl
BuildRequires: plexus-digest

Requires: maven-plugin-testing-harness
Requires: maven2
Requires:       jpackage-utils
Requires:       java
Requires(post):       jpackage-utils
Requires(postun):     jpackage-utils

Provides:       maven2-plugin-resources = %{version}-%{release}
Obsoletes:      maven2-plugin-resources <= 0:2.0.8

%description
The Resources Plugin handles the copying of project resources 
to the output directory.

%package javadoc
Group:          Development/Java
Summary:        Javadoc for %{name}
Requires:       jpackage-utils

%description javadoc
API documentation for %{name}.


%prep
%setup -q -n %{name}-%{version}

%build
export MAVEN_REPO_LOCAL=$(pwd)/.m2/repository
mvn-jpp \
        -e \
        -Dmaven2.jpp.mode=true \
        -Dmaven.repo.local=$MAVEN_REPO_LOCAL \
        -Dmaven.test.failure.ignore=true \
        install javadoc:javadoc

%install
rm -rf %{buildroot}

# jars
install -d -m 0755 %{buildroot}%{_javadir}
install -m 644 target/%{name}-%{version}.jar   %{buildroot}%{_javadir}/%{name}-%{version}.jar

(cd %{buildroot}%{_javadir} && for jar in *-%{version}*; \
    do ln -sf ${jar} `echo $jar| sed "s|-%{version}||g"`; done)

%add_to_maven_depmap org.apache.maven.plugins maven-resources-plugin %{version} JPP maven-resources-plugin

# poms
install -d -m 755 %{buildroot}%{_mavenpomdir}
install -pm 644 pom.xml \
    %{buildroot}%{_mavenpomdir}/JPP-%{name}.pom

# javadoc
install -d -m 0755 %{buildroot}%{_javadocdir}/%{name}-%{version}
cp -pr target/site/api*/* %{buildroot}%{_javadocdir}/%{name}-%{version}/
ln -s %{name}-%{version} %{buildroot}%{_javadocdir}/%{name}
rm -rf target/site/api*

%post
%update_maven_depmap

%postun
%update_maven_depmap

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%{_javadir}/*
%{_mavenpomdir}/*
%{_mavendepmapfragdir}/*

%files javadoc
%defattr(-,root,root,-)
%{_javadocdir}/%{name}-%{version}
%{_javadocdir}/%{name}

