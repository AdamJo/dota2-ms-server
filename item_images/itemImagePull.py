import requests

def main():
  for item in item_links:
    if item_links[item] != '':
      response = requests.get(item_links[item])
    if response.status_code == 200:
      f = open('E:\\Projects\\dota2-ms-server\\item_images\\items\\{0}.png'.format(item), 'wb')
      f.write(response.content)
      f.close()
    else:
      print('not found')

item_links = {'shadow_amulet': 'http://cdn.dota2.com/apps/dota2/images/items/shadow_amulet_lg.png', 'recipe_magic_wand': 'http://cdn.dota2.com/apps/dota2/images/items/recipe_lg.png', 'mask_of_madness': 'http://cdn.dota2.com/apps/dota2/images/items/mask_of_madness_lg.png', 'recipe_vladmir': 'http://cdn.dota2.com/apps/dota2/images/items/recipe_lg.png', 'skadi': 'http://cdn.dota2.com/apps/dota2/images/items/skadi_lg.png', 'recipe_hurricane_pike': 'http://cdn.dota2.com/apps/dota2/images/items/recipe_lg.png', 'recipe_refresher': 'http://cdn.dota2.com/apps/dota2/images/items/recipe_lg.png', 'soul_booster': 'http://cdn.dota2.com/apps/dota2/images/items/soul_booster_lg.png', 'stout_shield': 'http://cdn.dota2.com/apps/dota2/images/items/stout_shield_lg.png', 'wraith_band': 'http://cdn.dota2.com/apps/dota2/images/items/wraith_band_lg.png', 'recipe_rapier': 'http://cdn.dota2.com/apps/dota2/images/items/recipe_lg.png', 'mekansm': 'http://cdn.dota2.com/apps/dota2/images/items/mekansm_lg.png', 'recipe_octarine_core': 'http://cdn.dota2.com/apps/dota2/images/items/recipe_lg.png', 'dagon_4': 'http://cdn.dota2.com/apps/dota2/images/items/dagon_4_lg.png', 'tome_of_knowledge': 'http://cdn.dota2.com/apps/dota2/images/items/tome_of_knowledge_lg.png', 'recipe_dagon_2': 'http://cdn.dota2.com/apps/dota2/images/items/recipe_lg.png', 'orb_of_venom': 'http://cdn.dota2.com/apps/dota2/images/items/orb_of_venom_lg.png', 'gloves': 'http://cdn.dota2.com/apps/dota2/images/items/gloves_lg.png', 'halloween_rapier': 'http://cdn.dota2.com/apps/dota2/images/items/halloween_rapier_lg.png', 'mjollnir': 'http://cdn.dota2.com/apps/dota2/images/items/mjollnir_lg.png', 'monkey_king_bar': 'http://cdn.dota2.com/apps/dota2/images/items/monkey_king_bar_lg.png', 'winter_coco': 'http://cdn.dota2.com/apps/dota2/images/items/winter_coco_lg.png', 'mystery_hook': 'http://cdn.dota2.com/apps/dota2/images/items/mystery_hook_lg.png', 'cloak': 'http://cdn.dota2.com/apps/dota2/images/items/cloak_lg.png', 'phase_boots': 'http://cdn.dota2.com/apps/dota2/images/items/phase_boots_lg.png', 'recipe_butterfly': 'http://cdn.dota2.com/apps/dota2/images/items/recipe_lg.png', 'recipe_silver_edge': 'http://cdn.dota2.com/apps/dota2/images/items/recipe_lg.png', 'river_painter6': 'http://cdn.dota2.com/apps/dota2/images/items/river_painter6_lg.png', 'bracer': 'http://cdn.dota2.com/apps/dota2/images/items/bracer_lg.png', 'recipe_vanguard': 'http://cdn.dota2.com/apps/dota2/images/items/recipe_lg.png', 'ancient_janggo': 'http://cdn.dota2.com/apps/dota2/images/items/ancient_janggo_lg.png', 'quarterstaff': 'http://cdn.dota2.com/apps/dota2/images/items/quarterstaff_lg.png', 'helm_of_the_dominator': 'http://cdn.dota2.com/apps/dota2/images/items/helm_of_the_dominator_lg.png', 'recipe_satanic': 'http://cdn.dota2.com/apps/dota2/images/items/recipe_lg.png', 'vladmir': 'http://cdn.dota2.com/apps/dota2/images/items/vladmir_lg.png', 'recipe_yasha': 'http://cdn.dota2.com/apps/dota2/images/items/recipe_lg.png', 'tranquil_boots': 'http://cdn.dota2.com/apps/dota2/images/items/tranquil_boots_lg.png', 'dagon_2': 'http://cdn.dota2.com/apps/dota2/images/items/dagon_2_lg.png', 'recipe_assault': 'http://cdn.dota2.com/apps/dota2/images/items/recipe_lg.png', 'satanic': 'http://cdn.dota2.com/apps/dota2/images/items/satanic_lg.png', 'recipe_bracer': 'http://cdn.dota2.com/apps/dota2/images/items/recipe_lg.png', 'recipe_abyssal_blade': 'http://cdn.dota2.com/apps/dota2/images/items/recipe_lg.png', 'winter_cake': 'http://cdn.dota2.com/apps/dota2/images/items/winter_cake_lg.png', 'abyssal_blade': 'http://cdn.dota2.com/apps/dota2/images/items/abyssal_blade_lg.png', 'demon_edge': 'http://cdn.dota2.com/apps/dota2/images/items/demon_edge_lg.png', 'recipe_ancient_janggo': 'http://cdn.dota2.com/apps/dota2/images/items/recipe_lg.png', 'rod_of_atos': 'http://cdn.dota2.com/apps/dota2/images/items/rod_of_atos_lg.png', 'recipe_skadi': 'http://cdn.dota2.com/apps/dota2/images/items/recipe_lg.png', 'buckler': 'http://cdn.dota2.com/apps/dota2/images/items/buckler_lg.png', 'winter_mushroom': 'http://cdn.dota2.com/apps/dota2/images/items/winter_mushroom_lg.png', 'recipe_ethereal_blade': 'http://cdn.dota2.com/apps/dota2/images/items/recipe_lg.png', 'recipe_ring_of_aquila': 'http://cdn.dota2.com/apps/dota2/images/items/recipe_lg.png', 'recipe_necronomicon_2': 'http://cdn.dota2.com/apps/dota2/images/items/recipe_lg.png', 'blade_mail': 'http://cdn.dota2.com/apps/dota2/images/items/blade_mail_lg.png', 'river_painter2': 'http://cdn.dota2.com/apps/dota2/images/items/river_painter2_lg.png', 'aether_lens': 'http://cdn.dota2.com/apps/dota2/images/items/aether_lens_lg.png', 'recipe_black_king_bar': 'http://cdn.dota2.com/apps/dota2/images/items/recipe_lg.png', 'helm_of_iron_will': 'http://cdn.dota2.com/apps/dota2/images/items/helm_of_iron_will_lg.png', 'diffusal_blade': 'http://cdn.dota2.com/apps/dota2/images/items/diffusal_blade_lg.png', 'recipe_oblivion_staff': 'http://cdn.dota2.com/apps/dota2/images/items/recipe_lg.png', 'mystery_toss': 'http://cdn.dota2.com/apps/dota2/images/items/mystery_toss_lg.png', 'recipe_bfury': 'http://cdn.dota2.com/apps/dota2/images/items/recipe_lg.png', 'None': '', 'shivas_guard': 'http://cdn.dota2.com/apps/dota2/images/items/shivas_guard_lg.png', 'recipe_helm_of_the_dominator': 'http://cdn.dota2.com/apps/dota2/images/items/recipe_lg.png', 'recipe_bloodthorn': 'http://cdn.dota2.com/apps/dota2/images/items/recipe_lg.png', 'mystic_staff': 'http://cdn.dota2.com/apps/dota2/images/items/mystic_staff_lg.png', 'boots_of_elves': 'http://cdn.dota2.com/apps/dota2/images/items/boots_of_elves_lg.png', 'dagon': 'http://cdn.dota2.com/apps/dota2/images/items/dagon_lg.png', 'recipe_echo_sabre': 'http://cdn.dota2.com/apps/dota2/images/items/recipe_lg.png', 'javelin': 'http://cdn.dota2.com/apps/dota2/images/items/javelin_lg.png', 'ring_of_regen': 'http://cdn.dota2.com/apps/dota2/images/items/ring_of_regen_lg.png', 'river_painter': 'http://cdn.dota2.com/apps/dota2/images/items/river_painter_lg.png', 'dust': 'http://cdn.dota2.com/apps/dota2/images/items/dust_lg.png', 'winter_greevil_chewy': 'http://cdn.dota2.com/apps/dota2/images/items/winter_greevil_chewy_lg.png', 'blight_stone': 'http://cdn.dota2.com/apps/dota2/images/items/blight_stone_lg.png', 'mantle': 'http://cdn.dota2.com/apps/dota2/images/items/mantle_lg.png', 'recipe_dagon_4': 'http://cdn.dota2.com/apps/dota2/images/items/recipe_lg.png', 'manta': 'http://cdn.dota2.com/apps/dota2/images/items/manta_lg.png', 'blades_of_attack': 'http://cdn.dota2.com/apps/dota2/images/items/blades_of_attack_lg.png', 'recipe_diffusal_blade': 'http://cdn.dota2.com/apps/dota2/images/items/recipe_lg.png', 'recipe_hand_of_midas': 'http://cdn.dota2.com/apps/dota2/images/items/recipe_lg.png', 'recipe_sphere': 'http://cdn.dota2.com/apps/dota2/images/items/recipe_lg.png', 'gauntlets': 'http://cdn.dota2.com/apps/dota2/images/items/gauntlets_lg.png', 'magic_wand': 'http://cdn.dota2.com/apps/dota2/images/items/magic_wand_lg.png', 'bloodthorn': 'http://cdn.dota2.com/apps/dota2/images/items/bloodthorn_lg.png', 'ring_of_health': 'http://cdn.dota2.com/apps/dota2/images/items/ring_of_health_lg.png', 'recipe_cyclone': 'http://cdn.dota2.com/apps/dota2/images/items/recipe_lg.png', 'greevil_whistle': 'http://cdn.dota2.com/apps/dota2/images/items/greevil_whistle_lg.png', 'recipe_travel_boots': 'http://cdn.dota2.com/apps/dota2/images/items/recipe_lg.png', 'recipe_pipe': 'http://cdn.dota2.com/apps/dota2/images/items/recipe_lg.png', 'claymore': 'http://cdn.dota2.com/apps/dota2/images/items/claymore_lg.png', 'bloodstone': 'http://cdn.dota2.com/apps/dota2/images/items/bloodstone_lg.png', 'recipe_bloodstone': 'http://cdn.dota2.com/apps/dota2/images/items/recipe_lg.png', 'river_painter3': 'http://cdn.dota2.com/apps/dota2/images/items/river_painter3_lg.png', 'recipe_necronomicon_3': 'http://cdn.dota2.com/apps/dota2/images/items/recipe_lg.png', 'recipe_null_talisman': 'http://cdn.dota2.com/apps/dota2/images/items/recipe_lg.png', 'yasha': 'http://cdn.dota2.com/apps/dota2/images/items/yasha_lg.png', 'recipe_necronomicon': 'http://cdn.dota2.com/apps/dota2/images/items/recipe_lg.png', 'recipe_mekansm': 'http://cdn.dota2.com/apps/dota2/images/items/recipe_lg.png', 'necronomicon_3': 'http://cdn.dota2.com/apps/dota2/images/items/necronomicon_3_lg.png', 'heavens_halberd': 'http://cdn.dota2.com/apps/dota2/images/items/heavens_halberd_lg.png', 'circlet': 'http://cdn.dota2.com/apps/dota2/images/items/circlet_lg.png', 'recipe_desolator': 'http://cdn.dota2.com/apps/dota2/images/items/recipe_lg.png', 'recipe_tranquil_boots': 'http://cdn.dota2.com/apps/dota2/images/items/recipe_lg.png', 'iron_talon': 'http://cdn.dota2.com/apps/dota2/images/items/iron_talon_lg.png', 'recipe_manta': 'http://cdn.dota2.com/apps/dota2/images/items/recipe_lg.png', 'ring_of_protection': 'http://cdn.dota2.com/apps/dota2/images/items/ring_of_protection_lg.png', 'tango': 'http://cdn.dota2.com/apps/dota2/images/items/tango_lg.png', 'maelstrom': 'http://cdn.dota2.com/apps/dota2/images/items/maelstrom_lg.png', 'winter_kringle': 'http://cdn.dota2.com/apps/dota2/images/items/winter_kringle_lg.png', 'heart': 'http://cdn.dota2.com/apps/dota2/images/items/heart_lg.png', 'relic': 'http://cdn.dota2.com/apps/dota2/images/items/relic_lg.png', 'recipe_pers': 'http://cdn.dota2.com/apps/dota2/images/items/recipe_lg.png', 'enchanted_mango': 'http://cdn.dota2.com/apps/dota2/images/items/enchanted_mango_lg.png', 'winter_greevil_treat': 'http://cdn.dota2.com/apps/dota2/images/items/winter_greevil_treat_lg.png', 'recipe_dragon_lance': 'http://cdn.dota2.com/apps/dota2/images/items/recipe_lg.png', 'force_staff': 'http://cdn.dota2.com/apps/dota2/images/items/force_staff_lg.png', 'recipe_mask_of_madness': 'http://cdn.dota2.com/apps/dota2/images/items/recipe_lg.png', 'clarity': 'http://cdn.dota2.com/apps/dota2/images/items/clarity_lg.png', 'infused_raindrop': 'http://cdn.dota2.com/apps/dota2/images/items/infused_raindrop_lg.png', 'eagle': 'http://cdn.dota2.com/apps/dota2/images/items/eagle_lg.png', 'travel_boots_2': 'http://cdn.dota2.com/apps/dota2/images/items/travel_boots_2_lg.png', 'guardian_greaves': 'http://cdn.dota2.com/apps/dota2/images/items/guardian_greaves_lg.png', 'recipe_ward_dispenser': 'http://cdn.dota2.com/apps/dota2/images/items/recipe_lg.png', 'rapier': 'http://cdn.dota2.com/apps/dota2/images/items/rapier_lg.png', 'butterfly': 'http://cdn.dota2.com/apps/dota2/images/items/butterfly_lg.png', 'blink': 'http://cdn.dota2.com/apps/dota2/images/items/blink_lg.png', 'recipe_dagon': 'http://cdn.dota2.com/apps/dota2/images/items/recipe_lg.png', 'recipe_force_staff': 'http://cdn.dota2.com/apps/dota2/images/items/recipe_lg.png', 'boots': 'http://cdn.dota2.com/apps/dota2/images/items/boots_lg.png', 'recipe_hood_of_defiance': 'http://cdn.dota2.com/apps/dota2/images/items/recipe_lg.png', 'sphere': 'http://cdn.dota2.com/apps/dota2/images/items/sphere_lg.png', 'energy_booster': 'http://cdn.dota2.com/apps/dota2/images/items/energy_booster_lg.png', 'lifesteal': 'http://cdn.dota2.com/apps/dota2/images/items/lifesteal_lg.png', 'recipe_medallion_of_courage': 'http://cdn.dota2.com/apps/dota2/images/items/recipe_lg.png', 'orchid': 'http://cdn.dota2.com/apps/dota2/images/items/orchid_lg.png', 'headdress': 'http://cdn.dota2.com/apps/dota2/images/items/headdress_lg.png', 'blade_of_alacrity': 'http://cdn.dota2.com/apps/dota2/images/items/blade_of_alacrity_lg.png', 'winter_skates': 'http://cdn.dota2.com/apps/dota2/images/items/winter_skates_lg.png', 'recipe_orchid': 'http://cdn.dota2.com/apps/dota2/images/items/recipe_lg.png', 'courier': 'http://cdn.dota2.com/apps/dota2/images/items/courier_lg.png', 'sobi_mask': 'http://cdn.dota2.com/apps/dota2/images/items/sobi_mask_lg.png', 'moon_shard': 'http://cdn.dota2.com/apps/dota2/images/items/moon_shard_lg.png', 'octarine_core': 'http://cdn.dota2.com/apps/dota2/images/items/octarine_core_lg.png', 'reaver': 'http://cdn.dota2.com/apps/dota2/images/items/reaver_lg.png', 'recipe_basher': 'http://cdn.dota2.com/apps/dota2/images/items/recipe_lg.png', 'veil_of_discord': 'http://cdn.dota2.com/apps/dota2/images/items/veil_of_discord_lg.png', 'medallion_of_courage': 'http://cdn.dota2.com/apps/dota2/images/items/medallion_of_courage_lg.png', 'recipe_sheepstick': 'http://cdn.dota2.com/apps/dota2/images/items/recipe_lg.png', 'travel_boots': 'http://cdn.dota2.com/apps/dota2/images/items/travel_boots_lg.png', 'talisman_of_evasion': 'http://cdn.dota2.com/apps/dota2/images/items/talisman_of_evasion_lg.png', 'flask': 'http://cdn.dota2.com/apps/dota2/images/items/flask_lg.png', 'flying_courier': 'http://cdn.dota2.com/apps/dota2/images/items/flying_courier_lg.png', 'ultimate_scepter': 'http://cdn.dota2.com/apps/dota2/images/items/ultimate_scepter_lg.png', 'sange_and_yasha': 'http://cdn.dota2.com/apps/dota2/images/items/sange_and_yasha_lg.png', 'recipe_soul_ring': 'http://cdn.dota2.com/apps/dota2/images/items/recipe_lg.png', 'recipe_armlet': 'http://cdn.dota2.com/apps/dota2/images/items/recipe_lg.png', 'present': 'http://cdn.dota2.com/apps/dota2/images/items/present_lg.png', 'hand_of_midas': 'http://cdn.dota2.com/apps/dota2/images/items/hand_of_midas_lg.png', 'ring_of_basilius': 'http://cdn.dota2.com/apps/dota2/images/items/ring_of_basilius_lg.png', 'void_stone': 'http://cdn.dota2.com/apps/dota2/images/items/void_stone_lg.png', 'recipe_solar_crest': 'http://cdn.dota2.com/apps/dota2/images/items/recipe_lg.png', 'null_talisman': 'http://cdn.dota2.com/apps/dota2/images/items/null_talisman_lg.png', 'belt_of_strength': 'http://cdn.dota2.com/apps/dota2/images/items/belt_of_strength_lg.png', 'faerie_fire': 'http://cdn.dota2.com/apps/dota2/images/items/faerie_fire_lg.png', 'recipe_travel_boots_2': 'http://cdn.dota2.com/apps/dota2/images/items/recipe_lg.png', 'recipe_lotus_orb': 'http://cdn.dota2.com/apps/dota2/images/items/recipe_lg.png', 'halloween_candy_corn': 'http://cdn.dota2.com/apps/dota2/images/items/halloween_candy_corn_lg.png', 'recipe_phase_boots': 'http://cdn.dota2.com/apps/dota2/images/items/recipe_lg.png', 'recipe_buckler': 'http://cdn.dota2.com/apps/dota2/images/items/recipe_lg.png', 'tpscroll': 'http://cdn.dota2.com/apps/dota2/images/items/tpscroll_lg.png', 'recipe_soul_booster': 'http://cdn.dota2.com/apps/dota2/images/items/recipe_lg.png', 'greevil_whistle_toggle': 'http://cdn.dota2.com/apps/dota2/images/items/greevil_whistle_toggle_lg.png', 'banana': 'http://cdn.dota2.com/apps/dota2/images/items/banana_lg.png', 'assault': 'http://cdn.dota2.com/apps/dota2/images/items/assault_lg.png', 'echo_sabre': 'http://cdn.dota2.com/apps/dota2/images/items/echo_sabre_lg.png', 'hyperstone': 'http://cdn.dota2.com/apps/dota2/images/items/hyperstone_lg.png', 'ogre_axe': 'http://cdn.dota2.com/apps/dota2/images/items/ogre_axe_lg.png', 'vanguard': 'http://cdn.dota2.com/apps/dota2/images/items/vanguard_lg.png', 'urn_of_shadows': 'http://cdn.dota2.com/apps/dota2/images/items/urn_of_shadows_lg.png', 'smoke_of_deceit': 'http://cdn.dota2.com/apps/dota2/images/items/smoke_of_deceit_lg.png', 'dragon_lance': 'http://cdn.dota2.com/apps/dota2/images/items/dragon_lance_lg.png', 'armlet': 'http://cdn.dota2.com/apps/dota2/images/items/armlet_lg.png', 'ring_of_aquila': 'http://cdn.dota2.com/apps/dota2/images/items/ring_of_aquila_lg.png', 'recipe_dagon_3': 'http://cdn.dota2.com/apps/dota2/images/items/recipe_lg.png', 'recipe_rod_of_atos': 'http://cdn.dota2.com/apps/dota2/images/items/recipe_lg.png', 'black_king_bar': 'http://cdn.dota2.com/apps/dota2/images/items/black_king_bar_lg.png', 'recipe_monkey_king_bar': 'http://cdn.dota2.com/apps/dota2/images/items/recipe_lg.png', 'recipe_wraith_band': 'http://cdn.dota2.com/apps/dota2/images/items/recipe_lg.png', 'recipe_moon_shard': 'http://cdn.dota2.com/apps/dota2/images/items/recipe_lg.png', 'radiance': 'http://cdn.dota2.com/apps/dota2/images/items/radiance_lg.png', 'power_treads': 'http://cdn.dota2.com/apps/dota2/images/items/power_treads_lg.png', 'vitality_booster': 'http://cdn.dota2.com/apps/dota2/images/items/vitality_booster_lg.png', 'wind_lace': 'http://cdn.dota2.com/apps/dota2/images/items/wind_lace_lg.png', 'ultimate_orb': 'http://cdn.dota2.com/apps/dota2/images/items/ultimate_orb_lg.png', 'recipe_shivas_guard': 'http://cdn.dota2.com/apps/dota2/images/items/recipe_lg.png', 'dagon_5': 'http://cdn.dota2.com/apps/dota2/images/items/dagon_5_lg.png', 'river_painter5': 'http://cdn.dota2.com/apps/dota2/images/items/river_painter5_lg.png', 'lesser_crit': 'http://cdn.dota2.com/apps/dota2/images/items/lesser_crit_lg.png', 'recipe_lesser_crit': 'http://cdn.dota2.com/apps/dota2/images/items/recipe_lg.png', 'recipe_power_treads': 'http://cdn.dota2.com/apps/dota2/images/items/recipe_lg.png', 'recipe_diffusal_blade_2': 'http://cdn.dota2.com/apps/dota2/images/items/recipe_lg.png', 'mystery_arrow': 'http://cdn.dota2.com/apps/dota2/images/items/mystery_arrow_lg.png', 'ward_observer': 'http://cdn.dota2.com/apps/dota2/images/items/ward_observer_lg.png', 'oblivion_staff': 'http://cdn.dota2.com/apps/dota2/images/items/oblivion_staff_lg.png', 'bottle': 'http://cdn.dota2.com/apps/dota2/images/items/bottle_lg.png', 'mithril_hammer': 'http://cdn.dota2.com/apps/dota2/images/items/mithril_hammer_lg.png', 'winter_ham': 'http://cdn.dota2.com/apps/dota2/images/items/winter_ham_lg.png', 'recipe_ultimate_scepter': 'http://cdn.dota2.com/apps/dota2/images/items/recipe_lg.png', 'glimmer_cape': 'http://cdn.dota2.com/apps/dota2/images/items/glimmer_cape_lg.png', 'hood_of_defiance': 'http://cdn.dota2.com/apps/dota2/images/items/hood_of_defiance_lg.png', 'tango_single': 'http://cdn.dota2.com/apps/dota2/images/items/tango_single_lg.png', 'ward_sentry': 'http://cdn.dota2.com/apps/dota2/images/items/ward_sentry_lg.png', 'recipe_ring_of_basilius': 'http://cdn.dota2.com/apps/dota2/images/items/recipe_lg.png', 'desolator': 'http://cdn.dota2.com/apps/dota2/images/items/desolator_lg.png', 'magic_stick': 'http://cdn.dota2.com/apps/dota2/images/items/magic_stick_lg.png', 'recipe_poor_mans_shield': 'http://cdn.dota2.com/apps/dota2/images/items/recipe_lg.png', 'pers': 'http://cdn.dota2.com/apps/dota2/images/items/pers_lg.png', 'invis_sword': 'http://cdn.dota2.com/apps/dota2/images/items/invis_sword_lg.png', 'recipe_greater_crit': 'http://cdn.dota2.com/apps/dota2/images/items/recipe_lg.png', 'sheepstick': 'http://cdn.dota2.com/apps/dota2/images/items/sheepstick_lg.png', 'river_painter7': 'http://cdn.dota2.com/apps/dota2/images/items/river_painter7_lg.png', 'winter_cookie': 'http://cdn.dota2.com/apps/dota2/images/items/winter_cookie_lg.png', 'point_booster': 'http://cdn.dota2.com/apps/dota2/images/items/point_booster_lg.png', 'recipe_maelstrom': 'http://cdn.dota2.com/apps/dota2/images/items/recipe_lg.png', 'solar_crest': 'http://cdn.dota2.com/apps/dota2/images/items/solar_crest_lg.png', 'recipe_glimmer_cape': 'http://cdn.dota2.com/apps/dota2/images/items/recipe_lg.png', 'recipe_dagon_5': 'http://cdn.dota2.com/apps/dota2/images/items/recipe_lg.png', 'arcane_boots': 'http://cdn.dota2.com/apps/dota2/images/items/arcane_boots_lg.png', 'aegis': 'http://cdn.dota2.com/apps/dota2/images/items/aegis_lg.png', 'necronomicon': 'http://cdn.dota2.com/apps/dota2/images/items/necronomicon_lg.png', 'pipe': 'http://cdn.dota2.com/apps/dota2/images/items/pipe_lg.png', 'recipe_aether_lens': 'http://cdn.dota2.com/apps/dota2/images/items/recipe_lg.png', 'chainmail': 'http://cdn.dota2.com/apps/dota2/images/items/chainmail_lg.png', 'soul_ring': 'http://cdn.dota2.com/apps/dota2/images/items/soul_ring_lg.png', 'gem': 'http://cdn.dota2.com/apps/dota2/images/items/gem_lg.png', 'recipe_heart': 'http://cdn.dota2.com/apps/dota2/images/items/recipe_lg.png', 'ward_dispenser': 'http://cdn.dota2.com/apps/dota2/images/items/ward_dispenser_lg.png', 'recipe_sange_and_yasha': 'http://cdn.dota2.com/apps/dota2/images/items/recipe_lg.png', 'necronomicon_2': 'http://cdn.dota2.com/apps/dota2/images/items/necronomicon_2_lg.png', 'recipe_crimson_guard': 'http://cdn.dota2.com/apps/dota2/images/items/recipe_lg.png', 'staff_of_wizardry': 'http://cdn.dota2.com/apps/dota2/images/items/staff_of_wizardry_lg.png', 'ghost': 'http://cdn.dota2.com/apps/dota2/images/items/ghost_lg.png', 'recipe_blade_mail': 'http://cdn.dota2.com/apps/dota2/images/items/recipe_lg.png', 'mystery_vacuum': 'http://cdn.dota2.com/apps/dota2/images/items/mystery_vacuum_lg.png', 'recipe_headdress': 'http://cdn.dota2.com/apps/dota2/images/items/recipe_lg.png', 'quelling_blade': 'http://cdn.dota2.com/apps/dota2/images/items/quelling_blade_lg.png', 'refresher': 'http://cdn.dota2.com/apps/dota2/images/items/refresher_lg.png', 'recipe_iron_talon': 'http://cdn.dota2.com/apps/dota2/images/items/recipe_lg.png', 'recipe_urn_of_shadows': 'http://cdn.dota2.com/apps/dota2/images/items/recipe_lg.png', 'poor_mans_shield': 'http://cdn.dota2.com/apps/dota2/images/items/poor_mans_shield_lg.png', 'recipe_heavens_halberd': 'http://cdn.dota2.com/apps/dota2/images/items/recipe_lg.png', 'recipe_veil_of_discord': 'http://cdn.dota2.com/apps/dota2/images/items/recipe_lg.png', 'recipe_mjollnir': 'http://cdn.dota2.com/apps/dota2/images/items/recipe_lg.png', 'mystery_missile': 'http://cdn.dota2.com/apps/dota2/images/items/mystery_missile_lg.png', 'recipe_sange': 'http://cdn.dota2.com/apps/dota2/images/items/recipe_lg.png', 'dagon_3': 'http://cdn.dota2.com/apps/dota2/images/items/dagon_3_lg.png', 'sange': 'http://cdn.dota2.com/apps/dota2/images/items/sange_lg.png', 'greater_crit': 'http://cdn.dota2.com/apps/dota2/images/items/greater_crit_lg.png', 'platemail': 'http://cdn.dota2.com/apps/dota2/images/items/platemail_lg.png', 'silver_edge': 'http://cdn.dota2.com/apps/dota2/images/items/silver_edge_lg.png', 'winter_stocking': 'http://cdn.dota2.com/apps/dota2/images/items/winter_stocking_lg.png', 'hurricane_pike': 'http://cdn.dota2.com/apps/dota2/images/items/hurricane_pike_lg.png', 'recipe_radiance': 'http://cdn.dota2.com/apps/dota2/images/items/recipe_lg.png', 'lotus_orb': 'http://cdn.dota2.com/apps/dota2/images/items/lotus_orb_lg.png', 'recipe_arcane_boots': 'http://cdn.dota2.com/apps/dota2/images/items/recipe_lg.png', 'branches': 'http://cdn.dota2.com/apps/dota2/images/items/branches_lg.png', 'broadsword': 'http://cdn.dota2.com/apps/dota2/images/items/broadsword_lg.png', 'bfury': 'http://cdn.dota2.com/apps/dota2/images/items/bfury_lg.png', 'diffusal_blade_2': 'http://cdn.dota2.com/apps/dota2/images/items/diffusal_blade_2_lg.png', 'crimson_guard': 'http://cdn.dota2.com/apps/dota2/images/items/crimson_guard_lg.png', 'cyclone': 'http://cdn.dota2.com/apps/dota2/images/items/cyclone_lg.png', 'recipe_invis_sword': 'http://cdn.dota2.com/apps/dota2/images/items/recipe_lg.png', 'ethereal_blade': 'http://cdn.dota2.com/apps/dota2/images/items/ethereal_blade_lg.png', 'river_painter4': 'http://cdn.dota2.com/apps/dota2/images/items/river_painter4_lg.png', 'slippers': 'http://cdn.dota2.com/apps/dota2/images/items/slippers_lg.png', 'basher': 'http://cdn.dota2.com/apps/dota2/images/items/basher_lg.png', 'robe': 'http://cdn.dota2.com/apps/dota2/images/items/robe_lg.png', 'cheese': 'http://cdn.dota2.com/apps/dota2/images/items/cheese_lg.png', 'winter_greevil_garbage': 'http://cdn.dota2.com/apps/dota2/images/items/winter_greevil_garbage_lg.png', 'recipe_guardian_greaves': 'http://cdn.dota2.com/apps/dota2/images/items/recipe_lg.png'}

# dict(zip(arr1, arr2))

main()