from django.core.management.base import BaseCommand, CommandError
from django.db import connection
from account.models import Profile
from blog.models import Post, Image, Category

class Command(BaseCommand):
    help = "Creates posts and assign it to categories and assign its images together"

    def handle(self, *args, **options):
        self.flush_table(Post , Image)
        self.create_posts()

    def flush_table(self ,*model):
        self.stdout.write('Flushing data from Post table...\n')
        with connection.cursor() as cursor:
            cursor.execute(f'TRUNCATE TABLE {model[0]._meta.db_table} RESTART IDENTITY CASCADE')

        self.stdout.write('Flushing data from Image table...\n')
        with connection.cursor() as cursor:
            cursor.execute(f'TRUNCATE TABLE {model[1]._meta.db_table} RESTART IDENTITY CASCADE')
    def create_posts(self):
        try:
            categories = Category.objects.all()
            posts_data = [
                {
                    "author_id": 2,
                    "category_id": categories.filter(name='Nature').first().id,
                    "images": ["posts/images/iceland_1.jpg", "posts/images/iceland_2.jpg" , "posts/images/iceland_3.jpg"],
                    "hero_image": "posts/hero_images/iceland.jpg",
                    "title": "Exploring the Wonders of Iceland",
                    "short_content": "Iceland, known as the Land of Fire and Ice, offers breathtaking landscapes. From glaciers to volcanoes, it's a paradise for nature lovers. The Northern Lights are a must-see. Reykjavik, the capital, is a hub of culture and history.",
                    "main_content": "Iceland is a Nordic island country in the North Atlantic Ocean. It is known for its dramatic landscapes with volcanoes, geysers, hot springs, and lava fields. The country is also famous for its glaciers, which cover about 11% of the land area. The Vatnajökull glacier is the largest in Europe. Iceland's capital, Reykjavik, is home to the National and Saga museums, tracing the country's Viking history. The Blue Lagoon geothermal spa is one of the most popular tourist attractions. Iceland is also a great place to see the Northern Lights, a natural light display in the Earth's sky. The country has a rich cultural heritage, with traditional music, literature, and cuisine. Icelandic cuisine includes dishes like lamb, seafood, and skyr, a traditional dairy product. The country is also known for its strong literary tradition, with many famous authors like Halldór Laxness. Iceland is a popular destination for adventure tourism, offering activities like hiking, ice climbing, and whale watching. The country is also known for its commitment to renewable energy, with most of its electricity coming from hydroelectric and geothermal sources. Iceland is a unique and fascinating destination that offers something for everyone."
                },
                {
                    "author_id": 3,
                    "category_id": categories.filter(name='Technology').first().id,
                    "images": ["posts/images/future_tech_1.jpg", "posts/images/future_tech_2.jpg" , "posts/images/future_tech_3.jpg"],
                    "hero_image": "posts/hero_images/future_tech.jpg",
                    "title": "The Rise of Artificial Intelligence",
                    "short_content": "Artificial Intelligence (AI) is transforming industries worldwide. From healthcare to finance, AI is revolutionizing how we work. Machine learning and deep learning are key components. Ethical concerns around AI are also growing.",
                    "main_content": "Artificial Intelligence (AI) refers to the simulation of human intelligence in machines that are programmed to think like humans and mimic their actions. AI is a broad field that includes machine learning, deep learning, natural language processing, and robotics. AI is being used in various industries, including healthcare, finance, transportation, and entertainment. In healthcare, AI is being used to diagnose diseases, develop treatment plans, and even perform surgeries. In finance, AI is used for fraud detection, risk management, and algorithmic trading. Self-driving cars are one of the most exciting applications of AI in transportation. AI is also being used in the entertainment industry to create realistic video game characters and generate music and art. Machine learning, a subset of AI, involves training algorithms to learn from data and make predictions. Deep learning, a more advanced form of machine learning, uses neural networks to model complex patterns in data. Despite its many benefits, AI also raises ethical concerns, such as job displacement, privacy issues, and the potential for bias in decision-making. Governments and organizations are working to develop regulations and guidelines to ensure the responsible use of AI. The future of AI is promising, with ongoing research and development leading to new and innovative applications. AI has the potential to transform our world in ways we can only imagine."
                },
                {
                    "author_id": 2,
                    "category_id": categories.filter(name='Food').first().id,
                    "images": ["posts/images/french_cuisine_1.jpg" , "posts/images/french_cuisine_2.jpg" , "posts/images/french_cuisine_3.jpg"],
                    "hero_image": "posts/hero_images/french_cuisine.jpg",
                    "title": "The Art of French Cuisine",
                    "short_content": "French cuisine is renowned for its elegance and flavor. From croissants to coq au vin, French food is a culinary delight. Techniques like sous-vide and flambé are widely used. French wine and cheese are also world-famous.",
                    "main_content": "French cuisine is known for its sophistication and variety. It is characterized by its use of fresh, high-quality ingredients and meticulous preparation techniques. French cuisine includes a wide range of dishes, from simple country fare to elaborate haute cuisine. Some of the most famous French dishes include coq au vin, boeuf bourguignon, and ratatouille. French pastries, such as croissants, éclairs, and macarons, are also world-renowned. French cooking techniques, such as sous-vide, flambé, and braising, are widely used in professional kitchens. French cuisine is also known for its use of sauces, with classics like béchamel, hollandaise, and velouté. French wine and cheese are integral parts of the cuisine, with regions like Bordeaux, Burgundy, and Champagne producing some of the world's best wines. French cheese varieties, such as Brie, Camembert, and Roquefort, are beloved by food enthusiasts. The French take great pride in their culinary traditions, and meals are often seen as a time to relax and enjoy good food and company. French cuisine has had a significant influence on global culinary practices, with many chefs around the world training in French cooking techniques. The art of French cuisine is a testament to the country's rich cultural heritage and its dedication to the culinary arts."
                },
                {
                    "author_id": 3,
                    "category_id": categories.filter(name='Fashion').first().id,
                    "images":["posts/images/streetwearfashion_1.jpg" , "posts/images/streetwearfashion_2.jpg" , "posts/images/streetwearfashion_3.jpg"],
                    "hero_image": "posts/hero_images/streetwearfashion.jpg",
                    "title": "The Evolution of Streetwear Fashion",
                    "short_content": "Streetwear has become a global fashion phenomenon. Originating from skate and hip-hop cultures, it blends comfort and style. Brands like Supreme and Off-White dominate the scene. Streetwear continues to influence high fashion.",
                    "main_content": "Streetwear is a style of casual clothing that became global in the 1990s. It originated from the skate and hip-hop cultures of California and New York. Streetwear is characterized by its comfortable, casual, and often oversized fit. It includes items like hoodies, t-shirts, sneakers, and baseball caps. Streetwear brands, such as Supreme, Off-White, and Bape, have gained a cult following and are known for their limited-edition releases and collaborations with high-end fashion brands. Streetwear has also been influenced by Japanese fashion, with brands like A Bathing Ape and Comme des Garçons playing a significant role in its development. The rise of social media has helped streetwear gain mainstream popularity, with influencers and celebrities often seen wearing streetwear brands. Streetwear has also had a significant impact on high fashion, with luxury brands like Louis Vuitton and Gucci incorporating streetwear elements into their collections. The streetwear movement is not just about clothing; it is also a lifestyle that includes music, art, and skateboarding. Streetwear continues to evolve, with new brands and trends emerging regularly. The future of streetwear looks promising, with its influence on fashion and culture showing no signs of slowing down."
                },
                {
                    "author_id": 2,
                    "category_id": categories.filter(name='Health').first().id,
                    "images": ["posts/images/mental_health_1.jpg" , "posts/images/mental_health_2.jpg" , "posts/images/mental_health_3.jpg"],
                    "hero_image": "posts/hero_images/mental_health.jpg",
                    "title": "The Importance of Mental Health Awareness",
                    "short_content": "Mental health is as important as physical health. Awareness campaigns aim to reduce stigma and promote well-being. Common issues include anxiety, depression, and stress. Seeking help is a sign of strength, not weakness.",
                    "main_content": "Mental health refers to our emotional, psychological, and social well-being. It affects how we think, feel, and act. Mental health is important at every stage of life, from childhood and adolescence through adulthood. Mental health issues, such as anxiety, depression, and stress, are common and can affect anyone. Mental health awareness campaigns aim to reduce the stigma associated with mental health issues and promote well-being. These campaigns encourage people to seek help when they need it and to support others who may be struggling. Mental health issues can be caused by a variety of factors, including genetics, environment, and life experiences. Treatment for mental health issues often includes therapy, medication, and lifestyle changes. It is important to seek help if you are experiencing mental health issues, as early intervention can lead to better outcomes. Mental health is just as important as physical health, and taking care of your mental health is essential for overall well-being. There are many resources available for those struggling with mental health issues, including hotlines, support groups, and online resources. Mental health awareness is crucial for creating a society where everyone feels supported and valued. By promoting mental health awareness, we can help reduce the stigma and ensure that everyone has access to the help they need."
                },
                {
                    "author_id": 3,
                    "category_id": categories.filter(name='Sports').first().id,
                    "images": ["posts/images/extreme_sports_1.jpg" , "posts/images/extreme_sports_2.jpg" , "posts/images/extreme_sports_3.jpg"],
                    "hero_image": "posts/hero_images/extreme_sports.jpg",
                    "title": "The Thrill of Extreme Sports",
                    "short_content": "Extreme sports offer adrenaline-pumping experiences. Activities like skydiving, snowboarding, and rock climbing are popular. Safety is paramount, with proper gear and training essential. Extreme sports push the limits of human capability.",
                    "main_content": "Extreme sports are activities that involve a high level of risk and adrenaline. They often require specialized equipment and training. Some of the most popular extreme sports include skydiving, snowboarding, rock climbing, and BASE jumping. Extreme sports are not for the faint of heart, as they often involve pushing the limits of human capability. Safety is a top priority in extreme sports, with participants required to use proper gear and follow strict safety protocols. Extreme sports can be physically and mentally demanding, requiring a high level of fitness and concentration. Despite the risks, extreme sports offer a unique sense of freedom and exhilaration. Many extreme sports enthusiasts describe the experience as life-changing. Extreme sports have gained popularity in recent years, with events like the X Games showcasing the skills of top athletes. The rise of social media has also helped extreme sports gain a wider audience, with athletes sharing their experiences and stunts online. Extreme sports are not just about the thrill; they also promote a sense of community and camaraderie among participants. The future of extreme sports looks bright, with new activities and innovations constantly emerging. Whether you're a seasoned athlete or a beginner, extreme sports offer an exciting way to challenge yourself and experience the world in a new way."
                },
                {
                    "author_id": 2,
                    "category_id": categories.filter(name='Music').first().id,
                    "images": ["posts/images/music_streaming_1.jpg" , "posts/images/music_streaming_2.jpg" , "posts/images/music_streaming_3.jpg"],
                    "hero_image": "posts/hero_images/music_streaming.jpg",
                    "title": "The Impact of Streaming on the Music Industry",
                    "short_content": "Streaming has revolutionized how we consume music. Platforms like Spotify and Apple Music dominate the market. Artists benefit from wider reach but face challenges with revenue. The music industry continues to adapt to this new era.",
                    "main_content": "Streaming has transformed the music industry, changing how we discover, listen to, and share music. Platforms like Spotify, Apple Music, and YouTube have become the primary way people consume music. Streaming offers convenience and accessibility, allowing users to listen to millions of songs on demand. For artists, streaming provides a global platform to reach a wider audience. However, the revenue model of streaming has been a point of contention, with many artists arguing that they are not fairly compensated. Despite these challenges, streaming has become the dominant form of music consumption, surpassing physical sales and digital downloads. The rise of playlists and algorithm-driven recommendations has also changed how music is promoted and discovered. Streaming has also led to the resurgence of older music, as listeners can easily access catalogs from past decades. The music industry continues to adapt to the streaming era, with new business models and strategies emerging. Live performances and merchandise have become important revenue streams for artists. The future of the music industry will likely be shaped by further advancements in technology and changes in consumer behavior. Streaming has democratized music, giving independent artists a platform to succeed without the need for major record labels. As the industry evolves, it will be interesting to see how streaming continues to shape the future of music."
                },
                {
                    "author_id": 3,
                    "category_id": categories.filter(name='Technology').first().id,
                    "images": ["posts/images/television_golden_1.jpg" , "posts/images/television_golden_2.jpg" , "posts/images/television_golden_3.jpg"],
                    "hero_image": "posts/hero_images/television_golden.jpg",
                    "title": "The Golden Age of Television",
                    "short_content": "Television has entered a golden age with high-quality content. Streaming services like Netflix and HBO produce critically acclaimed shows. Genres like drama, comedy, and sci-fi thrive. Binge-watching has become a cultural phenomenon.",
                    "main_content": "Television has undergone a renaissance in recent years, with the rise of high-quality content produced by streaming services like Netflix, HBO, and Amazon Prime. This era, often referred to as the Golden Age of Television, has seen the production of critically acclaimed shows across various genres. Dramas like 'Breaking Bad' and 'Game of Thrones' have set new standards for storytelling and production quality. Comedies like 'Fleabag' and 'The Marvelous Mrs. Maisel' have redefined the genre with their unique voices and complex characters. Science fiction and fantasy series, such as 'Stranger Things' and 'The Expanse,' have captivated audiences with their imaginative worlds and intricate plots. The availability of entire seasons at once has led to the rise of binge-watching, where viewers consume multiple episodes in one sitting. This shift in viewing habits has changed how shows are written and produced, with creators often crafting stories that are meant to be watched in quick succession. The Golden Age of Television has also seen an increase in diversity, with more representation of different cultures, genders, and sexual orientations. The competition among streaming services has led to an explosion of content, giving viewers more choices than ever before. As the industry continues to evolve, the Golden Age of Television shows no signs of slowing down, with new and innovative shows constantly pushing the boundaries of what television can achieve."
                },
                {
                    "author_id": 2,
                    "category_id": categories.filter(name='Books').first().id,
                    "images": ["posts/images/power_reading_1.jpg" , "posts/images/power_reading_2.jpg" , "posts/images/power_reading_3.jpg"],
                    "hero_image": "posts/hero_images/power_reading.jpg",
                    "title": "The Power of Reading: Why Books Matter",
                    "short_content": "Books have the power to educate, inspire, and entertain. Reading improves cognitive function and empathy. Genres like fiction, non-fiction, and poetry offer diverse experiences. Books remain a vital part of our culture.",
                    "main_content": "Books have been a cornerstone of human culture for centuries, offering a wealth of knowledge, inspiration, and entertainment. Reading has numerous benefits, including improving cognitive function, enhancing empathy, and reducing stress. Books come in various genres, each offering a unique experience. Fiction allows readers to immerse themselves in different worlds and perspectives, while non-fiction provides valuable insights into real-world issues and events. Poetry, with its lyrical language and emotional depth, offers a different kind of reading experience. Books have the power to educate, with many serving as important resources for learning and personal growth. They also have the ability to inspire, with stories of triumph, resilience, and creativity motivating readers to pursue their own goals. Reading is also a form of escapism, allowing people to temporarily leave behind their worries and immerse themselves in a good story. Despite the rise of digital media, books remain a vital part of our culture, with many people still preferring the tactile experience of holding a physical book. Libraries and bookstores continue to play an important role in promoting literacy and a love of reading. The future of books looks bright, with new authors and genres constantly emerging. Whether you're a lifelong reader or just starting out, books offer something for everyone, making them an enduring and valuable part of our lives."
                },
                {
                    "author_id": 3,
                    "category_id": categories.filter(name='Art').first().id,
                    "images": ["posts/images/contemporary_art_1.jpg" , "posts/images/contemporary_art_2.jpg" , "posts/images/contemporary_art_3.jpg"],
                    "hero_image": "posts/hero_images/contemporary_art.jpg",
                    "title": "The Renaissance of Contemporary Art",
                    "short_content": "Contemporary art is thriving with innovative works. Artists explore themes like identity, politics, and technology. Mediums range from painting to digital art. Art fairs and galleries showcase the best of modern creativity.",
                    "main_content": "Contemporary art refers to art produced in the present era, typically from the late 20th century to the present day. It is characterized by its diversity and innovation, with artists exploring a wide range of themes and mediums. Contemporary art often addresses issues like identity, politics, technology, and the environment. Artists use various mediums, including painting, sculpture, photography, and digital art, to express their ideas. The rise of digital technology has led to the emergence of new forms of art, such as virtual reality and interactive installations. Contemporary art is showcased in galleries, museums, and art fairs around the world. Events like the Venice Biennale and Art Basel attract artists, collectors, and enthusiasts from all over the globe. Contemporary art is not just about aesthetics; it also challenges viewers to think critically and engage with the world around them. The art market has also grown significantly, with contemporary works fetching high prices at auctions. Despite its popularity, contemporary art can be controversial, with some works sparking debates about what constitutes art. The future of contemporary art looks promising, with new artists and movements constantly emerging. Whether you're an art enthusiast or a casual observer, contemporary art offers a fascinating glimpse into the creative minds of today's artists."
                },
                {
                    "author_id": 2,
                    "category_id": categories.filter(name='Science').first().id,
                    "images": ["posts/images/space_exploration_1.jpg" , "posts/images/space_exploration_2.jpg" , "posts/images/space_exploration_3.jpg"],
                    "hero_image": "posts/hero_images/space_exploration.jpg",
                    "title": "The Wonders of Space Exploration",
                    "short_content": "Space exploration has expanded our understanding of the universe. Missions to Mars and beyond are pushing the boundaries of science. Technologies like telescopes and rovers are essential tools. The future of space exploration is full of possibilities.",
                    "main_content": "Space exploration has been one of the most significant scientific endeavors of the modern era. It has expanded our understanding of the universe and our place within it. Missions to the Moon, Mars, and beyond have provided valuable insights into the origins and evolution of our solar system. Space exploration has also led to the development of new technologies, such as telescopes, satellites, and rovers, which are essential tools for scientific research. The Hubble Space Telescope, for example, has captured stunning images of distant galaxies and nebulae, deepening our understanding of the cosmos. Rovers like Curiosity and Perseverance have explored the surface of Mars, searching for signs of past life and studying the planet's geology. Space exploration is not just about scientific discovery; it also inspires people to dream big and push the boundaries of what is possible. The future of space exploration is full of possibilities, with plans for manned missions to Mars, the establishment of lunar bases, and the search for extraterrestrial life. Private companies like SpaceX and Blue Origin are also playing a significant role in advancing space exploration. The challenges of space exploration are immense, but the potential rewards are even greater. As we continue to explore the cosmos, we are not only expanding our knowledge but also paving the way for future generations to reach new frontiers."
                },
                {
                    "author_id": 3,
                    "category_id": categories.filter(name='Business').first().id,
                    "images": ["posts/images/ecommerce_evolution_1.jpg" , "posts/images/ecommerce_evolution_2.jpg" , "posts/images/ecommerce_evolution_3.jpg"],
                    "hero_image": "posts/hero_images/ecommerce_evolution.jpg",
                    "title": "The Evolution of E-Commerce",
                    "short_content": "E-commerce has transformed the way we shop. Online platforms like Amazon and eBay dominate the market. Convenience and variety are key drivers. The future of e-commerce includes AI and personalized shopping experiences.",
                    "main_content": "E-commerce, or electronic commerce, refers to the buying and selling of goods and services over the internet. It has revolutionized the way we shop, offering convenience, variety, and competitive prices. Online platforms like Amazon, eBay, and Alibaba have become household names, dominating the e-commerce market. E-commerce has also enabled small businesses and entrepreneurs to reach a global audience, leveling the playing field with larger retailers. The rise of mobile commerce, or m-commerce, has further expanded the reach of e-commerce, allowing consumers to shop from their smartphones and tablets. E-commerce platforms use advanced technologies like artificial intelligence and machine learning to personalize the shopping experience, offering product recommendations and targeted ads. The future of e-commerce includes innovations like virtual reality shopping, where customers can explore virtual stores and try on clothes using augmented reality. E-commerce has also led to changes in supply chain management, with companies investing in automation and robotics to streamline operations. Despite its many benefits, e-commerce also poses challenges, such as cybersecurity risks and the environmental impact of packaging and shipping. As the e-commerce industry continues to evolve, it will be interesting to see how new technologies and consumer trends shape its future. E-commerce has transformed the retail landscape, and its impact will only continue to grow in the years to come."
                },
                {
                    "author_id": 2,
                    "category_id": categories.filter(name='Education').first().id,
                    "images": ["posts/images/lifelong_learning_1.jpg" , "posts/images/lifelong_learning_2.jpg" , "posts/images/lifelong_learning_3.jpg"],
                    "hero_image": "posts/hero_images/lifelong_learning.jpg",
                    "title": "The Importance of Lifelong Learning",
                    "short_content": "Lifelong learning is essential in a rapidly changing world. It helps individuals adapt to new challenges and opportunities. Online courses and certifications are popular options. Lifelong learning promotes personal and professional growth.",
                    "main_content": "Lifelong learning refers to the continuous pursuit of knowledge and skills throughout one's life. In a rapidly changing world, lifelong learning is essential for adapting to new challenges and opportunities. It helps individuals stay relevant in their careers, improve their personal lives, and contribute to society"
                },
                {
                    "author_id": 3,
                    "category_id": categories.filter(name='Culture').first().id,
                    "images": ["posts/images/exploring_japan_1.jpg" , "posts/images/exploring_japan_2.jpg" , "posts/images/exploring_japan_3.jpg"],
                    "hero_image": "posts/hero_images/exploring_japan.jpg",
                    "title": "Exploring the Wonders of Japan",
                    "short_content": "Japan is a land of contrasts, blending ancient traditions with modern marvels.\nFrom the cherry blossoms of Kyoto to the bustling streets of Tokyo, every corner has a story.\nThe country boasts breathtaking landscapes, from Mount Fuji to Okinawa’s beaches.\nIts unique cuisine, culture, and hospitality make it a top travel destination.",
                    "main_content": "Japan offers a mesmerizing blend of tradition and innovation. Cities like Tokyo and Osaka are technological hubs, while Kyoto and Nara preserve historical treasures. The food scene is another highlight, with sushi, ramen, and wagyu beef being global favorites. Transportation is seamless, thanks to the Shinkansen bullet train. Travelers can immerse themselves in Japan’s deep-rooted customs, from tea ceremonies to sumo wrestling. The country is also known for its stunning natural beauty, including cherry blossom festivals and the snow-covered peaks of Hokkaido. Temples and shrines, such as Fushimi Inari, provide a spiritual retreat. The disciplined and polite nature of Japanese people adds to the charm. Whether hiking in the Japanese Alps, shopping in Harajuku, or soaking in an onsen, Japan never disappoints. Festivals like Gion Matsuri and Tanabata bring vibrant celebrations. Japan’s futuristic technology can be seen in everything from high-tech toilets to humanoid robots. Tourists can enjoy themed cafes, from cat cafes to robot restaurants. Anime and manga culture also attract millions of fans worldwide. With its safe and efficient transport system, traveling around is hassle-free. A visit to Japan is an unforgettable journey through history, culture, and modernity."
                },
                {
                    "author_id": 2,
                    "category_id": categories.filter(name='Technology').first().id,
                    "images": ["posts/images/future_ai_1.jpg" , "posts/images/future_ai_2.jpg" , "posts/images/future_ai_3.jpg"],
                    "hero_image": "posts/hero_images/future_ai.jpg",
                    "title": "The Future of Artificial Intelligence",
                    "short_content": "AI is revolutionizing industries, from healthcare to finance and beyond.\nMachine learning and deep learning are making systems smarter and more efficient.\nEthical concerns and job displacement are major discussions in AI development.\nThe future promises advancements in autonomous systems and human-AI collaboration.",
                    "main_content": "Artificial Intelligence is reshaping our world at an unprecedented pace. From self-driving cars to virtual assistants like Siri and Alexa, AI is becoming integral to daily life. Healthcare is witnessing breakthroughs with AI-driven diagnostics and robotic surgeries. Financial institutions use AI for fraud detection and risk assessment. Businesses leverage AI for personalized marketing and customer engagement. Ethical considerations, such as bias in algorithms and data privacy, remain critical. Governments and organizations are working on regulations to ensure responsible AI usage. AI-powered automation is transforming the job market, necessitating upskilling for the workforce. Deep learning and neural networks are enabling machines to understand and predict complex patterns. In education, AI tutors provide personalized learning experiences. AI’s role in cybersecurity is expanding, with advanced threat detection systems. The gaming industry utilizes AI for intelligent NPCs and procedural content generation. In entertainment, AI-driven recommendation systems improve user experience. Robotics integrated with AI is enhancing industrial production and logistics. AI in climate science helps predict weather patterns and mitigate disasters. As AI evolves, its impact will continue to shape the future of humanity."
                },
                {
                    "author_id": 3,
                    "category_id": categories.filter(name='Food').first().id,
                    "images": ["posts/images/italian_pasta_1.jpg" , "posts/images/italian_pasta_2.jpg" , "posts/images/italian_pasta_3.jpg"],
                    "hero_image": "posts/hero_images/italian_pasta.jpg",
                    "title": "The Art of Making Italian Pasta",
                    "short_content": "Italian pasta is more than just food; it's a cultural tradition.\nFrom spaghetti to lasagna, each region has its own unique styles and flavors.\nHomemade pasta uses simple ingredients: flour, eggs, and a touch of olive oil.\nThe secret to perfect pasta lies in the sauce, whether it's creamy carbonara or tangy marinara.",
                    "main_content": "Italy’s love for pasta is deeply rooted in its history and culinary traditions. Each region boasts its own signature pasta dish, from Sicilian seafood pasta to Bologna’s famous tagliatelle al ragù. The art of making fresh pasta involves kneading dough, rolling it thin, and cutting it into different shapes. Traditional sauces like pesto, arrabbiata, and alfredo bring out the best flavors. Italian pasta is often paired with high-quality olive oil, fresh basil, and Parmesan cheese. Cooking pasta ‘al dente’ ensures a perfect bite. Ravioli and tortellini are popular stuffed pasta varieties, often filled with cheese, spinach, or meat. Pasta dishes are commonly served with a glass of Italian wine. Restaurants in Italy take pride in serving handmade pasta with locally sourced ingredients. Modern chefs experiment with fusion pasta dishes, blending global flavors. Pasta is a comfort food that unites families around the dinner table. Many believe that Marco Polo introduced pasta to Italy from China, though its origins remain debated. Pasta-making classes are a popular activity for tourists in Italy. Whether baked, boiled, or tossed in sauce, pasta remains a universal favorite. The joy of eating fresh Italian pasta is an experience that never gets old."
                },
                {
                    "author_id": 2,
                    "category_id": categories.filter(name='Fashion').first().id,
                    "images": ["posts/images/fashion_trends_1.jpg" , "posts/images/fashion_trends_2.jpg" , "posts/images/fashion_trends_3.jpg"],
                    "hero_image": "posts/hero_images/fashion_trends.jpg",
                    "title": "Fashion Trends in 2025",
                    "short_content": "Sustainable fashion is on the rise, with eco-friendly materials gaining popularity.\nBold colors and futuristic designs are dominating the runway this year.\nVintage fashion is making a comeback, especially styles from the ‘90s and 2000s.\nTech-integrated clothing, such as smart fabrics, is becoming the new norm.",
                    "main_content": "Fashion is constantly evolving, and 2025 is no different. Designers are embracing sustainability, using biodegradable fabrics and ethical production methods. Vintage aesthetics, including baggy jeans and oversized blazers, are returning. Streetwear continues to dominate, with sneaker culture influencing mainstream fashion. Athleisure is expanding, blending comfort with high-end style. Smart clothing with temperature regulation and biometric tracking is gaining traction. Brands are focusing on diversity, promoting inclusivity in their collections. Gender-neutral fashion is becoming widely accepted. The fusion of traditional and modern designs is evident in high-fashion collections. Bold prints, neon colors, and experimental silhouettes define the year’s trends. The resale market for luxury fashion is booming. Fast fashion brands are shifting towards sustainable production methods. Customization is in high demand, with brands offering personalized designs. Accessories like oversized sunglasses and chunky jewelry are making statements. The rise of digital fashion, including virtual outfits for the metaverse, is an emerging trend. As technology and fashion merge, the future of clothing looks more innovative than ever."
                },
                {
                    "author_id": 3,
                    "category_id": categories.filter(name='Travel').first().id,
                    "images": ["posts/images/world_wonders_1.jpg", "posts/images/world_wonders_2.jpg"  , "posts/images/world_wonders_3.jpg"],
                    "title": "Exploring the Wonders of the World",
                    "hero_image": "posts/hero_images/world_wonders.jpg",
                    "short_content": "Join us as we explore the most breathtaking wonders of the world. From ancient structures to natural marvels, these wonders will leave you in awe. Discover the history and significance behind each wonder. Get ready for an unforgettable journey.",
                    "main_content": "From the Great Wall of China to the Pyramids of Giza, the world is full of incredible wonders. In this post, we will take you on a journey to some of the most awe-inspiring places on Earth. The Great Wall of China, stretching over 13,000 miles, is a testament to human ingenuity and perseverance. The Pyramids of Giza, built over 4,500 years ago, continue to baffle historians and archaeologists with their precision and grandeur. The natural wonder of the Grand Canyon, carved by the Colorado River, showcases the raw power of nature. The majestic Machu Picchu, perched high in the Andes Mountains, offers a glimpse into the advanced engineering of the Inca civilization. Join us as we delve into the stories, legends, and mysteries surrounding these wonders and more.",
                },
                {
                    "author_id": 2,
                    "category_id": categories.filter(name='Technology').first().id,
                    "images": ["posts/images/future_technology_1.jpg" , "posts/images/future_technology_2.jpg" , "posts/images/future_technology_3.jpg"],
                    "hero_image": "posts/hero_images/future_technology.jpg",
                    "title": "The Future of Technology",
                    "short_content": "A look into the future of technology and its impact on our lives. From AI advancements to space exploration, technology is reshaping our world. Discover the latest trends and innovations. Learn how technology will influence various industries.",
                    "main_content": "Technology is evolving at a rapid pace, and it is transforming the way we live and work. In this post, we will explore the latest advancements in technology and what the future holds. Artificial Intelligence (AI) is making significant strides, with applications ranging from healthcare to autonomous vehicles. The Internet of Things (IoT) is connecting devices and creating smart environments. Blockchain technology is revolutionizing finance and supply chain management. Space exploration is reaching new heights with missions to Mars and beyond. Virtual Reality (VR) and Augmented Reality (AR) are changing the way we interact with digital content. Quantum computing promises to solve complex problems that are currently beyond our reach. Join us as we delve into these exciting developments and their potential impact on society.",
                },
                {
                    "author_id": 3,
                    "category_id": categories.filter(name='Food').first().id,
                    "images": ["posts/images/delicious_recipes_1.jpg" , "posts/images/delicious_recipes_2.jpg" , "posts/images/delicious_recipes_3.jpg"],
                    "hero_image": "posts/hero_images/delicious_recipes.jpg",
                    "title": "Delicious Recipes for Food Lovers",
                    "short_content": "Discover mouth-watering recipes that will delight your taste buds. From appetizers to desserts, we have something for everyone. Whether you are a seasoned chef or a beginner, these recipes are easy to follow. Get ready to impress your family and friends.",
                    "main_content": "Whether you are a seasoned chef or a beginner in the kitchen, these recipes are sure to impress. From appetizers to desserts, we have something for everyone. Start your meal with a refreshing Caprese salad, featuring ripe tomatoes, fresh mozzarella, and basil drizzled with balsamic glaze. For the main course, try our succulent roasted chicken with garlic and herbs, served with a side of creamy mashed potatoes. Indulge in a rich and decadent chocolate lava cake for dessert, with a gooey molten center that will satisfy any sweet tooth. Each recipe is carefully crafted with step-by-step instructions and tips to ensure success. Join us as we explore the world of culinary delights and elevate your cooking skills.",
                },
                {
                    "author_id": 2,
                    "category_id": categories.filter(name='Fashion').first().id,
                    "images": ["posts/images/latest_fashion_trends_1.jpg" , "posts/images/latest_fashion_trends_2.jpg" , "posts/images/latest_fashion_trends_3.jpg"],
                    "hero_image": "posts/hero_images/latest_fashion_trends.jpg",
                    "title": "The Latest Fashion Trends",
                    "short_content": "Stay up-to-date with the latest fashion trends and styles. From runway looks to street style, we cover it all. Learn how to incorporate these trends into your wardrobe. Discover tips and tricks from fashion experts.",
                    "main_content": "Fashion is constantly changing, and it can be hard to keep up with the latest trends. In this post, we will highlight the hottest styles and how you can incorporate them into your wardrobe. This season, bold colors and patterns are making a statement on the runway. Animal prints, neon hues, and oversized silhouettes are all the rage. Sustainable fashion is also gaining traction, with designers focusing on eco-friendly materials and ethical production practices. Accessories are playing a key role in elevating outfits, with statement jewelry, belts, and bags adding a touch of flair. We will also share tips on how to mix and match pieces to create versatile and stylish looks. Join us as we explore the world of fashion and help you stay ahead of the curve.",
                },
                {
                    "author_id": 3,
                    "category_id": categories.filter(name='Health').first().id,
                    "images": ["posts/images/healthy_lifestyle_1.jpg" , "posts/images/healthy_lifestyle_2.jpg" , "posts/images/healthy_lifestyle_3.jpg"],
                    "hero_image": "posts/hero_images/healthy_lifestyle.jpg",
                    "title": "Tips for a Healthy Lifestyle",
                    "short_content": "Learn how to live a healthier and happier life with these tips. From nutrition to exercise, we cover all aspects of wellness. Discover simple changes you can make to improve your health. Start your journey to a better you today.",
                    "main_content": "Living a healthy lifestyle is important for both your physical and mental well-being. In this post, we will share tips on how to eat healthy, stay active, and manage stress. A balanced diet rich in fruits, vegetables, whole grains, and lean proteins is essential for optimal health. Regular exercise, such as walking, jogging, or yoga, helps maintain a healthy weight and reduces the risk of chronic diseases. Managing stress through mindfulness practices, such as meditation and deep breathing, can improve mental clarity and emotional resilience. Getting enough sleep and staying hydrated are also crucial for overall well-being. Join us as we explore these tips and more to help you lead a healthier and happier life.",
                },
                {
                    "author_id": 2,
                    "category_id": categories.filter(name='Technology').first().id,
                    "images": ["posts/images/artificial_intelligence_in_health_care_1.jpg" , "posts/images/artificial_intelligence_in_health_care_2.jpg" , "posts/images/artificial_intelligence_in_health_care_3.jpg"],
                    "hero_image": "posts/hero_images/artificial_intelligence_in_health_care.jpg",
                    "title": "Artificial Intelligence in Healthcare",
                    "short_content": "AI is revolutionizing healthcare by improving diagnostics and treatment plans. Machine learning algorithms analyze medical data to predict diseases. AI-powered tools assist doctors in making faster and more accurate decisions. This technology is transforming patient care and reducing costs.",
                    "main_content": "Artificial Intelligence (AI) is making significant strides in the healthcare industry, offering innovative solutions to long-standing challenges. One of the most notable applications is in diagnostics, where AI algorithms can analyze medical images, such as X-rays and MRIs, with remarkable accuracy. These systems can detect anomalies like tumors or fractures faster than human doctors, enabling early intervention. AI is also being used to predict patient outcomes by analyzing vast amounts of data, including medical histories and genetic information. This helps in creating personalized treatment plans tailored to individual patients. Additionally, AI-powered chatbots and virtual assistants are improving patient engagement by providing 24/7 support and answering medical queries. In drug discovery, AI accelerates the process of identifying potential compounds, reducing the time and cost of developing new medications. Despite its benefits, challenges like data privacy and ethical concerns remain. However, as technology advances, AI is poised to become an indispensable tool in modern healthcare, enhancing both the quality and accessibility of medical services."
                },
                {
                    "author_id": 3,
                    "category_id": categories.filter(name='Technology').first().id,
                    "images": ["posts/images/quantum_computing_1.jpg" , "posts/images/quantum_computing_2.jpg" , "posts/images/quantum_computing_3.jpg"],
                    "hero_image": "posts/hero_images/quantum_computing.jpg",
                    "title": "The Rise of Quantum Computing",
                    "short_content": "Quantum computing promises to solve complex problems beyond the reach of classical computers. It leverages quantum bits (qubits) to perform calculations at unprecedented speeds. Industries like cryptography, finance, and logistics stand to benefit greatly. However, practical quantum computers are still in the experimental stage.",
                    "main_content": "Quantum computing is a groundbreaking technology that harnesses the principles of quantum mechanics to perform computations. Unlike classical computers, which use bits as the smallest unit of data (0 or 1), quantum computers use quantum bits or qubits, which can exist in multiple states simultaneously. This allows them to process vast amounts of information at incredible speeds. One of the most promising applications of quantum computing is in cryptography, where it could break traditional encryption methods and create ultra-secure communication systems. In finance, quantum algorithms can optimize trading strategies and risk management. Logistics companies can use quantum computing to solve complex optimization problems, such as route planning and supply chain management. Despite its potential, quantum computing faces significant challenges, including maintaining qubit stability and minimizing errors. Major tech companies like IBM, Google, and Microsoft are investing heavily in quantum research, with Google achieving 'quantum supremacy' in 2019. While practical quantum computers are still years away, the technology holds the promise of revolutionizing industries and solving problems that are currently intractable."
                },
                {
                    "author_id": 2,
                    "category_id": categories.filter(name='Technology').first().id,
                    "images": ["posts/images/5g_technology_1.jpg" , "posts/images/5g_technology_2.jpg" , "posts/images/5g_technology_3.jpg"],
                    "hero_image": "posts/hero_images/5g_technology.jpg",
                    "title": "5G Technology and Its Impact",
                    "short_content": "5G is the next generation of wireless technology, offering faster speeds and lower latency. It enables advancements in IoT, autonomous vehicles, and smart cities. With 5G, users can download large files in seconds and enjoy seamless streaming. However, concerns about infrastructure costs and health risks persist.",
                    "main_content": "5G technology represents a significant leap forward in wireless communication, offering speeds up to 100 times faster than 4G and latency as low as 1 millisecond. This enables real-time communication between devices, paving the way for innovations like the Internet of Things (IoT), where billions of connected devices can interact seamlessly. Autonomous vehicles, for example, rely on 5G for instant data exchange, ensuring safe and efficient navigation. Smart cities are another area where 5G can make a profound impact, enabling real-time monitoring of traffic, energy usage, and public safety. For consumers, 5G means faster downloads, smoother streaming, and enhanced virtual reality experiences. However, the rollout of 5G requires significant infrastructure investment, including the installation of small cells and fiber-optic cables. Additionally, there are ongoing debates about potential health risks associated with increased exposure to radiofrequency radiation. Despite these challenges, 5G is set to transform industries and everyday life, driving economic growth and technological innovation."
                },
                {
                    "author_id": 3,
                    "category_id": categories.filter(name='Technology').first().id,
                    "images": ["posts/images/blockchain_technology_1.jpg" , "posts/images/blockchain_technology_2.jpg" , "posts/images/blockchain_technology_3.jpg"],
                    "hero_image": "posts/hero_images/blockchain_technology.jpg",
                    "title": "Blockchain Beyond Cryptocurrency",
                    "short_content": "Blockchain technology is more than just the backbone of cryptocurrencies like Bitcoin. It offers secure, transparent, and decentralized solutions for various industries. Applications include supply chain management, voting systems, and digital identity verification. Blockchain is reshaping how data is stored and shared globally.",
                    "main_content": "Blockchain technology, originally developed for cryptocurrencies like Bitcoin, has evolved into a versatile tool with applications across multiple industries. At its core, blockchain is a decentralized ledger that records transactions in a secure and transparent manner. This makes it ideal for supply chain management, where it can track the movement of goods from origin to destination, ensuring authenticity and reducing fraud. In the financial sector, blockchain enables faster and cheaper cross-border payments by eliminating intermediaries. Governments are exploring blockchain for secure voting systems, which can enhance transparency and reduce the risk of tampering. Digital identity verification is another promising application, allowing individuals to control their personal data and share it securely with authorized parties. Blockchain also has potential in healthcare, where it can securely store and share patient records. Despite its advantages, challenges like scalability and energy consumption remain. Nevertheless, as the technology matures, blockchain is poised to revolutionize how data is stored, shared, and trusted in a digital world."
                },
                {
                    "author_id": 2,
                    "category_id": categories.filter(name='Technology').first().id,
                    "images": ["posts/images/autonomous_vehicles_1.jpg" , "posts/images/autonomous_vehicles_2.jpg" , "posts/images/autonomous_vehicles_3.jpg"],
                    "hero_image": "posts/hero_images/autonomous_vehicles.jpg",
                    "title": "The Future of Autonomous Vehicles",
                    "short_content": "Autonomous vehicles are set to transform transportation by reducing accidents and improving efficiency. These self-driving cars use AI, sensors, and cameras to navigate roads. Companies like Tesla, Waymo, and Uber are leading the charge in this technology. Regulatory and ethical challenges remain before widespread adoption.",
                    "main_content": "Autonomous vehicles, or self-driving cars, are one of the most anticipated technological advancements of the 21st century. These vehicles rely on a combination of artificial intelligence, sensors, cameras, and radar systems to navigate roads and make real-time decisions. The primary goal is to reduce human error, which is responsible for the majority of traffic accidents. Companies like Tesla, Waymo, and Uber are at the forefront of developing and testing autonomous vehicle technology. Tesla's Autopilot and Full Self-Driving features are already available in consumer vehicles, offering advanced driver-assistance capabilities. Waymo, a subsidiary of Alphabet, has launched fully autonomous taxi services in select cities. Beyond personal transportation, autonomous vehicles have the potential to revolutionize logistics and public transit, reducing costs and improving efficiency. However, significant challenges remain, including regulatory hurdles, ethical dilemmas, and public skepticism. Questions about liability in the event of an accident and the impact on jobs in the transportation industry are also critical concerns. Despite these obstacles, the future of autonomous vehicles looks promising, with the potential to create safer, more efficient, and environmentally friendly transportation systems."
                },
                {
                    "author_id": 3,
                    "category_id": categories.filter(name='Culture').first().id,
                    "images": ["posts/images/k_pop_influence_1.jpg" , "posts/images/k_pop_influence_2.jpg" , "posts/images/k_pop_influence_3.jpg"],
                    "hero_image": "posts/hero_images/k_pop_influence.jpg",
                    "title": "The Global Influence of K-Pop",
                    "short_content": "K-Pop has become a global phenomenon, transcending language and cultural barriers. Groups like BTS and BLACKPINK have amassed millions of fans worldwide. The genre blends catchy music, intricate choreography, and vibrant visuals. K-Pop is reshaping the global music industry and promoting Korean culture.",
                    "main_content": "K-Pop, or Korean Pop music, has taken the world by storm, becoming a cultural force that transcends borders. Groups like BTS and BLACKPINK have achieved unprecedented success, topping global charts and selling out stadiums worldwide. What sets K-Pop apart is its unique blend of catchy melodies, high-energy choreography, and visually stunning music videos. The genre is not just about music; it’s a cultural movement that includes fashion, beauty, and lifestyle. Social media platforms like YouTube and Twitter have played a crucial role in spreading K-Pop’s influence, allowing fans to connect and share content globally. Beyond entertainment, K-Pop has become a powerful tool for promoting Korean culture, known as the 'Korean Wave' or Hallyu. This has led to increased interest in Korean language, food, and traditions. However, the industry also faces criticism for its rigorous training systems and the pressure placed on artists. Despite these challenges, K-Pop continues to grow, proving that music can be a universal language that brings people together."
                },
                {
                    "author_id": 2,
                    "category_id": categories.filter(name='Culture').first().id,
                    "images": ["posts/images/indigenous_art_1.jpg" , "posts/images/indigenous_art_2.jpg" , "posts/images/indigenous_art_3.jpg"],
                    "hero_image": "posts/hero_images/indigenous_art.jpg",
                    "title": "The Renaissance of Indigenous Art",
                    "short_content": "Indigenous art is experiencing a renaissance, with growing recognition and appreciation worldwide. Artists are blending traditional techniques with modern styles to tell their stories. This movement is helping to preserve cultural heritage and raise awareness about Indigenous issues. Galleries and museums are increasingly showcasing these works.",
                    "main_content": "Indigenous art is undergoing a significant revival, gaining recognition and respect on the global stage. This renaissance is driven by artists who are blending traditional methods with contemporary styles to create powerful works that tell their communities' stories. From intricate beadwork and weaving to bold paintings and sculptures, Indigenous art is diverse and deeply rooted in cultural heritage. This movement is not just about aesthetics; it’s a form of activism that raises awareness about Indigenous rights, land preservation, and historical injustices. Institutions like the National Museum of the American Indian and the Australian Aboriginal Art Gallery are playing a crucial role in showcasing these works. Additionally, social media platforms have provided Indigenous artists with a space to share their creations with a broader audience. The growing interest in Indigenous art is also fostering economic opportunities for communities, as collectors and enthusiasts seek authentic pieces. By celebrating Indigenous art, society is taking a step toward acknowledging and honoring the rich cultural contributions of Indigenous peoples."
                },
                {
                    "author_id": 3,
                    "category_id": categories.filter(name='Culture').first().id,
                    "images": ["posts/images/street_food_culture_1.jpg" , "posts/images/street_food_culture_2.jpg" , "posts/images/street_food_culture_3.jpg"],
                    "hero_image": "posts/hero_images/street_food_culture.jpg",
                    "title": "The Evolution of Street Food Culture",
                    "short_content": "Street food has evolved from a cheap, quick meal option to a culinary phenomenon. Cities around the world are known for their unique street food offerings, from tacos in Mexico City to satay in Bangkok. Food trucks and festivals have popularized street food globally. This trend reflects a growing appreciation for diverse and authentic flavors.",
                    "main_content": "Street food culture has undergone a remarkable transformation, becoming a celebrated aspect of global cuisine. What was once considered a humble, quick meal option is now a culinary trend embraced by food enthusiasts worldwide. Cities like Mexico City, Bangkok, and Istanbul are renowned for their vibrant street food scenes, offering dishes that are deeply rooted in local traditions. Tacos, satay, kebabs, and banh mi are just a few examples of street foods that have gained international fame. The rise of food trucks and street food festivals has further popularized this trend, bringing diverse flavors to urban centers around the globe. Street food is not just about affordability; it’s a way to experience authentic, regional cuisines that are often passed down through generations. This evolution reflects a broader cultural shift toward valuing diversity and authenticity in food. Additionally, street food vendors are increasingly recognized for their entrepreneurial spirit and creativity. As the world becomes more interconnected, street food culture continues to thrive, offering a delicious glimpse into the heart of different communities."
                },
                {
                    "author_id": 2,
                    "category_id": categories.filter(name='Culture').first().id,
                    "images": ["posts/images/streaming_impact_1.jpg" , "posts/images/streaming_impact_2.jpg" , "posts/images/streaming_impact_3.jpg"],
                    "hero_image": "posts/hero_images/streaming_impact.jpg",
                    "title": "The Impact of Streaming on Film and TV Culture",
                    "short_content": "Streaming platforms like Netflix, Hulu, and Disney+ have revolutionized how we consume media. They offer a vast library of content, from blockbuster movies to niche indie films. Binge-watching has become a cultural norm, changing storytelling techniques. Streaming is also giving rise to diverse voices and global stories.",
                    "main_content": "The rise of streaming platforms has fundamentally transformed film and TV culture, reshaping how content is created, distributed, and consumed. Services like Netflix, Hulu, and Disney+ offer an unprecedented variety of programming, from Hollywood blockbusters to independent films and international series. This accessibility has made binge-watching a cultural norm, influencing storytelling techniques to favor serialized narratives and cliffhangers. Streaming has also democratized content creation, providing a platform for diverse voices and stories that might not have found a place in traditional media. For example, shows like 'Money Heist' from Spain and 'Squid Game' from South Korea have achieved global success, highlighting the appeal of non-English content. Additionally, streaming platforms are investing heavily in original programming, challenging the dominance of traditional studios. However, this shift has also raised concerns about the sustainability of the film industry, with debates over fair compensation for creators and the impact on movie theaters. Despite these challenges, streaming continues to dominate the entertainment landscape, offering viewers more choices and fostering a more inclusive media environment."
                }
            ]
            for post_data in posts_data:
                post = Post.objects.create(
                    author_id=post_data["author_id"],
                    category_id=post_data["category_id"],
                    title=post_data["title"],
                    hero_image=post_data["hero_image"],
                    short_content=post_data["short_content"],
                    main_content=post_data["main_content"]
                )
                self.stdout.write(self.style.SUCCESS(f"Successfully created post '{post.title}'"))
                for image_path in post_data["images"]:
                    post.images.create(image=image_path)
                    self.stdout.write(self.style.SUCCESS(f"Successfully added image '{image_path}' to post '{post.title}'"))

        except Exception as e:
            raise CommandError(f"Error: {e}")


