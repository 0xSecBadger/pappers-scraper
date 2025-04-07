import argparse
import json
import pandas as pd
from colorama import init, Fore, Style, Back
import asyncio
from pyppeteer import launch
import random
from urllib.parse import quote
import time
import logging
from tabulate import tabulate

# Initialize colorama for cross-platform colored output
init()

# Configure logging with colors
class ColoredFormatter(logging.Formatter):
    def format(self, record):
        if record.levelno == logging.INFO:
            record.msg = f"{Fore.CYAN}{record.msg}{Style.RESET_ALL}"
        elif record.levelno == logging.WARNING:
            record.msg = f"{Fore.YELLOW}{record.msg}{Style.RESET_ALL}"
        elif record.levelno == logging.ERROR:
            record.msg = f"{Fore.RED}{record.msg}{Style.RESET_ALL}"
        return super().format(record)

logger = logging.getLogger(__name__)
handler = logging.StreamHandler()
handler.setFormatter(ColoredFormatter('%(message)s'))
logger.addHandler(handler)
logger.setLevel(logging.INFO)

def parse_arguments():
    """Parse command line arguments"""
    parser = argparse.ArgumentParser(description="Recherche d'entreprises sur pappers.fr")
    parser.add_argument('query', type=str, help="Nom de l'entreprise à rechercher")
    parser.add_argument('--tab', action='store_true', help="Afficher les résultats sous forme de tableau")
    return parser.parse_args()

def format_date(date_str):
    """Format a date string to French format"""
    if not date_str:
        return "Non renseignée"
    try:
        year, month, day = date_str.split('-')
        return f"{day}/{month}/{year}"
    except:
        return date_str

def format_status(status):
    """Format company status with color"""
    if status == "Active":
        return f"{Fore.GREEN}●{Style.RESET_ALL} Active"
    return f"{Fore.RED}●{Style.RESET_ALL} Fermée"

def truncate_text(text, max_length=50):
    """Truncate text to max_length and add ellipsis if necessary"""
    if not text:
        return "N/A"
    if len(text) <= max_length:
        return text
    return text[:max_length-3] + "..."

def display_table(results):
    """Display results in a professional table format"""
    # Prepare data for tabulate
    table_data = []
    headers = [
        "№", "Nom", "SIREN", "Statut", "Forme juridique", 
        "Création", "Activité", "Siège", "Dirigeants"
    ]
    
    for idx, result in enumerate(results, 1):
        status = "🟢 Active" if result['statut'] == "Active" else "🔴 Fermée"
        row = [
            idx,
            truncate_text(result['nom'], 30),
            result['siren'],
            status,
            truncate_text(result['forme_juridique'], 20),
            format_date(result['date_creation']),
            truncate_text(result['activite'], 30),
            truncate_text(result['siege'], 30),
            truncate_text(', '.join(result['dirigeants']), 30)
        ]
        table_data.append(row)
    
    # Create and print the table
    print(f"\n{Fore.WHITE}{Back.GREEN} 📊 Résultats détaillés ({len(results)} entreprises) {Style.RESET_ALL}\n")
    
    table = tabulate(
        table_data,
        headers=headers,
        tablefmt="fancy_grid",
        numalign="center",
        stralign="left"
    )
    
    print(table)

class PappersScraper:
    def __init__(self):
        self.base_url = "https://www.pappers.fr"
        self.api_url = "https://api.pappers.fr/v2"
        self.api_token = "97a405f1664a83329a7d89ebf51dc227b90633c4ba4a2575"
        self.browser = None
        self.page = None

    async def init(self):
        self.browser = await launch(
            headless=True,
            args=['--no-sandbox', '--disable-setuid-sandbox']
        )
        self.page = await self.browser.newPage()
        await self.page.setViewport({'width': 1920, 'height': 1080})
        await self.page.setUserAgent('Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36')

    async def close(self):
        if self.browser:
            await self.browser.close()

    async def search(self, query):
        logger.info(f"\n🔍 Recherche pour : {Fore.WHITE}{Back.BLUE} {query} {Style.RESET_ALL}\n")
        
        encoded_query = quote(query)
        api_url = f"{self.api_url}/recherche"
        params = {
            'q': query,
            'api_token': self.api_token,
            'precision': 'standard',
            'bases': 'entreprises,dirigeants,publications',
            'page': 1,
            'par_page': 20,
            'case_sensitive': False
        }

        results = []
        page = 1
        has_more = True

        while has_more:
            logger.info(f"📃 Chargement de la page {page}...")
            params['page'] = page

            response = await self.page.evaluate('''
                async (url, params) => {
                    const queryString = new URLSearchParams(params).toString();
                    const response = await fetch(`${url}?${queryString}`);
                    return await response.json();
                }
            ''', api_url, params)

            if not response or 'resultats' not in response:
                logger.warning("⚠️  Erreur lors de la récupération des résultats")
                break
                    
            current_results = response.get('resultats', [])
            if not current_results:
                logger.warning(f"⚠️  Aucun résultat sur la page {page}")
                break
            
            for result in current_results:
                company_data = {
                    'nom': result.get('nom_entreprise'),
                    'siren': result.get('siren'),
                    'statut': 'Active' if result.get('statut') == 'Active' else 'Fermée',
                    'forme_juridique': result.get('forme_juridique'),
                    'date_creation': result.get('date_creation'),
                    'activite': result.get('libelle_code_naf'),
                    'siege': result.get('siege', {}).get('adresse_ligne_1'),
                    'dirigeants': [d.get('nom_complet') for d in result.get('dirigeants', [])]
                }
                results.append(company_data)
                logger.info(f"📎 Entreprise trouvée : {Fore.CYAN}{company_data['nom']}{Style.RESET_ALL}")

            total_results = response.get('total', 0)
            current_page = response.get('page', 1)
            total_pages = (total_results + params['par_page'] - 1) // params['par_page']

            if current_page >= total_pages:
                has_more = False
            else:
                page += 1
                await asyncio.sleep(random.uniform(1, 2))

        if not results:
            logger.warning("⚠️  Aucun résultat trouvé")
        else:
            logger.info(f"\n✅ {len(results)} entreprise(s) trouvée(s)")

        return results

def display_company_info(idx, total, result):
    """Display formatted company information"""
    # Header with company name and basic info
    print(f"\n{Fore.WHITE}{Back.BLUE} {idx}/{total} {result['nom']} {Style.RESET_ALL}")
    
    # Status and SIREN
    print(f"\n{Fore.YELLOW}État & Identité{Style.RESET_ALL}")
    print(f"├─ Statut    : {format_status(result['statut'])}")
    print(f"├─ SIREN     : {result['siren']}")
    print(f"└─ Création  : {format_date(result['date_creation'])}")
    
    # Legal form and activity
    if result['forme_juridique'] or result['activite']:
        print(f"\n{Fore.YELLOW}Informations juridiques{Style.RESET_ALL}")
        if result['forme_juridique']:
            print(f"├─ Forme     : {result['forme_juridique']}")
        if result['activite']:
            print(f"└─ Activité  : {result['activite']}")
    
    # Address
    if result['siege']:
        print(f"\n{Fore.YELLOW}Localisation{Style.RESET_ALL}")
        print(f"└─ Siège     : {result['siege']}")
    
    # Directors
    if result['dirigeants']:
        print(f"\n{Fore.YELLOW}Direction{Style.RESET_ALL}")
        for i, dirigeant in enumerate(result['dirigeants'], 1):
            prefix = "└─" if i == len(result['dirigeants']) else "├─"
            print(f"{prefix} Dirigeant : {dirigeant}")

async def main():
    args = parse_arguments()
    scraper = PappersScraper()
    
    try:
        await scraper.init()
        results = await scraper.search(args.query)
        
        if results:
            if args.tab:
                display_table(results)
            else:
                for idx, result in enumerate(results, 1):
                    display_company_info(idx, len(results), result)
    except Exception as e:
        logger.error(f"Une erreur est survenue : {e}")
    finally:
        await scraper.close()

if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(main())