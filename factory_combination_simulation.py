import simpy
import random

unit_made = 0

print(f'STARTING SIMULATION')
print(f'----------------------------------')

#-------------------------------------------------

#Parameters

#total working time (days)
total_time = 180

#containers
material_capacity = 3000
material_treatment_capacity = 3000
parts_processing_capacity = 3000
underframe_assembly_capacity = 3000
roof_assembly_capacity = 3000
total_assembly_capacity = 3000
welding_capacity = 3000
painting_capacity = 3000
renovation_capacity = 3000

#material treatment
num_treatment = 1
mean_treatment = 3.111
std_treatment = 1

#parts processing
num_processing = 1
mean_processing = 3.333
std_processing = 1

#underframe assembly
num_uassembly = 1
mean_uassembly = 5.945
std_uassembly = 2

#roof assembly
num_rassembly = 1
mean_rassembly = 5.945
std_rassembly = 2

#total assembly
num_tassembly = 1
mean_tassembly = 15.444
std_tassembly = 3

#welding
num_welding = 1
mean_welding = 3.233
std_welding = 1

#painting
num_painting = 1
mean_painting = 15.244
std_painting = 3

#renovation
num_renovate = 1
mean_renovate = 30.256
std_renovate = 5

class Mic_factory:
    def __init__(self, env):
        self.material = simpy.Container(env, capacity = material_capacity, init = 1440)
        self.material_treatment = simpy.Container(env, capacity = material_treatment_capacity, init = 0)
        self.parts_processing = simpy.Container(env, capacity = parts_processing_capacity, init = 0)
        self.underframe_assembly = simpy.Container(env, capacity = underframe_assembly_capacity, init = 0)
        self.roof_assembly = simpy.Container(env, capacity = roof_assembly_capacity, init = 0)
        self.total_assembly = simpy.Container(env, capacity = total_assembly_capacity, init = 0)
        self.welding = simpy.Container(env, capacity = welding_capacity, init = 0)
        self.painting = simpy.Container(env, capacity = painting_capacity, init = 0)
        self.renovation = simpy.Container(env, capacity = renovation_capacity, init = 0)

#-------------------------------------------------

def Material(env, mic_factory):
    while True:
        yield env.timeout(0)
        yield mic_factory.material.put(6)

def Mtreatment(env, mic_factory):
    while True:
        yield mic_factory.material.get(3) 
        treatment_time = random.gauss(mean_treatment, std_treatment)
        yield env.timeout(treatment_time)
        yield mic_factory.material_treatment.put(3)

def Pprocessing(env, mic_factory):
    while True:
        yield mic_factory.material.get(3) 
        yield mic_factory.material_treatment.get(3) 
        propcessing_time = random.gauss(mean_processing, std_processing)
        yield env.timeout(propcessing_time)
        yield mic_factory.parts_processing.put(3)

def Uassembly(env, mic_factory):
    while True:
        yield mic_factory.material.get(3) 
        yield mic_factory.material_treatment.get(3) 
        yield mic_factory.parts_processing.get(3) 
        uassembly_time = random.gauss(mean_uassembly, std_uassembly)
        yield env.timeout(uassembly_time)
        yield mic_factory.underframe_assembly.put(3)

def Rassembly(env, mic_factory):
    while True:
        yield mic_factory.material.get(3) 
        yield mic_factory.material_treatment.get(3) 
        yield mic_factory.parts_processing.get(3) 
        rassembly_time = random.gauss(mean_rassembly, std_rassembly)
        yield env.timeout(rassembly_time)
        yield mic_factory.roof_assembly.put(3)

def Tassembly(env, mic_factory):
    while True:
        yield mic_factory.material_treatment.get(6) 
        yield mic_factory.parts_processing.get(6) 
        yield mic_factory.underframe_assembly.get(6) 
        yield mic_factory.roof_assembly.get(6) 
        rassembly_time = random.gauss(mean_tassembly, std_tassembly)
        yield env.timeout(rassembly_time)
        yield mic_factory.total_assembly.put(6)

def Welding(env, mic_factory):
    while True:
        yield mic_factory.total_assembly.get(3) 
        treatment_time = random.gauss(mean_welding, std_welding)
        yield env.timeout(treatment_time)
        yield mic_factory.welding.put(3)

def Painting(env, mic_factory):
    while True:
        yield mic_factory.welding.get(3) 
        treatment_time = random.gauss(mean_painting, std_painting)
        yield env.timeout(treatment_time)
        yield mic_factory.painting.put(3)

def Renovation(env, mic_factory):
    while True:
        yield mic_factory.painting.get(3) 
        treatment_time = random.gauss(mean_renovate, std_renovate)
        yield env.timeout(treatment_time)
        yield mic_factory.renovation.put(3)

#Generators

def material_treatment_gen(env, mic_factory):
    for i in range(num_treatment):
        env.process(Mtreatment(env, mic_factory))
        yield env.timeout(0)

def part_processing_gen(env, mic_factory):
    for i in range(num_processing):
        env.process(Pprocessing(env, mic_factory))
        yield env.timeout(0)

def underframe_assembly_gen(env, mic_factory):
    for i in range(num_uassembly):
        env.process(Uassembly(env, mic_factory))
        yield env.timeout(0)

def roof_assembly_gen(env, mic_factory):
    for i in range(num_rassembly):
        env.process(Rassembly(env, mic_factory))
        yield env.timeout(0)

def total_assembly_gen(env, mic_factory):
    for i in range(num_tassembly):
        env.process(Tassembly(env, mic_factory))
        yield env.timeout(0)

def welding_gen(env, mic_factory):
    for i in range(num_welding):
        env.process(Welding(env, mic_factory))
        yield env.timeout(0)

def painting_gen(env, mic_factory):
    for i in range(num_painting):
        env.process(Painting(env, mic_factory))
        yield env.timeout(0)

def renovation_gen(env, mic_factory):
    for i in range(num_renovate):
        env.process(Renovation(env, mic_factory))
        yield env.timeout(0)

#-------------------------------------------------

env = simpy.Environment()
mic_factory = Mic_factory(env)


treat_gen =  env.process(material_treatment_gen(env, mic_factory))
parts_gen = env.process(part_processing_gen(env, mic_factory))
underframe_gen = env.process(underframe_assembly_gen(env, mic_factory))
roof_gen = env.process(roof_assembly_gen(env, mic_factory))
total_gen = env.process(total_assembly_gen(env, mic_factory))
welding = env.process(welding_gen(env, mic_factory))
painting = env.process(painting_gen(env, mic_factory))
renovation = env.process(renovation_gen(env, mic_factory))

env.run(until = total_time)


print(f'Renovation has %d units ready to go!' % mic_factory.renovation.level)
print(f'----------------------------------')
print(f'SIMULATION COMPLETED')