FILE_LIST = ./.installed_files.txt

.PHONY: pull push clean check install post-install uninstall

default: | pull clean check install post-install

install:
	@ ./setup.py install --record $(FILE_LIST)

uninstall:
	@ while read FILE; do echo "Removing: $$FILE"; rm "$$FILE"; done < $(FILE_LIST)

clean:
	@ rm -Rf ./build

check:
	@ find . -type f -name "*.py" -not -path "./build/*" -not -path "./termgr/dom.py" -exec pep8 --hang-closing {} \;

pull:
	@ git pull

push:
	@ git push

post-install:
	fixuwsgi termsetup termcheck termquery
