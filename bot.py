import discord
from discord import app_commands
import os
from dotenv import load_dotenv
import aiohttp
import logging
from datetime import datetime, timedelta

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('F1Bot')

# Load environment variables
load_dotenv()

# API Configuration
OPENF1_API = "https://api.openf1.org/v1"
CURRENT_SEASON = 2025

class F1Bot(discord.Client):
    def __init__(self):
        intents = discord.Intents.default()
        intents.message_content = True
        super().__init__(intents=intents)
        self.tree = app_commands.CommandTree(self)
        self.session = None

    async def setup_hook(self):
        self.session = aiohttp.ClientSession()
        await self.tree.sync()
        logger.info("Commands synced successfully")

    async def close(self):
        if self.session:
            await self.session.close()
        await super().close()

bot = F1Bot()

# ============================================
# 🔧 HELPER FUNCTIONS (API Calls)
# ============================================

async def fetch_api(endpoint, params=None):
    """Fetch data from OpenF1 API"""
    try:
        url = f"{OPENF1_API}/{endpoint}"
        async with bot.session.get(url, params=params, timeout=15) as response:
            if response.status == 200:
                data = await response.json()
                return data
            else:
                logger.error(f"API returned status {response.status}")
                return None
    except Exception as e:
        logger.error(f"API Error: {e}")
        return None

def create_error_embed(message):
    """Create a standard error embed"""
    return discord.Embed(
        title="❌ Erreur",
        description=message,
        color=0xFF0000
    )

# Static F1 2025 Data (since APIs might not have full season data yet)
F1_2025_CALENDAR = [
    {"round": 1, "name": "Australian Grand Prix", "circuit": "Albert Park", "country": "Australia", "city": "Melbourne", "date": "2025-03-16"},
    {"round": 2, "name": "Chinese Grand Prix", "circuit": "Shanghai International Circuit", "country": "China", "city": "Shanghai", "date": "2025-03-23"},
    {"round": 3, "name": "Japanese Grand Prix", "circuit": "Suzuka Circuit", "country": "Japan", "city": "Suzuka", "date": "2025-04-06"},
    {"round": 4, "name": "Bahrain Grand Prix", "circuit": "Bahrain International Circuit", "country": "Bahrain", "city": "Sakhir", "date": "2025-04-13"},
    {"round": 5, "name": "Saudi Arabian Grand Prix", "circuit": "Jeddah Corniche Circuit", "country": "Saudi Arabia", "city": "Jeddah", "date": "2025-04-20"},
    {"round": 6, "name": "Miami Grand Prix", "circuit": "Miami International Autodrome", "country": "USA", "city": "Miami", "date": "2025-05-04"},
    {"round": 7, "name": "Emilia Romagna Grand Prix", "circuit": "Autodromo Enzo e Dino Ferrari", "country": "Italy", "city": "Imola", "date": "2025-05-18"},
    {"round": 8, "name": "Monaco Grand Prix", "circuit": "Circuit de Monaco", "country": "Monaco", "city": "Monte Carlo", "date": "2025-05-25"},
    {"round": 9, "name": "Spanish Grand Prix", "circuit": "Circuit de Barcelona-Catalunya", "country": "Spain", "city": "Barcelona", "date": "2025-06-01"},
    {"round": 10, "name": "Canadian Grand Prix", "circuit": "Circuit Gilles Villeneuve", "country": "Canada", "city": "Montreal", "date": "2025-06-15"},
    {"round": 11, "name": "Austrian Grand Prix", "circuit": "Red Bull Ring", "country": "Austria", "city": "Spielberg", "date": "2025-06-29"},
    {"round": 12, "name": "British Grand Prix", "circuit": "Silverstone Circuit", "country": "Great Britain", "city": "Silverstone", "date": "2025-07-06"},
    {"round": 13, "name": "Belgian Grand Prix", "circuit": "Circuit de Spa-Francorchamps", "country": "Belgium", "city": "Spa", "date": "2025-07-27"},
    {"round": 14, "name": "Hungarian Grand Prix", "circuit": "Hungaroring", "country": "Hungary", "city": "Budapest", "date": "2025-08-03"},
    {"round": 15, "name": "Dutch Grand Prix", "circuit": "Circuit Zandvoort", "country": "Netherlands", "city": "Zandvoort", "date": "2025-08-31"},
    {"round": 16, "name": "Italian Grand Prix", "circuit": "Autodromo Nazionale di Monza", "country": "Italy", "city": "Monza", "date": "2025-09-07"},
    {"round": 17, "name": "Azerbaijan Grand Prix", "circuit": "Baku City Circuit", "country": "Azerbaijan", "city": "Baku", "date": "2025-09-21"},
    {"round": 18, "name": "Singapore Grand Prix", "circuit": "Marina Bay Street Circuit", "country": "Singapore", "city": "Singapore", "date": "2025-10-05"},
    {"round": 19, "name": "United States Grand Prix", "circuit": "Circuit of the Americas", "country": "USA", "city": "Austin", "date": "2025-10-19"},
    {"round": 20, "name": "Mexico City Grand Prix", "circuit": "Autódromo Hermanos Rodríguez", "country": "Mexico", "city": "Mexico City", "date": "2025-10-26"},
    {"round": 21, "name": "São Paulo Grand Prix", "circuit": "Autódromo José Carlos Pace", "country": "Brazil", "city": "São Paulo", "date": "2025-11-09"},
    {"round": 22, "name": "Las Vegas Grand Prix", "circuit": "Las Vegas Street Circuit", "country": "USA", "city": "Las Vegas", "date": "2025-11-22"},
    {"round": 23, "name": "Qatar Grand Prix", "circuit": "Losail International Circuit", "country": "Qatar", "city": "Lusail", "date": "2025-11-30"},
    {"round": 24, "name": "Abu Dhabi Grand Prix", "circuit": "Yas Marina Circuit", "country": "UAE", "city": "Abu Dhabi", "date": "2025-12-07"},
]

F1_2025_DRIVERS = [
    {"number": "1", "name": "Max Verstappen", "team": "Red Bull Racing", "nationality": "Dutch"},
    {"number": "11", "name": "Sergio Pérez", "team": "Red Bull Racing", "nationality": "Mexican"},
    {"number": "44", "name": "Lewis Hamilton", "team": "Ferrari", "nationality": "British"},
    {"number": "16", "name": "Charles Leclerc", "team": "Ferrari", "nationality": "Monégasque"},
    {"number": "4", "name": "Lando Norris", "team": "McLaren", "nationality": "British"},
    {"number": "81", "name": "Oscar Piastri", "team": "McLaren", "nationality": "Australian"},
    {"number": "63", "name": "George Russell", "team": "Mercedes", "nationality": "British"},
    {"number": "17", "name": "Andrea Kimi Antonelli", "team": "Mercedes", "nationality": "Italian"},
    {"number": "14", "name": "Fernando Alonso", "team": "Aston Martin", "nationality": "Spanish"},
    {"number": "18", "name": "Lance Stroll", "team": "Aston Martin", "nationality": "Canadian"},
    {"number": "10", "name": "Pierre Gasly", "team": "Alpine", "nationality": "French"},
    {"number": "31", "name": "Esteban Ocon", "team": "Haas", "nationality": "French"},
    {"number": "27", "name": "Nico Hülkenberg", "team": "Sauber", "nationality": "German"},
    {"number": "77", "name": "Valtteri Bottas", "team": "Sauber", "nationality": "Finnish"},
    {"number": "22", "name": "Yuki Tsunoda", "team": "RB", "nationality": "Japanese"},
    {"number": "21", "name": "Isack Hadjar", "team": "RB", "nationality": "French"},
    {"number": "23", "name": "Alex Albon", "team": "Williams", "nationality": "Thai"},
    {"number": "55", "name": "Carlos Sainz", "team": "Williams", "nationality": "Spanish"},
    {"number": "20", "name": "Kevin Magnussen", "team": "Haas", "nationality": "Danish"},
    {"number": "87", "name": "Jack Doohan", "team": "Alpine", "nationality": "Australian"},
]

# ============================================
# 🏎️ BOT EVENTS
# ============================================

@bot.event
async def on_ready():
    logger.info(f'✅ Bot connecté: {bot.user.name}')
    await bot.change_presence(activity=discord.Game(name=f"/f1 help | Saison {CURRENT_SEASON}"))

# ============================================
# 📨 MAIN COMMAND
# ============================================

@bot.tree.command(name="f1", description=f"Commandes F1 {CURRENT_SEASON}")
@app_commands.describe(commande="Choisis une commande")
@app_commands.choices(commande=[
    app_commands.Choice(name="🏎️ Pilotes", value="pilotes"),
    app_commands.Choice(name="📅 Calendrier", value="calendrier"),
    app_commands.Choice(name="🏆 Classement Pilotes", value="classement"),
    app_commands.Choice(name="🏭 Classement Équipes", value="equipes"),
    app_commands.Choice(name="⏭️ Prochaine Course", value="prochaine"),
    app_commands.Choice(name="🏁 Derniers Résultats", value="resultats"),
    app_commands.Choice(name="❓ Aide", value="help")
])
async def f1_command(interaction: discord.Interaction, commande: str):
    """Main F1 command handler"""
    
    await interaction.response.defer()
    
    commands = {
        "help": show_help,
        "pilotes": get_drivers,
        "calendrier": get_calendar,
        "classement": get_driver_standings,
        "equipes": get_constructor_standings,
        "prochaine": get_next_race,
        "resultats": get_last_results
    }
    
    handler = commands.get(commande)
    if handler:
        await handler(interaction)
    else:
        await interaction.followup.send(embed=create_error_embed("Commande inconnue"))

# ============================================
# 🏎️ PILOTES
# ============================================

async def get_drivers(interaction):
    """Get all drivers for current season"""
    
    embed = discord.Embed(
        title=f"🏎️ PILOTES F1 {CURRENT_SEASON}",
        description=f"Total: {len(F1_2025_DRIVERS)} pilotes",
        color=0x0600EF
    )
    
    # Group by team
    teams = {}
    for driver in F1_2025_DRIVERS:
        team = driver['team']
        if team not in teams:
            teams[team] = []
        teams[team].append(driver)
    
    for team, drivers in teams.items():
        driver_text = "\n".join([
            f"#{d['number']} {d['name']} 🌍 {d['nationality']}"
            for d in drivers
        ])
        embed.add_field(
            name=f"🏎️ {team}",
            value=driver_text,
            inline=True
        )
    
    embed.set_footer(text=f"Saison {CURRENT_SEASON}")
    await interaction.followup.send(embed=embed)

# ============================================
# 📅 CALENDRIER
# ============================================

async def get_calendar(interaction):
    """Get race calendar for current season"""
    
    embed = discord.Embed(
        title=f"📅 CALENDRIER F1 {CURRENT_SEASON}",
        description=f"Total: {len(F1_2025_CALENDAR)} courses",
        color=0xFF1801
    )
    
    now = datetime.now()
    
    for race in F1_2025_CALENDAR:
        race_date = datetime.strptime(race['date'], "%Y-%m-%d")
        
        if race_date < now:
            status = "✅ Terminé"
        elif race_date.date() == now.date():
            status = "🔴 EN COURS"
        else:
            status = "⏳ À venir"
        
        embed.add_field(
            name=f"#{race['round']} - {race['name']}",
            value=f"📍 {race['city']}, {race['country']}\n🏁 {race['circuit']}\n📅 {race['date']}\n{status}",
            inline=True
        )
    
    embed.set_footer(text=f"Saison {CURRENT_SEASON}")
    await interaction.followup.send(embed=embed)

# ============================================
# 🏆 CLASSEMENT PILOTES
# ============================================

async def get_driver_standings(interaction):
    """Get current driver standings from OpenF1 API"""
    
    # Try to get real data from sessions
    sessions = await fetch_api("sessions", {"year": CURRENT_SEASON})
    
    if sessions and len(sessions) > 0:
        # Get the latest session
        latest_session = sessions[-1]
        session_key = latest_session.get('session_key')
        
        # Get driver data for latest session
        drivers_data = await fetch_api("drivers", {"session_key": session_key})
        
        if drivers_data:
            embed = discord.Embed(
                title=f"🏆 PILOTES F1 {CURRENT_SEASON}",
                description=f"Dernière session: {latest_session.get('session_name', 'N/A')}",
                color=0xFFD700
            )
            
            for i, driver in enumerate(drivers_data[:20], 1):
                name = driver.get('full_name', 'N/A')
                team = driver.get('team_name', 'N/A')
                number = driver.get('driver_number', 'N/A')
                
                embed.add_field(
                    name=f"{i}. #{number} {name}",
                    value=f"{team}",
                    inline=True
                )
            
            embed.set_footer(text=f"Données OpenF1 API - Saison {CURRENT_SEASON}")
            await interaction.followup.send(embed=embed)
            return
    
    # Fallback to static list
    embed = discord.Embed(
        title=f"🏆 PILOTES F1 {CURRENT_SEASON}",
        description="Liste des pilotes (classement en direct disponible pendant la saison)",
        color=0xFFD700
    )
    
    for i, driver in enumerate(F1_2025_DRIVERS, 1):
        embed.add_field(
            name=f"{i}. #{driver['number']} {driver['name']}",
            value=f"{driver['team']}",
            inline=True
        )
    
    embed.set_footer(text=f"Saison {CURRENT_SEASON}")
    await interaction.followup.send(embed=embed)

# ============================================
# 🏭 CLASSEMENT CONSTRUCTEURS
# ============================================

async def get_constructor_standings(interaction):
    """Get current constructor standings"""
    
    teams = {}
    for driver in F1_2025_DRIVERS:
        team = driver['team']
        if team not in teams:
            teams[team] = {"drivers": [], "count": 0}
        teams[team]["drivers"].append(driver['name'])
        teams[team]["count"] += 1
    
    embed = discord.Embed(
        title=f"🏭 ÉQUIPES F1 {CURRENT_SEASON}",
        description=f"Total: {len(teams)} équipes",
        color=0x00D2BE
    )
    
    for i, (team, data) in enumerate(teams.items(), 1):
        drivers_text = "\n".join(data["drivers"])
        embed.add_field(
            name=f"{i}. {team}",
            value=f"👥 {drivers_text}",
            inline=True
        )
    
    embed.set_footer(text=f"Saison {CURRENT_SEASON}")
    await interaction.followup.send(embed=embed)

# ============================================
# ⏭️ PROCHAINE COURSE
# ============================================

async def get_next_race(interaction):
    """Get next race information"""
    
    now = datetime.now()
    
    next_race = None
    for race in F1_2025_CALENDAR:
        race_date = datetime.strptime(race['date'], "%Y-%m-%d")
        if race_date >= now:
            next_race = race
            break
    
    if not next_race:
        embed = discord.Embed(
            title="🏁 SAISON TERMINÉE",
            description="Toutes les courses de la saison sont terminées !",
            color=0xFFD700
        )
        await interaction.followup.send(embed=embed)
        return
    
    race_date = datetime.strptime(next_race['date'], "%Y-%m-%d")
    days_until = (race_date - now).days
    
    embed = discord.Embed(
        title="⏭️ PROCHAINE COURSE",
        description=f"**{next_race['name']}**",
        color=0x0090FF
    )
    
    embed.add_field(name="🏁 Circuit", value=next_race['circuit'], inline=False)
    embed.add_field(name="📍 Lieu", value=f"{next_race['city']}, {next_race['country']}", inline=True)
    embed.add_field(name="📅 Date", value=next_race['date'], inline=True)
    embed.add_field(name="🔢 Round", value=next_race['round'], inline=True)
    embed.add_field(name="⏳ Dans", value=f"{days_until} jour(s)", inline=True)
    
    embed.set_footer(text=f"Saison {CURRENT_SEASON}")
    await interaction.followup.send(embed=embed)

# ============================================
# 🏁 DERNIERS RÉSULTATS
# ============================================

async def get_last_results(interaction):
    """Get last race results from OpenF1 API"""
    
    # Get latest race sessions
    sessions = await fetch_api("sessions", {"year": CURRENT_SEASON, "session_name": "Race"})
    
    if not sessions or len(sessions) == 0:
        await interaction.followup.send(embed=create_error_embed("Aucune course terminée pour le moment"))
        return
    
    # Get the most recent completed race
    latest_race = sessions[-1]
    session_key = latest_race.get('session_key')
    
    # Get position data
    positions = await fetch_api("position", {"session_key": session_key})
    
    if not positions:
        await interaction.followup.send(embed=create_error_embed("Impossible de récupérer les résultats"))
        return
    
    # Get unique drivers and their final positions
    drivers_final = {}
    for pos in positions:
        driver_num = pos.get('driver_number')
        position = pos.get('position')
        if driver_num and position:
            drivers_final[driver_num] = position
    
    # Sort by position
    sorted_drivers = sorted(drivers_final.items(), key=lambda x: x[1])
    
    embed = discord.Embed(
        title=f"🏁 {latest_race.get('meeting_name', 'Dernière Course')}",
        description=f"📅 {latest_race.get('date_start', 'N/A')[:10]}",
        color=0xFF1801
    )
    
    medals = ["🥇", "🥈", "🥉"]
    
    for i, (driver_num, position) in enumerate(sorted_drivers[:10]):
        # Find driver name
        driver_info = next((d for d in F1_2025_DRIVERS if d['number'] == str(driver_num)), None)
        driver_name = driver_info['name'] if driver_info else f"Driver #{driver_num}"
        team = driver_info['team'] if driver_info else "N/A"
        
        medal = medals[i] if i < 3 else ""
        
        embed.add_field(
            name=f"{medal} {position}. {driver_name}",
            value=team,
            inline=True
        )
    
    embed.set_footer(text=f"Circuit: {latest_race.get('circuit_short_name', 'N/A')}")
    await interaction.followup.send(embed=embed)

# ============================================
# ❓ AIDE
# ============================================

async def show_help(interaction):
    """Show help message"""
    embed = discord.Embed(
        title=f"🏎️ BOT F1 {CURRENT_SEASON} - AIDE",
        description="Bot F1 avec données en temps réel via OpenF1 API",
        color=0xFF1801
    )
    
    commands = [
        ("🏎️ Pilotes", "Liste de tous les pilotes par équipe"),
        ("📅 Calendrier", "Calendrier complet avec statut des courses"),
        ("🏆 Classement Pilotes", "Liste des pilotes actifs"),
        ("🏭 Classement Équipes", "Liste des équipes et leurs pilotes"),
        ("⏭️ Prochaine Course", "Informations sur la prochaine course"),
        ("🏁 Derniers Résultats", "Résultats de la dernière course")
    ]
    
    for name, description in commands:
        embed.add_field(name=name, value=description, inline=False)
    
    embed.add_field(
        name="📡 Source",
        value="Données via [OpenF1 API](https://openf1.org)",
        inline=False
    )
    
    embed.set_footer(text=f"Saison {CURRENT_SEASON} | Données en temps réel")
    await interaction.followup.send(embed=embed)

# ============================================
# 🚀 LAUNCH BOT
# ============================================

if __name__ == "__main__":
    token = os.getenv('DISCORD_TOKEN')
    if token:
        try:
            bot.run(token)
        except KeyboardInterrupt:
            logger.info("Bot arrêté manuellement")
        except Exception as e:
            logger.error(f"Erreur fatale: {e}")
    else:
        logger.error("❌ DISCORD_TOKEN introuvable dans .env")
