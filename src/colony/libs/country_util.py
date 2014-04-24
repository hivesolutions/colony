#!/usr/bin/python
# -*- coding: utf-8 -*-

# Hive Colony Framework
# Copyright (c) 2008-2014 Hive Solutions Lda.
#
# This file is part of Hive Colony Framework.
#
# Hive Colony Framework is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Hive Colony Framework is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Hive Colony Framework. If not, see <http://www.gnu.org/licenses/>.

__author__ = "João Magalhães <joamag@hive.pt>"
""" The author(s) of the module """

__version__ = "1.0.0"
""" The version of the module """

__revision__ = "$LastChangedRevision$"
""" The revision number of the module """

__date__ = "$LastChangedDate$"
""" The last change date of the module """

__copyright__ = "Copyright (c) 2008-2014 Hive Solutions Lda."
""" The copyright for the module """

__license__ = "GNU General Public License (GPL), Version 3"
""" The license for the module """

COUNTRIES = {
    "aaland islands" : ("AX", "ALA", "248"),
    "afghanistan" : ("AF", "AFG", "004"),
    "albania" : ("AL", "ALB", "008"),
    "algeria" : ("DZ", "DZA", "012"),
    "american samoa" : ("AS", "ASM", "016"),
    "andorra" : ("AD", "AND", "020"),
    "angola" : ("AO", "AGO", "024"),
    "anguilla" : ("AI", "AIA", "660"),
    "antarctica" : ("AQ", "ATA", "010"),
    "antigua and barbuda" : ("AG", "ATG", "028"),
    "argentina" : ("AR", "ARG", "032"),
    "armenia" : ("AM", "ARM", "051"),
    "aruba" : ("AW", "ABW", "533"),
    "australia" : ("AU", "AUS", "036"),
    "austria" : ("AT", "AUT", "040"),
    "azerbaijan" : ("AZ", "AZE", "031"),
    "bahamas" : ("BS", "BHS", "044"),
    "bahrain" : ("BH", "BHR", "048"),
    "bangladesh" : ("BD", "BGD", "050"),
    "barbados" : ("BB", "BRB", "052"),
    "belarus" : ("BY", "BLR", "112"),
    "belgium" : ("BE", "BEL", "056"),
    "belize" : ("BZ", "BLZ", "084"),
    "benin" : ("BJ", "BEN", "204"),
    "bermuda" : ("BM", "BMU", "060"),
    "bhutan" : ("BT", "BTN", "064"),
    "bolivia" : ("BO", "BOL", "068"),
    "bosnia and herzegowina" : ("BA", "BIH", "070"),
    "botswana" : ("BW", "BWA", "072"),
    "bouvet island" : ("BV", "BVT", "074"),
    "brazil" : ("BR", "BRA", "076"),
    "british indian ocean territory" : ("IO", "IOT", "086"),
    "brunei darussalam" : ("BN", "BRN", "096"),
    "bulgaria" : ("BG", "BGR", "100"),
    "burkina faso" : ("BF", "BFA", "854"),
    "burundi" : ("BI", "BDI", "108"),
    "cambodia" : ("KH", "KHM", "116"),
    "cameroon" : ("CM", "CMR", "120"),
    "canada" : ("CA", "CAN", "124"),
    "cape verde" : ("CV", "CPV", "132"),
    "cayman islands" : ("KY", "CYM", "136"),
    "central african republic" : ("CF", "CAF", "140"),
    "chad" : ("TD", "TCD", "148"),
    "chile" : ("CL", "CHL", "152"),
    "china" : ("CN", "CHN", "156"),
    "christmas island" : ("CX", "CXR", "162"),
    "cocos (keeling) islands" : ("CC", "CCK", "166"),
    "colombia" : ("CO", "COL", "170"),
    "comoros" : ("KM", "COM", "174"),
    "congo, democratic republic of (was zaire)" : ("CD", "COD", "180"),
    "congo, republic of" : ("CG", "COG", "178"),
    "cook islands" : ("CK", "COK", "184"),
    "costa rica" : ("CR", "CRI", "188"),
    "cote d'ivoire" : ("CI", "CIV", "384"),
    "croatia (local name: hrvatska)" : ("HR", "HRV", "191"),
    "cuba" : ("CU", "CUB", "192"),
    "cyprus" : ("CY", "CYP", "196"),
    "czech republic" : ("CZ", "CZE", "203"),
    "denmark" : ("DK", "DNK", "208"),
    "djibouti" : ("DJ", "DJI", "262"),
    "dominica" : ("DM", "DMA", "212"),
    "dominican republic" : ("DO", "DOM", "214"),
    "ecuador" : ("EC", "ECU", "218"),
    "egypt" : ("EG", "EGY", "818"),
    "el salvador" : ("SV", "SLV", "222"),
    "equatorial guinea" : ("GQ", "GNQ", "226"),
    "eritrea" : ("ER", "ERI", "232"),
    "estonia" : ("EE", "EST", "233"),
    "ethiopia" : ("ET", "ETH", "231"),
    "falkland islands (malvinas)" : ("FK", "FLK", "238"),
    "faroe islands" : ("FO", "FRO", "234"),
    "fiji" : ("FJ", "FJI", "242"),
    "finland" : ("FI", "FIN", "246"),
    "france" : ("FR", "FRA", "250"),
    "french guiana" : ("GF", "GUF", "254"),
    "french polynesia" : ("PF", "PYF", "258"),
    "french southern territories" : ("TF", "ATF", "260"),
    "gabon" : ("GA", "GAB", "266"),
    "gambia" : ("GM", "GMB", "270"),
    "georgia" : ("GE", "GEO", "268"),
    "germany" : ("DE", "DEU", "276"),
    "ghana" : ("GH", "GHA", "288"),
    "gibraltar" : ("GI", "GIB", "292"),
    "greece" : ("GR", "GRC", "300"),
    "greenland" : ("GL", "GRL", "304"),
    "grenada" : ("GD", "GRD", "308"),
    "guadeloupe" : ("GP", "GLP", "312"),
    "guam" : ("GU", "GUM", "316"),
    "guatemala" : ("GT", "GTM", "320"),
    "guinea" : ("GN", "GIN", "324"),
    "guinea-bissau" : ("GW", "GNB", "624"),
    "guyana" : ("GY", "GUY", "328"),
    "haiti" : ("HT", "HTI", "332"),
    "heard and mc donald islands" : ("HM", "HMD", "334"),
    "honduras" : ("HN", "HND", "340"),
    "hong kong" : ("HK", "HKG", "344"),
    "hungary" : ("HU", "HUN", "348"),
    "iceland" : ("IS", "ISL", "352"),
    "india" : ("IN", "IND", "356"),
    "indonesia" : ("ID", "IDN", "360"),
    "iran (islamic republic of)" : ("IR", "IRN", "364"),
    "iraq" : ("IQ", "IRQ", "368"),
    "ireland" : ("IE", "IRL", "372"),
    "israel" : ("IL", "ISR", "376"),
    "italy" : ("IT", "ITA", "380"),
    "jamaica" : ("JM", "JAM", "388"),
    "japan" : ("JP", "JPN", "392"),
    "jordan" : ("JO", "JOR", "400"),
    "kazakhstan" : ("KZ", "KAZ", "398"),
    "kenya" : ("KE", "KEN", "404"),
    "kiribati" : ("KI", "KIR", "296"),
    "korea, democratic people's republic of" : ("KP", "PRK", "408"),
    "korea, republic of" : ("KR", "KOR", "410"),
    "kuwait" : ("KW", "KWT", "414"),
    "kyrgyzstan" : ("KG", "KGZ", "417"),
    "lao people's democratic republic" : ("LA", "LAO", "418"),
    "latvia" : ("LV", "LVA", "428"),
    "lebanon" : ("LB", "LBN", "422"),
    "lesotho" : ("LS", "LSO", "426"),
    "liberia" : ("LR", "LBR", "430"),
    "libyan arab jamahiriya" : ("LY", "LBY", "434"),
    "liechtenstein" : ("LI", "LIE", "438"),
    "lithuania" : ("LT", "LTU", "440"),
    "luxembourg" : ("LU", "LUX", "442"),
    "macau" : ("MO", "MAC", "446"),
    "macedonia, the former yugoslav republic of" : ("MK", "MKD", "807"),
    "madagascar" : ("MG", "MDG", "450"),
    "malawi" : ("MW", "MWI", "454"),
    "malaysia" : ("MY", "MYS", "458"),
    "maldives" : ("MV", "MDV", "462"),
    "mali" : ("ML", "MLI", "466"),
    "malta" : ("MT", "MLT", "470"),
    "marshall islands" : ("MH", "MHL", "584"),
    "martinique" : ("MQ", "MTQ", "474"),
    "mauritania" : ("MR", "MRT", "478"),
    "mauritius" : ("MU", "MUS", "480"),
    "mayotte" : ("YT", "MYT", "175"),
    "mexico" : ("MX", "MEX", "484"),
    "micronesia, federated states of" : ("FM", "FSM", "583"),
    "moldova, republic of" : ("MD", "MDA", "498"),
    "monaco" : ("MC", "MCO", "492"),
    "mongolia" : ("MN", "MNG", "496"),
    "montserrat" : ("MS", "MSR", "500"),
    "morocco" : ("MA", "MAR", "504"),
    "mozambique" : ("MZ", "MOZ", "508"),
    "myanmar" : ("MM", "MMR", "104"),
    "namibia" : ("NA", "NAM", "516"),
    "nauru" : ("NR", "NRU", "520"),
    "nepal" : ("NP", "NPL", "524"),
    "netherlands" : ("NL", "NLD", "528"),
    "netherlands antilles" : ("AN", "ANT", "530"),
    "new caledonia" : ("NC", "NCL", "540"),
    "new zealand" : ("NZ", "NZL", "554"),
    "nicaragua" : ("NI", "NIC", "558"),
    "niger" : ("NE", "NER", "562"),
    "nigeria" : ("NG", "NGA", "566"),
    "niue" : ("NU", "NIU", "570"),
    "norfolk island" : ("NF", "NFK", "574"),
    "northern mariana islands" : ("MP", "MNP", "580"),
    "norway" : ("NO", "NOR", "578"),
    "oman" : ("OM", "OMN", "512"),
    "pakistan" : ("PK", "PAK", "586"),
    "palau" : ("PW", "PLW", "585"),
    "palestinian territory, occupied" : ("PS", "PSE", "275"),
    "panama" : ("PA", "PAN", "591"),
    "papua new guinea" : ("PG", "PNG", "598"),
    "paraguay" : ("PY", "PRY", "600"),
    "peru" : ("PE", "PER", "604"),
    "philippines" : ("PH", "PHL", "608"),
    "pitcairn" : ("PN", "PCN", "612"),
    "poland" : ("PL", "POL", "616"),
    "portugal" : ("PT", "PRT", "620"),
    "puerto rico" : ("PR", "PRI", "630"),
    "qatar" : ("QA", "QAT", "634"),
    "reunion" : ("RE", "REU", "638"),
    "romania" : ("RO", "ROU", "642"),
    "russian federation" : ("RU", "RUS", "643"),
    "rwanda" : ("RW", "RWA", "646"),
    "saint helena" : ("SH", "SHN", "654"),
    "saint kitts and nevis" : ("KN", "KNA", "659"),
    "saint lucia" : ("LC", "LCA", "662"),
    "saint pierre and miquelon" : ("PM", "SPM", "666"),
    "saint vincent and the grenadines" : ("VC", "VCT", "670"),
    "samoa" : ("WS", "WSM", "882"),
    "san marino" : ("SM", "SMR", "674"),
    "sao tome and principe" : ("ST", "STP", "678"),
    "saudi arabia" : ("SA", "SAU", "682"),
    "senegal" : ("SN", "SEN", "686"),
    "serbia and montenegro" : ("CS", "SCG", "891"),
    "seychelles" : ("SC", "SYC", "690"),
    "sierra leone" : ("SL", "SLE", "694"),
    "singapore" : ("SG", "SGP", "702"),
    "slovakia" : ("SK", "SVK", "703"),
    "slovenia" : ("SI", "SVN", "705"),
    "solomon islands" : ("SB", "SLB", "090"),
    "somalia" : ("SO", "SOM", "706"),
    "south africa" : ("ZA", "ZAF", "710"),
    "south georgia and the south sandwich islands" : ("GS", "SGS", "239"),
    "spain" : ("ES", "ESP", "724"),
    "sri lanka" : ("LK", "LKA", "144"),
    "sudan" : ("SD", "SDN", "736"),
    "suriname" : ("SR", "SUR", "740"),
    "svalbard and jan mayen islands" : ("SJ", "SJM", "744"),
    "swaziland" : ("SZ", "SWZ", "748"),
    "sweden" : ("SE", "SWE", "752"),
    "switzerland" : ("CH", "CHE", "756"),
    "syrian arab republic" : ("SY", "SYR", "760"),
    "taiwan" : ("TW", "TWN", "158"),
    "tajikistan" : ("TJ", "TJK", "762"),
    "tanzania, united republic of" : ("TZ", "TZA", "834"),
    "thailand" : ("TH", "THA", "764"),
    "timor-leste" : ("TL", "TLS", "626"),
    "togo" : ("TG", "TGO", "768"),
    "tokelau" : ("TK", "TKL", "772"),
    "tonga" : ("TO", "TON", "776"),
    "trinidad and tobago" : ("TT", "TTO", "780"),
    "tunisia" : ("TN", "TUN", "788"),
    "turkey" : ("TR", "TUR", "792"),
    "turkmenistan" : ("TM", "TKM", "795"),
    "turks and caicos islands" : ("TC", "TCA", "796"),
    "tuvalu" : ("TV", "TUV", "798"),
    "uganda" : ("UG", "UGA", "800"),
    "ukraine" : ("UA", "UKR", "804"),
    "united arab emirates" : ("AE", "ARE", "784"),
    "united kingdom" : ("GB", "GBR", "826"),
    "united states" : ("US", "USA", "840"),
    "united states minor outlying islands" : ("UM", "UMI", "581"),
    "uruguay" : ("UY", "URY", "858"),
    "uzbekistan" : ("UZ", "UZB", "860"),
    "vanuatu" : ("VU", "VUT", "548"),
    "vatican city state (holy see)" : ("VA", "VAT", "336"),
    "venezuela" : ("VE", "VEN", "862"),
    "viet nam" : ("VN", "VNM", "704"),
    "virgin islands (british)" : ("VG", "VGB", "092"),
    "virgin islands (u.s.)" : ("VI", "VIR", "850"),
    "wallis and futuna islands" : ("WF", "WLF", "876"),
    "western sahara" : ("EH", "ESH", "732"),
    "yemen" : ("YE", "YEM", "887"),
    "zambia" : ("ZM", "ZMB", "894"),
    "zimbabwe" : ("ZW", "ZWE", "716")
}
""" The map associating the various countries with the
tuple containing the iso 3166 information (two character
code, three character code and the number code) """

def country_get(name):
    """
    Retrieves a tuple containing the complete set of iso 3166
    information for the country with the provided name.

    The returned tuple contains a two character code a three
    character code and the number code.

    @type name: String
    @param name: The name of the country for which the information
    is meant to be retrieved.
    @rtype: Tuple
    @return: A tuple containing the iso 3166 information for the
    request country.
    @see: http://en.wikipedia.org/wiki/ISO_3166
    """

    return COUNTRIES.get(name, (None, None, None))
