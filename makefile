DOTFILES = $(basename $(wildcard *.dot))

all: $(addsuffix .png, $(DOTFILES)) $(addsuffix .jpg, $(DOTFILES)) $(addsuffix .pdf, $(DOTFILES))

%.png: %.dot
	dot "$<" -Tpng -o "$@"

%.jpg: %.dot
	dot "$<" -Tjpg -o "$@"

%.pdf: %.dot
	dot "$<" -Tpdf -o "$@"

clean: rm *.png *.pdf
