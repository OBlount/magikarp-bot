import requests


# A method to get all gen 1 pokemon from pokeapi.co.
# DOCUMENTATION:
# RETURNS:
# boolean error OR json species
def get_pokemon_species():
    API = "https://pokeapi.co/api/v2/generation/1/"
    print(f"[API] Getting pokemon species from: {API}")
    res = requests.get(API)

    if res.status_code != 200:
        print(f"[API] Failed getting pokemon species from: {API}")
        return False
    else:
        return res.json()["pokemon_species"]


# A method to get the selected pokemon's attributes.
# DOCUMENTATION:
# int pokemon_API_ID
# RETURNS:
# boolean error OR dict attributes
def get_a_pokemons_attributes(pokemon_API_ID):
    API = "https://pokeapi.co/api/v2/pokemon-species/" + str(pokemon_API_ID) + "/"
    print(f"[API] Getting pokemonID {pokemon_API_ID}'s attributes from: {API}")
    res = requests.get(API)

    if res.status_code != 200:
        print(f"[API] Failed getting pokemon's attributes from: {API}")
        return False
    else:
        res_json = res.json()
        return {
            "pokedex_ID":   res_json["pokedex_numbers"][0]["entry_number"],
            "name":         res_json["name"],
            "evolves_from": res_json["evolves_from_species"]
        }


# A method that returns the number of pokemon in gen 1.
# DOCUMENTATION:
# RETURNS:
# boolean error OR int count
def get_pokemon_species_count():
    res = requests.get("https://pokeapi.co/api/v2/generation/1/")

    if res.status_code != 200:
        return False
    else:
        return len(res.json()["pokemon_species"])


# A method that returns the pokedex number given a name.
# DOCUMENTATION:
# string name
# RETURNS:
# boolean error OR int number
def get_pokedexID_from_name(name):
    res = requests.get(f"https://pokeapi.co/api/v2/pokemon/{name}/")

    if res.status_code != 200:
        return False
    else:
        return res.json()["id"]


if __name__ == "__main__":
    pass
