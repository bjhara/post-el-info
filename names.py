from datetime import datetime
from typing import List

__names = {
  "01-01": [],
  "01-02": [
    "Svea"
  ],
  "01-03": [
    "Alfred",
    "Alfrida"
  ],
  "01-04": [
    "Rut"
  ],
  "01-05": [
    "Hanna",
    "Hannele"
  ],
  "01-06": [
    "Kasper",
    "Melker",
    "Baltsar"
  ],
  "01-07": [
    "August",
    "Augusta"
  ],
  "01-08": [
    "Erland"
  ],
  "01-09": [
    "Gunnar",
    "Gunder"
  ],
  "01-10": [
    "Sigurd",
    "Sigbritt"
  ],
  "01-11": [
    "Jan",
    "Jannike"
  ],
  "01-12": [
    "Frideborg",
    "Fridolf"
  ],
  "01-13": [
    "Knut"
  ],
  "01-14": [
    "Felix",
    "Felicia"
  ],
  "01-15": [
    "Laura",
    "Lorentz"
  ],
  "01-16": [
    "Hjalmar",
    "Helmer"
  ],
  "01-17": [
    "Anton",
    "Tony"
  ],
  "01-18": [
    "Hilda",
    "Hildur"
  ],
  "01-19": [
    "Henrik"
  ],
  "01-20": [
    "Fabian",
    "Sebastian"
  ],
  "01-21": [
    "Agnes",
    "Agneta"
  ],
  "01-22": [
    "Vincent",
    "Viktor"
  ],
  "01-23": [
    "Frej",
    "Freja"
  ],
  "01-24": [
    "Erika"
  ],
  "01-25": [
    "Paul",
    "Pål"
  ],
  "01-26": [
    "Bodil",
    "Boel"
  ],
  "01-27": [
    "Göte",
    "Göta"
  ],
  "01-28": [
    "Karl",
    "Karla"
  ],
  "01-29": [
    "Diana"
  ],
  "01-30": [
    "Gunilla",
    "Gunhild"
  ],
  "01-31": [
    "Ivar",
    "Joar"
  ],
  "02-01": [
    "Max",
    "Maximilian"
  ],
  "02-02": [],
  "02-03": [
    "Disa",
    "Hjördis"
  ],
  "02-04": [
    "Ansgar",
    "Anselm"
  ],
  "02-05": [
    "Agata",
    "Agda"
  ],
  "02-06": [
    "Dorotea",
    "Doris"
  ],
  "02-07": [
    "Rikard",
    "Dick"
  ],
  "02-08": [
    "Berta",
    "Bert"
  ],
  "02-09": [
    "Fanny",
    "Franciska"
  ],
  "02-10": [
    "Iris"
  ],
  "02-11": [
    "Yngve",
    "Inge"
  ],
  "02-12": [
    "Evelina",
    "Evy"
  ],
  "02-13": [
    "Agne",
    "Ove"
  ],
  "02-14": [
    "Valentin"
  ],
  "02-15": [
    "Sigfrid"
  ],
  "02-16": [
    "Julia",
    "Julius"
  ],
  "02-17": [
    "Alexandra",
    "Sandra"
  ],
  "02-18": [
    "Frida",
    "Fritiof"
  ],
  "02-19": [
    "Gabriella",
    "Ella"
  ],
  "02-20": [
    "Vivianne"
  ],
  "02-21": [
    "Hilding"
  ],
  "02-22": [
    "Pia"
  ],
  "02-23": [
    "Torsten",
    "Torun"
  ],
  "02-24": [
    "Mattias",
    "Mats"
  ],
  "02-25": [
    "Sigvard",
    "Sivert"
  ],
  "02-26": [
    "Torgny",
    "Torkel"
  ],
  "02-27": [
    "Lage"
  ],
  "02-28": [
    "Maria"
  ],
  "03-01": [
    "Albin",
    "Elvira"
  ],
  "03-02": [
    "Ernst",
    "Erna"
  ],
  "03-03": [
    "Gunborg",
    "Gunvor"
  ],
  "03-04": [
    "Adrian",
    "Adriana"
  ],
  "03-05": [
    "Tora",
    "Tove"
  ],
  "03-06": [
    "Ebba",
    "Ebbe"
  ],
  "03-07": [
    "Camilla"
  ],
  "03-08": [
    "Siv",
    "Saga"
  ],
  "03-09": [
    "Torbjörn",
    "Torleif"
  ],
  "03-10": [
    "Edla",
    "Ada"
  ],
  "03-11": [
    "Edvin",
    "Egon"
  ],
  "03-12": [
    "Viktoria"
  ],
  "03-13": [
    "Greger"
  ],
  "03-14": [
    "Matilda",
    "Maud"
  ],
  "03-15": [
    "Kristoffer",
    "Christel"
  ],
  "03-16": [
    "Herbert",
    "Gilbert"
  ],
  "03-17": [
    "Gertrud"
  ],
  "03-18": [
    "Edvard",
    "Edmund"
  ],
  "03-19": [
    "Josef",
    "Josefina"
  ],
  "03-20": [
    "Joakim",
    "Kim"
  ],
  "03-21": [
    "Bengt"
  ],
  "03-22": [
    "Kennet",
    "Kent"
  ],
  "03-23": [
    "Gerda",
    "Gerd"
  ],
  "03-24": [
    "Gabriel",
    "Rafael"
  ],
  "03-25": [],
  "03-26": [
    "Emanuel"
  ],
  "03-27": [
    "Rudolf",
    "Ralf"
  ],
  "03-28": [
    "Malkolm",
    "Morgan"
  ],
  "03-29": [
    "Jonas",
    "Jens"
  ],
  "03-30": [
    "Holger",
    "Holmfrid"
  ],
  "03-31": [
    "Ester"
  ],
  "04-01": [
    "Harald",
    "Hervor"
  ],
  "04-02": [
    "Gudmund",
    "Ingemund"
  ],
  "04-03": [
    "Ferdinand",
    "Nanna"
  ],
  "04-04": [
    "Marianne",
    "Marlene"
  ],
  "04-05": [
    "Irene",
    "Irja"
  ],
  "04-06": [
    "Vilhelm",
    "William"
  ],
  "04-07": [
    "Irma",
    "Irmelin"
  ],
  "04-08": [
    "Nadja",
    "Tanja"
  ],
  "04-09": [
    "Otto",
    "Ottilia"
  ],
  "04-10": [
    "Ingvar",
    "Ingvor"
  ],
  "04-11": [
    "Ulf",
    "Ylva"
  ],
  "04-12": [
    "Liv"
  ],
  "04-13": [
    "Artur",
    "Douglas"
  ],
  "04-14": [
    "Tiburtius"
  ],
  "04-15": [
    "Olivia",
    "Oliver"
  ],
  "04-16": [
    "Patrik",
    "Patricia"
  ],
  "04-17": [
    "Elias",
    "Elis"
  ],
  "04-18": [
    "Valdemar",
    "Volmar"
  ],
  "04-19": [
    "Olaus",
    "Ola"
  ],
  "04-20": [
    "Amalia",
    "Amelie"
  ],
  "04-21": [
    "Anneli",
    "Annika"
  ],
  "04-22": [
    "Allan",
    "Glenn"
  ],
  "04-23": [
    "Georg",
    "Göran"
  ],
  "04-24": [
    "Vega"
  ],
  "04-25": [
    "Markus"
  ],
  "04-26": [
    "Teresia",
    "Terese"
  ],
  "04-27": [
    "Engelbrekt"
  ],
  "04-28": [
    "Ture",
    "Tyra"
  ],
  "04-29": [
    "Tyko"
  ],
  "04-30": [
    "Mariana"
  ],
  "05-01": [
    "Valborg"
  ],
  "05-02": [
    "Filip",
    "Filippa"
  ],
  "05-03": [
    "John",
    "Jane"
  ],
  "05-04": [
    "Monika",
    "Mona"
  ],
  "05-05": [
    "Gotthard",
    "Erhard"
  ],
  "05-06": [
    "Marit",
    "Rita"
  ],
  "05-07": [
    "Carina",
    "Carita"
  ],
  "05-08": [
    "Åke"
  ],
  "05-09": [
    "Reidar",
    "Reidun"
  ],
  "05-10": [
    "Esbjörn",
    "Styrbjörn"
  ],
  "05-11": [
    "Märta",
    "Märit"
  ],
  "05-12": [
    "Charlotta",
    "Lotta"
  ],
  "05-13": [
    "Linnea",
    "Linn"
  ],
  "05-14": [
    "Halvard",
    "Halvar"
  ],
  "05-15": [
    "Sofia",
    "Sonja"
  ],
  "05-16": [
    "Ronald",
    "Ronny"
  ],
  "05-17": [
    "Rebecka",
    "Ruben"
  ],
  "05-18": [
    "Erik"
  ],
  "05-19": [
    "Maj",
    "Majken"
  ],
  "05-20": [
    "Karolina",
    "Carola"
  ],
  "05-21": [
    "Konstantin",
    "Conny"
  ],
  "05-22": [
    "Hemming",
    "Henning"
  ],
  "05-23": [
    "Desideria",
    "Desirée"
  ],
  "05-24": [
    "Ivan",
    "Vanja"
  ],
  "05-25": [
    "Urban"
  ],
  "05-26": [
    "Vilhelmina",
    "Vilma"
  ],
  "05-27": [
    "Beda",
    "Blenda"
  ],
  "05-28": [
    "Ingeborg",
    "Borghild"
  ],
  "05-29": [
    "Yvonne",
    "Jeanette"
  ],
  "05-30": [
    "Vera",
    "Veronika"
  ],
  "05-31": [
    "Petronella",
    "Pernilla"
  ],
  "06-01": [
    "Gun",
    "Gunnel"
  ],
  "06-02": [
    "Rutger",
    "Roger"
  ],
  "06-03": [
    "Ingemar",
    "Gudmar"
  ],
  "06-04": [
    "Solbritt",
    "Solveig"
  ],
  "06-05": [
    "Bo"
  ],
  "06-06": [
    "Gustav",
    "Gösta"
  ],
  "06-07": [
    "Robert",
    "Robin"
  ],
  "06-08": [
    "Eivor",
    "Majvor"
  ],
  "06-09": [
    "Börje",
    "Birger"
  ],
  "06-10": [
    "Svante",
    "Boris"
  ],
  "06-11": [
    "Bertil",
    "Berthold"
  ],
  "06-12": [
    "Eskil"
  ],
  "06-13": [
    "Aina",
    "Aino"
  ],
  "06-14": [
    "Håkan",
    "Hakon"
  ],
  "06-15": [
    "Margit",
    "Margot"
  ],
  "06-16": [
    "Axel",
    "Axelina"
  ],
  "06-17": [
    "Torborg",
    "Torvald"
  ],
  "06-18": [
    "Björn",
    "Bjarne"
  ],
  "06-19": [
    "Germund",
    "Görel"
  ],
  "06-20": [
    "Linda"
  ],
  "06-21": [
    "Alf",
    "Alvar"
  ],
  "06-22": [
    "Paulina",
    "Paula"
  ],
  "06-23": [
    "Adolf",
    "Alice"
  ],
  "06-24": [],
  "06-25": [
    "David",
    "Salomon"
  ],
  "06-26": [
    "Rakel",
    "Lea"
  ],
  "06-27": [
    "Selma",
    "Fingal"
  ],
  "06-28": [
    "Leo"
  ],
  "06-29": [
    "Peter",
    "Petra"
  ],
  "06-30": [
    "Elof",
    "Leif"
  ],
  "07-01": [
    "Aron",
    "Mirjam"
  ],
  "07-02": [
    "Rosa",
    "Rosita"
  ],
  "07-03": [
    "Aurora"
  ],
  "07-04": [
    "Ulrika",
    "Ulla"
  ],
  "07-05": [
    "Laila",
    "Ritva"
  ],
  "07-06": [
    "Esaias",
    "Jessika"
  ],
  "07-07": [
    "Klas"
  ],
  "07-08": [
    "Kjell"
  ],
  "07-09": [
    "Jörgen",
    "Örjan"
  ],
  "07-10": [
    "André",
    "Andrea"
  ],
  "07-11": [
    "Eleonora",
    "Ellinor"
  ],
  "07-12": [
    "Herman",
    "Hermine"
  ],
  "07-13": [
    "Joel",
    "Judit"
  ],
  "07-14": [
    "Folke"
  ],
  "07-15": [
    "Ragnhild",
    "Ragnvald"
  ],
  "07-16": [
    "Reinhold",
    "Reine"
  ],
  "07-17": [
    "Bruno"
  ],
  "07-18": [
    "Fredrik",
    "Fritz"
  ],
  "07-19": [
    "Sara"
  ],
  "07-20": [
    "Margareta",
    "Greta"
  ],
  "07-21": [
    "Johanna"
  ],
  "07-22": [
    "Magdalena",
    "Madeleine"
  ],
  "07-23": [
    "Emma",
    "Emmy"
  ],
  "07-24": [
    "Kristina",
    "Kerstin"
  ],
  "07-25": [
    "Jakob"
  ],
  "07-26": [
    "Jesper",
    "Jasmine"
  ],
  "07-27": [
    "Marta"
  ],
  "07-28": [
    "Botvid",
    "Seved"
  ],
  "07-29": [
    "Olof"
  ],
  "07-30": [
    "Algot"
  ],
  "07-31": [
    "Helena",
    "Elin"
  ],
  "08-01": [
    "Per"
  ],
  "08-02": [
    "Karin",
    "Kajsa"
  ],
  "08-03": [
    "Tage"
  ],
  "08-04": [
    "Arne",
    "Arnold"
  ],
  "08-05": [
    "Ulrik",
    "Alrik"
  ],
  "08-06": [
    "Alfons",
    "Inez"
  ],
  "08-07": [
    "Dennis",
    "Denise"
  ],
  "08-08": [
    "Silvia",
    "Sylvia"
  ],
  "08-09": [
    "Roland"
  ],
  "08-10": [
    "Lars"
  ],
  "08-11": [
    "Susanna"
  ],
  "08-12": [
    "Klara"
  ],
  "08-13": [
    "Kaj"
  ],
  "08-14": [
    "Uno"
  ],
  "08-15": [
    "Stella",
    "Estelle"
  ],
  "08-16": [
    "Brynolf"
  ],
  "08-17": [
    "Verner",
    "Valter"
  ],
  "08-18": [
    "Ellen",
    "Lena"
  ],
  "08-19": [
    "Magnus",
    "Måns"
  ],
  "08-20": [
    "Bernhard",
    "Bernt"
  ],
  "08-21": [
    "Jon",
    "Jonna"
  ],
  "08-22": [
    "Henrietta",
    "Henrika"
  ],
  "08-23": [
    "Signe",
    "Signhild"
  ],
  "08-24": [
    "Bartolomeus"
  ],
  "08-25": [
    "Lovisa",
    "Louise"
  ],
  "08-26": [
    "Östen"
  ],
  "08-27": [
    "Rolf",
    "Raoul"
  ],
  "08-28": [
    "Fatima",
    "Leila"
  ],
  "08-29": [
    "Hans",
    "Hampus"
  ],
  "08-30": [
    "Albert",
    "Albertina"
  ],
  "08-31": [
    "Arvid",
    "Vidar"
  ],
  "09-01": [
    "Sam",
    "Samuel"
  ],
  "09-02": [
    "Justus",
    "Justina"
  ],
  "09-03": [
    "Alfhild",
    "Alva"
  ],
  "09-04": [
    "Gisela"
  ],
  "09-05": [
    "Adela",
    "Heidi"
  ],
  "09-06": [
    "Lilian",
    "Lilly"
  ],
  "09-07": [
    "Kevin",
    "Roy"
  ],
  "09-08": [
    "Alma",
    "Hulda"
  ],
  "09-09": [
    "Anita",
    "Annette"
  ],
  "09-10": [
    "Tord",
    "Turid"
  ],
  "09-11": [
    "Dagny",
    "Helny"
  ],
  "09-12": [
    "Åsa",
    "Åslög"
  ],
  "09-13": [
    "Sture"
  ],
  "09-14": [
    "Ida"
  ],
  "09-15": [
    "Sigrid",
    "Siri"
  ],
  "09-16": [
    "Dag",
    "Daga"
  ],
  "09-17": [
    "Hildegard",
    "Magnhild"
  ],
  "09-18": [
    "Orvar"
  ],
  "09-19": [
    "Fredrika"
  ],
  "09-20": [
    "Elise",
    "Lisa"
  ],
  "09-21": [
    "Matteus"
  ],
  "09-22": [
    "Maurits",
    "Moritz"
  ],
  "09-23": [
    "Tekla",
    "Tea"
  ],
  "09-24": [
    "Gerhard",
    "Gert"
  ],
  "09-25": [
    "Tryggve"
  ],
  "09-26": [
    "Enar",
    "Einar"
  ],
  "09-27": [
    "Dagmar",
    "Rigmor"
  ],
  "09-28": [
    "Lennart",
    "Leonard"
  ],
  "09-29": [
    "Mikael",
    "Mikaela"
  ],
  "09-30": [
    "Helge"
  ],
  "10-01": [
    "Ragnar",
    "Ragna"
  ],
  "10-02": [
    "Ludvig",
    "Love"
  ],
  "10-03": [
    "Evald",
    "Osvald"
  ],
  "10-04": [
    "Frans",
    "Frank"
  ],
  "10-05": [
    "Bror"
  ],
  "10-06": [
    "Jenny",
    "Jennifer"
  ],
  "10-07": [
    "Birgitta",
    "Britta"
  ],
  "10-08": [
    "Nils"
  ],
  "10-09": [
    "Ingrid",
    "Inger"
  ],
  "10-10": [
    "Harry",
    "Harriet"
  ],
  "10-11": [
    "Erling",
    "Jarl"
  ],
  "10-12": [
    "Valfrid",
    "Manfred"
  ],
  "10-13": [
    "Berit",
    "Birgit"
  ],
  "10-14": [
    "Stellan"
  ],
  "10-15": [
    "Hedvig",
    "Hillevi"
  ],
  "10-16": [
    "Finn"
  ],
  "10-17": [
    "Antonia",
    "Toini"
  ],
  "10-18": [
    "Lukas"
  ],
  "10-19": [
    "Tore",
    "Tor"
  ],
  "10-20": [
    "Sibylla"
  ],
  "10-21": [
    "Ursula",
    "Yrsa"
  ],
  "10-22": [
    "Marika",
    "Marita"
  ],
  "10-23": [
    "Severin",
    "Sören"
  ],
  "10-24": [
    "Evert",
    "Eilert"
  ],
  "10-25": [
    "Inga",
    "Ingalill"
  ],
  "10-26": [
    "Amanda",
    "Rasmus"
  ],
  "10-27": [
    "Sabina"
  ],
  "10-28": [
    "Simon",
    "Simone"
  ],
  "10-29": [
    "Viola"
  ],
  "10-30": [
    "Elsa",
    "Isabella"
  ],
  "10-31": [
    "Edit",
    "Edgar"
  ],
  "11-01": [],
  "11-02": [
    "Tobias"
  ],
  "11-03": [
    "Hubert",
    "Hugo"
  ],
  "11-04": [
    "Sverker"
  ],
  "11-05": [
    "Eugen",
    "Eugenia"
  ],
  "11-06": [
    "Gustav Adolf"
  ],
  "11-07": [
    "Ingegerd",
    "Ingela"
  ],
  "11-08": [
    "Vendela"
  ],
  "11-09": [
    "Teodor",
    "Teodora"
  ],
  "11-10": [
    "Martin",
    "Martina"
  ],
  "11-11": [
    "Mårten"
  ],
  "11-12": [
    "Konrad",
    "Kurt"
  ],
  "11-13": [
    "Kristian",
    "Krister"
  ],
  "11-14": [
    "Emil",
    "Emilia"
  ],
  "11-15": [
    "Leopold"
  ],
  "11-16": [
    "Vibeke",
    "Viveka"
  ],
  "11-17": [
    "Naemi",
    "Naima"
  ],
  "11-18": [
    "Lillemor",
    "Moa"
  ],
  "11-19": [
    "Elisabet",
    "Lisbet"
  ],
  "11-20": [
    "Pontus",
    "Marina"
  ],
  "11-21": [
    "Helga",
    "Olga"
  ],
  "11-22": [
    "Cecilia",
    "Sissela"
  ],
  "11-23": [
    "Klemens"
  ],
  "11-24": [
    "Gudrun",
    "Rune"
  ],
  "11-25": [
    "Katarina",
    "Katja"
  ],
  "11-26": [
    "Linus"
  ],
  "11-27": [
    "Astrid",
    "Asta"
  ],
  "11-28": [
    "Malte"
  ],
  "11-29": [
    "Sune"
  ],
  "11-30": [
    "Andreas",
    "Anders"
  ],
  "12-01": [
    "Oskar",
    "Ossian"
  ],
  "12-02": [
    "Beata",
    "Beatrice"
  ],
  "12-03": [
    "Lydia"
  ],
  "12-04": [
    "Barbara",
    "Barbro"
  ],
  "12-05": [
    "Sven"
  ],
  "12-06": [
    "Nikolaus",
    "Niklas"
  ],
  "12-07": [
    "Angela",
    "Angelika"
  ],
  "12-08": [
    "Virginia"
  ],
  "12-09": [
    "Anna"
  ],
  "12-10": [
    "Malin",
    "Malena"
  ],
  "12-11": [
    "Daniel",
    "Daniela"
  ],
  "12-12": [
    "Alexander",
    "Alexis"
  ],
  "12-13": [
    "Lucia"
  ],
  "12-14": [
    "Sten",
    "Sixten"
  ],
  "12-15": [
    "Gottfrid"
  ],
  "12-16": [
    "Assar"
  ],
  "12-17": [
    "Stig"
  ],
  "12-18": [
    "Abraham"
  ],
  "12-19": [
    "Isak"
  ],
  "12-20": [
    "Israel",
    "Moses"
  ],
  "12-21": [
    "Tomas"
  ],
  "12-22": [
    "Natanael",
    "Jonatan"
  ],
  "12-23": [
    "Adam"
  ],
  "12-24": [
    "Eva"
  ],
  "12-25": [],
  "12-26": [
    "Stefan",
    "Staffan"
  ],
  "12-27": [
    "Johannes",
    "Johan"
  ],
  "12-28": [
    "Benjamin"
  ],
  "12-29": [
    "Natalia",
    "Natalie"
  ],
  "12-30": [
    "Abel",
    "Set"
  ],
  "12-31": [
    "Sylvester"
  ]
}

def get_names(date: datetime) -> List[str]:
    day = date.day
    month = date.month

    lookup = f"{month:0>2}-{day:0>2}"
    return __names[lookup]

def todays_names() -> List[str]:
    return get_names(datetime.today())
