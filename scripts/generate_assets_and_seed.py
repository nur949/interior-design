import sys
from pathlib import Path
BASE_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(BASE_DIR))
from PIL import Image, ImageDraw, ImageFilter
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE','config.settings')
import django
django.setup()
from django.contrib.auth.models import User
from core.models import SiteSettings
from blog.models import Category, Tag, BlogPost, Comment
from furniture.models import FurnitureCategory, FurnitureItem
from portfolio.models import PortfolioProject, ProjectImage
from contact.models import ContactMessage, Subscriber
from django.core.files import File
from datetime import date, timedelta
from textwrap import fill

BASE = Path(__file__).resolve().parents[1]
MEDIA = BASE / 'media' / 'seed'
MEDIA.mkdir(parents=True, exist_ok=True)
STATIC = BASE / 'static' / 'img'
STATIC.mkdir(parents=True, exist_ok=True)

palette = [(245,238,229),(220,200,176),(187,147,108),(67,58,52),(151,127,110),(139,92,246),(16,185,129)]

def make_art(path, title, size=(1200,800), idx=0):
    im = Image.new('RGB', size, palette[idx % len(palette)])
    d = ImageDraw.Draw(im)
    d.rounded_rectangle((40,40,size[0]-40,size[1]-40), radius=40, outline=(255,255,255), width=3)
    d.rectangle((120,170, size[0]-120, size[1]-130), fill=palette[(idx+1)%len(palette)])
    d.ellipse((90,90,280,280), fill=palette[(idx+2)%len(palette)])
    d.rectangle((200,280, 420,650), fill=palette[(idx+3)%len(palette)])
    d.rectangle((470,240, 860,650), fill=palette[(idx+4)%len(palette)])
    d.rectangle((910,320, 1030,650), fill=palette[(idx+5)%len(palette)])
    try:
        from PIL import ImageFont
        font_big = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf', 44)
        font_small = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', 24)
    except Exception:
        font_big = None
        font_small = None
    d.text((110, 80), title, fill=(255,255,255), font=font_big)
    d.text((110, size[1]-95), 'Seed fallback image used when remote stock photo is unavailable', fill=(255,255,255), font=font_small)
    im = im.filter(ImageFilter.SMOOTH_MORE)
    im.save(path, quality=92)

make_art(STATIC/'hero-room.png','Atelier Habitat Hero', idx=0)
(STATIC/'hero-room.svg').write_text("""<svg xmlns='http://www.w3.org/2000/svg' width='1200' height='800' viewBox='0 0 1200 800'><rect width='1200' height='800' fill='#0f172a'/><rect x='70' y='70' width='1060' height='660' rx='34' fill='#1e293b'/><rect x='160' y='180' width='270' height='360' rx='24' fill='#475569'/><rect x='470' y='150' width='430' height='430' rx='28' fill='#6366f1'/><rect x='930' y='230' width='120' height='300' rx='20' fill='#06b6d4'/><circle cx='230' cy='170' r='82' fill='#f59e0b'/><text x='120' y='110' font-size='48' font-family='Playfair Display, serif' fill='#fff'>Atelier Habitat</text></svg>""")

for i in range(1,61):
    make_art(MEDIA/f'img{i}.jpg', f'Interior Editorial {i}', idx=i)

user, _ = User.objects.get_or_create(username='admin', defaults={'email':'admin@example.com'})
user.set_password('admin12345')
user.is_superuser = True
user.is_staff = True
user.save()

settings, _ = SiteSettings.objects.get_or_create(pk=1)
settings.site_name = 'Atelier Habitat'
settings.tagline = 'Interior stories, furniture curation, and spatial elegance.'
settings.hero_title = 'Curated interiors for modern living'
settings.hero_subtitle = 'A visually rich editorial platform for interior design inspiration, furniture sourcing, and hospitality-grade portfolio storytelling.'
settings.about_text = 'Atelier Habitat is a Dhaka-rooted design journal and furniture atelier focused on warm minimalism, layered textures, livable luxury, and hospitality-inspired styling.'
settings.contact_email = 'hello@atelierhabitat.com'
settings.phone = '+880 1711-550055'
settings.address = 'Gulshan Avenue, Dhaka, Bangladesh'
settings.instagram = 'https://instagram.com/atelierhabitat'
settings.facebook = 'https://facebook.com/atelierhabitat'
settings.linkedin = 'https://linkedin.com/company/atelierhabitat'
settings.meta_description = 'Luxury interior design and furniture blog with portfolio case studies, editorial articles, and consultation-ready lead generation.'
settings.save()

categories = [
    ('Space Planning','space-planning','Editorial coverage for layout strategy, zoning, and circulation.'),
    ('Material Stories','material-stories','Material, finish, and tactile design thinking.'),
    ('Furniture Curation','furniture-curation','Furniture-led styling, sourcing, and mix advice.'),
    ('Lighting Design','lighting-design','Ambient, task, accent, and hospitality lighting topics.'),
    ('Hospitality Interiors','hospitality-interiors','Design lessons from boutique hotels, lounges, and cafés.'),
    ('Small Space Living','small-space-living','Compact apartment planning and multifunctional solutions.'),
]
cat_objs = {}
for name, slug, desc in categories:
    cat, _ = Category.objects.get_or_create(slug=slug, defaults={'name':name, 'description':desc})
    cat.description = desc
    cat.name = name
    cat.save()
    cat_objs[slug] = cat

for tag in ['Minimalism','Textiles','Woodwork','Small Spaces','Color Layering','Hospitality','Storage','Lighting','Stone','Open Plan','Hotel Style','Dining']:
    slug = tag.lower().replace(' ','-')
    Tag.objects.get_or_create(slug=slug, defaults={'name':tag})

tag_objs = {t.slug: t for t in Tag.objects.all()}

article_specs = [
    ('How to Layer Warm Neutrals Without Flattening a Room','A warm-neutral scheme works when tonal contrast, texture, and light reflection are planned together rather than selected one finish at a time.','space-planning',['color-layering','textiles']),
    ('Choosing Dining Chairs for Open-Plan Apartments','The best dining chairs in compact homes balance pull-back clearance, upholstery durability, and visual porosity.','furniture-curation',['small-spaces','dining']),
    ('Five Upholstery Fabrics That Age Gracefully in Family Homes','Performance linen blends, boucles with tight construction, and solution-dyed weaves are strong options when comfort and maintenance must coexist.','material-stories',['textiles']),
    ('Why Indirect Lighting Makes Luxury Interiors Feel Calm','Layered cove lighting softens contrast and lets architectural textures read without glare.','lighting-design',['lighting']),
    ('A Better Way to Design Entry Consoles','Entry furniture should manage drop zones, conceal charging clutter, and set the emotional tone for the home.','furniture-curation',['storage','woodwork']),
    ('Designing Boutique Bedrooms With Hotel-Level Comfort','The best boutique-style bedrooms use scale, tactile layering, and controlled symmetry to create rest.','hospitality-interiors',['hotel-style','textiles']),
    ('The Case for Rounded Furniture in Tight Living Rooms','Curved silhouettes improve circulation and visually soften dense furniture groupings.','small-space-living',['small-spaces']),
    ('How to Mix Oak, Walnut, and Painted Finishes in One Home','Mixed timber palettes feel deliberate when one undertone leads and the others play supporting roles.','material-stories',['woodwork','color-layering']),
    ('A Practical Guide to Reading Rug Proportions','A properly sized rug anchors a seating zone and clarifies circulation lines.','space-planning',['textiles']),
    ('Creating Kitchen Corners That Invite Conversation','Corner breakfast zones work best when light, back support, and acoustic softness are considered together.','space-planning',['small-spaces','dining']),
    ('Why Hospitality Designers Obsess Over Lighting Temperature','Color temperature changes how materials read, how skin tones feel, and how long guests want to linger.','hospitality-interiors',['hospitality','lighting']),
    ('Storage Furniture That Does Not Look Bulky','The cleanest storage pieces hide volume in plinths, shadow gaps, and visually lighter upper sections.','furniture-curation',['storage']),
    ('How Designers Use Contrast to Create Quiet Drama','Quiet drama comes from balancing matte and reflective surfaces, hard edges and soft forms, shadow and glow.','material-stories',['color-layering']),
    ('Before-and-After Lessons From Compact Apartment Renovations','Compact renovations succeed when walls, lighting, and furniture are considered as one system instead of separate purchases.','small-space-living',['small-spaces','lighting']),
    ('Styling Coffee Tables With Editorial Discipline','A composed coffee table relies on height variation, negative space, and one anchoring sculptural object.','furniture-curation',['minimalism']),
    ('Small Bedroom Layout Moves That Add Hotel Energy','Visual calm in compact bedrooms comes from disciplined furniture footprints, low-noise palettes, and integrated bedside lighting.','small-space-living',['hotel-style','small-spaces']),
    ('Travertine, Marble, and Limestone: When Each One Belongs','Stone feels elevated when its porosity, tone, and maintenance burden are matched to how the room is actually used.','material-stories',['stone']),
    ('Open-Plan Living Rooms Need More Than a Pretty Sofa','Open-plan rooms work when seating, lighting, storage, and circulation are tuned to one another instead of competing for attention.','space-planning',['open-plan','storage']),
]

for i, (title, excerpt, cat_slug, tags) in enumerate(article_specs, start=1):
    slug = title.lower().replace(' ','-').replace('?','').replace(',','').replace(':','')
    content = fill(
        excerpt + ' ' +
        'This article explains layout strategy, finish hierarchy, material selection, procurement timing, maintenance priorities, and styling decisions that help the room feel complete. ' +
        'It is written for homeowners, interior stylists, and design-build studios that want premium-looking results without wasteful over-decoration. ' +
        'Expect practical checkpoints, sourcing notes, dimension guidance, and a balanced view of mood, durability, and long-term maintenance.',
        92
    ).replace('\n', '\n\n')
    post, created = BlogPost.objects.get_or_create(slug=slug, defaults={
        'title': title,
        'excerpt': excerpt,
        'content': content,
        'category': cat_objs[cat_slug],
        'author': user,
        'published': True,
        'featured': i <= 6,
        'meta_description': excerpt,
        'read_time': 5 + (i % 6),
        'published_at': date.today() - timedelta(days=i*2)
    })
    post.title = title
    post.excerpt = excerpt
    post.content = content
    post.category = cat_objs[cat_slug]
    post.author = user
    post.published = True
    post.featured = i <= 6
    post.meta_description = excerpt
    post.read_time = 5 + (i % 6)
    post.published_at = date.today() - timedelta(days=i*2)
    if not post.featured_image:
        with open(MEDIA/f'img{i}.jpg','rb') as f:
            post.featured_image.save(f'post{i}.jpg', File(f), save=False)
    post.save()
    post.tags.set([tag_objs[tag] for tag in tags if tag in tag_objs])

sample_comments = [
    ('Nadia Rahman','nadia@example.com','Love how practical this breakdown is for real apartments.'),
    ('Sajid Karim','sajid@example.com','The furniture and circulation advice here is genuinely helpful.'),
    ('Maliha Noor','maliha@example.com','Would love a follow-up on lighting layers for rentals.'),
    ('Arif Hasan','arif@example.com','Very sharp guidance on balancing storage with visual calm.'),
]
for index, post in enumerate(BlogPost.objects.order_by('published_at')[:8], start=1):
    for j, (name, email, message) in enumerate(sample_comments[:2], start=1):
        Comment.objects.get_or_create(
            post=post,
            email=f'{index}-{j}-{email}',
            defaults={'name': name, 'message': message, 'approved': True}
        )

f_categories = [
    ('Seating','seating'),('Tables','tables'),('Storage','storage'),('Lighting','lighting'),('Bedroom','bedroom'),('Accessories','accessories')
]
fc_objs = {slug: FurnitureCategory.objects.get_or_create(slug=slug, defaults={'name':name})[0] for name,slug in f_categories}
items = [
    ('Crescent Lounge Chair','seating','Soft bouclé accent chair with walnut base.','Solid walnut, bouclé upholstery','740W x 810D x 760H mm'),
    ('Linear Travertine Coffee Table','tables','Low sculptural centerpiece with softened corners.','Travertine veneer, engineered core','1200W x 650D x 340H mm'),
    ('Ridge Media Console','storage','Clean-lined storage with cable concealment.','Oak veneer, powder-coated steel','1800W x 420D x 560H mm'),
    ('Halo Floor Lamp','lighting','Ambient lamp designed to wash walls with warm glow.','Brass finish, linen shade','1620H mm'),
    ('Aster Dining Chair','seating','Slim profile chair suited for open-plan dining.','Ash wood, saddle leather','520W x 560D x 780H mm'),
    ('Contour Sideboard','storage','Layered storage piece with ribbed door fronts.','Stained oak, brass pulls','1600W x 430D x 780H mm'),
    ('Marlow Bed Bench','bedroom','End-of-bed bench sized for boutique bedroom styling.','Oak frame, performance fabric','1400W x 420D x 460H mm'),
    ('Dune Bedside Table','bedroom','Compact bedside storage with rounded drawer detailing.','American oak, brass feet','520W x 420D x 540H mm'),
    ('Orchid Wall Sconce','lighting','Soft-glow wall light for bedroom and corridor use.','Brushed brass, frosted glass','320H mm'),
    ('Arc Dining Table','tables','Rounded rectangular dining table for family gatherings.','Oak veneer, solid edge, matte lacquer','2200W x 1000D x 760H mm'),
    ('Studio Mirror Console','accessories','Lean console mirror built for entry styling and reflection.','Metal frame, bronze mirror','900W x 250D x 1900H mm'),
    ('Vale Ottoman','seating','Low upholstered ottoman that doubles as informal seating.','Performance fabric, solid ash base','620W x 620D x 420H mm'),
]
for i,(title,cslug,subtitle,mat,dim) in enumerate(items, start=19):
    slug = title.lower().replace(' ','-')
    obj, _ = FurnitureItem.objects.get_or_create(slug=slug, defaults={
        'category': fc_objs[cslug],
        'title': title,
        'subtitle': subtitle,
        'description': subtitle + ' Designed for interior projects that need timeless proportion, practical durability, and a premium tactile finish.',
        'material': mat,
        'dimensions': dim,
        'price_label': 'Available on request',
        'featured': i <= 24,
        'published': True,
    })
    obj.category = fc_objs[cslug]
    obj.title = title
    obj.subtitle = subtitle
    obj.description = subtitle + ' Designed for interior projects that need timeless proportion, practical durability, and a premium tactile finish.'
    obj.material = mat
    obj.dimensions = dim
    obj.price_label = 'Available on request'
    obj.featured = i <= 24
    obj.published = True
    if not obj.cover_image:
        with open(MEDIA/f'img{i}.jpg','rb') as f:
            obj.cover_image.save(f'fur{i}.jpg', File(f), save=False)
    obj.save()

projects = [
    ('The Ash Residence','Boutique residential client','Gulshan, Dhaka','Interior design + furniture curation'),
    ('Noor Reading Lounge','Independent bookstore founder','Dhanmondi, Dhaka','Interior styling + custom millwork'),
    ('Terracotta Courtyard Suite','Hospitality operator','Cox\'s Bazar','Concept design + FF&E selection'),
    ('Monsoon Penthouse','Private client','Banani, Dhaka','Renovation + lighting strategy'),
    ('Harbor View Lobby','Hotel group','Chattogram','Lobby refresh + furniture sourcing'),
    ('Serein Studio Apartment','Young professional client','Bashundhara, Dhaka','Small-space planning + custom storage'),
]
for i,(title,client,loc,scope) in enumerate(projects, start=33):
    slug = title.lower().replace(' ','-').replace("'",'')
    obj, _ = PortfolioProject.objects.get_or_create(slug=slug, defaults={
        'title': title,
        'client': client,
        'location': loc,
        'scope': scope,
        'summary': 'A layered interior scheme built around calm material transitions, warm timber, and hospitality-inspired detailing.',
        'challenge': 'The project needed to feel elevated without becoming precious, while solving storage, circulation, and lighting constraints.',
        'solution': 'We introduced a restrained palette, custom joinery, and layered ambient lighting to create visual rhythm and functional clarity.',
        'result': 'The finished space photographs beautifully, supports daily use, and gives the client a distinctive business-ready environment.',
        'completed_on': date.today()-timedelta(days=i*18),
        'published': True,
        'featured': i <= 36,
    })
    obj.title = title
    obj.client = client
    obj.location = loc
    obj.scope = scope
    obj.summary = 'A layered interior scheme built around calm material transitions, warm timber, and hospitality-inspired detailing.'
    obj.challenge = 'The project needed to feel elevated without becoming precious, while solving storage, circulation, and lighting constraints.'
    obj.solution = 'We introduced a restrained palette, custom joinery, and layered ambient lighting to create visual rhythm and functional clarity.'
    obj.result = 'The finished space photographs beautifully, supports daily use, and gives the client a distinctive business-ready environment.'
    obj.completed_on = date.today()-timedelta(days=i*18)
    obj.published = True
    obj.featured = i <= 36
    if not obj.cover_image:
        with open(MEDIA/f'img{i}.jpg','rb') as f:
            obj.cover_image.save(f'proj{i}.jpg', File(f), save=False)
    obj.save()
    for offset in range(1, 3):
        caption = f'{title} gallery scene {offset}'
        if not obj.images.filter(caption=caption).exists():
            with open(MEDIA/f'img{i + offset}.jpg','rb') as f:
                gallery = ProjectImage(project=obj, caption=caption)
                gallery.image.save(f'proj{i}_{offset}.jpg', File(f), save=True)

leads = [
    ('Nadia Rahman','nadia.rahman@example.com','+8801711111111','Residential redesign consultation','Looking for interior concept design and furniture sourcing support for a 2,400 sq ft apartment in Dhaka.'),
    ('Fahim Chowdhury','fahim@example.com','+8801711222233','Boutique café design','Need a moodboard-led concept and seating plan for a compact hospitality space.'),
    ('Sadia Islam','sadia@example.com','+8801711333344','Bedroom refresh project','Interested in a warm neutral bedroom with custom storage and layered lighting.'),
    ('Tanvir Ahmed','tanvir@example.com','+8801711444455','Office lounge styling','We want a client lounge corner with hospitality quality furniture and softer lighting.'),
    ('Nusrat Jahan','nusrat@example.com','+8801711555566','Furniture sourcing help','Please share a quote for dining chairs, a sideboard, and one custom rug.'),
    ('Ayon Karim','ayon@example.com','+8801711666677','Apartment styling','Need styling support before a property photo shoot in Gulshan.'),
    ('Maria Sultana','maria@example.com','+8801711777788','Hotel corridor refresh','Looking for hallway lighting and wall treatment suggestions for a boutique property.'),
    ('Rakib Hasan','rakib@example.com','+8801711888899','Living room layout advice','Would like a consultation on sofa placement, rug scale, and a new coffee table.'),
]
for name, email, phone, subject, message in leads:
    ContactMessage.objects.get_or_create(email=email, subject=subject, defaults={'name':name,'phone':phone,'message':message})

subscriber_emails = [
    'subscriber@example.com','designlover01@example.com','linenandlight@example.com','warmminimal@example.com','spaceplan@example.com',
    'hospitalitynotes@example.com','studioedit@example.com','texturejournal@example.com','oakandstone@example.com','thecalmhome@example.com',
    'dhakadecor@example.com','moodboardmail@example.com','atelierreader@example.com','furnituredrop@example.com','interiordispatch@example.com',
    'quietluxury@example.com','projectnotes@example.com','designbrief@example.com','casestudy@example.com','curatedcorners@example.com'
]
for email in subscriber_emails:
    Subscriber.objects.get_or_create(email=email)

print('Seed complete. Login: admin / admin12345')
