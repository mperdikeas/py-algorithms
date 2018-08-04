.PHONY: all clean

all:
	@echo -n 'testing select sort'; (python select-sort.py > /dev/null 2>&1 && echo " - success") || (echo " - failed" ; exit 1)
	@echo -n 'testing insert sort'; (python insert-sort.py > /dev/null 2>&1 && echo " - success") || (echo " - failed" ; exit 1)
	@echo -n 'testing bubble sort'; (python bubble-sort.py > /dev/null 2>&1 && echo " - success") || (echo " - failed" ; exit 1)
	@echo -n 'testing merge  sort'; (python  merge-sort.py > /dev/null 2>&1 && echo " - success") || (echo " - failed" ; exit 1)

clean:
	rm -fr *.pyc
