const fs = require("fs");
const {
  Document, Packer, Paragraph, TextRun, AlignmentType, HeadingLevel,
  LevelFormat, BorderStyle, ExternalHyperlink, PageBreak
} = require("docx");

// ---- inline tag helpers ----------------------------------------------------
const GREEN = "1F7A3D", RED = "B23B16", GREY = "666666", MAROON = "6B2D1A";
function tag(text, color) {
  return new TextRun({ text, bold: true, size: 18, color, font: "Arial" });
}
function CONFIRMED() { return tag("  [CONFIRMED]", GREEN); }
function NEEDS()     { return tag("  [NEEDS JOHN]", RED); }
function SRC(t)      { return tag(`  [${t}]`, GREY); }

// body paragraph
function p(children, opts = {}) {
  return new Paragraph({ spacing: { after: 120 }, children: Array.isArray(children) ? children : [new TextRun({ text: children, size: 22 })], ...opts });
}
function run(text, opts = {}) { return new TextRun({ text, size: 22, ...opts }); }
function bullet(children) {
  return new Paragraph({ numbering: { reference: "b", level: 0 }, spacing: { after: 60 },
    children: Array.isArray(children) ? children : [new TextRun({ text: children, size: 22 })] });
}
// quoted/approved copy block (indented, italic, maroon left feel)
function quote(text) {
  return new Paragraph({
    indent: { left: 480 }, spacing: { after: 120, before: 60 },
    border: { left: { style: BorderStyle.SINGLE, size: 18, color: MAROON, space: 12 } },
    children: [new TextRun({ text, italics: true, size: 22 })]
  });
}
function h1(text) { return new Paragraph({ heading: HeadingLevel.HEADING_1, children: [new TextRun(text)] }); }
function h2(text) { return new Paragraph({ heading: HeadingLevel.HEADING_2, children: [new TextRun(text)] }); }
function spacer() { return new Paragraph({ children: [], spacing: { after: 80 } }); }

const children = [];

// ---- Title -----------------------------------------------------------------
children.push(new Paragraph({ alignment: AlignmentType.CENTER, spacing: { after: 60 },
  children: [new TextRun({ text: "Izcalli.org", bold: true, size: 48, color: MAROON, font: "Arial" })] }));
children.push(new Paragraph({ alignment: AlignmentType.CENTER, spacing: { after: 40 },
  children: [new TextRun({ text: "Website Content Map", size: 30, font: "Arial" })] }));
children.push(new Paragraph({ alignment: AlignmentType.CENTER, spacing: { after: 240 },
  children: [new TextRun({ text: "Phase 0 draft for John's review", italics: true, size: 22, color: GREY })] }));

children.push(p([run("This is the blueprint for the new site. Every block below is the "),
  run("actual proposed text", { bold: true }),
  run(" for each page, pulled from Izcalli's own documents. Please review and red-line BEFORE any design happens.")]));

children.push(h2("How to read the tags"));
children.push(bullet([tag("[CONFIRMED]", GREEN), run("  — pulled verbatim or near-verbatim from a vetted Izcalli document.")]));
children.push(bullet([tag("[NEEDS JOHN]", RED), run("  — a gap, a dated number to refresh, or a decision only you / Izcalli can make.")]));
children.push(bullet([tag("[source: x]", GREY), run("  — which Izcalli file the copy came from.")]));
children.push(p([run("Proposed sitemap: ", { bold: true }),
  run("Home · About / Our Approach · Programs · Annual Men's Gathering · Get Involved · Donate · Contact, plus an EN | ES language toggle.")]));

children.push(new Paragraph({ children: [new PageBreak()] }));

// ---- 0. Global -------------------------------------------------------------
children.push(h1("0. Global (every page)"));
children.push(bullet([run("Org name / logo: ", { bold: true }), run("Izcalli — “House of Re-awakening” (Nahuatl)."), CONFIRMED()]));
children.push(bullet([run("Tagline: ", { bold: true }), run("Chicana/o and Indigenous arts, education, and healing — San Diego, since 1993."), CONFIRMED()]));
children.push(bullet([run("Top nav: ", { bold: true }), run("Home · About · Programs · Men's Gathering · Get Involved · Donate · Contact + EN | ES toggle.")]));
children.push(bullet([run("Footer: ", { bold: true }), run("mission line, San Diego CA, izcalli.org, social icons, Donate button, 501(c)(3) note (federally recognized since 2004)."), NEEDS(), run(" which social handles?", { size: 22 })]));
children.push(bullet([run("Persistent Donate button in header.")]));

// ---- 1. Home ---------------------------------------------------------------
children.push(h1("1. Home"));
children.push(h2("Hero (your approved copy)"));
children.push(SRC_line("source: Website Edits.docx"));
children.push(quote("Izcalli is a San Diego nonprofit serving Chicana/o and Indigenous communities through cultural arts, education, and healing circles. For more than 30 years, we have worked alongside youth, families, and educators — building identity, belonging, and self-determination rooted in culture and history."));
children.push(p([CONFIRMED_inline(), run("   Hero image: pick a strong ceremony/gathering photo from the master set."), NEEDS()]));

children.push(h2("Mission strip"));
children.push(SRC_line("source: history page"));
children.push(quote("The mission of Izcalli is to transform the lives of Chicana/o and Indigenous communities by promoting cultural consciousness through the arts, education, and community dialogue."));
children.push(p([CONFIRMED_inline()]));

children.push(h2("“What we do” cards (link to Programs)"));
["Weekly Indigenous Healing Circles", "Teatro Izcalli (Chicana/o comedy troupe)",
 "Tlahtolli Rites of Passage & Trainings", "Annual Men's Gathering & Cihua Ollin"].forEach(t => children.push(bullet(t)));
children.push(p([SRC("source: program plan 2026")]));

children.push(h2("Impact band (quick numbers)"));
children.push(bullet([run("30+ years serving San Diego (since 1993)."), CONFIRMED()]));
children.push(bullet([run("~1,000 people engage with Izcalli each year."), SRC("source: program plan 2026")]));
children.push(bullet([run("Thousands of youth reached since founding."), NEEDS(), run(" replace with a current hard number if available.", { size: 22 })]));
children.push(p([run("Featured event: ", { bold: true }), run("rotating callout for the next Annual Men's Gathering (currently the entire homepage — demote to a card).")]));
children.push(p([run("Closing CTA: ", { bold: true }), run("Get Involved + Donate.")]));

// ---- 2. About --------------------------------------------------------------
children.push(h1("2. About / Our Approach"));
children.push(h2("About intro (your approved copy)"));
children.push(SRC_line("source: Website Edits.docx"));
children.push(quote("Izcalli is a San Diego-based nonprofit dedicated to transforming the lives of Chicana/o and Indigenous communities through cultural consciousness, the arts, education, and community dialogue."));
children.push(quote("Founded in 1993 by young Chicana/o activists, Izcalli began as the Escuelita, a Saturday school rooted in the belief that knowledge of Chicana/o and Indigenous culture is the foundation of identity, purpose, and self-determination. More than 30 years later, that founding conviction remains at the center of everything we do."));
children.push(p([CONFIRMED_inline()]));

children.push(h2("Our Approach (the funder-credibility centerpiece)"));
children.push(SRC_line("source: Decolonizing Wealth narrative"));
children.push(p("Izcalli heals intergenerational trauma and dehumanization — particularly among BIPOC youth — through a community-based, Indigenous-led model rooted in Maya-Nahua philosophy and a 7,000-year-old maíz-based culture. Pillars:"));
[["Holistic healing", "connecting physical, mental, emotional, and spiritual with community and the sacred; “inherent wholeness,” not symptom-suppression."],
 ["Palabra (dialogue & truth)", "honest dialogue in safe, substance-free spaces."],
 ["Challenging toxic masculinity", "Círculo de Hombres builds vulnerability, humility, and critical consciousness."],
 ["Disrupting the school-to-prison pipeline", "addressing dropout, criminalization, and self-destruction."],
 ["Youth voice", "youth write and perform their own stories and help run the organization."],
 ["Elder-Youth epistemology & the 7Rs", "respect, reciprocity, relationship, responsibility, regeneration, resistance, resilience."]
].forEach(([b, t]) => children.push(bullet([run(b + " — ", { bold: true }), run(t)])));
children.push(p([CONFIRMED_inline()]));

children.push(h2("Our Story (timeline)"));
children.push(p([run("Reuse the existing izcalli-history.html timeline (1993 → today), redesigned to match the new site. It is already well-written and factual, and it already uses the warm earth-tone palette we want."),
  CONFIRMED(), NEEDS(), run(" confirm all dated milestones are OK to publish.", { size: 22 })]));

children.push(h2("Recognition (selected)"));
children.push(p([run("KPBS Local Hero & Bank of America Local Hero (Macedonio Arteaga, 2005) · CA Arts Council Legacy Award (2021) · Prebys Foundation Leader in Belonging (2024) · CA State Senate Resolution honoring Teatro Izcalli (2016) · “Nopal Boy & Other Actos” published (2010), CA Association of Teachers of English Award of Merit."),
  CONFIRMED()]));
children.push(p([run("Board & Staff: ", { bold: true }), run("full bios are strong and ready — see section 8.")]));

// ---- 3. Programs -----------------------------------------------------------
children.push(h1("3. Programs"));
children.push(SRC_line("source: program plan 2026 + DWP narrative + history"));
[["Weekly Indigenous Healing Circles", "Círculo de Hombres and Cihua Ollin (Círculo de Mujeres). Weekly, facilitator-led circles in schools and community settings using the traditional Popoxcomitl, plus field trips to the Manzanita reservation. Culturally responsive mental health support, especially for male-identifying youth (ages 14–24)."],
 ["Tlahtolli — Restorative Rites of Passage Curriculum & Trainings", "3-day trainings (evidence-based curriculum by Dr. Stan Rodriguez) for community leaders, professors, school staff, teachers, and arts educators. Launched June 2024."],
 ["Teatro Izcalli", "Chicana/o comedy troupe (since 1995) honoring La Carpa and Teatro Campesino; multi-state tours (San Diego, El Centro, Modesto, Denver, Arizona State University), about 4,500 reached per touring year."],
 ["Youth Leadership & Steering Committee", "youth shape program design, budgeting, fundraising, social media, and documentation; a new Youth Steering Committee is forming."],
 ["Cultural events & traditions", "non-commercialized annual Day of the Dead celebration, traditional instrument-making (Huehuetl, Teponaxtli), songs, storytelling, beadwork, woodcarving, regalia (Tilma), inter-tribal ceremonies."]
].forEach(([b, t]) => children.push(bullet([run(b + " — ", { bold: true }), run(t)])));
children.push(p([CONFIRMED_inline(), NEEDS(), run(" the current /programs/ page is outdated — confirm this is the right public program set, and whether to name the SDUSD/school partnership here.", { size: 22 })]));

// ---- 4. Men's Gathering ----------------------------------------------------
children.push(h1("4. Annual Men's Gathering"));
children.push(SRC_line("source: history + program plan"));
children.push(bullet([run("Tradition since 1998; grew from ~100 men to a multi-generational gathering at Manzanita Reservation on Kumeyaay land."), CONFIRMED()]));
children.push(bullet([run("Grounded in the National Compadres Network tradition; honors elders (Maestro Jose Montoya, Jerry Tello, and others).")]));
children.push(bullet([run("Paired with Cihua Ollin (“movement of women”).")]));
children.push(bullet([run("Date, location, and registration for the next gathering (28th Annual per current site). Add a registration / RSVP CTA."), NEEDS()]));

// ---- 5. Get Involved -------------------------------------------------------
children.push(h1("5. Get Involved"));
children.push(SRC_line("source: program plan + narrative"));
["Join a circle (youth + adults)",
 "Attend an event (Men's Gathering, Day of the Dead, Teatro performances)",
 "Bring a training to your school/org (Tlahtolli, Restorative Circles, Storytelling/Theater)",
 "Volunteer / serve on the Youth Steering Committee or advisory board",
 "Donate (link to Donate page)"].forEach(t => children.push(bullet(t)));
children.push(p([NEEDS(), run(" confirm which calls-to-action Izcalli actually wants, plus the intake path for each (email signup? Teatro booking form? contact per item).", { size: 22 })]));

// ---- 6. Donate -------------------------------------------------------------
children.push(h1("6. Donate"));
children.push(bullet([run("Donation platform / link? (current processor, PayPal, Givebutter, Zeffy, etc.)"), NEEDS()]));
children.push(bullet([run("Short case-for-support paragraph (can draw from the About / Approach copy).")]));
children.push(bullet([run("501(c)(3) tax-deductibility note + EIN."), CONFIRMED(), run(" 501(c)(3) since 2004; ", { size: 22 }), tag("EIN [NEEDS JOHN]", RED)]));
children.push(bullet([run("Optional: monthly-giving and in-kind / volunteer alternatives.")]));

// ---- 7. Contact ------------------------------------------------------------
children.push(h1("7. Contact"));
children.push(SRC_line("source: recon — current contact page formatting is broken"));
children.push(bullet([run("Mailing address / service area (San Diego; City Heights & Diamond District neighborhoods named in programs)."), NEEDS()]));
children.push(bullet([run("General email + phone."), NEEDS()]));
children.push(bullet([run("Social links (YouTube confirmed; others?)."), NEEDS()]));
children.push(bullet([run("Simple contact form.")]));

// ---- 8. Board & Staff ------------------------------------------------------
children.push(h1("8. Board & Staff (lives under About)"));
children.push(SRC_line("source: Website/Izcalli Board and Staff.docx"));
children.push(p([CONFIRMED_inline(), run("   Full bios already written and strong.")]));
children.push(h2("Executive Leadership"));
children.push(bullet([run("Macedonio Arteaga Jr. — ", { bold: true }), run("Co-Founder & Executive Director. 21 years as Restorative Practices Pupil Advocate in SDUSD; National Trainer for the National Compadres Network; 2024 Prebys Leader in Belonging; “Macedonio Arteaga Day,” City of San Diego (Feb 27, 2007).")]));
children.push(bullet([run("Alicia Chavez-Arteaga — ", { bold: true }), run("Co-Founder & Director of Operations. MA Women's Studies, BS Social Work (SDSU); 20+ years nonprofit administration; leads compliance, finance, logistics, and the SDCOE/CYBHI partnership.")]));
children.push(h2("Board of Directors"));
[["Mirna Hernandez", "Board President (Assistant Principal, Escondido Union HSD)."],
 ["Viviana Ochoa, CPA", "Treasurer (internal controls, SAIC; 25+ yrs audit/governance)."],
 ["Dr. Ryan Santos", "Secretary (Principal, Bayfront Charter HS; Ph.D. Education)."],
 ["Dr. Francisco Mendoza, M.D.", "Member (Lead Physician, AltaMed)."],
 ["Victor Chavez Jr.", "Member (30 yrs nonprofit & higher ed)."]
].forEach(([b, t]) => children.push(bullet([run(b + " — ", { bold: true }), run(t)])));
children.push(p([NEEDS(), run(" headshots for board/staff? confirm bios are publication-ready and current.", { size: 22 })]));

// ---- Open questions --------------------------------------------------------
children.push(new Paragraph({ children: [new PageBreak()] }));
children.push(h1("Consolidated open questions for John"));
["Donate: which platform/link, and the EIN.",
 "Contact: address, email, phone, social handles (YouTube + others).",
 "Impact numbers: confirm/refresh the headline figures with a current hard number.",
 "Programs: confirm the program set is the right public list; name the SDUSD/school partnership publicly or not?",
 "Men's Gathering: next date / location / registration.",
 "Get Involved: which CTAs Izcalli actually wants + intake paths.",
 "Photos: pick a hero image + section photos from the master set.",
 "Spanish: who supplies/approves the ES translation (Izcalli staff vs. we draft and they verify)?",
 "Publication check: OK to publish all dated milestones and named elders/awards from the history timeline?"
].forEach(t => children.push(new Paragraph({ numbering: { reference: "n", level: 0 }, spacing: { after: 80 }, children: [new TextRun({ text: t, size: 22 })] })));

// helpers that need closures over TextRun
function SRC_line(t) { return new Paragraph({ spacing: { after: 60 }, children: [tag(`[${t}]`, GREY)] }); }
function CONFIRMED_inline() { return tag("[CONFIRMED]", GREEN); }

// ---- assemble --------------------------------------------------------------
const doc = new Document({
  styles: {
    default: { document: { run: { font: "Arial", size: 22 } } },
    paragraphStyles: [
      { id: "Heading1", name: "Heading 1", basedOn: "Normal", next: "Normal", quickFormat: true,
        run: { size: 30, bold: true, font: "Arial", color: MAROON },
        paragraph: { spacing: { before: 280, after: 140 }, outlineLevel: 0,
          border: { bottom: { style: BorderStyle.SINGLE, size: 8, color: "C4844A", space: 4 } } } },
      { id: "Heading2", name: "Heading 2", basedOn: "Normal", next: "Normal", quickFormat: true,
        run: { size: 24, bold: true, font: "Arial", color: "2C1F14" },
        paragraph: { spacing: { before: 160, after: 80 }, outlineLevel: 1 } },
    ]
  },
  numbering: {
    config: [
      { reference: "b", levels: [{ level: 0, format: LevelFormat.BULLET, text: "•", alignment: AlignmentType.LEFT, style: { paragraph: { indent: { left: 540, hanging: 280 } } } }] },
      { reference: "n", levels: [{ level: 0, format: LevelFormat.DECIMAL, text: "%1.", alignment: AlignmentType.LEFT, style: { paragraph: { indent: { left: 540, hanging: 280 } } } }] },
    ]
  },
  sections: [{
    properties: { page: { size: { width: 12240, height: 15840 }, margin: { top: 1440, right: 1440, bottom: 1440, left: 1440 } } },
    children
  }]
});

Packer.toBuffer(doc).then(buf => {
  fs.writeFileSync("Izcalli Website Content Map.docx", buf);
  console.log("wrote Izcalli Website Content Map.docx");
});
