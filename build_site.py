#!/usr/bin/env python3
"""
Izcalli.org — Phase 1 static prototype builder.
Writes 8 standalone HTML files that open by double-click (no server needed).
Content is the Phase-0 content map after John's red-line (2026-06-14).
Rerun: python3 build_site.py
"""
import os, datetime, json

OUT = os.path.dirname(os.path.abspath(__file__))

# --- Editable content (Decap CMS) -------------------------------------------
# These JSON files are what the Decap web editor reads and writes. Keeping the
# content here (instead of hardcoded below) is what lets a non-technical editor
# change the homepage and supporters wall through the /admin panel. Edit the
# JSON (or the admin panel), then this build regenerates the HTML.
def _load(name):
    with open(os.path.join(OUT, "content", name), encoding="utf-8") as f:
        return json.load(f)

HOME = _load("home.json")
SUPPORTERS = _load("supporters.json")["supporters"]

# --- Custom domain (GitHub Pages) -------------------------------------------
# When this site is cut over to its real domain, GitHub Pages needs a CNAME file
# in the published output naming the custom domain. Because build_site.py
# regenerates the site on every run, the CNAME must be emitted here or it would
# be wiped on the next rebuild. See the Domain Cutover Runbook (Phase 3/4).
#
# SAFETY GATE: keep this None until DNS is actually pointed at GitHub. Pushing a
# live CNAME early flips GitHub Pages onto the custom domain before DNS resolves,
# which breaks the preview URL and HTTPS. On cutover day, set:
#     CUSTOM_DOMAIN = "izcalli.org"
# then rebuild + push.
CUSTOM_DOMAIN = None  # e.g. "izcalli.org" at cutover

# nav: (slug, label)
NAV = [
    ("index", "Home"),
    ("about", "About"),
    ("programs", "Programs"),
    ("mural", "Mural"),
    ("mens-gathering", "Men's Gathering"),
    ("research", "Research"),
    ("get-involved", "Get Involved"),
    ("contact", "Contact"),
]

def header(active, home=False):
    links = "".join(
        f'<a href="{("index" if s=="index" else s)}.html"'
        f'{" class=\"active\"" if s==active else ""}>{l}</a>'
        for s, l in NAV
    )
    cls = "site-header home" if home else "site-header"
    return f"""<header class="{cls}"><div class="wrap">
  <a class="brand" href="index.html"><img src="assets/img/logo.png" alt="Izcalli"></a>
  <nav class="nav">{links}
    <a class="btn" href="donate.html">Donate</a>
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
    <span>&copy; %YEAR% Izcalli. A federally recognized 501(c)(3) since 2004 &middot; EIN 33-0971908</span>
  </div>
</div></footer>""".replace("%YEAR%", str(datetime.date.today().year))

def strip(*imgs, cls=""):
    """A row of real-moment photos placed under a program description.
    imgs: (filename, alt) tuples. cls: optional modifier (e.g. "natural"
    to show horizontal photos uncropped)."""
    cells = "".join(f'<img src="assets/img/{s}" alt="{a}">' for s, a in imgs)
    klass = "photo-strip" + (f" {cls}" if cls else "")
    return f'<div class="{klass}">{cells}</div>'

def gallery(*imgs):
    """A 3-up grid of photos (taller cells than a strip). Each item is
    (filename, alt) or (filename, alt, posclass); posclass anchors the
    crop, e.g. "top" keeps heads in tall/portrait photos."""
    cells = ""
    for item in imgs:
        s, a = item[0], item[1]
        pos = item[2] if len(item) > 2 else ""
        c = f' class="{pos}"' if pos else ""
        cells += f'<figure><img src="assets/img/{s}" alt="{a}"{c}></figure>'
    return f'<div class="gallery">{cells}</div>'

def funders():
    """Our Supporters wall. Each logo sits on its own card on a light section.
    Logos are kept in their original brand colors (never recolored). Most funder
    logos are full color and read on white cards; Prebys and Decolonizing Wealth
    ship only as reverse (white/cream) wordmarks built for dark backgrounds, so
    those two get a dark brand-ink card instead. The San Diego DA brand is a
    round gold seal with no horizontal lockup (confirmed: their site/reports use
    the seal plus typeset text), so its card pairs the seal with a name caption.
    kind: "" normal logo, "dark" reverse logo on ink card, "seal" seal+caption.
    Order: current funders first, then past supporters."""
    items = [(s["logo"], s["name"], s.get("style", "")) for s in SUPPORTERS]
    def cell(f, n, kind):
        # Decap stores newly uploaded logos as a full path (contains "/"); the
        # original entries are bare filenames living in assets/img/funders.
        src = f if "/" in f else f"assets/img/funders/{f}"
        cls = "funder-card"
        if kind == "dark":
            cls += " funder-card--dark"
        if kind == "seal":
            cls += " funder-card--seal"
            return (f'<div class="{cls}"><img src="{src}" alt="{n}">'
                    f'<span class="funder-name">{n}</span></div>')
        return f'<div class="{cls}"><img src="{src}" alt="{n}" title="{n}"></div>'
    cells = "".join(cell(f, n, kind) for f, n, kind in items)
    return f"""
<section class="section funders-section"><div class="wrap center">
  <h2>Our supporters</h2>
  <p class="muted" style="max-width:62ch;margin:0 auto">The foundations and public agencies whose grants make Izcalli's cultural-healing work possible.</p>
  <div class="funders">{cells}</div>
</div></section>"""

def page(slug, title, body, active=None, is_home=False):
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
{header(active, is_home)}
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
_stats_html = "".join(
    f'<div class="stat"><div class="num">{s["number"]}</div>'
    f'<div class="lbl">{s["label"]}</div></div>'
    for s in HOME["stats"]
)
home = f"""
<section class="hero">
  <img src="assets/img/hero-circle.jpg" alt="Community gathered around a fire at night">
  <div class="overlay">
    <h1>{HOME["hero_heading"]}</h1>
    <p>{HOME["hero_intro"]}</p>
    <div class="cta-row">
      <a class="btn" href="programs.html">Our Programs</a>
      <a class="btn ghost" href="get-involved.html">Get Involved</a>
    </div>
  </div>
</section>

<section class="section">
  <div class="wrap center">
    <p class="lead" style="max-width:64ch;margin:0 auto">{HOME["mission_lead"]}</p>
  </div>
</section>

<section class="section alt">
  <div class="wrap">
    <div class="grid cols-3">
      <a class="card" href="programs.html#healing-circles"><img src="assets/img/healing-circle.jpg" alt="Indigenous healing circle"><div class="body"><h3>Healing circles</h3><p>Weekly Indigenous circles &mdash; C&iacute;rculo de Hombres and Cihua Ollin &mdash; in schools and community settings.</p></div></a>
      <a class="card" href="programs.html#restorative-theater"><img src="assets/img/restorative-theater.jpg" alt="Youth performing original theater at Chicano Park"><div class="body"><h3>Restorative theater</h3><p>Youth from Barrio Logan and Logan Heights create and perform original theater on the theme of freedom at the Chicano Park Museum.</p></div></a>
      <a class="card" href="programs.html#teatro"><img src="assets/img/teatro.jpg" alt="Teatro Izcalli performers"><div class="body"><h3>Teatro Izcalli</h3><p>A Chicana/o comedy troupe carrying the tradition of La Carpa and Teatro Campesino since 1995.</p></div></a>
      <a class="card" href="programs.html#tlahtolli"><img src="assets/img/training.jpg" alt="Tlahtolli training circle"><div class="body"><h3>Tlahtolli trainings</h3><p>Restorative rites-of-passage curriculum and trainings for educators and community leaders.</p></div></a>
      <a class="card" href="mens-gathering.html"><img src="assets/img/hero-circle.jpg" alt="Annual Men's Gathering fire"><div class="body"><h3>Men's Gathering</h3><p>An annual multi-generational gathering on Kumeyaay land, paired with Cihua Ollin.</p></div></a>
      <a class="card" href="mural.html"><img src="assets/img/mural-izcalli.jpg" alt="The Izcalli mural at Chicano Park"><div class="body"><h3>The Izcalli mural</h3><p>The mural at Chicano Park honors our mission.</p></div></a>
    </div>
  </div>
</section>

<section class="section impact">
  <div class="wrap">
    <div class="grid">
      {_stats_html}
    </div>
  </div>
</section>

<section class="section">
  <div class="wrap">
    <div class="calloutbox">
      <h2 style="margin-bottom:.2em">{HOME["event_title"]}</h2>
      <p class="lead">{HOME["event_dates"]}</p>
      <p><a class="btn" href="mens-gathering.html">{HOME["event_cta_label"]}</a></p>
    </div>
  </div>
</section>
"""
page("index", "Home", home + funders(), is_home=True)

# ----------------------------------------------------------------------------
# ABOUT / OUR APPROACH
# ----------------------------------------------------------------------------
about = """
<section class="pagehead"><div class="wrap">
  <h1>Izcalli: a house of reawakening for cultural consciousness and collective healing</h1>
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
    <h2>Board &amp; staff</h2>
    <h3 style="margin-top:18px">Executive leadership</h3>
    <div class="bios">
      <div class="bio">
        <h3>Macedonio Arteaga Jr.</h3>
        <p class="role">Co-Founder &amp; Executive Director</p>
        <p>Macedonio Arteaga Jr. is the architect of Izcalli's healing framework and the primary relationship holder with the school districts, county offices, and community networks that make its work possible. For 21 years he served as a Restorative Practices Pupil Advocate within the San Diego Unified School District's Department of Race, Human Relations and Advocacy, leading the district's restorative practices initiative, developing its first Chicana/o Studies course, and training staff district-wide in trauma-informed, culturally relevant instruction. He is a senior facilitator and National Trainer for the National Compadres Network, one of the most respected Latino-serving networks in the United States, through which he has trained practitioners across the country in Indigenous-rooted restorative practice. He is the 2024 Leader in Belonging Awardee (Prebys Foundation) and was honored by the City of San Diego, which proclaimed "Macedonio Arteaga Day" on February 27, 2007. As Executive Director, Mr. Arteaga provides the programmatic vision, community trust, and district-level access at the heart of Izcalli's work.</p>
      </div>
      <div class="bio">
        <h3>Alicia Chavez-Arteaga</h3>
        <p class="role">Co-Founder &amp; Director of Operations</p>
        <p>Alicia Chavez-Arteaga holds a Master of Arts in Women's Studies and a Bachelor of Science in Social Work, both from San Diego State University, and brings over 20 years of nonprofit administration experience to Izcalli's operations. As Director of Operations, she oversees compliance, financial systems, and program logistics. Earlier in her career she managed the wellness center at a San Diego high school, giving her firsthand operational knowledge of the school sites where Izcalli's circles are delivered. Her academic background in social work and gender equity ensures that Izcalli's programming is grounded in evidence-based frameworks and responsive to the specific needs of girls, non-binary youth, and others underserved by traditional mental health systems. As Director of Operations, Ms. Chavez-Arteaga is the organizational anchor ensuring Izcalli's work is executed with precision.</p>
      </div>
    </div>
    <h3 style="margin-top:28px">Board of directors</h3>
    <div class="bios">
      <div class="bio">
        <h3>Mirna Hernandez</h3>
        <p class="role">Board President</p>
        <p>Mirna Hernandez is an Assistant Principal within the Escondido Union High School District and holds a Master's degree in Educational Leadership from California State University San Marcos and a Bachelor's degree in Kinesiology with a minor in Chicana/o Studies from San Diego State University. With over two decades of experience in student achievement, curriculum design, and school administration, she has been a core Izcalli leader since the organization's early years, previously serving as Camp Director for the Izcalli Youth Leadership Camp. As Board President, Ms. Hernandez provides expert guidance on youth development and educational policy, and her active role within the regional school system gives Izcalli direct insight into how its school-embedded model can best serve students' social-emotional and mental health needs.</p>
      </div>
      <div class="bio">
        <h3>Viviana Ochoa, CPA</h3>
        <p class="role">Board Treasurer</p>
        <p>Viviana Ochoa is a high-level auditing and governance expert with over 25 years of experience in the public accounting and defense sectors. She currently manages the internal controls function for Science Applications International Corporation (SAIC), a $6B technology leader. Her background includes directing international audits for government and nonprofit organizations across Latin America, ensuring rigorous compliance and fiscal integrity in complex environments. A veteran of nonprofit leadership, Viviana has served in executive roles for the Mexican American National Association of San Diego and the Association of Latino Professionals For America. She recently completed three terms as a board member for the Metropolitan Area Advisory Committee on Anti-Poverty and currently serves on the audit committee for the ACLU of San Diego &amp; Imperial Counties. With an accounting degree from San Diego State University and a Board of Director Certificate from the University of San Diego, Viviana provides Izcalli with elite financial oversight.</p>
      </div>
      <div class="bio">
        <h3>Dr. Ryan Santos</h3>
        <p class="role">Board Secretary</p>
        <p>Dr. Ryan Santos is a veteran educational leader with over 20 years of experience dedicated to student advocacy and social justice in the San Diego region. Currently serving as Principal of Bayfront Charter High School in Chula Vista, Dr. Santos has played a pivotal role in the design and opening of innovative new middle and high school environments. A distinguished scholar-practitioner, he earned his Ph.D. in Education from Claremont Graduate University. His expertise in democratic schooling and restorative practices extends to higher education, where he has taught graduate-level courses at San Diego State University and the University of San Diego. As Secretary of the Izcalli Board, Dr. Santos helps ensure that Izcalli's Indigenous-rooted programs are academically rigorous, operationally sound, and strategically integrated into the educational systems serving today's youth.</p>
      </div>
      <div class="bio">
        <h3>Dr. Francisco Mendoza, M.D.</h3>
        <p class="role">Board Member</p>
        <p>Dr. Francisco Mendoza is the Lead Physician at AltaMed Medical and Dental Group &mdash; Santa Ana Main, one of the nation's largest Federally Qualified Health Centers. A Family Medicine specialist, his practice centers on health equity, mental health, and social justice. Dr. Mendoza's personal narrative, from navigating the United States as an undocumented immigrant to becoming a lead physician, aligns with Izcalli's mission of reclaiming one's story. He holds a bachelor's degree from UCLA and a medical degree from the UC Davis School of Medicine, followed by a residency at Harbor-UCLA Medical Center. A dedicated advocate for MiMentor and the Alliance in Mentorship, he works extensively to build professional pipelines for underrepresented students. As an Izcalli board member, Dr. Mendoza bridges clinical medicine and cultural wellness.</p>
      </div>
      <div class="bio">
        <h3>Victor Chavez Jr.</h3>
        <p class="role">Board Member</p>
        <p>Victor M. Chavez Jr. has nearly 30 years of experience in the nonprofit sector (EYE Counseling &amp; Crisis Services, YMCA of San Diego County) and higher education (San Diego Mesa College, UC San Diego, Cal State Fullerton, and Los Angeles City College). He holds a bachelor's degree in History (minor in Political Science) from UC San Diego and a Master's degree in Public Administration from the University of Washington. Victor is a graduate of the Chicano Federation of San Diego County's Leadership Training Institute (Class XV) and the Latino Academy of the William C. Vel&aacute;squez Institute.</p>
      </div>
    </div>
  </div>
</section>

<section class="section">
  <div class="wrap">
    <h2>Rehumanization through Indigeneity: reclaiming our sacred purpose and inherent worth</h2>
    <p class="lead" style="max-width:70ch">Izcalli heals intergenerational trauma and dehumanization &mdash; particularly among BIPOC youth &mdash; through a community-based, Indigenous-led model rooted in Maya-Nahua philosophy and a 7,000-year-old ma&iacute;z-based culture.</p>
    <h3 style="margin-top:26px">The 7,000-year-old story: restoring humanity through ma&iacute;z-based philosophies</h3>
    <div class="pillars">
      <div class="pillar"><h3>Holistic healing</h3><p>Connecting physical, mental, emotional, and spiritual with community and the sacred &mdash; inherent wholeness, not symptom-suppression.</p></div>
      <div class="pillar"><h3>Palabra (dialogue &amp; truth)</h3><p>Honest dialogue in safe, substance-free spaces.</p></div>
      <div class="pillar"><h3>Challenging toxic masculinity</h3><p>C&iacute;rculo de Hombres builds vulnerability, humility, and critical consciousness.</p></div>
      <div class="pillar"><h3>Disrupting the school-to-prison pipeline</h3><p>Addressing dropout, criminalization, and self-destruction.</p></div>
      <div class="pillar"><h3>Youth voice</h3><p>Youth write and perform their own stories and help run the organization.</p></div>
      <div class="pillar"><h3>Intergenerational by design</h3><p>Elders, parents, and youth share the same circle. Young people who grow up in Izcalli return as facilitators, mentors, and board members.</p></div>
      <div class="pillar"><h3>Elder-Youth epistemology &amp; the 7Rs</h3><p>Respect, reciprocity, relationship, responsibility, regeneration, resistance, resilience.</p></div>
    </div>
  </div>
</section>

<section class="section alt">
  <div class="wrap">
    <h2>Our story</h2>
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

<section class="section">
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
  </div>
</section>
"""
page("about", "About", about + funders())

# ----------------------------------------------------------------------------
# PROGRAMS
# ----------------------------------------------------------------------------
programs = """
<section class="pagehead"><div class="wrap">
  <h1>The power of palabra: reclaiming narratives to transform generations</h1>
  <p>Our programs meet youth and families where they are &mdash; in schools, on the land, and on stage.</p>
</div></section>

<section class="section"><div class="wrap">
  <blockquote class="pullquote feature">
    &ldquo;There is no other work being done in our community with the profound impact on men. For over 25 years, I have joyfully seen the lives of teens, young adults and grandfathers changed. Embracing culture and the arts, theatre specifically, Izcalli has provided humor and healing needed in our community.&rdquo;
    <cite>&mdash; California Assemblymember David Alvarez</cite>
  </blockquote>
</div></section>

<section class="section" id="healing-circles"><div class="wrap">
  <div class="split">
  <div>
    <h2>Weekly Indigenous healing circles</h2>
    <h3 class="tagline">Doing things with people, not to them: a restorative model for collective well-being</h3>
    <p>We hold weekly Indigenous healing circles, including C&iacute;rculo de Hombres for men. Facilitators lead them in schools and community settings, with field trips to the Manzanita reservation. The circles offer culturally responsive mental health support.</p>
    <p>Many of the people facilitating circles today first sat in them as young participants. Since the 1990s, youth who grow up in Izcalli's circles have come back to lead circles of their own &mdash; so those guiding each circle have walked the same path as the young people in front of them.</p>
  </div>
  <img src="assets/img/healing-circle.jpg" alt="A weekly healing circle">
  </div>
  """ + strip(
    ("circle-1.jpg", "A community healing circle gathered around a drum"),
    ("circle-2.jpg", "A small circle of young people with a facilitator"),
    ("circle-3.jpg", "Students in a classroom healing circle"),
    ("circle-4.jpg", "A community circle beneath a Day of the Dead banner"),
    ("circle-5.jpg", "A circle of young men with their elder facilitator on a university campus visit"),
  ) + """
</div></section>

<section class="section alt" id="tlahtolli"><div class="wrap">
  <div class="split">
  <img src="assets/img/training.jpg" alt="Tlahtolli training circle">
  <div>
    <h2>Tlahtolli &mdash; restorative rites of passage</h2>
    <p>Three-day trainings for community leaders, professors, school staff, teachers, and arts educators.</p>
  </div>
  </div>
  """ + strip(
    ("tlahtolli-1.jpg", "Participants at a Tlahtolli training working with Indigenous glyphs"),
    ("tlahtolli-2.jpg", "A Tlahtolli training cohort gathered with ceremonial items"),
    cls="natural",
  ) + """
  <div class="quote-pair">
    <blockquote class="pullquote">
      &ldquo;First of all, the entire training was very meaningful to me. Second, the part that I am walking away with the most is on building teacher capacity around the restorative lens and seeing kids as human. The changing mindsets piece is my goal for my school site this next academic year.&rdquo;
      <cite>&mdash; 2024 Tlahtolli Training Participant</cite>
    </blockquote>
    <blockquote class="pullquote">
      &ldquo;This program should be mandatory for any teacher to take as a part of their credentialing process. All teachers, admin, and teaching artists should take this course before they make their way into the classroom.&rdquo;
      <cite>&mdash; 2024 Tlahtolli Training Participant</cite>
    </blockquote>
  </div>
</div></section>

<section class="section" id="teatro"><div class="wrap">
  <div class="split">
  <div>
    <h2>Teatro Izcalli</h2>
    <p>A Chicana/o comedy troupe (since 1995) honoring La Carpa and Teatro Campesino.</p>
  </div>
  <img src="assets/img/teatro.jpg" alt="Teatro Izcalli">
  </div>
  """ + strip(
    ("teatro-1.jpg", "Teatro Izcalli performing on the Chicano Park backdrop"),
    ("teatro-2.jpg", "An outdoor Teatro Izcalli performance at Chicano Park"),
    ("teatro-3.jpg", "Teatro Izcalli rehearsing a scene"),
  ) + """
</div></section>

<section class="section alt" id="restorative-theater"><div class="wrap">
  <div class="split">
  <img src="assets/img/restorative-theater.jpg" alt="Youth performing original theater at Chicano Park">
  <div>
    <h2>Restorative theater &mdash; youth theater at Chicano Park</h2>
    <p>In partnership with the Chicano Park Museum and Cultural Center, Izcalli brings young people from Barrio Logan and Logan Heights together to create and perform original live theater on the theme of freedom. Guided by professional teaching artists using the Tlahtolli curriculum &mdash; Izcalli's evidence-based, culturally responsive framework &mdash; participants (ages 11&ndash;22) develop artistic voice, claim the stage, and speak their truth.</p>
  </div>
  </div>
  """ + strip(
    ("theater-1.jpg", "Youth performing original theater on stage"),
    ("theater-2.jpg", "The youth cast gathered in a circle backstage"),
    ("theater-3.jpg", "Young performers in costume with a teaching artist"),
    ("theater-4.jpg", "Youth preparing backstage before a performance"),
  ) + """
</div></section>

<section class="section" id="youth-leadership"><div class="wrap">
  <h2>Youth leadership</h2>
  <h3 class="tagline">Planting the seed of reawakening: cultivating identity and resilience from within</h3>
  <p>Youth shape program design, budgeting, fundraising, social media, and documentation, and grow into student leaders and facilitators across Izcalli's programs.</p>
  <p>A Youth Steering Committee formalizes the youth leadership process, giving young people a structured role in guiding Izcalli's direction. Many of the youth who grow up in the program go on to become circle facilitators, community and social-justice advocates, and members of Izcalli's board.</p>
  """ + strip(
    ("comm-youth-1.jpg", "A youth cohort with their certificates"),
    ("comm-youth-2.jpg", "Izcalli youth on a recent trip together"),
    ("comm-youth-3.jpg", "Youth leadership camp group photo"),
    ("comm-youth-4.jpg", "Youth leaders posing together outdoors"),
    ("comm-youth-6.jpg", "Youth with an Izcalli elder and mentor"),
  ) + """
</div></section>

<section class="section alt"><div class="wrap">
  <h2>Cultural events &amp; traditions</h2>
  <p class="lead" style="max-width:72ch">A non-commercialized annual Day of the Dead celebration, traditional instrument-making (Huehuetl, Teponaxtli), songs, storytelling, beadwork, woodcarving, regalia (Tilma), and inter-tribal ceremonies.</p>
  """ + gallery(
    ("comm-culture-1.jpg", "A community ceremony with danza at the cultural center"),
    ("comm-culture-2.jpg", "A drum circle at the cultural center"),
    ("comm-culture-3.jpg", "A youth group with a Day of the Dead altar"),
    ("comm-culture-4.jpg", "Children and a mentor making art together at a workshop", "top"),
    ("comm-culture-5.jpg", "A hands-on workshop at a community event"),
  ) + """
  <p class="muted" style="max-width:72ch;margin-top:34px">Families and youth working the soil together and gathering for multi-generational retreats on Kumeyaay land &mdash; growing food, building the temazcal, and ceremony at sunrise.</p>
  """ + gallery(
    ("comm-garden-1.jpg", "Children planting seedlings in a raised bed", "top"),
    ("comm-garden-2.jpg", "A father holding his child in the garden", "top"),
    ("comm-garden-3.jpg", "A youth and a mentor working at the garden bed", "top"),
    ("comm-garden-4.jpg", "Youth tending the garden beds together"),
    ("comm-garden-5.jpg", "A child planting a seedling in the soil"),
    ("comm-retreat-1.jpg", "An elder leading ceremony at sunrise on the land"),
    ("comm-retreat-2.jpg", "A father and son at the land retreat"),
    ("comm-retreat-3.jpg", "A mentor and youth at the land retreat", "top"),
    ("comm-retreat-4.jpg", "Generations walking together at the retreat"),
    ("comm-retreat-5.jpg", "Community members building the temazcal together"),
    ("comm-retreat-6.jpg", "Youth sharing a meal at the camp table"),
  ) + """
</div></section>
"""
page("programs", "Programs", programs)

# ----------------------------------------------------------------------------
# MURAL
# ----------------------------------------------------------------------------
mural = """
<section class="pagehead"><div class="wrap">
  <h1>Our name lives at Chicano Park</h1>
  <p>In the heart of Barrio Logan, Izcalli's mural was recently restored.</p>
</div></section>

<section class="section"><div class="wrap split">
  <div>
    <h2>Chicano Park</h2>
    <p>Beneath the San Diego&ndash;Coronado Bridge in Barrio Logan lies Chicano Park, one of the most significant sites of Chicano cultural and political history in the United States. In 1970, after years of displacement by freeway and bridge construction, the Barrio Logan community reclaimed the land beneath the bridge through direct action, occupying the site until the city agreed to dedicate it as a park.</p>
    <p>In the decades since, the park's towering concrete pylons have become canvases for the largest collection of outdoor murals in the country, depicting Mexican and Chicano history, Indigenous heritage, and the community's enduring struggle for justice. Today Chicano Park is recognized as a National Historic Landmark.</p>
  </div>
  <img src="assets/img/mural.jpg" alt="The Izcalli mural beneath the bridge at Chicano Park">
</div></section>

<section class="section alt"><div class="wrap">
  <h2>The Izcalli mural</h2>
  <p class="lead" style="max-width:74ch">Izcalli's mural is part of this living gallery, carrying the organization's name and its Maya-Nahua imagery into the cultural landscape of Barrio Logan. It stands where Izcalli's youth theater takes the stage and where the community gathers each year for Chicano Park Day, connecting Izcalli's cultural-healing work to the park's history of resistance and renewal.</p>
  <figure class="mural-pano">
    <img src="assets/img/mural-izcalli.jpg" alt="The full Izcalli mural beneath the San Diego&ndash;Coronado Bridge at Chicano Park, spelling out IZCALLI across the bridge support">
    <figcaption>Izcalli's mural beneath the San Diego&ndash;Coronado Bridge at Chicano Park.</figcaption>
  </figure>
</div></section>

<section class="section"><div class="wrap">
  <h2>The artists at work</h2>
  <p class="lead" style="max-width:74ch">Izcalli's mural is painted and renewed by community artists. These images capture the work in progress, high on the scaffolding beneath the bridge.</p>
  <div class="gallery">
    <figure><img src="assets/img/mural-art-1.jpg" alt="An artist painting the golden eagle of the Izcalli mural"></figure>
    <figure><img src="assets/img/mural-art-2.jpg" alt="An artist painting from the scaffold"></figure>
    <figure><img src="assets/img/mural-art-4.jpg" alt="An artist on the scaffold against the blue mural panels"></figure>
    <figure><img src="assets/img/mural-art-3.jpg" alt="The community artist crew in front of the finished mural"></figure>
  </div>
</div></section>
"""
page("mural", "The Izcalli Mural", mural)

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
  <h2>Multi-generational healing on Kumeyaay land</h2>
  <p class="lead" style="max-width:72ch">What began in 1998 with roughly 100 men has grown into a multi-generational gathering at the Manzanita Reservation, paired with Cihua Ollin, the "movement of women." Grandfathers, fathers, and sons sit in the same circle &mdash; the elders carry the songs and teachings, and the youngest learn by being there.</p>
  <p style="max-width:72ch">Hello relatives, we are excited to announce our 28th Annual C&iacute;rculo de Hombres Men's Gathering. The gathering is held at the Manzanita Reservation, on land belonging to the Elliot family. There are important changes to this year's gathering, so please take time to read the information below.</p>
  <figure class="mural-pano" style="margin-top:24px">
    <img src="assets/img/intergen-fire.jpg" alt="Three generations gathered around the fire at night during the Annual Men's Gathering on Kumeyaay land">
  </figure>
  <div class="note" style="margin-top:20px">We ask all participants to commit to the whole ceremony: we arrive before sundown on Friday evening and remain until Sunday at noon. Please know that this is a <strong>camping experience</strong>.</div>
  """ + strip(
    ("mens-2.jpg", "Men gathered around the fire at night to sing and pray"),
    ("mens-1.jpg", "A drum circle singing at the gathering"),
    ("mens-3.jpg", "A young child at the gathering on the land"),
    ("mens-4.jpg", "A ceremonial fire at the gathering"),
  ) + """
  <p style="margin-top:28px"><a class="btn" href="https://forms.gle/FjAdQnE8hETpf9pB9">Register here</a></p>
</div></section>

<section class="section alt"><div class="wrap">
  <h2>What to bring</h2>
  <div class="grid cols-2">
    <div>
      <h3>Camping items</h3>
      <ul>
        <li>Camping chair</li>
        <li>Camping tent</li>
        <li>Water bottle</li>
        <li>Sleeping bag or blankets</li>
        <li>Personal hygiene items (toothbrush, etc.)</li>
        <li>Clothing &mdash; consider a sweatshirt or jacket for the evening</li>
      </ul>
    </div>
    <div>
      <h3>For the sweat lodge ceremony</h3>
      <ul>
        <li>Shorts and a towel</li>
        <li>Sacred items for the community altar</li>
        <li>Small giveaways for fire-keepers, cooks, elders, and loved ones</li>
      </ul>
    </div>
  </div>
</div></section>

<section class="section"><div class="wrap">
  <h2>Directions from San Diego</h2>
  <ol style="max-width:72ch;line-height:1.7">
    <li>Get on the 8 East freeway.</li>
    <li>Take Exit 61 for Live Oak Springs.</li>
    <li>Turn RIGHT on Crestwood Rd. and continue onto Old HWY 80.</li>
    <li>Take a LEFT on Live Oak Trail (you will see the Live Oak Market on the right).</li>
    <li>Continue on Live Oak Trail; it will eventually turn into Manzanita Road.</li>
    <li>Stay on Manzanita Road for about 6 miles.</li>
    <li>Once the street turns into a dirt road, drive 50 yards forward.</li>
    <li>Take your first RIGHT (look for red flags posted on the front gate).</li>
    <li>Drive into the land about 500 yards, look for cars, and find a spot to park.</li>
  </ol>
  <div class="note" style="margin-top:20px"><strong>Important:</strong> there is no cell service on many parts of the reservation, including where the gathering takes place. In case of a family emergency, contact Sam Elliot at (619) 540-1005.</div>
</div></section>

<section class="section alt"><div class="wrap" style="max-width:820px">
  <h2>Words from our organizers</h2>
  <p>This is our 28th year!!! Even though 28 years may seem like a long time, we acknowledge that gathering to share palabra in c&iacute;rculo has been part of our sacred heritage since time immemorial. The Men's Gathering is an opportunity for male-identifying relatives to experience story, laughter, ceremony, and reflection through an intercambio of words, feelings, pain, joy, and spiritual energy.</p>
  <p>This tradition, handed down by ancestors, elders, grandparents, and families, is our way of cleansing from the false teachings and woundedness that have become part of our lives. We invite you to join us, and we look forward to sharing space together to continue these teachings for generations to come.</p>
  <p>The San Diego C&iacute;rculo de Hombres Men's Gathering is coordinated through Izcalli and the National Compadres Network. We hold immense gratitude for our Kumeyaay relatives and tribal communities who have allowed us to continue this sacred tradition on Kumeyaay land.</p>
  <p class="muted">&mdash; Izcalli</p>
  <p style="margin-top:24px"><a class="btn" href="https://forms.gle/FjAdQnE8hETpf9pB9">Register for the 28th Annual Men's Gathering</a></p>
</div></section>
"""
page("mens-gathering", "Annual Men's Gathering", mens)

# ----------------------------------------------------------------------------
# RESEARCH
# ----------------------------------------------------------------------------
research = """
<section class="pagehead"><div class="wrap">
  <h1>Our model, studied and published</h1>
  <p>Izcalli's healing-circle approach is the subject of independent academic research &mdash; evidence that cultural, community-led practice changes lives.</p>
</div></section>

<section class="section impact"><div class="wrap">
  <p class="kicker center">What the research found &middot; Caporale, 2020 &middot; n=50</p>
  <div class="grid">
    <div class="stat"><div class="num">94%</div><div class="lbl">of members reported profound personal transformation</div></div>
    <div class="stat"><div class="num">84%</div><div class="lbl">became more engaged in social justice</div></div>
    <div class="stat"><div class="num">16.74 yrs</div><div class="lbl">average participation in the Circle (range: 1&ndash;27 years)</div></div>
  </div>
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

<section class="section alt"><div class="wrap">
  <h2>"The Circle, Indigeneity, and Healing"</h2>
  <p class="lead" style="max-width:74ch">Before the peer-reviewed article, Dr. Juvenal Caporale documented Izcalli's C&iacute;rculo de Hombres in his 2020 Ph.D. dissertation, <em>The Circle, Indigeneity, and Healing: Rehumanizing Chicano, Mexican, and Indigenous Men.</em></p>
  <p style="max-width:74ch">Drawing on in-depth interviews with 50 longtime Circle members, the study examines how Chicano, Mexican, and Indigenous men use the healing circle to recover from street violence, incarceration, and self-destructive cycles &mdash; and to rehumanize themselves and their relationships. Its findings put numbers to what participants have always described: the Circle changes lives, and keeps them.</p>
</div></section>

<section class="section"><div class="wrap center">
  <p class="lead" style="max-width:64ch;margin:0 auto">Independent research affirms what our community has always known: when culture leads, healing follows.</p>
</div></section>
"""
page("research", "Research", research)

# ----------------------------------------------------------------------------
# GET INVOLVED
# ----------------------------------------------------------------------------
involved = """
<section class="pagehead"><div class="wrap">
  <h1>Bring Izcalli to your school or community</h1>
  <p>Three simple ways to start the conversation.</p>
</div></section>

<section class="section"><div class="wrap">
  <div class="grid cols-3">
    <div class="card"><img src="assets/img/training.jpg" alt="Tlahtolli training circle"><div class="body">
      <h3>Request a training</h3>
      <p>Learn about bringing a Tlahtolli rites-of-passage training, restorative circle, or storytelling and theater workshop to your school or organization.</p>
      <p style="margin-top:16px"><a class="btn" href="contact.html">Request more information</a></p>
    </div></div>
    <div class="card"><img src="assets/img/healing-circle.jpg" alt="Healing circle"><div class="body">
      <h3>Request a circle at your site</h3>
      <p>Ask about hosting a weekly C&iacute;rculo de Hombres or Cihua Ollin healing circle for the youth you serve.</p>
      <p style="margin-top:16px"><a class="btn" href="contact.html">Request information about a circle</a></p>
    </div></div>
    <div class="card"><img src="assets/img/restorative-theater.jpg" alt="Youth performing original theater at Chicano Park"><div class="body">
      <h3>Request a restorative theater program at your site</h3>
      <p>Bring Izcalli's youth restorative theater &mdash; original performance guided by the Tlahtolli curriculum &mdash; to the young people you serve.</p>
      <p style="margin-top:16px"><a class="btn" href="contact.html">Request information about a program</a></p>
    </div></div>
  </div>
</div></section>
"""
page("get-involved", "Get Involved", involved)

# ----------------------------------------------------------------------------
# DONATE (placeholder)
# ----------------------------------------------------------------------------
donate = """
<section class="pagehead"><div class="wrap">
  <h1>Support cultural healing in San Diego</h1>
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
  <h1>Reach out</h1>
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
"""
page("contact", "Contact", contact)

# Emit (or remove) the GitHub Pages CNAME file based on the safety gate above.
cname_path = os.path.join(OUT, "CNAME")
if CUSTOM_DOMAIN:
    with open(cname_path, "w") as f:
        f.write(CUSTOM_DOMAIN + "\n")
    print("wrote CNAME ->", CUSTOM_DOMAIN)
elif os.path.exists(cname_path):
    os.remove(cname_path)
    print("removed CNAME (CUSTOM_DOMAIN is off)")

print("\nDone. Open index.html in a browser.")
