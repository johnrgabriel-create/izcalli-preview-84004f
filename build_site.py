#!/usr/bin/env python3
"""
Izcalli.org — Phase 1 static prototype builder.
Writes 8 standalone HTML files that open by double-click (no server needed).
Content is the Phase-0 content map after John's red-line (2026-06-14).
Rerun: python3 build_site.py
"""
import os, datetime

OUT = os.path.dirname(os.path.abspath(__file__))

# nav: (slug, label)
NAV = [
    ("index", "Home"),
    ("about", "About"),
    ("programs", "Programs"),
    ("mens-gathering", "Men's Gathering"),
    ("research", "Research"),
    ("get-involved", "Get Involved"),
    ("contact", "Contact"),
]

def header(active):
    links = "".join(
        f'<a href="{("index" if s=="index" else s)}.html"'
        f'{" class=\"active\"" if s==active else ""}>{l}</a>'
        for s, l in NAV
    )
    return f"""<header class="site-header"><div class="wrap">
  <a class="brand" href="index.html">IZCALLI<small>House of Re-awakening</small></a>
  <nav class="nav">{links}
    <a class="btn" href="donate.html">Donate</a>
    <span class="lang"><button class="on" type="button">EN</button><button type="button" onclick="esNote()">ES</button></span>
  </nav>
</div></header>"""

FOOTER = """<footer class="site-footer"><div class="wrap">
  <div class="grid">
    <div>
      <h4>Izcalli</h4>
      <p>Transforming the lives of Chicana/o and Indigenous communities by promoting cultural consciousness through the arts, education, and community dialogue. San Diego, since 1993.</p>
    </div>
    <div>
      <h4>Contact</h4>
      <p>PO Box 50208<br>San Diego, CA 92165-0208<br>
      <a href="mailto:info@izcalli.org">info@izcalli.org</a><br>(619) 857-1148</p>
    </div>
    <div>
      <h4>Connect</h4>
      <p><a href="https://www.instagram.com/teatroizcalli/">Instagram</a><br>
      <a href="https://www.youtube.com/@IzcalliOrg">YouTube</a><br>
      <a href="donate.html">Donate</a></p>
    </div>
  </div>
  <div class="bottom">
    <span>&copy; %YEAR% Izcalli. A federally recognized 501(c)(3) since 2004 &middot; EIN 33-0971908.</span>
    <span>Prototype &mdash; content under review.</span>
  </div>
</div></footer>
<script>function esNote(){alert("La versi\\u00f3n en espa\\u00f1ol est\\u00e1 en camino. The Spanish version of this site is coming soon.");}</script>""".replace("%YEAR%", str(datetime.date.today().year))

def page(slug, title, body, active=None):
    active = active or slug
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="robots" content="noindex, nofollow">
<title>{title} &middot; Izcalli</title>
<link rel="stylesheet" href="assets/style.css">
</head>
<body>
{header(active)}
{body}
{FOOTER}
</body>
</html>"""
    with open(os.path.join(OUT, f"{slug}.html"), "w") as f:
        f.write(html)
    print("wrote", slug + ".html")

# ----------------------------------------------------------------------------
# HOME
# ----------------------------------------------------------------------------
home = """
<section class="hero">
  <img src="assets/img/hero-circle.jpg" alt="Community gathered around a fire at night">
  <div class="overlay">
    <h1>Culture is healing.</h1>
    <p>Izcalli is a San Diego nonprofit serving Chicana/o and Indigenous communities through cultural arts, education, and healing circles &mdash; for more than 30 years.</p>
    <div class="cta-row">
      <a class="btn" href="programs.html">Our Programs</a>
      <a class="btn ghost" href="get-involved.html">Get Involved</a>
    </div>
  </div>
</section>

<section class="section">
  <div class="wrap center">
    <p class="kicker">Our Mission</p>
    <p class="lead" style="max-width:64ch;margin:0 auto">The mission of Izcalli is to transform the lives of Chicana/o and Indigenous communities by promoting cultural consciousness through the arts, education, and community dialogue.</p>
  </div>
</section>

<section class="section alt">
  <div class="wrap">
    <p class="kicker center">What We Do</p>
    <div class="grid cols-4">
      <div class="card"><img src="assets/img/healing-circle.jpg" alt="Indigenous healing circle"><div class="body"><h3>Healing Circles</h3><p>Weekly Indigenous circles &mdash; C&iacute;rculo de Hombres and Cihua Ollin &mdash; in schools and community settings.</p></div></div>
      <div class="card"><img src="assets/img/teatro.jpg" alt="Teatro Izcalli performers"><div class="body"><h3>Teatro Izcalli</h3><p>A Chicana/o comedy troupe carrying the tradition of La Carpa and Teatro Campesino since 1995.</p></div></div>
      <div class="card"><img src="assets/img/cihua-ollin.jpg" alt="Tlahtolli youth cohort"><div class="body"><h3>Tlahtolli</h3><p>Restorative rites-of-passage curriculum and trainings for educators and community leaders.</p></div></div>
      <div class="card"><img src="assets/img/hero-circle.jpg" alt="Annual Men's Gathering fire"><div class="body"><h3>Men's Gathering</h3><p>An annual multi-generational gathering on Kumeyaay land, paired with Cihua Ollin.</p></div></div>
    </div>
    <p class="center" style="margin-top:28px"><a class="btn" href="programs.html">See all programs</a></p>
  </div>
</section>

<section class="section impact">
  <div class="wrap">
    <div class="grid">
      <div class="stat"><div class="num">30+</div><div class="lbl">years serving San Diego, since 1993</div></div>
      <div class="stat"><div class="num">~1,000</div><div class="lbl">people engage with Izcalli each year</div></div>
      <div class="stat"><div class="num">5,700</div><div class="lbl">young people reached through our circles over 25 years</div></div>
    </div>
  </div>
</section>

<section class="section">
  <div class="wrap">
    <div class="calloutbox">
      <p class="kicker">Featured</p>
      <h2 style="margin-bottom:.2em">28th Annual Men's Gathering</h2>
      <p class="lead">July 31 &ndash; August 2, 2026 &middot; Manzanita Reservation, Kumeyaay land</p>
      <p><a class="btn" href="mens-gathering.html">Learn more &amp; register</a></p>
    </div>
  </div>
</section>
"""
page("index", "Home", home)

# ----------------------------------------------------------------------------
# ABOUT / OUR APPROACH
# ----------------------------------------------------------------------------
about = """
<section class="pagehead"><div class="wrap">
  <p class="kicker">About / Our Approach</p>
  <h1>Knowledge of culture is the foundation of identity.</h1>
  <p>Founded in 1993 by young Chicana/o activists, Izcalli began as the Escuelita &mdash; a Saturday school. More than 30 years later, that founding conviction remains at the center of everything we do.</p>
</div></section>

<section class="section">
  <div class="wrap split">
    <div>
      <h2>Who we are</h2>
      <p>Izcalli is a San Diego-based nonprofit dedicated to transforming the lives of Chicana/o and Indigenous communities through cultural consciousness, the arts, education, and community dialogue.</p>
      <p>Founded in 1993 by young Chicana/o activists, Izcalli began as the Escuelita, a Saturday school rooted in the belief that knowledge of Chicana/o and Indigenous culture is the foundation of identity, purpose, and self-determination. More than 30 years later, that founding conviction remains at the center of everything we do.</p>
    </div>
    <img src="assets/img/approach-circle.jpg" alt="Macedonio Arteaga facilitating a community circle">
  </div>
</section>

<section class="section alt">
  <div class="wrap">
    <p class="kicker">Our Approach</p>
    <h2>An Indigenous-led model of healing</h2>
    <p class="lead" style="max-width:70ch">Izcalli heals intergenerational trauma and dehumanization &mdash; particularly among BIPOC youth &mdash; through a community-based, Indigenous-led model rooted in Maya-Nahua philosophy and a 7,000-year-old ma&iacute;z-based culture.</p>
    <div class="pillars">
      <div class="pillar"><h3>Holistic healing</h3><p>Connecting physical, mental, emotional, and spiritual with community and the sacred &mdash; inherent wholeness, not symptom-suppression.</p></div>
      <div class="pillar"><h3>Palabra (dialogue &amp; truth)</h3><p>Honest dialogue in safe, substance-free spaces.</p></div>
      <div class="pillar"><h3>Challenging toxic masculinity</h3><p>C&iacute;rculo de Hombres builds vulnerability, humility, and critical consciousness.</p></div>
      <div class="pillar"><h3>Disrupting the school-to-prison pipeline</h3><p>Addressing dropout, criminalization, and self-destruction.</p></div>
      <div class="pillar"><h3>Youth voice</h3><p>Youth write and perform their own stories and help run the organization.</p></div>
      <div class="pillar"><h3>Elder-Youth epistemology &amp; the 7Rs</h3><p>Respect, reciprocity, relationship, responsibility, regeneration, resistance, resilience.</p></div>
    </div>
  </div>
</section>

<section class="section">
  <div class="wrap">
    <h2>Our Story</h2>
    <ul class="timeline">
      <li><span class="yr">1993</span> &mdash; Izcalli is founded as the Escuelita, a Saturday school by young Chicana/o activists.</li>
      <li><span class="yr">1995</span> &mdash; Teatro Izcalli, a Chicana/o comedy troupe, takes the stage.</li>
      <li><span class="yr">1998</span> &mdash; The first Annual Men's Gathering brings together roughly 100 men.</li>
      <li><span class="yr">2004</span> &mdash; Izcalli becomes a federally recognized 501(c)(3) nonprofit.</li>
      <li><span class="yr">2016</span> &mdash; California State Senate Resolution honors Teatro Izcalli.</li>
      <li><span class="yr">2021</span> &mdash; California Arts Council Legacy Award.</li>
      <li><span class="yr">2024</span> &mdash; Prebys Foundation Leader in Belonging; Tlahtolli trainings launch.</li>
      <li><span class="yr">Today</span> &mdash; ~1,000 community members each year, across circles, theater, and trainings.</li>
    </ul>
  </div>
</section>

<section class="section alt">
  <div class="wrap">
    <h2>Recognition</h2>
    <ul class="recog clean">
      <li>KPBS Local Hero &amp; Bank of America Local Hero (Macedonio Arteaga, 2005)</li>
      <li>California Arts Council Legacy Award (2021)</li>
      <li>Prebys Foundation Leader in Belonging (2024)</li>
      <li>California State Senate Resolution honoring Teatro Izcalli (2016)</li>
      <li>"Nopal Boy &amp; Other Actos" published (2010)</li>
      <li>California Association of Teachers of English Award of Merit</li>
    </ul>
    <p style="margin-top:24px"><a class="btn" href="contact.html">Meet our board &amp; staff</a></p>
  </div>
</section>
"""
page("about", "About", about)

# ----------------------------------------------------------------------------
# PROGRAMS
# ----------------------------------------------------------------------------
programs = """
<section class="pagehead"><div class="wrap">
  <p class="kicker">Programs</p>
  <h1>Culture, healing, and youth leadership.</h1>
  <p>Our programs meet youth and families where they are &mdash; in schools, on the land, and on stage.</p>
</div></section>

<section class="section"><div class="wrap split">
  <div>
    <h2>Weekly Indigenous Healing Circles</h2>
    <p>C&iacute;rculo de Hombres and Cihua Ollin (C&iacute;rculo de Mujeres). Weekly, facilitator-led circles in schools and community settings using the traditional Popoxcomitl, plus field trips to the Manzanita reservation. Culturally responsive mental health support, especially for male-identifying youth (ages 14&ndash;24).</p>
  </div>
  <img src="assets/img/healing-circle.jpg" alt="A weekly healing circle">
</div></section>

<section class="section alt"><div class="wrap split">
  <img src="assets/img/cihua-ollin.jpg" alt="Tlahtolli cohort">
  <div>
    <h2>Tlahtolli &mdash; Restorative Rites of Passage</h2>
    <p>Three-day trainings built on an evidence-based curriculum by Dr. Stan Rodriguez, for community leaders, professors, school staff, teachers, and arts educators. Launched June 2024.</p>
  </div>
</div></section>

<section class="section"><div class="wrap split">
  <div>
    <h2>Teatro Izcalli</h2>
    <p>A Chicana/o comedy troupe (since 1995) honoring La Carpa and Teatro Campesino, with multi-state tours &mdash; San Diego, El Centro, Modesto, Denver, and Arizona State University &mdash; reaching about 4,500 people per touring year.</p>
  </div>
  <img src="assets/img/teatro.jpg" alt="Teatro Izcalli">
</div></section>

<section class="section alt"><div class="wrap split">
  <img src="assets/img/youth.jpg" alt="Youth at a gathering">
  <div>
    <h2>Youth Leadership &amp; Steering Committee</h2>
    <p>Youth shape program design, budgeting, fundraising, social media, and documentation. A new Youth Steering Committee is forming.</p>
  </div>
</div></section>

<section class="section"><div class="wrap">
  <h2>Cultural events &amp; traditions</h2>
  <p class="lead" style="max-width:72ch">A non-commercialized annual Day of the Dead celebration, traditional instrument-making (Huehuetl, Teponaxtli), songs, storytelling, beadwork, woodcarving, regalia (Tilma), and inter-tribal ceremonies.</p>
</div></section>
"""
page("programs", "Programs", programs)

# ----------------------------------------------------------------------------
# MEN'S GATHERING
# ----------------------------------------------------------------------------
mens = """
<section class="hero" style="min-height:auto">
  <img src="assets/img/hero-circle.jpg" alt="Men gathered around the fire">
  <div class="overlay">
    <h1>28th Annual Men's Gathering</h1>
    <p>July 31 &ndash; August 2, 2026 &middot; Manzanita Reservation, Kumeyaay land</p>
    <div class="cta-row"><a class="btn" href="https://forms.gle/FjAdQnE8hETpf9pB9">Register here</a></div>
  </div>
</section>

<section class="section"><div class="wrap">
  <p class="kicker">A tradition since 1998</p>
  <h2>Multi-generational healing on Kumeyaay land</h2>
  <p class="lead" style="max-width:72ch">What began in 1998 with roughly 100 men has grown into a multi-generational gathering at the Manzanita Reservation. Grounded in the National Compadres Network tradition, it honors elders &mdash; Maestro Jos&eacute; Montoya, Jerry Tello, and others &mdash; and is paired with Cihua Ollin, the "movement of women."</p>
  <div class="note" style="margin-top:20px">This is a camping experience: full commitment from Friday evening through Sunday noon. Participants bring their own camping gear and supplies.</div>
  <p style="margin-top:28px"><a class="btn" href="https://forms.gle/FjAdQnE8hETpf9pB9">Register on the gathering form</a></p>
</div></section>
"""
page("mens-gathering", "Annual Men's Gathering", mens)

# ----------------------------------------------------------------------------
# RESEARCH
# ----------------------------------------------------------------------------
research = """
<section class="pagehead"><div class="wrap">
  <p class="kicker">Research &amp; Evidence</p>
  <h1>Our model, studied and published.</h1>
  <p>Izcalli's healing-circle approach is the subject of independent academic research &mdash; evidence that cultural, community-led practice changes lives.</p>
</div></section>

<section class="section"><div class="wrap split">
  <div>
    <h2>Peer-reviewed research on the C&iacute;rculo de Hombres</h2>
    <p>Scholar Juvenal Caporale (Department of Ethnic Studies, California State University, Stanislaus) has studied Izcalli's C&iacute;rculo de Hombres &mdash; first in his doctoral dissertation, and most recently in a peer-reviewed, open-access article.</p>
    <blockquote>"Preventing Gang Violence Through Healing Circles: The Case of the C&iacute;rculo de Hombres in San Diego"</blockquote>
    <p class="muted">Juvenal Caporale. <em>Social Sciences</em>, 2025, 14(11), 655. Open access.<br>
    DOI: <a href="https://doi.org/10.3390/socsci14110655">10.3390/socsci14110655</a></p>
    <p>The work examines how Chicano and Mexican men navigate street gangs, the criminal justice system, and self-destructive behaviors &mdash; and how the healing circle becomes a space to rehumanize and transform.</p>
    <p><a class="btn" href="https://doi.org/10.3390/socsci14110655">Read the article</a></p>
  </div>
  <img src="assets/img/approach-circle.jpg" alt="Izcalli healing circle in session">
</div></section>

<section class="section alt"><div class="wrap center">
  <p class="lead" style="max-width:64ch;margin:0 auto">Independent research affirms what our community has always known: when culture leads, healing follows.</p>
</div></section>
"""
page("research", "Research", research)

# ----------------------------------------------------------------------------
# GET INVOLVED
# ----------------------------------------------------------------------------
involved = """
<section class="pagehead"><div class="wrap">
  <p class="kicker">Get Involved</p>
  <h1>Bring Izcalli to your school or community.</h1>
  <p>Two simple ways to start the conversation.</p>
</div></section>

<section class="section"><div class="wrap">
  <div class="grid cols-2">
    <div class="card"><img src="assets/img/cihua-ollin.jpg" alt="Training cohort"><div class="body">
      <h3>Request a training</h3>
      <p>Learn about bringing a Tlahtolli rites-of-passage training, restorative circle, or storytelling and theater workshop to your school or organization.</p>
      <p style="margin-top:16px"><a class="btn" href="contact.html">Request more information</a></p>
    </div></div>
    <div class="card"><img src="assets/img/healing-circle.jpg" alt="Healing circle"><div class="body">
      <h3>Request a circle at your school or program</h3>
      <p>Ask about hosting a weekly C&iacute;rculo de Hombres or Cihua Ollin healing circle for the youth you serve.</p>
      <p style="margin-top:16px"><a class="btn" href="contact.html">Request information about a circle</a></p>
    </div></div>
  </div>
  <p class="center" style="margin-top:32px">You can also <a href="mens-gathering.html">attend the Annual Men's Gathering</a> or <a href="donate.html">support our work</a>.</p>
</div></section>
"""
page("get-involved", "Get Involved", involved)

# ----------------------------------------------------------------------------
# DONATE (placeholder)
# ----------------------------------------------------------------------------
donate = """
<section class="pagehead"><div class="wrap">
  <p class="kicker">Donate</p>
  <h1>Support cultural healing in San Diego.</h1>
</div></section>

<section class="section"><div class="wrap" style="max-width:760px">
  <p class="lead">Your gift sustains weekly healing circles, youth leadership, and the cultural traditions that have rooted our community for more than 30 years.</p>
  <div class="note" style="margin:28px 0">Online giving is coming soon. Our donation page is being set up &mdash; check back shortly, or <a href="contact.html">contact us</a> to give in the meantime.</div>
  <p class="muted">Izcalli is a federally recognized 501(c)(3) nonprofit (since 2004). EIN 33-0971908. Contributions are tax-deductible to the extent allowed by law.</p>
</div></section>
"""
page("donate", "Donate", donate, active="index")

# ----------------------------------------------------------------------------
# CONTACT (includes board & staff)
# ----------------------------------------------------------------------------
contact = """
<section class="pagehead"><div class="wrap">
  <p class="kicker">Contact</p>
  <h1>Reach out.</h1>
  <p>We'd love to hear from you &mdash; whether you're a young person, a family, an educator, or a partner.</p>
</div></section>

<section class="section"><div class="wrap split">
  <div>
    <h2>Get in touch</h2>
    <p><strong>Mailing address</strong><br>PO Box 50208<br>San Diego, CA 92165-0208</p>
    <p><strong>Email</strong><br><a href="mailto:info@izcalli.org">info@izcalli.org</a></p>
    <p><strong>Phone</strong><br>(619) 857-1148</p>
    <p><strong>Follow</strong><br><a href="https://www.instagram.com/teatroizcalli/">Instagram</a> &middot; <a href="https://www.youtube.com/@IzcalliOrg">YouTube</a></p>
  </div>
  <div class="calloutbox" style="text-align:left">
    <h3>Send us a message</h3>
    <p class="muted">A simple contact form will go here in the live site.</p>
    <p><label class="sans" style="font-size:.9rem">Name<br><input style="width:100%;padding:8px" disabled placeholder="Your name"></label></p>
    <p><label class="sans" style="font-size:.9rem">Email<br><input style="width:100%;padding:8px" disabled placeholder="you@email.com"></label></p>
    <p><label class="sans" style="font-size:.9rem">Message<br><textarea style="width:100%;padding:8px" rows="4" disabled placeholder="How can we help?"></textarea></label></p>
    <button class="btn" disabled>Send (prototype)</button>
  </div>
</div></section>

<section class="section alt"><div class="wrap">
  <p class="kicker">Our People</p>
  <h2>Board &amp; Staff</h2>
  <h3 style="margin-top:18px">Executive Leadership</h3>
  <ul class="clean">
    <li><strong>Macedonio Arteaga Jr.</strong> &mdash; Co-Founder &amp; Executive Director. 21 years as Restorative Practices Pupil Advocate in SDUSD; National Trainer for the National Compadres Network; 2024 Prebys Leader in Belonging.</li>
    <li><strong>Alicia Chavez-Arteaga</strong> &mdash; Co-Founder &amp; Director of Operations. MA Women's Studies, BS Social Work (SDSU); 20+ years nonprofit administration; leads compliance, finance, and logistics.</li>
  </ul>
  <h3 style="margin-top:24px">Board of Directors</h3>
  <ul class="clean">
    <li><strong>Mirna Hernandez</strong> &mdash; Board President (Assistant Principal, Escondido Union HSD).</li>
    <li><strong>Viviana Ochoa, CPA</strong> &mdash; Treasurer (internal controls, SAIC; 25+ yrs audit/governance).</li>
    <li><strong>Dr. Ryan Santos</strong> &mdash; Secretary (Principal, Bayfront Charter HS; Ph.D. Education).</li>
    <li><strong>Dr. Francisco Mendoza, M.D.</strong> &mdash; Member (Lead Physician, AltaMed).</li>
    <li><strong>Victor Chavez Jr.</strong> &mdash; Member (30 yrs nonprofit &amp; higher ed).</li>
  </ul>
</div></section>
"""
page("contact", "Contact", contact)

print("\nDone. Open index.html in a browser.")
