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
    ("mural", "Mural"),
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
    <span>&copy; %YEAR% Izcalli. A federally recognized 501(c)(3) since 2004 &middot; EIN 33-0971908.</span>
    <span>Prototype &mdash; content under review.</span>
  </div>
</div></footer>""".replace("%YEAR%", str(datetime.date.today().year))

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
    <div class="grid cols-3">
      <div class="card"><img src="assets/img/healing-circle.jpg" alt="Indigenous healing circle"><div class="body"><h3>Healing Circles</h3><p>Weekly Indigenous circles &mdash; C&iacute;rculo de Hombres and Cihua Ollin &mdash; in schools and community settings.</p></div></div>
      <div class="card"><a href="programs.html"><img src="assets/img/restorative-theater.jpg" alt="Youth performing original theater at Chicano Park"></a><div class="body"><h3>Restorative Theater</h3><p>Youth from Barrio Logan and Logan Heights create and perform original theater on the theme of freedom at the Chicano Park Museum.</p></div></div>
      <div class="card"><img src="assets/img/teatro.jpg" alt="Teatro Izcalli performers"><div class="body"><h3>Teatro Izcalli</h3><p>A Chicana/o comedy troupe carrying the tradition of La Carpa and Teatro Campesino since 1995.</p></div></div>
      <div class="card"><img src="assets/img/training.jpg" alt="Tlahtolli training circle"><div class="body"><h3>Tlahtolli</h3><p>Restorative rites-of-passage curriculum and trainings for educators and community leaders.</p></div></div>
      <div class="card"><img src="assets/img/hero-circle.jpg" alt="Annual Men's Gathering fire"><div class="body"><h3>Men's Gathering</h3><p>An annual multi-generational gathering on Kumeyaay land, paired with Cihua Ollin.</p></div></div>
      <div class="card"><a href="mural.html"><img src="assets/img/mural.jpg" alt="The Izcalli mural at Chicano Park"></a><div class="body"><h3>The Izcalli Mural</h3><p>Our mural at Chicano Park carries Izcalli's name and Maya-Nahua imagery into the heart of Barrio Logan.</p></div></div>
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
    <p class="kicker">Our People</p>
    <h2>Board &amp; Staff</h2>
    <h3 style="margin-top:18px">Executive Leadership</h3>
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
    <h3 style="margin-top:28px">Board of Directors</h3>
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

<section class="section alt">
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
  <img src="assets/img/restorative-theater.jpg" alt="Youth performing original theater at Chicano Park">
  <div>
    <h2>Restorative Theater &mdash; Youth Theater at Chicano Park</h2>
    <p>In partnership with the Chicano Park Museum and Cultural Center, Izcalli brings young people from Barrio Logan and Logan Heights together to create and perform original live theater on the theme of freedom. Guided by professional teaching artists using the Tlahtolli curriculum &mdash; Izcalli's evidence-based, culturally responsive Creative Youth Development framework &mdash; participants (ages 11&ndash;22) develop artistic voice, claim the stage, and speak their truth to thousands of community members.</p>
    <p>Culminating performances at Barrio Station and Chicano Park Day put youth in front of broad San Diego audiences, transforming the narrative of their neighborhoods from one of burden to one of resilience and self-determination. Returning participants step into student leadership, mentoring peers and running production.</p>
  </div>
</div></section>

<section class="section"><div class="wrap split">
  <img src="assets/img/youth.jpg" alt="Youth at a gathering">
  <div>
    <h2>Youth Leadership</h2>
    <p>Youth shape program design, budgeting, fundraising, social media, and documentation, and grow into student leaders and facilitators across Izcalli's programs.</p>
  </div>
</div></section>

<section class="section alt"><div class="wrap">
  <h2>Cultural events &amp; traditions</h2>
  <p class="lead" style="max-width:72ch">A non-commercialized annual Day of the Dead celebration, traditional instrument-making (Huehuetl, Teponaxtli), songs, storytelling, beadwork, woodcarving, regalia (Tilma), and inter-tribal ceremonies.</p>
</div></section>
"""
page("programs", "Programs", programs)

# ----------------------------------------------------------------------------
# MURAL
# ----------------------------------------------------------------------------
mural = """
<section class="pagehead"><div class="wrap">
  <p class="kicker">The Izcalli Mural</p>
  <h1>Our name lives at Chicano Park.</h1>
  <p>In the heart of Barrio Logan, Izcalli's mural takes its place among the most storied murals in the country.</p>
</div></section>

<section class="section"><div class="wrap split">
  <div>
    <h2>Chicano Park</h2>
    <p>Beneath the San Diego&ndash;Coronado Bridge in Barrio Logan lies Chicano Park, one of the most significant sites of Chicano cultural and political history in the United States. In 1970, after years of displacement by freeway and bridge construction, the Barrio Logan community reclaimed the land beneath the bridge through direct action, occupying the site until the city agreed to dedicate it as a park.</p>
    <p>In the decades since, the park's towering concrete pylons have become canvases for the largest collection of outdoor murals in the country, depicting Mexican and Chicano history, Indigenous heritage, and the community's enduring struggle for justice. Today Chicano Park is recognized as a National Historic Landmark.</p>
  </div>
  <img src="assets/img/mural-2.jpg" alt="Murals on the pylons of Chicano Park">
</div></section>

<section class="section alt"><div class="wrap">
  <h2>The Izcalli Mural</h2>
  <p class="lead" style="max-width:74ch">Izcalli's mural is part of this living gallery, carrying the organization's name and its Maya-Nahua imagery into the cultural landscape of Barrio Logan. It stands where Izcalli's youth theater takes the stage and where the community gathers each year for Chicano Park Day, connecting Izcalli's cultural-healing work to the park's history of resistance and renewal.</p>
  <div class="gallery">
    <figure><img src="assets/img/mural.jpg" alt="The Izcalli mural at Chicano Park during restoration"><figcaption>The Izcalli mural at Chicano Park, undergoing restoration.</figcaption></figure>
    <figure><img src="assets/img/mural-restoration.jpg" alt="Restoring the Izcalli mural"><figcaption>Community artists restoring the mural.</figcaption></figure>
    <figure><img src="assets/img/mural-2.jpg" alt="Murals at Chicano Park"><figcaption>Izcalli's mural among the murals of Chicano Park.</figcaption></figure>
  </div>
  <div class="note" style="margin-top:24px">We're adding the full history of the mural and the artists who created and restored it. Check back soon.</div>
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
  <p class="kicker">A tradition since 1998</p>
  <h2>Multi-generational healing on Kumeyaay land</h2>
  <p class="lead" style="max-width:72ch">What began in 1998 with roughly 100 men has grown into a multi-generational gathering at the Manzanita Reservation, paired with Cihua Ollin, the "movement of women."</p>
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

<section class="section alt"><div class="wrap">
  <p class="kicker">The doctoral study behind the model</p>
  <h2>"The Circle, Indigeneity, and Healing"</h2>
  <p class="lead" style="max-width:74ch">Before the peer-reviewed article, Dr. Juvenal Caporale documented Izcalli's C&iacute;rculo de Hombres in his 2020 Ph.D. dissertation, <em>The Circle, Indigeneity, and Healing: Rehumanizing Chicano, Mexican, and Indigenous Men.</em></p>
  <p style="max-width:74ch">Drawing on in-depth interviews with 50 longtime Circle members, the study examines how Chicano, Mexican, and Indigenous men use the healing circle to recover from street violence, incarceration, and self-destructive cycles &mdash; and to rehumanize themselves and their relationships. Its findings put numbers to what participants have always described: the Circle changes lives, and keeps them.</p>
</div></section>

<section class="section impact"><div class="wrap">
  <p class="kicker center">What the research found &middot; Caporale, 2020 &middot; n=50</p>
  <div class="grid">
    <div class="stat"><div class="num">94%</div><div class="lbl">of members reported profound personal transformation</div></div>
    <div class="stat"><div class="num">84%</div><div class="lbl">became more engaged in social justice</div></div>
    <div class="stat"><div class="num">16.74 yrs</div><div class="lbl">average participation in the Circle (range: 1&ndash;27 years)</div></div>
  </div>
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
  <p class="kicker">Get Involved</p>
  <h1>Bring Izcalli to your school or community.</h1>
  <p>Two simple ways to start the conversation.</p>
</div></section>

<section class="section"><div class="wrap">
  <div class="grid cols-2">
    <div class="card"><img src="assets/img/training.jpg" alt="Tlahtolli training circle"><div class="body">
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
"""
page("contact", "Contact", contact)

print("\nDone. Open index.html in a browser.")
