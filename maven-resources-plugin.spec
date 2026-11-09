Name:		maven-resources-plugin
Version:	3.5.0
Release:	1
Summary:	Copies project resources to the output directory
Group:		Development/Java
License:	Apache-2.0
URL:		https://maven.apache.org/plugins/maven-resources-plugin/
Source0:	https://github.com/apache/maven-resources-plugin/archive/refs/tags/maven-resources-plugin-%{version}.tar.gz#/maven-resources-plugin-%{version}.tar.gz
# The tag has no license file. This copy is in git, so the build does not
# download it.
Source1:	LICENSE-2.0.txt
BuildArch:	noarch
BuildRequires:	python
BuildRequires:	maven
BuildRequires:	maven-components >= 3.10.0
BuildRequires:	java-current-devel
# Generates META-INF/maven/plugin.xml. The separate annotations package
# conflicts with maven-components on the same index file.
BuildRequires:	maven-plugin-tools
BuildRequires:	mvn(org.apache.maven.plugins:maven-plugin-plugin)
BuildRequires:	mvn(org.apache.maven.shared:maven-filtering)
BuildRequires:	maven-filtering >= 3.5.1
Requires:	maven-filtering >= 3.5.1
BuildRequires:	mvn(org.codehaus.plexus:plexus-utils)
BuildRequires:	plexus-utils >= 3.6.2
Requires:	plexus-utils >= 3.6.2
BuildRequires:	mvn(org.apache.maven:maven-plugin-api)
BuildRequires:	mvn(org.apache.maven:maven-core)
BuildRequires:	mvn(org.apache.maven:maven-model)
BuildRequires:	mvn(org.apache.maven.plugin-tools:maven-plugin-annotations)
BuildRequires:	mvn(javax.inject:javax.inject)
# javax.inject and jakarta-inject both provide this coordinate.
BuildRequires:	javax.inject >= 1-2
Requires:	javax.inject >= 1-2
BuildSystem:	maven
BuildOption(install):	--file-name %{name}

Obsoletes:	maven2-plugin-resources <= 0:2.0.8
Provides:	maven2-plugin-resources = %{EVRD}
Obsoletes:	maven-resources-plugin-javadoc < %{EVRD}

%description
Copies main and test resources into the build output, and filters them
through maven-filtering. 3.5.0 adds filename filtering and change
detection. 4.0.0 is still a beta, so this package stays on 3.5.0.
Tests need JUnit Jupiter, so they are not run.

%prep
%autosetup -n maven-resources-plugin-maven-resources-plugin-%{version}
rm -rf src/test src/it .github
cp -p %{SOURCE1} LICENSE
python - <<'PY'
import xml.etree.ElementTree as ET
NS = "http://maven.apache.org/POM/4.0.0"
ET.register_namespace("", NS)

def tag(name):
    return "{" + NS + "}" + name

def add(parent, name, text):
    node = ET.SubElement(parent, tag(name))
    node.text = text
    return node

root = ET.Element(tag("project"))
add(root, "modelVersion", "4.0.0")
add(root, "groupId", "org.apache.maven.plugins")
add(root, "artifactId", "maven-resources-plugin")
add(root, "version", "%{version}")
add(root, "packaging", "maven-plugin")
add(root, "name", "Apache Maven Resources Plugin")
props = ET.SubElement(root, tag("properties"))
add(props, "maven.compiler.release", "8")
add(props, "project.build.sourceEncoding", "UTF-8")
deps = ET.SubElement(root, tag("dependencies"))
items = (
    ("org.apache.maven.shared", "maven-filtering", "3.5.1", None),
    ("org.codehaus.plexus", "plexus-utils", "3.6.2", None),
    ("org.apache.maven", "maven-plugin-api", "3.10.0", "provided"),
    ("org.apache.maven", "maven-core", "3.10.0", "provided"),
    ("org.apache.maven", "maven-model", "3.10.0", "provided"),
    ("org.apache.maven.plugin-tools", "maven-plugin-annotations", "3.15.2", "provided"),
    ("javax.inject", "javax.inject", "1", "provided"),
)
for group, artifact, version, scope in items:
    dep = ET.SubElement(deps, tag("dependency"))
    add(dep, "groupId", group)
    add(dep, "artifactId", artifact)
    add(dep, "version", version)
    if scope:
        add(dep, "scope", scope)
build = ET.SubElement(root, tag("build"))
plugins = ET.SubElement(build, tag("plugins"))
plugin = ET.SubElement(plugins, tag("plugin"))
add(plugin, "groupId", "org.apache.maven.plugins")
add(plugin, "artifactId", "maven-plugin-plugin")
# The lifecycle binding asks for 3.15.1. The packaged plugin is 3.16.0.
add(plugin, "version", "3.16.0")
ET.ElementTree(root).write("pom.xml", encoding="utf-8", xml_declaration=True)
PY

%files -f .mfiles
%doc LICENSE README.md
