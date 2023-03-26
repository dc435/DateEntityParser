import enum
from pyparsing import Word, nums, Suppress, oneOf, MatchFirst, CaselessLiteral, ParseException
from datetime import date
import dateutil.parser as date_parser
from dateutil.parser import ParserError


# Representing the format of the successful parse
# eg. "May 2017" -> "MY"
# eg. "14 February 2021" -> "DMY"
class DateFormat(enum.Enum):
    UNKNOWN = 1
    Y = 2
    MY = 3
    DMY = 4


# Each 'Pattern' represents a separate syntactic pattern
# The parser object initiates an array of separate 'Pattern' object, which the parser iterates through each call
class Pattern:
    
    pattern: str
    format: DateFormat
    default_date: date

    def __init__(self, pattern, format, default_date=date(9999,1,1)):
        self.pattern = pattern
        self.format = format
        self.default_date = default_date


# The return object from the parser call. Variables:
# - original text (text);
# - boolean indicating if parse was successful (success);
# - formatted date in python date format (formatted);
# - DateFormat object indicating the level of date information in the string (format)
class ParsedDate:

    text: str
    success: bool
    formatted: date 
    format: DateFormat
    
    def __init__(self, text, success=False, formatted=date.today(), format=DateFormat.UNKNOWN):
        self.text=text
        self.success=success
        self.formatted=formatted
        self.format=format

    # 'Display date' returns a clean string representation of the original text.
    # The return string is limited to those elements of the original text (D,M and/or Y) which were successfully parsed.
    # eg. The original text: "early May 2017" -> return "May 2017"
    # eg. The original text: "2017" -> return "2017"
    def display_date(self):
        
        if self.format == DateFormat.DMY:
            display_date = self.formatted.strftime('%e %B %Y')
        elif self.format == DateFormat.MY:
            display_date = self.formatted.strftime('%B %Y')
        elif self.format == DateFormat.Y:
            display_date = self.formatted.strftime('%Y')
        else:
            display_date = "(?)"
        
        return display_date


# Called when parser() object is initiatalised
# Returns a list of Pattern objects containing date syntax patterns, through which the parser will iterate when called
def get_patterns():
   
    early_prefix = Suppress(MatchFirst([
        CaselessLiteral("about early"),
        CaselessLiteral("around early"),
        CaselessLiteral("around the beginning of"),
        CaselessLiteral("as early as"),
        CaselessLiteral("at least"),
        CaselessLiteral("beginning"),
        CaselessLiteral("between the"),
        CaselessLiteral("between then and"),
        CaselessLiteral("between this date and"),
        CaselessLiteral("during the period from"),
        CaselessLiteral("each month from"),
        CaselessLiteral("each month"),
        CaselessLiteral("earlier than"),
        CaselessLiteral("for the month of"),
        CaselessLiteral("for the years"),
        CaselessLiteral("from about"),
        CaselessLiteral("in about"),
        CaselessLiteral("in around"),
        CaselessLiteral("in the period"),
        CaselessLiteral("on about"),
        CaselessLiteral("prior to"),
        CaselessLiteral("shortly before"),
        CaselessLiteral("the 1st day of"),
        CaselessLiteral("the beginning of"),
        CaselessLiteral("the early"),
        CaselessLiteral("the few months after"),
        CaselessLiteral("the financial year ended"),
        CaselessLiteral("the financial year ending"),
        CaselessLiteral("the first half of"),
        CaselessLiteral("the first months of"),
        CaselessLiteral("the first quarter of"),
        CaselessLiteral("the first week of"),
        CaselessLiteral("the period after"),
        CaselessLiteral("the period ended"),
        CaselessLiteral("the period ending"),
        CaselessLiteral("the period following"),
        CaselessLiteral("the period from"),
        CaselessLiteral("the period from early"),
        CaselessLiteral("the period to"),
        CaselessLiteral("the periods ending"),
        CaselessLiteral("the period"),
        CaselessLiteral("the same day"),
        CaselessLiteral("the week of"),
        CaselessLiteral("the whole of"),
        CaselessLiteral("up to"),
        CaselessLiteral("up until"),
        CaselessLiteral("various days between"),
        oneOf("early- early first before pre to from between and during", caseless=True)
    ]))
    mid_prefix = Suppress(MatchFirst([
        CaselessLiteral("about mid-"),
        CaselessLiteral("about mid"),
        CaselessLiteral("around mid-"),
        CaselessLiteral("around the second half of"),
        CaselessLiteral("early to mid-"),        
        CaselessLiteral("early to mid"),
        CaselessLiteral("no earlier than mid"),
        CaselessLiteral("mid-late"),
        CaselessLiteral("the following day"),
        CaselessLiteral("the middle of"),
        CaselessLiteral("the month of"),
        CaselessLiteral("the months of"),
        CaselessLiteral("the next day"),
        CaselessLiteral("the same day"),
        CaselessLiteral("the same month"),
        CaselessLiteral("the second half of"),
        CaselessLiteral("the week ended"),
        CaselessLiteral("the week ending"),
        CaselessLiteral("the week of"),
        CaselessLiteral("to mid"),
        oneOf("approximately about around circa mid mid- middle through", caseless=True)
    ]))
    late_prefix = Suppress(MatchFirst([
        CaselessLiteral("about late"),
        CaselessLiteral("after"),
        CaselessLiteral("all the years since"),
        CaselessLiteral("around the end of"),
        CaselessLiteral("before the end of"),
        CaselessLiteral("financial year ending"),
        CaselessLiteral("from late"),
        CaselessLiteral("mid to late"),
        CaselessLiteral("no later than"),
        CaselessLiteral("the end of"),
        CaselessLiteral("the final days of"),
        CaselessLiteral("the last day of"),
        CaselessLiteral("the last month of"),
        CaselessLiteral("the last quarter of"),
        CaselessLiteral("the last weeks of"),
        CaselessLiteral("the period after"),
        CaselessLiteral("the tax year ending"),
        CaselessLiteral("the year ended"),
        CaselessLiteral("the year ending"),
        CaselessLiteral("the year of"),
        CaselessLiteral("the year to"),
        CaselessLiteral("the years ended"),
        CaselessLiteral("the years ending"),
        CaselessLiteral("the years"),
        CaselessLiteral("the year"),
        CaselessLiteral("to late"),
        oneOf("after end for last late late- post since the Year", caseless=True)
    ]))
    range_prefix = Suppress(MatchFirst([
        CaselessLiteral("between about"),
        CaselessLiteral("during the period from"),
        CaselessLiteral("earlier than"),
        CaselessLiteral("for the years"),
        CaselessLiteral("from about"),
        CaselessLiteral("in about"),
        CaselessLiteral("in around"),
        CaselessLiteral("in the period"),
        CaselessLiteral("on about"),
        CaselessLiteral("the period between"),
        CaselessLiteral("the period from"),
        CaselessLiteral("the period"),
        CaselessLiteral("the years"),
        oneOf("in on the from during about around period year years between", caseless=True)
    ]))
    connector = Suppress(MatchFirst([
        CaselessLiteral("and on"),
        CaselessLiteral("to about"),
        CaselessLiteral("or early"),
        oneOf("to or and on and until of - ‑ / ( ) , [ ]", caseless=True)
    ]))
    day = Word(nums, max=2) 
    month = oneOf("Jan Feb Mar Apr May Jun Jul Aug Sep Oct Nov Dec January February March April May June July August September October November December", caseless=True)
    year = Word(nums, exact=4)

    dmy = day("day") + month("month") + year("year")
    dym = year("year") + month("month") + day("day")
    mdy = month("month") + day("day") + year("year")
    DMY = dmy | dym | mdy
    my = month("month") + year("year")
    ym = year("year") + month("month")
    MY = my | ym

    patterns = [
        Pattern(
            pattern=DMY,
            format=DateFormat.DMY,
        ),
        Pattern(
            pattern=MY,
            format=DateFormat.MY,
        ),        
        Pattern(
            pattern=year("year"),
            format=DateFormat.Y,
        ),
        Pattern(
            pattern=early_prefix + DMY,
            format=DateFormat.DMY,
        ),
        Pattern(
            pattern=early_prefix + MY,
            format=DateFormat.MY,
        ),  
        Pattern(
            pattern=early_prefix + year("year"),
            format=DateFormat.Y,
        ), 
        Pattern(
            pattern=mid_prefix + DMY,
            format=DateFormat.DMY,
            default_date=date(date.today().year,7,15)
        ),
        Pattern(
            pattern=mid_prefix + MY,
            format=DateFormat.MY,
            default_date=date(date.today().year,7,15)
        ),  
        Pattern(
            pattern=mid_prefix + year("year"),
            format=DateFormat.Y,
            default_date=date(date.today().year,7,15)
        ), 
        Pattern(
            pattern=late_prefix + DMY,
            format=DateFormat.DMY,
            default_date = date(date.today().year,12,28)
        ),
        Pattern(
            pattern=late_prefix + MY,
            format=DateFormat.MY,
            default_date = date(date.today().year,12,28)
        ),
        Pattern(
            pattern=late_prefix + year("year"),
            format=DateFormat.Y,
            default_date = date(date.today().year,12,28)
        ),   
        Pattern(
            pattern=range_prefix + day("day") + month("month") + connector + day + month + year("year"),
            format=DateFormat.DMY,
        ),
        Pattern(
            pattern=day("day") + month("month") + year("year") + connector + day + month + year,
            format=DateFormat.DMY
        ),
        Pattern(
            pattern=day("day") + month("month") + year("year") + day + month + year,
            format=DateFormat.DMY
        ),
        Pattern(
            pattern=range_prefix + day("day") + month("month") + year("year") + connector + day + month + year,
            format=DateFormat.DMY
        ),
        Pattern(
            pattern=range_prefix + day("day") + month("month") + year("year") + connector + month + year,
            format=DateFormat.DMY
        ),
        Pattern(
            pattern=range_prefix + day("day") + connector + day + month("month") + year("year"),
            format=DateFormat.DMY
        ),
        Pattern(
            pattern=range_prefix + month("month") + connector + month + year("year"),
            format=DateFormat.MY
        ),
        Pattern(
            pattern=range_prefix + month("month") + year("year") + connector + month + year,
            format=DateFormat.MY
        ),
        Pattern(
            pattern=range_prefix + month("month") + year("year") + connector + day + month + year,
            format=DateFormat.MY
        ),
        Pattern(
            pattern=range_prefix + month("month") + year("year") + connector + year,
            format=DateFormat.MY
        ),
        Pattern(
            pattern=range_prefix + year("year") + connector + year,
            format=DateFormat.Y
        ),
        Pattern(
            pattern=range_prefix + year("year") + connector + month("month") + year,
            format=DateFormat.MY
        ),
        Pattern(
            pattern=month("month") + connector + month + year("year"),
            format=DateFormat.MY
        ),
        Pattern(
            pattern=month("month") + year("year") + connector + month + year,
            format=DateFormat.MY
        ),
        Pattern(
            pattern=month("month") + connector + month + connector + year("year"),
            format=DateFormat.MY
        ),
        Pattern(
            pattern=day("day") + connector + day + month("month") + year("year"),
            format=DateFormat.DMY
        ),
        Pattern(
            pattern=month("month") + day("day") + connector + year("year"),
            format=DateFormat.DMY
        ),
        Pattern(
            pattern=day("day") + month("month") + connector + day + month + year("year"),
            format=DateFormat.DMY
        ),
        Pattern(
            pattern=day("day") + month("month") + year("year") + connector + day + month + year,
            format=DateFormat.DMY
        ),
        Pattern(
            pattern=year("year") + connector + year,
            format=DateFormat.Y
        ),
        Pattern(
            pattern=month("month") + connector + month + connector + year("year"),
            format=DateFormat.MY
        ),
        Pattern(
            pattern=month("month") + connector + month + connector + year("year"),
            format=DateFormat.MY
        ),
    ]

    return patterns


# Main parser object class:
class parser():

    patterns: list

    def __init__(self):
        self.patterns = get_patterns()

    def parse(self, text):

        # Set defaults:
        default_date=date(9999,12,31)
        format=DateFormat.UNKNOWN

        # Set return object
        pd = ParsedDate(text=text,formatted=default_date)

        # Pre-process text:
        text = text.replace("."," ").replace("["," ").replace("]"," ").strip()

        # Loop through defined date patterns. If successful parse, re-format text, then break:
        for p in self.patterns:
            try:
                result = p.pattern.parseString(text)
                day_txt = result["day"] if "day" in result.keys() else ""
                month_txt = result["month"] if "month" in result.keys() else ""
                year_txt = result["year"] if "year" in result.keys() else "" 
                text = f"{day_txt} {month_txt} {year_txt}".strip()
                default_date = p.default_date
                format = p.format
                break
            except ParseException:
                pass

        # Use date_util parser to parse refined text, and set formt & success variables:
        try:
            pd.formatted = date_parser.parse(text, default=default_date, dayfirst=True)
            pd.success = True
            pd.format = format
        except (ParserError, TypeError):
            pd.formatted = default_date
            pd.success = False
            pd.format = DateFormat.UNKNOWN

        return pd
