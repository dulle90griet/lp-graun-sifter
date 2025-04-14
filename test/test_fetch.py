from unittest.mock import Mock, patch
import pytest
import requests
import os

from src.lp_graun_sifter.fetch import fetch


@pytest.fixture
def sample_response():
    return {
        "response": {
            "status": "ok",
            "userTier": "developer",
            "total": 10,
            "startIndex": 1,
            "pageSize": 10,
            "currentPage": 1,
            "pages": 1,
            "orderBy": "newest",
            "results": [
                {
                    "id": "artanddesign/2025/mar/30/ken-grant-welsh-valleys-cwm-a-fair-country-photography",
                    "type": "article",
                    "sectionId": "artanddesign",
                    "sectionName": "Art and design",
                    "webPublicationDate": "2025-03-30T09:00:15Z",
                    "webTitle": "‘People have walked through here for centuries’: the rhythms of the Welsh valleys in pictures",
                    "webUrl": "https://www.theguardian.com/artanddesign/2025/mar/30/ken-grant-welsh-valleys-cwm-a-fair-country-photography",
                    "apiUrl": "https://content.guardianapis.com/artanddesign/2025/mar/30/ken-grant-welsh-valleys-cwm-a-fair-country-photography",
                    "fields": {
                        "body": "<p>Ken Grant’s <em>Cwm: A Fair Country</em>, a collection of nearly 30 years of landscape photography in the South Walian valleys, begins with a moving prologue. It mentions a painting he’s known since his Liverpudlian childhood, still sitting above his 92-year-old father’s mantelpiece: “Dapple-bruised Welsh horses, painted in a loose herd, are imagined beneath a sky that promises rain.”</p> <p>From 1998, on commutes from Liverpool to the University of Wales, Newport (where he led a documentary photography degree), he noticed similar horses – completely by coincidence. “I didn’t seek them out at first, but on my drives, I soon got aware that they were there. Sometimes up a valley’s road, you’d see packs of 40 or 50.”</p>  <aside class=\"element element-pullquote element--supporting\"> <blockquote> <p>You’re rewarded by staying with subjects over time, seeing any kinds of changes or shifts, slow dismantlings or initiations</p> </blockquote> </aside>  <p>Some were descendants of animals once used in mining; other herds would have pre-dated industry; either way, they now roam wild and free. Grant’s horses sit, lie, nuzzle each other and look directly into his lens. He became struck by the creatures’ hardiness in all seasons. “They’re beautiful, observant, built to last – they let things happen around them. They became a loose metaphor for me for thinking about communities in these areas – communities built around a particular purpose which is not active any more in any shape or form, but which carries on, having endured all those upheavals, and the shifts that have taken place in the land.”</p>    <p>The horses in Cwm (the name of a mining village Grant photographs and a Welsh word for valley or steep-sided hollow at the head of a valley) act like solid anchors among images of striking environments. Harsh hills, often pillaged by industry, sit behind pale, pastel rows of terrace houses. A photography studio sits in an old building, its front wall soaked with stormwater. An old playground sits quietly alongside the site of a demolished steelworks.</p> <p>There are signs of development – new redbrick houses and road improvement projects – between the battered allotments and ruined buildings. “It struck me how strongly these roads are built to take people past a place,” Grant says. Moving on from Newport in 2013, he has to-and-froed between Wales and Liverpool ever since, often returning to the same places – like the village of Beaufort, named after a duke who originally owned the land, and Manmoel Common outside Ebbw Vale, high on a ridge, near abandoned quarries.</p>    <p>Mid-century Czech photographer Josef Sudek inspired this approach. “There’s a lovely phrase of his – ‘rush slowly’ – about how you’re rewarded by staying with subjects over time, seeing any kinds of changes or shifts, or slow dismantlings or initiations. You’re made aware that something’s still happening, or you’re reminded to find something again.” Other influences include the American photojournalists W Eugene Smith and Robert Frank, and people closer to his experience in Wales, such as West Wales-based photographer Paul Cabuts and photographic historian Ian Walker.</p> <p>The book’s subtitle is a nod to Alexander Cordell’s bestselling 1959 novel <em>Rape </em><em>of </em><em>the Fair Country</em>, about the iron-making communities of Nantyglo and Blaenavon before the Chartist uprisings in Wales. Best known as a photographer of people within places (in series such as <a href=\"https://www.ken-grant.info/new-brighton-revisited\">New Brighton Revisited</a> and <a href=\"https://www.ken-grant.info/shankly\">Shankly</a>), Grant talks warmly about those he has met in these communities (“there is a beautiful temperament and decency in these people”). He’s also done a project simultaneously in the area about pub football teams (“It’s as much about football as it is about men navigating being part of something that their dads were part of”).</p>    <p>The only people we see in <em>Cwm</em> are walkers, on the edges of frames, often in startling landscapes. “People use and walk through these places just because they’ve walked through them for centuries,” Grant says. He also loves the vivid colours of the land, the saturated browns, yellows and greens that partly come from the wetness of the Welsh weather. This resilience and richness, he says, is part of everyday life.</p> <p>“I’ve got a lot to be thankful for in Wales,” he adds. He’s now living back in Wirral, near his father, but his daughter lives in Cardiff, so he still has a reason to take strange, cross-country diversions. “The beautiful, gentle landscapes and full-blown mountains in which people still live – it’s still incredible, even in the winter, when it’s quite tough. But in the time of year we’re in now, I love watching how everything comes alive.” <em>Cwm</em> speaks to the same, startling spirit.</p> <p>• <em><a href=\"https://rrbphotobooks.com/products/0201007007601\">Cwm: A Fair Country</a></em> by Ken Grant is published by RRB Photobooks (£45)</p>"
                    },
                    "isHosted": False,
                    "pillarId": "pillar/arts",
                    "pillarName": "Arts"
                },
                {
                    "id": "artanddesign/2025/feb/12/rijksmuseum-amsterdam-american-photography",
                    "type": "article",
                    "sectionId": "artanddesign",
                    "sectionName": "Art and design",
                    "webPublicationDate": "2025-02-12T13:19:55Z",
                    "webTitle": "American Photography: unforgettable images of the beauty and brutality of a nation ",
                    "webUrl": "https://www.theguardian.com/artanddesign/2025/feb/12/rijksmuseum-amsterdam-american-photography",
                    "apiUrl": "https://content.guardianapis.com/artanddesign/2025/feb/12/rijksmuseum-amsterdam-american-photography",
                    "fields": {
                        "body": "<p>As the land of the free and the home of the brave reverberates to cries of Make America Great Again, what is often overlooked is the complicated notion of the word “again”. As highlighted in American Photography, an expansive, sometimes beautiful but often shocking survey at the Rijksmuseum in Amsterdam over the past two centuries, what has been great for some has been downright awful for others.</p>    <p>“America and photography are entwined. You can’t see the two apart from each other,” says Mattie Boom, curator of photographs at the Rijksmuseum, who has spent two decades helping build the American collection. It now amounts to around 7,000 photographs – all by American photographers of American subjects – and 1,500 American photobooks and magazines. The current exhibition is the first major survey of the field to be staged in Europe, and is a triumphant swansong for Boom as she retires from her post.</p> <p>There is no hierarchy to the selection. A sequence of rooms present numerous fields – portraiture, landscape, advertising work, art photography – like chapters in a novel. “We tried to find surprising images and things we’ve never seen before,” says Boom. The result is a broad mix, shaped with co-curator Hans Rooseboom, of anonymous photography, commercial work, news coverage, medical prints and propaganda, presented in tandem with masterpieces such as Robert Frank’s enigmatic picture of a woman watching a New Jersey parade in 1955, her face partially obscured by an unfurled Stars and Stripes.</p> <p>Photography proved to be the perfect medium for the new world: fast, largely democratic in its availability (if not its dissemination) and cheap. At the Rijksmuseum, two 19th-century daguerreotypes hint at the fractures to come. The first is one of the oldest known American photographs: a tiny 1840 self-portrait of Henry Fitz Jr, a pioneer photographer from Long Island. He captures himself with his eyes closed. Another plate, taken seven years later in the studio of Thomas M Easterly, an accomplished daguerreotypist in St Louis, pictures <a href=\"https://iowahistoryjournal.com/chief-keokuk-man-of-peace-in-an-age-of-war/\">Chief Keokuk </a>– also known as Watchful Fox – leader of the Sac and Fox people. It humanises the Native American chief – his face is astoundingly sharp – while also viewing him as a novelty.</p>    <p>Signs of racism – and its opposition – ripple through the galleries, as images of segregation and plantations give way to documentary photographs of the civil rights movement. A <em>carte de visite</em> studio portrait taken in the 1860s shows a semi-naked Black man scarred from multiple floggings, a horrible picture used to positive ends in a campaign for the abolition of slavery. Nearly a century later, in 1957, Jack Jenkins pictured Black student <a href=\"https://www.theguardian.com/world/2017/sep/24/little-rock-arkansas-school-segregation-racism\">Elizabeth Eckford arriving at the newly integrated Little Rock Central High School</a> to a jeering mob of white women. The photograph’s power lies in Eckford’s extraordinary composure in the face of such hatred.</p> <p>The epic grandeur of the American landscape is largely absent from the walls – with the exception of a majestic albumen print of <a href=\"https://www.theguardian.com/artanddesign/photography-blog/2014/nov/04/carleton-watkins-yosemite-photography-america\">Cathedral Rocks, Yosemite, taken by Carleton E Watkins</a> in 1861. Instead photographs show the conquest of nature and its bounty: Margaret Bourke-White’s widescreen shots of wheat plains; postcards of oil wells in Oklahoma. Meanwhile, in the monochrome street photography of <a href=\"https://www.theguardian.com/artanddesign/2024/feb/04/photographer-saul-leiter-an-unfinished-world-mk-gallery-milton-keynes-retrospective-the-everyday-new-york-sublime\">Saul Leiter</a> and <a href=\"https://www.theguardian.com/culture/william-klein\">William Klein</a>, we discover the ragged beauty of American cities, both its bustling sidewalks and lonesome figures, its cinemas and storefronts.</p>    <p>And, naturally, American photography sold stuff – Tupperware, confectionery, toboggans, razor blades, station wagons and, of course, Coca-Cola – in peppy, sometimes surreal, advertising campaigns. One early example at the Rijksmuseum is a small late-19th-century photo-card promoting a Manhattan butcher, in which a moustachioed merchant stabs his tenderloin cuts alongside some out-of-control alliterative copy: “Finest Flesh, Fattest Fowl, Freshest Fish, Furnished.”</p> <p>During the 1930s, many avant garde photographers fled Europe for the US, energising the medium in their adoptive nation. An aerial view of tire tracks in a snowy Chicago car park, taken by Hungarian émigré <a href=\"https://www.theguardian.com/artanddesign/2006/mar/18/art.modernism\">László Moholy-Nagy</a> in 1937, is indicative of these fresh perspectives. And photographers with an edge became highly sought after in postwar America, as full-throttle capitalism accelerated its development. Companies tried ever more eye-catching ways to attract customers and the gaudy palette of shop windows and flickering neon can be found reflected in the colour-saturated covers of Playboy and Time.</p>    <p>Perhaps the strongest sell was to keep America American. During the second world war, photographic posters, featuring the all-American eagle in flight, called on patriots to enlist in the civil defence. Another used Walker Evans’s photographs of small-town life to extol the virtues of a nation “where, through free enterprise, a free people have carved a great nation out of a wilderness. This is <em>your</em> America.” The <em>your </em>was conditional.</p> <p>The ghosts of conflict also materialise in two poignant portraits: an 1865 study of a civil war major, with a colossal bullet wound through his abdomen but still standing tall in his uniform; the other, a record of the 2006 wedding day of a badly injured Gulf war soldier. </p> <p>The Rijksmuseum presents some eccentric mini-collections within its American holdings. A mixed group of photographs – each annotated with the word “Me” to indicate where the various owners are situated in the frame – was one of several boxes donated to the Rijksmuseum by a New York collector of amateur snapshots. “He has sorted them out by category,” Boom says. “There’s a box called ‘Views from the car’. ‘Ladies by televisions’ is another category. He has a whole wall of these boxes in a little room and he gives donations to museums.”</p> <p>But the most mysterious pictures on view are a pair of monumental cyanotypes of human torsos, discovered in the mid-1990s at the 26th Street flea market in Manhattan, objects with a shady past worthy of a true-crime podcast. These 1930s positives were printed from X-ray negatives of cross-sectioned frozen cadavers as part of a university study in Chicago. Recent research has uncovered that the subjects were largely Black Chicagoans – who endured a death rate twice that of their white neighbours – and that the bodies were used in an institution that didn’t accept Black medical students. The exhibition illustrates photography’s power both to illuminate and obfuscate.</p>    <p>Boom equates 20th-century American photography with Dutch golden age painting. Both, she points out, were created “for citizens, by citizens and bought by people all over.” But is this a particularly European edit of an imperfect American dream? Boom shrugs. It would, she acknowledges, probably be more reverent if it were staged in the US, where celebratory monographic shows dominate. “For them the big names – <a href=\"https://www.theguardian.com/artanddesign/2010/aug/18/edward-weston-photography\">Edward Weston</a>, <a href=\"https://www.theguardian.com/artanddesign/gallery/2015/dec/03/walker-evans-documentary-photography-great-depression-gallery\">Walker Evans</a>, <a href=\"https://www.theguardian.com/artanddesign/2019/sep/11/robert-frank-the-americans-outsider-genius-photography\">Robert Frank</a>, <a href=\"https://www.theguardian.com/artanddesign/2023/apr/27/richard-avedon-photos-ny-exhibit\">Richard Avedon</a> – they are part of the history of the country, they are part of the image culture of the country, and for them these names are the same as Rembrandt and Vermeer for us Dutch.”</p> <p>In its subjective way – a different selection would tell a different story – the exhibition looks at American life in the round, with trauma and contradictions adjacent to glamour and enterprise. “It’s full of the force of photography, so it doesn’t leave things out,” says Boom. “America has always been 10 years ahead of Europe with photography and it still is.” It is one area in which – incontrovertibly and tellingly – America has always been great.</p> <ul> <li><p><a href=\"https://www.rijksmuseum.nl/nl?gad_source=1&amp;gclid=CjwKCAiAh6y9BhBREiwApBLHC0L__-232t_-Mvwx-tIwOYYiA3y0Y4uTHUxQT9u2SkdI6ScTlr59lRoCU_MQAvD_BwE\">American Photography is at the Rijksmuseum, Amsterdam, until 9 June</a></p></li> </ul>"
                    },
                    "isHosted": False,
                    "pillarId": "pillar/arts",
                    "pillarName": "Arts"
                },
                {
                    "id": "artanddesign/2023/nov/26/the-big-picture-brian-graham-robert-frank-raoul-hague-goin-down-the-road",
                    "type": "article",
                    "sectionId": "artanddesign",
                    "sectionName": "Art and design",
                    "webPublicationDate": "2023-11-26T07:00:12Z",
                    "webTitle": "The big picture: artists Robert Frank, Raoul Hague and a lost bohemia",
                    "webUrl": "https://www.theguardian.com/artanddesign/2023/nov/26/the-big-picture-brian-graham-robert-frank-raoul-hague-goin-down-the-road",
                    "apiUrl": "https://content.guardianapis.com/artanddesign/2023/nov/26/the-big-picture-brian-graham-robert-frank-raoul-hague-goin-down-the-road",
                    "fields": {
                        "body": "<p>Brian Graham took this picture of two artists – Raoul Hague and Robert Frank – at Hague’s cabin on Old Maverick Road in Woodstock, New York, in 1988. Hague, an abstract sculptor working mainly in wood, was a friend and mentor to Frank, whose 1958 coast to coast journey, <em>The Americans</em>, had been a landmark in documentary photography. The picture is included in Graham’s new book, <em>Goin’ Down the Road </em><em>With Robert Frank</em>, about the photographer. Frank <a href=\"xhttps://www.theguardian.com/artanddesign/2019/sep/11/robert-frank-the-americans-outsider-genius-photography\">died in 2019 aged 94</a>.</p> <p>Graham’s memoir is a personal homage to Frank’s influence and an intimate pictorial history of his later years. Graham met the older photographer in the late 1970s when he had spent a couple of years working on oil rigs and was looking for a change of life. Frank bought him a camera and some film and subsequently worked with him for a decade “in and out of the darkroom”.</p> <p>Frank divided those years between a ramshackle home on Bleecker Street in New York and a house on Cape Breton Island, Nova Scotia, in Graham’s native Canada.</p> <p>Both places look a little like lost worlds through Graham’s lens: dusty and beaten-up rooms and yards in which Frank’s wild-haired friends from different bohemias, Allen Ginsberg and Tom Waits and Jim Jarmusch, come and go. Hague’s cabin feels emblematic of that spirit, eccentric and homebuilt and full of life. In a diary note in the book, Graham recalls visits to that cabin, remembering how Hague described to him walking home 13 miles in the winter from the public libraries where he went to read. “Raoul kept scrapbooks and enjoyed showing me pictures of snow storms taken around the time he returned home from bypass surgery,” he wrote. “Back in New York, I imagine Hague forever in a snow globe.”</p> <ul> <li><p><em><a href=\"https://steidl.de/Books/Goin-Down-the-Road-with-Robert-Frank-1337405057.html\">Goin’ Down the Road </a></em><em><a href=\"https://steidl.de/Books/Goin-Down-the-Road-with-Robert-Frank-1337405057.html\">With Robert Frank</a></em> is published by Steidl</p></li> </ul>"
                    },
                    "isHosted": False,
                    "pillarId": "pillar/arts",
                    "pillarName": "Arts"
                }
            ]
        }
    }


@pytest.fixture
def requests_get_patcher(sample_response):
    response_mock = Mock()
    response_mock.json.return_value = sample_response
    patcher = patch("src.lp_graun_sifter.fetch.requests.get", return_value = response_mock)
    patcher.start()
    yield patcher
    patcher.stop()


@pytest.fixture
def test_api_key():
    saved_key = os.environ['GRAUN_API_KEY']
    os.environ['GRAUN_API_KEY'] = "test"
    yield
    os.environ['GRAUN_API_KEY'] = saved_key


def test_query_string_well_formed(test_api_key):
    requests_get_spy = Mock(wraps=requests.get)
    with patch(
        "src.lp_graun_sifter.fetch.requests.get",
        side_effect=requests_get_spy
    ):
        fetch("\"debussy on ice\"")
        formed_query = requests_get_spy.call_args.args[0]
        assert formed_query == "https://content.guardianapis.com/search?q=\"debussy on ice\"&show-fields=body&api-key=test"

        fetch("\"pinwheel cantata\"", date_from="2025-04-01")
        formed_query = requests_get_spy.call_args.args[0]
        assert formed_query == "https://content.guardianapis.com/search?from-date=2025-04-01&q=\"pinwheel cantata\"&show-fields=body&api-key=test"


def test_required_fields_appear_expected_num_of_times_in_fetched_data(requests_get_patcher):
    str_of_return = str(fetch("test_search"))
    assert str_of_return.count("webPublicationDate") == 3
    assert str_of_return.count("webTitle") == 3
    assert str_of_return.count("webUrl") == 3
    assert str_of_return.count("contentPreview") == 3


def test_fetch_returns_list_of_dicts_containing_only_expected_fields(requests_get_patcher):
    fetched_json = fetch("a_search_string")
    assert isinstance(fetched_json, list)
    for result in fetched_json:
        assert isinstance(result, dict)
        keys = result.keys()
        assert len(keys) == 4
        assert "webPublicationDate" in keys
        assert "webTitle" in keys
        assert "webUrl" in keys
        assert "contentPreview" in keys


def test_content_previews_of_expected_length(requests_get_patcher):
    fetched_json = fetch("test meridian")
    for result in fetched_json:
        assert 0 < len(result['contentPreview']) <= 1000


# def test_raises_error_on_timeout(sample_response):

