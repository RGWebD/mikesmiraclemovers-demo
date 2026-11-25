# Facts for Mike's Miracle Movers, L.L.C. Sources (captured 2026-11-25): Google Business Profile + truck lettering (photo g01/g02).
# See /workspace/site3-research/notes.md. Nothing here is invented: no address, no owner name as fact, no prices.
BASE = "https://rgwebd.github.io/mikesmiraclemovers-demo/"
NAME = "Mike's Miracle Movers"
LEGAL = "Mike's Miracle Movers, L.L.C."
PHONE = "(904) 710-1565"; TEL = "+19047101565"
CITY = "Jacksonville"; REGION = "FL"
RATING = "4.7"; REVIEWS = 354
TAGLINE = "We make it look EASY!"          # painted on the truck
SLOGAN = "Let's make a move"               # on their own flyer (Google photos)
MAPS = "https://maps.app.goo.gl/jXwExXL5nJ8bVdNc8"
MAPS_LONG = "https://www.google.com/maps/place/Mike's+Miracle+Movers,+L.L.C./data=!4m6!3m5!1s0x88e5b436aa611997:0xbe6fd3cb3e9adc6e!8m2!3d30.2260024!4d-81.600999!16s%2Fg%2F11g6hv279f"
TRUCK_LINES = ["Moving", "Commercial", "Residential", "Local", "Storage", "Business"]   # truck lettering
ATTRS = ["Online estimates", "LGBTQ+ friendly", "Asian-owned"]                     # Google attributes
# hours (Google): day index 0=Sun
HOURS = [("Sunday","8 AM","8 PM",8,20),("Monday","6 AM","10 PM",6,22),("Tuesday","6 AM","10 PM",6,22),("Wednesday","6 AM","10 PM",6,22),
         ("Thursday","6 AM","10 PM",6,22),("Friday","6 AM","10 PM",6,22),("Saturday","6 AM","9 PM",6,21)]
HOLIDAYS = {"2026-11-26":"Thanksgiving","2026-11-27":"Black Friday"}   # Google: "hours might differ"
AREAS = ["Jacksonville", "Orange Park", "the Jacksonville area", "long-distance trips like Jacksonville to Savannah"]

REVIEWS_LIST = [
 dict(name="Manzima Jain", age="3 months ago", tag="Jacksonville \u2192 Savannah", pull="Mike made the whole process smooth and hassle-free.",
  text="Mike did a fantastic job helping us move from Jacksonville to Savannah. He was professional, punctual, careful, and very helpful throughout the entire move. He handled our furniture and belongings with great care, and everything arrived safely.\nMoving to another city can be stressful, but Mike made the whole process smooth and hassle-free. I really appreciate his hard work and positive attitude.\nI would definitely recommend Mike to anyone looking for a reliable and trustworthy mover. Great service from start to finish!"),
 dict(name="Laura Mitchell", age="a year ago", tag="2 bed / 2 bath", pull="They are Tetris masters!",
  text="Absolutely the BEST! Mike and his crew are amazing. They are fast and efficient amongst being gentle with your stuff. They are Tetris masters! Super friendly and professional. I have used them several times and will continue to do so!!  Moved my 2 bed 2 bath packed and unloaded in total 3 hours. The pricing is the most affordable and so worth it!!  Your back will thank you!!"),
 dict(name="Keith Knapp", age="11 months ago", tag="Last-minute move", pull="Michael saved the day.",
  text="I highly recommend Michael and his moving company. When my original movers canceled last minute, Michael stepped in without hesitation. He was professional, responsive, and turned what could have been a stressful day into a seamless experience. His crew arrived promptly, worked efficiently, and handled my belongings with exceptional care\u2014nothing was damaged. Michael remained calm and organized throughout, ensuring the move was smooth despite the short notice.\nIf you\u2019re looking for reliability and top\u2011notch service, this is the company to call. Michael saved the day, and I\u2019ll definitely be recommending Michael to anyone in need of movers."),
 dict(name="Erin Montgomery", age="8 months ago", tag="Townhome \u2192 storage unit", pull="Friendly, responsive, efficient, organized, very reasonably priced (and strong!).",
  text="I\u2019m so thankful a neighbor recommended Mike\u2019s Miracle Movers to me! Mike and Chris moved my furniture and other belongings out of my townhome and into a storage unit. They were friendly, responsive, efficient, organized, very reasonably priced (and strong!). It gave me so much peace of mind knowing I had these 2 awesome guys taking care of my move, and I will most definitely hire them again to move me into a new home in the near future. Five stars all around for Mike and his team!"),
 dict(name="Amy Crum", age="a year ago", tag="Local move", pull="I have used this company for 8 years!!!",
  text="5/5 Stars - Excellent Service!\nI have used this company for 8 years!!! I recently hired Mike\u2019s Miracle Movers for a local move, and I couldn\u2019t be more impressed with their professionalism and efficiency. From the very first phone call, they were friendly, helpful, and provided a clear breakdown of the pricing and moving process.\nOn the day of the move, the crew arrived on time, ready to get started. They handled all of my furniture with care, wrapping delicate items and making sure everything was securely loaded onto the truck. I was especially impressed by how quickly they worked without sacrificing the quality of their service.\nThe move was completed smoothly, and everything arrived at the new location in perfect condition. The team was courteous and respectful throughout the entire process, and they made a typically stressful experience much easier.\nI highly recommend Mike\u2019s Miracle Movers for anyone looking for a reliable and efficient moving company. Great service, competitive prices, and a job well done!"),
 dict(name="Ken Juhlin", age="a year ago", tag="Jacuzzi move", pull="Tough moving job made to look easy.",
  text="Mike came thru with a 2 day moving deadline. These guys showed up on time and ready to move the Jacuzzi to my house. Tough moving job made to look easy with Mike and crew. No damage to either yard/landscaping at both homes. Thanks"),
 dict(name="Emily Vidal-Torres", age="2 years ago", tag="House move", pull="The pricing was fair and transparent\u2014no hidden fees or surprises.",
  text="I had an excellent experience with Mike and his team. From start to finish, the team was professional, efficient, and friendly. They arrived on time and handled all of our belongings with great care, making sure everything was transported safely. The movers worked quickly but without rushing, and they even went the extra mile to ensure that everything was placed exactly where I wanted it in the new house. The pricing was fair and transparent\u2014no hidden fees or surprises. Highly recommend this moving company to anyone looking for reliable movers!"),
 dict(name="Ana Maria McPherson", age="4 weeks ago", tag="Dining room set", pull="Took great care to wrap and protect the table and chairs.",
  text="Mike and his crew did a fantastic job moving my dining room set. They showed up right when promised, took great care to wrap and protect the table and chairs, and made the whole process completely stress-free. Very polite, helpful, and professional throughout. Highly recommend Mike for any moving needs!"),
 dict(name="Joan Warren", age="2 months ago", tag="Marketplace pickup", pull="Reliable, careful with furniture and pleasant.",
  text="Moved a large hutch I purchased on Marketplace. Met at sellers home and delivered to mine. Reliable, careful with furniture and pleasant. Communication when obstacles delayed, but also patient when my route back delayed me. Would use their service again."),
 dict(name="Jaiden Munger", age="7 months ago", tag="Weekend move", pull="Even moved more items than we had originally asked them to!",
  text="We were recommended Mikes services & booked with him this past weekend to move. They arrived on time, were extremely efficient, & even moved more items than we had originally asked them to! We\u2019re grateful for Mikes Movers and will definitely use them again for our next move!"),
]

# services: key, title, photo or None, short, long, proof (reviewer name), icon
SVC = [
 ("local","Local moves","g07","Houses, townhomes and apartments across Jacksonville, Orange Park and nearby.",
  "Packed, loaded, driven across town and set down where you want it. Reviewers tell us about whole homes moved in an afternoon and furniture placed exactly where they wanted it in the new house.","Laura Mitchell","home"),
 ("long","Long-distance moves","g04","Out of town? We\u2019ve driven Jacksonville families all the way to Savannah.",
  "Same crew, same care, longer drive. Your furniture is wrapped and loaded tight so it arrives the way it left.","Manzima Jain","route"),
 ("apt","Apartments &amp; condos","g09","Stairs, elevators and tight hallways, handled.",
  "Apartment and condo moves done quick and tidy, careful with the building as well as your things. One reviewer’s 2 bed, 2 bath was packed and unloaded in three hours total.","Laura Mitchell","bldg"),
 ("storage","Storage unit moves","g06","Into storage, out of storage, or straight to your new place.",
  "We load your unit neatly so it\u2019s easy to get back into, then move it all again when you\u2019re ready.","Erin Montgomery","box"),
 ("office","Office &amp; commercial","g02","Commercial and business moves: it says so right on the truck.",
  "Desks, files and equipment moved with the same organized approach, so your team can get back to work.",None,"brief"),
 ("heavy","Hot tubs, pianos &amp; heavy items","g03","Jacuzzis, pianos and the pieces nobody else wants to lift.",
  "Hot tubs and other heavy, awkward items moved with straps, dollies and a plan, without wrecking the yard.","Ken Juhlin","weight"),
 ("pack","Packing &amp; wrapping","g05","Moving blankets, shrink wrap and careful hands.",
  "Delicate pieces get wrapped and protected before they ever leave the room, from dining sets to dressers.","Ana Maria McPherson","wrap"),
 ("single","Single items &amp; Marketplace pickups",None,"Bought a hutch on Marketplace? We\u2019ll grab it and bring it home.",
  "One big piece or a handful: we meet you at the seller\u2019s place and deliver to yours.","Joan Warren","truck"),
 ("rush","Last-minute moves",None,"Movers cancel? Deadline in two days? Call us.",
  "Reviewers tell us about stepping in when their original movers canceled and beating a two-day deadline.","Keith Knapp","bolt"),
 ("load","Loading &amp; unloading help",None,"Rented your own truck? We\u2019ll do the heavy lifting.",
  "Already have a rental truck? Our crew can load it or unload it for you, packed tight and secure.",None,"dolly"),
]

CAP = {  # gallery captions + filter tags
 'g01':("Our truck and crew, ready to roll","crew"),
 'g02':("The truck on a commercial job","crew"),
 'g04':("A truck load, wrapped and stacked tight","pack"),
 'g05':("Shrink-wrapped and strapped for the carry","pack"),
 'g03':("A hot tub delivered and set down","heavy"),
 'g11':("Hot tub in place on the back patio","heavy"),
 'g06':("A storage unit, loaded neatly","rooms"),
 'g07':("Sectional set down in the new place","rooms"),
 'g09':("Condo move in progress","rooms"),
}
