from ext import app, db
from models import User, Product

PRODUCTS_DATA = {
    "Adidas": [
        ("Ultraboost 23",           "Running",    189.99, "Premium running shoes with BOOST midsole for incredible energy return and a Primeknit upper."),
        ("Stan Smith Classic",      "Lifestyle",   89.99, "Iconic tennis-inspired leather sneaker with clean perforated three-stripe detailing."),
        ("Predator Accuracy FG",    "Football",   149.99, "Control-focused football boots with CONTROLFRAME outsole and rubber elements for precision."),
        ("Tiro 23 Training Pants",  "Apparel",     49.99, "Slim-fit training pants made from recycled materials with zip pockets and tapered legs."),
        ("Adizero Adios Pro 3",     "Running",    249.99, "Elite marathon racer with ENERGYRODS2.0 and Lightstrike Pro foam technology."),
        ("NMD_R1 V3",               "Lifestyle",  129.99, "Futuristic streetwear with Boost cushioning and a sleek sock-like Primeknit upper."),
        ("Terrex Free Hiker 2.0",   "Hiking",     199.99, "Trail boot with Continental rubber outsole and responsive Boost midsole for any terrain."),
        ("Adidas Hoodie Essential", "Apparel",     64.99, "Classic fleece hoodie with kangaroo pocket and embroidered logo, made from recycled polyester."),
        ("Alphaskin Tights",        "Training",    44.99, "Compression training tights with Climalite technology to keep you cool during intense workouts."),
        ("Pro Next Volleyball",     "Equipment",   34.99, "Butyl bladder volleyball with deep channel design for consistent flight and outstanding grip."),
    ],
    "Nike": [
        ("Air Max 270",             "Lifestyle",  149.99, "Lifestyle shoe featuring the largest Max Air unit yet for all-day comfort and a bold look."),
        ("ZoomX Vaporfly NEXT% 3",  "Running",    259.99, "Elite race shoe with ZoomX foam and carbon fiber plate for maximum speed and energy return."),
        ("Dri-FIT Academy Shorts",  "Training",    34.99, "Lightweight training shorts with Dri-FIT technology to wick sweat and keep you dry."),
        ("Mercurial Superfly 9",    "Football",   229.99, "Speed-focused football boot with ACC texture and Dynamic Fit collar for explosive play."),
        ("Air Force 1 07",          "Lifestyle",  109.99, "The classic all-white leather basketball-inspired sneaker that never goes out of style."),
        ("Metcon 9",                "Training",   129.99, "Purpose-built for cross-training with a wide, flat heel for heavy lifts and rope climbs."),
        ("Pegasus 41",              "Running",    139.99, "Workhorse daily trainer updated with React X foam and a wider forefoot for a stable ride."),
        ("Therma-FIT Legacy Hoodie","Apparel",     74.99, "Warm fleece-lined hoodie with Therma-FIT technology designed for cold-weather training."),
        ("Court Vision Low",        "Basketball",  79.99, "Retro basketball shoe with a cupsole and perforated toe for a clean, timeless profile."),
        ("Strike Football",         "Equipment",   29.99, "Durable all-surface training football with textured casing for consistent touch and control."),
    ],
    "Puma": [
        ("RS-X Reinvention",        "Lifestyle",  109.99, "Chunky retro runner inspired by the 80s RS series with a multi-layer mesh upper and bold colorways."),
        ("Future 7 Ultimate FG",    "Football",   199.99, "Ultimate football boot with FUZIONFIT+ upper and GripControl Pro texture for elite ball touch."),
        ("Velocity Nitro 3",        "Running",    139.99, "Daily trainer with NITRO Elite foam offering feather-light cushioning and springy energy return."),
        ("Suede Classic XXI",       "Lifestyle",   74.99, "The all-time classic suede sneaker with formstrip detailing — a streetwear icon since 1968."),
        ("Evostripe Hoodie",        "Apparel",     59.99, "Bold graphic hoodie made from recycled materials with DryCell moisture management technology."),
        ("PWRFRAME TR 3",           "Training",    99.99, "Training shoe with reinforced PWRFRAME for stability during lateral movements and heavy lifts."),
        ("Deviate Nitro Elite 2",   "Running",    219.99, "Carbon-plated race shoe with NITROFOAM Elite for maximum energy return in competition."),
        ("King Top DI TT",          "Football",    89.99, "Indoor training boot with a leather upper and non-marking rubber outsole for hard court surfaces."),
        ("Session Gym Bag",         "Equipment",   44.99, "Spacious gym bag with separate shoe compartment, water bottle pocket and padded laptop sleeve."),
        ("Essentials Logo Tee",     "Apparel",     24.99, "Clean cotton t-shirt with small Cat logo — the perfect everyday training or casual wear top."),
    ],
    "Air Jordan": [
        ("Air Jordan 1 Retro High OG", "Basketball", 179.99, "The shoe that started it all — the original high-top with premium leather and iconic Wings logo."),
        ("Air Jordan 4 Retro",         "Basketball", 209.99, "Visible Air unit, mesh panels and plastic wing eyelets define this legendary 1989 basketball silhouette."),
        ("Air Jordan 11 Retro",        "Basketball", 219.99, "Patent leather mudguard, carbon fiber shank plate and full-length Air unit for performance and style."),
        ("Air Jordan 3 Retro",         "Lifestyle",  189.99, "Elephant print detailing and a visible Air heel unit make this the most iconic Jordan silhouette."),
        ("Jumpman Classic Cap",        "Apparel",     34.99, "Structured six-panel cap with iconic Jumpman embroidery and an adjustable snapback closure."),
        ("Air Jordan 6 Retro",         "Basketball", 199.99, "Rubber pull tabs, integrated lace locks and a sculpted midsole from the first championship run."),
        ("Jordan Sport Shorts",        "Apparel",     44.99, "Lightweight Dri-FIT shorts with side panels and elastic waist — designed for court and street."),
        ("Air Jordan 36 PF",           "Basketball", 159.99, "Performance basketball shoe with Eclipse Plate and Zoom Air for explosive court movements."),
        ("Air Jordan 5 Retro",         "Lifestyle",  199.99, "Reflective tongue, shark-tooth midsole and mesh upper inspired by WWII fighter planes."),
        ("Jordan Flight MVP Bag",      "Equipment",   49.99, "Large duffel with adjustable strap, Jumpman logo and multiple compartments for all your gear."),
    ],
    "Under Armour": [
        ("HOVR Phantom 3",         "Running",    139.99, "Connected running shoe with UA HOVR cushioning and MapMyRun integration to track your metrics."),
        ("Curry 11 Basketball",    "Basketball", 159.99, "Stephen Curry signature shoe with Flow cushioning and traction pattern for explosive cuts."),
        ("Project Rock 5",         "Training",   129.99, "Dwayne Johnson signature cross-trainer with external heel clip and UA TriBase for heavy lifts."),
        ("Streaker Run Tee",       "Apparel",     34.99, "Ultra-lightweight HeatGear fabric tee that moves with you and wicks sweat during hard runs."),
        ("Charged Assert 10",      "Running",     74.99, "Versatile everyday runner with Charged Cushioning midsole for comfort and long-lasting durability."),
        ("Vanish Woven Shorts",    "Training",    44.99, "Super-light woven training shorts with 4-way stretch and an internal waistband phone pocket."),
        ("HOVR Apex 5 Training",   "Training",   109.99, "Versatile training shoe with HOVR foam, wide base for squats and herringbone rubber for grip."),
        ("ColdGear Armour Hoodie", "Apparel",     89.99, "Fitted fleece hoodie with ColdGear technology to trap heat and keep you warm during cold sessions."),
        ("TB12 Football",          "Equipment",  119.99, "Official football with deep pebble grain leather and a consistent spiral for precision passing."),
        ("UA Hustle 5.0 Backpack", "Equipment",   54.99, "Large backpack with laptop sleeve, UA Storm finish for water resistance and HeatGear-lined straps."),
    ],
}


def init_db():
    with app.app_context():
        db.create_all()


        if Product.query.count() == 0:
            for brand, items in PRODUCTS_DATA.items():
                for name, cat, price, desc in items:
                    p = Product(name=name, brand=brand, category=cat, price=price, description=desc, stock=20)
                    db.session.add(p)
            db.session.commit()
            print(f"Seeded {Product.query.count()} products.")
        else:
            print("Products already seeded.")


        if not User.query.filter_by(username="admin").first():
            admin = User(username="admin", email="admin@prozone.com", role="admin")
            admin.set_password("admin123")
            db.session.add(admin)
            db.session.commit()
            print("Admin user created: username=admin  password=admin123")
        else:
            print("Admin already exists.")


if __name__ == "__main__":
    init_db()
    print("Database ready.")
