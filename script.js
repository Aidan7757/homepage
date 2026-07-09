// Injects window.CONFIG (from assets/config.js) into the page. Works from file:// — no server needed.

const el = (id) => document.getElementById(id);

// Build one <li>: bold title, then any number of detail lines, optional link.
function item({ title, details = [], link, linkText }) {
	const li = document.createElement("li");
	const strong = document.createElement("strong");
	strong.textContent = title;
	li.appendChild(strong);
	for (const line of details) {
		if (!line) continue;
		li.appendChild(document.createElement("br"));
		li.appendChild(document.createTextNode(line));
	}
	if (link) {
		li.appendChild(document.createElement("br"));
		const a = document.createElement("a");
		a.href = link;
		a.textContent = linkText || link;
		a.target = "_blank";
		a.rel = "noopener";
		li.appendChild(a);
	}
	return li;
}

// Org-based section: each org has a heading and one or more roles with bulleted lists.
function renderExperience(id, section) {
	const container = el(id);
	for (const org of Object.values(section || {})) {
		const h = document.createElement("h4");
		h.textContent = org.organization;
		container.appendChild(h);
		for (const role of org.roles || []) {
			const p = document.createElement("p");
			p.className = "role";
			p.innerHTML = `<strong>${role.title}</strong> <span class="dates">${role.dates}</span>`;
			container.appendChild(p);
			const desc = document.createElement("p");
			desc.className = "role-desc";
			desc.textContent = role.description;
			container.appendChild(desc);
		}
	}
}

function render(cfg) {
	if (cfg.aidan_image_file) el("photo").src = cfg.aidan_image_file;
	el("position").textContent = cfg.position.replace(/\s*-\s*$/, "");
	el("university").textContent = cfg.university;

	const mail = el("email");
	mail.href = `mailto:${cfg.email}`;
	mail.textContent = cfg.email;

	el("cv").href = cfg.cv_file;

	const scholar = el("scholar");
	if (cfg.scholar_url) {
		scholar.href = cfg.scholar_url;
	} else {
		scholar.previousSibling.remove(); // drop the " · " separator
		scholar.remove();
	}

	el("biography").textContent = cfg.biography;
	if (cfg.last_updated) el("last_updated").textContent = `Last updated ${cfg.last_updated}`;

	renderExperience("research_experience", cfg.research_experience);
	renderExperience("professional_experience", cfg.professional_experience);

	for (const p of Object.values(cfg.papers || {})) {
		el("papers").appendChild(item({
			title: p.name,
			details: [p.authors, [p.status, p.journal || p.conference].filter(Boolean).join(" — ")],
			link: p.link,
			linkText: "Read",
		}));
	}

	for (const p of Object.values(cfg.presentations || {})) {
		el("presentations").appendChild(item({
			title: p.presentation_name,
			details: [p.conference_name || p.location, p.date],
		}));
	}

	for (const a of Object.values(cfg.honors_awards || {})) {
		el("honors_awards").appendChild(item({
			title: a.name,
			details: [a.date, a.description],
		}));
	}
}

render(window.CONFIG);
