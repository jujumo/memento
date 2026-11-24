# Install the Claude Code skills of this directory by symlinking them into SKILLS_DIR.
# A skill is any sub-directory containing a SKILL.md.
SKILLS_DIR ?= $(HOME)/.claude/skills
SKILLS := $(patsubst %/SKILL.md,%,$(wildcard */SKILL.md))

.PHONY: install uninstall list

install:
	@mkdir -p "$(SKILLS_DIR)"
	@for s in $(SKILLS); do \
		ln -sfn "$(CURDIR)/$$s" "$(SKILLS_DIR)/$$s" && echo "linked  $$s -> $(SKILLS_DIR)/$$s"; \
	done

uninstall:
	@for s in $(SKILLS); do \
		t="$(SKILLS_DIR)/$$s"; \
		if [ -L "$$t" ] && [ "$$(readlink "$$t")" = "$(CURDIR)/$$s" ]; then \
			/bin/rm "$$t" && echo "removed $$t"; \
		fi; \
	done

list:
	@for s in $(SKILLS); do \
		t="$(SKILLS_DIR)/$$s"; \
		if [ -L "$$t" ] && [ "$$(readlink "$$t")" = "$(CURDIR)/$$s" ]; then st=linked; \
		elif [ -e "$$t" ]; then st="conflict (not ours)"; else st="not linked"; fi; \
		printf '%-24s %s\n' "$$s" "$$st"; \
	done
