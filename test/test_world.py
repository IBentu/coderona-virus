import os
import json
import random
from src.run_utils import INITIAL_DATE 
from src.seir import DiseaseState
from src.simulation.params import Params
from src.simulation.simulation import Simulation
from src.world import Person
from src.world.environments.household import Household
from src.world.population_generation import population_loader
from src.world.population_generation import generate_city
from src.world.world import World

#Test the amount of the  created Immune
def test_createInfectedPersons():
    config_path = os.path.join(os.path.dirname(__file__),"..","src","config.json")
    Expected  = -1
    with open(config_path) as json_data_file:
        ConfigData = json.load(json_data_file)
        paramsDataPath = ConfigData['ParamsFilePath']
    Params.load_from(os.path.join(os.path.dirname(__file__),"..","src", paramsDataPath), override=True)

    kids = [random.randint(0,17) for i in range(5)]    
    adults  = [random.randint(19,40) for i in range(5)]    
    ageList = kids + adults 
    PersonList = list(map(Person, ageList))

    env_arr = []
    my_world = World(
        all_people = PersonList,
        all_environments=env_arr,
        generating_city_name = "test",
        generating_scale = 1)

    my_simulation = Simulation(world = my_world, initial_date= INITIAL_DATE)
    my_simulation.infect_random_set(num_infected = 0, infection_doc = "", per_to_immune = 0.5,city_name = None,min_age=18,people_per_day =5)
    my_simulation.simulate_day()
    #assert events dictionary is not empty
    cnt_immune = 0 
    for person in my_world.all_people():
        if person.get_disease_state() == DiseaseState.IMMUNE:
            cnt_immune = cnt_immune + 1
    per_immune  = cnt_immune / len(PersonList)
    #Assert that the amount of people that created in recovered state are 
    # within 5 percent of expected
    assert abs(per_immune - 0.5)< 0.0005

def test_createInfectedPersons2():
    config_path = os.path.join(os.path.dirname(__file__),"..","src","config.json")
    Expected  = -1
    with open(config_path) as json_data_file:
        ConfigData = json.load(json_data_file)
        paramsDataPath = ConfigData['ParamsFilePath']
    Params.load_from(os.path.join(os.path.dirname(__file__),"..","src", paramsDataPath), override=True)

    kids = [random.randint(0,17) for i in range(5)]    
    adults  = [random.randint(19,40) for i in range(5)]    
    ageList = kids + adults 
    PersonList = list(map(Person, ageList))

    env_arr = []
    my_world = World(
        all_people = PersonList,
        all_environments=env_arr,
        generating_city_name = "test",
        generating_scale = 1)

    my_simulation = Simulation(world = my_world, initial_date= INITIAL_DATE)
    my_simulation.infect_random_set(num_infected = 0, infection_doc = "", per_to_immune = 0.5,city_name = None,min_age=18,people_per_day =1)
    
    #Can't check day by day lots of noise with seir times
    for _ in range(5):
        my_simulation.simulate_day()
    cnt_immune =0 
    for person in my_world.all_people():
        if person.get_disease_state() == DiseaseState.IMMUNE:
            cnt_immune = cnt_immune + 1
    assert cnt_immune <= 5

def test_createInfectedPersonsBestEffort():
    """
    Test that when the population size is less then the amount of people that had been chosen to be infected,
    the simulation doesn't crash 
    """
    config_path = os.path.join(os.path.dirname(__file__),"..","src","config.json")
    with open(config_path) as json_data_file:
        ConfigData = json.load(json_data_file)
        paramsDataPath = ConfigData['ParamsFilePath']
    Params.load_from(os.path.join(os.path.dirname(__file__),"..","src", paramsDataPath), override=True)

    ageList  = [random.randint(19,40) for i in range(10)]    
    PersonList = list(map(Person, ageList))

    env_arr = []
    my_world = World(
        all_people = PersonList,
        all_environments=env_arr,
        generating_city_name = "test",
        generating_scale = 1)

    my_simulation = Simulation(world = my_world, initial_date= INITIAL_DATE)
    my_simulation.infect_random_set(num_infected = 20, infection_doc = "", per_to_immune = 0,city_name = None,min_age=18,people_per_day =0)
    my_simulation.simulate_day()
    cnt_immune = 0 
    cnt_sick = 0 
    for person in my_world.all_people():
        if person.get_disease_state() == DiseaseState.IMMUNE:
            cnt_immune += 1
        else:
            cnt_sick += 1
    assert cnt_immune == 0
    assert cnt_sick == 10

def test_createInfectedPersonsBestEffort2():
    """
    Test that when the population size is less then the amount of people that had been chosen to be infected,
    the simulation doesn't crash 
    """
    config_path = os.path.join(os.path.dirname(__file__),"..","src","config.json")
    with open(config_path) as json_data_file:
        ConfigData = json.load(json_data_file)
        paramsDataPath = ConfigData['ParamsFilePath']
    Params.load_from(os.path.join(os.path.dirname(__file__),"..","src", paramsDataPath), override=True)

    ageList  = [random.randint(19,40) for i in range(10)]    
    PersonList = list(map(Person, ageList))

    env_arr = []
    my_world = World(
        all_people = PersonList,
        all_environments=env_arr,
        generating_city_name = "test",
        generating_scale = 1)

    my_simulation = Simulation(world = my_world, initial_date= INITIAL_DATE)
    my_simulation.infect_random_set(num_infected = 0, infection_doc = "", per_to_immune = 2,city_name = None,min_age=18,people_per_day =0)
    my_simulation.simulate_day()
    cnt_immune = 0 
    cnt_sick = 0 
    for person in my_world.all_people():
        if person.get_disease_state() == DiseaseState.IMMUNE:
            cnt_immune += 1
        else:
            cnt_sick += 1
    assert cnt_immune == 10
    assert cnt_sick == 0


def test_createImmunehouseholds():
    config_path = os.path.join(os.path.dirname(__file__),"..","src","config.json")
    with open(config_path) as json_data_file:
        ConfigData = json.load(json_data_file)
        paramsDataPath = ConfigData['ParamsFilePath']
    Params.load_from(os.path.join(os.path.dirname(__file__),"..","src", paramsDataPath), override=True)

    #create diff enviroments
    KidsHouse = Household(city = None,contact_prob_between_each_two_people=1)
    AdultsHouse = Household(city = None,contact_prob_between_each_two_people=1)
    MixedHouse = Household(city = None,contact_prob_between_each_two_people=1)

    kidsAges = [random.randint(0,17) for i in range(4)]    
    adultsAges  = [random.randint(19,40) for i in range(3)]    
    KidsLst  = list(map(Person, kidsAges))
    adultsLst = list(map(Person, adultsAges))
    persons_arr = KidsLst + adultsLst

    #register people to diff env
    KidsHouse.sign_up_for_today(KidsLst[0],1)
    KidsHouse.sign_up_for_today(KidsLst[1],1)

    AdultsHouse.sign_up_for_today(adultsLst[0],1)
    AdultsHouse.sign_up_for_today(adultsLst[1],1)

    MixedHouse.sign_up_for_today(adultsLst[2],1)
    MixedHouse.sign_up_for_today(KidsLst[2],1)
    MixedHouse.sign_up_for_today(KidsLst[3],1)
    
    assert len(KidsHouse.get_people()) == 2
    assert len(AdultsHouse.get_people()) == 2
    assert len(MixedHouse.get_people()) == 3

    env_arr = [KidsHouse,AdultsHouse,MixedHouse]
    my_world = World(
        all_people = persons_arr,
        all_environments=env_arr,
        generating_city_name = "test",
        generating_scale = 1,)

    my_simulation = Simulation(world = my_world, initial_date= INITIAL_DATE)
    my_simulation.immune_households_infect_others(num_infected = 0, infection_doc = "", per_to_immune = 1,city_name = None,min_age=18,people_per_day= 3 )
    my_simulation.simulate_day()
    #assert events dictionary is not empty
    cnt_immune = 0 
    for person in my_world.all_people():
        if person.get_disease_state() == DiseaseState.IMMUNE:
            cnt_immune = cnt_immune + 1
    assert cnt_immune == 3

def test_createImmunehouseholds2():
    config_path = os.path.join(os.path.dirname(__file__),"..","src","config.json")
    with open(config_path) as json_data_file:
        ConfigData = json.load(json_data_file)
        paramsDataPath = ConfigData['ParamsFilePath']
    Params.load_from(os.path.join(os.path.dirname(__file__),"..","src", paramsDataPath), override=True)

    #create diff enviroments
    KidsHouse = Household(city = None,contact_prob_between_each_two_people=1)
    AdultsHouse = Household(city = None,contact_prob_between_each_two_people=1)
    MixedHouse = Household(city = None,contact_prob_between_each_two_people=1)

    kidsAges = [random.randint(0,17) for i in range(4)]    
    adultsAges  = [random.randint(19,40) for i in range(3)]    
    KidsLst  = list(map(Person, kidsAges))
    adultsLst = list(map(Person, adultsAges))
    persons_arr = KidsLst + adultsLst

    #register people to diff env
    KidsHouse.sign_up_for_today(KidsLst[0],1)
    KidsHouse.sign_up_for_today(KidsLst[1],1)

    AdultsHouse.sign_up_for_today(adultsLst[0],1)
    AdultsHouse.sign_up_for_today(adultsLst[1],1)

    MixedHouse.sign_up_for_today(adultsLst[2],1)
    MixedHouse.sign_up_for_today(KidsLst[2],1)
    MixedHouse.sign_up_for_today(KidsLst[3],1)
    
    assert len(KidsHouse.get_people()) == 2
    assert len(AdultsHouse.get_people()) == 2
    assert len(MixedHouse.get_people()) == 3

    env_arr = [KidsHouse,AdultsHouse,MixedHouse]
    my_world = World(
        all_people = persons_arr,
        all_environments=env_arr,
        generating_city_name = "test",
        generating_scale = 1,)

    my_simulation = Simulation(world = my_world, initial_date= INITIAL_DATE)
    my_simulation.immune_households_infect_others(num_infected = 3, infection_doc = "", per_to_immune = 0.5,city_name = None,min_age=18,people_per_day= 1 )
    cnt_immune = 0 

    my_simulation.simulate_day()
    for person in my_world.all_people():
        if person.get_disease_state() == DiseaseState.IMMUNE:
            cnt_immune = cnt_immune + 1
    assert cnt_immune <= 1

    cnt_immune = 0 
    my_simulation.simulate_day()
    for person in my_world.all_people():
        if person.get_disease_state() == DiseaseState.IMMUNE:
            cnt_immune = cnt_immune + 1
    assert cnt_immune <= 2

    cnt_immune = 0 
    my_simulation.simulate_day()
    for person in my_world.all_people():
        if person.get_disease_state() == DiseaseState.IMMUNE:
            cnt_immune = cnt_immune + 1
    assert cnt_immune <= 3
    
def test_createInfectedPersonsByHouseHoldBestEffort():
    """
    Test that when the population size is less then the amount of people that had been chosen to be infected by households,
    the simulation doesn't crash 
    """
    config_path = os.path.join(os.path.dirname(__file__),"..","src","config.json")
    with open(config_path) as json_data_file:
        ConfigData = json.load(json_data_file)
        paramsDataPath = ConfigData['ParamsFilePath']
    Params.load_from(os.path.join(os.path.dirname(__file__),"..","src", paramsDataPath), override=True)

    #create diff enviroments
    KidsHouse = Household(city = None,contact_prob_between_each_two_people=1)
    AdultsHouse = Household(city = None,contact_prob_between_each_two_people=1)
    MixedHouse = Household(city = None,contact_prob_between_each_two_people=1)

    kidsAges = [random.randint(0,17) for i in range(4)]    
    adultsAges  = [random.randint(19,40) for i in range(3)]    
    KidsLst  = list(map(Person, kidsAges))
    adultsLst = list(map(Person, adultsAges))
    persons_arr = KidsLst + adultsLst

    #register people to diff env
    KidsHouse.sign_up_for_today(KidsLst[0],1)
    KidsHouse.sign_up_for_today(KidsLst[1],1)

    AdultsHouse.sign_up_for_today(adultsLst[0],1)
    AdultsHouse.sign_up_for_today(adultsLst[1],1)

    MixedHouse.sign_up_for_today(adultsLst[2],1)
    MixedHouse.sign_up_for_today(KidsLst[2],1)
    MixedHouse.sign_up_for_today(KidsLst[3],1)
    
    assert len(KidsHouse.get_people()) == 2
    assert len(AdultsHouse.get_people()) == 2
    assert len(MixedHouse.get_people()) == 3

    env_arr = [KidsHouse,AdultsHouse,MixedHouse]
    my_world = World(
        all_people = persons_arr,
        all_environments=env_arr,
        generating_city_name = "test",
        generating_scale = 1,)

    my_simulation = Simulation(world = my_world, initial_date= INITIAL_DATE)
    my_simulation.immune_households_infect_others(num_infected = 20, infection_doc = "", per_to_immune = 0,city_name = None,min_age=18,people_per_day =0)
    my_simulation.simulate_day()
    cnt_immune = 0 
    cnt_sick = 0 
    for person in my_world.all_people():
        if person.get_disease_state() == DiseaseState.IMMUNE:
            cnt_immune += 1
        else:
            cnt_sick += 1
    assert cnt_immune == 0
    assert cnt_sick == 7

def test_createInfectedPersonsByHouseHoldBestEffort2():
    """
    Test that when the population size is less then the amount of people that had been chosen to be infected by households,
    the simulation doesn't crash 
    """
    config_path = os.path.join(os.path.dirname(__file__),"..","src","config.json")
    with open(config_path) as json_data_file:
        ConfigData = json.load(json_data_file)
        paramsDataPath = ConfigData['ParamsFilePath']
    Params.load_from(os.path.join(os.path.dirname(__file__),"..","src", paramsDataPath), override=True)

    #create diff enviroments
    KidsHouse = Household(city = None,contact_prob_between_each_two_people=1)
    AdultsHouse = Household(city = None,contact_prob_between_each_two_people=1)
    MixedHouse = Household(city = None,contact_prob_between_each_two_people=1)

    kidsAges = [random.randint(0,17) for i in range(4)]    
    adultsAges  = [random.randint(19,40) for i in range(3)]    
    KidsLst  = list(map(Person, kidsAges))
    adultsLst = list(map(Person, adultsAges))
    persons_arr = KidsLst + adultsLst

    #register people to diff env
    KidsHouse.sign_up_for_today(KidsLst[0],1)
    KidsHouse.sign_up_for_today(KidsLst[1],1)

    AdultsHouse.sign_up_for_today(adultsLst[0],1)
    AdultsHouse.sign_up_for_today(adultsLst[1],1)

    MixedHouse.sign_up_for_today(adultsLst[2],1)
    MixedHouse.sign_up_for_today(KidsLst[2],1)
    MixedHouse.sign_up_for_today(KidsLst[3],1)
    
    assert len(KidsHouse.get_people()) == 2
    assert len(AdultsHouse.get_people()) == 2
    assert len(MixedHouse.get_people()) == 3

    env_arr = [KidsHouse,AdultsHouse,MixedHouse]
    my_world = World(
        all_people = persons_arr,
        all_environments=env_arr,
        generating_city_name = "test",
        generating_scale = 1,)

    my_simulation = Simulation(world = my_world, initial_date= INITIAL_DATE)
    my_simulation.immune_households_infect_others(num_infected = 0, infection_doc = "", per_to_immune = 2 ,city_name = None,min_age=18,people_per_day =5)
    my_simulation.simulate_day()
    cnt_immune = 0 
    cnt_sick = 0 
    for person in my_world.all_people():
        if person.get_disease_state() == DiseaseState.IMMUNE:
            cnt_immune += 1
        elif person.get_disease_state() != DiseaseState.SUSCEPTIBLE:
            cnt_sick += 1
    assert cnt_immune == 3
    assert cnt_sick == 0