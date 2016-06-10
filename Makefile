FILE_LIST = ./.installed_files.txt
ECHO = /bin/echo -e

install:
	@ ./setup.py install --record $(FILE_LIST)
	@ ./compile.sh files/termexec.py /usr/bin/termexec
	@ chown termgr.termgr /usr/bin/termexec
	@ chmod +s /usr/bin/termexec

uninstall:
	@ while read FILE; do
		rm "${FILE}"
	done < ${FILE_LIST}

clean:
	@ rm -R ./build

check:
	@ find . -type f -name "*.py" -not -path "./build/*" -exec pep8 --hang-closing {} \;

pull:
	@ git pull

push:
	@ git push
