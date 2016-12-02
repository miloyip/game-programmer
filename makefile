DOTFILES = $(basename $(wildcard *.dot))

all: $(addsuffix .jpg, $(DOTFILES)) $(addsuffix .svg, $(DOTFILES))

%.jpg: %.dot
	dot "$<" -Tjpg -o "$@"

%.svg: %.dot
	dot "$<" -Tsvg -o "$@"

clean: rm *.jpg *.svg
