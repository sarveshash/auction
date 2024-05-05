import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, PhotoSize
from telegram.ext import Updater, CommandHandler, CallbackContext, CallbackQueryHandler, MessageHandler, Filters, ConversationHandler
import datetime
import threading
import re

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# Set your Telegram Bot Token here
TOKEN = "6850951701:AAGEe31Vupc20pg1fEPwN4L3WznFP1QJprE"

# Set pokemons,teams,tms name here
LEGENDARY_POKEMON_NAMES = ["Articuno", "Zapdos", "Moltres", "Raikou", "Entei", "Suicune", "Regirock", "Regice", "Registeel", "Latias", "Latios", "Uxie", "Mesprit", "Azelf", "Heatran", "Regigigas", "Cresselia", "Cobalion", "Terrakion", "Virizion", "Buzzwole", "Thundurus", "Tornadus", "Landorus", "Type: Null", "Silvally", "Tapu Koko", "Tapu Bulu", "Tapu Fini", "Tapu Lele", "Nihilego", "Pheromosa", "Xurkitree", "Celesteela", "Kartana", "Guzzlord", "Poipole", "Naganadel", "Stakataka", "Blacephalon", "Kubfu", "Urshifu", "Regieleki", "Regidrago", "Glastrier", "Spectrier", "Enamorus", "Wo-chien", "Chien-pao", "Ting-lu", "Chi-yu", "Okidogi", "Munkidori", "Fezandipiti", "Ogerpon", "Mewtwo", "Lugia", "Ho-oh", "Kyogre", "Groudon", "Rayquaza", "Dialga", "Palkia", "Giratina", "Reshiram", "Zekrom", "Kyurem", "Xerneas", "Yveltal", "Zygarde", "Cosmog", "Cosmoem", "Solgaleo", "Lunala", "Necrozma", "Zacian", "Zamazenta", "Eternatus", "Calyrex", "Koraidon", "Miraidon", "Terapagos", "Mew", "Celebi", "Jirachi", "Deoxys", "Phione", "Manaphy", "Darkrai", "Arceus", "shaymin", "Victini", "Keldeo", "Meloetta", "Genesect", "Diancie", "Hoopa", "Volcanion", "Megearna", "Marshadow", "Zeraora", "Meltan", "Melmetal", "Zarude"]

NON_LEGENDARY_POKEMON_NAMES = ["Bulbasaur", "Ivysaur", "Venusaur", "Charmander", "Charmeleon", "Charizard", "Squirtle", "Wartortle", "Blastoise", "Caterpie", "Metapod", "Butterfree", "Weedle", "Kakuna", "Beedrill", "Pidgey", "Pidgeotto", "Pidgeot", "Rattata", "Raticate", "Spearow", "Fearow", "Ekans", "Arbok", "Pikachu", "Raichu", "Sandshrew", "Sandslash", "Nidoran-F", "Nidorina", "Nidoqueen", "Nidoran-M", "Nidorino", "Nidoking", "Clefairy", "Clefable", "Vulpix", "Ninetales", "Jigglypuff", "Wigglytuff", "Zubat", "Golbat", "Oddish", "Gloom", "Vileplume", "Paras", "Parasect", "Venonat", "Venomoth", "Diglett", "Dugtrio", "Meowth", "Persian", "Psyduck", "Golduck", "Mankey", "Primeape", "Growlithe", "Arcanine", "Poliwag", "Poliwhirl", "Poliwrath", "Abra", "Kadabra", "Alakazam", "Machop", "Machoke", "Machamp", "Bellsprout", "Weepinbell", "Victreebel", "Tentacool", "Tentacruel", "Geodude", "Graveler", "Golem", "Ponyta", "Rapidash", "Slowpoke", "Slowbro", "Magnemite", "Magneton", "Farfetchd", "Doduo", "Dodrio", "Seel", "Dewgong", "Grimer", "Muk", "Shellder", "Cloyster", "Gastly", "Haunter", "Gengar", "Onix", "Drowzee", "Hypno", "Krabby", "Kingler", "Voltorb", "Electrode", "Exeggcute", "Exeggutor", "Cubone", "Marowak", "Hitmonlee", "Hitmonchan", "Lickitung", "Koffing", "Weezing", "Rhyhorn", "Rhydon", "Chansey", "Tangela", "Kangaskhan", "Horsea", "Seadra", "Goldeen", "Seaking", "Staryu", "Starmie", "Mr-Mime", "Scyther", "Jynx", "Electabuzz", "Magmar", "Pinsir", "Tauros", "Magikarp", "Gyarados", "Lapras", "Ditto", "Eevee", "Vaporeon", "Jolteon", "Flareon", "Porygon", "Omanyte", "Omastar", "Kabuto", "Kabutops", "Aerodactyl", "Snorlax", "Dratini", "Dragonair", "Dragonite", "Chikorita", "Bayleef", "Meganium", "Cyndaquil", "Quilava", "Typhlosion", "Totodile", "Croconaw", "Feraligatr", "Sentret", "Furret", "Hoothoot", "Noctowl", "Ledyba", "Ledian", "Spinarak", "Ariados", "Crobat", "Chinchou", "Lanturn", "Pichu", "Cleffa", "Igglybuff", "Togepi", "Togetic", "Natu", "Xatu", "Mareep", "Flaaffy", "Ampharos", "Bellossom", "Marill", "Azumarill", "Sudowoodo", "Politoed", "Hoppip", "Skiploom", "Jumpluff", "Aipom", "Sunkern", "Sunflora", "Yanma", "Wooper", "Quagsire", "Espeon", "Umbreon", "Murkrow", "Slowking", "Misdreavus", "Unown", "Wobbuffet", "Girafarig", "Pineco", "Forretress", "Dunsparce", "Gligar", "Steelix", "Snubbull", "Granbull", "Qwilfish", "Scizor", "Shuckle", "Heracross", "Sneasel", "Teddiursa", "Ursaring", "Slugma", "Magcargo", "Swinub", "Piloswine", "Corsola", "Remoraid", "Octillery", "Delibird", "Mantine", "Skarmory", "Houndour", "Houndoom", "Kingdra", "Phanpy", "Donphan", "Porygon2", "Stantler", "Smeargle", "Tyrogue", "Hitmontop", "Smoochum", "Elekid", "Magby", "Miltank", "Blissey", "Larvitar", "Pupitar", "Tyranitar", "Treecko", "Grovyle", "Sceptile", "Torchic", "Combusken", "Blaziken", "Mudkip", "Marshtomp", "Swampert", "Poochyena", "Mightyena", "Zigzagoon", "Linoone", "Wurmple", "Silcoon", "Beautifly", "Cascoon", "Dustox", "Lotad", "Lombre", "Ludicolo", "Seedot", "Nuzleaf", "Shiftry", "Taillow", "Swellow", "Wingull", "Pelipper", "Ralts", "Kirlia", "Gardevoir", "Surskit", "Masquerain", "Shroomish", "Breloom", "Slakoth", "Vigoroth", "Slaking", "Nincada", "Ninjask", "Shedinja", "Whismur", "Loudred", "Exploud", "Makuhita", "Hariyama", "Azurill", "Nosepass", "Skitty", "Delcatty", "Sableye", "Mawile", "Aron", "Lairon", "Aggron", "Meditite", "Medicham", "Electrike", "Manectric", "Plusle", "Minun", "Volbeat", "Illumise", "Roselia", "Gulpin", "Swalot", "Carvanha", "Sharpedo", "Wailmer", "Wailord", "Numel", "Camerupt", "Torkoal", "Spoink", "Grumpig", "Spinda", "Trapinch", "Vibrava", "Flygon", "Cacnea", "Cacturne", "Swablu", "Altaria", "Zangoose", "Seviper", "Lunatone", "Solrock", "Barboach", "Whiscash", "Corphish", "Crawdaunt", "Baltoy", "Claydol", "Lileep", "Cradily", "Anorith", "Armaldo", "Feebas", "Milotic", "Castform", "Kecleon", "Shuppet", "Banette", "Duskull", "Dusclops", "Tropius", "Chimecho", "Absol", "Wynaut", "Snorunt", "Glalie", "Spheal", "Sealeo", "Walrein", "Clamperl", "Huntail", "Gorebyss", "Relicanth", "Luvdisc", "Bagon", "Shelgon", "Salamence", "Beldum", "Metang", "Metagross", "Turtwig", "Grotle", "Torterra", "Chimchar", "Monferno", "Infernape", "Piplup", "Prinplup", "Empoleon", "Starly", "Staravia", "Staraptor", "Bidoof", "Bibarel", "Kricketot", "Kricketune", "Shinx", "Luxio", "Luxray", "Budew", "Roserade", "Cranidos", "Rampardos", "Shieldon", "Bastiodon", "Burmy", "Wormadam-Plant", "Mothim", "Combee", "Vespiquen", "Pachirisu", "Buizel", "Floatzel", "Cherubi", "Cherrim", "Shellos", "Gastrodon", "Ambipom", "Drifloon", "Drifblim", "Buneary", "Lopunny", "Mismagius", "Honchkrow", "Glameow", "Purugly", "Chingling", "Stunky", "Skuntank", "Bronzor", "Bronzong", "Bonsly", "Mime-Jr", "Happiny", "Chatot", "Spiritomb", "Gible", "Gabite", "Garchomp", "Munchlax", "Riolu", "Lucario", "Hippopotas", "Hippowdon", "Skorupi", "Drapion", "Croagunk", "Toxicroak", "Carnivine", "Finneon", "Lumineon", "Mantyke", "Snover", "Abomasnow", "Weavile", "Magnezone", "Lickilicky", "Rhyperior", "Tangrowth", "Electivire", "Magmortar", "Togekiss", "Yanmega", "Leafeon", "Glaceon", "Gliscor", "Mamoswine", "Porygon-Z", "Gallade", "Probopass", "Dusknoir", "Froslass", "Rotom,Snivy", "Servine", "Serperior", "Tepig", "Pignite", "Emboar", "Oshawott", "Dewott", "Samurott", "Patrat", "Watchog", "Lillipup", "Herdier", "Stoutland", "Purrloin", "Liepard", "Pansage", "Simisage", "Pansear", "Simisear", "Panpour", "Simipour", "Munna", "Musharna", "Pidove", "Tranquill", "Unfezant", "Blitzle", "Zebstrika", "Roggenrola", "Boldore", "Gigalith", "Woobat", "Swoobat", "Drilbur", "Excadrill", "Audino", "Timburr", "Gurdurr", "Conkeldurr", "Tympole", "Palpitoad", "Seismitoad", "Throh", "Sawk", "Sewaddle", "Swadloon", "Leavanny", "Venipede", "Whirlipede", "Scolipede", "Cottonee", "Whimsicott", "Petilil", "Lilligant", "Basculin-Red-Striped", "Sandile", "Krokorok", "Krookodile", "Darumaka", "Darmanitan-Standard", "Maractus", "Dwebble", "Crustle", "Scraggy", "Scrafty", "Sigilyph", "Yamask", "Cofagrigus", "Tirtouga", "Carracosta", "Archen", "Archeops", "Trubbish", "Garbodor", "Zorua", "Zoroark", "Minccino", "Cinccino", "Gothita", "Gothorita", "Gothitelle", "Solosis", "Duosion", "Reuniclus", "Ducklett", "Swanna", "Vanillite", "Vanillish", "Vanilluxe", "Deerling", "Sawsbuck", "Emolga", "Karrablast", "Escavalier", "Foongus", "Amoonguss", "Frillish", "Jellicent", "Alomomola", "Joltik", "Galvantula", "Ferroseed", "Ferrothorn", "Klink", "Klang", "Klinklang", "Tynamo", "Eelektrik", "Eelektross", "Elgyem", "Beheeyem", "Litwick", "Lampent", "Chandelure", "Axew", "Fraxure", "Haxorus", "Cubchoo", "Beartic", "Cryogonal", "Shelmet", "Accelgor", "Stunfisk", "Mienfoo", "Mienshao", "Druddigon", "Golett", "Golurk", "Pawniard", "Bisharp", "Bouffalant", "Rufflet", "Braviary", "Vullaby", "Mandibuzz", "Heatmor", "Durant", "Deino", "Zweilous", "Hydreigon", "Larvesta", "Chespin", "Thwackey", "Rillaboom", "Scorbunny", "Raboot", "Cinderace", "Sobble", "Drizzile", "Inteleon", "Skwovet", "Greedent", "Rookidee", "Corvisquire", "Corviknight", "Blipbug", "Dottler", "Orbeetle", "Nickit", "Thievul", "Gossifleur", "Eldegoss", "Wooloo", "Dubwool", "Chewtle", "Drednaw", "Yamper", "Boltund", "Rolycoly", "Carkol", "Coalossal", "Applin", "Flapple", "Appletun", "Silicobra", "Sandaconda", "Cramorant", "Arrokuda", "Barraskewda", "Toxel", "Toxtricity-Amped", "Sizzlipede", "Centiskorch", "Clobbopus", "Grapploct", "Sinistea", "Polteageist", "Hatenna", "Hattrem", "Hatterene", "Impidimp", "Morgrem", "Grimmsnarl", "Obstagoon", "Perrserker", "Cursola", "Sirfetchd", "Mr-Rime", "Runerigus", "Milcery", "Alcremie", "Falinks", "Pincurchin", "Snom", "Frosmoth", "Stonjourner", "Eiscue-Ice", "Indeedee-Male", "Morpeko-Full-Belly", "Cufant", "Copperajah", "Dracozolt", "Arctozolt", "Dracovish", "Dartrix", "Decidueye", "Litten", "Torracat", "Incineroar", "Popplio", "Brionne", "Primarina", "Pikipek", "Trumbeak", "Toucannon", "Yungoos", "Gumshoos", "Grubbin", "Charjabug", "Vikavolt", "Crabrawler", "Crabominable", "Oricorio-Baile", "Cutiefly", "Ribombee", "Rockruff", "Lycanroc-Midday", "Wishiwashi-Solo", "Mareanie", "Toxapex", "Mudbray", "Mudsdale", "Dewpider", "Araquanid", "Fomantis", "Lurantis", "Morelull", "Shiinotic", "Salandit", "Salazzle", "Stufful", "Bewear", "Bounsweet", "Steenee", "Tsareena", "Comfey", "Oranguru", "Passimian", "Wimpod", "Golisopod", "Sandygast", "Palossand", "Pyukumuku", "Type-Null", "Silvally", "Minior-Red-Meteor", "Komala", "Turtonator", "Togedemaru", "Mimikyu-Disguised", "Bruxish", "Drampa", "Dhelmise", "Jangmo-O", "Hakamo-O", "Kommo-O", "Poipole", "Naganadel"]

SHINY_POKEMON_NAMES = LEGENDARY_POKEMON_NAMES + NON_LEGENDARY_POKEMON_NAMES

POKEMON_TEAM = ["Hp", "Attack", "Defense", "Sp. Attack", "Sp. Defense", "Speed"]

TM = ["Tm02", "Tm03", "Tm09", "Tm10", "Tm13", "Tm14", "Tm15", "Tm22", "Tm23", "Tm24", "Tm25", "Tm26", "Tm28", "Tm29", "Tm30", "Tm31", "Tm34", "Tm35", "Tm36", "Tm38", "Tm39", "Tm40", "Tm42", "Tm43", "Tm46", "Tm47", "Tm48", "Tm49", "Tm50", "Tm51", "Tm52", "Tm53", "Tm54", "Tm55", "Tm57", "Tm58", "Tm59", "Tm62", "Tm65", "Tm66", "Tm67", "Tm68", "Tm71", "Tm72", "Tm76", "Tm78", "Tm79", "Tm80", "Tm81", "Tm82", "Tm83", "Tm84", "Tm85", "Tm89", "Tm91", "Tm93", "Tm94", "Tm95", "Tm97", "Tm98", "Tm99"]

# Set approved user, banned user, admin and owner id and username here
APPROVED_USER = []

BANNED_USER = []

ADMIN_ID = ['6277479627']

OWNER_ID = '5752004942'

USER_LIST = []
USER_NAME = ["USER LIST:"]

seller_data = {}
legendary_list = []
non_legendary_list = []
shiny_list = []
tm_list = []
team_list = []

# Define the conversation states
ITEM_NAME, NATURE_PAGE, ITEM_DETAILS, POKEMON_IV, MOVESET_PAGE, BOOSTED, BASE_PRICE = range(7)

# Online photo url
ONLINE_PHOTO_URL = "https://telegra.ph/file/b874e06be8fef6409a89e.jpg"

# Groups username and id with without @
MAIN_GROUP_USERNAME = 'Pokemongohexafriends'
MAIN_GROUP_ID = '-1001822603599'
AUCTION_GROUP_USERNAME = 'pw_auction'
AUCTION_GROUP_ID = '-1002068969951'
SUBMISSION_GROUP_USERNAME = 'guys_no_abuse_allowed'
SUBMISSION_GROUP_ID = '-1002058607013'
REPORT_GROUP_USERNAME = 'pghfbotreportgroup'
REPORT_GROUP_ID = '-1002077064776'

# check if user is member of groups
def check_membership(user_id):
    roles_to_consider = ['creator', 'administrator', 'member', 'restricted']
    is_member_main_group = updater.bot.get_chat_member(MAIN_GROUP_ID, user_id).status in roles_to_consider
    is_member_auction_group = updater.bot.get_chat_member(AUCTION_GROUP_ID, user_id).status in roles_to_consider
    return is_member_main_group, is_member_auction_group

def start(update, context):
    user = update.effective_user
    user_id = str(update.message.from_user.id)

    if user_id not in USER_LIST:
        USER_LIST.append(user_id)
        USER_NAME.append(user.name)

    is_member_main_group, is_member_auction_group = check_membership(user_id)

    inline_buttons = []
    if is_member_main_group and is_member_auction_group:
        inline_buttons.append([InlineKeyboardButton("JOINED", callback_data='joined')])
        reply_text = f"<b>HEY </b>{user.full_name}<b>! YOU ARE ALREADY JOINED OUR MAIN GROUP(POKEMON WARRIORS) AND AUCTION GROUP(PW AUCTION GROUP). JUST CLICK ON 'JOINED' AND CONTINUE YOUR PROCESS.</b>"
    elif is_member_main_group:
        inline_buttons.extend([
            [InlineKeyboardButton("AUCTION GROUP", url='https://t.me/pw_auction')],
            [InlineKeyboardButton("JOINED", callback_data='joined')]
        ])
        reply_text = f"<b>HEY </b>{user.full_name}<b>! YOU ARE ALREADY JOINED OUR MAIN GROUP(POKEMON GO/HEXA FRIENDS GROUP). PLEASE JOIN OUR AUCTION GROUP JUST TAP ON BELOW BUTTON. AFTER JOIN CLICK ON 'JOINED'</b>"
    elif is_member_auction_group:
        inline_buttons.extend([
            [InlineKeyboardButton("MAIN GROUP", url='https://t.me/Pokemongohexafriends')],
            [InlineKeyboardButton("JOINED", callback_data='joined')]
        ])
        reply_text = f"<b>HEY </b>{user.full_name}<b>! YOU ALREADY JOINED OUR AUCTION GROUP(PGHFG AUCTION GROUP). PLEASE JOIN OUR MAIN GROUP(POKEMON GO/HEXA FRIENDS GROUP) TAP ON BELOW BUTTON. AFTER JOIN CLLICK ON 'JOINED'</b>"
    else:
        inline_buttons.extend([
            [InlineKeyboardButton("MAIN GROUP", url='https://t.me/Pokemongohexafriends')],
            [InlineKeyboardButton("AUCTION GROUP", url='https://t.me/pw_auction')],
            [InlineKeyboardButton("JOINED", callback_data='joined')]
        ])
        reply_text = f"<b>HEY </b>{user.full_name}<b>! WELCOME TO PGHFG AUCTION BOT. PLEASE JOIN OUR MAIN GROUP  AND AUCTION GROUP FOR START YOUR AUCTION WITH US.</b>"

    reply_markup = InlineKeyboardMarkup(inline_buttons)	
    update.message.reply_photo(ONLINE_PHOTO_URL, caption=reply_text, reply_markup=reply_markup, parse_mode='HTML')

# Define a function to handle button callback
def button_start(update, context):
    user = update.effective_user
    user_id = user.id
    query = update.callback_query
    query.answer()

    if query.data == 'joined':
        user_id = str(update.callback_query.from_user.id)
        is_member_main_group, is_member_auction_group = check_membership(user_id)

        if is_member_main_group and is_member_auction_group:
            query.message.reply_text(f"<b>Hey </b>{user.first_name}<b> you have join our main and auction group. Use /add to sell anything in auction.</b>", parse_mode='HTML')
        elif is_member_main_group:
            query.message.reply_text(f"<b>Hey </b>{user.first_name}<b> Please join AUCTION GROUP at first.</b>", parse_mode='HTML')
        elif is_member_auction_group:
            query.message.reply_text(f"<b>Hey </b>{user.first_name}<b> Please join MAIN GROUP at first.</b>", parse_mode='HTML')
        else:
            query.message.reply_text(f"<b>Hey </b>{user.first_name}<b> Please join both groups.</b>", parse_mode='HTML')

# Define the conversation handler functions
def add(update, context):
    user = update.effective_user
    user_id = user.id

    keyboard = [
        [
            InlineKeyboardButton("LEGENDARY", callback_data='legendary'),
            InlineKeyboardButton("NON-LEGENDARY", callback_data='non-legendary'),
        ],
        [
            InlineKeyboardButton("SHINY", callback_data='shiny'),
            InlineKeyboardButton("TEAM", callback_data='team'),
        ],
        [
            InlineKeyboardButton("TM", callback_data='tm')
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    if user_id in seller_data:
        update.message.reply_text("please wait till approve/disapprove the last item")
    else:
        message = update.message.reply_text('<b>WHAT YOU WANT TO SELL?(CHOOSE FROM BELOW👇</b>', reply_markup=reply_markup, parse_mode='HTML')
        context.user_data['message_id'] = message.message_id  # Save the message_id for updating later
        context.user_data["user"] = user

        return ITEM_NAME

def category(update, context):
    user = update.effective_user
    query = update.callback_query

    callback_data = query.data

    context.user_data['category'] = callback_data

    if callback_data == 'legendary':
        reply_text = f"HEY {user.full_name.upper()}! WHICH LEGENDARY POKEMON YOU WANT TO SELL?"
    elif callback_data == 'non-legendary':
        reply_text = f"HEY {user.full_name.upper()}! WHICH NON-LEGENDARY POKEMON YOU WANT TO SELL?"
    elif callback_data == 'shiny':
        reply_text = f"HEY {user.full_name.upper()}! WHICH SHINY POKEMON YOU WANT TO SELL?"
    elif callback_data == 'team':
        reply_text = f"HEY {user.full_name.upper()}! WHICH TEAM YOU WANT TO SELL?"
    elif callback_data == 'tm':
        reply_text = f"HEY {user.full_name.upper()}! WHICH TM YOU WANT TO SELL? (PLEASE TELL THE TM NUMBER NOT TM NAME)."

    context.bot.edit_message_text(chat_id=update.callback_query.message.chat_id,
                                  message_id=context.user_data.get('message_id'),
                                  text=reply_text)

def item_name(update, context):
    item_name = update.message.text.title()
    category = context.user_data['category']

    if category == 'legendary':
        if item_name in LEGENDARY_POKEMON_NAMES:
            context.user_data["item_name"] = item_name
            update.message.reply_text(f"PLEASE FORWARD THE NATURE PAGE OF <b>{item_name.upper()}</b> FROM @HeXamonbot", parse_mode='HTML')
            return NATURE_PAGE
        else:
            update.message.reply_text(f"{item_name} is not a name of a legendary Pokémon. Please provide a valid legendary Pokémon name.")
    elif category == 'non-legendary':
        if item_name in NON_LEGENDARY_POKEMON_NAMES:
            update.message.reply_text(f"PLEASE FORWARD THE NATURE PAGE OF {item_name} FROM @HeXamonbot")
            context.user_data["item_name"] = item_name
            return NATURE_PAGE
        else:
            update.message.reply_text(f"{item_name} is not a name of a non-legendary Pokémon. Please provide a valid non-legendary Pokémon name.")
    elif category == 'shiny':
        if item_name in SHINY_POKEMON_NAMES:
            update.message.reply_text(f"PLEASE FORWARD THE NATURE PAGE OF {item_name} FROM @HeXamonbot")
            context.user_data["item_name"] = item_name
            return NATURE_PAGE
        else:
            update.message.reply_text(f"{item_name} is not a name of a shiny Pokémon. Please provide a valid shiny Pokémon name.")
    elif category == 'team':
        if item_name in POKEMON_TEAM:
            update.message.reply_text(f"PLEASE FORWARD THE TEAM PAGE OF {item_name} FROM @HeXamonbot")
            context.user_data["item_name"] = item_name
            return ITEM_DETAILS
        else:
            update.message.reply_text(f"{item_name} is not a name of a team. Please provide a valid team name.")
    elif category == 'tm':
        if item_name in TM:
            update.message.reply_text(f"PLEASE FORWARD THE TM PAGE OF {item_name} FROM @HeXamonbot")
            context.user_data["item_name"] = item_name
            return ITEM_DETAILS
        else:
            update.message.reply_text(f"{item_name} is not a name of a TM. Please provide a valid TM name.")

def nature_page(update, context):
    user = update.effective_user
    user_id = user.id

    item_name = context.user_data.get("item_name")  # Using get() method to avoid KeyError

    if item_name:
        if update.message.caption:
           caption_text = update.message.caption
           if "Nature" in caption_text and "Lv" in caption_text:
               if update.message.forward_from and update.message.forward_from.id == 572621020:
                   # Extracting nature and level from the caption
                   nature_index = caption_text.find("Nature: ") + len("Nature: ")
                   lv_index = caption_text.find("Lv. ") + len("Lv. ")
                   types_index = caption_text.find("Types: [") + len("Types: [")

                   # Finding the end of the nature
                   nature_end_index = caption_text.find(" ", nature_index)
                   if nature_end_index == -1:
                       nature_end_index = caption_text.find("\n", nature_index)
                   nature = caption_text[nature_index:nature_end_index]

                   # Finding the end of the level
                   lv_end_index = caption_text.find(" ", lv_index)
                   if lv_end_index == -1:
                       lv_end_index = caption_text.find("\n", lv_index)
                   lv = caption_text[lv_index:lv_end_index]

                   # Finding the end of the types
                   types_end_index = caption_text.find("]", types_index)
                   if types_end_index == -1:
                       types_end_index = caption_text.find("\n", types_index)
                   types = caption_text[types_index:types_end_index]

                   # Save photo file_id
                   photo = update.message.photo[-1]  # Get the largest photo size
                   context.user_data["picture"] = photo.file_id

                   # Save nature and level in user_data
                   context.user_data["nature"] = nature.strip()
                   context.user_data["lv"] = lv.strip()
                   context.user_data["type"] = types.strip()

                   # Forward the message to the submission group
                   context.bot.forward_message(chat_id=SUBMISSION_GROUP_ID, from_chat_id=update.message.chat_id,
                                               message_id=update.message.message_id)
                   update.message.reply_text("PLEASE FORWARD IV/EV PAGE OF YOUR POKEMON FROM @HeXamonbot")
                   return POKEMON_IV
               else:
                   update.message.reply_text("PLEASE FORWARD FROM @HeXamonbot otherwise process will not work for send to submission")
                   return NATURE_PAGE
           else:
               update.message.reply_text("PLEASE FORWARD THE NATURE PAGE FROM @HeXamonbot")
               return NATURE_PAGE
        else:
            update.message.reply_text("PLEASE DON'T SEND ONLY PHOTO/DETAILS. FORWARD FULL PAGE FROM @HeXamonbot")
            return NATURE_PAGE


def item_details(update, context):
    user = update.effective_user
    user_id = user.id

    item_name = context.user_data.get("item_name")
    category = context.user_data.get("category")

    if item_name:
       if update.message.forward_from and update.message.forward_from.id == 572621020:
           update.message.reply_text(f"PLEASE TELL ME BASE PRICE FOR YOUR '{category.upper()}'[{item_name}]")
           # Forward the information to submission group
           context.bot.forward_message(chat_id=SUBMISSION_GROUP_ID, from_chat_id=update.message.chat_id,
                                       message_id=update.message.message_id)


           context.user_data["details"] = update.message.text
           return BASE_PRICE
       else:
           update.message.reply_text(f"PLEASE FORWARD INFORMATION OF {item_name} FROM @HeXamonbot")
           return ITEM_DETAILS
    else:
        update.message.reply_text("PLEASE TELL ITEM NAME AT FIRST")
        return ITEM_NAME

def pokemon_iv(update, context):
    if update.message.caption:
        if "IV" in update.message.caption and "EV" in update.message.caption:
            if update.message.forward_from and update.message.forward_from.id == 572621020:
                context.user_data["iv_page"] = update.message.caption
                update.message.reply_text("PLEASE FORWARD THE MOVESET PAGE OF YOUR POKEMON FROM @HeXamonbot")
                return MOVESET_PAGE
            else:
                update.message.reply_text("PLEASE FORWARD FROM @HeXamonbot. OTHERWISE PROCESS WILL NOT EXCUTE.")
                return POKEMON_IV
        else:
            update.message.reply_text("PLEASE FORWARD IV/EV PAGE FROM @HeXamonbot")
            return POKEMON_IV
    else:
        update.message.reply_text("Please forward right page of ivs/evs from @HeXamonbot.")
        return POKEMON_IV

def moveset_page(update, context):
    if update.message.caption:
        if "Power" in update.message.caption and "Accuracy" in update.message.caption:
            if update.message.forward_from and update.message.forward_from.id == 572621020:
                context.user_data["moveset_page"] = update.message.caption
                update.message.reply_text("PLEASE TELL ME IS ANY IV IS BOOSTED?")
                return BOOSTED
            else:
                update.message.reply_text("Please forward from @HeXamonbot")
                return MOVESET_PAGE
        else:
            update.message.reply_text("Please forward right page of moveset from @HeXamonbot")
            return MOVESET_PAGE
    else:
        update.message.reply_text("Please forward right page of moveset from @HeXamonbot")
        return MOVESET_PAGE

def boosted(update, context):
    boosted = update.message.text.title()
    item_name = context.user_data.get("item_name")

    if boosted == 'Yes':
        context.user_data["boosted"] = boosted
        update.message.reply_text(f"PLEASE TELL ME THE BASE PRICE FOR YOUR {item_name}")
        return BASE_PRICE

    elif boosted == 'No':
         context.user_data["boosted"] = boosted
         update.message.reply_text(f"PLEASE TELL ME THE BASE PRICE FOR YOU {item_name}")
         return BASE_PRICE

    else:
         update.message.reply_text("I WILL ACCEPT ONLY YES/NO SO GIVE ANSWER IN YES/NO")
         return BOOSTED

def base_price(update, context):
    base = update.message.text
    # Extracting data from context.user_data
    item_name = context.user_data.get("item_name")
    seller = context.user_data.get("user")
    boosted = context.user_data.get("boosted")
    moveset_page = context.user_data.get("moveset_page")
    iv_page = context.user_data.get("iv_page")
    nature = context.user_data.get("nature")
    lv = context.user_data.get("lv")
    details = context.user_data.get("details")
    types = context.user_data.get("type")
    category = context.user_data.get("category")  # Added category variable
    picture = context.user_data.get("picture")

    # Assuming seller is an object with an id attribute
    seller_id = seller.id

    # Create a dictionary to store the seller's data
    seller_data[seller_id] = {}

# Save each variable in the dictionary if it contains data
    seller_data[seller_id]["item_name"] = item_name
    seller_data[seller_id]["seller"] = seller
    seller_data[seller_id]["boosted"] = boosted
    seller_data[seller_id]["moveset_page"] = moveset_page
    seller_data[seller_id]["iv_page"] = iv_page
    seller_data[seller_id]["nature"] = nature
    seller_data[seller_id]["lv"] = lv
    seller_data[seller_id]["details"] = details
    seller_data[seller_id]["types"] = types
    seller_data[seller_id]["category"] = category
    seller_data[seller_id]["picture"] = picture
    seller_data[seller_id]["base_price"] = base
    seller_data[seller_id]["name"] = seller.name

    try:
        number_text = update.message.text
        number = float(number_text[:-1]) * 1000 if number_text[-1].lower() == 'k' else float(number_text)
        if number % 100 == 0:
            if category in ['legendary', 'non-legendary', 'shiny']:
                update.message.reply_text(f"THANK YOU FOR ADD YOUR POKEMON HERE. YOUR {item_name}[{nature}] HAS BEEN SENT FOR SUBMISSION")
                context.user_data["base"] = number
                # Inline options
                inline_keyboard = [
                    [
                        InlineKeyboardButton("Approve", callback_data=f'papprove_{seller_id}'),
                    ],
                    [
                        InlineKeyboardButton("Disapprove:👇", callback_data=f'disapprove_{seller_id}'),
                    ],
                    [
                        InlineKeyboardButton("RIP Nature", callback_data=f'ripnature_{seller_id}'),
                        InlineKeyboardButton("RIP IVs/EVs", callback_data=f'ripivsevs_{seller_id}'),
                    ],
                    [
                        InlineKeyboardButton("Base High", callback_data=f'pbasehigh_{seller_id}'),
                        InlineKeyboardButton("Wrong Information", callback_data=f'pwronginfo_{seller_id}'),
                    ],
                    [
                        InlineKeyboardButton("Useless Poke", callback_data=f'uselesspoke_{seller_id}'),
                        InlineKeyboardButton("Not in Demand", callback_data=f'notindemand_{seller_id}'),
                    ]
                ]

                reply_markup = InlineKeyboardMarkup(inline_keyboard)

                # Sending message with inline options to submission group
                message = context.bot.send_photo(chat_id=SUBMISSION_GROUP_ID, photo=picture, caption=f"""
POKEMON CATEGORY: {category}

POKEMON DETAILS:-

NAME: {item_name}
LEVEL: {lv}
NATURE: {nature}
TYPES: {types}

IV AND EV POINTS:-
{iv_page}

MOVESETS:-
{moveset_page}

BOOSTED: {boosted}
BASE PRICE: {number}

SELLER USERNAME:- {seller.name}
SELLER ID:- {seller.id}
""", reply_markup=reply_markup)

            elif category in ['team', 'tm']:
                update.message.reply_text(f"THANK YOU FOR ADD YOUR {category} HERE. YOUR {category} HAS BEEN SENT FOR SUBMISSION")
                context.user_data["base"] = number
                # Inline options
                Inline_keyboard = [
                    [
                        InlineKeyboardButton("Approve", callback_data=f'tapprove_{seller_id}')
                    ],
                    [
                        InlineKeyboardButton("Disapprove", callback_data=f'disapprove_{seller_id}')
                    ],
                    [
                        InlineKeyboardButton("Wrong Info", callback_data=f'twronginfo_{seller_id}'),
                        InlineKeyboardButton("Useless Team", callback_data=f'uselessteam_{seller_id}')
                    ],
                    [
                        InlineKeyboardButton("Base high", callback_data=f'tbasehigh_{seller_id}'),
                        InlineKeyboardButton("Wrong Display", callback_data=f'wrongdisplay_{seller_id}')
                    ]
                ]
                reply_markup = InlineKeyboardMarkup(Inline_keyboard)
                #send message to submission group
                message = context.bot.send_message(chat_id=SUBMISSION_GROUP_ID, text=f"""
{category.upper()} NAME: {item_name}

{category.upper()} DETAILS:
{details}

BASE PRICE: {number}

SELLER USERNAME: {seller.name}
SELLER ID: {seller.id}
""", reply_markup=reply_markup)

            seller_data[seller_id]["message_id"] = message.message_id
            return ConversationHandler.END
        else:
            update.message.reply_text(f"OUR ADMINS DECIDE THAT BASE PRICE SHOULD BE MULTIPLE OF 100. BUT YOU TELL ({number_text}) IT IS MULTIPLE OF 100. SO IT WILL BE NOT ACCEPTED BY US.")
            return BASE_PRICE
    except ValueError:
        update.message.reply_text("PLEASE WRITE FULL NUMBER OR GIVE IN FORMAT [(number)k]. NO OTHER FORMAT WILL ACCEPT." )
        return BASE_PRICE

def stats(update, context):
    query = update.callback_query
    if query.data.startswith('papprove'):
        stats = "APPROVED"
    elif query.data.startswith('tapprove'):
        stats = "APPROVED"
    else:
        stats = "DISAPPROVED"

    return stats

def submission(update, context):
    query = update.callback_query
    callback_data = query.data
    seller_id = int(callback_data.split('_')[1])
    # Assuming you want to retrieve the data using the variable names
    Stats = stats(update, context)
    seller_name = seller_data[seller_id]["name"]
    item_name = seller_data[seller_id]["item_name"]
    seller = seller_data[seller_id]["seller"]
    boosted = seller_data[seller_id]["boosted"]
    moveset_page = seller_data[seller_id]["moveset_page"]
    iv_page = seller_data[seller_id]["iv_page"]
    nature = seller_data[seller_id]["nature"]
    lv = seller_data[seller_id]["lv"]
    details = seller_data[seller_id]["details"]
    types = seller_data[seller_id]["types"]
    category = seller_data[seller_id]["category"]
    picture = seller_data[seller_id]["picture"]
    base_price = seller_data[seller_id]["base_price"]
    message_id = seller_data[seller_id]["message_id"]

    admin = update.effective_user
    admin_name = admin.name

    query = update.callback_query
    callback_data = query.data

    approved = 'APPROVED'
    disapproved = 'DISAPPROVED'

    pmessage = f"""
POKEMON NAME: {item_name}
LEVEL: {lv}
NATURE: {nature}
TYPES: {types}

IVs AND EVs:
{iv_page}

MOVESETS :
{moveset_page}

Boosted: {boosted}
Base Price: {base_price}
"""

    updated_text = f"""
POKEMON CATEGORY: {category}

POKEMON DETAILS:-

NAME: {item_name}
LEVEL: {lv}
NATURE: {nature}
TYPES: {types}

IV AND EV POINTS:-
{iv_page}

MOVESETS:-
{moveset_page}

BOOSTED: {boosted}
BASE PRICE: {base_price}

SELLER USERNAME:- {seller_name}
SELLER ID:- {seller_id}

IT HAS BEEN {Stats} BY {admin.full_name}({admin_name})
"""

    tupdated_text = f"""
{category.upper()} NAME: {item_name}

{category.upper()} DETAILS:
{details}

BASE PRICE: {base_price}

SELLER USERNAME: {seller_name}
SELLER ID: {seller_id}

It has been {Stats} by {admin.full_name}({admin.name})
"""

    if callback_data.startswith('papprove'):
        context.bot.send_message(chat_id=seller.id, text=f"YOUR {item_name}[LV:{lv} & NATURE:{nature}] HAS BEEN APPROVED FOR NEXT AUCTION.")
        context.bot.send_photo(chat_id=AUCTION_GROUP_ID, photo=picture, caption=f"""
POKEMON DETAILS:

NAME: {item_name}
LEVEL: {lv}
NATURE: {nature}
TYPE: {types}

IVS/EVS:
{iv_page}

MOVESETS:
{moveset_page}

BOOSTED: {boosted}
BASE PRICE: {base_price}
""")
       # Edit the message with the updated text and photo
        context.bot.edit_message_caption(chat_id=update.callback_query.message.chat_id,
                                         message_id=message_id,
                                         caption=updated_text)

        if category == "legendary":
            legendary_list.append(f"{item_name}({nature}): {seller_name}")
        elif category == "non_legendary":
            non_legendary_list.append(f"{item_name}({nature}): {seller_name}")
        elif category == "shiny":
            shiny_list.append(f"{item_name}({nature}): {seller_name}")

    if callback_data.startswith('tapprove'):
        context.bot.send_message(chat_id=seller.id, text=f"YOUR {item_name} HAS BEEN APPROVED FOR NEXT AUCTION.")
        context.bot.send_message(chat_id=AUCTION_GROUP_ID, text=f"""
{category.upper()} NAME: {item_name}

{category.upper()} DETAILS:
{details}

BASE PRICE: {base_price}
""")
        # Edit the message with the updated text and photo
        context.bot.edit_message_text(chat_id=update.callback_query.message.chat_id,
                                      message_id=message_id,
                                      text=tupdated_text)

        if category == "team":
            team_list.append(f"{item_name} Team: {seller_name}")
        elif category == "tm":
            tm_list.append(f"{item_name}: {seller_name}")

    if callback_data.startswith('disapprove'):
        update.callback_query.answer(text="PLEASE CHOOSE ANY REASON FROM BELOW TO DISAPPPROVE.", show_alert=True)

    if callback_data.startswith('ripnature'):
        context.bot.send_message(chat_id=seller_id, text=f"YOUR {item_name}[{nature}] HAS BEEN DISAPPROVED FOR IT'S RIP NATURE")
        # Edit the message with the updated text and photo
        context.bot.edit_message_caption(chat_id=update.callback_query.message.chat_id,
                                         message_id=message_id,
                                         caption=updated_text)

    if callback_data.startswith('ripivsevs'):
        context.bot.send_message(chat_id=seller_id, text=f"YOUR {item_name}[{nature}] HAS BEEN DISAPPROVED FOR IT'S RIP IV/EV")
        # Edit the message with the updated text and photo
        context.bot.edit_message_caption(chat_id=update.callback_query.message.chat_id,
                                         message_id=message_id,
                                         caption=updated_text)

    if callback_data.startswith('uselesspoke'):
        context.bot.send_message(chat_id=seller_id, text=f"YOUR {item_name} HAS BEEN DISAPPROVED BECAUSE IT IS USELESS POKEMON")
        # Edit the message with the updated text and photo
        context.bot.edit_message_caption(chat_id=update.callback_query.message.chat_id,
                                         message_id=message_id,
                                         caption=updated_text)

    if callback_data.startswith('notindemand'):
        context.bot.send_message(chat_id=seller_id, text=f"YOUR {item_name} HAS BEEN DISAPPROVED BECAUSE IT IS NOT IN DEMAND")
        # Edit the message with the updated text and photo
        context.bot.edit_message_caption(chat_id=update.callback_query.message.chat_id,
                                         message_id=message_id,
                                         caption=updated_text)

    if callback_data.startswith('twronginfo'):
        context.bot.send_message(chat_id=seller_id, text=f"YOUR {item_name} HAS BEEN DISAPPROVED BECAUSE YOU GIVE WRONG INFORMATION.")
        # Edit the message with the updated text and photo
        context.bot.edit_message_caption(chat_id=update.callback_query.message.chat_id,
                                         message_id=message_id,
                                         caption=tupdated_text)

    if callback_data.startswith('uselessteam'):
        context.bot.send_message(chat_id=seller_id, text="Your team is disapproved because it is useless")
        # Edit the message with the updated text and photo
        context.bot.edit_message_caption(chat_id=update.callback_query.message.chat_id,
                                         message_id=message_id,
                                         caption=tupdated_text)

    if callback_data.startswith('tbasehigh'):
        context.bot.send_message(chat_id=seller_id, text="Your tm has been disapproved because it's base is too high.")
        # Edit the message with the updated text and photo
        context.bot.edit_message_caption(chat_id=update.callback_query.message.chat_id,
                                         message_id=message_id,
                                         caption=tupdated_text)

    if callback_data.startswith('wrongdisplay'):
        context.bot.send_message(chat_id=seller_id, text=f"Your {item_name} has been disapproved because you give wrong display of it")
        # Edit the message with the updated text and photo
        context.bot.edit_message_caption(chat_id=update.callback_query.message.chat_id,
                                         message_id=message_id,
                                         caption=tupdated_text)

    if callback_data.startswith('pbasehigh'):
        context.bot.send_message(chat_id=seller_id, text=f" Your {item_name} has been disapproved because it's base is too high")
        # Edit the message with the updated text and photo
        context.bot.edit_message_caption(chat_id=update.callback_query.message.chat_id,
                                         message_id=message_id,
                                         caption=updated_text)

    if callback_data.startswith('pwronginfo'):
        context.bot.send_message(chat_id=seller_id, text=f" yYour {item_name} is disapproved because you gave wrong information of it")
        # Edit the message with the updated text and photo
        context.bot.edit_message_caption(chat_id=update.callback_query.message.chat_id,
                                         message_id=message_id,
                                         caption=updated_text)

    del seller_data[seller_id]

# Define the function for handling the /cancel command
def cancel(update, context):
    update.message.reply_text("DONE YOUR RUNNING COMMAND HAS STOPED.")
    return ConversationHandler.END

# AUTO COUNT handler
def auto_count(update, context):
    if update.effective_chat.id == -1002068969951:
       if is_admin(update, context):
           message = update.message.reply_text('•')

           # Define functions for editing message with dots
           def edit_two_dots():
               message.edit_text('••')

           def edit_three_dots():
               message.edit_text('•••')

           def edit_final_message():
               message.edit_text('this item sold')

           # Schedule editing the message with additional dots
           threading.Timer(3, edit_two_dots).start()
           threading.Timer(6, edit_three_dots).start()
           threading.Timer(12, edit_final_message).start()

       else:
           update.message.reply_text("you are not authorized")

# broadcast to all users
def broadcast(update, context):
    user = update.effective_user
    user_id = user.id

    if not is_admin(update, context):
         update.message.reply_text('You are not authorized to use this command.')
         return

    args = context.args
    if not args:
        update.message.reply_text('Please provide a message in the format /broad (message)')
        return

    message_text = ' '.join(args)
    for user_id in USER_LIST:
        context.bot.send_message(chat_id=user_id, text=message_text)

    update.message.reply_text('Broadcast sent to all users.')


# when anyone want to report
def report(update, context):
    user = update.message.from_user

    report_text = ' '.join(context.args)

    if not report_text:
        update.message.reply_text("Please provide a report in the specified format. format is '/report (report_text)'")
        return

    report_message = f'USER NAME - {user.full_name}\nUSER USERNAME - {user.name}\nUSER ID - {user.id}\nREPORT - {report_text}'

    # Forward the report to the bot owner
    context.bot.forward_message(chat_id=REPORT_GROUP_ID, from_chat_id=update.message.chat_id, message_id=update.message.message_id)
    context.bot.send_message(chat_id=REPORT_GROUP_ID, text=report_message)

    update.message.reply_text('Your report has been forwarded to the bot admins.')

# Checking if he is admin
def is_admin(update, context):
    user = update.effective_user
    user_id = str(user.id)

    # checking
    if user_id in ADMIN_ID:
       return True
    if user_id in OWNER_ID.split(','):
       return True
    else:
        return False

# message an user who report
def message_user(update, context):
    user = update.effective_user
    user_id = user.id
    # Check if the user who sent the command is an admin
    if is_admin(update, context):
        try:
            # Extract user ID and message from the command
            user_id = int(context.args[0])
            message = ' '.join(context.args[1:])
        except (ValueError, IndexError):
            update.message.reply_text("Invalid command format. Use /message (user_id) (message)")
            return

        # Send the message to the specified user
        context.bot.send_message(chat_id=user_id, text=message)
        update.message.reply_text("Message sent.")
    else:
        update.message.reply_text("You are not authorized to use this command.")

# check if he is owner
def is_owner(update, context):
    user = update.effective_user
    user_id = str(user.id)

    # checking
    if user_id in OWNER_ID.split(','):
       return True

#prmote to bot admin
def promote_admin(update, context):
    admin_id = update.message.from_user.id

    if not is_owner(update, context):
        update.message.reply_text('You are not authorized to use this command.')
        return

    args = context.args
    if not args:
        update.message.reply_text('please type in format /promote (user id)')
        return

    new_admin_id = str(args[0])
    if new_admin_id not in ADMIN_ID:
        ADMIN_ID.append(new_admin_id)
        update.message.reply_text(f'User {new_admin_id} has been promoted to bot admin.')

#prmote to bot admin
def demote_admin(update, context):
    admin_id = update.message.from_user.id

    if not is_owner(update, context):
        update.message.reply_text('You are not authorized to use this command.')
        return

    args = context.args
    if not args:
        update.message.reply_text('please type in format /demote (user id)')
        return

    new_admin_id = str(args[0])
    if new_admin_id in ADMIN_ID:
        ADMIN_ID.remove(new_admin_id)
        update.message.reply_text(f'User {new_admin_id} has been demoted to bot admin.')

def users(update, context):
    global USER_NAME

    indexed_users = []
    for index, user_name in enumerate(USER_NAME):
        if index == 0:
            indexed_users.append(f"{user_name}")
        else:
            indexed_users.append(f"{index}: {user_name}")
        total_user = index
    # Join the news items into a single string
    users = '\n'.join(indexed_users)
    if is_admin(update, context):
        update.message.reply_text(f"{users}\n\n\nTOTAL USER: {total_user}")
    else:
        update.message.reply_text("you are not authorized to use this command.")

def item_list(update, context):
    legendary = ' '.join(legendary_list)
    non_legendary = ' '.join(non_legendary_list)
    shiny = ' '.join(shiny_list)
    tm = ' '.join(tm_list)
    team = ' '.join(team_list)

    if is_admin(update, context):
       update.message.reply_text(f"""
------Legendary------
{legendary}

------Non-legendary------
{non_legendary}

------Shiny------
{shiny}

------Tms------
{tm}

------Teams------
{team}
""")
    else:
        update.message.reply_text("You are not authorized to run this command.")

def slots(update, context):
    user = update.effective_user
    user_id = user.id

    legendary_num = len(legendary_list)
    non_legendary_num = len(non_legendary_list)
    shiny_num = len(shiny_list)
    tm_num = len(tm_list)
    team_num = len(team_list)



    if is_admin(update, context):
        update.message.reply_text(f"""
LEGENDARY: {legendary_num}/25
Non-legendary: {non_legendary_num}/25
Shiny: {shiny_num}/25
Tm: {tm_num}/25
Team: { team_num}/25
""")
    else:
        update.message.reply_text("you are not authorized.")

def clear(update, context):
    user_id = update.effective_user.id

    if is_owner(update, context):
        legendary_list.clear()
        non_legendary_list.clear()
        shiny_list.clear()
        team_list.clear()
        tm_list.clear()

        del own_dict
        update.message.reply_text("Cleared")
    else:
        update.message.reply_text("You are not authorized to run this command.")
# Set up the conversation handler
conv_handler = ConversationHandler(
    entry_points=[CommandHandler('add', add)],
    states={
        ITEM_NAME: [MessageHandler(Filters.text & ~Filters.command, item_name)],
        NATURE_PAGE: [MessageHandler((Filters.text | Filters.photo) & ~Filters.command, nature_page)],
        ITEM_DETAILS: [MessageHandler(Filters.text & ~Filters.command, item_details)],
        POKEMON_IV: [MessageHandler((Filters.text | Filters.photo) & ~Filters.command, pokemon_iv)],
        MOVESET_PAGE: [MessageHandler((Filters.text | Filters.photo) & ~Filters.command, moveset_page)],
        BOOSTED: [MessageHandler(Filters.text & ~Filters.command, boosted)],
        BASE_PRICE: [MessageHandler(Filters.text & ~Filters.command, base_price)],

    },
    fallbacks=[CommandHandler('cancel', cancel)],
)

# Initialize the Updater and dispatcher
updater = Updater(TOKEN, use_context=True)
dispatcher = updater.dispatcher
dispatcher.add_handler(conv_handler)
submission_pattern = re.compile(r'^disapprove_|^ripnature_|^papprove_|^wrongdisplay_|^tbasehigh_|^uselessteam_|^twronginfo_|^tapprove_|^ripivsevs_|^pbasehigh_|^pwronginfo_|^uselesspoke_|^notindemand_|')

# Add handlers
dispatcher.add_handler(CommandHandler('start', start))
dispatcher.add_handler(CallbackQueryHandler(button_start, pattern='^joined$'))
dispatcher.add_handler(CallbackQueryHandler(category, pattern='^(legendary|non-legendary|shiny|team|tm)$'))
dispatcher.add_handler(CommandHandler('breport', report))
dispatcher.add_handler(CommandHandler('bmessage', message_user))
dispatcher.add_handler(CommandHandler('bpromote', promote_admin))
dispatcher.add_handler(CommandHandler('bdemote', demote_admin))
dispatcher.add_handler(CommandHandler('bbroad', broadcast))
dispatcher.add_handler(CommandHandler('users', users))
dispatcher.add_handler(CommandHandler('list', item_list))
dispatcher.add_handler(CommandHandler('slots', slots))
dispatcher.add_handler(CommandHandler('clear', clear))
dispatcher.add_handler(CallbackQueryHandler(submission, pattern=submission_pattern))
dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command & Filters.regex(r'^\.$'), auto_count))

# Start the bot
updater.start_polling()
updater.idle()

