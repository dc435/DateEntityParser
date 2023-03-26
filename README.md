## DateEntityParser

A wrapper for the dateutil parser (https://github.com/dateutil/dateutil/), built specifically to parse longer Date Entity strings extracted using Named Entity Recognition (NER) tools, such as in SpaCy. Also utilizing the pyparsing library (https://github.com/pyparsing/pyparsing).

## Benefits

The code wraps dateutil parser, so it captures all the parsing power of that library. It adds the following functionality.

### *Parses longer date strings*
This module parses out longer 'date entity' strings which are commonly returned by Named Entity Recognisers, such as the SpaCy NER functions. These include phrases such as:

'the first week of March 1958' -> March 1958

'the final days of June 1961' -> June 1961

### *Extracts 'early' / 'mid' / 'late' emphasise*
The module identifies timing prefixes such as 'early' in 'early July 2021'. It sets the default date accordingly, so the resultant parsed date will be sorted earlier than 'late July 2021', for example:

'early July 2021' -> (1) July 2021

'late July 2021'  -> (31) July 2021

### *Identifies DMY, MY, Y date formats*
The module identifies whether the original string includes Day, Month and/or Year information.
This allows the output to be formatted accordingly, for example:

'in early 2015'    -> DateFormat.Y

'15 December 1998; -> DateFormat.DMY

## Example - The Beatles Timeline

(See **example.py** for workings):

**Input text:**

*"In the last weeks of 1956, John Lennon formed a skiffle group with several friends from Quarry Bank High School in Liverpool. They briefly called themselves the Blackjacks, before changing their name to the Quarrymen after discovering that another local group were already using the name. Paul McCartney met Lennon on 6 July 1957, and joined as a rhythm guitarist shortly after. In February 1958, McCartney invited his friend George Harrison to watch the band. Harrison auditioned for Lennon, impressing him with his playing, but Lennon initially thought Harrison was too young. In the first week of March 1958 during a second meeting (arranged by McCartney), Harrison performed the lead guitar part of the instrumental song "Raunchy" on the upper deck of a Liverpool bus, and they enlisted him as lead guitarist.
By early January 1959, Lennon's Quarry Bank friends had left the group, and he began his studies at the Liverpool College of Art. The three guitarists, billing themselves as Johnny and the Moondogs, were playing rock and roll whenever they could find a drummer. Lennon's art school friend Stuart Sutcliffe, who had just sold one of his paintings and was persuaded to purchase a bass guitar with the proceeds, joined prior to January 1960. He suggested changing the band's name to Beatals, as a tribute to Buddy Holly and the Crickets. They used this name during May 1958, when they became the Silver Beetles, before undertaking a brief tour of Scotland as the backing group for pop singer and fellow Liverpudlian Johnny Gentle. By early July 1960, they had refashioned themselves as the Silver Beatles, and by the middle of August 1960, simply the Beatles.
Allan Williams, the Beatles' unofficial manager, arranged a residency for them in Hamburg. They auditioned and hired drummer Pete Best in mid-August 1960. The band, now a five-piece, departed Liverpool for Hamburg, contracted to club owner Bruno Koschmider for a residency. Beatles historian Mark Lewisohn writes: "They pulled into Hamburg at dusk on 17 August 1959, the time when the red-light area comes to life ... flashing neon lights screamed out the various entertainment on offer, while scantily clad women sat unabashed in shop windows waiting for business opportunities."
Koschmider had converted a couple of strip clubs in the district into music venues, and he initially placed the Beatles at the Indra Club. After closing Indra due to noise complaints, he moved them to the Kaiserkeller. When he learned they had been performing at the rival Top Ten Club in breach of their contract, he gave them a termination notice, and reported the underage Harrison, who had obtained permission to stay in Hamburg by lying to the German authorities about his age. The authorities arranged for Harrison's deportation in late Nov 1960. In late-August 1960, Koschmider had McCartney and Best arrested for arson after they set fire to a condom in a concrete corridor; the authorities deported them. Lennon returned to Liverpool at the beginning of December 1960, while Sutcliffe remained in Hamburg until around the end of February 1961 with his German fiancée Astrid Kirchherr, who took the first semi-professional photos of the Beatles over a period of about four weeks.
During the period from 1961 to 1962, the Beatles were resident for periods in Hamburg, where they used Preludin both recreationally and to maintain their energy through all-night performances. In about mid-1961, during their second Hamburg engagement, Kirchherr cut Sutcliffe's hair in the "exi" (existentialist) style, later adopted by the other Beatles. Later on, Sutcliffe decided to leave the band and resume his art studies in Germany. McCartney took over bass. Producer Bert Kaempfert contracted what was now a four-piece group until June 1962, and he used them as Tony Sheridan's backing band on a series of recordings for Polydor Records. As part of the sessions, the Beatles were signed to Polydor. Credited to "Tony Sheridan & the Beat Brothers", the single "My Bonnie", recorded in the final days of June 1961 and released in mid-late Oct 1961, reached number 32 on the Musikmarkt chart.
About six months later, after the Beatles completed their second Hamburg residency, they enjoyed increasing popularity in Liverpool with the growing Merseybeat movement. However, they were growing tired of the monotony of numerous appearances at the same clubs night after night. In the tax year ending November 1961, during one of the group's frequent performances at the Cavern Club, they encountered Brian Epstein, a local record-store owner and music columnist. He later recalled: "I immediately liked what I heard. They were fresh, and they were honest, and they had what I thought was a sort of presence ... [a] star quality."*

**Formatted output:**

     PY DATE |               FORMAT |   SUCCESSFUL PARSE |       DISPLAY DATE | ORIGINAL TEXT
         --- |                  --- |                --- |                --- | ---
  1956-12-28 |         DateFormat.Y |               True |               1956 | 'the last weeks of 1956'
  1957-07-06 |       DateFormat.DMY |               True |        6 July 1957 | '6 July 1957'
  1958-02-01 |        DateFormat.MY |               True |      February 1958 | 'February 1958'
  1958-03-01 |        DateFormat.MY |               True |         March 1958 | 'the first week of March 1958'
  1958-05-01 |        DateFormat.MY |               True |           May 1958 | 'May 1958'
  1959-01-01 |        DateFormat.MY |               True |       January 1959 | 'early January 1959'
  1959-08-17 |       DateFormat.DMY |               True |     17 August 1959 | '17 August 1959'
  1960-01-01 |        DateFormat.MY |               True |       January 1960 | 'January 1960'
  1960-07-01 |        DateFormat.MY |               True |          July 1960 | 'early July 1960'
  1960-08-15 |        DateFormat.MY |               True |        August 1960 | 'the middle of August 1960'
  1960-08-15 |        DateFormat.MY |               True |        August 1960 | 'mid-August 1960'
  1960-08-28 |        DateFormat.MY |               True |        August 1960 | 'late-August 1960'
  1960-11-28 |        DateFormat.MY |               True |      November 1960 | 'late Nov 1960'
  1960-12-01 |        DateFormat.MY |               True |      December 1960 | 'the beginning of December 1960'
  1961-01-01 |         DateFormat.Y |               True |               1961 | '1961'
  1961-02-28 |        DateFormat.MY |               True |      February 1961 | 'around the end of February 1961'
  1961-06-28 |        DateFormat.MY |               True |          June 1961 | 'the final days of June 1961'
  1961-07-15 |         DateFormat.Y |               True |               1961 | 'about mid-1961'
  1961-10-15 |        DateFormat.MY |               True |       October 1961 | 'mid-late Oct 1961'
  1961-11-28 |        DateFormat.MY |               True |      November 1961 | 'the tax year ending November 1961'
  1962-06-01 |        DateFormat.MY |               True |          June 1962 | 'June 1962'
  9999-12-31 |   DateFormat.UNKNOWN |              False |                (?) | 'about four weeks'
  9999-12-31 |   DateFormat.UNKNOWN |              False |                (?) | 'About six months later'


