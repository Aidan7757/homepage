// Reads content.yaml and fills the empty scaffolding in the HTML.
// Home page uses only items marked `selected: true`; list pages show everything.

const esc = s => (s ?? "").toString()
	.replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;");

const set = (id, html) => { const el = document.getElementById(id); if (el) el.innerHTML = html; };
const attr = (id, name, val) => { const el = document.getElementById(id); if (el) el[name] = val; };
const selected = arr => arr.filter(x => x.selected);

const experience = groups => groups.map(g =>
	`<h4>${esc(g.org)}</h4>` + g.roles.map(r =>
		`<p class="role"><strong>${esc(r.role)}</strong> <span class="dates">${esc(r.dates)}</span></p>` +
		`<p class="role-desc">${esc(r.desc)}</p>`).join("")).join("");

const line = parts => {
	const [head, ...rest] = parts.filter(Boolean);
	return `<li><strong>${esc(head)}</strong>` + rest.map(x => `<br>${esc(x)}`).join("") + `</li>`;
};

const paperLi = p => `<li><strong>${esc(p.title)}</strong>` +
	[p.authors, p.venue].filter(Boolean).map(x => `<br>${esc(x)}`).join("") +
	(p.link ? `<br><a href="${esc(p.link)}" target="_blank" rel="noopener">Read</a>` : "") + `</li>`;

const talkLi = t => line([t.title, t.venue, t.date]);
const honorLi = (h, full) => line([h.title, h.date, full ? h.desc : null]);

const rows = (items, fn) => items.map(fn).join("");

async function main() {
	const d = jsyaml.load(await (await fetch("content.yaml")).text());
	const page = document.body.dataset.page;

	if (page === "home") {
		const p = d.profile;
		set("name", esc(p.name));
		set("position", esc(p.title));
		set("university", esc(p.university));
		attr("email", "textContent", p.email);
		attr("email", "href", `mailto:${p.email}`);
		set("biography", esc(p.bio));
		attr("cv", "href", p.cv);
		attr("scholar", "href", p.scholar);
		attr("photo", "src", p.photo);
		attr("photo", "alt", p.name);
		attr("photo", "title", p.name);
		set("photo_caption", esc(p.photo_caption));
		set("research_experience", experience(d.research));
		set("professional_experience", experience(d.professional));
		set("papers", rows(selected(d.papers), paperLi));
		set("presentations", rows(selected(d.presentations), talkLi));
		set("honors_awards", rows(selected(d.honors), h => honorLi(h, false)));
		set("last_updated", `Last updated ${esc(p.updated)}`);
	} else if (page === "papers") {
		set("papers", rows(d.papers, paperLi));
	} else if (page === "presentations") {
		set("presentations", rows(d.presentations, talkLi));
	} else if (page === "honors") {
		set("honors_awards", rows(d.honors, h => honorLi(h, true)));
	}
}

main();
