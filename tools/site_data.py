"""Content data for the generated service and location pages.

Edit this file to add a city/county or change page copy, then run
`python3 tools/build_pages.py` from the repo root.
"""

SITE = "https://mississippisealcoating.com"
QUOTE_URL = "https://dandzsealcoating.com/"
PHONE = "(662) 587-3525"
TEL = "+16625873525"
EMAIL = "dandzsealcoating@gmail.com"

# ---------------------------------------------------------------------------
# Core services (each gets its own page at /<slug>/)
# ---------------------------------------------------------------------------
SERVICES = [
    {
        "slug": "asphalt-sealcoating",
        "name": "Asphalt Sealcoating",
        "nav": "Sealcoating",
        "card": "Commercial-grade sealer applied in two coats to shield {place} asphalt from sun, rain, oil and oxidation &mdash; and restore that rich, jet-black finish.",
        "link_text": "Asphalt sealcoating",
    },
    {
        "slug": "asphalt-repair",
        "name": "Asphalt Repair",
        "nav": "Asphalt Repair",
        "card": "Hot-pour crack sealing, pothole patching and edge repair for driveways, parking lots and private roads around {place}.",
        "link_text": "Asphalt repair",
    },
    {
        "slug": "asphalt-driveways",
        "name": "Asphalt Driveways",
        "nav": "Driveways",
        "card": "Driveway sealcoating, crack filling and restoration that add curb appeal and years of life to {place} asphalt driveways.",
        "link_text": "Asphalt driveways",
    },
    {
        "slug": "parking-lot-sealing",
        "name": "Parking Lot Sealing",
        "nav": "Parking Lots",
        "card": "Parking lot sealcoating, crack repair and fresh line striping for {place} businesses, churches, schools and HOAs.",
        "link_text": "Parking lot sealing",
    },
]

# ---------------------------------------------------------------------------
# Regions (used to group counties and vary local copy)
# ---------------------------------------------------------------------------
REGIONS = {
    "home": {
        "name": "Northeast Hills &mdash; Our Home Base",
        "heading": "Hill-Country Asphalt Care",
        "text": "Northeast Mississippi's rolling hills mean long, sloped driveways and heavy runoff during spring storms. Water that finds its way into cracks washes out the base and turns into potholes and crumbling edges. Our crews work out of Ripley, so we're close by to inspect, repair and sealcoat on a schedule that works for you.",
    },
    "tupelo": {
        "name": "Tupelo &amp; Pontotoc Area",
        "heading": "Built for Busy Commercial Corridors",
        "text": "Retail, medical, church and industrial lots across the Tupelo area see thousands of vehicles a week. Turning tires, oil drips and summer heat break down unsealed asphalt quickly. Crack sealing plus a fresh sealcoat every two to three years keeps pavement safe, sharp and far cheaper to maintain than repaving.",
    },
    "oxford": {
        "name": "Oxford &amp; North-Central Mississippi",
        "heading": "Protecting High-Traffic Asphalt",
        "text": "Rental properties, apartment complexes, churches and businesses in this part of the state see big swings in traffic &mdash; from quiet summers to packed game weekends. We schedule around your calendar and use commercial-grade sealers so your pavement is back in service quickly.",
    },
    "desoto": {
        "name": "DeSoto County &amp; the Memphis Metro",
        "heading": "Keeping Up with Mid-South Growth",
        "text": "Rapid growth in Mississippi's Memphis-area suburbs means plenty of newer asphalt reaching the age for its first sealcoat (typically 6&ndash;12 months after paving), plus older lots that need crack repair and restriping. We handle subdivisions, HOAs, apartment communities and commercial centers.",
    },
}
REGION_ORDER = ["home", "tupelo", "oxford", "desoto"]

# ---------------------------------------------------------------------------
# Counties  (slug -> data).  `neighbors` are adjacent Mississippi counties.
# ---------------------------------------------------------------------------
COUNTIES = {
    "tippah": {
        "name": "Tippah", "region": "home", "seat": "Ripley",
        "towns": ["Ripley", "Walnut", "Falkner", "Blue Mountain", "Dumas", "Tiplersville"],
        "neighbors": ["benton", "union", "prentiss", "alcorn"],
        "blurb": "Tippah County is our home turf &mdash; D&amp;Z Sealcoating is headquartered in Ripley, the county seat. We've sealed, patched and striped asphalt in nearly every corner of the county, from Walnut and Falkner to Blue Mountain and Dumas.",
    },
    "alcorn": {
        "name": "Alcorn", "region": "home", "seat": "Corinth",
        "towns": ["Corinth", "Kossuth", "Rienzi", "Glen", "Farmington", "Biggersville"],
        "neighbors": ["tishomingo", "prentiss", "tippah"],
        "blurb": "Alcorn County sits on the Tennessee line in Mississippi's northeast corner, centered on Corinth and the busy US-45 / US-72 crossroads.",
    },
    "prentiss": {
        "name": "Prentiss", "region": "home", "seat": "Booneville",
        "towns": ["Booneville", "Baldwyn", "Marietta", "Wheeler", "New Site", "Jumpertown"],
        "neighbors": ["alcorn", "tishomingo", "itawamba", "lee", "union", "tippah"],
        "blurb": "Prentiss County runs along the US-45 corridor between Corinth and Tupelo, with Booneville at its center and small communities spread across rolling farmland.",
    },
    "pontotoc": {
        "name": "Pontotoc", "region": "tupelo", "seat": "Pontotoc",
        "towns": ["Pontotoc", "Ecru", "Sherman", "Thaxton", "Algoma", "Toccopola"],
        "neighbors": ["union", "lee", "chickasaw", "calhoun", "lafayette"],
        "blurb": "Pontotoc County links the Oxford and Tupelo areas along MS-6 and is crossed north to south by MS-15 and the Tanglefoot Trail.",
    },
    "lafayette": {
        "name": "Lafayette", "region": "oxford", "seat": "Oxford",
        "towns": ["Oxford", "Abbeville", "Taylor", "Harmontown", "Tula"],
        "neighbors": ["marshall", "union", "pontotoc", "calhoun", "yalobusha", "panola"],
        "blurb": "Lafayette County is anchored by Oxford and the University of Mississippi, with rural homes, farms and lake properties spread across the rest of the county.",
    },
    "lee": {
        "name": "Lee", "region": "tupelo", "seat": "Tupelo",
        "towns": ["Tupelo", "Saltillo", "Baldwyn", "Guntown", "Verona", "Shannon", "Plantersville", "Mooreville"],
        "neighbors": ["prentiss", "itawamba", "monroe", "chickasaw", "pontotoc", "union"],
        "blurb": "Lee County is Northeast Mississippi's commercial center, with Tupelo, Saltillo and Baldwyn strung along US-45 and I-22.",
    },
    "desoto": {
        "name": "DeSoto", "region": "desoto", "seat": "Hernando",
        "towns": ["Southaven", "Olive Branch", "Horn Lake", "Hernando", "Walls", "Nesbit", "Lake Cormorant"],
        "neighbors": ["tunica", "tate", "marshall"],
        "blurb": "DeSoto County is Mississippi's fast-growing gateway to Memphis, with Southaven, Olive Branch, Horn Lake and Hernando lining I-55, I-69 and I-22.",
    },
    "benton": {
        "name": "Benton", "region": "home", "seat": "Ashland",
        "towns": ["Ashland", "Hickory Flat", "Snow Lake Shores", "Michigan City"],
        "neighbors": ["marshall", "union", "tippah"],
        "blurb": "Benton County is a rural county between Tippah and Marshall counties, centered on Ashland and Hickory Flat &mdash; just a short drive from our Ripley shop.",
    },
    "union": {
        "name": "Union", "region": "home", "seat": "New Albany",
        "towns": ["New Albany", "Blue Springs", "Myrtle", "Ingomar"],
        "neighbors": ["benton", "tippah", "prentiss", "lee", "pontotoc", "lafayette", "marshall"],
        "blurb": "Union County, centered on New Albany along I-22, has grown alongside the Toyota plant at Blue Springs and a steady stream of new homes and businesses.",
    },
    "marshall": {
        "name": "Marshall", "region": "desoto", "seat": "Holly Springs",
        "towns": ["Holly Springs", "Byhalia", "Potts Camp", "Red Banks", "Waterford"],
        "neighbors": ["desoto", "tate", "panola", "lafayette", "union", "benton"],
        "blurb": "Marshall County stretches from historic Holly Springs to the edge of the Memphis metro, with I-22 / US-78 carrying growing industrial traffic.",
    },
    "tishomingo": {
        "name": "Tishomingo", "region": "home", "seat": "Iuka",
        "towns": ["Iuka", "Belmont", "Burnsville", "Tishomingo", "Golden", "Paden"],
        "neighbors": ["alcorn", "prentiss", "itawamba"],
        "blurb": "Tishomingo County, in Mississippi's far northeast corner, is lake country &mdash; Pickwick Lake, the Tenn-Tom Waterway and rolling hills around Iuka and Belmont.",
    },
    "itawamba": {
        "name": "Itawamba", "region": "tupelo", "seat": "Fulton",
        "towns": ["Fulton", "Mantachie", "Tremont", "Dorsey"],
        "neighbors": ["tishomingo", "prentiss", "lee", "monroe"],
        "blurb": "Itawamba County lies just east of Tupelo along I-22 and the Tenn-Tom Waterway, with Fulton as its county seat.",
    },
    "monroe": {
        "name": "Monroe", "region": "tupelo", "seat": "Aberdeen",
        "towns": ["Amory", "Aberdeen", "Hatley", "Smithville", "Hamilton"],
        "neighbors": ["itawamba", "lee", "chickasaw"],
        "blurb": "Monroe County lines the Tombigbee River, with Aberdeen as its county seat and Amory as its largest town.",
    },
    "chickasaw": {
        "name": "Chickasaw", "region": "tupelo", "seat": "Houston and Okolona",
        "towns": ["Houston", "Okolona", "Houlka", "Woodland", "Van Vleet"],
        "neighbors": ["pontotoc", "lee", "monroe", "calhoun"],
        "blurb": "Chickasaw County is one of the few Mississippi counties with two county seats &mdash; Houston and Okolona &mdash; and sits just south of Tupelo and Pontotoc.",
    },
    "calhoun": {
        "name": "Calhoun", "region": "oxford", "seat": "Pittsboro",
        "towns": ["Calhoun City", "Bruce", "Vardaman", "Pittsboro", "Derma"],
        "neighbors": ["lafayette", "pontotoc", "chickasaw", "yalobusha"],
        "blurb": "Calhoun County is a rural county south of Pontotoc and Lafayette counties, with Pittsboro as its seat and Calhoun City, Bruce and Vardaman as its main towns.",
    },
    "yalobusha": {
        "name": "Yalobusha", "region": "oxford", "seat": "Water Valley and Coffeeville",
        "towns": ["Water Valley", "Coffeeville", "Oakland", "Tillatoba"],
        "neighbors": ["panola", "lafayette", "calhoun"],
        "blurb": "Yalobusha County, just south of Oxford, has two county seats &mdash; Water Valley and Coffeeville &mdash; and a mix of small-town neighborhoods and rural homesteads.",
    },
    "panola": {
        "name": "Panola", "region": "oxford", "seat": "Batesville and Sardis",
        "towns": ["Batesville", "Sardis", "Como", "Crenshaw", "Pope", "Courtland"],
        "neighbors": ["tate", "marshall", "lafayette", "yalobusha"],
        "blurb": "Panola County spans I-55 south of Tate County, with county seats in Batesville and Sardis and busy highway-side businesses near the interstate.",
    },
    "tate": {
        "name": "Tate", "region": "desoto", "seat": "Senatobia",
        "towns": ["Senatobia", "Coldwater", "Independence", "Arkabutla"],
        "neighbors": ["desoto", "marshall", "panola", "tunica"],
        "blurb": "Tate County sits just south of DeSoto County along I-55, with Senatobia as its county seat and a growing number of Memphis-area commuters.",
    },
    "tunica": {
        "name": "Tunica", "region": "desoto", "seat": "Tunica",
        "towns": ["Tunica", "Tunica Resorts", "Robinsonville", "Dundee"],
        "neighbors": ["desoto", "tate"],
        "blurb": "Tunica County lies in the Mississippi Delta just southwest of DeSoto County and is home to the Tunica Resorts entertainment district.",
    },
}

# Order counties appear in on hub pages
COUNTY_ORDER = [
    "tippah", "alcorn", "prentiss", "benton", "union", "tishomingo",
    "lee", "pontotoc", "itawamba", "monroe", "chickasaw",
    "lafayette", "calhoun", "yalobusha", "panola",
    "desoto", "marshall", "tate", "tunica",
]

# ---------------------------------------------------------------------------
# Cities (slug -> data).  `featured` cities appear in the footer.
# ---------------------------------------------------------------------------
CITIES = {
    "ripley": {
        "name": "Ripley", "county": "tippah", "featured": True,
        "blurb": "Ripley is where D&amp;Z Sealcoating calls home. From homes off MS-15 and MS-4 to the businesses around the historic courthouse square, we've sealed, patched and striped more asphalt in Ripley than anywhere else &mdash; and because our crews are local, scheduling here is fast.",
    },
    "walnut": {
        "name": "Walnut", "county": "tippah",
        "blurb": "Walnut sits where US-72 meets MS-15 in northern Tippah County, just up the road from our Ripley shop. We handle driveways, church lots and business parking along the US-72 corridor.",
    },
    "corinth": {
        "name": "Corinth", "county": "alcorn", "featured": True,
        "blurb": "Corinth grew up where two railroads crossed, and today US-45 and US-72 still funnel steady traffic through town. From historic-district homes to retail, medical and industrial lots along the highway corridors, we keep Corinth asphalt sealed and safe.",
    },
    "booneville": {
        "name": "Booneville", "county": "prentiss", "featured": True,
        "blurb": "Booneville, the Prentiss County seat, sits right on US-45 and is home to Northeast Mississippi Community College. We serve homeowners, churches, schools and businesses from downtown Booneville out to the county line.",
    },
    "baldwyn": {
        "name": "Baldwyn", "county": "lee",
        "blurb": "Baldwyn straddles the Lee&ndash;Prentiss county line along US-45, near Brices Cross Roads National Battlefield Site. We seal and repair driveways and small-business lots throughout the Baldwyn area.",
    },
    "pontotoc": {
        "name": "Pontotoc", "county": "pontotoc", "featured": True,
        "blurb": "Pontotoc is a proud county seat where MS-15 meets MS-6, with the Tanglefoot Trail running right through town. We bring driveway sealcoating, asphalt repair and parking lot sealing to homes and businesses across Pontotoc.",
    },
    "oxford": {
        "name": "Oxford", "county": "lafayette", "featured": True,
        "blurb": "Oxford &mdash; home of the University of Mississippi and the famous Square &mdash; puts its pavement through more than most towns its size, from game-day crowds to year-round student housing and rental properties. We help Oxford homeowners, property managers and businesses keep asphalt looking sharp and lasting longer.",
    },
    "tupelo": {
        "name": "Tupelo", "county": "lee", "featured": True,
        "blurb": "Tupelo is the commercial hub of Northeast Mississippi, where US-45, I-22 and the Natchez Trace Parkway come together. Retail centers, medical offices, churches and neighborhoods across Tupelo count on well-kept asphalt &mdash; and that's what we deliver.",
    },
    "saltillo": {
        "name": "Saltillo", "county": "lee",
        "blurb": "Saltillo is one of Lee County's fastest-growing communities, just north of Tupelo along US-45. Many driveways in its newer subdivisions are reaching the age when they need a first or second sealcoat.",
    },
    "southaven": {
        "name": "Southaven", "county": "desoto", "featured": True,
        "blurb": "Southaven is one of Mississippi's largest cities, anchored by I-55, I-69 and the busy Goodman Road corridor. Its retail centers, apartment communities and subdivisions see heavy daily traffic that wears down unprotected asphalt fast.",
    },
    "olive-branch": {
        "name": "Olive Branch", "county": "desoto",
        "blurb": "Olive Branch has grown into a major DeSoto County hub for homes, distribution and light industry along Goodman Road and I-22 / US-78. We provide parking lot sealing, asphalt repair and driveway sealcoating throughout Olive Branch.",
    },
    "horn-lake": {
        "name": "Horn Lake", "county": "desoto",
        "blurb": "Horn Lake sits along I-55 and US-51 right on the Tennessee state line. Established neighborhoods and busy commercial lots here benefit from regular crack sealing and sealcoating to stay ahead of Mid-South weather.",
    },
    "hernando": {
        "name": "Hernando", "county": "desoto",
        "blurb": "Hernando is the DeSoto County seat, with a historic courthouse square and quick access to I-55. We serve Hernando homes, churches and downtown businesses with sealcoating, asphalt repair and line striping.",
    },
    "new-albany": {
        "name": "New Albany", "county": "union",
        "blurb": "New Albany, the Union County seat, sits on I-22 and marks the northern trailhead of the Tanglefoot Trail. Homes, churches and businesses across Union County rely on us for sealcoating and asphalt repair.",
    },
    "holly-springs": {
        "name": "Holly Springs", "county": "marshall",
        "blurb": "Holly Springs is known for its historic homes, Rust College and its spot along I-22 / US-78. From long residential driveways to commercial and church lots, we keep Marshall County asphalt protected.",
    },
    "byhalia": {
        "name": "Byhalia", "county": "marshall",
        "blurb": "Byhalia sits along I-22 in western Marshall County, with a growing base of distribution and industrial properties. We handle large-lot sealcoating, crack repair and striping as well as residential driveways.",
    },
    "iuka": {
        "name": "Iuka", "county": "tishomingo",
        "blurb": "Iuka, the Tishomingo County seat along US-72, is the gateway to Pickwick Lake. Lake homes, campgrounds and local businesses trust us to keep their asphalt sealed and smooth.",
    },
    "fulton": {
        "name": "Fulton", "county": "itawamba",
        "blurb": "Fulton is the Itawamba County seat, home to Itawamba Community College and located on I-22 near the Tenn-Tom Waterway. We serve Fulton-area driveways, schools, churches and business lots.",
    },
    "amory": {
        "name": "Amory", "county": "monroe",
        "blurb": "Amory is a railroad town in Monroe County with a tight-knit downtown and plenty of residential streets. We bring professional driveway sealcoating, asphalt repair and parking lot sealing to Amory property owners.",
    },
    "aberdeen": {
        "name": "Aberdeen", "county": "monroe",
        "blurb": "Aberdeen, the Monroe County seat on the Tombigbee River, is known for its historic homes and downtown. We help Aberdeen homeowners and businesses protect their asphalt from sun, rain and age.",
    },
    "houston": {
        "name": "Houston", "county": "chickasaw",
        "blurb": "Houston is a Chickasaw County seat at the southern end of the Tanglefoot Trail. We provide driveway sealing, crack and pothole repair, and parking lot maintenance throughout the Houston area.",
    },
    "okolona": {
        "name": "Okolona", "county": "chickasaw",
        "blurb": "Okolona is Chickasaw County's other county seat, located on the US-45 Alternate corridor. Our crews serve homes, farm drives and business lots across the Okolona area.",
    },
    "calhoun-city": {
        "name": "Calhoun City", "county": "calhoun",
        "blurb": "Calhoun City is one of Calhoun County's main towns, alongside Bruce, Vardaman and the county seat of Pittsboro. We serve driveways, churches and small-business lots across the county.",
    },
    "water-valley": {
        "name": "Water Valley", "county": "yalobusha",
        "blurb": "Water Valley is a historic railroad town in Yalobusha County, just south of Oxford along MS-7. Its revitalized downtown and neighborhoods count on us for sealcoating and asphalt repair.",
    },
    "batesville": {
        "name": "Batesville", "county": "panola",
        "blurb": "Batesville sits at the junction of I-55 and MS-6 in Panola County, with busy retail and restaurant lots near the interstate. We keep Batesville parking lots and driveways sealed, patched and striped.",
    },
    "senatobia": {
        "name": "Senatobia", "county": "tate",
        "blurb": "Senatobia, the Tate County seat on I-55, is home to Northwest Mississippi Community College. We serve Senatobia homes, churches and businesses with asphalt sealcoating and repair.",
    },
    "tunica": {
        "name": "Tunica", "county": "tunica",
        "blurb": "Tunica is the county seat of Tunica County along US-61, just south of the Tunica Resorts entertainment district. We handle commercial lot sealing and striping as well as residential driveways.",
    },
    "ashland": {
        "name": "Ashland", "county": "benton",
        "blurb": "Ashland is the Benton County seat, a small rural community just west of Tippah County. Long rural driveways and church and school lots here are right in our wheelhouse.",
    },
}

# Featured counties shown in the footer
FEATURED_COUNTIES = ["tippah", "alcorn", "prentiss", "pontotoc", "lafayette", "lee", "desoto"]

# Rotating project photos used on location pages (path, alt text)
PHOTOS = [
    ("/images/residential-driveway.webp", "Freshly sealcoated residential asphalt driveway"),
    ("/images/commercial-lot.webp", "Commercial parking lot after professional sealcoating"),
    ("/images/crack-sealing.webp", "Hot-pour crack sealing on an asphalt surface"),
    ("/images/line-striping.webp", "New parking lot line striping on sealed asphalt"),
    ("/images/commercial-property.webp", "Commercial property asphalt maintenance project"),
]
