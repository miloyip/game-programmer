DOTFILES = $(basename $(wildcard *.dot))

all: \
	$(addsuffix .png, $(DOTFILES)) \
	$(addsuffix .jpg, $(DOTFILES)) \
	$(addsuffix .svg, $(DOTFILES)) \
	$(addsuffix .pdf, $(DOTFILES))

%.png: %.dot
	dot "$<" -Tpng -o "$@"

%.jpg: %.dot
	dot "$<" -Tjpg -o "$@"

%.svg: %.dot
	dot "$<" -Tsvg -o "$@"

%.pdf: %.dot
	dot "$<" -Tpdf -o main.pdf -Tps2 -o main.ps2
	sh keeplinks.sh < main.ps2 > link.ps2
	ps2pdf link.ps2 link.pdf
	cpdf -stamp-on link.pdf main.pdf -o $@
	rm main.pdf main.ps2 link.ps2 link.pdf

clean: 
	rm -f *.jpg *.svg *.pdf *.png
