const fs = require("fs");
const {
  Document, Packer, Paragraph, TextRun, Table, TableRow, TableCell,
  AlignmentType, LevelFormat, HeadingLevel, BorderStyle, WidthType,
  ShadingType, ExternalHyperlink, PageNumber, Header, Footer,
} = require("docx");

const NAVY = "1F3A5F";
const ACCENT = "2E75B6";
const GREY = "555555";

// ---- helpers ----------------------------------------------------------
const border = { style: BorderStyle.SINGLE, size: 1, color: "CCCCCC" };
const borders = { top: border, bottom: border, left: border, right: border };
const cellMargins = { top: 80, bottom: 80, left: 120, right: 120 };

function h1(text) {
  return new Paragraph({ heading: HeadingLevel.HEADING_1, children: [new TextRun(text)] });
}
function h2(text) {
  return new Paragraph({ heading: HeadingLevel.HEADING_2, children: [new TextRun(text)] });
}
function p(runs, opts = {}) {
  const children = Array.isArray(runs) ? runs : [new TextRun(runs)];
  return new Paragraph({ children, spacing: { after: 120 }, ...opts });
}
function bullet(runs, level = 0) {
  const children = Array.isArray(runs) ? runs : [new TextRun(runs)];
  return new Paragraph({ numbering: { reference: "bullets", level }, children, spacing: { after: 60 } });
}
function num(ref, runs) {
  const children = Array.isArray(runs) ? runs : [new TextRun(runs)];
  return new Paragraph({ numbering: { reference: ref, level: 0 }, children, spacing: { after: 80 } });
}
function who(tag) {
  return new TextRun({ text: tag + " ", bold: true, color: ACCENT });
}
function code(text) {
  return new TextRun({ text, font: "Consolas", size: 20, color: NAVY });
}

// table builder
function makeTable(rows, widths) {
  return new Table({
    width: { size: widths.reduce((a, b) => a + b, 0), type: WidthType.DXA },
    columnWidths: widths,
    rows: rows.map((cells, ri) =>
      new TableRow({
        children: cells.map((c, ci) =>
          new TableCell({
            borders,
            width: { size: widths[ci], type: WidthType.DXA },
            margins: cellMargins,
            shading: ri === 0 ? { fill: NAVY, type: ShadingType.CLEAR } : { fill: ci === 0 ? "EFF3F8" : "FFFFFF", type: ShadingType.CLEAR },
            children: [new Paragraph({
              children: [new TextRun({ text: c, bold: ri === 0, color: ri === 0 ? "FFFFFF" : "000000", size: 20 })],
            })],
          })
        ),
      })
    ),
  });
}

// ---- document ---------------------------------------------------------
const doc = new Document({
  creator: "Strategic Resource Specialist",
  title: "Izcalli Website Domain Cutover Runbook",
  styles: {
    default: { document: { run: { font: "Arial", size: 22 } } },
    paragraphStyles: [
      { id: "Heading1", name: "Heading 1", basedOn: "Normal", next: "Normal", quickFormat: true,
        run: { size: 30, bold: true, font: "Arial", color: NAVY },
        paragraph: { spacing: { before: 320, after: 160 }, outlineLevel: 0 } },
      { id: "Heading2", name: "Heading 2", basedOn: "Normal", next: "Normal", quickFormat: true,
        run: { size: 24, bold: true, font: "Arial", color: ACCENT },
        paragraph: { spacing: { before: 220, after: 100 }, outlineLevel: 1 } },
    ],
  },
  numbering: {
    config: [
      { reference: "bullets", levels: [
        { level: 0, format: LevelFormat.BULLET, text: "•", alignment: AlignmentType.LEFT,
          style: { paragraph: { indent: { left: 720, hanging: 360 } } } },
        { level: 1, format: LevelFormat.BULLET, text: "◦", alignment: AlignmentType.LEFT,
          style: { paragraph: { indent: { left: 1440, hanging: 360 } } } },
      ] },
      { reference: "need", levels: [{ level: 0, format: LevelFormat.DECIMAL, text: "%1.", alignment: AlignmentType.LEFT,
        style: { paragraph: { indent: { left: 540, hanging: 360 } } } }] },
      { reference: "p0", levels: [{ level: 0, format: LevelFormat.DECIMAL, text: "%1.", alignment: AlignmentType.LEFT,
        style: { paragraph: { indent: { left: 540, hanging: 360 } } } }] },
    ],
  },
  sections: [{
    properties: {
      page: {
        size: { width: 12240, height: 15840 },
        margin: { top: 1296, right: 1296, bottom: 1296, left: 1296 },
      },
    },
    footers: {
      default: new Footer({ children: [new Paragraph({
        alignment: AlignmentType.CENTER,
        children: [
          new TextRun({ text: "Izcalli Website Domain Cutover Runbook   |   Page ", size: 16, color: GREY }),
          new TextRun({ children: [PageNumber.CURRENT], size: 16, color: GREY }),
        ],
      })] }),
    },
    children: [
      // Title block
      new Paragraph({ spacing: { after: 40 }, children: [new TextRun({ text: "IZCALLI", bold: true, size: 44, color: NAVY })] }),
      new Paragraph({ spacing: { after: 60 }, children: [new TextRun({ text: "Website Domain Cutover Runbook", size: 30, color: ACCENT })] }),
      new Paragraph({ spacing: { after: 40 }, children: [new TextRun({ text: "Moving izcalli.org to the new site, without breaking email.", italics: true, color: GREY, size: 22 })] }),
      new Paragraph({ spacing: { after: 200 }, children: [
        new TextRun({ text: "Prepared: June 22, 2026", size: 18, color: GREY }),
        new TextRun({ text: "    •    Owner: John Gabriel    •    Live preview: ", size: 18, color: GREY }),
        new ExternalHyperlink({ children: [new TextRun({ text: "izcalli-preview-84004f", style: "Hyperlink", size: 18 })], link: "https://johnrgabriel-create.github.io/izcalli-preview-84004f/" }),
      ] }),
      new Paragraph({ border: { bottom: { style: BorderStyle.SINGLE, size: 8, color: ACCENT, space: 1 } }, spacing: { after: 160 }, children: [] }),

      // Mental model
      h1("1. How this works (30-second mental model)"),
      p("DNS is the phone book for your domain. When someone types izcalli.org, their computer looks up the phone book to find which server answers. Different services have separate entries:"),
      bullet([new TextRun({ text: "A record", bold: true }), new TextRun(" = the website lives at this address (an IP number).")]),
      bullet([new TextRun({ text: "MX record", bold: true }), new TextRun(" = email for this domain goes to this mail server.")]),
      bullet([new TextRun({ text: "TTL", bold: true }), new TextRun(" = how long the world caches an old entry before re-checking. A low TTL makes changes (and undo) take effect in minutes.")]),
      p([new TextRun("The whole cutover is just editing the website's "), new TextRun({ text: "A record", bold: true }), new TextRun(" to point at GitHub instead of HostGator, "), new TextRun({ text: "without disturbing the email (MX) entry.", bold: true })]),

      // Current setup
      h1("2. What izcalli.org looks like today (already verified)"),
      p("I inspected the live DNS directly, so most of what we would normally have to ask Izcalli is already known:"),
      makeTable([
        ["Item", "Current reality"],
        ["Registrar (owns the name)", "Webcentral / Netregistry (Australian). Renews 2031, so no lapse risk."],
        ["DNS host (where records are edited)", "HostGator (nameservers ns6071/ns6072.hostgator.com)"],
        ["Current website host", "HostGator shared hosting, IP 50.6.2.0"],
        ["Email host", "Also HostGator, same server (MX points to izcalli.org; SPF includes websitewelcome.com)"],
      ], [3000, 6360]),
      new Paragraph({ spacing: { before: 140, after: 120 }, shading: { fill: "FCEFD6", type: ShadingType.CLEAR }, border: { left: { style: BorderStyle.SINGLE, size: 18, color: "E0A100", space: 8 } }, children: [
        new TextRun({ text: "Critical risk: ", bold: true, color: "9A6A00" }),
        new TextRun({ text: "the website and email run on the SAME HostGator server, and the email (MX) record points at the domain itself. If we naively repoint izcalli.org to GitHub, email goes dark instantly. The fix is to give email its own address that stays on HostGator BEFORE moving the website (Phase 2). Once that is done, the website move cannot affect email.", color: "7A5400" }),
      ] }),
      p([new TextRun({ text: "Good news: ", bold: true }), new TextRun("because DNS is hosted at HostGator, you only need ONE login (HostGator) to do everything. The Australian registrar login is not needed for this cutover.")]),

      // What I need from Izcalli
      h1("3. What I need from Izcalli"),
      num("need", [new TextRun({ text: "HostGator account access. ", bold: true }), new TextRun("The keystone. It controls DNS, the website, and the email all at once. Ask: “the HostGator (cPanel) login, or add johnRgabriel@gmail.com as an authorized contact.”")]),
      num("need", [new TextRun({ text: "Full list of @izcalli.org email addresses in use ", bold: true }), new TextRun("(info@, serafin@, anything else) plus forwarders, so we protect every one. I can usually see these in cPanel once I have access; their confirmation is the safety check.")]),
      num("need", [new TextRun({ text: "Decision: keep email on HostGator, or move it later ", bold: true }), new TextRun("(e.g. Google Workspace). For this transition, “keep on HostGator” is simplest and safest. Moving email is a separate future project.")]),
      num("need", [new TextRun({ text: "Anything on the current site to preserve ", bold: true }), new TextRun("that is not already in the new site (old posts, a PDF, an event page). I back up the whole old site regardless.")]),
      num("need", [new TextRun({ text: "Two launch confirmations: ", bold: true }), new TextRun("(a) Spanish version live before public launch, or is English-first OK? (b) Is izcalli.org the primary address with www.izcalli.org redirecting to it (the standard choice)?")]),
      p([new TextRun({ text: "That is genuinely all. ", italics: true }), new TextRun({ text: "Registrar login and current-host details are already resolved.", italics: true })]),

      // Runbook
      h1("4. The transition runbook (step by step)"),
      p([new TextRun({ text: "Order matters: ", bold: true }), new TextRun("email is protected before the website is ever touched, and every change is fast to undo. Tags: "), who("(me)"), new TextRun("= I do it; "), who("(you)"), new TextRun("= you, in HostGator; "), who("(us)"), new TextRun("= together.")]),

      h2("Phase 0 — Prep and safety net"),
      num("p0", [who("(you)"), new TextRun("Get HostGator access. Confirm you can reach the "), new TextRun({ text: "DNS Zone Editor", bold: true }), new TextRun(" and the "), new TextRun({ text: "Email Accounts", bold: true }), new TextRun(" page in cPanel.")]),
      num("p0", [who("(me)"), new TextRun("Inventory the current site and email records exactly as they stand.")]),
      num("p0", [who("(us)"), new TextRun("Back up the old site: in cPanel use the Backup tool to download a full backup (or at least the public_html files). Our “nothing is lost” insurance.")]),
      num("p0", [who("(you)"), new TextRun("Lower the TTL on the A and MX records to 300 seconds, at least a day before cutover. This makes the switch and any rollback take effect in minutes. Wait ~24h for the old TTL to expire.")]),

      h2("Phase 1 — Verify the domain on GitHub (anti-takeover, recommended)"),
      num("p0", [who("(me)"), new TextRun("In the GitHub repo Settings → Pages, start “Verify domain.” GitHub provides a TXT record.")]),
      num("p0", [who("(you)"), new TextRun("Add that TXT record in the HostGator Zone Editor. "), who("(us)"), new TextRun("Confirm verification. Prevents anyone else from hijacking the domain on GitHub Pages.")]),

      h2("Phase 2 — Protect the email FIRST (before any website change)"),
      num("p0", [who("(you)"), new TextRun("In HostGator Zone Editor, create a new A record: name "), code("mail.izcalli.org"), new TextRun(", value "), code("50.6.2.0"), new TextRun(" (the current HostGator IP). Gives the mail server its own stable address.")]),
      num("p0", [who("(you)"), new TextRun("Change the MX record to point to "), code("mail.izcalli.org"), new TextRun(" instead of "), code("izcalli.org"), new TextRun(". Leave the SPF/TXT (websitewelcome.com) untouched.")]),
      num("p0", [who("(us)"), new TextRun("Verify email still works: "), code("dig MX izcalli.org"), new TextRun(" shows mail.izcalli.org, then send a test email TO and FROM an @izcalli.org address. "), new TextRun({ text: "Do not proceed until email is confirmed healthy.", bold: true })]),

      h2("Phase 3 — Prepare the GitHub side (no public impact yet)"),
      num("p0", [who("(me)"), new TextRun("Make build_site.py emit a "), code("CNAME"), new TextRun(" file containing izcalli.org into the built output, so it survives every rebuild. (Code change I handle.)")]),
      num("p0", [who("(me)"), new TextRun("Rebuild and push so the CNAME file is live in the repo.")]),
      num("p0", [who("(us)"), new TextRun("In repo Settings → Pages, set Custom domain = izcalli.org and Save.")]),

      h2("Phase 4 — Cut the website over (the actual switch)"),
      num("p0", [who("(you)"), new TextRun("In HostGator Zone Editor, edit the apex A record: remove the single 50.6.2.0 entry and add the four GitHub Pages A records:")]),
      p([code("185.199.108.153   185.199.109.153   185.199.110.153   185.199.111.153")], { indent: { left: 720 } }),
      p([new TextRun({ text: "Optional IPv6 (AAAA): ", size: 20, color: GREY }), code("2606:50c0:8000::153 / 8001::153 / 8002::153 / 8003::153")], { indent: { left: 720 } }),
      num("p0", [who("(you)"), new TextRun("Add a CNAME record: "), code("www"), new TextRun(" → "), code("johnrgabriel-create.github.io"), new TextRun(" (no repo name, no path). GitHub auto-redirects www to the apex.")]),
      num("p0", [who("(us)"), new TextRun("Verify: "), code("dig izcalli.org +noall +answer -t A"), new TextRun(" lists the four 185.199.x addresses. With the low TTL this appears within minutes.")]),

      h2("Phase 5 — HTTPS and public-launch hygiene"),
      num("p0", [who("(us)"), new TextRun("In Settings → Pages, wait for GitHub to issue the TLS certificate (up to 24h), then tick "), new TextRun({ text: "Enforce HTTPS", bold: true }), new TextRun(" so the padlock works and http redirects to https.")]),
      num("p0", [who("(me)"), new TextRun("At true public launch only: remove the noindex meta tag and the robots.txt Disallow in build_site.py so search engines can index the site; rebuild and push. Until you say “go public,” these stay in place.")]),
      num("p0", [who("(me)"), new TextRun("Optional polish: add a favicon and social-share (Open Graph) meta tags.")]),

      h2("Phase 6 — Final verification (sign-off checklist)"),
      bullet("https://izcalli.org loads the new site, padlock present, all 9 pages and images/logos load."),
      bullet("https://www.izcalli.org redirects to it."),
      bullet("Send and receive a test email one more time."),
      bullet("Check the site on a phone."),

      h2("Phase 7 — Decommission, carefully"),
      new Paragraph({ spacing: { before: 60, after: 120 }, shading: { fill: "FCE4E4", type: ShadingType.CLEAR }, border: { left: { style: BorderStyle.SINGLE, size: 18, color: "C0392B", space: 8 } }, children: [
        new TextRun({ text: "Do NOT cancel HostGator. ", bold: true, color: "8E2A1E" }),
        new TextRun({ text: "The email still lives there. The website is simply no longer served from it. Keep the HostGator plan active. (If email is later moved to Google Workspace, that is when HostGator could be dropped. Separate future step.)", color: "7A2419" }),
      ] }),

      h1("5. Rollback plan (if anything looks wrong at Phase 4)"),
      p("Revert the apex A record back to the single 50.6.2.0. The old site returns within minutes (low TTL). Email was never touched (protected in Phase 2), so it stays up throughout. This is why the order matters."),

      h1("6. Notes and options"),
      bullet([new TextRun({ text: "Optional upgrade — Cloudflare DNS: ", bold: true }), new TextRun("moving DNS management from HostGator to Cloudflare (free) gives faster propagation and a friendlier editor, and is a nicer long-term home for self-management. Needs the registrar login once to change nameservers. Not required.")]),
      bullet([new TextRun({ text: "build_site.py is the single source of truth: ", bold: true }), new TextRun("never hand-edit generated HTML; change the source and rebuild. assets/style.css is edited directly.")]),
      bullet([new TextRun({ text: "Confidence note: ", bold: true }), new TextRun("the GitHub IPs and steps were quoted from GitHub’s official docs, fetched June 22, 2026. GitHub occasionally changes these IPs, so I will re-verify against the docs on execution day.")]),
      p([new TextRun({ text: "Source: ", size: 18, color: GREY }), new ExternalHyperlink({ children: [new TextRun({ text: "GitHub Docs — Managing a custom domain for your GitHub Pages site", style: "Hyperlink", size: 18 })], link: "https://docs.github.com/en/pages/configuring-a-custom-domain-for-your-github-pages-site/managing-a-custom-domain-for-your-github-pages-site" })]),

      // Ownership / key custody
      h1("7. Ownership and key custody (the real long-term risk)"),
      p([new TextRun("The cutover itself is low-risk. The bigger concern is "), new TextRun({ text: "who holds the keys", bold: true }), new TextRun(". Today the whole stack sits on individual logins, not Izcalli-owned accounts:")]),
      bullet([new TextRun({ text: "The website repository ", bold: true }), new TextRun("lives on John's personal GitHub account (johnrgabriel-create), not an Izcalli-owned GitHub organization.")]),
      bullet([new TextRun({ text: "The registrar ", bold: true }), new TextRun("(Webcentral, Australian) and the HostGator DNS/email logins may not currently be in Izcalli's own hands.")]),
      new Paragraph({ spacing: { before: 60, after: 120 }, shading: { fill: "FCEFD6", type: ShadingType.CLEAR }, border: { left: { style: BorderStyle.SINGLE, size: 18, color: "E0A100", space: 8 } }, children: [
        new TextRun({ text: "Why it matters: ", bold: true, color: "9A6A00" }),
        new TextRun({ text: "if John steps away, Izcalli could be unable to control its own website or domain. The technology keeps running, but custody is fragile. This is a bigger risk than anything GitHub does.", color: "7A5400" }),
      ] }),
      p([new TextRun({ text: "Recommended (post-launch, low effort): ", bold: true }), new TextRun("(a) create an Izcalli-owned GitHub organization and transfer the repository into it; (b) make sure Izcalli has documented copies of the registrar and HostGator credentials in a place the org controls (a shared password manager or sealed document). None of this blocks the domain move; it just removes the single-person dependency afterward.")]),

      // Open items before "done"
      h1("8. Open items before public launch (not blockers for the domain move)"),
      p("The domain cutover can succeed on its own, but these static-site gaps should be settled before calling the site truly “done.” They are separate from the DNS work:"),
      bullet([new TextRun({ text: "Contact form backend. ", bold: true }), new TextRun("A static site cannot process form submissions on its own (there is no server). Options: a third-party form service (e.g. Formspree) that posts to an email, or a plain mailto:/phone contact block. "), new TextRun({ text: "Decision needed before launch.", italics: true })]),
      bullet([new TextRun({ text: "Donate button = link-out only. ", bold: true }), new TextRun("GitHub Pages terms forbid using it as an e-commerce host, but explicitly permit donation buttons and crowdfunding links. So the Donate button must "), new TextRun({ text: "link out", bold: true }), new TextRun(" to a processor (PayPal, Givebutter, etc.); a full on-site donation checkout is not allowed on Pages.")]),
      bullet([new TextRun({ text: "Spanish (EN/ES). ", bold: true }), new TextRun("Still an English-first stub. Izcalli named bilingual as a top requirement, so confirm whether English-first launch is acceptable or Spanish must ship first (this is also asked in section 3).")]),
      bullet([new TextRun({ text: "Headshots, favicon, social-share image. ", bold: true }), new TextRun("Final polish items for public launch.")]),
      new Paragraph({ spacing: { before: 60, after: 120 }, shading: { fill: "EFF3F8", type: ShadingType.CLEAR }, border: { left: { style: BorderStyle.SINGLE, size: 18, color: ACCENT, space: 8 } }, children: [
        new TextRun({ text: "GitHub Pages usage limits (for reference): ", bold: true, color: NAVY }),
        new TextRun({ text: "soft limits of 100 GB bandwidth/month, ~100k requests/month, and 1 GB published site size. An informational nonprofit site is nowhere near these. Source: GitHub Pages limits docs, fetched June 22, 2026.", color: "333333" }),
      ] }),
      p([new TextRun({ text: "Sources: ", size: 18, color: GREY }),
        new ExternalHyperlink({ children: [new TextRun({ text: "GitHub Pages limits", style: "Hyperlink", size: 18 })], link: "https://docs.github.com/en/pages/getting-started-with-github-pages/github-pages-limits" }),
        new TextRun({ text: "  •  ", size: 18, color: GREY }),
        new ExternalHyperlink({ children: [new TextRun({ text: "Securing your GitHub Pages site with HTTPS", style: "Hyperlink", size: 18 })], link: "https://docs.github.com/en/pages/configuring-a-custom-domain-for-your-github-pages-site/securing-your-github-pages-site-with-https" })]),
    ],
  }],
});

Packer.toBuffer(doc).then((buffer) => {
  const out = "/Users/pruegabriel/Projects/izcalli-website/Izcalli Website Domain Cutover Runbook.docx";
  fs.writeFileSync(out, buffer);
  console.log("WROTE", out);
});
