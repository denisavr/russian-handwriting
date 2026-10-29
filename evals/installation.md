# Installation and worked-example check — 2026-10-29

A fresh Git clone of the prepared release was installed into the user's Codex skills
directory under `russian-handwriting`. Its origin was set to the public repository.
No pre-existing skill folder was overwritten. Structural inventory and all ten helper
tests passed in the installed copy. The bundled skill-creator frontmatter validator
also passed in the development checkout (using an isolated validation dependency).

An independent fresh agent was asked to use the **installed** SKILL.md and actual
`strekoza-1880-letter.jpg`, read only the salutation, and report literal text, modern
form if needed, grounds, uncertainty, source and review status. It inspected the full
page, record and linked guidance; all required resources were accessible. The image
checksum matched. Result: «Милостивый Государь!», with separate lowercased modern
form, source, confirmed human review and appropriate evidence limits.

The answer explicitly said this applies an already reviewed reference and is **not**
a blind accuracy test. It did not infer the writer's identity from author attribution
or claim the rest of the letter verified. The five-line copybook passage was confirmed
by the maintainer after this smoke run; updating that record changes review metadata,
not reading instructions or executable helpers. Installed files are checked again
against the final release before completion.

This verifies installed resource access and the requested worked example. It does not
prove automatic discovery in an already-running agent session; reload the skill list
or start a fresh session if needed. No user documents were uploaded and no outside
recognition service was used.
