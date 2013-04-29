webdir=~/www.nico.schottelius.org/software/

all: ctt.1

clean:
	rm -f *.1

pub:
	git push --mirror
	git push --mirror github

webpub:
	cp ctt.mdwn $(webdir)
	cd $(webdir) && git add ctt.mdwn && git commit -m "ctt update" ctt.mdwn ; git push


%.1: %.text
	a2x -f manpage --no-xmllint -a encoding=UTF-8 $<
