FILE_LIST = ./.installed_files.txt

.PHONY: pull push clean install uninstall bindings

default: | pull clean bindings install

install:
	@ ./setup.py install --record $(FILE_LIST)

uninstall:
	@ while read FILE; do echo "Removing: $$FILE"; rm "$$FILE"; done < $(FILE_LIST)

clean:
	@ rm -Rf ./build

pull:
	@ git pull

push:
	@ git push

bindings:
	@ pyxbgen -u doc/terminals.xsd --module-prefix=termgr -m dom
