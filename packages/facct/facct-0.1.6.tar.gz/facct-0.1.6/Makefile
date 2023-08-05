py2=$(shell python2 -V 2>&1| sed  's+Python \(.*\)\.[0-9]+\1+')
py3=$(shell python3 -V 2>&1| sed  's+Python \(.*\)\.[0-9]+\1+')
user_install=~/.local
local_pip2_home=$(user_install)/lib/python$(py2)/site-packages
local_pip3_home=$(user_install)/lib/python$(py3)/site-packages
name=$(shell python setup.py --name)
version=$(shell python setup.py --version)
project_version_named=$(name)-$(version)

############################# PIP ##############################
local-pip-install:zip
	pip install  dist/$(project_version_named).tar.gz --user
local-pip3-install:zip3
	python3-pip install  dist/$(project_version_named).tar.gz --user
zip3:clean3
	python3 setup.py sdist
zip:clean
	python setup.py sdist
clean:
	rm -rf dist/ $(name).egg-info/ \
		$(local_pip2_home)/$(project_version_named)-py$(py2).egg-info \
		$(local_pip2_home)/$(name) $(user_install)/$(name)
clean3:
	rm -rf dist/ $(name).egg-info/ \
		$(local_pip3_home)/$(project_version_named)-py$(py3).egg-info \
		$(local_pip3_home)/$(name) $(user_install)/$(name)

uninstall:
	pip              uninstall $(name)   ;\
	python3-pip      uninstall $(name)   ;\
	sudo pip         uninstall $(name)   ;\
	sudo python3-pip uninstall $(name)

bench:
	mkdir -p tmp
	rm -f tmp/bench.ko tmp/bench.res
	./scripts/bench.sh > tmp/bench.res || touch tmp/bench.ko; touch tmp/bench.res
	if [ ! -z "$(grep \"\[KO\]\" tmp/bench.res)" ]; then \
		touch tmp/bench.ko; cat tmp/bench.res; \
	fi

register:bench
	if [ ! -f tmp/bench.ko ]; then               \
		echo "Registring....";                   \
		python setup.py register sdist upload;   \
	else                                         \
		echo "Registring aborted";               \
	fi



############################# RPM ##############################
rpm_name=python-$(name)
rpm_py3_name=python3-$(name)
release=1
rpm_version_named=$(rpm_name)-$(version)
rpm_version3_named=$(rpm_py3_name)-$(version)
rpm_v2=$(rpm_version_named)-$(release)
rpm_v3=$(rpm_version3_named)-$(release)
dist=$(shell uname -a | sed 's+.* .*-.*\.\(.*\)\..*+\1+')

py_files=$(shell find $(name) -type f -name "*.py")

check_spec_version:
	@if [ ! "`cat $(name).spec | grep '^Version: '| cut -d' ' -f2`" = "$(version)" ]; then \
		echo "Please update spec verion to $(version) with:\n" >&2; \
		echo -n "* `git log -n1 | grep '^Date:' | cut -d: -f2- | sed 's+ *\(.*\)+\1+'` -" ;\
			echo " `cat $(name).spec | grep '^*'| head -n1| cut -d- -f2` - $(version)-1" ;\
		git log --since="`cat $(name).spec | grep '^*'| sed 's+\* \([^-]*\) -.*+\1+'| head -n1`"  |\
			grep -vE "^commit|^Author:|^Date:|^Merge|^$$" >&2 ; \
		exit 2; \
	fi

bdist:dist/$(project_version_named).tar.gz
dist/$(project_version_named).tar.gz:$(name).spec $(py_files)
	rm -rf ~/rpm/SOURCES
	python setup.py bdist --formats=rpm
	
rpmbuild:dist/$(project_version_named).tar.gz
	mkdir -p dist && \
	cp $(name).spec dist/$(rpm_name).spec && \
	cp $(name).spec dist/$(rpm_py3_name).spec && \
	cd dist &&\
	mkdir -p ~/rpm/SOURCES ;\
	cp $(project_version_named).tar.gz ~/rpm/SOURCES/ &&\
	rpmbuild -v -ba --clean $(rpm_name).spec \

rpmlint:rpmbuild
	rpmlint $(HOME)/rpm/RPMS/noarch/$(rpm_v2).$(dist).noarch.rpm dist/$(rpm_name).spec
	rpmlint $(HOME)/rpm/SRPMS/$(rpm_v2).$(dist).src.rpm dist/$(rpm_name).spec
	rpmlint $(HOME)/rpm/RPMS/noarch/$(rpm_v3).$(dist).noarch.rpm dist/$(rpm_py3_name).spec
mock:rpmlint
	mock --verbose  $(HOME)/rpm/SRPMS/$(rpm_v2).$(dist).src.rpm
win_pkg:
	@if [ ! "`uname`" = "Linux" ]; then \
		python setup.py bdist --formats=wininst ;\
	else \
		echo "Not a windows platform, sorry." >&2 ;\
	fi
rpm_install:rpmbuild
	sudo rpm -ivh $(HOME)/rpm/RPMS/noarch/$(rpm_v2).$(dist).noarch.rpm
	@#sudo rpm -ivh dist/$(rpm_v2).$(dist).noarch.rpm
