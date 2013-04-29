all: ctt.1

clean:
	rm -f *.1

pub:
	git push --mirror
	git push --mirror github


%.1: %.text
	a2x -f manpage --no-xmllint -a encoding=UTF-8 $<
